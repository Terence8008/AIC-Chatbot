# Chatbot Main file is here
# packages needed:  SpeechRecognition, gTTS, transformers, tensorflow,python-dotenv, langchain,
# langchainopenai (partner package)
# keyboard pacakge maybe keyboard-mac for mac
# pyttsx3

import keyboard
import speech_recognition as sr
import time
from dotenv import load_dotenv
from langchain_community.llms import HuggingFaceHub
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
import pyttsx3

os.environ['HUGGINGFACEHUB_API_TOKEN'] = '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'
load_dotenv()

engine = pyttsx3.init()

hub_llm = HuggingFaceHub(
        repo_id="google/flan-t5-large",
        model_kwargs={'temperature': 0.8, 'min_length': 40, 'max_length': 100}
    )

prompt = PromptTemplate(
    input_variables=["question"],
    template="Answer this question in a happy manner: {question}"
)


class Chatbot:
    def __init__(self, name):
        print("----- Starting up", name, "-----")
        self.name = name
        self.audioText = ""
        self.response = ""
        self.status = "Sleep"


    def speech_to_text(self):
        recognizer = sr.Recognizer()

        # Represents the energy level threshold for sounds.
        # Values below this threshold are considered silence, and values above this threshold are considered speech.
        recognizer.energy_threshold = 300

        # Represents the minimum length of silence (in seconds) that will register as the end of a phrase.
        recognizer.pause_threshold = 0.8

        with sr.Microphone() as mic:
            print("listening...")
            audio = recognizer.listen(mic)
        try:
            self.audioText = recognizer.recognize_google(audio, language="en-US",)
            print("You :", self.audioText)
        except Exception:
            pass

    def text_to_speech(self, ai_text):
        engine.say(ai_text)
        engine.runAndWait()

    def response(self, audiotext):
        if audiotext != "":
            hub_chain = LLMChain(prompt=prompt, llm=hub_llm, verbose=True)
            print(hub_chain.run(audiotext))
        else:
            print("No input found please try again")

    def wake_up(self, audio_text):
        return True if self.name in audio_text.lower() else False


# Boot the AI
if __name__ == "__main__":
    ai = Chatbot("John")
    ex = True
    while ex:
        if keyboard.read_key() == 'z':
            ai.speech_to_text()
            ai.response(ai.audioText)
            #ai.text_to_speech(ai.response())
        elif keyboard.read_key() == 'q':
            ex = False
        else:
            pass

print("----- Closing down chatbot -----")
