from dotenv import load_dotenv
import os
load_dotenv()

lang_dict = {'Afar': 'aa', 'Abkhazian': 'ab', 'Afrikaans': 'af', 'Amharic': 'am', 'Arabic': 'ar',
             'Assamese': 'as', 'Aymara': 'ay', 'Azerbaijani': 'az', 'Bashkir': 'ba', 'Byelorussian': 'be',
             'Bulgarian': 'bg', 'Bihari': 'bh', 'Bislama': 'bi', 'Bengali': 'bn', 'Tibetan': 'bo', 'Breton': 'br',
             'Catalan': 'ca', 'Corsican': 'co', 'Czech': 'cs', 'Welch': 'cy', 'Danish': 'da', 'German': 'de',
             'Bhutani': 'dz', 'Greek': 'el', 'English': 'en', 'Esperanto': 'eo', 'Spanish': 'es', 'Estonian': 'et',
             'Basque': 'eu', 'Persian': 'fa', 'Finnish': 'fi', 'Fiji': 'fj', 'Faeroese': 'fo', 'French': 'fr',
             'Frisian': 'fy', 'Irish': 'ga', 'Scots Gaelic': 'gd', 'Galician': 'gl', 'Guarani': 'gn', 'Gujarati': 'gu',
             'Hausa': 'ha', 'Hindi': 'hi', 'Hebrew': 'he', 'Croatian': 'hr', 'Hungarian': 'hu', 'Armenian': 'hy',
             'Interlingua': 'ia', 'Indonesian': 'id', 'Interlingue': 'ie', 'Inupiak': 'ik', 'former Indonesian': 'in',
             'Icelandic': 'is', 'Italian': 'it', 'Inuktitut (Eskimo)': 'iu', 'former Hebrew': 'iw', 'Japanese': 'ja',
             'former Yiddish': 'ji', 'Javanese': 'jw', 'Georgian': 'ka', 'Kazakh': 'kk', 'Greenlandic': 'kl',
             'Cambodian': 'km', 'Kannada': 'kn', 'Korean': 'ko', 'Kashmiri': 'ks', 'Kurdish': 'ku', 'Kirghiz': 'ky',
             'Latin': 'la', 'Lingala': 'ln', 'Laothian': 'lo', 'Lithuanian': 'lt', 'Latvian, Lettish': 'lv',
             'Malagasy': 'mg', 'Maori': 'mi', 'Macedonian': 'mk', 'Malayalam': 'ml', 'Mongolian': 'mn',
             'Moldavian': 'mo', 'Marathi': 'mr', 'Malay': 'ms', 'Maltese': 'mt', 'Burmese': 'my', 'Nauru': 'na',
             'Nepali': 'ne', 'Dutch': 'nl', 'Norwegian': 'no', 'Occitan': 'oc', '(Afan) Oromo': 'om', 'Oriya': 'or',
             'Punjabi': 'pa', 'Polish': 'pl', 'Pashto, Pushto': 'ps', 'Portuguese': 'pt', 'Quechua': 'qu',
             'Rhaeto-Romance': 'rm', 'Kirundi': 'rn', 'Romanian': 'ro', 'Russian': 'ru', 'Kinyarwanda': 'rw',
             'Sanskrit': 'sa', 'Sindhi': 'sd', 'Sangro': 'sg', 'Serbo-Croatian': 'sh', 'Singhalese': 'si', 'Slovak': 'sk',
             'Slovenian': 'sl', 'Samoan': 'sm', 'Shona': 'sn', 'Somali': 'so', 'Albanian': 'sq', 'Serbian': 'sr',
             'Siswati': 'ss', 'Sesotho': 'st', 'Sudanese': 'su', 'Swedish': 'sv', 'Swahili': 'sw', 'Tamil': 'ta',
             'Tegulu': 'te', 'Tajik': 'tg', 'Thai': 'th', 'Tigrinya': 'ti', 'Turkmen': 'tk', 'Tagalog': 'tl', 'Setswana': 'tn',
             'Tonga': 'to', 'Turkish': 'tr', 'Tsonga': 'ts', 'Tatar': 'tt', 'Twi': 'tw', 'Uigur': 'ug', 'Ukrainian': 'uk',
             'Urdu': 'ur', 'Uzbek': 'uz', 'Vietnamese': 'vi', 'Volapuk': 'vo', 'Wolof': 'wo', 'Xhosa': 'xh', 'Yiddish': 'yi',
             'Yoruba': 'yo', 'Zhuang': 'za', 'Chinese': 'zh', 'Zulu': 'zu'}
time_related = ['days', 'hours', 'minutes', 'seconds', 'minute', 'hour']
watch_out = ['tomorrow', 'today']
week_days = ['sundays', 'mondays', 'tuesday', 'wednesday', 'friday', 'saturday']
meridiem = ['a.m.', 'p.m.', 'am', 'pm', "a m", "p m"]
set_alarm_prompt = ["alarm", "alum", "alarms"]
send_reminder =["reminder"]
voice_ = ["voice"]
text_ = ["text"]
away_messages_command =  ["messages", "message", "away message"]
# Note making keyword
note_str = ["note", "make a note", "write this down", "take this down", "notes"]

# calculator keyword
calculator_term = ['-', '+', '*', '/', 'plus', 'minus', 'multiply', 'divided', 'base']
calculator_command = ["pop me a calculator",  "get me a calculator", "i need a calculator", "give me a calculator", "give me calculator"]
in_calculator_prompt = ["activate calculator", "activate calculator mode", "calculator"]


#General keys
wikipedia_prompt = ["about", "who is","who"]
wolphram_prompt = ["what is", "define", "integrate", "differentiate", "meaning", 'temperature']
play_song_command = ["play me a song", "song"]
news_prompt = ["news", "news headline" , "headline"]
virtual_key_prompt = ["virtual", "keyboard"]
translator_prompt = ["translate", "translation", "translates"]
editor_mode_prompt = ["editor"]
shut_exit = ["shutdown" , "exit" , "goodnight"]
natural_language = ["natural language", "chat"]
#About NOORA
my_self_prompt = ["features" , "yourself"]
functionalities = ["Calculator functions", "setting reminders", "setting alarm", "playing song", "virtual keyboard", "translator function", "note makeingh", "wiki search" , "mathematical computations", "getting news"]
online_features = ["getting news", "language translation", "web searching", "sending reminder"]
features = ["online features" , "offline features", "blind features", "mathematical features"]
offline_features = ["getting calculator", "playing song", "basic mathematical computation", "virtual keyboard", "keeping note"]
blind_features = ["activating voice command keyboard", "voice input", "opening apps", "voice typing", "note making"]

#SEC MODE
sec_mode_act = ["sec" , "secretary", "psychiatry", "secondary", "tree"]
in_office_orhome = ["office", "home", "around"]
set_office_home_mode = ["set","sets"]
check_in_office_mode = ["check"]
date_time = ["time" , "date"]
#SCHEDULER MODE
sched = ["schedule" , "schedules", "scheduled", "seduced", "shed" ,"should use", "shed use", "dues", "care dues"]

quran = list(range(1 , 115))


acc_sid =  os.getenv('TWILIO_ACC_SID')
acc_token = os.getenv('TWILIO_ACC_TOKEN')
twilio_phone_number = os.getenv('TWILIO_PHONE_NUMBER')
HANGMAN = ['''
         +---+
         |   |
             |
             |
             |
             |
     =========''', '''
      +---+
      |   |
      O   |
          |
          |
          |
  =========''', '''
         +---+
         |   |
         O   |
         |   |
             |
             |
     =========''', '''

         +---+
         |   |
         O   |
        /|   |
             |
             |
     =========''', '''
      +---+
      |   |
      O   |
     /|\  |
          |
          |
  =========''', '''
       +---+
       |   |
       O   |
      /|\  |   
      /    |
           |
   =========''', '''
      +---+
      |   |
     O    |
     /|\  |
     / \  |
          |
  =========''']

LEVEL = ['BEGINNERS', 'AMATEUR', 'REGULAR', 'PROFESSIONAL', 'TOPPLAYER']
ge = ["Guess again !" , "Another guess !" , "again"]
highest = []
caller_name = "Ahmad"  # os.environ["USERNAME"]

wakeup_call = ["laila", "elena", "leila", "leyla", "layla","alila","la la la","lula","alola",
               "lila", "Layla", "laino", "later"]  # when he hears this (Her name), He wakes up
greetings = [f"Hello {caller_name}", f"Hi {caller_name}", "You called?"]
response = ["How can i help you", "What do u need sir"]
time_units = {
        "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
        "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12,
        "thirteen": 13, "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17,
        "eighteen": 18, "nineteen": 19, "twenty": 20, "thirty": 30, "forty": 40,
        "fifty": 50, "sixty": 60
    }

number_units = time_units

grammar = ["days", "hours", "minutes", "seconds", "minute", "hour",
           "tomorrow", "today", "sundays", "mondays", "tuesday", "wednesday", "friday", "saturday",
           "a.m.", "p.m.", "am", "pm", "a m", "p m",
           "alarm", "alum", "alarms", "reminder", "voice", "text", "messages", "message", "away message",
           "note", "make a note", "write this down", "take this down",
           "-", "+", "*", "/", "plus", "minus", "multiply", "divided", "base",
           "pop me a calculator", "get me a calculator", "i need a calculator", "give me a calculator", "give me calculator",
           "activate calculator", "activate calculator mode", "calculator",
           "about", "who is", "who", "what is", "define", "integrate", "differentiate", "meaning", 'temperature',
           "play me a song", "song", "news", "news headline", "headline", "virtual", "keyboard", "translate", "translation",
           "editor", "shutdown", "exit", "goodnight", "natural language", "chat", "features", "yourself",
           "sec", "secretary", "psychiatry", "secondary", "tree", "office", "home", "around", "set", "sets", "check",
           "time", "date", "schedule", "schedules", "scheduled", "seduced", "shed", "should use", "shed use", "dues", "care dues", "laila", "elena", "leila", "leyla", "layla","alila","la la la","lula","alola",
               "lila", "Layla", "laino"]

