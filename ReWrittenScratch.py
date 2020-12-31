import json
import os
from datetime import datetime

from defs import greetings, listen, say, search, wikipedia, langtranslator

f = open(os.path.join(os.path.dirname(__file__), 'config.json'), "r+t", encoding="utf8")
datajson = json.loads(f.read())
languages = []
for obj in datajson["languages"]:
    languages.append(datajson["languages"][obj])

if not datajson["language"]:
    say('Choose a language (either English or Danish)', "en")
    language = input()
    while language.lower() not in languages:
        print(f"\u0007")
        say(f"\"{language}\" Doesn't seem like a supported language, please try again.", "en")
        language = input()
else:
    language = datajson["language"]

lang, sr_lang = langtranslator(language.lower())

if datajson["language"] != lang:
    datajson["language"] = lang
    with open(os.path.join(os.path.dirname(__file__), 'config.json'), "wt") as f:
        json.dump(datajson, f, indent=4, ensure_ascii=False)

try:
    say(greetings(lang), lang)
    text, textl = listen(sr_lang)
    print(f"{datajson['said'][lang]}: {text}")
    if textl in (datajson["HelpMe"][lang], datajson["WhatCanYouDo"][lang], datajson["Help"][lang]):
        say(datajson["WhatICanDo"][lang], lang)
    elif textl in (datajson["createFileAndWrite"][lang],
                   datajson["createFile"][lang],
                   datajson["makeFile"][lang],
                   datajson["writeInFile"][lang]):
        say(datajson["FilenameQuestion"][lang], lang)
        filename, filenamel = listen(sr_lang)
        print(f"{datajson['said'][lang]}: {filename}")
        fil = open(f"{filename}.txt", "w")
        say(datajson["FileOpenedWhatNext"][lang], lang)
        filetext, filetextl = listen(sr_lang)
        print(f"{datajson['said'][lang]}: {filetext}")
        fil.write(filetext)
        fil.close()
        say(datajson["Done"][lang], lang)

    elif textl.startswith(datajson["searchFor"][lang]):
        words = textl.split()

        if textl.endswith(datajson["onWikipedia"][lang]):
            wikipedia(words[2:][:-2], lang)

        elif textl.endswith("wikipedia"):
            wikipedia(words[2:][:-1], lang)

        elif textl.endswith(datajson["onBrowser"][lang]):
            search(words[2:][:-2], lang)

        elif textl.endswith("browser"):
            search(words[2:][:-1], lang)

        else:
            search(words[2:], lang)

    else:
        say(f'{datajson["NothingFound"][lang]} {text} {datajson["ShouldISearch"][lang]}', lang)
        yesorno, yesornol = listen(sr_lang)
        while yesornol not in (datajson["yes"][lang], datajson["no"][lang]):
            say(f"{yesorno} {datajson['invalidExpression'][lang]}")
            yesorno, yesornol = listen(sr_lang)
        print(f"{datajson['said'][lang]}: {yesorno}")

        if yesornol in datajson["nothanks"][lang]:
            say(datajson["Won'tSearch"][lang], lang)

        elif yesornol in datajson["yesplease"][lang]:
            search(text, lang)

        else:
            say(datajson["Didn'tUnderstand"][lang], lang)

except ValueError:
    say(datajson["UnknownValueError"][lang], lang)
except ConnectionError:
    say(datajson["RequestError"][lang], lang)
except TimeoutError:
    say(datajson["timeoutError"][lang], lang)
f.close()
