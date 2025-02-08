import os
import eel

from engine.features import *
from engine.command import *

def start():

    eel.init('www')  # Initialize Eel with the directory containing your HTML/JS

    playAssistantSound()

    eel.start('index.html', mode='edge', host='localhost', block=True)  # Start the Eel app
    os.system('start msedge.exe --app="http://127.0.0.1:5500/www/index.html"')

    #eel.start('index.html', mode=None, host='localhost', block=True)