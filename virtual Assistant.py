# This is a virtual assistant bot written by Dr.Anonymous
import pyttsx3
import speech_recognition as sr
import pyaudio
import datetime
import os, random
import playsound
import os
import wolframalpha
import wikipedia
from random import choice

import calendar
import threading
import time
import datetime as dt
import subprocess
import bs4
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
#import nooradb
import pyaut
import goslate
import urllib
from twilio.rest import Client


acc_sid = "AC221f4496a708695971f54efbf70d222c"

acc_token = "35ed4d199954472a15d7627890778047"
# in the block above, all needed library are installed

# Answering questions keyword


# Alarm and time keyword

time_related = ['days', 'hours', 'minutes', 'seconds', 'minute', 'hour']
watch_out = ['tomorrow', 'today']
week_days = ['sundays', 'mondays', 'tuesday', 'wednesday', 'friday', 'saturday']
meridiem = ['a.m.', 'p.m.']
set_alarm_prompt = ["alarm"]
send_reminder =["send", "reminder"]

# Note making keyword
note_str = ["note", "make a note", "write this down", "take this down"]

# calculator keyword
calculator_term = ['-', '+', '*', '/', 'plus', 'minus', 'multiply', 'divided', 'base']
calculator_command = ["pop me a calculator", "get me a calculator", "i need a calculator"]
in_calculator_prompt = ["activate calculator"]

#General keys
wikipedia_prompt = ["about", "who is","who"]
wolphram_prompt = ["what is", "define", "integrate", "differentiate", "meaning", 'temperature']
play_song_command = ["play me a song", "song"]
news_prompt = ["news", "news headline" , "headline"]
virtual_key_prompt = ["virtual", "keyboard"]
translator_prompt = ["translate"]
editor_mode_prompt = ["editor"]

#About NOORA
my_self_prompt = ["features"]
functionalities = ["Calculator functions", "setting reminders", "setting alarm", "playing song", "virtual keyboard", "translator function", "note makeingh", "wiki search" , "mathematical computations", "getting news"]
online_features = ["getting news", "language translation", "web searching", "sending reminder"]
features = ["online features" , "offline features", "blind features", "mathematical features"]
offline_features = ["getting calculator", "playing song", "basic mathematical computation", "virtual keyboard", "keeping note"]
blind_features = ["activating voice command keyboard", "voice input", "opening apps", "voice typing", "note making"]

global flag

flag = True

app_id = "86AT7X-523WTL6JVH"
client = wolframalpha.Client(app_id=app_id)


# we have our wolfram api key here

def speak(text):
    # This function returns everything drano wish to say
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)
    engine.setProperty("volume", 0.9)
    engine.say(text)
    print(text)
    engine.runAndWait()


def get_audio():
    global flag
    try:



        # this function allows voice input command
        r = sr.Recognizer()  # the regognizer class was initiated
        r.energy_threshold = 1200
        with sr.Microphone() as source:
            print("listning.............")

            audio = r.listen(source)

            said = ''


        try:
            print("understanding.......")
            # we check if our voice was taken in
            said = r.recognize_google(audio)
            print(said)



        except sr.RequestError:
            speak('Do you want to switch to text input')
            yes_no = input('YESS/NO: ')
            if yes_no.lower() == "yes":
                speak("I am switching to text input")
                var: bool = False
                flag = var
                print(flag)
                return change_text()

            if yes_no.lower() == "no":
                flag = True
                return change_to_voice()

        return said.lower()
    except:
        return get_audio()


def get_input():
    global flag
    said = input("Enter your text: ")
    if said.lower() == "voice input":
        flag =True
        speak("I am switching to voice input")

        get_audio()
    return said




def my_Self():
    speak("what do you want to know about me")
    if flag:
        text = get_audio()
    elif flag == False:
        text = input("Enter your command: ")
    date_of_birth = "12th of June 2020 "
    response = """My name is  NOORA , a multipurpose virtual assistant bot 
                created by Ahmad."""
    if "features" in text or "feature" in text:
        speak("My features include: ")
        for i in features:
            speak(i)
    if "function" in text or "functions" in text:
        speak("My functionalities include: ")
        for i in functionalities:
            speak(i)
    if "online" in text:
        speak("my online features are: ")
        for i in online_features:
            speak(i)
    if "self" in text:
        speak(response)


    speak(response)


def answer_questions(text):
    # This is well she does most his question answering
    text_s = text.lower().split(" ")

    for c in wikipedia_prompt:
        if c in text:
            for i in range(len(text_s)):

                if text_s[i] == "who" and text_s[i + 1] == "is":
                    try:
                        res = wikipedia.summary(" ".join(text_s[i + 2:]), sentences=3)
                        return speak(res)
                    except:
                        return speak("Sorry , I dont have any on " + " ".join(text_s[i + 2:]))

                elif text_s[i] == "tell" and text_s[i + 2] == "about":

                    try:
                        res = wikipedia.summary(" ".join(text_s[text_s.index("about") + 1:]))
                        return speak(res)
                    except:
                        return speak("Sorry , I dont have any on " + " ".join(text_s[text_s.index("about") + 1:]))

    for c in wolphram_prompt:
        if c in text:
            for i in range(len(text_s)):
                if (text_s[i] == "what" and text_s[i + 1] == "is") and "time" not in text:
                    res = client.query(text)
                    return speak(next(res.results).text)
                elif text_s[i] == "define":
                    res = client.query(text)
                    return speak(next(res.results).text)
                else:
                    res = client.query(text)
                    return speak(next(res.results).text)

    return speak("sory, I dont know")


def note(text):
    # This allows me to note things down using notepad
    date = datetime.datetime.now()
    file_name = str(date).replace(":", "_")
    var = text
    if "write" in var:
        speak("what should i write")
    else:
        speak("what should i note")

    if flag:
        texts = get_audio()
    elif flag == False:
        texts = input("what should i note: ")

    with open(file_name, "w") as file:
        file.write(texts)
    subprocess.Popen(["notepad.exe", file_name])
    return speak("written sir")


def set_alarm(text):
    "This function set an alarm"
    try:
        global temp_time
        alarm_time = None
        recent_date = dt.datetime.now()  # this give the resent date time

        delta_init = dt.timedelta()  # a time delta was initiated, it allows us to add date/time

        texts = text.split(" ")  # we split the input text

        for i, c in enumerate(texts):
            if c in time_related:

                if c.startswith('m'):

                    delta_init += dt.timedelta(minutes=int(texts[i - 1]))
                    time_f = delta_init + recent_date


                    speak("Alarm set to " + time_f.strftime("%I:%M  %p "))
                    print("Alarm set to " + time_f.strftime("%I:%M  %p "))
                    return time_f

                if c.startswith('h'):
                    delta_init += dt.timedelta(hours=int(texts[i - 1]))
                    time_f = delta_init + recent_date

                    speak("Alarm set to " + time_f.strftime("%I:%M  %p "))
                    print("Alarm set to " + time_f.strftime("%I:%M  %p "))
                    return time_f
            elif c in watch_out:

                if c == 'tomorrow' and 'p.m.' in texts:

                    t = texts[texts.index('p.m.') - 1]
                    if ":" in t:
                        t = t.split(":")
                        temp_time = dt.datetime(recent_date.year, recent_date.month, recent_date.day, int(t[0]), int(t[1]))
                    elif len(t) == 1:

                        temp_time = dt.datetime(recent_date.year, recent_date.month, recent_date.day, int(t))
                    alarm_time = dt.timedelta(days=1) + temp_time

                elif c == 'tomorrow' and 'a.m.' in texts:
                    t = texts[texts.index('a.m.') - 1]
                    if ":" in t:
                        t = t.split(":")
                        temp_time = dt.datetime(recent_date.year, recent_date.month, recent_date.day, int(t[0]), int(t[1]))
                    elif len(t) == 1:
                        temp_time = dt.datetime(recent_date.year, recent_date.month, recent_date.day, int(t))
                    alarm_time = dt.timedelta(days=1) + temp_time


                elif c == 'tomorrow':
                    delta_init += dt.timedelta(days=1)

            if c in meridiem:
                if c == 'p.m.' and ('tomorrow' not in texts or 'today' in texts):
                    t = texts[i - 1]
                    if ":" in t:
                        t = t.split(":")
                        if len(t[0]) == 1:
                            t[0] = int(t[0]) + 12

                        alarm_time = dt.datetime(recent_date.year, recent_date.month, recent_date.day, int(t[0]), int(t[1]))

                    elif len(t) == 1 or len(t) == 2:
                        if len(t) == 1:
                            t = int(t) + 12
                        alarm_time = dt.datetime(recent_date.year, recent_date.month, recent_date.day, int(t))
                        print(alarm_time)

                elif c == 'a.m.' and ('tomorrow' not in texts or 'today' in texts):
                    t = texts[i - 1]

                    if ":" in t:
                        t = t.split(":")

                        alarm_time = dt.datetime(recent_date.year, recent_date.month, recent_date.day, int(t[0]), int(t[1]))

                    elif len(t) == 1:
                        alarm_time = dt.datetime(recent_date.year, recent_date.month, recent_date.day, int(t))
                        print(alarm_time)



        if alarm_time:

            speak("Alarm set to " + alarm_time.strftime("%H:%M  %p %A ,%d of %B  %Y"))
            print("Alarm set to " + alarm_time.strftime("%H:%M  %p %A ,%d of %B  %Y"))
            return alarm_time
        elif delta_init + recent_date != recent_date:

            time_f = delta_init + recent_date

            speak("Alarm set to " + time_f.strftime("%I:%M  %p "))
            return time_f

    except :
        speak("That's an invalid input")
        if flag == False:
            change_text()
        elif flag == True:
            change_to_voice()

def ring_alarm():
    speak("what time do you want to set alarm to")
    if flag:
        text = get_audio()
    elif flag == False:
        text = input("What time do you want to set alarm to: ")
    "This is where the alarm is rang oncee its time"
    time_set = set_alarm(text)
    while dt.datetime.now() < time_set:
        time.sleep(1)
    speak("This is the time you set")





def in_calculator(text):
    speak("calculator activated")


    speak("what do u want to compute")
    if flag == False:
        text_split = input("what do u want to compute: ").split(" ")
    elif flag:
        text_split = get_audio().split(' ')
    sums = int(text_split[0])

    for i, c in enumerate(text_split):
        if c == '+' or c == 'plus':
            sums += int(text_split[i + 1])

        if c == '-' or c == 'minus':
            sums -= int(text_split[i + 1])

        if c == '*' or c == 'multiply':
            if c == "multiply" :
                sums *= int(text_split[i + 2])
            elif c == "*" :
                sums *= int(text_split[i + 1])

        if c == '/' or c == 'divided':
            if c == "divided":
                sums /= int(text_split[i + 2])
            elif c == "/":
                sums /= int(text_split[i + 1])

        if c == 'base' and int(text_split[i + 1]) == 10:

            def converter(num, base):

                rem = []

                while num != 0:
                    rem.append(str(num % base))
                    num = num // base

                    rem = rem[::-1]

                speak(''.join(rem))

            return converter(int(text_split[i - 1]), int(text_split[text_split.index('to') + 1]))
        if c == 'base' and int(text_split[i + 1]) < 10:

            def convert(num, base):

                m = []

                for i in range(len(str(num))):
                    m.append(int(str(num)[-(i + 1)]) * base ** i)

                speak(sum(m))

            return convert(int(text_split[i - 1]), int(text_split[i + 1]))

    speak(round(sums, 2))


def get_mp3():
    try:
        randomfile = random.choice(os.listdir("C:\Music\\"))
        file = "C:\Music\\" + randomfile

        playsound.playsound(file, True)
    except playsound.PlaysoundException :
        speak("An Mp3 was not generated")


def show_calculator():
    speak("ok sir")
    subprocess.Popen(['C:\\Windows\\System32\\calc.exe'])

#def word_processor():
#    speak ("ok sir")
#   subprocess.Popen(pass)



def EditorMode():
    text = input()

    def select_all():

        pyatutogui.hotkey('ctrl', 'a')
        return

    def copy(self):
        pyautogui.hotkey('ctrl', 'c')
        return

    def paste(self):
        pyautogui.hotkey('ctrl', 'v')

    if "paste" in text:
        paste()
    elif "copy" in text:
        copy()
    elif "select" in text:
        select_all()
    else:
        print("I did'nt get that")

    if "exit" in text:
        print("Ok boss")
        return

    return EditorMode()


def virtual_keyboard():
    text = input("Enter your text: ")
    f_keys = ['f1', "f2", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11", "f12"]

    volume_keys = ['volumemute', 'volumedown', 'volumeup']

    if 'volume' in text:
        text = text.split(" ")
        pyautogui.press("".join(text))
    if "type" in text:
        speak("Listning")

        text = input('Enter your text: ')
        pyautogui.typewrite(text)

    if "scroll" in text and "lock" not in text:
        if "down" in text:
            pyautogui.press('down')
        elif "up" in text:
            pyautogui.press('up')
        elif "left" in text:
            pyautogui.press("left")
        elif "right" in text:
            pyautogui.press("right")

        else:
            print("not gotten")

    if "enter" in text or 'newline' in text:
        pyautogui.press("enter")

    if "delete" in text:
        pyautogui.press("backspace")

    if "lock" in text:
        if "cap" in text:
            pyautogui.press("caplock")
        if "num" in text:
            pyautogui.press("numlock")

        if "scroll" in text:
            pyautogui.press("scrolllock")

        if text in f_keys:
            pyautogui.press(text)

    if "quit" in text:

        return
    else:
        return virtual_keyboard()


def translators():
    text = input('input your text: ')

    try:
        gs = goslate.Goslate()

        to_what = input("which language do u want to tranalate to: ").title()
        translated = gs.translate(text, lang_dict[to_what])

        print(translated)

    except urllib.error.HTTPError:
        print("Service overloaded")





# Your Account Sid and Auth Token from twilio.com/console

def text_me(message):
    phone_num = "+12029335461"

    client = Client(acc_sid, acc_token)

    message = client.messages.create(body=message, from_=phone_num,
                                     to='+2348050664320')

    print(message.sid)


# client credentials are read from TWILIO_ACCOUNT_SID and AUTH_TOKEN
def whatsapp_reminder():
    client = Client(acc_sid, acc_token)

    # this is the Twilio sandbox testing number
    from_whatsapp_number = 'whatsapp:+14155238886'
    # replace this number with your own WhatsApp Messaging number
    to_whatsapp_number = 'whatsapp:+2348065007606'

    client.messages.create(body='hello, world!',
                           from_=from_whatsapp_number,
                           to=to_whatsapp_number)
    speak("message sent")

def get_news_head():
    try:

        news_url = "https://news.google.com/news/rss"
        Client = urlopen(news_url)
        xml_page = Client.read()
        Client.close()

        soup_page = soup(xml_page, "xml")
        news_list = soup_page.findAll("item")
        # Print news title, url and publish date
        for news in news_list:
            speak(news.title.text)
    except urllib.error.URLError:
        speak("Sorry, Network is down now")
        if flag :
            change_to_voice()
        if flag == False:
            change_text()
class Input:

    def __init__(self):
        self.text_input = get_audio()

def actions(text):
    text_list = text.split(' ')
    for c in text_list:
        print(c)
        if  c in wikipedia_prompt or text in wikipedia_prompt :
            return answer_questions(text)

        elif c in note_str or text in note_str:
            return note(c)
        elif c in calculator_command or text in calculator_command:
            return show_calculator()
        elif c in in_calculator_prompt or text in in_calculator_prompt:
            return in_calculator(text)
        elif c in set_alarm_prompt or text in set_alarm_prompt:
            thread_object = threading.Thread(target=ring_alarm)

            thread_object.start()

            time.sleep(20)

            return change_text()
        elif c in play_song_command or text in play_song_command:
            return get_mp3()
        elif c in news_prompt or text in news_prompt:
            return get_news_head()
        elif c in my_self_prompt or text in my_self_prompt:
            return my_Self()
        elif c in virtual_key_prompt or text in virtual_key_prompt:
            pass
        elif c in translator_prompt or text in translator_prompt:
            pass
        elif c in editor_mode_prompt or text in translator_prompt  :
            pass
        elif c in send_reminder or text in send_reminder:
            pass

    speak("didnt get")
    if flag == True:
        change_to_voice()
    elif flag == False:
        change_text()

def wake_up(text):
    # This function wakes her up
    try:
        wakeup_call = ["Nura", "noora", "Nora" , "nora"]  # when he hears this (Her name), He wakes up
        greetings = ["Hello sir", "Hi Ahmad", "yes Doctor"]

        for t in text.split(" "):
            if t in wakeup_call:
                speak(choice(greetings))  # This gives randomness to the greeting
                print(flag)
                if flag == False:
                    text = input("what do u want:")
                    print(text)
                    return text
                elif flag == True:
                    speak("How can i help you: ")
                    text = get_audio()
                    print(text)
                    return text
        return
    except :
        return


#def change_to_voice():


#   while flag:
#        print(flag)
#        text = get_audio()
#        if flag == False:
#            break
#        actions(text)
#        return change_to_voice()


#    return

def change_to_voice():
    global text
    global flag
    while True:
        text = get_audio()

        text = wake_up(text)
        print(text)
        if text is not None:
            while True:
                while flag == True:
                    print(flag)
                    actions(text)

                    return change_to_voice()

def change_text():
    global flag
    global text
    flag = False
    text = input("Enter your command: ")
    text = wake_up(text)
    print(text)
    if text is not None:
        while True:
            while flag == False:
                print(flag)
                actions(text)

                return change_text()
change_to_voice()
