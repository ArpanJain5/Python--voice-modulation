import pyttsx3 # Voice Recognition (Base of AI)
import datetime # Date and time
import requests # For Weather
import speech_recognition as sr # Speech Recognition
import pyautogui # WhatsApp Imports
import webbrowser as wb 
from time import sleep  # Whatsapp delay 
import wikipedia # Wikipedia Search 
import pywhatkit # Youtube Videos
import bs4 # Weather
from newsapi import NewsApiClient # News
import os   # For remeber function
import psutil   # CPU_Battery usage

# Initializing voice
engine = pyttsx3.init()

def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    
# Male / female Voice
def getvoices(voice):
        voices = engine.getProperty("voices")
        if voice == 1 :
            engine.setProperty("voice",voices[0].id)
            speak('Hello, This is Jarvis')
            print('JARVIS initialized')
        
        if voice == 2 :
            engine.setProperty("voice",voices[1].id)       
            speak('Hello, This is Friday')
            print('FRIDAY initialized')

def time():
    Time = datetime.datetime.now().strftime('%I:%M:%S')
    speak("The Current time is : ")
    print(Time)
    speak(Time)

def date():
    year = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    date = int(datetime.datetime.now().day)
    speak("The Current Date is : ")
    print(date, month, year)
    speak(date)
    speak(month)
    speak(year)

def greeting():
    hour = datetime.datetime.now().hour
    if hour >= 6 and hour < 12:
        speak("Good morning sir!")
    elif hour >= 12 and hour < 18:
        speak("Good afternoon sir!")
    elif hour >= 18 and hour < 24:
        speak("Good evening sir!")
    else:
        speak("Good night sir!")

def wishme():
    greeting()
    speak('AI At your service, How Can I Help U')

# Using Text
def commandCMD():
    print("Please tell me how can I help you?\n")
    query = input("Enter input: ")
    return query

# Hands-free/Using Speech
def commandMIC():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        r.pause_threshold = 1
        audio = r.listen(source)
        r.adjust_for_ambient_noise(source)
    try:
        print('Recognizing...')
        query = r.recognize_google(audio,language="en-IN")
        print(query)
    except Exception as e:
        print(e)
        speak('Say that Again..')
        return "none" 
                 
    return query

# Whatsapp
def sendwpmsg(phone,msg):
    Msg = msg
    wb.open('https://web.whatsapp.com/send?phone='+phone+'&text='+Msg)
    sleep(10)
    pyautogui.press('enter')

# Google Search
def googleSearch():
    speak("What should I search for?")
    print("What should I search for?")
    search = commandMIC()
    wb.open('https://www.google.com/search?q='+search)

# Weather
def weather():
    speak("Name the city?")
    cityName = commandMIC()
    search = f'temperature in {cityName}'
    url = f"https://www.google.com/search?q={search}"
    r = requests.get(url)    
    data = bs4.BeautifulSoup(r.text,"html.parser")
    temp = data.find("div",class_="BNeawe").text
    print(f"Current {search} is {temp}")
    speak(f"Current {search} is {temp}")

# News
def news():
    newsapi = NewsApiClient(api_key = '64e7361636b44727b988428e1df0ccc1')
    data = newsapi.get_top_headlines(q='latest',language='en',page_size=3)
    newsdata = data['articles']
    for x,y in enumerate(newsdata):
        print(f'{x+1}. {y["description"]}')
        speak((f'{x+1}{y["description"]}'))  
    speak("That's all for now, I will update in some time.")

# Remember
def remember():
    speak("what should I remember?")
    data=commandMIC()
    speak("you said me to remember that "+data)
    remember=open('data.txt','w')  
    remember.write(data)
    remember.close()

# Battery 
def cpu_battery():
    usage = str(psutil.cpu_percent())
    speak('CPU is at '+usage+' percent usage')
    print('CPU is at '+usage+' percent usage')
    battery = psutil.sensors_battery()
    speak("Battery is at ")
    speak(battery.percent)
    speak('percent')


if __name__ == '__main__':
    # Jarvis / Friday Choosing
    number = int(input('Press 1 for Jarvis \nPress 2 for Friday \n'))
    getvoices(number)
    wishme()
    while True:
        # query = commandCMD().lower()
        query = commandMIC().lower()
        
        if 'time' in query:
            time()
            
        elif 'date' in query:
            date()

        elif 'message' in query:
            speak('Please enter Name and phone number:')
            name = input("Name: ")
            phone = input("Phone number: ")
            username = {name:phone}
            try:
                phone = username[name]
                speak("What is the message to send?")
                print("What is the message to send?")
                msg = commandMIC()
                sendwpmsg(phone,msg)
                speak("Message sent!")
                print("Message sent!")

            except Exception as e:
                print(e)
                speak("Unable to send message")

        elif 'hello google' in query:
            googleSearch()
        
        elif 'wikipedia' in query:
            speak('Searching On Wikipedia..')
            query = query.replace('wikipedia','')
            result = wikipedia.summary(query,sentences = 2)
            print(result)
            speak(result)

        elif 'youtube' in query:
            speak('Searching on Youtube..')
            topic=commandMIC()
            print('You searched for', topic)
            pywhatkit.playonyt(topic)
            break

        elif 'weather' in query:
            weather()

        elif 'news' in query:
            news()

        elif 'remember' in query:
            remember()
            
        elif 'do you know anything' in query:
            remember=open('data.txt','r')
            filesize = os.path.getsize("data.txt")
           
            if filesize == 0:
                speak("Sorry, you told me nothing!")
            else:
                speak("you told me to remember that "+remember.read())

        elif 'battery' in query:
            cpu_battery()

        elif 'quit' in query:
            speak('Have a good day sir')
            print('Have a good day sir')
            quit() 