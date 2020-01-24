import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Fetch the service account key JSON file contents
cred = credentials.Certificate("PUT YOUR CRED JSON PATH HERE")

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': "PUT YOUR URL HERE"
})

# As an admin, the app has access to read and write all data, regradless of Security Rules
ref = db.reference('lastSeen')
index = "P0001"
img = "pythonsuccess2"
loc = "adsfadsfa"
time = "adsfafads"


array = ref.child(index).get()

obj = {
    "image": img,
    "location": loc,
    "time": time
}
array = [obj] + array
array = array[:-1] 

ref.child(index).set({
    "0" : array[0],
    "1" : array[1],
    "2" : array[2],
    "3" : array[3]
})

print("write complete")

