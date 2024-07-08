import speech_recognition as sr
import pyttsx3
import pyautogui
import time
import subprocess
import webbrowser
import wikipedia

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Initialize recognizer
recognizer = sr.Recognizer()
speak("Hello, how can i help you?")
# Function to recognize speech
def recognize_speech_from_mic():
    with sr.Microphone() as source:
        speak("Listening...")
        print("Listening...")
        audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            speak(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            speak("Sorry, I did not understand that.")
            return None
        except sr.RequestError:
            print("Request error.")
            return None

def open_icon(command):
    if "browser" in command.lower():
        icon_x, icon_y=100, 100
        pyautogui.click(icon_x, icon_y)

    elif "calculator" in command.lower():
        icon_x, icon_y=100, 100
        pyautogui.click(icon_x, icon_y)

    elif "notepad" in command.lower():
        icon_x, icon_y=100, 100
        pyautogui.click(icon_x, icon_y)

def open_website(url):
    webbrowser.open(url)
    speak(f"Opening {url}")

def search_wikipedia(query):
    results = wikipedia.summary(query, sentences=2)
    speak(f"According to Wikipedia, {results}")

# Function to execute commands
def execute_command(command):
    if "move cursor" in command:
        try:
            direction, distance = command.split(" ")[2], int(command.split(" ")[3])
            if direction == "left":
                pyautogui.moveRel(-distance, 0, duration=0.25)
            elif direction == "right":
                pyautogui.moveRel(distance, 0, duration=0.25)
            elif direction == "up":
                pyautogui.moveRel(0, -distance, duration=0.25)
            elif direction == "down":
                pyautogui.moveRel(0, distance, duration=0.25)
        except:
            print("Invalid move mouse command")

    elif "open website" in command:
            speak("Which website would you like to open?")
            website = recognize_speech_from_mic()
            open_website(f"https://{website}")

    elif "search wikipedia for" in command:
            query = command.replace("search wikipedia for", "").strip()
            search_wikipedia(query)
    
    elif "click" in command:
        pyautogui.click()

    elif "double click" in command:
        pyautogui.doubleClick()

    elif "right click" in command:
        pyautogui.rightClick()

    elif "minimise window" in command:
        pyautogui.hotkey('win', 'down')

    elif "maximize window" in command:
        pyautogui.hotkey('win', 'up')

    elif "close window" in command:
        pyautogui.hotkey('alt', 'f4')

    elif "explorer" in command:
        pyautogui.hotkey('win', 'e')
        '''file_name= command.replace("open file","").strip()
        file_path=f"C:/Users/bless/OneDrive/Documents/{file_name}"

        try:
            subprocess.Popen(["open", file_path])
            print(f"opening {file_name}")
        except FileNotFoundError:
            print(f"File '{file_name}' not found")'''

    elif "increase volume" in command:
        pyautogui.press('volumeup')

    elif "decrease volume" in command:
        pyautogui.press('volumedown')

    elif "scroll up" in command:
        pyautogui.scroll(100)
        print("Scrolling up")

    elif "scroll down" in command:
        pyautogui.scroll(-100)
        print("Scrolling down")

    elif "select" in command:
        pyautogui.mouseDown()
        pyautogui.moveTo(500, 500, duration=1)
        pyautogui.mouseUp()

    elif "all" in command:
        pyautogui.hotkey('ctrl','a')

    elif "copy" in command:
        pyautogui.hotkey('ctrl','c')

    elif "paste" in command:
        pyautogui.hotkey('ctrl','v')

    elif "save" in command:
        pyautogui.hotkey('ctrl','s')


    else:
        print("Unknown command")

# Main loop
while True:
    command = recognize_speech_from_mic()
    if command:
        execute_command(command)
