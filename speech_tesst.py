import speech_recognition as sp
import paho.mqtt.client as mqtt
mic=sp.Microphone()
hostname = 'mqtt.pi40.ru'  # сервер
client = mqtt.Client()  # клиент mqtt
client.username_pw_set('tutor', 'password1')
client.connect(hostname, 1883, 60)
message=''
# topic1 = 'tutor/r_letter'
letters_sm=['а','н','в','ж','д']
letter_b=['А','Н','В','Ж','Д']
r=sp.Recognizer()
with sp.Microphone() as source:
    print("Say something!")
    audio=r.listen(source)

try:
    # for testing purposes, we're just using the default API key
    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
    # instead of `r.recognize_google(audio)`
    a=r.recognize_google(audio, language='RU-ru')
    print("Google Speech Recognition thinks you said " + a)
    letter=a[-1:]
    print(letter)
    if letter in letters_sm:
        for i in letters_sm:
            if letter==letters_sm:
                message=letter_b[i]
    elif letter in letter_b:
        message=letter
    client.publish('tutor/2letter',str(message))

except sp.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sp.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))