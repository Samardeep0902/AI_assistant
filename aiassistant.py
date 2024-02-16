import pyttsx3
import datetime
import speech_recognition as sr 
import wikipedia 
import webbrowser
import os
import pywhatkit as kit
import cv2
import openai
from dotenv import dotenv_values

config = dotenv_values("samar.env")
openai.api_key = config["api_key"]
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[1].id)
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")   

    else:
        speak("Good Evening!")  

    speak("I am your personal ai assistant. Please tell me how may I help you")       

def takeCommand():
    #It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        # print(e)    
        print("Say that again please...")  
        return "None"
    return query



def ai(prompt):
    response= openai.Completion.create(
          model="text-davinci-003",
          prompt = prompt ,
          max_tokens = 16
      )
    if not os.path.exists('openai'):
        os.mkdir('openai')
    f = open(f"openai/{''.join(prompt.split('intelligence')[1:])}.txt","w")
    f.write(response["choices"][0]["text"])
    return response["choices"][0]["text"]    

def cam():
    vid = cv2.VideoCapture(0)
    while True:
        ret , frame = vid.read()
         # Display the resulting frame
        cv2.imshow('press q to quit', frame)
        
        # the 'q' button is set as the
        # quitting button you may use any
        # desired button of your choice
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
  
    # After the loop release the cap object
    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()    

if __name__ == "__main__":
    wishMe()
    while True:
    # if 1:
        query = takeCommand().lower()

        # Logic for executing tasks based on query
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            webbrowser.open("google.com")

        elif 'open stackoverflow' in query:
            webbrowser.open("stackoverflow.com")   


        elif 'play music' in query:
            music_dir = 'D:\\Non Critical\\songs\\Favorite Songs2'
            songs = os.listdir(music_dir)
            print(songs)    
            os.startfile(os.path.join(music_dir, songs[0]))

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            speak(f"Sir, the time is {strTime}")

        elif 'open code' in query:
            codePath = "C:\\Users\\Haris\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)


        elif "send whatsapp message" in query:
            speak("say the number")
            b= speak()
            c  = b.replace(" ",'')
            speak("say the message")
            message = speak()
            kit.sendwhatmsg_instantly(f"+91{c}",f'{message}',12)        

        elif " on youtube" in query:
           query =query.replace("on youtube","")
           kit.playonyt(query)
        elif "play " in query:
            kit.playonyt(query)
        elif "open camera" in query:
            cam()

        elif "artificial intelligence" in query:
            speak(ai(query))                

          
        elif 'bye' in query:
            speak('good bye!')
            exit(0)
