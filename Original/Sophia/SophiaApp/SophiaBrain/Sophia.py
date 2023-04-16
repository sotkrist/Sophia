# started project at 05/03/2021, lat: 47.4979 lon: 19.0402
import os

isReqInstalled = False
errorWithReq = False
brain_path = os.getcwd()
x = brain_path + "\\"

try:
    os.system('cmd /c "pip install -r {}requirements.txt"'.format(x))
    try:
        os.system('cmd /c "pip install {}PyAudio-0.2.11-cp39-cp39-win_amd64.whl"'.format(brain_path))
    except:
        try:
            os.system('cmd /c "pip install {}PyAudio-0.2.11-cp310-cp310-win32.whl"'.format(brain_path))
        except:
            try:
                os.system('cmd /c "pip install {}PyAudio-0.2.11-cp39-cp39-win32.whl"'.format(brain_path))
            except:
                try:
                    os.system('cmd /c "pip install {}PyAudio-0.2.11-cp38-cp38-win_amd64.whl"'.format(brain_path))
except:
    try:
        os.system('cmd /c "pip3 install {}-r requirements.txt"'.format(x))
    except:
        try:
            os.system('cmd /c "python -m pip install -r {}requirements.txt"'.format(x))
        except:
            errorWithReq = True

isReqInstalled = True
os.system('cmd /c "cls"')

import json
import datetime
import webbrowser
import pyttsx3
import requests
import aiml
import time
from os import path
import random
import pywhatkit
import psutil
import platform
import yaml
import wikipedia as wikipedia
import speech_recognition as sr
from joke.quotes import *
from joke.jokes import *

aiml_kernel = aiml.Kernel()
aiml_kernel.setBotPredicate("name", "Sophia")
aiml_kernel.setBotPredicate("botmaster", "R2 System")


def getPath(p):
    if "\\" not in p:
        p = "\\" + p
    return brain_path + "\storedDatas" + p


def getPathForBrain(p):
    return brain_path + p


def readFile(filePath):
    with open(filePath, 'r') as f:
        read = f.read()
    return read


def writeToFile(pa, s):
    f = open(pa, 'w')
    f.write(str(s))
    f.close()


brain_path2 = readFile(getPath("workingDir.txt"))[0:-9]
config = yaml.safe_load(open(brain_path2 + "\config.yaml"))
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
todo_path = getPath(config["todo_path"])

sophia_wake = ["sophia", "sofia", "sofie", "sophie", "soften"]
greeting_wake = ["hello", "hi", "good morning", "hello there", "morning", "hey"]
pcInfo_wake = ["cpu", "ram", "operation system", "system"]
showTodo_wake = ["my todo", "my to-do", "my to do", "mine to do", "mine to-do"]
newTodo_wake = ["new todo", "new to-do", "new to do"]
password_wake = ["my password", "my passwords"]
weather_wake = ["weather", "temperature"]
whatInspections = ["what is the time", "what is the weather", "what is the news", "what is the date"]

newTodoListening = False

usedSophiaWakeWord = ""
lat = ""
lon = ""

ambient = readFile(getPath(config["ambient"]))
timeOut = float(readFile(getPath(config["timeOut"])))


def checkSentence(words, sentence):
    global usedSophiaWakeWord
    for word in words:
        if word in sentence:
            usedSophiaWakeWord = word
            return True
    return False


def checkForExit():
    isExit = readFile(getPath(config["exit_path"]))
    if isExit == '1':
        writeToFile(getPath(config["exit_path"]), "0")
        os.remove(getPath(config["running"]))
        exit(1)


def SophiaCommunication(msg):
    print("\33[33mSophia: {}".format(msg))
    engine.say(msg)
    engine.runAndWait()


def saveFile(filePath, text):
    with open(filePath, 'w') as f:
        json.dump(text, f)


def personDefinition(cmd):
    person = cmd.replace("who is", "")
    try:
        infoOfPerson = wikipedia.summary(person, 1)
        SophiaCommunication(infoOfPerson)
    except:
        SophiaCommunication("I couldn't find that person!")


def openWebsites(cmd):
    ix = cmd.index("open")
    website = cmd[ix + 5:]
    try:
        webbrowser.open("https://{}.com/".format(website))
    except:
        try:
            webbrowser.open("https://www.{}.com/".format(website))
        except:
            SophiaCommunication("Sorry, but i couldn't open that website!")


def objectDefinition(cmd):
    RandomObject = cmd.replace("what is", "")
    try:
        infoOfObject = wikipedia.summary(RandomObject, 1)
        SophiaCommunication(infoOfObject)
    except:
        SophiaCommunication("Here's what i found on google.")
        webbrowser.open("https://www.google.com/search?q={}".format(RandomObject))


def greeting():
    time_check = int(time.strftime("%H"))
    if time_check < 10:
        SophiaCommunication("Good morning sir, did you sleep well?")
    elif time_check < 16:
        SophiaCommunication("Good afternoon sir!")
    elif time_check > 16:
        SophiaCommunication("Good evening sir!")


def weather():
    global lat, lon

    lat = readFile(getPath(config["lat_path"]))
    lon = readFile(getPath(config["lon_path"]))
    if lon and lat == "0":
        SophiaCommunication(
            "Your location's coordinates are not set. Please open Sophia's app and go to settings to set one!")
        return
    currentWeather_url = config["weather_url"].format(lat, lon)
    req = requests.get(currentWeather_url)
    current_weather_response = req.json()
    description = current_weather_response["weather"]
    main = current_weather_response["main"]
    wind = current_weather_response["wind"]
    temp = main["temp"]
    humidity = main["humidity"]
    feelsLike = main["feels_like"]
    windSpeed = wind["speed"]
    msg = config["weather_msg"].format(temp, windSpeed, humidity, feelsLike, description[0]["description"])
    SophiaCommunication(msg)
    if description[0]["main"] == "Rain":
        SophiaCommunication("I recommend you bring an umbrella, it is raining!")


def news():
    query_params = {"source": "bbc-news", "sortBy": "top", "apiKey": "4dbc17e007ab436fb66416009dfb59a8"}
    main_url = " https://newsapi.org/v1/articles"
    res = requests.get(main_url, params=query_params)
    open_bbc_page = res.json()
    article = open_bbc_page["articles"]
    results = []
    for ar in article:
        results.append(ar["title"])
    for i in range(5):
        SophiaCommunication(results[i])


def Time():
    SophiaCommunication("The current time is {}.".format(datetime.datetime.now().strftime("%H:%M")))


def coin():
    num = random.randint(1, 2)
    if num == 1:
        SophiaCommunication("Heads!")
    else:
        SophiaCommunication("Tails!")


def date():
    SophiaCommunication("Today's date is {}.".format(datetime.datetime.now().strftime('%Y-%m-%d')))


def sayWord(cmd):
    word = cmd.replace("say", "")
    SophiaCommunication(word)


def play(cmd):
    video = cmd.replace("play", "")
    SophiaCommunication("Playing{}!".format(video))
    pywhatkit.playonyt(video)


def listeningForTodoMsg():
    global newTodoListening
    newTodoListening = True
    SophiaCommunication("I'm listening to your todo...")


def systemInformation(cmd):
    my_system = platform.uname()
    if "cpu" in cmd:
        SophiaCommunication("Cpu's percentage: {}%".format(psutil.cpu_percent()))
    if "ram" in cmd:
        SophiaCommunication("Ram's percentage: {}%".format(psutil.virtual_memory().percent))
    if "system" in cmd:
        SophiaCommunication("Operation system: {}.".format(my_system.system))


def locationSearch(cmd):
    data = cmd.replace("where is", "")
    SophiaCommunication("Here's what i found.")
    location_url = "https://www.google.com/maps/place/" + data
    webbrowser.open(location_url)


def quote():
    SophiaCommunication(stormconsultancy())


def joke():
    SophiaCommunication(chucknorris())


def Sophia(cmd):
    try:
        if "who is" in cmd:  # person definition by name with wikipedia
            personDefinition(cmd)
        elif "time" in cmd:  # current time
            Time()
        elif "date" in cmd:  # current date
            date()
        elif "what is" in cmd and not checkSentence(whatInspections, cmd):  # object definition by name with wikipedia
            objectDefinition(cmd)
        elif "play" in cmd:  # playing music/video on youtube
            play(cmd)
        elif "say" in cmd:  # saying words
            sayWord(cmd)
        elif "quote" in cmd:  # quote
            quote()
        elif "joke" in cmd:  # jokes
            joke()
        elif "open" in cmd:  # opening websites
            openWebsites(cmd)
        elif "news" in cmd:  # daily news
            news()
        elif "flip a coin" in cmd:  # coin flipping
            coin()
        elif "where is" in cmd:  # location on maps
            locationSearch(cmd)
        elif checkSentence(weather_wake, cmd):  # current weather
            weather()
        elif checkSentence(greeting_wake, cmd):  # greetings
            greeting()
        elif checkSentence(newTodo_wake, cmd):  # new task
            listeningForTodoMsg()
        elif checkSentence(showTodo_wake, cmd):  # see your given task
            msg = readFile(todo_path)[1:-1]
            SophiaCommunication(msg)
        elif checkSentence(pcInfo_wake, cmd):  # pc's specs
            systemInformation(cmd)
        else:
            try:
                SophiaCommunication(aiml_kernel.respond(cmd))
            except KeyError:
                SophiaCommunication("I found an error in my libraries while finding the answer, please don't ask that answer again!")
    except Exception as err:
        writeToFile(getPath(config["error"]), err)


def analyzing(cmd):
    global newTodoListening

    if cmd is not None:
        if checkSentence(sophia_wake, cmd):
            cmd = cmd.replace(usedSophiaWakeWord, "")
            print("\33[32mYou:{}".format(cmd))
            Sophia(cmd)
        elif newTodoListening:
            print("\33[32mYou:{}".format(cmd))
            newTodoListening = False
            saveFile(todo_path, cmd)
            SophiaCommunication("I saved your todo!")


def startup():
    if os.path.isfile("bot_brain.brn"):
        aiml_kernel.bootstrap(brainFile="bot_brain.brn")
    else:
        aiml_kernel.bootstrap(learnFiles=getPath(config['startUp']), commands="load aiml b")
        aiml_kernel.saveBrain("bot_brain.brn")
    if isReqInstalled:
        writeToFile(getPath(config["reqIs"]), "1")
    if errorWithReq:
        SophiaCommunication(config["reqError"])
        webbrowser.open("https://discord.gg/n78CsGwKt3")
        webbrowser.open("https://r2systems.000webhostapp.com/")
    writeToFile(getPath(config["exit_path"]), "0")
    writeToFile(getPath(config["running"]), "1")
    SophiaCommunication("Im listening to your commands!")


def speechRecognition():
    global newTodoListening, usedSophiaWakeWord
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            if ambient == "1":
                recognizer.adjust_for_ambient_noise(source, duration=1)
            Voice = recognizer.listen(source, timeOut, phrase_time_limit=timeOut)
            cmd = recognizer.recognize_google(Voice, language="en-US").lower()
            return cmd
    except sr.WaitTimeoutError:
        pass
    except sr.UnknownValueError:
        pass
    except sr.RequestError:
        pass


startup()

while True:
    try:
        checkForExit()
        command = speechRecognition()
        analyzing(command)
    except Exception as e:
        writeToFile(getPath(config["error"]), e)
