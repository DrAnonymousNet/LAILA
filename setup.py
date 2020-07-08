from setuptools import setup

setup(
   name='Laila',
   version='1.0',
   description='A smart virtual assistant bot',
   author='Dr. Anonymous',
   author_email='fix your mail here',
   packages=['Laila'],
   install_requires=['goslate', 'playsound', 'pyttsx3', 'pyaudio', 'SpeechRecognition', 'wikipedia', 'wolframalpha', 'bs4', 'twilio'], #external packages as dependencies
)