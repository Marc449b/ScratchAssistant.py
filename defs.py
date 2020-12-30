import datetime
import itertools
import os
import webbrowser

import speech_recognition as sr
import wikipedia
from googlesearch import search
from gtts import gTTS
from playsound import playsound
from wikipedia import summary

r = sr.Recognizer()
filename_cycle = [1, 2]
salts = itertools.cycle(filename_cycle)


def langtranslator(input: str):
    if input in ('da', 'dk', 'danish', 'dansk', 'denmark', 'danmark'):
        lang, sr_lang = "da", "da"
    else:
        lang, sr_lang = "en", "en-GB"
    return(lang, sr_lang)


def greetings(lang: str):
    hour = datetime.datetime.now()
    if lang == "da":
        if 6 <= hour <= 10:
            return "Godmorgen. Jeg lytter"
        elif 10 <= hour <= 11:
            return "God formiddag. Jeg lytter"
        elif 12 <= hour <= 15:
            return "God eftermiddag. Jeg lytter"
        elif 16 <= hour <= 20:
            return "God aften. Jeg lytter"
        else:
            return "Godnat. Jeg lytter"
    else:
        if 6 <= hour <= 12:
            return "Good Morning. I am listening"
        elif 12 <= hour <= 18:
            return "Good afternoon. I am listening"
        else:
            return "Good night. I am listening"


def search(text, lang: str):
    say(f'ok, searching for {text} now', lang)
    s = search(text, num_results=1, lang=lang)
    say(f'opening {text} in browser now', lang)
    webbrowser.open(s)


def wikipedia(text, lang: str):
    wikipedia.set_lang(lang)
    say(summary(title=text), lang)


def say(string, lang: str):
    salt = next(salts)
    filename = f"say{salt}.mp3"
    gTTS(text=string, lang=lang).save(filename)
    print(string)
    playsound(filename)
    os.remove(filename)

def listen(sr_lang: str):
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            text = r.recognize_google(audio, language=sr_lang)
            textl = text.lower()
            return(text, textl)
    except sr.UnknownValueError:
        raise ValueError()
    except sr.RequestError:
        raise ConnectionError()
