import cv2
import numpy
from project1.letters7x7 import *
import paho.mqtt.client as mqtt
import random
import speech_recognition as speech_recog


i, j = 0, 0
letters = ['О', 'И', 'М', 'Г', 'Й', 'З', 'К', 'Е', 'Б', 'В', 'А', 'П', 'Н', 'Д', 'Ж']
mas = [letter_o, letter_i, letter_m, letter_g, letter_ji, letter_z, letter_k, letter_e, letter_b, letter_v, letter_a,
       letter_p ,
       letter_n, letter_d,letter_j]


def destroy_windows():
    """Закрытие окон """
    cv2.destroyWindow('window_mask')
    cv2.destroyWindow('window')
    cv2.destroyWindow('crop_rotated')
    cv2.destroyWindow('crop')
    cv2.destroyWindow('crop_rotated2')


def recording_audio(filename):
    # Set chunk size of 1024 samples per data frame



    print('ЗВУУУУУУУУУУУУК')

    # Close and terminate the streamobject


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
    z = 4 * h // 15 + 0.5 * h // 15
    row = 0
    count_black = 0
    for i in range(7):
        x = 4 * w // 15 + 0.5 * w // 15
        column = 0
        for i in range(7):
            pixel = crop_rotated2[int(z), int(x)]
            cv2.circle(crop_rotated2, (int(x), int(z)), 10, (int(pixel[0]), int(pixel[1]), int(pixel[2])), -1)
            cv2.circle(crop_rotated2, (int(x), int(z)), 10, (int(255), int(0), int(0)), 2)
            if int(pixel[0]) < 150 and int(pixel[1]) < 150 and int(pixel[2]) < 150:
                letter[int(row)][int(column)] = 1
                count_black += 1
            x += w // 15
            column += 1
        z += h // 15
        row += 1
    return letter, count_black


def find_letter():  # распознаем букву
    flag = False
    message_current = ''

    '''Определяем букву, считываем кваддратики 7 на 7( объединяющая функция)'''
    global i, j, message, last_message, last_letter, letter_now

    letter, black_points = check_letter_points()
    if letter_correct_massiv == letter:
        i += 1
        j = 0
        print('Молодец!правильно!')
        cv2.putText(image, 'Молодец! Правильно!', (30, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0))
        # if last_letter != letter_correct:
        #     last_letter = letter_correct
    else:
        j += 1
        i = 0
        print('Неправильно!')
        cv2.putText(image, 'Неправильно!', (30, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0))
        for i in range(len(mas)):
            if letter == mas[i]:
                print('it is letter ' + letters[i])
                cv2.putText(image,
                            'Неправильно,это буква ' + letters[i] + ', положи  букву   ' + str(
                                letter_correct) + '     пожалуйста',
                            (30, 60), cv2.FONT_HERSHEY_COMPLEX, 0.75, (0, 0, 255))
                letter_now = letters[i]
                # if last_letter != letters[i]:
                #     last_letter = letters[i]
    #
    # if i > 10:
    #     message_current = '1'
    #     flag = True
    #     i = 0
    if j > 10:
        message_current = '0'
        flag = True
        j = 0
    print("!!!!!!!!!!", last_letter, letter_now)
    if last_letter != letter_now and letter_now in letters:
        recording_audio(filename=1)
        if letter_correct == letter_now:
            client.publish('serkarim/say_otvet', '0')

        else:
            client.publish('serkarim/camera_robot1', 'drive')

            client.publish('serkarim/2game', str(letter_now))
    last_letter=letter_now
    # if str(last_letter) != str(letter_now) and last_message==message5:
    #     client.publish(topic, message5)
    print(i, j)
    print('points:' + str(black_points))

    return flag


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


def client_on_message(client, userdata, msg):  # функция для получения сообщений
    '''Работа с протоколом передачи сообщений mqtt'''
    global message
    global topic_msg
    global old_message
    message = msg.payload.decode()
    topic_msg = msg.topic
    # if message=='ok':
    #     client.publish('serkarim/say_otvet','repite')
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

topic = 'serkarim/say_otvet'
key_stop = 32
last_letter = ''
word = 0
key = 0
letter_now = ''
global message1
topic2 = 'serkarim/say_otvet'
letter = ''
hostname = 'mqtt.pi40.ru'  # сервер
client = mqtt.Client()  # клиент mqtt
client.username_pw_set('serkarim', 'Serkarim_2009')
client.connect(hostname, 1883, 60)
topic1 = 'serkarim/r_letter'
client.subscribe('serkarim/r_letter')
client.subscribe('serkarim/done')
client.subscribe('serkarim/scan')
client.subscribe('serkarim/work')
client.subscribe('serkarim/otvet_robot')
client.subscribe('serkarim/camera_robot1')


client.subscribe('serkarim/otvet_letter')

client.on_message = client_on_message  # заходим в mqtt под своим userом
client.loop_start()
letter_correct_massiv = ''
# Resize the image using resize() method

topic_msg = ''
message = ''
last_message = ''
cap = cv2.VideoCapture(0)

flag = False
normal_squares = [1, 1, 1, 0]
print(HSV_down, HSV_up)
number = random.randint(0, len(letters) - 1)
letter_correct = letters[number]
print('prinyal letter')
client.publish('serkarim/camera_turn_head', '1')


while topic_msg != 'serkarim/done' and message != '1':
    pass
client.publish('serkarim/say_letter', str(letter_correct))
while topic_msg != 'serkarim/otvet_letter' and message != 'ok':
    pass
while True:
    while topic_msg != 'serkarim/otvet_robot' and message != 'ok':
        pass
    message=''
    flag_s = False
    print('start working')
    while flag_s != True:
        message = ''
        squares_now, image = create_windows(cap)
        contours, mask = create_mask_and_contour(image)
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if w > 100 and h > 100:
                new_coords, approx, crop = create_approx()
                if len(approx) == 4:
                    print(approx[0][0])
                    crop_rotated = create_crop_rotated(image)
                    cv2.imshow('window_rotated', crop_rotated)
                    cv2.drawContours(image, contour, -1, (0, 255, 0), 3)
                    w, h, crop_rotated2 = work_with_contour()
                    flag_s = find_letter()  # Flag = True

                    print('flag_s: ', flag_s)
                    cv2.imshow('crop_rotated', crop_rotated2)
                    cv2.imshow('crop', crop_rotated)
        cv2.imshow('window_mask', mask)
        cv2.imshow('window', image)
        cv2.waitKey(20)
        message = ''
        cv2.imshow('window', image)
        # key = cv2.waitKey(20)

cap.release()
