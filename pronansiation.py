import pyttsx3
import random
import paho.mqtt.client as mqtt
def client_on_message(client, userdata, msg):  # функция для получения сообщений
    global mes, text,  old_message
    global old_phrase
    global phrase
    message = msg.payload.decode()
    print(message)
    if str(msg.topic)== 'serkarim/say_letter':
        phrase='Покажи, пожалуйста букву'+str(message)
    if str(msg.topic) == 'serkarim/say_otvet':
        if message=='0':
            phrase='Молодец!Правильно!'
        elif message=='1':
            phrase='Неправильно!Попробуй еще раз'
    if str(msg.topic)=='serkarim/2game':
        phrase='Это буква '+str(message)
    message=''
    if phrase!=old_phrase:
        text=phrase
    if text!='':
        engine.say(text)
        engine.runAndWait()
        client.publish('serkarim/otvet_letter','ok')
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
old_message=''
hostname = 'mqtt.pi40.ru'  # сервер
client = mqtt.Client()  # клиент mqtt
client.username_pw_set('serkarim', 'Serkarim_2009')
client.connect(hostname, 1883, 60)
client.subscribe('serkarim/say_otvet')
client.subscribe('serkarim/return')

client.subscribe('serkarim/say_letter')# заходим в mqtt под своим userом
client.subscribe('serkarim/2game')
client.on_message = client_on_message # подключаемся к mqtt
client.loop_forever()
 # подписываемся на топик робота
  # обновление сообщений



