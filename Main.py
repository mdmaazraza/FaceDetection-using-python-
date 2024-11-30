import os
import cv2
import pickle
import face_recognition
import numpy as np
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime
from ultralytics import Yolo

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://facerecognitionwithrealt-e9796-default-rtdb.firebaseio.com/",
    'storageBucket': "facerecognitionwithrealt-e9796.appspot.com"
})
bucket = storage.bucket()
cap = cv2.VideoCapture(0)

cap.set(3, 640)
cap.set(4, 480)

imgbackground = cv2.imread("Resources/background.png")

# importing images from resources
folderModePath = 'Resources/Modes'
Modepathlist = os.listdir(folderModePath)
imgModeList = []
for path in Modepathlist:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))
print(len(imgModeList))

# Loading encoded Img
print("File is loading.....")
file = open("encodefile.p", "rb")
knownencodeListwithIDs = pickle.load(file)
file.close()
knownencodeList, StudentsIDs = knownencodeListwithIDs
print("Encoded file has been loaded")
print(StudentsIDs)
#----------- variables to later use--------------------------
TypeMode = 0
counter = 0
id = -1
color = (0,255,0)
imgStudent = []
#attendence = 0
while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2GRAY)

    FacecurFrame = face_recognition.face_locations(img)
    encodecurFace = face_recognition.face_encodings(img, FacecurFrame)
    imgbackground[162:162 + 480, 55:55 + 640] = img
    imgbackground[44:44 + 633, 808:808 + 414] = imgModeList[TypeMode]
    print(FacecurFrame)
    if FacecurFrame:

        for encodeFace, FaceLoc in zip(encodecurFace, FacecurFrame):
            Facecomp = face_recognition.compare_faces(knownencodeList, encodeFace)
            FaceDis = face_recognition.face_distance(knownencodeList, encodeFace)
            print("Matches", Facecomp)
            #print("Distance", FaceDis)
            matchIndex = np.argmin(FaceDis)
            #print("The face is at {} index in list".format(matchIndex))
            if Facecomp[matchIndex]:
                #print("Face Known ")
                #print(StudentsIDs[matchIndex])
                #----------------------------------
                '''results = model(img, stream=True, verbose=False)
                for r in results:
                    boxes = r.boxes
                    for box in boxes:
                        # Bounding Box
                        x1, y1, x2, y2 = box.xyxy[0]
                        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                        # cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,255),3)
                        w, h = x2 - x1, y2 - y1'''
                #----------------------------------
                y1, x2, y2, x1 = FaceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 55+x1, 162+y1, x2-x1, y2 - y1
                #imgbackground =cvzone.cornerRect(img, (x1, y1, x2, y2), colorC=color, colorR=color)
                imgbackground = cvzone.cornerRect(imgbackground, bbox, colorC=color, colorR=color, rt=0)
                id = StudentsIDs[matchIndex]
                if counter == 0:
                    cvzone.putTextRect(imgbackground, "Loading",(275, 400))
                    cv2.imshow("Face Attendance", imgbackground)
                    cv2.waitKey(1)

                    counter = 1
                    TypeMode = 1
        if counter != 0:


            if counter == 1:
                i = 1
                # Downloading data from realtime database

                Studentsinfo = db.reference(f'Employees/{id}').get()
                #print(Studentsinfo)
                # getting the images from the server

                blob = bucket.blob(f'Images/{id}.png')
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)

                # updating the database
                datetimeobject = datetime.strptime(Studentsinfo['Last_Attendance_Time'], "%d-%m-%Y %H:%M:%S")
                secondElapsed = (datetime.now() - datetimeobject).total_seconds()
                if secondElapsed > 30:

                    ref = db.reference(f'Employees/{id}')


                    Studentsinfo['total_attendance'] = int(Studentsinfo['total_attendance']) + 1

                    #attendence +=1


                    ref.child('total_attendance').set(Studentsinfo['total_attendance'])
                    ref.child('Last_Attendance_Time').set(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))

                else:
                    TypeMode = 3
                    counter = 0
                    imgbackground[44:44 + 633, 808:808 + 414] = imgModeList[TypeMode]

            if TypeMode != 3:

                if 10 < counter < 20:
                    TypeMode = 2
                imgbackground[44:44 + 633, 808:808 + 414] = imgModeList[TypeMode]


                if counter <= 10:

                    cv2.putText(imgbackground, str(Studentsinfo["total_attendance"]), (861, 125),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgbackground, str(Studentsinfo['Major']), (1006, 550),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgbackground, str(id), (1006, 493),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgbackground, str(Studentsinfo['Standing']), (910, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    cv2.putText(imgbackground, str(Studentsinfo['year']), (1025, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    cv2.putText(imgbackground, str(Studentsinfo['Starting_year']), (1125, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    #Adjusting name text in the middle
                    (w, h), _ = cv2.getTextSize(Studentsinfo['Name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                    offset = (414-w)//2

                    cv2.putText(imgbackground, str(Studentsinfo['Name']), (808+offset, 445),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (55, 55, 55), 1)
                    # showing image in right box of gui
                    imgbackground[175:175+216, 909:909+216] = imgStudent


                counter += 1
                if counter >= 20:
                    TypeMode = 0
                    counter = 0
                    Studentsinfo = []
                    imgStudent = []
                    imgbackground[44:44 + 633, 808:808 + 414] = imgModeList[TypeMode]
    else:
        TypeMode = 0
        counter = 0




    cv2.imshow("Face Attendance", imgbackground)
    #cv2.imshow("webcam", img)
    cv2.waitKey(1)
    #cv2.destroyallwindows()


