import datetime
import os.path
import smtplib
import ssl
import webbrowser
import winsound

from PyDictionary import PyDictionary as PyDictionary
import pyautogui
import pyjokes
import pyttsx3
import pywhatkit
import speech_recognition as sr
import wikipedia
import face_recognition
import cv2

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('rate', 150)
engine.setProperty('voice', voices[0].id)


def changevoice():
    engine.setProperty('voice', voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishme():
    hour = int(datetime.datetime.now().hour)
    if 4 <= hour < 12:
        speak("Good morning sir!")
    elif 12 <= hour < 16:
        speak("Good afternoon sir!")
    else:
        speak("Good evening sir!")

    speak("What do you want me to do, sir?")


def command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...\n")
        said = r.recognize_google(audio, language='en-in')
        print(f"You said : {said}")
    except Exception as e:
        print("Say that again please...")
        return "None"
    return said


def sendEmail(to, content):
    port = 465
    file = open('pass.txt')
    password = str(file.read()).strip()
    file.close()
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login("abc@gmail.com", password)
        server.sendmail("abc@gmail.com", to, content)
        speak("Email Sent!")

todo_list = []
email_list = {'myself': 'abc@gmail.com', 'father': 'xyz@gmail.com'}
contact = {'father':'+91123456789','mummy':'+91987654321'}
wishme()
while True:
    task = command().lower()
    if 'change your voice' in task:
        changevoice()
    elif 'explore' in task:
        speak("Searching Wikipedia")
        task = task.replace("explore", "")
        result = wikipedia.summary(task, sentences=4)
        speak("According to wikipedia")
        print(result)
        speak(result)
    elif 'search' in task:
        task = task.replace("search", "")
        pywhatkit.search(task.strip())
    elif 'launch' in task:
        task = task.replace("launch", "")
        if 'code' in task:
            speak('Opening VS Code')
            os.startfile('code')
        elif 'chrome' in task:
            speak('Opening Chrome')
            os.startfile('chrome')
        elif 'maps' in task:
            speak('Showing Maps')
            webbrowser.open('https://www.google.com/maps')
        else:
            speak("Opening "+task.strip())
            webbrowser.open(task.strip() + ".com")
    elif 'close' in task:
        task = task.replace("close", "")
        if 'edge' in task:
            os.system("TASKKILL /f /im msedge.exe")
        else:
            s = "TASKKILL /f /im "+task.strip()+".exe"
            os.system(s)
        speak('Closed!')
    elif 'show details' in task:
        task = task.replace("show details", "details")
        webbrowser.open(task.strip())
    elif 'time' in task:
        time = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The time is {time}")
    elif 'play' in task:
        task = task.replace('play', '').strip()
        speak("Playing " + task)
        pywhatkit.playonyt(task)
    elif 'email' in task:
        speak("Whom should I send the email to?")
        to = command()
        speak("What should the email say?")
        content = command()
        sendEmail(email_list[to], content)
    elif 'whatsapp' in task:
        speak('Whom is the message directed to sir?')
        person = command()
        speak("What should the message say sir?")
        msg = command()
        speak("Tell me the time of sending message in hours")
        hrs = int(command())
        speak("At what minute of hour sir?")
        minutes = int(command())
        pywhatkit.sendwhatmsg(contact[person], msg, hrs, minutes, 3)
        speak("Ok Sir! Sending message!")
    elif 'screenshot' in task:
        kk = pyautogui.screenshot()
        i = 1
        kk.save('./screenshots/SS'+str(i)+".jpg")
        i += 1
    elif 'joke' in task:
        speak(pyjokes.get_joke())
    elif 'meaning' in task:
        speak("Searching dictionary!")
        task = task.replace("what is the meaning of", "")
        result = PyDictionary.meaning(task)
        print(f"The meaning of {task} is {result}")
        speak(f"The meaning of {task} is {result}")
    elif 'check for security' in task:
        image = face_recognition.load_image_file('./images/xyz.png')
        image_encoding = face_recognition.face_encodings(image)[0]
        known_face_encodings = [
            image_encoding
        ]

        known_face_names = [
            "xyz"
        ]

        videoCaptureObject = cv2.VideoCapture(0)
        result = True
        while (result):
            ret, frame = videoCaptureObject.read()
            cv2.imwrite("Capture.jpg", frame)
            result = False
        videoCaptureObject.release()
        cv2.destroyAllWindows()

        cap = face_recognition.load_image_file("Capture.jpg")
        face_locations = face_recognition.face_locations(cap)
        face_encoding = face_recognition.face_encodings(cap,face_locations)
        matches =None
        for (top, right, bottom, left), f_e in zip(face_locations, face_encoding):
            matches = face_recognition.compare_faces(known_face_encodings, f_e)
        if matches is not None:
            if True in matches:
                speak("I can see you sir!")
            else:
                winsound.PlaySound("alert.wav", winsound.SND_ASYNC)
        else:
            speak("No one present at your place sir!")
