# Chatbot Main file is here
# packages needed: numpy, SpeechRecognition, gTTS, transformers, tensorflow, Pyaudio, keras
# keras3 not supported
import speech_recognition as sr
from gtts import gTTS
import transformers
import os
from tensorflow import keras
import segmentation_models as sm


import numpy as np
import time



class Chatbot:
    def __init__(self, name):
        print("----- Starting up", name, "-----")
        self.name = name
        self.audioText = ""
        self.status = "Sleep"


    def speech_to_text(self):
        recognizer = sr.Recognizer()

        # Represents the energy level threshold for sounds.
        # Values below this threshold are considered silence, and values above this threshold are considered speech.
        recognizer.energy_threshold = 300

        # Represents the minimum length of silence (in seconds) that will register as the end of a phrase.
        recognizer.pause_threshold = 0.8;

        with sr.Microphone() as mic:
            print("listening...")
            audio = recognizer.listen(mic)
        try:
            self.text = recognizer.recognize_google(audio, language="en-US",)
            print("You :", self.audioText)
        except Exception:
            pass

    def text_to_speech(self, ai_text):
        print("Dev --> ", ai_text)
        speaker = gTTS(text=ai_text, lang="en", slow=False)
        speaker.save("res.mp3")
        statbuf = os.stat("res.mp3")
        mbytes = statbuf.st_size / 1024
        duration = mbytes / 200
        os.system('start res.mp3')  # if you are using mac->afplay or else for windows->start
        # os.system("close res.mp3")
        time.sleep(int(50 * duration))
        os.remove("res.mp3")


# Boot the AI
if __name__ == "__main__":
    ai = Chatbot("John")
    nlp = transformers.pipeline("conversational", model="microsoft/DialoGPT-medium")
    os.environ["TOKENIZERS_PARALLELISM"] = 'true'
    ex = True
    while ex:
        res = False
        ai.speech_to_text()
        if ai.status == "Sleep":
            if ai.wake_up(ai.audioText) is True:
                print("Hello, I'm " + ai.name + "the AI, what can I help you with?")
                ai.status = "Awake"
            else:
                pass

        if ai.status == "Awake":
            if any(i in ai.text for i in ["thank","thanks"]):
                res = np.random.choice(["you're welcome!","anytime!","no problem!","cool!","I'm here if you need me!","mention not"])
            elif any(i in ai.text for i in ["exit","close"]):
                res = np.random.choice(["Tata","Have a good day","Bye","Goodbye","Hope to meet soon","peace out!"])
                ex=False

        else:
            if ai.text == "ERROR":
                res = "Sorry, come again?"
            else:
                chat = nlp(transformers.Conversation(ai.text), pad_token_id=50256)
                res = str(chat)
                res = res[res.find("bot >> ") + 6:].strip()

        if res:
            ai.text_to_speech(res)

    print("----- Closing down chatbot -----")
