# Immediately figure out who is stealing food from your fridge

facedetector is the cheapest, best solution to fix hunger caused by room mates stealing your food. It involves getting the RTSP stream of your IP cameras (must be connected to the same network as the machine running the application, or through direct ethernet connection to machine), performing  frame-by-frame facial recognition on the streams, and storing any detected faces in a google firebase realtime database. Google cloud functions was used to expose the database to facedetector

## Use Cases

When your friends steal your food even though you labelled it

When someone keeps leaving dishes unwashed in the sink

When your house has an ant situation and you want to know who is filthy

When there is always piss on the toilet seat

## Directory Breakdown

| DIRECTORY NAME | DESCRIPTION |
|----|----|
|cloud_database| includes all functions and scripts related to creating the endpoint to expose the realtime database|
|dataset| includes all training images|
|eyeball| includes all main files needed |


## Built With
create a virtual environment and install all requirements

you would get an error requiring you to install CMake (for the face_recognition API) if you don't have it in your computer. Hence, please install cmake with the following command

```bash
pip install cmake
```

please ensure you have the latest version of pip installed

```bash
pip install --upgrade pip
```

```bash
pip install -r requirements.txt
```

The following are the details of the main packages needed:

* face_recognition API
  * from site: built with deep learning. The model has an accuracy of 99.38% on the Labeled Faces in the Wild benchmark.
  * requires dlib to be installed on the computer too. When using pip to install, you need CMake to ensure that it is installed
  * see docs [here](https://pypi.org/project/face_recognition/) and sample github projects that this was adapted from [here](https://github.com/ageitgey/face_recognition/blob/master/examples/facerec_from_webcam_faster.py)
* OpenCV
  * OpenCV (Open Source Computer Vision Library) is an open source computer vision and machine learning software library. See releases [here](https://opencv.org/releases/). I used version 4.1.0 with python 3.7.2 on Windows. What we are installing is [opencv-python](https://pypi.org/project/opencv-python/), a pre-built opencv package for python
* numpy
* firebase-admin for access to the google firestore realtime database


if you do not fancy using the requirements.txt, just use the package manager [pip](https://pip.pypa.io/en/stable/) to install them.

```bash
pip install [package_name]
```

## Startup Instructions 
1. create virtual environment and install all requirements
2. enter the eyeball directory
```
 cd eyeball
```
3. run the start_digital_eyeball.sh script. After first use, just run this script to start the cameras again
 ```
 ./start_digital_eyeball.sh
 ```
4. to stop eyeball, enter the video window and hit "q". The script runs on 2 cameras with 2 video feeds so you will have to hit "q" on both windows

## Google Cloud Functions
google cloud functions was used to expose the realtime database to facedetector. The function was writing in javascript and can be found in cloud_database/index.js
In order to edit and then deploy the cloud function, you need to have firebase tools installed
```
npm install -g firebase-tools
```
follow the rest of the tutorial to set up your google firebase project [here](https://firebase.google.com/docs/functions/get-started)

edit the index.js file to change the endpoints. we use the following:
* firebase-admin
* firebase-functions
* cors
* express

more help on how to write cloud functions for the realtime db found [here](https://firebase.google.com/docs/database/admin/retrieve-data)

## More on Database Structure
realtimedb stores everything in JSON format. The 3 highest level objects are "lastSeen", "locations", and "trainedFaces".

each person is identified by its unique key, "P0001" to "P9999"
each camera is tagged to a location tag "L0001" to "L9999". The corresponding location to each tag is stored in "locations"

| KEY | DESCRIPTION |
|-----|-----|
|"lastSeen"| stores the 4 most recent sighting's image, location, and time for each person. each lastSeen entry also has a unique key, which composes of the person's index, location tag and timestamp|
|"locations"| The corresponding location to each tag is stored here |
|"trainedFaces"| stores the people enrolled in the database. also includes a profile picture for each person|

## Training New Faces
1. to train new faces, first add a few pictures to the dataset directory. Follow the file structure shown

```
dataset
 |- name
    |- name1.jpg
    |- name2.jpg
    |- name3.jpg
.
.
.
```

2. After which, you must update the database to enroll the person under "trainedFaces". To do so, edit the following global variables in addprofiles.py
```
cd cloud_database
cd helper_scripts
nano addprofiles.py

FIRST_NAME = "Jerome"
LAST_NAME = "Lee"
INDEX = "P0012"
PP_IMG_PATH = "C:/Users/milla/Desktop/digital-eyeball-v2/dataset/jerome/jerome1.jpg"
```

3. now, you need to update the model to include your new face. do this by running ``` python train_face_encodings.py```

4. after which, add the index and name to global_constants.py

## Model Tweaking
There are 3 main ways to tweak the model for better accuracy. You can read them in detail over [here](https://github.com/ageitgey/face_recognition/wiki/Face-Recognition-Accuracy-Problems)

1.  Changing tolerance values. Using tolerance values lower than 0.6 will make the comparison more strict.
```
#inside eyeball/run_one_camera.py
matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.38)
```
2.  Distort training images. That will tell dlib to randomly distort your image 100 times (randomly zoomed, rotated, translated, flipped), take the encoding of each version of the image and return the average. 
```
#inside eyeball/train_face_encodings.py
 known_face_encodings.append(face_recognition.face_encodings(img, num_jitters=100)[0])
```
3.  Upsampling. That means that the original image will be scaled up twice when looking for faces. This can help find smaller faces in the image that might otherwise
```
 face_locations = face_recognition.face_locations(rgb_small_frame, number_of_times_to_upsample=1, model = "cnn")
```

Finally, to GPU accelerate the model, you need to add the ``` model = "cnn" ``` parameter 
```
 face_locations = face_recognition.face_locations(rgb_small_frame, number_of_times_to_upsample=1, model = "cnn")
```

## Changing Cameras URI
to do so, you need to open eyeball/start_digital_eyeball.sh and change the CAMERA_URL.

## Bypassing The Script
In the event that you do not want to run the 2 cameras from the scripts, you can run the python file directly.
```
cd eyeball
python run_one_camera.py --camera-id L0001 --camera-uri "https://putyourcamerauri.here/1231322"
```

if you do not pass any camera-uri parameter, it will use your webcam by default.
you must put a camera-id parameter.