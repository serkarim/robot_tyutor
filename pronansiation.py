import pyttsx3
import random
import paho.mqtt.client as mqtt

phrases_good_1part=['Молодец!','Умничка!','Верно!','Так держать!','Замечательно!','Блестяще!','Умница!']
phrases_good_2part=['У тебя хорошо получается!','Поразительно!','Превосходно выполнено!','Твои родители могут гордиться тобой!','Ты настоящий мастер!','Просто прелесть!']
phrase_bad_1part=['н НЕ    правильно!','н НЕ  верно!']
phrase_bad_2part=['Попробуй еще раз','Ничего страшного.','Я понимаю, что это для тебя сложно ,но попробуй еще раз ','Не переживай, всё будет хорошо!']
def client_on_message(client, userdata, msg):  # функция для получения сообщенийп
    global mes, text,  old_message, name
    global old_phrase
    global phrase
    message = msg.payload.decode()
    print(message)
    if str(msg.topic)=='tutor/znakomstvo':
        if message=='no':
            phrase='Ятебя не знаю , давай знакомится.Меня зовут робот азбуковед. '
        elif message!='no':
            name=message
    if str(msg.topic)== 'tutor/say_letter':
        phrase=str(name)+'Покажи, пожалуйста букву'+str(message)
    if str(msg.topic) == 'tutor/say_otvet':
        if message=='0':
            number_part1=random.randint(0,len(phrases_good_1part)-1)
            number_part2=random.randint(0,len(phrases_good_2part)-1)

            phrase=str(name)+phrases_good_1part[number_part1]+phrases_good_2part[number_part2]
        elif message=='1':
            number_part1 = random.randint(0, len(phrase_bad_1part) - 1)
            number_part2 = random.randint(0, len(phrase_bad_2part) - 1)

            phrase = str(name)+ phrase_bad_1part[number_part1] + phrase_bad_2part[number_part2]
            print(phrase)
    if str(msg.topic)=='tutor/2game':
        phrase='Это буква '+str(message)
    message=''
    if phrase!=old_phrase:
        text=phrase
    if text!='':
        engine.say(text)
        engine.runAndWait()
        client.publish('tutor/otvet_letter','ok')
        old_phrase=''
        phrase=''
        text = ''
    old_message=mes
    old_phrase=phrase
    text=''


engine=pyttsx3.init()
mes=''
text=''
phrase=''
old_phrase=''
name=''
old_message=''
hostname = 'mqtt.pi40.ru'  # сервер
client = mqtt.Client()  # клиент mqtt
client.username_pw_set('tutor', 'password1')
client.connect(hostname, 1883, 60)
client.subscribe('tutor/say_otvet')
client.subscribe('tutor/return')

client.subscribe('tutor/say_letter')# заходим в mqtt под своим userом
client.subscribe('tutor/2game')
client.on_message = client_on_message # подключаемся к mqtt
client.loop_forever()
 # подписываемся на топик робота
  # обновление сообщений



