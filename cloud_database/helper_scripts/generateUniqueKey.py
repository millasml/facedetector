import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import datetime

# Fetch the service account key JSON file contents
cred = credentials.Certificate("PUT YOUR CRED JSON PATH HERE")

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': "PUT YOUR URL HERE"
})

# As an admin, the app has access to read and write all data, regradless of Security Rules
ref = db.reference('lastSeen')


face_to_index = {
    "milla" : "P0001",
    "cs" : "P0002",
    "brandon" : "P0003",
    "james" : "P0004",
    "alex" : "P0005",
    "celeste" : "P0006",
    "roy" : "P0007",
    "akbar": "P0008",
    "gabriel": "P0009",
    "caroline": "P0010",
    "tim": "P0011"
}

for person in face_to_index:
    for x in range(4):
        location = ref.child(face_to_index[person]).child(str(x)).child("location").get()
        time = ref.child(face_to_index[person]).child(str(x)).child("time").get()
        key = face_to_index[person] + location + time
        ref.child(face_to_index[person]).child(str(x)).update({"key" : key})

# obj = {
#     "image": img,
#     "location": loc,
#     "time": time
# }
# array = [obj] + array
# array = array[:-1] 

# ref.child(index).set({
#     "0" : array[0],
#     "1" : array[1],
#     "2" : array[2],
#     "3" : array[3]
# })

print("write complete")

