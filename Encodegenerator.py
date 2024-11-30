import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://facerecognitionwithrealt-e9796-default-rtdb.firebaseio.com/",
    'storageBucket': "facerecognitionwithrealt-e9796.appspot.com"
})
#-------converting image type 8 bits RGB


#img = cv2.imread("/Images")
#rgb_image = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)


# importing candidate images for recognition

ImgFolderPath = 'Images'
ImgPathList = os.listdir(ImgFolderPath)
ImgList = []
StudentIDs = []
for path in ImgPathList:
    ImgList.append(cv2.imread(os.path.join(ImgFolderPath, path)))
    #print(os.path.splitext(path)[0])
    StudentIDs.append(os.path.splitext(path)[0])

    # Database images upload
    filename = f'{ImgFolderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(filename)
    blob.upload_from_filename(filename)
#print(ImgList)
#print(StudentIDs)
def Findencoding(ImgList):
    EncodeList = []
    MissingImages = []  # List to store image paths with no detected faces
    for i, img in enumerate(ImgList):

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodings = face_recognition.face_encodings(img)
        if len(encodings) == 0:
            # No faces detected in the image
            #print(f"No faces detected in image: {ImgPathList[i]}")
            MissingImages.append(ImgPathList[i])
            continue
        encode = encodings[0]
        EncodeList.append(encode)
    return EncodeList, MissingImages


print("Encoding started")
knownencodeList = Findencoding(ImgList)
knownencodeList, missing_images = Findencoding(ImgList)

print("Missing Images:")
for image_path in missing_images:
    print(image_path)

#print(knownencodeList)
knownencodeListwithIDs = [knownencodeList, StudentIDs]
print("Encoding ended")
file = open("encodefile.p", "wb")
pickle.dump(knownencodeListwithIDs, file)
file.close()
print("file saved ")