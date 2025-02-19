import pyttsx3

def speak(text):
    # Speaking engine
    engine = pyttsx3.init()
    engine.setProperty('rate', 275) # Adjust speaking rate
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id) # Change voice

    engine.say(text)
    engine.runAndWait()