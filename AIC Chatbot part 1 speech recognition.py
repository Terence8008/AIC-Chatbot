# Speech recognition
# packages needed: numpy, SpeechRecognition, gTTS
import speech_recognition as sr


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
            self.audioText = recognizer.recognize_google(audio, language="en-US",)
            print("You :", self.audioText)
        except Exception:
            pass


# Boot the AI
if __name__ == "__main__":
    ai = Chatbot("John")
    ex = True
    while ex:
        res = False
        ai.speech_to_text()

    print("----- Closing down chatbot -----")
