FIRST_NAME = "Jerome"
LAST_NAME = "Lee"
INDEX = "P0012"
PP_IMG_PATH = "C:/Users/milla/Desktop/digital-eyeball-v2/dataset/jerome/jerome1.jpg"

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import base64

# Fetch the service account key JSON file contents
cred = credentials.Certificate("PUT YOUR CRED JSON PATH HERE")

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': "PUT YOUR URL HERE"
})

# As an admin, the app has access to read and write all data, regradless of Security Rules
ref = db.reference('trainedFaces')

ref.update({ INDEX : {
            "firstName": FIRST_NAME,
            "image": "",
            "lastName" : LAST_NAME
        }})

with open( PP_IMG_PATH, "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())
    ref.child(INDEX).child("image").set("data:image/jpeg;base64," + encoded_string.decode("utf-8"))


ref = db.reference('lastSeen')

iniarray = []

for x in range(4):
    iniarray.append({
        "image": "",
        "location": "L0001",
        "time": "2000-07-05 14:56:54.807" + str(x) + str(x) + str(x)
         })
    
print(iniarray)

ref.child(INDEX).set(iniarray)
    


print("write complete")

