# This is a virtual assistant bot written by Dr.Anonymous
import datetime
from dotenv import load_dotenv
from fuzzywuzzy import process
import spacy
import fitz  # PyMuPDF
from docx import Document
import textwrap
import re
import datetime as dt
import os
import random
import subprocess
import sys
import threading
import time
import requests
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
# import argostranslate.package
# import argostranslate.translate
import wikipedia
import wolframalpha
from bs4 import BeautifulSoup as Soup
from twilio.rest import Client
from openai import OpenAI
import os
import queue
import sounddevice as sd
import vosk
import json
import threading
import tkinter as tk
from tkinter import font
from IPython.display import display
from IPython.display import Markdown


from nooradb import *
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=gemini_api_key)
nlp = spacy.load("en_core_web_sm")

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

flag = True
stop_thread = False

app_id = ""
client = wolframalpha.Client(app_id=app_id)

reminder_thread = 0
alarm_thread = 0
interrupted = False

####TRANSCRIPTION

# def setup_translator():

#     # Download and install Argos Translate package
#     argostranslate.package.update_package_index()
#     available_packages = argostranslate.package.get_available_packages()
#     package_to_install = next(
#         filter(
#             lambda x: x.from_code == from_code and x.to_code == to_code, available_packages
#         )
#     )
#     argostranslate.package.install_from_path(package_to_install.download())

# def translate():
#     from_code = "en"
#     to_code = "es"
#     # Translate
#     translatedText = argostranslate.translate.translate("Hello World", from_code, to_code)
#     print(translatedText)
#     # '¡Hola Mundo!'

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import datetime

custom_vocabulary_path = "./vocabulary.json"
def load_custom_vocabulary(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)
    
custom_vocabulary = load_custom_vocabulary(custom_vocabulary_path)

    
def setup_and_activate_transcription_mode(model_path, email_to, email_from, email_password, samplerate=16000):
    if not os.path.exists(model_path):
        print(f"Please download the model from https://alphacephei.com/vosk/models and unpack as {model_path}")
        exit(1)

    q = queue.Queue()
    recent_texts = ["", "", ""]
    audio_filename = "recorded_audio.wav"
    text_filename = "transcribed_text.txt"
    exit_flag = threading.Event()


    def callback(indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        q.put(bytes(indata))

    def listen_and_recognize():
        with sd.RawInputStream(samplerate=samplerate, blocksize=8000, dtype='int16', channels=1, callback=callback):
            rec = vosk.KaldiRecognizer(model, samplerate)

            with open(audio_filename, 'wb') as audio_file:
                while not exit_flag.is_set():
                    data = q.get()
                    audio_file.write(data)
                    if rec.AcceptWaveform(data):
                        result = json.loads(rec.Result())
                        if "exit" in result['text'].lower():
                            exit_flag.set()
                        add_final_text(result['text'])
                    else:
                        partial_result = json.loads(rec.PartialResult())
                        update_partial_text(partial_result['partial'])

    def add_final_text(text):
        if text.strip():
            recent_texts.append(text)
            if len(recent_texts) > 3:
                recent_texts.pop(0)
            root.after(0, update_text_widget)
        write_text_to_file(text_filename, text)

    def update_partial_text(text):
        if text.strip():
            root.after(0, update_text_widget, text)

    def update_text_widget(partial_text=""):
        text_widget.config(state=tk.NORMAL)
        text_widget.delete('1.0', tk.END)
        for t in recent_texts:
            text_widget.insert(tk.END, t + "\n")
        text_widget.insert(tk.END, partial_text)
        text_widget.tag_configure("center", justify='center')
        text_widget.tag_add("center", "1.0", "end")
        text_widget.config(state=tk.DISABLED)

    def write_text_to_file(filename, text):
        with open(filename, 'a') as file:
            file.write(text + "\n")

    def send_email_with_attachments():
        msg = MIMEMultipart()
        msg['From'] = email_from
        msg['To'] = email_to
        msg['Subject'] = "Transcribed Text and Audio"

        body = "Please find the transcribed text and recorded audio attached."
        msg.attach(MIMEText(body, 'plain'))

        for filename in [audio_filename, text_filename]:
            attachment = open(filename, "rb")
            part = MIMEBase('application', 'octet-stream')
            part.set_payload((attachment).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(filename)}")
            msg.attach(part)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_from, email_password)
        text = msg.as_string()
        server.sendmail(email_from, email_to, text)
        server.quit()

    def on_closing():
        exit_flag.set()
        send_email_thread = threading.Thread(target=send_email_with_attachments)
        send_email_thread.start()
        root.destroy()

    def check_exit():
        if not exit_flag.is_set():
            root.after(100, check_exit)
        else:
            root.quit()
            send_email_thread = threading.Thread(target=send_email_with_attachments)
            send_email_thread.start()
            speak("Ok sir, ")
            speak("The transcribed text and the audio recording has been sent to your email")
            root.destroy()



    root = tk.Tk()
    root.title("LAILA Transcription")
    root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
    large_font = font.Font(size=50)
    global text_widget
    text_widget = tk.Text(root, state=tk.DISABLED, wrap='word', font=large_font)
    text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    label = tk.Label(root, text="POWERED BY LAILA", font=large_font, fg="grey")
    label.pack(side=tk.BOTTOM, pady=10)
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.after(100, check_exit)
    recognition_thread = threading.Thread(target=listen_and_recognize, daemon=True)
    recognition_thread.start()
    root.mainloop()






model_path = "vosk-model-en-us-0.42-gigaspeech"
email_to = "haryourjb@gmail.com"
email_from = "haryourjb2@gmail.com"
email_password = "uxwamdhnnihprlxm"


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


gemini_url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_api_key}'

headers = {
    'Content-Type': 'application/json',
}



def chat_with_gemini():
    speak("Hi, How can i help you today ?")
    conversation = []

    text = get_command()
    while "exit" not in text:
        role = "user"
        
        conversation.append({
            "role": role,
            "parts": [
                {"text": text}
            ]
        })
        data = {
            "contents": conversation
        }

        response = requests.post(gemini_url, headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            response_json = response.json()
            for content in response_json.get('contents', []):
                for part in content.get('parts', []):
                    if 'text' in part:
                        speak(part['text'])
        else:
            speak(f"Request failed with status code {response.status_code}")
            speak(response.text)


def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

# def list_voices():
#     engine = pyttsx3.init()
#     voices = engine.getProperty('voices')
#     for index, voice in enumerate(voices):
#         print(f"Voice {index}: {voice.name}, Gender: {voice.gender}, ID: {voice.id}")

# list_voices()
model = vosk.Model(model_path)

# Create a queue to hold audio data
audio_queue = queue.Queue()
model_path = "vosk-model-en-us-0.42-gigaspeech"

# Callback function to receive audio data
def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    audio_queue.put(bytes(indata))

def get_audio(wake_up=True):
    audio_source = os.getenv("AUDIO_SOURCE")
    if audio_source == "offline":
        return get_audio_offline(wake_up)
    return get_audio_with_internet(wake_up)


def get_audio_offline(wake_up=True):
    global flag
    try:
        print("listening for command............." if not wake_up else "listening for wake up call")

        # Start audio stream
        with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16', channels=1, callback=callback):
            rec = vosk.KaldiRecognizer(model, 16000, f'{grammar}')

            while True:
                data = audio_queue.get()
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    said = result['text']
                    print(said)
                    return said.lower()
                else:
                    partial_result = json.loads(rec.PartialResult())
                    print(partial_result['partial'])

    except Exception as e:
        print(f"Error: {e}")
        return get_audio()


def get_audio_with_internet(wake_up=True):
    global flag
    try:
        # this function allows voice input command
        r = sr.Recognizer()  # the recognizer class was initiated
        r.energy_threshold = 1200
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            print("listening for command............." if not wake_up else "listening for wake up call")

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
        return get_audio(wake_up=False).lower()
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

        get_audio(wake_up=True)
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
        
        elif c in news_prompt or _text in news_prompt:
            return get_news_head()
        elif "news" not in text_list and (c in ["read", "reach", "read"] or "read" in text_list) :
            return handle_read_command(_text)
        
        elif c in ["send", "sends", "sent"] and "email" in text_list:
            return handle_email_command(_text)
        
        elif c == "contact" and "add" in text_list:
            return handle_add_contact_command()
        
        elif natural_language[0] in _text or natural_language[1] in _text:
            return chat_with_gemini()
         
        elif "transcription" in _text:
            speak("Transcription mode activated")
            setup_and_activate_transcription_mode(model_path, email_to, email_from, email_password)
            returner()


        elif (c in wolphram_prompt or " ".join(text_list[:count]) in wolphram_prompt) and "yourself" not in _text:
            return answer_questions(_text)

        elif c in note_str or _text in note_str:
            return note()
        # elif c in calculator_command or _text in calculator_command:
        #     return show_calculator()
        elif _text in in_calculator_prompt or c in in_calculator_prompt:
            return in_calculator(_text)
        elif c in set_alarm_prompt or _text in set_alarm_prompt:
            print(c)
            print(_text)
            if os.getenv("AUDIO_SOURCE") == "online":
                time_to_set_alarm_to =  get_alarm_time("alarm " + _text)
            else:
                time_to_set_alarm_to = convert_text_to_time(text_)

            alarm_thread = threading.Thread(target=ring_alarm, args=[time_to_set_alarm_to])
            alarm_thread.start()

            time.sleep(3)

            if flag:
                return change_to_voice()

            return change_text()

        elif c in play_song_command or _text in play_song_command:

            song_thread = threading.Thread(target=get_mp3)
            song_thread.start()

            time.sleep(5)
            returner()


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
            sms_reminder(mess)
            time.sleep(3)
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


def convert_text_to_time(text):

    # Define AM and PM indicators
    am_pm_indicators = {"a": "AM", "am": "AM", "p": "PM", "pm": "PM", "p m":"PM","a m":"AM"}

    # Extract the hour and minute
    if isinstance(text, list):
        text = " ".join(text)
    text = text.lower()
    time_match = re.search(r'(\b(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty)\b)', text)
    if not time_match:
        raise ValueError("Invalid time format")

    hour = time_units[time_match.group(1)]
    text = text.replace(time_match.group(1), '').strip()

    minute_match = re.search(r'(\b(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty)\b)', text)
    if minute_match:
        minute = time_units[minute_match.group(1)]
        text = text.replace(minute_match.group(1), '').strip()
    else:
        minute = 0

    # Determine AM/PM
    am_pm = "AM"  # Default to AM if not specified
    for indicator in am_pm_indicators:
        if indicator in text:
            am_pm = am_pm_indicators[indicator]
            break

    # Create the time string and convert to datetime object
    time_str = f"{hour:02}:{minute:02} {am_pm}"
    time_obj = dt.datetime.strptime(time_str, "%I:%M %p")
    speak("Alarm set to " + time_obj.strftime("%H:%M %p %A, %d of %B %Y"))


    return time_obj

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
        for news in news_list[:10]:
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
    retry_counter = 0
    speak("ok sir")
    speak("which language should i translate to?")
    to_what = get_command().title()
    speak(f"Ok sir, I will translate all subsequent words into {to_what}, you can keep them coming now")
    
    text = get_command()

    while "exit" not in text and retry_counter < 5:
        try:
            gs = goslate.Goslate()


            translated = gs.translate(text, lang_dict[to_what])

            speak(translated)

        except urllib.error.HTTPError:
            speak("Service overloaded")
        except urllib.error.URLError:
            if retry_counter == 0:
                speak("No Network right now. Should I hold on till there is network or exit translation mode")
                decision = get_command()
                if "exit" in decision:
                    speak("Ok, I will be exiting the translation mode now")
                    break
                else:
                    speak("I will give it a try for about 5 times and exit this mode if unsuccessful")
                    retry_counter += 1
                    continue
            else:
                retry_counter += 1
                continue
        else:
            retry_counter = 0
            text = get_command()
    if "exit" in text:
        speak("Exiting translation mode")
    if retry_counter == 5:
        speak("I have tried for about 5 times but the network is not yet back. I am exiting the translation mode now")
    return returner()


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
    if secretary:
        secretary_message(filename, time_str, texts, from_who)
        return humanize_for_sms(texts, from_who)
    else:
        make_a_note(filename, texts, time_str)

    speak("Written, sir.")


def make_a_note(filename, texts, time_str):
    # Write the message to the file
    with open(filename, "a") as file:
        file.write(f"Time: {convert_to_human_readable_time(time_str)},\nNote: {texts}\n\n")


def secretary_message(filename, time_str, texts, from_who):
    with open(filename, "a") as file:
        file.write(f"Time: {convert_to_human_readable_time(time_str)},\nMessage: {texts},\nSender: {from_who}\n\n")
    
    


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

def get_alarm_time(mess: str, silent=False):
    "This function sets an alarm"
    text = parse_alarm_command(mess)
    try:
        recent_date = dt.datetime.now()
        delta_init = dt.timedelta()
        texts = text.split(" ")

        for i, c in enumerate(texts):
            if c in time_related:
                unit = c[0]  # Get the first character to determine the unit
                value = int(texts[i - 1])
                if unit == 'm':
                    delta_init += dt.timedelta(minutes=value)
                elif unit == 'h':
                    delta_init += dt.timedelta(hours=value)
                time_f = delta_init + recent_date
                if "reminder" in text:
                    if not silent:
                        speak("Reminder set to " + time_f.strftime("%I:%M %p"))
                    return time_f
                elif "alarm" in text:
                    speak("Alarm set to " + time_f.strftime("%I:%M %p"))
                    return time_f

            elif c in watch_out:
                if c == 'tomorrow':
                    delta_init += dt.timedelta(days=1)
                
                meridian = 'p.m.' if 'p.m.' in texts or 'pm' in texts else 'a.m.' if 'a.m.' in texts or 'am' in texts else None
                if meridian:
                    t_index = texts.index(meridian) - 1
                    t = texts[t_index]
                    if ":" in t:
                        t = t.split(":")
                        temp_time = dt.datetime(recent_date.year, recent_date.month, recent_date.day, int(t[0]), int(t[1]))
                    else:
                        temp_time = dt.datetime(recent_date.year, recent_date.month, recent_date.day, int(t))

                    if 'p.m.' in texts or 'pm' in texts:
                        if int(t[0]) < 12:
                            temp_time = temp_time.replace(hour=temp_time.hour + 12)

                    alarm_time = temp_time + delta_init
                    if alarm_time < dt.datetime.now():
                        alarm_time += dt.timedelta(days=1)

                    if "alarm" in text:
                        speak("Alarm set to " + alarm_time.strftime("%H:%M %p %A, %d of %B %Y"))
                        return alarm_time
                    elif "reminder" in text:
                        if not silent:
                            speak("Reminder set to " + alarm_time.strftime("%H:%M %p %A, %d of %B %Y"))
                        return alarm_time

            elif c in meridiem:
                t = texts[i - 1]
                if ":" in t:
                    t = t.split(":")
                    hour = int(t[0])
                    minute = int(t[1])
                else:
                    hour = int(t)
                    minute = 0

                if c in ['p.m.', 'pm'] and hour < 12:
                    hour += 12

                alarm_time = dt.datetime(recent_date.year, recent_date.month, recent_date.day, hour, minute)
                if alarm_time < dt.datetime.now():
                    alarm_time += dt.timedelta(days=1)

                if "alarm" in text:
                    speak("Alarm set to " + alarm_time.strftime("%H:%M %p %A, %d of %B %Y"))
                    return alarm_time
                elif "reminder" in text:
                    if not silent:
                        speak("Reminder set to " + alarm_time.strftime("%H:%M %p %A, %d of %B %Y"))
                    return alarm_time

        if delta_init.total_seconds() > 0:
            time_f = delta_init + recent_date
            if "alarm" in text:
                speak("Alarm set to " + time_f.strftime("%I:%M %p"))
                return time_f
            elif "reminder" in text:
                if not silent:
                    speak("Reminder set to " + time_f.strftime("%I:%M %p"))
                return time_f

    except Exception as e:
        speak("That's an invalid input")
        returner()
# def get_alarm_time(mess:str):
#     "This function set an alarm"
#     text = parse_alarm_command(mess)
#     try:
#         temp_time = None
#         alarm_time = None
#         recent_date = dt.datetime.now()  # this give the resent date time

#         delta_init = dt.timedelta()  # a time delta was initiated, it allows us to add date/time

#         texts = text.split(" ")  # we split the input _text

#         for i, c in enumerate(texts):
#             if c in time_related:
#                 # This handles the reminder of the type [minutes ,hour, seconds]
#                 if c.startswith('m'):

#                     delta_init += dt.timedelta(
#                         minutes=int(texts[i - 1]))  # Adding the minute specify to the empty time delta initiated
#                     time_f = delta_init + recent_date  # The minutes is added to the recent time
#                     if "reminder" in text:
#                         speak("reminder set to " + time_f.strftime("%I:%M  %p "))
#                         print("reminder set to " + time_f.strftime("%I:%M  %p "))
#                         return time_f
#                     elif "alarm" in text:
#                         speak("Alarm set to " + time_f.strftime("%I:%M  %p "))
#                         print("Alarm set to " + time_f.strftime("%I:%M  %p "))
#                         return time_f
#                     else:
#                         return time_f

#                 if c.startswith('h'):  # If the time set is hour
#                     delta_init += dt.timedelta(hours=int(texts[i - 1]))
#                     time_f = delta_init + recent_date  # does the same as minutes
#                     if "reminder" in text:
#                         speak("reminder set to " + time_f.strftime("%I:%M  %p "))
#                         print("reminder set to " + time_f.strftime("%I:%M  %p "))
#                         return time_f
#                     elif "alarm" in text:
#                         speak("Alarm set to " + time_f.strftime("%I:%M  %p "))
#                         print("Alarm set to " + time_f.strftime("%I:%M  %p "))
#                         return time_f
#                     else:
#                         return time_f

#             elif c in watch_out:
#                 # if [today or tomorrow in time]
#                 __import__("ipdb").set_trace()
#                 if c == 'tomorrow' and 'p.m.' in texts or c == 'tomorrow' and 'pm' in texts:  # If tomorrow
#                     if 'p.m.' in texts:
#                         t = texts[texts.index('p.m.') - 1]  # Accessing the time
#                     elif 'pm' in text:
#                         t = texts[texts.index('pm') - 1]
#                     if ":" in t:  # If the time is the likes of 3:45 p.m.
#                         t = t.split(":")  # Splitting the hour and minutes
#                         temp_time = dt.datetime(recent_date.year, recent_date.month, recent_date.day, int(t[0]),
#                                                 int(t[1]))
#                     elif len(t) in [1,2]:  # If the time is the likes of 3 p.m.

#                         temp_time = dt.datetime(recent_date.year, recent_date.month, recent_date.day,
#                                                 int(t))  # The hour is stored in
#                     alarm_time = dt.timedelta(
#                         days=1) + temp_time  # Since tomorrrow was specify, we add 1 more day to the time

#                 elif c == 'tomorrow' and 'a.m.' in texts or c == "tomorrow" and 'am' in texts:  # IF its a.m.
#                     t = texts[texts.index('a.m.') - 1]
#                     if ":" in t:
#                         t = t.split(":")
#                         temp_time = dt.datetime(recent_date.year, recent_date.month, recent_date.day, int(t[0]),
#                                                 int(t[1]))
#                     elif len(t) == 1:
#                         temp_time = dt.datetime(recent_date.year, recent_date.month, recent_date.day, int(t))
#                     alarm_time = dt.timedelta(days=1) + temp_time


#                 elif c == 'tomorrow':
#                     delta_init += dt.timedelta(days=1)

#             if c in meridiem:  # for cases of p.m. and q.m.
#                 if c in ['p.m.', 'pm'] and ('tomorrow' not in texts or 'today' in texts):  # if today was in _text o left out
#                     t = texts[i - 1]
#                     if ":" in t:
#                         t = t.split(":")
#                         if len(t[0]) == 1:
#                             t[0] = int(t[0]) + 12

#                         alarm_time = dt.datetime(recent_date.year, recent_date.month, recent_date.day, int(t[0]),
#                                                  int(t[1]))
#                         if alarm_time < dt.datetime.now():
#                             alarm_time += dt.timedelta(days=1)
#                     elif len(t) == 1 or len(t) == 2:
#                         if len(t) == 1:
#                             t = int(t) + 12

#                         alarm_time = dt.datetime(recent_date.year, recent_date.month, recent_date.day, int(t))
#                         if alarm_time < dt.datetime.now():
#                             alarm_time += dt.timedelta(days=1)
#                         print(alarm_time)

#                 elif c in ['a.m.', 'am'] and ('tomorrow' not in texts or 'today' in texts):
#                     t = texts[i - 1]

#                     if ":" in t:
#                         t = t.split(":")

#                         alarm_time = dt.datetime(recent_date.year, recent_date.month, recent_date.day, int(t[0]),
#                                                  int(t[1]))

#                     elif len(t) == 1:
#                         alarm_time = dt.datetime(recent_date.year, recent_date.month, recent_date.day, int(t))
#                         print(alarm_time)
#         if alarm_time:
#             if "alarm" in text:
#                 speak("Alarm set to " + alarm_time.strftime("%H:%M  %p %A ,%d of %B  %Y"))
#                 print("Alarm set to " + alarm_time.strftime("%H:%M  %p %A ,%d of %B  %Y"))
#                 return alarm_time
#             elif "reminder" in text:
#                 speak("reminder set to " + alarm_time.strftime("%H:%M  %p %A ,%d of %B  %Y"))
#                 print("reminder set to " + alarm_time.strftime("%H:%M  %p %A ,%d of %B  %Y"))
#                 return alarm_time
#             else:
#                 return alarm_time

#         elif delta_init + recent_date != recent_date:
#             time_f = delta_init + recent_date
#             if "alarm" in text:
#                 speak("Alarm set to " + time_f.strftime("%I:%M  %p "))
#                 return time_f
#             elif "reminder" in text:
#                 speak("reminder set to " + time_f.strftime("%I:%M  %p "))
#                 return time_f
#             return time_f
#     except Exception as e:
#         speak("That's an invalid input")
#         returner()

def parse_alarm_command(mess):
    global reminder_thread
    mag = False
    mess = mess.split(" ")
    for c in mess:
        if c.lower() in meridiem or c.lower() in time_related:
            mag = True
            break
    if mag:
        mess = " ".join(mess)
        return mess
    else:
        speak("what time do you want to set alarm to")
        text = get_command()
        return text
    

        
def ring_alarm(time_set):
    while dt.datetime.now() < time_set:
        time.sleep(1)
    playsound.playsound("alarm/alarm.mp3")
    sys.exit()


def sms_reminder(mess, secretary=False):
    global reminder_thread
    time_set = None
    # This handles all form of whatsapp reminders
    print("message:" ,mess)
    if isinstance(mess, str):
        mess = mess.split(" ")
    mag = False  # This reminder is accessed by different functions and they all have different foemat
    # So there is need to specify which is which
    for c in mess:
        if c in meridiem or c in time_related:  # If c is accessed through set reminder keyword
            mag = True
            time_set = get_alarm_time("reminder " + " ".join(mess), silent = True)
            break

    if mag:
        if isinstance(mess, list):
            mess = " ".join(mess)
    elif not mag:  # If it is accessed through set reminder keyword
        if not secretary:
            speak("what time do you want to set the reminder to")
            text = get_command()
            time_set = get_alarm_time("reminder " + text)
            speak("what is the reminder message")
            mess = get_command()
        
    if mag:
        while dt.datetime.now() < time_set:
            time.sleep(1)
    # if it was accessed by other functiong like the secratery mode, it send the reminder immediately
    # this ishe Twilio sandbox testing number
    if not time_set:
        time_set = datetime.datetime.now()

    reminder_thread = threading.Thread(target=send_message, args=[mess, twilio_phone_number, time_set])
    reminder_thread.start()
    if stop_thread:
        sys.exit(0)


def send_message(mess, from_number, time_to_send):
    wait_until_time_set(time_to_send)
    to_number = '+2348065007606'
    client = Client(acc_sid, acc_token)
    if isinstance(mess, list):
        mess = " ".join(mess)
    try:
        client.messages.create(body=mess, from_=from_number, to=to_number)
    except:
        speak("Network is currently unavailable, message will be sent to him later")
    else:
        speak("Message sent")

def wait_until_time_set(time_set):
    while dt.datetime.now() < time_set:
        time.sleep(1)

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

    while "quit" not in text or "exit" not in text:
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
            randomfile = random.choice(os.listdir("media/"))  # It randomly choose a file from my music folder
            if randomfile[-3:] == "mp3":
                break

        print(randomfile)
        file = "media/" + randomfile

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
    print(message)
    event_time = get_alarm_time(message)

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
            print(c)
            if "p.m." in c or "a.m." in c:

                thread_obj = threading.Thread(target=sms_reminder, args=["reminder " +c.strip()])
                thread_obj.start()
                # time.sleep(5)


# SECRETARY MODE in this mode , LAILA can act as a secrtary by checking if u are n office or not base on what u set,
# if u are in office , she does the necessary thing aswell if u are not
in_office = "available"


# Administrative Functions
def in_office_set(text):
    """This allows u to set either u are in office or not or u are busy"""

    global in_office
    if "no" in text:
        in_office = "unavailable"
    elif "yes" in text:
        in_office = "available"
    elif "busy" in text:
        in_office = "busy"

    speak(f"Availability set to {in_office}")
    return in_office.lower()


def check_in_office(text):
    # You can check mode u are in
    speak("your avaialability is set to " + in_office)
    return


def in_office_or_home(text):
    if in_office.lower() == "available":
        speak("yes, he is around")
    elif in_office.lower() == "unavailable":
        speak("No")
        speak("Do you want to leave a note")
        decision = get_command()
        if "yes" in decision:
            message_ = note(secretary=True)
            sms_reminder(message_, secretary=True)
        elif "no" in decision.lower():
            speak("ok sir")

    elif in_office == "busy":
        speak("yes, but Not ready to see anyone, but do you want to leave a note ?")
        decision = get_command()
        if "no" in decision.lower():
            return speak("ok sir")
        elif "yes" in decision:
            message_ = note(secretary=True)
            sms_reminder(message_, secretary=True)
    #return speak("thank you")



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
        speak("Yes sir, you do!")

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
        print(texts)
        for c in texts:
            print(c)
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
            elif "exit" in c or c == "quit":
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
            if "yes" in des.lower():
                make_schedules()
            else:
                speak("ok sir")

        elif available == True and "do" in command:
            speak("yes")

            speak("should i read them ?")
            yes_no = get_command().lower()
            if "yes" in yes_no:
                speak("Here are your schedules for today")
                with open(schedule_path, "r") as file:
                    speak(f"{file.read()},")

                speak("that's all you have for now")
            elif "no" in yes_no:
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
                if "yes" in des:
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




## Book reading feature


def read_pdf(file_path, page_number):
    document = fitz.open(file_path)
    page = document.load_page(page_number - 1)  # page_number is 1-based
    text = page.get_text("text")
    return text


def read_docx(file_path, page_number):
    document = Document(file_path)
    paragraphs = document.paragraphs
    # Assuming roughly 30 paragraphs per page, adjust as needed
    start_index = (page_number - 1) * 30
    end_index = start_index + 30
    text = "\n".join([para.text for para in paragraphs[start_index:end_index]])
    return text

def parse_read_command(command):
    command = command.lower()
    if "read" in command:
        if "from page" in command:
            match = re.match(r"read (.+) from page (\d+)", command, re.IGNORECASE)
            if match:
                book_name = match.group(1).strip()
                page_number = int(match.group(2).strip())
                return book_name, page_number
        elif "read the" in command:
            match = re.match(r"read the (.+)", command, re.IGNORECASE)
            if match:
                book_name = match.group(1).strip()
                return book_name, None
        else:
            return None, None
    return None, None

def extract_number(input_string):
    # Use a regular expression to find all numbers in the string
    numbers = re.findall(r'\d+', input_string)
    if numbers:
        # Join all numbers into a single string and convert to integer
        return int(''.join(numbers))
    else:
        raise ValueError("No numbers found in input")

def get_number_literal(text):
    for word in text.split(" "):
        if number_units.get(word):
            return int(number_units.get(word))
    return

def handle_read_command(command, book_name = None, page_number=None):
    if not book_name and not page_number:
        speak("Please provide the book name.")
        book_name = get_command().strip()
        speak("Which page do you want me to read from?")
        while True:
            try:
                number = get_command().strip()
                page_number = extract_number(number)
            except ValueError:
                # If no number is found, try to find a number literal
                page_number = get_number_literal(number)
                if page_number:
                    break
                speak("Sorry, I didn't get the page number, can you repeat that?")
                continue
            break
    elif book_name and not page_number:
        speak("Which page do you want me to read from?")
        while True:
            try:
                number = get_command().strip()
                page_number = extract_number(number)
            except ValueError:
                # If no number is found, try to find a number literal
                page_number = get_number_literal(number)
                if page_number:
                    break
                speak("Sorry, I didn't get the page number, can you repeat that?")
                continue
            break
    elif not book_name:
        speak("Please provide the book name.")
        book_name = get_command().strip()

    file_path = find_closest_matching_attachments(book_name)
    if not file_path:
        speak("Sorry, I couldn't find the book.")
        return
    file_path = file_path[0]

    if file_path.endswith(".pdf"):
        text = read_pdf(file_path, page_number)
    elif file_path.endswith(".docx"):
        text = read_docx(file_path, page_number)
    else:
        speak("Unsupported file format.")
        return
    
    speak("Okay, I'll read " + book_name + " from page " + str(page_number))


    speak(text)

    speak("Should i continue ?")
    cont = get_command()
    if "y" in cont:
        handle_read_command(command="", book_name=book_name, page_number=page_number+1)
    elif "re" in cont:
        handle_read_command(command="", book_name=book_name, page_number=page_number)
    else:
        speak("Ok, sir")


# Contact and Email management


def send_email_with_attachments(email_to, subject,  body, attachments):
    msg = MIMEMultipart()
    msg['From'] = email_from
    msg['To'] = email_to
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    for filename in attachments:
        attachment = open(filename, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(filename)}")
        msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_from, email_password)
    text = msg.as_string()
    server.sendmail(email_from, email_to, text)
    server.quit()


def handle_email_command(command: str):
    # Debugging removed for production code
    command = command.replace(",", " ")
    speak("ok sir!")

    if "send an email to" in command:
        handle_send_to_email_command(command)
    elif "send an email" in command:
        handle_simple_send_email_command()
    else:
        speak("I didn't understand the email command.")

def get_message_from_command(command, keyword):
    parts = command.split(keyword)[1]
    if "tell him" in command:
        recipient = parts.split("tell him")[0].strip()
        message = parts.split("tell him ")[1].strip().replace("to", "")
    else:
        recipient = parts.strip()
        message = None
    return recipient, message

def handle_send_to_email_command(command):
    recipient, message = get_message_from_command(command, "send an email to ")

    recipient_email = get_or_ask_for_email(recipient)

    if not message:
        speak("What should I tell him?")
        message = get_command()
    
    message = transform_to_direct_speech(message)

    subject, attachment = ask_email_details()
    send_email_async(recipient_email, subject, message, attachment)

def handle_simple_send_email_command():
    speak("Who would you like to send the email to?")
    recipient_name = get_command()
    recipient_email = get_or_ask_for_email(recipient_name)

    subject, message = ask_for_subject_and_message()
    attachment = ask_for_attachment()

    message = transform_to_direct_speech(message)


    send_email_async(recipient_email, subject, message, attachment)

def get_or_ask_for_email(name):
    email = get_contact_email(name)
    if not email:
        speak(f"I don't have an email address for {name}. Please provide the email address.")
        email = input("Email: ")
        add_contact(name, email)
    return email

def ask_email_details():
    speak("What is the subject of the email?")
    subject = get_command().title()
    attachment = ask_for_attachment()
    return subject, attachment

def ask_for_subject_and_message():
    speak("What is the subject of the email?")
    subject = get_command().title()
    speak("What is the message?")
    message = get_command()
    return subject, message


def ask_for_attachment():
    speak("Do you want to add any attachments?")
    yes_no = get_command().lower()
    attachments = []

    if 'y' in yes_no:
        speak("Please provide the name of the attachment.")
        search_name = get_command().lower()
        attachments = find_closest_matching_attachments(search_name)

        if attachments:
            speak(f"Attaching file: {attachments[0]}")
        else:
            speak("No matching files found.")

    return attachments

def find_closest_matching_attachments(search_name):
    directory = "./attachments"  # Specify the path to your attachments directory
    files_list = [os.path.join(directory, f) for f in os.listdir(directory)]
    file_names_without_extension = [os.path.splitext(os.path.basename(f))[0] for f in files_list]

    # Find the closest match to the search name
    closest_match = process.extractOne(search_name, file_names_without_extension)

    if closest_match:
        # Get the index of the closest match to find the corresponding full path file
        index = file_names_without_extension.index(closest_match[0])
        return [files_list[index]]
    return []

def transform_to_direct_speech(text):
    doc = nlp(text)
    transformed_sentences = []
    skip_next = False

    for sent in doc.sents:
        # Process each sentence to find "tell him" and modify accordingly
        parts = [token for token in sent if not skip_next]
        for token in parts:
            if token.lower_ in ["tell", "ask", "instruct", "order"] and token.nbor().lower_ == "him":
                # Create a new sentence from this point
                start_index = token.idx + len("tell him ")
                new_sentence = sent.text[start_index:].strip()
                # Change pronouns and adjust verbs in the new sentence
                new_sentence = nlp(new_sentence)
                for word in new_sentence:
                    if word.lower() == "i":
                        new_sentence = new_sentence.text.replace(" I ", " you ")
                    if word.lower() == "my":
                        new_sentence = new_sentence.text.replace(" my ", " your ")
                    if word.lower() == "all of them":
                        new_sentence = new_sentence.text.replace(" all of them", " all of you")
                transformed_sentences.append(new_sentence)
                skip_next = True
            else:
                skip_next = False
    if transformed_sentences == []:
        return text
    return ' '.join(transformed_sentences)

def send_email_async(email, subject, message, attachments):
    send_email_thread = threading.Thread(target=send_email_with_attachments, args=[email, subject, message, attachments])
    send_email_thread.start()
    speak("ok sir!, I will send the email right away!")



# File to store email contacts
CONTACTS_FILE = 'email_contacts.json'

# Initialize contacts file
def init_contacts():
    if not os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, 'w') as file:
            json.dump({}, file)

# Add a contact
def add_contact(name, email):
    with open(CONTACTS_FILE, 'r') as file:
        contacts = json.load(file)
    contacts[name.lower()] = email
    with open(CONTACTS_FILE, 'w') as file:
        json.dump(contacts, file)

# Get contact email by name
def get_contact_email(name):
    with open(CONTACTS_FILE, 'r') as file:
        contacts = json.load(file)
    return contacts.get(name.lower())

def handle_add_contact_command():
    speak("What is the name of the contact? Type it so that i can get it properly")
    name = input("Name: ")
    speak("What is the email address of the contact?")
    email = input("Email: ")
    add_contact(name, email)
    speak(f"Contact {name} with email {email} has been added.")

# Initialize contacts on first run

if os.path.isfile(schedule_path):  # Checking if there is a file for todays schedule
    initialise()
    time.sleep(2)
init_contacts()
returner()
