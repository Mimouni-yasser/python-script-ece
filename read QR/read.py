import cv2
import numpy as np
import urllib.request
import pymongo
from time import sleep
from bson.objectid import ObjectId
import sys

def read_qr_code(img):
    try:
        detect = cv2.QRCodeDetector()
        value, points, straight_qrcode = detect.detectAndDecode(img)
        return value
    except:
        return None


# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
collection = client.local[sys.argv[1] if len(sys.argv) > 1 else "ECE"]
data = collection.find({})

while True:
    req = urllib.request.urlopen('http://192.168.1.19:8080/shot.jpg')
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    img = cv2.imdecode(arr, -1) # 'Load it as it is'
    value = read_qr_code(img)
    if value != "" and value != None:
        #cv2.imshow('random_title', img)
        #get the student name from the QR code
        print(value)
        email = collection.find_one({"_id": ObjectId(value)})["email "]
        print(email)
    else:
        pass
