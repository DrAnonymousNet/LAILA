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
             'Sanskrit': 'sa', 'Sindhi': 'sd', 'Sangro': 'sg', 'Serbo-Croatian': 'sh', 'Singhalese': 'si',
             'Slovak': 'sk',
             'Slovenian': 'sl', 'Samoan': 'sm', 'Shona': 'sn', 'Somali': 'so', 'Albanian': 'sq', 'Serbian': 'sr',
             'Siswati': 'ss', 'Sesotho': 'st', 'Sudanese': 'su', 'Swedish': 'sv', 'Swahili': 'sw', 'Tamil': 'ta',
             'Tegulu': 'te', 'Tajik': 'tg', 'Thai': 'th', 'Tigrinya': 'ti', 'Turkmen': 'tk', 'Tagalog': 'tl',
             'Setswana': 'tn',
             'Tonga': 'to', 'Turkish': 'tr', 'Tsonga': 'ts', 'Tatar': 'tt', 'Twi': 'tw', 'Uigur': 'ug',
             'Ukrainian': 'uk',
             'Urdu': 'ur', 'Uzbek': 'uz', 'Vietnamese': 'vi', 'Volapuk': 'vo', 'Wolof': 'wo', 'Xhosa': 'xh',
             'Yiddish': 'yi',
             'Yoruba': 'yo', 'Zhuang': 'za', 'Chinese': 'zh', 'Zulu': 'zu'}
time_related = ['days', 'hours', 'minutes', 'seconds', 'minute', 'hour']
watch_out = ['tomorrow', 'today']
week_days = ['sundays', 'mondays', 'tuesday', 'wednesday', 'friday', 'saturday']
meridiem = ['a.m.', 'p.m.']
set_alarm_prompt = ["alarm"]
send_reminder = ["reminder"]
voice_ = ["voice"]
text_ = ["text"]
# Note making keyword
note_str = ["note", "make a note", "write this down", "take this down"]

# calculator keyword
calculator_term = ['-', '+', '*', '/', 'plus', 'minus', 'multiply', 'divided', 'base']
calculator_command = ["pop me a calculator", "get me a calculator", "i need a calculator", "give me a calculator",
                      "give me calculator"]
in_calculator_prompt = ["activate calculator", "activate calculator mode"]

# General keys
wikipedia_prompt = ["about", "who is", "who"]
wolphram_prompt = ["what is", "define", "integrate", "differentiate", "meaning", 'temperature']
play_song_command = ["play me a song", "song"]
news_prompt = ["news", "news headline", "headline"]
virtual_key_prompt = ["virtual", "keyboard"]
translator_prompt = ["translate"]
editor_mode_prompt = ["editor"]
shut_exit = ["shutdown", "exit", "goodnight"]

# About NOORA
my_self_prompt = ["features", "yourself"]
functionalities = ["Calculator functions", "setting reminders", "setting alarm", "playing song", "virtual keyboard",
                   "translator function", "note makeingh", "wiki search", "mathematical computations", "getting news"]
online_features = ["getting news", "language translation", "web searching", "sending reminder"]
features = ["online features", "offline features", "blind features", "mathematical features"]
offline_features = ["getting calculator", "playing song", "basic mathematical computation", "virtual keyboard",
                    "keeping note"]
blind_features = ["activating voice command keyboard", "voice input", "opening apps", "voice typing", "note making"]

# SEC MODE
sec_mode_act = ["sec", "secretary"]
in_office_orhome = ["office", "home", "around"]
set_office_home_mode = ["set"]
check_in_office_mode = ["check"]
date_time = ["time", "date"]
# SCHEDULER MODE
sched = ["schedule", "schedules", "scheduled"]

quran = list(range(1, 115))
print(quran)
acc_sid = "AC221f4496a708695971f54efbf70d222c"

acc_token = "35ed4d199954472a15d7627890778047"

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
ge = ["Guess again !", "Another guess !", "again"]
highest = []
