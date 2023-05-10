import pymongo
import pdfkit


#read html file


#setup connection to mongodb
client = pymongo.MongoClient("mongodb://localhost:27017/")
database = client["local"]
collection = database["ECE_col"]
i=0
f = open("index.html", "r")
content = f.read()
work = 0
#print(content)
for id in collection.find({}):
    i=i+1
    if(id['apogee'] == 1924577):
        work = 1
    if(work == 1):
        tmp = content.replace("//NAME_TO_REPLACE//", id["name "])
        tmp = tmp.replace("//SOURCE_TO_REPLACE//", "./QR/qr_"+str(id["_id"])+".png")
        f_mail = open("mail.html", "w")
        f_mail.write(tmp)
        pdfkit.from_file("mail.html", "PDF_"+str(id["_id"])+".pdf")    
        print(f"({i}/+{collection.count_documents({})} generating pdf for {id['_id']}")

