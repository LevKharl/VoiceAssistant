import json
import pyttsx3
import vosk
import pyaudio
import requests

# Инициализация движка речи
tts = pyttsx3.init()
voices = tts.getProperty('voices')
for voice in voices:
    if voice.name == 'Microsoft David Desktop - English (United States)':
        tts.setProperty('voice', voice.id)

# Инициализация модели распознавания речи
model = vosk.Model('model_small')
record = vosk.KaldiRecognizer(model, 16000)
pa = pyaudio.PyAudio()
stream = pa.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

def listen():
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if record.AcceptWaveform(data) and len(data) > 0:
            answer = json.loads(record.Result())
            if answer['text']:
                yield answer['text']

def speak(say):
    print(say)
    tts.say(say)
    tts.runAndWait()

def get_weather():
    req = requests.get('https://wttr.in/Saint-Petersburg?format=j1')
    weather = req.json()
    return weather

def is_good_for_walk(weather):
    temp = int(weather['current_condition'][0]['temp_C'])
    wind = int(weather['current_condition'][0]['windspeedKmph'])
    if temp > 5 and wind < 15:
        return "Погода подходит для прогулки"
    else:
        return "Прогулка не рекомендуется"


print('start')
pwd = ''
for text in listen():
    if text == 'закрыть':
        quit()
    elif text == 'погода':
        weather = get_weather()
        speak(weather['current_condition'][0]['temp_C'])
    elif text == 'ветер':
        weather = get_weather()
        speak(weather['current_condition'][0]['windspeedKmph'])
    elif text == 'направление':
        weather = get_weather()
        speak(weather['current_condition'][0]['winddir16Point'])
    elif text == 'прогулка':
        weather = get_weather()
        speak(is_good_for_walk(weather))
    else:
        print(text)
