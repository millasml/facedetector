const functions = require('firebase-functions');
const express = require('express');
const cors = require('cors');
var admin = require("firebase-admin");

const app = express();

// Automatically allow cross-origin requests
app.use(cors({ origin: true }));

//connect to real time db
var serviceAccount = require("PUT YOUR CRED JSON PATH HERE");

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  databaseURL: "PUT YOUR URL HERE"
});

var db = admin.database();
var ref = db.ref()
 
// // Create and Deploy Your First Cloud Functions
// // https://firebase.google.com/docs/functions/write-firebase-functions
//
// exports.helloWorld = functions.https.onRequest((request, response) => {
//  response.send("Hello from Firebase!");
// });

app.get('/', function(req, res){
  console.log("reached here!")
    ref.once("value", function(snapshot) {
      // console.log("hi")
      res.send(snapshot.val());
      }, function (errorObject) {
        console.log("The read failed: " + errorObject.code);
      });
    
})

// app.get('/lastSeen', function(req, res){
//   console.log("reached here!")
//     ref.child("lastSeen").on("value", function(snapshot) {
//       console.log("hi")
//       res.send(snapshot.val());
//       }, function (errorObject) {
//         console.log("The read failed: " + errorObject.code);
//       });
    
// })



app.get('/locations', function(req, res){
  ref.child('locations').once("value", function(snapshot) {
    // console.trace();
    res.send(snapshot.val());
    }, function (errorObject) {
      console.log("The read failed: " + errorObject.code);
    });
  
})

app.get('/tf', function(req, res){
  // console.trace();
  // console.log("reached here!")
  ref.once("value", function(snapshot) {
    // console.log("snapshot is reached")
    var data = snapshot.val();
    var trainedFaces = data.trainedFaces
    var lastSeen = data.lastSeen
    for (var [k, v] of Object.entries(trainedFaces)){
      trainedFaces[k].lasttime = lastSeen[k][0].time
      trainedFaces[k].lastloc = lastSeen[k][0].location
    }
    res.send(trainedFaces);
    // console.log(trainedFaces);
    }, function (errorObject) {
      console.log("The read failed: " + errorObject.code);
    });
  
})


// app.get('/tf', function(req, res){
//   console.trace();
//   console.log("reached here!")
//   ref.on("value", function(snapshot) {
//     console.log("snapshot is reached")
//     var data = snapshot.val();
//     var trainedFaces = data.trainedFaces
//     var lastSeen = data.lastSeen
//     for (var i = 0; i < 2; i++){
//       for(var j = 0; j < 2; j++){
//         if(trainedFaces[i].index === lastSeen[j].index){
//           trainedFaces[i].lasttime = lastSeen[j].lastSeen[0].time
//           trainedFaces[i].lastloc = lastSeen[j].lastSeen[0].location
//         }
//       }
//     }
//     res.send(trainedFaces);
//     // console.log(trainedFaces);
//     }, function (errorObject) {
//       console.log("The read failed: " + errorObject.code);
//     });
  
// })

app.get('/index/:index', function(req, res){
  var index = req.params.index
  ref.child('lastSeen').child(index).once("value", function(snapshot) {
    var tf = snapshot.val();
    ref.child('trainedFaces').child(index).once("value", function(snapshotTF){
      response = {
          "firstName": snapshotTF.val().firstName,
          "lastName": snapshotTF.val().lastName,
          "sightings": tf
        }
        res.send(response);
    })
    
    }, function (errorObject) {
      console.log("The read failed: " + errorObject.code);
    });
  
})


app.get('/name/:firstName', function(req, res){
  ref.once("value", function(snapshot) {
    var data = snapshot.val();
    for(var [k,v] of Object.entries(data.trainedFaces)){
      // console.log(`${k}: ${v}`)
      if(v.firstName === req.params.firstName){
        response = {
          "firstName": v.firstName,
          "lastName": v.lastName,
          "index": k,
          "sightings": data.lastSeen[k]
        }
        res.send(response)
      }
    }
 
    
    }, function (errorObject) {
      console.log("The read failed: " + errorObject.code);
    });
  
})





app.get('/picless/name/:firstName', function(req, res){
  ref.once("value", function(snapshot) {
    var data = snapshot.val();
    for(var [k,v] of Object.entries(data.trainedFaces)){
      // console.log(`${k}: ${v}`)
      if(v.firstName === req.params.firstName){
        response = {
          "firstName": v.firstName,
          "lastName": v.lastName,
          "index": k,
          "lasttime": data.lastSeen[k][0].time,
          "lastloc": data.lastSeen[k][0].location
        }
        res.send(response)
      }
    }
 
    
    }, function (errorObject) {
      console.log("The read failed: " + errorObject.code);
    });
  
})








// app.get('/recent_sightings/:firstName', function(req, res){
//   ref.on("value", function(snapshot) {
//     let data = snapshot.val();
//     let trainedFaces = data.trainedFaces
//     let lastSeen = data.lastSeen
//     for (let i = 0; i < 3; i++){
//       if ()
//     }
//     res.send(trainedFaces)
//     console.log(trainedFaces);
//     });
// })

exports.widgets = functions.https.onRequest(app);
