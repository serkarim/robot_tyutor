import cv2
import numpy
from letters7x7 import *
import paho.mqtt.client as mqtt
import random

i, j = 0, 0
letters = [  'В', 'А', 'Н', 'Д', 'Ж']
mas = [letter_v, letter_a, letter_n,letter_d,letter_j]

names=['no name','Karim','Aydar']
face_cascade=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
recognizer=cv2.face.LBPHFaceRecognizer_create()
recognizer.read('faces_info.yml')
# smile_cascade=cv2.CascadeClassifier('haarcascade_smile.xml')
number=1
face_number=2
def znakomstvo():
    global flag_f
    flag_f=True
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(image_gray, minNeighbors=20)
    id = 0
    if faces!=[]:
        flag_f=True
        for i in range(len(faces)):
            face = faces[i]
            x, y, width, height = face
            crop = image[y:y + height, x:x + width]
            crop_gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
            id, value = recognizer.predict(crop_gray)

            if value > 50:
                name = names[0]
            else:
                name = names[id]

            cv2.putText(image, str(id), (x, y), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 0), 3)
            cv2.imshow('face', crop)
            cv2.rectangle(image, (x, y), (x + width, y + height), (0, 255, 0), 5)
            return name


def destroy_windows():
    """Закрытие окон """
    cv2.destroyWindow('window_mask')
    cv2.destroyWindow('window')
    cv2.destroyWindow('crop_rotated')
    cv2.destroyWindow('crop')
    cv2.destroyWindow('crop_rotated2')






def check_letter_points():
    '''Получаем значение каждого пикселя буквы(7x7) и забиваем их массивы 1-черный 0- белый, чтобы определить какая это буква
    Возвращает текущий массив буквы'''
    letter = [[0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0]]
    z = 4 * h // 15 + 0.75* h // 15
    row = 0
    count_black = 0
    for i in range(7):
        x = 4 * w // 15 + 0.75* w // 15
        column = 0
        for i in range(7):
            pixel = crop_rotated2[int(z), int(x)]
            cv2.circle(crop_rotated2, (int(x), int(z)), 10, (int(pixel[0]), int(pixel[1]), int(pixel[2])), -1)
            cv2.circle(crop_rotated2, (int(x), int(z)), 10, (int(255), int(0), int(0)), 2)
            if int(pixel[0]) < 200 and int(pixel[1]) < 150 and int(pixel[2]) < 200:
                letter[int(row)][int(column)] = 1
                count_black += 1
            x += w // 15
            column += 1
        z += h // 15
        row += 1
    return letter, count_black


def find_letter2():  # распознаем букву
    flag = False
    message_current = ''

    '''Определяем букву, считываем кваддратики 7 на 7( объединяющая функция)'''
    global i, j, message, last_message, last_letter, letter_now,flag_s

    letter, black_points = check_letter_points()
    flag_r=False
    flag_s=False
    if letter_correct_massiv == letter:
        flag_r=True
        i += 1
        letter_now=letter_correct
        j = 0
        print('Молодец!правильно!')
        cv2.putText(image, 'Молодец! Правильно!', (30, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0))
        # if last_letter != letter_correct:
        #     last_letter = letter_correct
    else :

        flag_s=True

        j += 1
        i = 0
        print('Неправильно!')
        cv2.putText(image, 'Неправильно!', (30, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0))
        for i in range(len(mas)):
            if letter == mas[i]:
                letter_now = letters[i]

                print('it is letter ' + letters[i])
                cv2.putText(image,
                            'Неправильно,это буква ' + letters[i] + ', положи  букву   ' + str(
                                letter_correct) + '     пожалуйста',
                            (30, 60), cv2.FONT_HERSHEY_COMPLEX, 0.75, (0, 0, 255))
                # if last_letter != letters[i]:
                #     last_letter = letters[i]


    if i > 10:
        flag = True
        i = 0
    if j > 10:
        flag = False
        j = 0
    print("!!!!!!!!!!", last_letter, letter_now)
    if last_letter != letter_now and letter_now in letters:
        if letter_correct == letter_now:
            client.publish('tutor/2game', str(letter_now))
            client.publish('tutor/start', 'end')

        else:
            client.publish('tutor/camera_robot1', 'drive')

            client.publish('tutor/2game', str(letter_now))
    last_letter=letter_now
    # if str(last_letter) != str(letter_now) and last_message==message5:
    #     client.publish(topic, message5)
    print('points:' + str(black_points))

    return flag_r,flag_s


def draw_circles(w1, h1, w2, h2, w3, h3, w4, h4, square1, square2, square3, square4):
    '''рисуем круги в четырех квадратах(которые стоят по углам)'''
    cv2.circle(crop_rotated, (w2, h2), 10, (int(square2[0]), int(square2[1]), int(square2[2])), -1)
    cv2.circle(crop_rotated, (w2, h2), 14, (0, 255, 255), )
    cv2.circle(crop_rotated, (w1, h1), 10, (int(square1[0]), int(square1[1]), int(square1[2])), -1)
    cv2.circle(crop_rotated, (w1, h1), 14, (0, 255, 0), )
    cv2.circle(crop_rotated, (w3, h3), 10, (int(square3[0]), int(square3[1]), int(square3[2])), -1)
    cv2.circle(crop_rotated, (w3, h3), 14, (255, 255, 0), )
    cv2.circle(crop_rotated, (w4, h4), 10, (int(square4[0]), int(square4[1]), int(square4[2])), -1)
    cv2.circle(crop_rotated, (w4, h4), 14, (0, 0, 255), )


def draw_lines():
    '''Разлиновываем карточку на квадраты 15x15'''

    c = w // 15
    for i in range(15):
        cv2.line(crop_rotated, (c, 0), (c, h), (0, 255, 0))
        c += w // 15
    c = h // 15
    for i in range(15):
        cv2.line(crop_rotated, (0, c), (w, c), (0, 255, 0))
        c += h // 15


def rotate_card():
    '''Поворачиваем карточку в зависимости от значения цвета четырех квадаратов'''
    if normal_squares == squares_now:
        crop_rotated2 = crop_rotated
    elif squares_now == [0, 1, 1, 1]:
        crop_rotated2 = cv2.rotate(crop_rotated, cv2.ROTATE_90_COUNTERCLOCKWISE)
    elif squares_now == [1, 0, 1, 1]:
        crop_rotated2 = cv2.rotate(crop_rotated, cv2.ROTATE_180)
    else:
        crop_rotated2 = cv2.rotate(crop_rotated, cv2.ROTATE_90_CLOCKWISE)
    print(squares_now)
    return crop_rotated2


def black_squares(w1, h1, w2, h2, w3, h3, w4, h4, square1, square2, square3, square4):
    '''Опрделяем значения цвета квадратов 1-черный 0-белый и заносим их в массив'''
    if square1[0] < 160 and square1[1] < 160 and square1[2] < 160:
        squares_now[0] = 1
        cv2.putText(crop_rotated, 'black', (w1, h1), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0))

    if square2[0] < 160 and square2[1] < 160 and square2[2] < 160:
        squares_now[1] = 1
        cv2.putText(crop_rotated, 'black', (w2, h2), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0))
    if square3[0] < 160 and square3[1] < 160 and square3[2] < 160:
        squares_now[2] = 1
        cv2.putText(crop_rotated, 'black', (w3, h3), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0))
    if square4[0] < 160 and square4[1] < 160 and square4[2] < 160:
        squares_now[3] = 1
        cv2.putText(crop_rotated, 'black', (w4, h4), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0))
def find_letter():  # распознаем букву
    flag = False

    message_current = ''
    '''Определяем букву, считываем кваддратики 7 на 7( объединяющая функция)'''
    global i, j, message, last_message, last_letter, letter_now,flag_r
    letter, black_points = check_letter_points()
    flag_r=False
    flag_s=False
    if letter_correct_massiv == letter:
        i += 1
        flag_r= True

        message_current='0'
        j = 0
        print('Молодец!правильно!')
        cv2.putText(image, 'Молодец! Правильно!', (30, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0))
        letter_now=letter_correct
        # if last_letter != letter_correct:
        #     last_letter = letter_correct
    else:
        j += 1
        message_current='1'
        flag_s=True

        i = 0
        print('Неправильно!')
        cv2.putText(image, 'Неправильно!', (30, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0))
        for i in range(len(mas)):
            if letter == mas[i]:
                letter_now = letters[i]
                print('it is letter ' + letters[i])
                cv2.putText(image,
                            'Неправильно,это буква ' + letters[i] + ', положи  букву   ' + str(
                                letter_correct) + '     пожалуйста',
                            (30, 60), cv2.FONT_HERSHEY_COMPLEX, 0.75, (0, 0, 255))
                # if last_letter != letters[i]:
                #     last_letter = letters[i]
    print(letter_now)
    if i > 10:
        message_current = '1'
        i = 0
    if j > 10:
        message_current = '0'
        flag = True
        j = 0
    print("!!!!!!!!!!",last_letter, letter_now)
    if last_letter != letter_now:
        client.publish('tutor/say_otvet', str(message_current))
        last_message = message_current
        last_letter = letter_now

    # if str(last_letter) != str(letter_now) and last_message==message5:
    #     client.publish(topic, message5)
    print(i, j)
    print('points:' + str(black_points))

    return flag_r,flag_r

def work_with_contour():
    '''Объединяющаяя функция тех функций ,предназначенных для работы с контуром и угловыми квадратами'''

    w, h, w1, h1, w2, h2, w3, h3, w4, h4, square1, square2, square3, square4 = create_zones_of_squares()
    draw_circles(w1, h1, w2, h2, w3, h3, w4, h4, square1, square2, square3, square4)
    black_squares(w1, h1, w2, h2, w3, h3, w4, h4, square1, square2, square3, square4)
    crop_rotated2 = rotate_card()
    # draw_lines()
    return w, h, crop_rotated2


def create_windows(cap):
    '''Работа с основным изображением зеркалим его и задаем начальные параметры'''
    squares_now = [0, 0, 0, 0]
    isRead, image = cap.read()
    image = cv2.flip(image, 1)
    return squares_now, image
def create_windows2(cap):
    squares_now = [0, 0, 0, 0]
    y = 240
    x = 0
    height = 240
    width = 640
    isRead, image = cap.read()
    image = image[y:y + height, x:x + width]
    image = cv2.flip(image, 1)

    return squares_now, image
# def create_windows(cap):
#     squares_now = [0, 0, 0, 0]
#
#     y = 240
#     x = 0
#     height = 240
#     width = 640
#     isRead, image = cap.read()
#     image = cv2.flip(image, 1)


    # return image, squares_now

def client_on_message(client, userdata, msg):  # функция для получения сообщений
    '''Работа с протоколом передачи сообщений mqtt'''
    global message
    global topic_msg
    global old_message
    message = msg.payload.decode()
    topic_msg = msg.topic
    # if message=='ok':
    #     client.publish('tutor/say_otvet','repite')
    print(str(message))


def create_zones_of_squares():
    '''Определяем координаты квадратов'''
    h, w = 300, 300
    w2, h2 = int(0.5 * 300 // 11 + 300 // 11), int(0.5 * 300 // 11 + 300 // 11)
    h1, w1 = int(300 // 11 * 10 - 0.5 * 300 // 11), int(300 // 11 + 0.5 * 300 // 11)
    h3, w3 = int(300 // 11 + 0.5 * 300 // 11), int(300 // 11 * 10 - 0.5 * 300 // 11)
    h4, w4 = int(300 // 11 * 10 - 0.5 * 300 // 11), int(300 // 11 * 10 - 0.5 * 300 // 11)
    square2 = crop_rotated[h2, w2]
    square1 = crop_rotated[h1, w1]
    square3 = crop_rotated[h3, w3]
    square4 = crop_rotated[h4, w4]
    return w, h, w1, h1, w2, h2, w3, h3, w4, h4, square1, square2, square3, square4


def create_crop_rotated(image):
    '''Обрезаем картинку под размер карточки'''

    x1, y1 = approx[0][0][0], approx[0][0][1]
    x2, y2 = approx[1][0][0], approx[1][0][1]
    x3, y3 = approx[2][0][0], approx[2][0][1]
    x4, y4 = approx[3][0][0], approx[3][0][1]
    old_coords = numpy.float32([[x1, y1], [x2, y2], [x3, y3], [x4, y4]])
    M = cv2.getPerspectiveTransform(old_coords, new_coords)
    crop_rotated = cv2.warpPerspective(image, M, (300, 300))
    return crop_rotated


def create_mask_and_contour(image):
    '''Создаем маску и контур ;)'''

    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV_FULL)
    mask = cv2.inRange(image_hsv, HSV_down, HSV_up)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    return contours, mask


def create_approx():
    '''Упрощаем контуры'''

    crop = image[y:y + h, x:x + w]
    new_coords = numpy.float32([[0, 0], [300, 0], [300, 300], [0, 300]])
    perimetr = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.015 * perimetr, True)
    cv2.drawContours(image, [approx], -1, (0, 255, 255), 3)
    return new_coords, approx, crop


def read_file(filename):
    '''Функция для считывания файлов'''

    file = open(filename, 'r')
    data = file.read()
    HSV_values = data.split(',')
    H_up_blue = int(HSV_values[0])
    S_up_blue = int(HSV_values[1])
    V_up_blue = int(HSV_values[2])
    H_down_blue = int(HSV_values[3])
    S_down_blue = int(HSV_values[4])
    V_down_blue = int(HSV_values[5])
    file.close()
    return (H_up_blue, S_up_blue, V_up_blue, H_down_blue, S_down_blue, V_down_blue)


H_up_blue, S_up_blue, V_up_blue, H_down_blue, S_down_blue, V_down_blue = read_file('blue.txt')
HSV_up = numpy.array([H_up_blue, S_up_blue, V_up_blue])
HSV_down = numpy.array([H_down_blue, S_down_blue, V_down_blue])
flag_f=False
# topic = 'tutor/say_otvet'
last_letter = ''
letter_now = ''
# topic2 = 'tutor/say_otvet'
letter = ''
hostname = 'mqtt.pi40.ru'  # сервер
client = mqtt.Client()  # клиент mqtt
client.username_pw_set('tutor', 'password1')
client.connect(hostname, 1883, 60)
# topic1 = 'tutor/r_letter'
client.subscribe('tutor/r_letter')
client.subscribe('tutor/done')
client.subscribe('tutor/scan')
client.subscribe('tutor/work')
client.subscribe('tutor/otvet_robot')
client.subscribe('tutor/camera_robot')
client.subscribe('tutor/tg')

client.subscribe('tutor/otvet_letter')
client.on_message = client_on_message  # заходим в mqtt под своим userом
client.loop_start()
letter_correct_massiv = ''
topic_msg = ''
message = ''
is_camera=True
last_message = ''
cap = cv2.VideoCapture(0)
flag_mode=False
flag = False
normal_squares = [1, 1, 1, 0]
print(HSV_down, HSV_up)
flag_r=False
name=''
if is_camera==True:
    while True:
        while topic_msg != 'tutor/tg':
            pass
        print('prinyal letter')

        if message == '1':
            while flag_f != True:
                flag_f,name = znakomstvo()
            if name=='no name':
                client.publish('tutor/znakomstvo','no')
            else:
                client.publish('tutor/znakomstvo',str(name))


            print('first')
            flag = False
            normal_squares = [1, 1, 1, 0]
            print(HSV_down, HSV_up)
            number = random.randint(0, len(letters) - 1)
            letter_correct = letters[number]
            last_letter=''
            letter_now = ''

            print('prinyal letter')
            client.publish('tutor/start', 'start_mode1')
            while topic_msg != 'tutor/done' and message != '1':
                pass
            client.publish('tutor/say_letter', str(letter_correct))
            for i in range(len(letters)):
                if letter_correct == letters[i]:
                    letter_correct_massiv = mas[i]
            flag_s = False
            flag_r = False
            while flag_r!=True:
                while topic_msg != 'tutor/otvet_letter' and message != 'ok':
                    pass
                message = ''
                squares_now, image = create_windows(cap)

                contours, mask = create_mask_and_contour(image)
                for contour in contours:
                    x, y, w, h = cv2.boundingRect(contour)

                    if w > 50 and h > 50:
                        new_coords, approx, crop = create_approx()
                        if len(approx) == 4:
                            # print(approx[0][0])
                            crop_rotated = create_crop_rotated(image)
                            cv2.imshow('window_rotated', crop_rotated)
                            cv2.drawContours(image, contour, -1, (0, 255, 0), 3)
                            w, h, crop_rotated2 = work_with_contour()
                            flag_s, flag_r = find_letter()  # Flag = True
                            print('flag_s: ', flag_s)
                            cv2.imshow('crop_rotated', crop_rotated2)
                            cv2.imshow('crop', crop_rotated)
                cv2.imshow('window_mask', mask)
                cv2.imshow('window', image)
                cv2.waitKey(20)
                message = ''
                cv2.imshow('window', image)
            if flag_r == True:
                client.publish('tutor/start', 'end')
        elif message == '2':
            last_message = ''
            flag = False
            normal_squares = [1, 1, 1, 0]
            print(HSV_down, HSV_up)
            last_letter=''
            letter_now = ''
            letter = ''

            print('prinyal letter')
            while topic_msg != 'tutor/r_letter':
                pass
            letter_correct = message
            for i in range(len(letters)):
                if letter_correct == letters[i]:
                    letter_correct_massiv = mas[i]
            print(letter_correct_massiv)
            client.publish('tutor/start', 'start_mode2')

            # client.publish('tutor/say_letter', str(letter_correct))
            # while topic_msg != 'tutor/otvet_letter' and message != 'ok':
            #     pass
            flag_s = False

            while flag_r!=True:
                print('ddd')
                while topic_msg != 'tutor/otvet_robot' and message != 'ok':
                    pass
                print('ok')
                message = ''
                squares_now, image = create_windows2(cap)

                print('start working')
                flag_s=False
                while flag_s != True:
                    norm_contour = []
                    rast_spisok = []
                    message = ''
                    squares_now, image = create_windows2(cap)
                    contours, mask = create_mask_and_contour(image)
                    for contour in contours:
                        x, y, w, h = cv2.boundingRect(contour)
                        if w > 30 and h > 30:
                            new_coords, approx, crop = create_approx()
                            if len(approx) == 4:
                                norm_contour.append(contour)
                                # print(norm_contour,'sdcsdcsdcdcsdcsdcs')
                    if norm_contour != []:
                        for c in norm_contour:
                            x, y, w, h = cv2.boundingRect(c)
                            rast = abs(320 - x), abs(240 - y)

                            rast_spisok.append(rast)
                        # print(rast_spisok,'dcwedcwsdc')
                    if rast_spisok != []:
                        number = rast_spisok.index(min(rast_spisok))
                        contour = norm_contour[number]
                        # print(norm_contour,'norm_contour')
                        new_coords, approx, crop = create_approx()
                        # print(approx[0][0])
                        if len(approx) == 4:
                            crop_rotated = create_crop_rotated(image)

                            cv2.imshow('window_rotated', crop_rotated)
                            cv2.drawContours(image, contour, -1, (0, 255, 0), 3)
                            w, h, crop_rotated2 = work_with_contour()
                            flag_r,flag_s = find_letter2()  # Flag = True

                            print('flag_s: ', flag_s)
                            cv2.imshow('crop_rotated', crop_rotated2)
                            cv2.imshow('crop', crop_rotated)
                    cv2.imshow('window_mask', mask)
                    cv2.imshow('window', image)
                    cv2.waitKey(20)
                    message = ''
                    cv2.imshow('window', image)
            if flag_r == True:
                client.publish('tutor/start', 'end')


else:
    while True:
        message=''
        while topic_msg != 'tutor/tg':
            pass
        print('prinyal letter')
        last_letter=''
        if message == '1':
            print('first')
            flag = False
            last_letter=''
            letter_now = ''
            normal_squares = [1, 1, 1, 0]
            print(HSV_down, HSV_up)
            number = random.randint(0, len(letters) - 1)
            letter_correct = letters[number]
            print('prinyal letter')
            client.publish('tutor/start', 'start_mode1')
            while topic_msg != 'tutor/done' and message != '1':
                pass
            client.publish('tutor/say_letter', str(letter_correct))
            for i in range(len(letters)):
                if letter_correct == letters[i]:
                    letter_correct_massiv = mas[i]
            flag_s = False
            flag_r = False
            while flag_r != True:
                while topic_msg != 'tutor/otvet_letter' and message != 'ok':
                    pass
                message = ''
                squares_now, image = create_windows(cap)
                contours, mask = create_mask_and_contour(image)
                for contour in contours:
                    x, y, w, h = cv2.boundingRect(contour)

                    if w > 50 and h > 50:
                        new_coords, approx, crop = create_approx()
                        if len(approx) == 4:
                            # print(approx[0][0])
                            crop_rotated = create_crop_rotated(image)
                            cv2.drawContours(image, contour, -1, (0, 255, 0), 3)
                            w, h, crop_rotated2 = work_with_contour()
                            flag_s, flag_r = find_letter()  # Flag = True
                            print('flag_s: ', flag_s)

                cv2.waitKey(20)
                message = ''

            if flag_r == True:
                client.publish('tutor/start', 'end')
        elif message == '2':
            last_message = ''
            flag = False
            normal_squares = [1, 1, 1, 0]
            print(HSV_down, HSV_up)
            message=''
            flag_r=False
            flag_s=False
            topic_msg=''
            last_letter=''
            letter_now = ''
            letter = []

            print('prinyal letter')
            while topic_msg != 'tutor/r_letter':
                pass
            letter_correct = message
            for i in range(len(letters)):
                if letter_correct == letters[i]:
                    letter_correct_massiv = mas[i]
            print(letter_correct_massiv)
            client.publish('tutor/start', 'start_mode2')

            # client.publish('tutor/say_letter', str(letter_correct))
            # while topic_msg != 'tutor/otvet_letter' and message != 'ok':
            #     pass
            flag_s = False

            while flag_r != True:
                print('ddd')
                while topic_msg != 'tutor/otvet_robot' and message != 'ok':
                    pass
                print('ok')

                message = ''
                squares_now, image = create_windows2(cap)

                print('start working')
                flag_s=False

                while flag_s != True:
                    norm_contour = []
                    rast_spisok = []
                    message = ''
                    squares_now, image = create_windows2(cap)
                    contours, mask = create_mask_and_contour(image)
                    for contour in contours:
                        x, y, w, h = cv2.boundingRect(contour)
                        if w > 30 and h > 30:
                            new_coords, approx, crop = create_approx()
                            if len(approx) == 4:
                                norm_contour.append(contour)
                                # print(norm_contour,'sdcsdcsdcdcsdcsdcs')
                    if norm_contour != []:
                        for c in norm_contour:
                            x, y, w, h = cv2.boundingRect(c)
                            rast = abs(320 - x), abs(240 - y)

                            rast_spisok.append(rast)
                        # print(rast_spisok,'dcwedcwsdc')
                    if rast_spisok != []:
                        number = rast_spisok.index(min(rast_spisok))
                        contour = norm_contour[number]
                        # print(norm_contour,'norm_contour')
                        new_coords, approx, crop = create_approx()
                        # print(approx[0][0])
                        if len(approx) == 4:
                            crop_rotated = create_crop_rotated(image)


                            cv2.drawContours(image, contour, -1, (0, 255, 0), 3)
                            w, h, crop_rotated2 = work_with_contour()
                            flag_r, flag_s = find_letter2()  # Flag = True

                            print('flag_s: ', flag_s)

                    cv2.waitKey(20)
                    message = ''

            if flag_r == True:
                client.publish('tutor/start', 'end')
