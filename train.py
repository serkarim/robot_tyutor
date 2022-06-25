import cv2
import numpy
recognizer=cv2.face.LBPHFaceRecognizer_create()
images=[]
ids=[]
for face_number in range(1,4):
    number=1
    for number in range(1,251):

        image=cv2.imread('faces1/person.'+str(face_number)+'.'+str(number)+'.png')
        # cv2.imshow('window',image)
        print(face_number, number)
        image_gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

        cv2.imshow('window_GRAY',image_gray)
        cv2.waitKey(30)
        images.append(image_gray)
        ids.append(face_number)
print(images)
print(ids)
np_ids=numpy.array(ids)
recognizer.train(images, np_ids)
recognizer.write('faces_info.yml')