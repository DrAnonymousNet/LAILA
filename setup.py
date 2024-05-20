from setuptools import setup, find_packages

setup(
   name='Laila',
   version='1.0',
   description='A smart virtual assistant bot',
   author='Dr. Anonymous',
   author_email='Haryourdejijb@gmail.com',
   packages=find_packages(),

   install_requires=['goslate', 'playsound', 'pyttsx3', 'pyaudio', 'SpeechRecognition', 'wikipedia', 'wolframalpha', 'bs4', 'twilio'], #external packages as dependencies
)
