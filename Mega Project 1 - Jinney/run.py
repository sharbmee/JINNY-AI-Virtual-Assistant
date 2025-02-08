import multiprocessing
import time
from main import start
from engine.features import hotword  # Import at the top

# Create a stop event for clean termination
stop_event = multiprocessing.Event()

# Jarvis process
def startJarvis():
    print("Process 1 (Jarvis) is running.")
    start()

# To run hotword
def listenHotword():
        # Code for process 2
        print("Process 2 is running.")
        from engine.features import hotword
        hotword()

    # Start both processes
if __name__ == '__main__':
        p1 = multiprocessing.Process(target=startJarvis)
        p2 = multiprocessing.Process(target=listenHotword)
        p1.start()
        p2.start()
        p1.join()

        if p2.is_alive():
            p2.terminate()
            p2.join()

        print("system stop")