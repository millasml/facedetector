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
    "cs" : "P0002",
    "james" : "P0004",
    "akbar": "P0008",
    "tim": "P0011"
}

iniarray = []

# obj = {
#         "image": "",
#         "location": "L0001",
#         "time": "2000-07-05 14:56:54.807444"
#          }

for x in range(4):
    iniarray.append({
        "image": "",
        "location": "L0001",
        "time": "2000-07-05 14:56:54.807" + str(x) + str(x) + str(x)
         })
    
print(iniarray)

for person in face_to_index:
    ref.child(face_to_index[person]).set(iniarray)
    

# array = ref.child(index).get()

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

