


function modelPost(index, img, loc, time){

    var admin = require("firebase-admin");

    //connect to real time db
    var serviceAccount = require("PUT YOUR CRED JSON PATH HERE");

    admin.initializeApp({
    credential: admin.credential.cert(serviceAccount),
    databaseURL: "PUT YOUR URL HERE"
    });

    var db = admin.database();
    var ref = db.ref()

    ref.child('lastSeen').child(index).once("value", function(snapshot){
        var array = snapshot.val();
        obj = {
            "image": img,
            "location": loc,
            "time": time
        }
        array.unshift(obj);
        array.pop();
        // console.log(array);
        ref.child('lastSeen').child(index).set({
            "0" : array[0],
            "1" : array[1],
            "2" : array[2],
            "3" : array[3]
        });
        console.log("write complete")

    }, function (errorObject) {
      console.log("The read failed: " + errorObject.code);
    });

}

// console.log(modelPost("P0001", "imagebytes456", "L0003", "timestamp123"))