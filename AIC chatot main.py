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

os.environ['HUGGINGFACEHUB_API_TOKEN'] = 'put your hugging key here'
load_dotenv()

engine = pyttsx3.init()

hub_llm = HuggingFaceHub(
        repo_id="google/flan-t5-large", # Language Model name to use
        model_kwargs={'temperature': 0.8, 'min_length': 40, 'max_length': 100} # Keyword arguments to pass to the model.
        
        ### temperature (float, optional, defaults to 1.0) – The value used to module the next token probabilities / The temperature of the sampling operation. 1 means regular sampling, 0 means always take the highest score, 100.0 is getting closer to uniform probability.
        ### min_length/max_length: Integer to define the minimum/maximum length in tokens of the output summary.
        
    )

# Language models (LLMs) require prompts to function.
# A prompt is a set of instructions or inputs to guide the model’s response. 
# Accepts a set of parameters from the user that can be used to generate a prompt for a language model.
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
        # Each Recognizer instance has seven methods for recognizing speech from an audio source using various APIs. 
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
            # In this case, Google Web Speech API is used (recognize_google())
            # Alternatives: Microsoft Bing Speech, Wit.ai, IBM Speech to Text
            self.audioText = recognizer.recognize_google(audio, language="en-US",)
            print("You :", self.audioText)
        except Exception:
            pass

    def text_to_speech(self, ai_text):
        # Queues a command to speak an utterance. 
        engine.say(ai_text)
        # Blocks while processing all currently queued commands. 
        engine.runAndWait()

    def response(self, audiotext):
        if audiotext != "":
            hub_chain = LLMChain(prompt=prompt, llm=hub_llm, verbose=True) # Chain to run queries against LLMs.
            ### verbose parameter enables detailed output
            ### Benificial for understanding the abstraction that LangChain provides under the hood, while executing our query.
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
