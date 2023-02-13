import sys
import os
import pandas as pd
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import json
import yagmail


class style():
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    BOLD = '\033[1m'
    WHITE  = '\33[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

def check_call():
    if(len(sys.argv) == 2):
        print(style.RED+"[!] - " + style.RESET + "using preexisting data on MongoDB")
        return True
    elif(len(sys.argv) < 3):
        print(style.RED+"[!] - " + style.RESET + "Usage: python3 main.py <file> <collection>")
        exit()
    else:
        print(style.RED+"[+] - " + style.RESET + "File: " + sys.argv[1])
        print(style.RED+"[+] - " + style.RESET + "checking if file exists & is xlsx format...")
        if(os.path.exists(sys.argv[1]) and sys.argv[1].endswith(".xlsx")):
            print(style.RED+"[+] - " + style.RESET + "File exists.")
            print(style.RED+"[+] - " + style.RESET + "Done.")
        else:
            print(style.RED+"[!] - " + style.RESET + "File does not exist OR is not the correct format. Exiting...")
            exit()
        return False
def check_file():
    excel_data = pd.read_excel(sys.argv[1], sheet_name='Form Responses 1', dtype={'nom ': str, 'num': str})
    if(excel_data.empty):
        print(style.RED+"[!] - " + style.RESET + "File is empty. Exiting...")
        exit()
    if(excel_data is None):
        print(style.RED+"[!] - " + style.RESET + "error reading file. Exiting...")
        exit()
    data = excel_data.to_json(orient='records')
    if(data is None):
        print(style.RED+"[!] - " + style.RESET + "error converting file to json. Exiting...")
        exit()
    return json.loads(data)

def setup_mongo(collection: str):
    client = MongoClient('localhost', 27017)
    return client.local[collection]

if(__name__ == "__main__"):
    print(style.RED+"""
     _____ _____  _____            _____ _   _  _____  ___  ___  ___  ___  
    |  ___/  __ \|  ___|          |  ___| \ | |/  ___|/ _ \ |  \/  | / _ \ 
    | |__ | /  \/| |__    ______  | |__ |  \| |\ `--./ /_\ \| .  . |/ /_\ \ 
    |  __|| |    |  __|  |______| |  __|| . ` | `--. \  _  || |\/| ||  _  |
    | |___| \__/\| |___           | |___| |\  |/\__/ / | | || |  | || | | |
    \____/ \____/\____/           \____/\_| \_/\____/\_| |_/\_|  |_/\_| |_/                                                                                                                                                                                       
        """+style.RESET)
    pre = check_call()
    if(not pre):
        print(style.RED+"[+] - " + style.RESET + "Reading file...")
        data_json = check_file()
        print(style.RED+"[+] - " + style.RESET + "Done.")
        print(style.RED+"[+] - " + style.RESET + "Connecting to MongoDB...")
        collection = setup_mongo(sys.argv[2])
        print(style.RED+"[+] - " + style.RESET + "Done.")
        print(style.RED+"[+] - " + style.RESET + "Inserting data into MongoDB...")
        collection.insert_many(data_json)
        collection.update_many({}, {'$set': {'present': False}})
        print(style.RED+"[+] - " + style.RESET + "Done.")
    else:
        print(style.RED+"[+] - " + style.RESET + "Connecting to MongoDB & getting collection {}..." .format(sys.argv[1]))
        collection = setup_mongo(sys.argv[1])
        print(style.RED+"[+] - " + style.RESET + "Done.")
        if(input(style.RED+"[?] - do you want to generate the QR codes? [y/n]: " + style.RESET) == 'y'):
            print(style.RED+"[+] - " + style.RESET + "Generating QR codes...")
            i = 0
            for id in collection.find({}):
                i += 1
                print(style.RED+"[+] - " + style.RESET + "Generating QR code for {} ({}/{})" .format(id['nom '], i, collection.count_documents({})) )
                os.system("python3 \"generate QR\gen.py\" " + str(id['_id']) + "> NUL")
            print(style.RED+"[+] - " + style.RESET + "Done, QRs generated.")
        done = False
        while not done:
            print(style.BLUE + style.BOLD + "\t please chose one of the following options:" + style.RESET)
            print(style.BLUE + style.BOLD + "\t\t 1- show all data" + style.RESET)
            print(style.BLUE + style.BOLD + "\t\t 2- Bulk Email" + style.RESET)
            print(style.BLUE + style.BOLD + "\t\t 3- drop database" + style.RESET)
            print(style.BLUE + style.BOLD + "\t\t 4- exit" + style.RESET)
            while True:
                choice = int(input(style.BOLD + style.GREEN + "please enter your choice: [1..4]: " + style.RESET))
                if(choice > 0 and choice < 5):
                    break
                else:
                    print(style.RED + "please enter a valid choice" + style.RESET)
            if(choice == 1):
                print(style.RED + "showing all data" + style.RESET)
                for x in collection.find():
                    print(style.YELLOW + style.BOLD + "name: " + style.RESET + x['nom ']+" "+style.YELLOW + style.BOLD + " email: " + style.RESET + x['email '])
            elif(choice == 2):
                print(style.RED + "sending bulk email" + style.RESET)
                for x in collection.find():
                    print(style.YELLOW + style.BOLD + "name: " + style.RESET + x['nom ']+" "+style.YELLOW + style.BOLD + " email: " + style.RESET + x['email '])
                    print(style.RED + "sending email to: " + x['email '] + style.RESET)
                    print(x['email '])
            elif(choice == 3):
                print(style.RED + style.BOLD + "WARNING: " + "this will drop the database"+ style.RESET)
                answr = input(style.RED + "are you sure you want to drop the database? [y/n]: " + style.RESET)
                if(answr == 'y' or answr == 'Y'):
                    print(style.RED + "dropping database" + style.RESET)
                    collection.drop()
                else:
                    continue
            elif(choice == 4):
                print(style.RED + "exiting..." + style.RESET)
                done = True
                break
            elif(choice == 2):
                print(style.RED + "connecting to email server" + style.RESET)
                yag = yagmail.SMTP("yasmimouni2", "msgppgzwxuxoesix")

