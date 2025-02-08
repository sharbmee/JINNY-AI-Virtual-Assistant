import pyttsx3
import speech_recognition as sr
import eel
import time

eel.init("www") 

def speak_old(text):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 150)
    eel.DisplayMessage(f"You said: {text}")
    #print(voices)
    engine.say(text)
    engine.runAndWait()

def takecommand():

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        eel.DisplayMessage("Listening...")  # Display "Listening..." once
        # r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)

        audio = r.listen(source, timeout=10, phrase_time_limit=6)

    try:
        print("Recognizing...")
        eel.DisplayMessage("Recognizing...")  # Display "Recognizing..." once
        # Recognize speech using Google Web Speech API
        word = r.recognize_google(audio, language="en-in")
        print(f"User said: {word}")
        eel.DisplayMessage(f"You said: {word}")
        time.sleep(2)
        #speak_old(word)  # Speak back the user's command
        # eel.ShowHood()  # Update the frontend

    except Exception as e:
        # print("Error recognizing:", e)
        # eel.DisplayMessage("Error: Could not recognize speech!")
        return ""
    return word.lower()

@eel.expose
def allCommand(message=1):  
    if message == 1:
        word = takecommand()
        print(word)
    else:
        word = message

    try:
        # Ensure message is a valid string
        # if not message or message.strip() == "1":
        #     word = takecommand() or ""  # ✅ Avoids NoneType error
        # else:
        #     word = message.strip()

        # print(f"Received command: {word}")

        # # Default response
        # response = "Command not recognized."

        # Handle different commands
        if "open" in word:
            from engine.features import openCommand
            openCommand(word)
            response = f"Opened: {word}"

        elif "on youtube" in word:
            from engine.features import PlayYoutube
            PlayYoutube(word)
            response = f"Playing on YouTube: {word}"

        elif "on wikipedia" in word:
            from engine.features import search_wikipedia
            search_wikipedia(word)
            response = f"Searching Wikipedia for: {word}"

        #elif "send message" in word or "phone call" in word or "video call" in word:
            # from engine.features import findContact, whatsApp, makeCall, sendMessage
            
            # contact_no, name = findContact(word) or (None, None)  # ✅ Handle None case

            # if contact_no:
            #     speak_old("Which mode do you want to use: WhatsApp or Mobile?")
            #     preference = takecommand() or ""  # ✅ Avoid NoneType error
            #     print(f"User preference: {preference}")

            #     if "mobile" in preference:
            #         if "send message" in word or "send sms" in word: 
            #             speak_old("What message to send?")
            #             message_text = takecommand() or ""  # ✅ Avoid NoneType error
            #             sendMessage(message_text, contact_no, name)
            #             response = f"Message sent to {name or 'Unknown Contact'}"
            #         elif "phone call" in word:
            #             makeCall(name or "Unknown", contact_no)
            #             response = f"Calling {name or 'Unknown Contact'}"
            #         else:
            #             response = "Invalid mobile operation. Try again."

            #     elif "whatsapp" in preference:
            #         if "send message" in word:
            #             speak_old("What message to send?")
            #             message_text = takecommand() or ""  # ✅ Avoid NoneType error
            #             whatsApp(contact_no, message_text, "message", name or "Unknown")
            #             response = f"WhatsApp message sent to {name or 'Unknown Contact'}"
            #         elif "phone call" in word:
            #             whatsApp(contact_no, "", "call", name or "Unknown")
            #             response = f"WhatsApp call initiated to {name or 'Unknown Contact'}"
            #         else:
            #             whatsApp(contact_no, "", "video call", name or "Unknown")
            #             response = f"WhatsApp video call initiated to {name or 'Unknown Contact'}"

            #     else:
            #         response = "Invalid preference. Please try again."
            # else:
            #     response = "Contact not found."

        print(f"Response: {response}")  # Debugging log
        eel.ShowHood()  # Update the frontend
        return response  # ✅ Always return a string

    except Exception as e:
        print(f"Error in allCommand: {str(e)}")  # ✅ Logs actual error
        return f"Error: {str(e)}"  # ✅ Return error message to frontend
