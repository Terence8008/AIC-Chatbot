# Chatbot Main file is here
# packages needed: numpy, SpeechRecognition, gTTS, transformers, tensorflow, Pyaudio
import speech_recognition as sr


class Chatbot:
    def __init__(self, name):
        print("----- Starting up", name, "-----")
        self.name = name

    def speech_to_text(self):
        recognizer = sr.Recognizer()
        recognizer.energy_threshold = 300
        with sr.Microphone() as mic:
            print("listening...")
            audio = recognizer.listen(mic)
        try:
            self.text = recognizer.recognize_google(audio, language="en-US",)
            print("You :", self.text)
        except:
            print("Sorry can you repeat that?")


# Boot the AI
if __name__ == "__main__":
    ai = Chatbot("John")
    while True:
        ai.speech_to_text()

