import speech_recognition as sr
import pyttsx3

# Initialize the recognizer
r = sr.Recognizer() # Object used to interact with microphone

def record_text():
    # Loop in case of errors
    while(True):

        try:
            # Use microphone as source input
            with sr.Microphone(device_index=1) as source2:
                # prepares for input
                r.adjust_for_ambient_noise(source2, duration=0.2)

                # listens for user input
                audio2 = r.listen(source2)

                # recognize audio
                MyText = r.recognize_google(audio2)

                return MyText

        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        except sr.UnknownValueError:
            continue
            #print("unknown error occured")
            
    return

def output_text(text):
    f = open("History/output.txt", "a")
    f.write(text)
    f.write("\n")
    f.close()
    
    return
