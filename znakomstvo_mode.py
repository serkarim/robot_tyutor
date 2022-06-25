import cv2
cap=cv2.VideoCapture(0)
key=0
names=['no name','Karim','Ilya', 'Yulia']
face_cascade=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
recognizer=cv2.face.LBPHFaceRecognizer_create()
recognizer.read('faces_info.yml')
# smile_cascade=cv2.CascadeClassifier('haarcascade_smile.xml')
number=1
face_number=3
while key!=27:
    isRead,image=cap.read()
    image_gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    faces=face_cascade.detectMultiScale(image_gray, minNeighbors=20 )
    id=0
    for i in range (len(faces)):
        face=faces[i]
        x,y,width,height=face
        crop=image[y:y+height, x:x+width]
        crop_gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
        id, value=recognizer.predict(crop_gray)

        if value>50:
            name=names[0]
        else:
            name = names[id]
        print(id, value)
        cv2.putText(image,str(name),(x,y),cv2.FONT_HERSHEY_COMPLEX,2,(0,255,0),3)
        cv2.imshow('face',crop)
        cv2.rectangle(image,(x,y),(x+width,y+height),(0,255,0),5)
    cv2.imshow('window_gray',image_gray)

    cv2.imshow('window',image)
    key=cv2.waitKey(20)
cap.release()
