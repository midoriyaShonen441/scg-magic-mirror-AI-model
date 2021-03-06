# from tensorflow.keras.utils import img_to_array
from asyncore import write
import os
import cv2
import numpy as np
from keras.preprocessing import image
import warnings
warnings.filterwarnings("ignore")
from keras.models import  load_model
import keras
import time

# import matplotlib.pyplot as plt
import sys
import pickle


# import google face api functinon
from emotion_detect import detect_faces
import threading

# import google face api functinon
import voice

# function to sending data
def sendData(data):
    file = open('emotional.txt', 'wb')
    pickle.dump(data, file)
    file.close()

# funtion to send image to google vision api
def faceAPI():
    while True:
        try:
            time.sleep(5)
            detect_faces("test.png")
        except:
            pass

def voiceAPI():
    while True:
        voice.app_start()

# load model
# model = keras.models.load_model("best_model.h5")
# model = load_model("best_model.h5") 

face_haar_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)


thread_face = threading.Thread(target=faceAPI)
thread_face.start()
thread_voice = threading.Thread(target=voiceAPI)
thread_voice.start()

while True:
    ret, test_img = cap.read()  # captures frame and returns boolean value and captured image
    if not ret:
        continue
    # gray_img = cv2.cvtColor(test_img, cv2.COLOR_BGR2RGB)

    # faces_detected = face_haar_cascade.detectMultiScale(test_img, 1.32, 5)
    faces_detected = face_haar_cascade.detectMultiScale(test_img, 1.32, 5)

    for (x, y, w, h) in faces_detected:

        crop_x = x - int(w/2)
        crop_y = y - int(h/2)
        crop_w = x + int(1.5*w)
        crop_h = y + int(1.5*h)

        cv2.rectangle(test_img, (crop_x, crop_y), (crop_w, crop_h), (255, 0, 0), thickness=7)
        roi_gray = test_img[crop_y:crop_h, crop_x:crop_w]  # cropping region of interest i.e. face area from  image
        try:
            roi_gray = cv2.resize(roi_gray, (500, 500))
            cv2.imwrite("test.png", roi_gray)
        except:
            pass
        # print(roi_gray)
        # img_pixels = image.img_to_array(roi_gray)
        # img_pixels = np.expand_dims(img_pixels, axis=0)
        # img_pixels /= 255

        # predictions = model.predict(img_pixels)

        # find max indexed array
        # max_index = np.argmax(predictions[0])

        emotions = ('Face emotion: angry', 'Face emotion: disgust', 'Face emotion: fear', 'Face emotion: happy'
        , 'Face emotion: sad', 'Face emotion: surprise', 'Face emotion: neutral')
        # predicted_emotion = emotions[max_index]

        # send data to app.py
        # sendData(predicted_emotion)

        cv2.putText(test_img, "predicted_emotion", (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    resized_img = cv2.resize(test_img, (1000, 700))
    cv2.imshow('Facial emotion analysis ', resized_img)

    if cv2.waitKey(10) == ord('q'):  # wait until 'q' key is pressed
        break

cap.release()
cv2.destroyAllWindows
