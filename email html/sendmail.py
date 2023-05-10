import yagmail
import pymongo

import re

regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

def isValid(email):
    if re.fullmatch(regex, email):
        print("Valid email")
        return True
    else:
        print("Invalid email")
        return False

#setup yagmail client
c = yagmail.SMTP("ensam.career.expo@gmail.com", "wqpsawkfpmnlyaom")

#setup connection to mongodb
client = pymongo.MongoClient("mongodb://localhost:27017/")
database = client["local"]
collection = database["ECE_col"]

content = "<html><body><h>bonsoir, ci join votre E-badge personaliser. merci de la presenter demain matin lors de check in </h></body></html>"
invalid = list()
send = 0
i=0
for id in collection.find({}):
    i=i+1
    if(id['apogee'] == 1924577):
        send = 1
    if(send == 1):
        if(isValid(id['email']) == False):
            invalid.append(id['email'])
            continue
        c.send(to=id['email'], subject="invitation", contents=content, attachments="./PDF_"+str(id["_id"])+".pdf")
        print(f"{i} / {collection.count_documents({})}sending mail to {id['email']}")
        