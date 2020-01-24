import cv2
import face_recognition
import numpy as np
import datetime
import os


PATH_DATASET = '../dataset'
PATH_MODELS = 'models/'

known_face_encodings = []

known_face_names = []

for dirname in os.listdir(PATH_DATASET):
    print(dirname)
    for image in os.listdir(PATH_DATASET + "/" + dirname):
        print(" |- " + image)
        try:
            img = face_recognition.load_image_file(PATH_DATASET +"/" + dirname + "/" + image)
            known_face_encodings.append(face_recognition.face_encodings(img, num_jitters=100)[0])
            known_face_names.append(dirname)
        except Exception as e:
            print("couldnt do "+ image)
            print(str(e))

np.save("%s/known_face_encodings" %PATH_MODELS, known_face_encodings)
np.save("%s/known_face_names" %PATH_MODELS, known_face_names)

print("training done")


# for filename in glob.glob(os.path.join(path, '*.txt')):
