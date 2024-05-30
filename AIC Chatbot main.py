# Chatbot Main file is here
# packages needed:  SpeechRecognition, python-dotenv, langchain
# langchain-community
# langchain_huggingface
# Huggingface-hub
# Pyaudio (no import but needed)
# keyboard pacakge maybe keyboard-mac for mac
# pyttsx3 (text to speech)

import keyboard
import speech_recognition as sr
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_huggingface import HuggingFaceEndpoint
import os
from dotenv import load_dotenv
import pyttsx3

engine = pyttsx3.init()
os.environ['HUGGINGFACEHUB_API_TOKEN'] = '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'
load_dotenv()

# temperature (float, optional, defaults to 1.0) – The value used to module the next token probabilities
# The temperature of the sampling operation. 1 means regular sampling, 0 means always take the highest score,
# 100.0 is getting closer to uniform probability.
# min_length/max_length: Integer to define the minimum/maximum length in tokens of the output summary.
repo_id = "mistralai/Mistral-7B-Instruct-v0.3"
llm = HuggingFaceEndpoint(repo_id=repo_id, temperature=0.7, )

# Language models (LLMs) require prompts to function.
# A prompt is a set of instructions or inputs to guide the model’s response.
# Accepts a set of parameters from the user that can be used to generate a prompt for a language model.
prompt = PromptTemplate(
    input_variables=["question"],
    template="Your name is John, only answer what i have ask. Do not repeat yourself. Do not use any Emoji. Answer "
             "this question in a happy manner: {question}"
)


class Chatbot:
    # Constructor
    def __init__(self, name):
        print("----- Starting up", name, "-----")
        self.audioText = ""
        self.bot_response = ""

    def speech_to_text(self):
        # Each Recognizer instance has seven methods for recognizing speech from an audio source using various APIs. 
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
            # In this case, Google Web Speech API is used (recognize_google())
            # Alternatives: Microsoft Bing Speech, Wit.ai, IBM Speech to Text
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
            hub_chain = LLMChain(prompt=prompt, llm=llm, verbose=True)
            self.bot_response = hub_chain.run(audiotext)
            print(self.bot_response)
            return self.bot_response
            # verbose parameter enables detailed output
            # Beneficial for understanding the abstraction that LangChain provides under the hood,
            # while executing our query.

        else:
            print("No input found please try again")


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

