import datetime
import itertools
import json
import os
import webbrowser

import rich.color
import speech_recognition as sr
import wikipedia as wiki
from wikipedia import summary
from googlesearch import search as gsearch
from gtts import gTTS
from playsound import playsound
from rich import print

r = sr.Recognizer()
filename_cycle = [1, 2]
salts = itertools.cycle(filename_cycle)


def langtranslator(language: str):
    if language == "da":
        lang, sr_lang = "da", "da"
    else:
        lang, sr_lang = "en", "en-GB"
    return(lang, sr_lang)


def greetings(lang: str):
    hour = datetime.datetime.now().hour
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


def search(term: str, lang: str):
    with open(os.path.join(os.path.dirname(__file__), 'config.json'), "r+t", encoding="utf8") as f:
        datajson = json.loads(f.read())
    say(f'{datajson["searchingFor"][lang]} \"{term}\" {datajson["now"][lang]}', lang)
    s = gsearch(term=term, num_results=1, lang=lang)
    say(f'{datajson["opening"][lang]} \"{term}\" {datajson["inBrowserNow"][lang]}', lang)
    webbrowser.open(s[0])


def wikipedia(text: str, lang: str):
    wiki.set_lang(lang)
    say(summary(title=text), lang)


def say(string: str, lang: str):
    said_string = string
    for color in rich.color.ANSI_COLOR_NAMES:
        said_string = said_string.replace(f"[{color}]", "").replace(f"[/{color}]", "")
    salt = next(salts)
    filename = f"say{salt}.mp3"
    gTTS(text=said_string, lang=lang).save(filename)
    print(string)
    playsound(filename)
    os.remove(filename)


def listen(sr_lang: str):
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source, timeout=5)
            text = r.recognize_google(audio, language=sr_lang)
            return text
    except sr.UnknownValueError:
        raise ValueError()
    except sr.RequestError:
        raise ConnectionError()
    except sr.WaitTimeoutError:
        raise TimeoutError()
