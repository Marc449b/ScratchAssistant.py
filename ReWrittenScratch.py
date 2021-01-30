import json
import os

from rich import print
from defs import greetings, listen, say, search, wikipedia, langtranslator

with open(os.path.join(os.path.dirname(__file__), 'config.json'), "r+t", encoding="utf8") as f:
    datajson = json.loads(f.read())

languages = [obj for obj in datajson["languages"]]

language = datajson["language"]
if not language:
    say('Choose a language (either English or Danish)', "en")
    language = input()
    while language.lower() not in languages:
        print(f"\u0007")
        say(f"\"{language}\" Doesn't seem like a supported language, please try again.", "en")
        language = input()
    language = language.lower()

lang, sr_lang = langtranslator(datajson["languages"][language])

if datajson["language"] != lang:
    datajson["language"] = lang
    with open(os.path.join(os.path.dirname(__file__), 'config.json'), "wt") as f:
        json.dump(datajson, f, indent=4, ensure_ascii=False)

try:
    say(greetings(lang), lang)
    text = listen(sr_lang)
    textl = text.lower()
    print(f"{datajson['said'][lang]}: \"{text}\"")
    if textl in (datajson["HelpMe"][lang], datajson["WhatCanYouDo"][lang], datajson["Help"][lang]):
        say(datajson["WhatICanDo"][lang], lang)
    elif textl in (datajson["createFileAndWrite"][lang],
                   datajson["createFile"][lang],
                   datajson["makeFile"][lang],
                   datajson["writeInFile"][lang]):
        say(datajson["FilenameQuestion"][lang], lang)
        filename = listen(sr_lang)
        print(f"{datajson['said'][lang]}: \"{filename}\"")
        fil = open(f"{filename}.txt", "w")
        say(datajson["FileOpenedWhatNext"][lang], lang)
        filetext = listen(sr_lang)
        print(f"{datajson['said'][lang]}: \"{filetext}\"")
        fil.write(filetext)
        fil.close()
        say(datajson["Done"][lang], lang)

    elif textl.startswith(datajson["searchFor"][lang]):
        words = textl.split()[2:]

        if textl.endswith(datajson["onWikipedia"][lang]) or textl.endswith(datajson["onBrowser"][lang]):
            words, term, i = words[:-2], "", 1
            for word in words:
                term += word + f"{'' if i == len(words) else ' '}"
                i += 1
            if textl.endswith("wikipedia"):
                wikipedia(term, lang)
            else:
                search(term, lang)

        elif textl.endswith("wikipedia") or textl.endswith("browser"):
            words, term, i = words[:-1], "", 1
            for word in words:
                term += word + f"{'' if i == len(words) else ' '}"
                i += 1
            if textl.endswith("wikipedia"):
                wikipedia(term, lang)
            else:
                search(term, lang)

        else:
            term, i = "", 1
            for word in words:
                term += word + f"{'' if i == len(words) else ' '}"
                i += 1
            search(term, lang)

    else:
        say(f'{datajson["NothingFound"][lang]} \"{text}\" {datajson["ShouldISearch"][lang]}', lang)
        yesorno = listen(sr_lang)
        while yesorno.lower() not in (datajson["yes"][lang], datajson["no"][lang]):
            say(f"\"{yesorno}\" {datajson['invalidExpression'][lang]}", lang)
            yesorno = listen(sr_lang)
        print(f"{datajson['said'][lang]}: \"{yesorno}\"")

        if yesorno.lower() in datajson["nothanks"][lang]:
            say(datajson["Won'tSearch"][lang], lang)

        elif yesorno.lower() in datajson["yesplease"][lang]:
            search(text, lang)

        else:
            say(datajson["Didn'tUnderstand"][lang], lang)

except ValueError:
    say(datajson["UnknownValueError"][lang], lang)
except ConnectionError:
    say(datajson["RequestError"][lang], lang)
except TimeoutError:
    say(datajson["timeoutError"][lang], lang)
