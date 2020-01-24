#!/usr/bin/env python
import cv2
import face_recognition
import numpy as np
import datetime
import json
import base64
import time

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

from global_constants import *


def crop(frame, mid_x, mid_y):

    crop_x = mid_x - 400
    crop_y = mid_y - 300

    if crop_x < 0:
        crop_x = 0
    elif crop_x > 1120:
        crop_x = 1120

    if crop_y < 0:
        crop_y = 0
    elif crop_y > 480:
        crop_y = 480

    return frame[int(crop_y): int(crop_y + 600), int(crop_x):int(crop_x + 800)]


def main(camera_id, video_capture):
    # load models
    try:
        print('* loading face encodings...')
        known_face_encodings = np.load("models/known_face_encodings.npy")
        known_face_names = np.load("models/known_face_names.npy")
    except:
        print('* error loading face encodings')
        import sys, traceback
        traceback.print_exc(file=sys.stdout)

    try:
        print('* connecting to database...')
        # Fetch the service account key JSON file contents
        cred = credentials.Certificate("../cloud_database/tech-digital-eyeball-firebase-adminsdk-wjsff-0a91534fba.json")

        # Initialize the app with a service account, granting admin privileges
        firebase_admin.initialize_app(cred, {
            'databaseURL': "https://tech-digital-eyeball.firebaseio.com"
        })

        # Initialize db document reference
        ref = db.reference('lastSeen')
    except:
        print('* error connecting to db')
        import sys, traceback
        traceback.print_exc(file=sys.stdout)


    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []

    local_last_seen = {}
    # Initialize local dictionary (to enable 1write/1min/pax)
    for person in face_to_index:
        local_last_seen[person] = datetime.datetime(2000, 1, 1)
    local_last_seen["Unknown"] = datetime.datetime(2000, 1, 1)


    # alternating boolean to only process every-other frame
    process_this_frame = True

    print('* starting video capture processing...')
    """Video streaming generator function."""
    while True:

        try:
            """THE FACIAL RECOG MODEL"""
            ret, frame = video_capture.read()

            # Resize frame of video to 1/4 size for faster face recognition processing
            # small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = frame[:, :, ::-1]

            # Only process every other frame of video to save time
            if process_this_frame:
                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(rgb_small_frame, number_of_times_to_upsample=1, model = "cnn")
                
                #version that doesnt kill my xps
                # face_locations = face_recognition.face_locations(rgb_small_frame)
                
                
                # print("frame (width, height) is: " + str(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)) + " , " + str(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))


                
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                face_names = []
                for face_encoding in face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.38)
                    name = "Unknown"

                    # # If a match was found in known_face_encodings, just use the first one.
                    # if True in matches:
                    #     first_match_index = matches.index(True)
                    #     name = known_face_names[first_match_index]

                    # Or instead, use the known face with the smallest distance to the new face
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]

                    face_names.append(name)

                #remove unknowns
                for i, person in reversed(list(enumerate(face_names[:]))):
                    if person is "Unknown":
                        face_names.pop(i)
                        face_locations.pop(i)
                        print("Unknown found at " + str(i))


            process_this_frame = not process_this_frame


            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                # top *= 4
                # right *= 4
                # bottom *= 4
                # left *= 4

                # Draw a box around the face
                # cv2.rectangle(frame, (left - 30, top - 30), (right + 30, bottom + 30), (243,65,169), 6)


                mid_x = int(((right - left) / 2) + left)

                mid_y = int(((bottom - top) /2 ) + top)

                # print("mid_x is: " + str(mid_x))
                # print("mid_y is: " + str(mid_y))

                
                cv2.rectangle(frame, (left - 60, top - 60), (right + 60, bottom + 60), (0,255,0), 12)
                cv2.rectangle(frame, (left - 66, top - 110), (right + 66, top - 60), (0,255,0), cv2.FILLED)

                # cv2.rectangle(frame, (mid_x - 400, mid_y - 300), (mid_x + 400, mid_y + 300), (255,255,255), 6)


                # Draw a label with a name below the face
                #cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                # counter = ""
                # if name == "Lyron":
                #     counter = "True"
                # cv2.putText(frame, name.upper(), (left , top - 35), font, 2.0, (243,65,169), 4)

                cv2.putText(frame, name.upper(), (left - 60, top - 70), font, 1.4, (0,0,0), 3)

                
                person_frame = crop(frame, mid_x, mid_y) 


                """start of DATA ENTRY"""

                write_time = datetime.datetime.now()

                delta = write_time - local_last_seen[name]

                if (delta.total_seconds() > 60):

                    retval, buffer = cv2.imencode('.jpg', person_frame)
                    jpg_as_text = base64.b64encode(buffer)
                    array = ref.child(face_to_index[name]).get()
           
                    obj = {
                        "image": "data:image/jpeg;base64," + jpg_as_text.decode("utf-8"),
                        "location": camera_id,
                        "time": format(write_time)
                    }
                    array = [obj] + array[:-1]
                    
                    ref.child(face_to_index[name]).set({
                        "0" : array[0],
                        "1" : array[1],
                        "2" : array[2],
                        "3" : array[3]
                    })

                    local_last_seen[name] = write_time
                    print("* db updated! " + name + " was added")
                    
                else:
                    print("* "+ name + " was detected, not time yet! " + str(delta.total_seconds()))

                """end of DATA ENTRY"""

            cv2.imshow('Video', cv2.resize(frame, (0, 0), fx=0.50, fy=0.5))
            # cv2.imshow('Video', frame)


            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            """end of FACIAL RECOG MODEL """

        except Exception as e:
            import sys, traceback
            traceback.print_exc(file=sys.stdout)
            # print(f"feed down error: {e}")
            print("* ERROR: FEED DOWN\n" + str(e))

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        '--camera-id',
        help='Unique key for camera ref')
    parser.add_argument(
        '--camera-uri',
        help='video capture camera URI',
        default= 0)

    args = parser.parse_args()
    camera_id = args.camera_id

    print('* connecting to camera %s...' % camera_id)
    video_capture = cv2.VideoCapture(args.camera_uri)

    # video_capture = cv2.VideoCapture("rtsp://admin:Singapore2019@192.168.3.229:554/cam/realmonitor?channel=1&subtype=0")

    main(camera_id, video_capture)
