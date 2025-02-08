from shlex import quote
import struct
import subprocess
import time
import eel
import os
import threading
from playsound import playsound
import pvporcupine
import pyaudio
import pyautogui
from engine.config import ASSISTANT_NAME
from engine.command import speak_old
import pywhatkit as kit
import re
import sqlite3
import webbrowser
import wikipedia

from engine.helper import extract_yt_term, remove_words

con = sqlite3.connect("jinny.db")
cursor = con.cursor()

#playing assistant sound function

@eel.expose
def playAssistantSound():
    # print("playAssistantSound called")
    music_dir = "www/assets/audio/starting sounds.mp3"
    playsound(music_dir)

    # threading.Thread(target=play_sound).start()  #Use a thread to prevent blocking

def openCommand(word):
    word = word.replace(ASSISTANT_NAME, "")
    word = word.replace("open", "")
    word.lower()
    
    app_name = word.strip()

    if app_name != "":

        try:
            cursor.execute(
                'SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak_old("Opening "+word)
                os.startfile(results[0][0])

            elif len(results) == 0: 
                cursor.execute(
                'SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()
                
                if len(results) != 0:
                    speak_old("Opening "+word)
                    webbrowser.open(results[0][0])

                else:
                    speak_old("Opening "+word)
                    try:
                        os.system('start '+word)
                    except:
                        speak_old("not found")
        except:
            speak_old("some thing went wrong")

def PlayYoutube(word):
    search_term = extract_yt_term(word)
    speak_old("Playing "+search_term+" on YouTube")
    kit.playonyt(search_term)

def search_wikipedia(word):
    try:
        result = wikipedia.summary(word, sentences=1)  # Get 1 sentences summary
        speak_old (result)
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Multiple results found: {e.options[:5]}"  # Suggest 5 options
    except wikipedia.exceptions.PageError:
        return "Sorry, no results found on Wikipedia."
    except Exception as e:
        return f"An error occurred: {e}"

def hotword():
    porcupine=None
    paud=None
    audio_stream=None
    try:
        
        # pre trained keywords    
        porcupine=pvporcupine.create(keywords=["jinny","alexa"]) 
        paud=pyaudio.PyAudio()
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
        
        # loop for streaming
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

            # processing keyword comes from mic 
            keyword_index=porcupine.process(keyword)

            # checking first keyword detetcted for not
            if keyword_index>=0:
                print("hotword detected")

                # pressing shorcut key win+j
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")
                
    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()

# find contacts
def findContact(word):
    
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video']
    word = remove_words(word, words_to_remove)

    try:
        word = word.strip().lower()
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + word + '%', word + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])

        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, word
    except:
        speak_old('not exist in contacts')
        return 0, 0
    
def whatsApp(mobile_no, message, flag, name):
    

    if flag == 'message':
        target_tab = 12
        jarvis_message = "message send successfully to "+name

    elif flag == 'call':
        target_tab = 7
        message = ''
        jarvis_message = "calling to "+name

    else:
        target_tab = 6
        message = ''
        jarvis_message = "staring video call with "+name


    # Encode the message for URL
    encoded_message = quote(message)
    print(encoded_message)
    # Construct the URL
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"

    # Construct the full command
    full_command = f'start "" "{whatsapp_url}"'

    # Open WhatsApp with the constructed URL using cmd.exe
    subprocess.run(full_command, shell=True)
    time.sleep(5)
    subprocess.run(full_command, shell=True)
    
    pyautogui.hotkey('ctrl', 'f')

    for i in range(1, target_tab):
        pyautogui.hotkey('tab')

    pyautogui.hotkey('enter')
    speak_old(jarvis_message)