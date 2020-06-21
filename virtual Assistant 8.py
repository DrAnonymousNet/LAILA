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
from nooradb import*
import calendar
import threading
import time
import datetime as dt
import subprocess
import bs4
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
#import nooradb
import pyautogui
import goslate
import urllib
from twilio.rest import Client

# in the block above, all needed library are installed
global flag
flag = True

app_id = "86AT7X-523WTL6JVH"
client = wolframalpha.Client(app_id=app_id)


# we have our wolfram api key here
#HELPERS
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
            speak('HI, THE NETWORK IS DOWN, DO YOU WANT TO SWITCH  TO TEXT INPUT')
            yes_no = input('YESS/NO: ')
            if yes_no.lower() == "yes":
                speak("TEXT INPUT ACTIVATED")
                var: bool = False
                flag = var
                print(flag)
                return change_text()
            #SO , If you insisted on leavinng it at voice input, Flag
            #will remain at true and change_to_voice will be returned
            if yes_no.lower() == "no":
                flag = True
                return change_to_voice()

        return said.lower()
    except:
        return get_audio()


def get_input():
    "This function handles all form of text input"
    global flag
    said = input("Enter your command: ")
    said = said.lower()

    #At any moment you feel like changing to voice input, then this haandles it
    if said.lower() == "voice input":
        flag =True
        speak("I am switching to voice input")

        get_audio()
    return said

def change_to_voice():
    """This function runs if we are in voice input and handles all command related to
    voice input"""
    global text
    global flag
    print(flag)
    while True:
        text = get_audio() #We listen to a command here, and its stored in text variable

        text = wake_up(text) #Text is passed into the wake up call, which chelk iff the wake up call is heard
                            #and when the wakeup call is heard, it awiat your command. and the command given is
                            #returned and pass into text variable
        print(text)
        if text is not None: #This will only run if the value returned tot the text variable is not none
            while True:
                while flag == True:
                    print(flag)
                    actions(text) #The Action function execute the command given

                    return change_to_voice() #This will forever returned so far flag is true

def change_text():
    "just like chang_to_voice handles the VOICE input, this handles the text input"
    global flag
    global text
    print(flag)
    flag = False
    text = input("Ënter your command: ")
    print(text)
    text = wake_up(text)
    print(text)
    if text is not None:
        while True:
            while flag == False:
                print(flag)
                actions(text)

                return change_text()


def wake_up(text):
    global flag
    # This function receives a parameter from change_to_voice or change_text
    #depending on the value of flag and return the command given back to either of them
    #which is inturn executed by the action function
    try:
        print(text)
        wakeup_call = ["laila" ,"elena", "leila" , "leyla" , "layla", "lila"]  # when he hears this (Her name), He wakes up
        greetings = ["Hello sir", "Hi Ahmad", "yes Doctor"]

        for t in text.lower().split(" "):

            if t in wakeup_call and len(text.split(' ')) <= 2:
                speak(choice(greetings))  # This gives randomness to the greeting

                if flag == False:
                    speak("How can i help you")
                    text = input("what do u want:").lower()



                    return text
                elif flag == True:
                    speak("How can i help you: ")
                    text = get_audio().lower()


                    return text
            elif t  in wakeup_call and len(text.split(" ") )> 2:
                speak(choice(greetings))
                return text
        #If  no command was given or her name is not heard, the a none value will be returned back to either of the the that are mentioned
        #ABOVE
        if flag:
            return change_to_voice()
        elif flag == False:
            return change_text()
    except :
        return

def actions(text):
    global flag
    "This function receive command from the either oof the two form of input and compare the command to the \
    database of LAILA , if any command is seen, the command is executed"
    text_list = text.split(' ')
    count = 0
    for c in text_list:
        print(c)
        if  c in wikipedia_prompt or text in wikipedia_prompt :
            return answer_questions(text)
        if c in wolphram_prompt or " ".join(text_list[:count]) in wolphram_prompt:
            return answer_questions(text)

        elif c in note_str or text in note_str:
            return note(c)
        elif c in calculator_command or text in calculator_command:
            return show_calculator()
        elif  text in in_calculator_prompt:
            return in_calculator(text)
        elif c in set_alarm_prompt or text in set_alarm_prompt:
            mess = text.split(" ")
            thread_object = threading.Thread(target=ring_alarm, args=[mess])
            thread_object.start()

            time.sleep(20)

            return change_text()
        elif c in play_song_command or text in play_song_command:

            thread_object = threading.Thread(target= get_mp3)
            thread_object.start()

            time.sleep(2)
            if flag == True:
                return change_to_voice()
            elif flag == False:
                return change_text()
        elif c in news_prompt or text in news_prompt:
            return get_news_head()
        elif c in my_self_prompt or text in my_self_prompt:
            return my_Self()
        elif c in virtual_key_prompt or text in virtual_key_prompt:
            pass
        elif c in translator_prompt or text in translator_prompt:
            return translators()
        elif c in editor_mode_prompt or text in translator_prompt  :
            pass
        elif c in send_reminder or text in send_reminder:
            mess = text.split(" ")
            thread_object = threading.Thread(target=whatsapp_reminder, args=[mess])
            thread_object.start()
            time.sleep(60)
            return change_to_voice()
        elif c in sec_mode_act or text in sec_mode_act:
            return secretatry_mode()
        elif c in sched:
            return scheduler(text)
        elif c in text_:
            flag = False
            speak("text input activated")
            return change_text()
        elif c in voice_:
            flag = True
            speak("voice input activated")
            return change_to_voice()
        elif c == "love":
            speak("I Love you too , but no string attached")
            return 
        elif c == "time":
            pass
        count +=1
    speak("Sorry , i DIDNT GET THAT")
    if flag == True:
        change_to_voice()
    elif flag == False:
        change_text()



#ABOUT
def my_Self():
    "This function is run from by ACTION function and it contain everything yoou might neeed\
    to know about LAILA"
    speak("what do you want to know about me")
    if flag:
        text = get_audio()
    elif flag == False:
        text = input("Enter your command: ")
    date_of_birth = "12th of June 2020 "
    response = """My name is  LAILA , a multipurpose virtual assistant bot 
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


#ONLINE FUNCTIONS (Everything under this contain all functions that requires internet connection before they are exccuted)

def get_news_head():
    "This function gives the NEWS HEADLINE taken from GOOGLE NEWS"
    speak("OK SIR")
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


def answer_questions(text):
    # This is well she does most his question answering
    text_s = text.lower().split(" ")
    for c in wikipedia_prompt:
        if c in text:
            for i in range(len(text_s)):
                if text_s[i] == "who" and text_s[i + 1] == "is":
                    #try:
                    res = wikipedia.summary(" ".join(text_s[i + 2:]), sentences=2)
                    return speak(res)
                    #except:
                    return speak("Sorry , I dont have anything on " + " ".join(text_s[i + 2:]))
                elif text_s[i] == "tell" and text_s[i + 2] == "about":
                    #try:
                    res = wikipedia.summary(" ".join(text_s[text_s.index("about") + 1:]))
                    return speak(res)
                    #except:
                        #return speak("Sorry , I dont have anything on " + " ".join(text_s[text_s.index("about") + 1:]))
    try:
        for c in wolphram_prompt:
            if c in text:
                for i in range(len(text_s)):
                        if (text_s[i] == "what" and text_s[i + 1] == "is") and "time" not in text:
                            res = client.query(" ".join(text_s[text_s.index(" "):]))
                            return speak(next(res.results).text)
                        elif text_s[i] == "define":
                            res = client.query(text)
                            return speak(next(res.results).text)
                        else:
                            res = client.query(text)
                            return speak(next(res.results).text)
    except:
        try:
            res = wikipedia.summary(" ".join(text_s[text_s.index(" "):]))
            speak(res)
        except:
            return speak("sory, I dont know")

def translators():
    speak("ok sir")
    if flag:
        speak("what should i translate")
        text = get_audio()
    elif flag == False:
        speak("Enter the sentence you want to translate")
        text = input('input your text: ')

    try:
        gs = goslate.Goslate()
        if flag == False:
            speak("which language do u want to translate to")
            to_what = input("which language do u want to tranalate to: ").title()
        if flag:
            speak("which language do u want to translate to")
            to_what = get_audio().title()
        translated = gs.translate(text, lang_dict[to_what])

        speak(translated)

    except urllib.error.HTTPError:
        speak("Service overloaded")
    except urllib.error.URLError:
        speak("No Network")

def note(text):
    # This allows me to note things down using notepad
    date = datetime.datetime.now()
    file_name = str(date).replace(":", "_") + ".txt"
    file_names = str(date).replace(":", "_") + ".txt"

    var = text
    path = fr"C:\Users\USER\PycharmProjects\LAILA\secretary\{file_name}"
    if "write" in var or "yes" in text:
        speak("what should i write")
    else:
        speak("what should i note")

    if flag:
        texts = get_audio()
    elif flag == False:
        texts = input("what should i note: ")


    with open(path, "w") as file:
        file.write(texts)
    subprocess.Popen(["notepad.exe" , path])


    speak("written sir")
    return texts

#TIME RELATED FUNCTIONS
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
                    if "reminder" in text:
                        speak("reminder set to " + time_f.strftime("%I:%M  %p "))
                        print("reminder set to " + time_f.strftime("%I:%M  %p "))
                        return time_f
                    elif "alarm" in text:
                        speak("Alarm set to " + time_f.strftime("%I:%M  %p "))
                        print("Alarm set to " + time_f.strftime("%I:%M  %p "))
                        return time_f

                if c.startswith('h'):
                    delta_init += dt.timedelta(hours=int(texts[i - 1]))
                    time_f = delta_init + recent_date
                    if "reminder" in text:
                        speak("reminder set to " + time_f.strftime("%I:%M  %p "))
                        print("reminder set to " + time_f.strftime("%I:%M  %p "))
                        return time_f
                    elif "alarm" in text:
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
                        if alarm_time < dt.datetime.now():
                            alarm_time += dt.timedelta(days= 1)
                    elif len(t) == 1 or len(t) == 2:
                        if len(t) == 1:
                            t = int(t) + 12


                        alarm_time = dt.datetime(recent_date.year, recent_date.month, recent_date.day, int(t))
                        if alarm_time < dt.datetime.now():
                            alarm_time += dt.timedelta(days= 1)
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
            if "alarm" in text:
                speak("Alarm set to " + alarm_time.strftime("%H:%M  %p %A ,%d of %B  %Y"))
                print("Alarm set to " + alarm_time.strftime("%H:%M  %p %A ,%d of %B  %Y"))
                return alarm_time
            elif "reminder" in text:
                speak("reminder set to " + alarm_time.strftime("%H:%M  %p %A ,%d of %B  %Y"))
                print("reminder set to " + alarm_time.strftime("%H:%M  %p %A ,%d of %B  %Y"))
                return alarm_time
        elif delta_init + recent_date != recent_date:
            time_f = delta_init + recent_date
            if "alarm" in text:
                speak("Alarm set to " + time_f.strftime("%I:%M  %p "))
            elif "reminder" in text:
                speak("reminder set to " + time_f.strftime("%I:%M  %p "))

            return time_f

    except :
        speak("That's an invalid input")
        if flag == False:
            change_text()
        elif flag == True:
            change_to_voice()

def ring_alarm(mess):
    mag = False
    for c in mess:
        if c in meridiem or c in time_related:
            mag = True
            break
    if mag:
        mess = " ".join(mess)
        time_set = set_alarm(mess)
    elif mag == False:
        speak("what time do you want to set alarm to")
        if flag:
            text = get_audio()
        elif flag == False:
            text = input("What time do you want to set alarm to: ")
        "This is where the alarm is rang oncee its time"
        time_set = set_alarm("alarm " +  text)
    while dt.datetime.now() < time_set:
        time.sleep(1)
    playsound.playsound("swinging.mp3")
    return change_to_voice()


def whatsapp_reminder(mess):

    client = Client(acc_sid, acc_token)
    mag = False
    for c in mess:
        if c in meridiem or c in time_related:
            mag = True
            break

    if mag == False:
        mess = " ".join(mess)


    elif mag == True:
        speak("what time do you want to set the reminder to")
        if flag:
            text = get_audio()
            time_set = set_alarm("reminder " + text)
            speak("what is the reminder message")
            mess = get_audio()
        elif flag == False:
            text = input("What time do you want to set reminder to: ")
            time_set=  set_alarm("reminder " + text)
            speak("what is the reminder messagee")
            mess = input("type the mesage: ")

    if mag:
        while dt.datetime.now() < time_set:
            time.sleep(1)

    # this ishe Twilio sandbox testing number
    from_whatsapp_number = 'whatsapp:+14155238886'
    # replace this number with your own WhatsApp Messaging number
    to_whatsapp_number = 'whatsapp:+2348065007606'

    client.messages.create(body=mess,
                           from_=from_whatsapp_number,
                           to=to_whatsapp_number)
    speak("message sent")


#ARITHMETIC FUNCTIONS

def show_calculator():
    speak("ok sir")
    subprocess.Popen(['C:\\Windows\\System32\\calc.exe'])

def in_calculator(text):
    speak("calculator activated")
    speak("what do u want to compute")
    if flag == False:
        text_split = input("what do u want to compute: ").split(" ")
    elif flag:
        text_split = get_audio().split(' ')
    if "convert" not  in text_split:
        sums = int(text_split[0])
    elif "convert" in text_split:
        sums = int(text_split[1])
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

#MEDIA
def get_mp3():
    try:
        while True:
            randomfile = random.choice(os.listdir("C:\Music\\"))
            if randomfile[-3:] == "mp3":
                break

        print(randomfile)
        file = "C:\Music\\" + randomfile

        playsound.playsound(file, True)
    except playsound.PlaysoundException :
        speak("An Mp3 was not generated")

#def word_processor():
#    speak ("ok sir")
#   subprocess.Popen(pass)



# Your Account Sid and Auth Token from twilio.com/console

def text_me(message):
    phone_num = "+12029335461"

    client = Client(acc_sid, acc_token)

    message = client.messages.create(body=message, from_=phone_num,
                                     to='+2348050664320')

    print(message.sid)

# SECRETARY MODE
in_office = "yes"
# Administrative Functions
def in_office_set(text):
    global in_office
    if "no" in text:
        in_office = "No"
    elif "yes" in text:
        in_office = "yes"
    elif "busy" in text:
        in_office = "busy"

    speak(f"in office mode set to {in_office}")
    return in_office.lower()


def check_in_office(text):
    speak("in office mode is set to " + in_office)
    return

def in_office_or_home(text):
    if in_office.lower() == "yes":
        speak("yes, he is around")
    elif in_office.lower() == "no":
        speak("No")
        speak("Do you want to leave a note")
        if flag:
            decision = get_audio()
        elif flag == False:
            decision = input("Do you want to leave a note: ")
        if "yes" in decision:
            message_ = note(decision)
            whatsapp_reminder(message_)
        elif "no" in decision.lower():
            speak("ok sir")

    elif in_office == "busy":
        speak("yes, but Not ready to see anyone, but do you want to leave a note ?")
        decision = input("wanna leave a note: ")
        if "no" in decision.lower():
            return speak("ok sir")
        elif "yes" in decision:
            message_ = note(decision)
            whatsapp_reminder(message_)
    return speak("thank you")


def do_i_have_a_message():
    pass

def secretatry_mode():
    speak("secretatry mode activated")
    while True:
        if flag:
            text = get_audio()
            texts = text.split(" ")
        elif flag == False:
            text = input("enter command:  ")
            texts = text.split(" ")
        for c in texts:
            if c in in_office_orhome:
                in_office_or_home(text)
            elif c in set_office_home_mode:
                in_office_set(text)
            elif c in check_in_office_mode:
                check_in_office(c)
            elif c == "exit" or c == "quit":
                speak("ok sir")
                return change_to_voice()


#SCHEDUKER MODE
todays =datetime.date.today()
file_name = str(todays).replace(":", "_") + ".txt"
path = fr"C:\Users\USER\PycharmProjects\LAILA\Schedules\{file_name}"
def makie_schedules():
    speak("ok, what should i add")
    lisd = []
    tag = True
    while tag:
        if flag:
            sch_list = get_audio()
        elif flag ==False:
            sch_list = input("Enter your schedule:")

        if "all" in sch_list:
            speak("Ok sir")
            break
        speak("ok, next")
        lisd.append(sch_list)

    with open(path, "a") as file:
        for c in lisd:
            file.write(c + "\n")

    speak("All added sir")

def scheduler(get_command):
    file_no = len(os.listdir(r"C:\Users\USER\PycharmProjects\LAILA\Schedules"))
    available = os.path.isfile(path)
    #get_command =input("want to do: ").lower()
    if "add" in get_command or "make" in get_command:
        makie_schedules()
    elif "check" in get_command or "do" in get_command:

        if available == False and "do" in get_command:
            speak("No sir, do u wantt to make schedules")
            if flag == False:
                des = input("yes_no: ").lower()
            elif flag:
                des = get_audio().lower()
            if des.lower() == "yes":
                makie_schedules()
            else:
                speak("ok sir")

        elif available == True and "do" in get_command:
            speak("yes")


            speak("should i read them")
            if flag:
                yes_no = get_audio().lower()
            elif flag == False:
                yes_no = input("yes_no: ").lower()
            if yes_no == "yes":
                speak("Here are your schdules for today")
                with open(path, "r") as file:
                    speak(file.read())

                speak("that's all you have for now")
            elif yes_no == "no":
                speak("ok sir")

        elif "check" in get_command:
            if available == False:
                speak("You dont have a schedule sir, Do you want to make schedule")
                if flag:
                    des = get_audio().lower()
                elif flag == False:
                    des = input("yes_no: ").lower()
                if des == "yes":
                    makie_schedules()
                else:
                    speak("ok sir")
            elif available:
                speak("ok sir , here are your schedules for today")
                with open(path, "r") as file:
                    speak(file.read())

    elif "what" in get_command:
        if available == False:

            speak("you dont have any schedule for today, do you want to add")
            if flag:
                des = get_audio().lower()
            elif flag == False:
                des = input("yes_no: ").lower()
            if des == "yes":
                makie_schedules()
            else:
                speak("ok sir")

        elif available:
            speak("your schedules for today are :")
            with open(path, "r") as file:
                speak(file.read())

if flag:
    change_to_voice()
elif flag  == False:
    change_text()
