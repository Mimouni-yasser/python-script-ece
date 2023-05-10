import pandas as pd
import json
import sys
import pymongo


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



excel_data = pd.read_excel(sys.argv[1], sheet_name='form', dtype={"num": str})
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
data_json = json.loads(data)
# with open('data.json', 'w', ) as f:
#     
#     for line in data_json:
#         f.write(f"{line}\n")
#     f.close()
database = pymongo.MongoClient("mongodb://localhost:27017/")['local']
collection = database['ECE_col']
collection.insert_many(data_json)
collection.update_many({}, {'$set': {'present': False}})