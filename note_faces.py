import cv2
cap=cv2.VideoCapture(0)
key=0

face_cascade=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# smile_cascade=cv2.CascadeClassifier('haarcascade_smile.xml')
number=1
face_number=2
while number<=250:
    isRead,image=cap.read()
    image_gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    faces=face_cascade.detectMultiScale(image_gray, minNeighbors=20)

    for i in range (len(faces)):
        face=faces[i]
        x,y,width,height=face
        crop=image[y:y+height, x:x+width]
        cv2.imshow('face',crop)
        cv2.imwrite('faces1/person.'+str(face_number)+'.'+str(number)+'.png', crop)
        cv2.rectangle(image,(x,y),(x+width,y+height),(0,255,0),5)
        number+=1
    cv2.imshow('window_gray',image_gray)

    cv2.imshow('window',image)
    key=cv2.waitKey(20)
cap.release()
