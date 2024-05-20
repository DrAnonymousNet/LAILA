# This is a virtual assistant bot written by Dr.Anonymous
import datetime
from dotenv import load_dotenv

import datetime as dt
import os
import random
import subprocess
import sys
import threading
import time
import urllib
from random import choice
from typing import Any, Union
from urllib.request import urlopen
from dateutil import parser
from pynput import keyboard
import goslate
import playsound
import pyttsx3
import speech_recognition as sr
import google.generativeai as genai

import wikipedia
import wolframalpha
from bs4 import BeautifulSoup as Soup
from twilio.rest import Client
from openai import OpenAI

from nooradb import *
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=gemini_api_key)

# my_assistants = open_ai_client.beta.assistants.list(
#     order="desc",
#     limit="20",
# )
# if my_assistants.data == []:
#     my_assistant = open_ai_client.beta.assistants.create(
#         instructions="You are a virtual assistant. Assist users with various tasks, answer questions, and provide helpful information.",
#         name="laila",
#         tools=[{"type": "code_interpreter"}],
#         model="gpt-3.5-turbo",
#     )
#     assistant_id = my_assistant.id

# else:
#     __import__("ipdb").set_trace()
#     assistant_id = my_assistants.data[0].id


# empty_thread = open_ai_client.beta.threads.create()
# thread_id = empty_thread.id
# # in the block above, all needed library are installed

flag = False
stop_thread = False

app_id = "86AT7X-523WTL6JVH"
client = wolframalpha.Client(app_id=app_id)

reminder_thread = 0
alarm_thread = 0
interrupted = False

# we have our wolfram api key here
# HELPERS
def speak(_text):
    global interrupted
    # This function returns everything drano wish to say
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)
    engine.setProperty("volume", 0.9)
    voices = engine.getProperty('voices')

    engine.setProperty('voice', 'com.apple.speech.synthesis.voice.samantha')
    def on_word(name, location, length):
        if interrupted:
            engine.stop()

    engine.connect('started-word', on_word)
    engine.say(_text)
    print(_text)
    try:
        engine.runAndWait()
    except RuntimeError as e:
        if engine._inLoop:
            engine.endLoop()

            
def interrupt_speak():
    global interrupted

    def on_press(key):
        global interrupted
        try:
            if key == keyboard.Key.esc:
                interrupted = True
                print("\n[Interrupt signal received]")
                return False  # Stop listener
        except AttributeError:
            pass

    # Collect events until released
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

def chat_with_gpt():
    threading.Thread(target=interrupt_speak, daemon=True).start()

    speak("natural language activated")
    prompt = get_input()
    model = genai.GenerativeModel('gemini-pro')
    chat = model.start_chat(history=[])
    while "exit" not in prompt:
        try:
            response = chat.send_message(prompt)
            speak(response.text)

        except ValueError:
            continue
        prompt = get_input()

    if 'exit' in prompt:
        speak("Natural language deactivated")



def list_voices():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for index, voice in enumerate(voices):
        print(f"Voice {index}: {voice.name}, Gender: {voice.gender}, ID: {voice.id}")

list_voices()


def get_audio():
    global flag
    try:
        # this function allows voice input command
        r = sr.Recognizer()  # the recognizer class was initiated
        r.energy_threshold = 1200
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            print("listening.............")

            audio = r.listen(source)

            said = ''
        try:
            print("understanding.......")
            # we check if our voice was taken in
            said = r.recognize_google(audio)
            print(said)
        except sr.RequestError:
            speak('HI, THE NETWORK IS DOWN, DO YOU WANT TO SWITCH  TO TEXT INPUT')
            yes_no = input('YES/NO: ')
            if yes_no.lower() == "yes":
                speak("TEXT INPUT ACTIVATED")

                flag = False
                print(flag)
                return change_text()
            # SO , If you insisted on leaving it at voice input, Flag
            # will remain at true and change_to_voice will be returned
            if yes_no.lower() == "no":
                flag = True
                return change_to_voice()

        return said.lower()
    except Exception as e:
        return get_audio()


def get_command() -> str:
    if flag:
        return get_audio().lower()
    elif not flag:
        text = input("Input:  ").lower()
        return text


def get_input():
    """This function handles all form of _text input"""
    global flag
    said = input("Enter your command: ")
    said = said.lower()

    # At any moment you feel like changing to voice input, then this haandles it
    if said == "voice input":
        flag = True
        speak("I am switching to voice input")

        get_audio()
    return said


def change_to_voice():
    """This function runs if we are in voice input and handles all command related to
    voice input"""

    global flag
    while True:
        _text: Union[str, Any] = get_audio()  # We listen to a command here, and its stored in _text variable

        _text = wake_up(_text)  # Text is passed into the wake up call, which check iff the wake up call is heard
        # and when the wakeup call is heard, it await your command. and the command given is
        # returned and pass into _text variable
        if _text is not None:  # This will only run if the value returned tot the _text variable is not none
            while True:
                while flag is True:
                    actions(_text)  # The Action function execute the command given

                    return change_to_voice()  # This will forever returned so far flag is true


def change_text():
    """just like chang_to_voice handles the VOICE input, this handles the _text input"""
    global flag

    flag = False
    text = input("Enter your command: ")
    text = wake_up(text)
    if text is not None:
        while True:
            while flag is False:
                actions(text)

                return change_text()


def wake_up(_text):
    global flag
    # This function receives a parameter from change_to_voice or change_text
    # depending on the value of flag and return the command given back to either of them
    # which is in turn executed by the action function

    for t in _text.lower().split(" "):
        if t in wakeup_call and len(_text.split(' ')) <= 2:
            print(t)
            speak(choice(greetings))  # This gives randomness to the greeting

            speak(choice(response))
            _text = get_command().lower()
            print(_text)

            return _text

        elif t in wakeup_call and len(_text.split(" ")) > 2:
            print(_text)

            return _text
    # If  no command was given or her name is not heard, the a none value will be returned back to either of the the
    # that are mentioned ABOVE
    return returner()


def returner():
    if flag:
        return change_to_voice()
    return change_text()


def actions(_text):
    """

    :type _text: String
    """
    # Here in the action functions, All the checkings are done , and if there is a command that is recognized,
    # The command is executed
    # Some of the command in th database are either a single word or two or more words, so the checking is done
    # for single words or a group of words
    global flag, reminder_thread, alarm_thread

    text_list = _text.split(' ')
    count = 0
    for c in text_list:
        if (c in wikipedia_prompt or _text in wikipedia_prompt) and "yourself" not in _text:
            print("ok")
            return answer_questions(_text)
        
        elif natural_language[0] in _text:
            return chat_with_gpt()

        elif (c in wolphram_prompt or " ".join(text_list[:count]) in wolphram_prompt) and "yourself" not in _text:
            return answer_questions(_text)

        elif c in note_str or _text in note_str:
            return note()
        elif c in calculator_command or _text in calculator_command:
            return show_calculator()
        elif _text in in_calculator_prompt:
            return in_calculator(_text)
        elif c in set_alarm_prompt or _text in set_alarm_prompt:
            print(c)
            print(_text)
            mess = _text.split(" ")
            alarm_thread = threading.Thread(target=ring_alarm, args=[mess])
            alarm_thread.start()

            time.sleep(7)

            if flag:
                return change_to_voice()

            return change_text()

        elif c in play_song_command or _text in play_song_command:

            song_thread = threading.Thread(target=get_mp3)
            song_thread.start()

            time.sleep(5)
            returner()

        elif c in news_prompt or _text in news_prompt:
            return get_news_head()
        elif c in my_self_prompt or _text in my_self_prompt:
            return my_self()
        elif c in virtual_key_prompt or _text in virtual_key_prompt:
            pass
        elif c in translator_prompt or _text in translator_prompt:
            return translators() #Working
        elif c in editor_mode_prompt or _text in translator_prompt:
            pass
        elif c in send_reminder or _text in send_reminder:
            mess = _text.split(" ")
            reminder_thread = threading.Thread(target=sms_reminder, args=[mess])
            reminder_thread.start()
            time.sleep(5)
            return
        elif c in sec_mode_act or _text in sec_mode_act:
            return secretatry_mode()
        elif c in sched:
            return scheduler(_text)
        elif c in text_:
            flag = False
            speak("text input activated")
            return change_text()
        elif c in voice_:
            flag = True
            speak("voice input activated")
            return change_to_voice()

        elif c == "time" or c in "today's" or "date" in c:
            _today = dt.date.today()
            times = dt.datetime.now()
            if c == "time":
                speak("The time is " + times.strftime("%I:%M  %p "))
                return
            elif c == "today's":
                speak("Today is  " + _today.strftime(" %A ,%d of %B  %Y"))
                return
        elif c in shut_exit:
            if "goodnight" in c:
                speak("Good Night sir")
                exit(0)
            elif "exit" in c:
                speak("ok sir")
                exit(-1)
            elif "shutdown" in c:
                speak("Closing ALL program!!!")
                time.sleep(3)
                speak("Shutting Down system!!!")
                os.system('rundll32.exe powrprof.dll, SetSuspendState 0,1,0')
                exit(0)

        elif "game" in c:
            speak(
                "WELCOME TO HANGMAN GAME!!!")
            speak("In this game, i will choose a number between 1 and another number, based on the Level you choose.")
            speak("Guess right the number before ur chances runs out")

            speak("THE levels available are: ")
            for j in LEVEL:
                speak(j)
            time.sleep(1)
            choose_level = levelchoose()
            game_choice(choose_level)
            return
        elif "quran" in c:
            quran_player(_text)
            return

        count += 1
    speak("Sorry , I DIDNT GET THAT")
    if flag is True:
        change_to_voice()
    elif flag is False:
        change_text()


# ABOUT
def my_self():
    """
    This function is run from by ACTION function and it contain everything you might need to know about LAILA
    """

    speak("what do you want to know about me")
    text = get_command()
    date_of_birth = "12th of June 2020 "
    _response = """My name is  LAILA , a multipurpose virtual assistant bot 
                created by Ahmad"""
    if "features" in text or "feature" in text:
        speak("My features include: ")
        for i in features:
            speak(i)
    if "function" in text or "functions" in text:
        speak("My functionality include: ")
        for i in functionalities:
            speak(i)
    if "online" in text:
        speak("my online features are: ")
        for i in online_features:
            speak(i)
    if "self" in text:
        speak(_response)

    speak(_response)


# ONLINE FUNCTIONS (Everything under this contain all functions that requires internet connection before they are
# exccuted)

def get_news_head():
    "This function gives the NEWS HEADLINE taken from GOOGLE NEWS"
    speak("OK SIR")
    try:

        news_url = "https://news.google.com/news/rss"
        _client = urlopen(news_url)
        xml_page = _client.read()
        _client.close()

        soup_page = Soup(xml_page, "lxml")
        news_list = soup_page.findAll("item")
        # Print news title, url and publish date
        for news in news_list:
            speak(news.title.text)
    except urllib.error.URLError:
        speak("Sorry, Network is down now")
        returner()


def answer_questions(_text):
    # This is well she does most his question answering
    text_s = _text.lower().split(" ")
    for c in wikipedia_prompt:
        if c in _text:
            for i in range(len(text_s)):
                if text_s[i] == "who" and text_s[i + 1] == "is":
                    try:
                        res = wikipedia.summary(" ".join(text_s[i + 2:]), sentences=2)
                        return speak(res)
                    except:
                        return speak("Sorry , I dont have anything on " + " ".join(text_s[i + 2:]))
                elif text_s[i] == "tell" and text_s[i + 2] == "about":
                    try:
                        res = wikipedia.summary(" ".join(text_s[text_s.index("about") + 1:]))
                        return speak(res)
                    except:
                        return speak("Sorry , I dont have anything on " + " ".join(text_s[text_s.index("about") + 1:]))
    try:
        for c in wolphram_prompt:
            if c in _text:
                for i in range(len(text_s)):
                    if (text_s[i] == "what" and text_s[i + 1] == "is") and "time" not in _text:
                        res = client.query(" ".join(text_s[text_s.index(" "):]))
                        return speak(next(res.results).text)
                    elif text_s[i] == "define":
                        res = client.query(_text)
                        return speak(next(res.results).text)
                    else:
                        res = client.query(_text)
                        return speak(next(res.results).text)
    except:
        try:
            res = wikipedia.summary(" ".join(text_s[text_s.index(" "):]))
            speak(res)
        except:
            return speak("sory, I dont know")
    return speak("No network")


def translators():
    speak("ok sir")
    speak("what should i translate")
    text = get_command()

    try:
        gs = goslate.Goslate()

        speak("which language do u want to translate to")
        to_what = get_command().title()
        translated = gs.translate(text, lang_dict[to_what])

        speak(translated)

    except urllib.error.HTTPError:
        speak("Service overloaded")
    except urllib.error.URLError:
        speak("No Network")



import os
import datetime as dt

def note(secretary=False):
    # Ensure the secretary directory exists
    if not os.path.exists('secretary'):
        os.makedirs('secretary')
    if not os.path.exists("note"):
        os.makedirs("note")
    
    # Get current date and time
    now = dt.datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")

    # Define the filename and file path
    if secretary:
        directory = "secretary"
    else:
        directory = "note"

    filename = f"{directory}/{date_str}.txt"
    
    # Ask the user what to note
    speak("What should I note?")
    texts = get_command()

    if secretary:
        speak("From who ?")
        from_who = get_command()

    
    # Write the message to the file
    with open(filename, "a") as file:
        if not secretary:
            from_who = "yourself"
        file.write(f"Time: {convert_to_human_readable_time(time_str)},\nMessage: {texts},\nSender: {from_who}\n\n")
    
    speak("Written, sir.")
    return humanize_for_sms(texts, from_who)

def humanize_for_sms(texts, from_who):
    message = f"{texts} from {from_who}"
    return message



def convert_to_human_readable_time(time_str):
    # Parse the time string into a datetime object
    time_obj = parser.parse(time_str)
    
    # Convert the time to a human-readable format
    human_readable_time = time_obj.strftime("%I:%M %p")
    return human_readable_time

# TIME RELATED FUNCTIONS
def set_alarm(text:str):
    "This function set an alarm"
    try:
        global temp_time
        alarm_time = None
        recent_date = dt.datetime.now()  # this give the resent date time

        delta_init = dt.timedelta()  # a time delta was initiated, it allows us to add date/time

        texts = text.split(" ")  # we split the input _text

        for i, c in enumerate(texts):
            if c in time_related:
                # This handles the reminder of the type [minutes ,hour, seconds]
                if c.startswith('m'):

                    delta_init += dt.timedelta(
                        minutes=int(texts[i - 1]))  # Adding the minute specify to the empty time delta initiated
                    time_f = delta_init + recent_date  # The minutes is added to the recent time
                    if "reminder" in text:
                        speak("reminder set to " + time_f.strftime("%I:%M  %p "))
                        print("reminder set to " + time_f.strftime("%I:%M  %p "))
                        return time_f
                    elif "alarm" in text:
                        speak("Alarm set to " + time_f.strftime("%I:%M  %p "))
                        print("Alarm set to " + time_f.strftime("%I:%M  %p "))
                        return time_f
                    else:
                        return time_f

                if c.startswith('h'):  # If the time set is hour
                    delta_init += dt.timedelta(hours=int(texts[i - 1]))
                    time_f = delta_init + recent_date  # does the same as minutes
                    if "reminder" in text:
                        speak("reminder set to " + time_f.strftime("%I:%M  %p "))
                        print("reminder set to " + time_f.strftime("%I:%M  %p "))
                        return time_f
                    elif "alarm" in text:
                        speak("Alarm set to " + time_f.strftime("%I:%M  %p "))
                        print("Alarm set to " + time_f.strftime("%I:%M  %p "))
                        return time_f
                    else:
                        return time_f

            elif c in watch_out:
                # if [today or tomorrow in time]
                if c == 'tomorrow' and 'p.m.' in texts:  # If tomorrow

                    t = texts[texts.index('p.m.') - 1]  # Accessing the time
                    if ":" in t:  # If the time is the likes of 3:45 p.m.
                        t = t.split(":")  # Splitting the hour and minutes
                        temp_time = dt.datetime(recent_date.year, recent_date.month, recent_date.day, int(t[0]),
                                                int(t[1]))
                    elif len(t) == 1:  # If the time is the likes of 3 p.m.

                        temp_time = dt.datetime(recent_date.year, recent_date.month, recent_date.day,
                                                int(t))  # The hour is stored in
                    alarm_time = dt.timedelta(
                        days=1) + temp_time  # Since tomorrrow was specify, we add 1 more day to the time

                elif c == 'tomorrow' and 'a.m.' in texts:  # IF its a.m.
                    t = texts[texts.index('a.m.') - 1]
                    if ":" in t:
                        t = t.split(":")
                        temp_time = dt.datetime(recent_date.year, recent_date.month, recent_date.day, int(t[0]),
                                                int(t[1]))
                    elif len(t) == 1:
                        temp_time = dt.datetime(recent_date.year, recent_date.month, recent_date.day, int(t))
                    alarm_time = dt.timedelta(days=1) + temp_time


                elif c == 'tomorrow':
                    delta_init += dt.timedelta(days=1)

            if c in meridiem:  # for cases of p.m. and q.m.
                if c == 'p.m.' and ('tomorrow' not in texts or 'today' in texts):  # if today was in _text o left out
                    t = texts[i - 1]
                    if ":" in t:
                        t = t.split(":")
                        if len(t[0]) == 1:
                            t[0] = int(t[0]) + 12

                        alarm_time = dt.datetime(recent_date.year, recent_date.month, recent_date.day, int(t[0]),
                                                 int(t[1]))
                        if alarm_time < dt.datetime.now():
                            alarm_time += dt.timedelta(days=1)
                    elif len(t) == 1 or len(t) == 2:
                        if len(t) == 1:
                            t = int(t) + 12

                        alarm_time = dt.datetime(recent_date.year, recent_date.month, recent_date.day, int(t))
                        if alarm_time < dt.datetime.now():
                            alarm_time += dt.timedelta(days=1)
                        print(alarm_time)

                elif c == 'a.m.' and ('tomorrow' not in texts or 'today' in texts):
                    t = texts[i - 1]

                    if ":" in t:
                        t = t.split(":")

                        alarm_time = dt.datetime(recent_date.year, recent_date.month, recent_date.day, int(t[0]),
                                                 int(t[1]))

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
            else:
                return alarm_time

        elif delta_init + recent_date != recent_date:
            time_f = delta_init + recent_date
            if "alarm" in text:
                speak("Alarm set to " + time_f.strftime("%I:%M  %p "))
                return time_f
            elif "reminder" in text:
                speak("reminder set to " + time_f.strftime("%I:%M  %p "))
                return time_f
            return time_f
    except:
        speak("That's an invalid input")
        returner()


def ring_alarm(mess):
    global reminder_thread
    mag = False
    for c in mess:
        if c.lower() in meridiem or c.lower() in time_related:
            mag = True
            break
    if mag:
        mess = " ".join(mess)
        time_set = set_alarm(mess)
    elif not mag:
        speak("what time do you want to set alarm to")
        text = get_command()
        "This is where the alarm is rang oncee its time"
        time_set = set_alarm("alarm " + text)
    while dt.datetime.now() < time_set:
        time.sleep(1)
    playsound.playsound("media/alarm.mp3")
    sys.exit()


def sms_reminder(mess):
    global reminder_thread
    # This handles all form of whatsapp reminders

    client = Client(acc_sid, acc_token)  # The API initiated
    mag = False  # This reminder is accessed by different functions and they all have different foemat
    # So there is need to specify which is which
    for c in mess:
        if c in meridiem or c in time_related:  # If c is accessed through set reminder keyword
            mag = True
            break

    if not mag:
        if isinstance(mess, list):
            mess = " ".join(mess)
    elif mag:  # If it is accessed through set reminder keyword
        speak("what time do you want to set the reminder to")
        text = get_command()
        time_set = set_alarm("reminder " + text)
        speak("what is the reminder message")
        mess = get_command()
    if mag:
        while dt.datetime.now() < time_set:
            time.sleep(1)
    # if it was accessed by other functiong like the secratery mode, it send the reminder immediately
    # this ishe Twilio sandbox testing number
    from_number = twilio_phone_number
    # replace this number with your own WhatsApp Messaging number
    to_number = '+2348065007606'

    client.messages.create(body=mess,
                           from_=from_number,
                           to=to_number)
    speak("message sent")
    if stop_thread:
        sys.exit(0)


# ARITHMETIC FUNCTIONS

def show_calculator():
    # Popping the calculation function
    speak("ok sir")
    subprocess.Popen(['C:\\Windows\\System32\\calc.exe'])


def in_calculator(text):
    # THE in program calculator that can do basic arithmetic and convert from a base to another
    speak("calculator activated")
    speak("what do u want to compute")

    text = get_command()

    while "quit" not in text:
        text_split = text.split(" ")

        if "convert" not in text_split:
            sums = float(text_split[0])
        elif "convert" in text_split:
            sums = float(text_split[1])
        for i, c in enumerate(text_split):
            if c == '+' or c == 'plus':
                sums += float(text_split[i + 1])

            if c == '-' or c == 'minus':
                sums -= float(text_split[i + 1])

            if c == '*' or c == 'multiply':
                if c == "multiply":
                    sums *= float(text_split[i + 2])
                elif c == "*":
                    sums *= float(text_split[i + 1])

            if c == '/' or c == 'divided':
                if c == "divided":
                    sums /= float(text_split[i + 2])
                elif c == "/":
                    sums /= float(text_split[i + 1])

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
        text = get_command()
        if "quit" in text:
            speak("ok sir")


# MEDIA
def get_mp3():
    speak("OK ,Sir")
    # The mp3 generator function
    try:
        while True:
            randomfile = random.choice(os.listdir("C:\Music\\"))  # It randomly choose a file from my music folder
            if randomfile[-3:] == "mp3":
                break

        print(randomfile)
        file = "C:\Music\\" + randomfile

        playsound.playsound(file, True)
        sys.exit()
    except playsound.PlaysoundException:
        speak("An Mp3 was not generated")


def quran_player(text):
    quran_file = os.listdir(r"C:\Music\shuraim\\")  # It randomly choose a file from my music folder

    for c in quran_file:
        quran_num = int(c[:3])
        if str(quran_num) in text:
            print(c)  # I want to know the name of the surah played

            playsound.playsound(r"C:\Music\shuraim\\" + c)


# def word_processor():
#    speak ("ok sir")
#   subprocess.Popen(pass)


# Your Account Sid and Auth Token from twilio.com/console
# THIS FUNCTION HA NOT BEEN INITIATED IN ANY FUNCTION
def text_me(message):
    event_time = set_alarm(message)

    if datetime.datetime.now() < event_time:

        while datetime.datetime.now() < event_time:
            time.sleep(1)

        phone_num = "+14127438749"

        client = Client(acc_sid, acc_token)

        message = client.messages.create(body=message, from_=phone_num,
                                         to='+2348050664320')
    # elif datetime.datetime.now() > event_time:

    # speak(f"The time for {message} has passed")


m = []


def initialise():
    with open(schedule_path, "r") as file:

        for c in file.readlines():
            if "p.m." in c or "a.m." in c:
                thread_obj = threading.Thread(target=text_me, args=[c.strip()])
                thread_obj.start()
                # time.sleep(5)


# SECRETARY MODE in this mode , LAILA can act as a secrtary by checking if u are n office or not base on what u set,
# if u are in office , she does the necessary thing aswell if u are not
in_office = "yes"


# Administrative Functions
def in_office_set(text):
    """This allows u to set either u are in office or not or u are busy"""

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
    # You can check mode u are in
    speak("in office mode is set to " + in_office)
    return


def in_office_or_home(text):
    if in_office.lower() == "yes":
        speak("yes, he is around")
    elif in_office.lower() == "no":
        speak("No")
        speak("Do you want to leave a note")
        decision = get_command()
        if "yes" in decision:
            message_ = note(secretary=True)
            #sms_reminder(message_)
        elif "no" in decision.lower():
            speak("ok sir")

    elif in_office == "busy":
        speak("yes, but Not ready to see anyone, but do you want to leave a note ?")
        decision = get_command()
        if "no" in decision.lower():
            return speak("ok sir")
        elif "yes" in decision:
            message_ = note(secretary=True)
            #sms_reminder(message_)
    return speak("thank you")



def do_i_have_a_message():
    # Ensure the secretary directory exists
    if not os.path.exists('secretary'):
        speak("There are no messages")
        return

    # Check for unread messages
    messages_exist = False
    messages = []

    for filename in os.listdir('secretary'):
        if filename.endswith(".txt") and not filename.endswith("_read.txt"):
            file_path = os.path.join('secretary', filename)
            with open(file_path, "r") as file:
                file_content = file.read()
                if file_content.strip():  # Check if file is not empty
                    messages_exist = True
                    messages.append(f"Messages from {filename[:-4]}:\n{file_content}\n")

            # Rename the file to mark it as read
            new_filename = filename.replace(".txt", "_read.txt")
            new_file_path = os.path.join('secretary', new_filename)
            os.rename(file_path, new_file_path)

    if messages_exist:
        for message in messages:
            print(message)  # Print messages to console
            speak(message)  # Speak messages
    else:
        speak("There are no unread messages.")




def secretatry_mode():
    speak("secretary mode activated")

    while True:
        text = get_command().lower()
        texts = text.split(" ")
        for c in texts:
            if c in in_office_orhome:
                in_office_or_home(text)
                break
            elif c in set_office_home_mode:
                in_office_set(text)
                break
            elif c in check_in_office_mode:
                check_in_office(c)
                break
            elif c in away_messages_command:
                do_i_have_a_message()
                break
            elif c == "exit" or c == "quit":
                speak("ok sir")
                returner()


# SCHEDUlER MODE
todays = datetime.date.today()  # A new file is created each day
schedule_file_name = str(todays).replace(":", "_") + ".txt"
schedule_path = fr"schedules\{schedule_file_name}"


def make_schedules():  # This function makes the schedules
    speak("ok, what should i add")
    lisd = []
    tag = True
    while tag:
        sch_list = get_command()  # Get all form of imput based on the value of flag
        if "all" in sch_list:  # Quiting condition
            speak("Ok sir")
            break
        if "p.m." in sch_list or "a.m." in sch_list:  # if time in the schedule, a thread is created and she send me
            # notification for the schedule

            thread_obj = threading.Thread(target=sms_reminder, args=[sch_list])
            thread_obj.start()
        speak("ok, next")
        lisd.append(sch_list)

    with open(schedule_path, "a") as file:  # all the schedules are written into schedule file
        for c in lisd:
            file.write(c + "\n")

    speak("All added sir")


def scheduler(command):  # This function gets my schedules and read my schedules
    available = os.path.isfile(schedule_path)  # Checking if there is a file for todays schedule
    # get_command =input("want to do: ").lower()
    if "add" in command or "make" in command:  # command check to make schedules
        make_schedules()
    elif "check" in command or "do" in command:  # command to check if i have schedules

        if available == False and "do" in command:
            speak("No sir, do u want to make schedules")

            des = get_command().lower()
            if des.lower() == "yes":
                make_schedules()
            else:
                speak("ok sir")

        elif available == True and "do" in command:
            speak("yes")

            speak("should i read them ?")
            yes_no = get_command().lower()
            if yes_no == "yes":
                speak("Here are your schedules for today")
                with open(schedule_path, "r") as file:
                    speak(f"{file.read()},")

                speak("that's all you have for now")
            elif yes_no == "no":
                speak("ok sir")

        elif "check" in command or "what" in command:
            if not available:
                speak("You dont have a schedule sir, Do you want to make schedule")
                des = get_command.lower()
                if des == "yes":
                    make_schedules()
                else:
                    speak("ok sir")
            elif available:
                speak("ok sir , here are your schedules for today")
                with open(schedule_path, "r") as file:
                    speak(f"{file.read()},")


        elif "what" in command:
            if not available:

                speak("you dont have any schedule for today, do you want to add")
                des = get_command.lower()
                if des == "yes":
                    make_schedules()
                else:
                    speak("ok sir")

            elif available:
                speak("your schedules for today are :")
                with open(schedule_path, "r") as file:
                    speak(file.read())


# GAMES

def levelchoose():
    speak("choose level sir")
    choose_level = get_command()
    choose_level = choose_level.upper()
    while choose_level not in LEVEL:
        speak("That's an invalid input sir")
        print('invalid input')
        speak("choose level again")
        choose_level = get_command()
        choose_level = choose_level.upper()
    return choose_level


def changes(n):
    start = time.time()
    from random import randint

    speak("I CHOOSE A NUMBER BETWEEN 1 AND " + str(n) + "....\n\nGUESS RIGHT TO SAVE YOUR LITTLE FRIEND")

    x = randint(1, n)
    for i in range(7):
        if i == 0:
            speak("what's your guess sir")
        else:

            speak(choice(ge))
        guess = int(get_command())
        while guess > n:
            speak('Invalid input!!! \n\nEnter a number between (1-' + str(50) + ')')
            guess = int(get_command())

        if guess == x:
            speak('Correct!!\n\nCongratulations, you saved your little friend!!')
            score = round(time.time() - start, 3)
            speak(f"It took you {score} seconds to safe your friend.")

            file_name = "hangman.txt"
            path = fr"C:\Users\USER\PycharmProjects\LAILA\Games\{file_name}"
            with open(path, "a") as file:
                file.write(str(score) + "\n")

            with open(path, "r") as file:
                for c in file.readlines():
                    if c != "\n":
                        highest.append(float(c.strip("\n")))
                if min(highest) == score:
                    speak("New Highest score made")
            print(highest)

            break
        if guess != x:
            print(HANGMAN[i])
        if guess > x:
            speak("Your guess is HIGHER")
        if guess < x:
            speak('LOWER than my number')
    if HANGMAN[6] and guess != x:
        speak(f'GAME OVER!! ,You lost your little friend The Number is: {x}')
    speak("Do you want to play again sir")
    choiced = get_command()
    if choiced.lower() == "yes":
        choose_level = levelchoose()
        game_choice(choose_level)
    else:
        speak("Thank You, Good Bye")


def game_choice(choose_level):
    if choose_level == LEVEL[0]:
        changes(50)
    if choose_level == LEVEL[1]:
        changes(100)
    if choose_level == LEVEL[2]:
        changes(150)
    if choose_level == LEVEL[3]:
        changes(200)
    if choose_level == LEVEL[4]:
        changes(500)


if os.path.isfile(schedule_path):  # Checking if there is a file for todays schedule
    initialise()
    time.sleep(2)

returner()
