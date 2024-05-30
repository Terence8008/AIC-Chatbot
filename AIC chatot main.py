# Chatbot Main file is here
# packages needed:  SpeechRecognition, tensorflow,python-dotenv, langchain,
# langchain-openai (partner package)
# langchain-community
# Huggingface-hub
# Pyaudio (no import but need)
# keyboard pacakge maybe keyboard-mac for mac
# pyttsx3 (text to speech)z

import keyboard
import speech_recognition as sr
from langchain_community.llms import HuggingFaceHub
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
# import os
# from dotenv import load_dotenv
import pyttsx3

# os.environ['HUGGINGFACEHUB_API_TOKEN'] = 'Hugging_face_token'
# load_dotenv()

engine = pyttsx3.init()

hub_llm = HuggingFaceHub(
        repo_id="google/flan-t5-large",
        model_kwargs={'temperature': 0.8, 'repetition_penalty': 1.2, 'num_return_sequences': 1, 'min_length': 40}
    )

prompt = PromptTemplate(
    input_variables=["question"],
    template="Answer this question in a happy manner: {question}"
)


class Chatbot:
    # Constructor
    def __init__(self, name):
        print("----- Starting up", name, "-----")
        self.name = name
        self.audioText = ""
        self.bot_response = ""

    def speech_to_text(self):
        recognizer = sr.Recognizer()

        # Represents the energy level threshold for sounds.
        # Values below this threshold are considered silence, and values above this threshold are considered speech.
        recognizer.energy_threshold = 300

        # Represents the minimum length of silence (in seconds) that will register as the end of a phrase.
        recognizer.pause_threshold = 0.5

        with sr.Microphone() as mic:
            print("listening...")
            audio = recognizer.listen(mic)
        try:
            self.audioText = recognizer.recognize_google(audio, language="en-US")
            print("You :", self.audioText)
        except Exception:
            pass

    def text_to_speech(self, ai_text):
        engine.say(ai_text)
        engine.runAndWait()

    def response(self, audiotext):
        if audiotext != "":
            hub_chain = LLMChain(prompt=prompt, llm=hub_llm, verbose=True)
            self.bot_response = hub_chain.run(audiotext)
            print(self.bot_response)
            return self.bot_response
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
            ai.text_to_speech(ai.bot_response)
        elif keyboard.read_key() == 'q':
            ex = False
        else:
            pass

print("----- Closing down chatbot -----")
