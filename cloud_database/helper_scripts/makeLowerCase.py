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
ref = db.reference('trainedFaces')


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
    "caroline": "P0010"
}


for person in face_to_index:
    personname = ref.child(face_to_index[person]).child("firstName").get()
    print(personname.lower())
    ref.child(face_to_index[person]).child("firstName").set(person.lower())


print("write complete")

