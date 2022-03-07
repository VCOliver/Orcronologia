from time import sleep
from datetime import datetime
from os import system, name

def clear():

    # For Windows
    if name == 'nt':
        _ = system('cls')

    # For Mac and Linux
    else:
        _ = system('clear')

def StartTime():
    return datetime.now()

def StopWatch():

    sec = 0
    min = 0
    hour = 0

    while True:
        try:
            input("Press enter to continue aand ctrl+C to exit the StopWatch")
            print("StopWatch has started")
            while True:
                time_elapsed = f"{hour:02d}:{min:02d}:{sec:02d}"
                print("Time elapsed:", time_elapsed, end='\n')
                print("Press ctrl+C to exit the StopWatch")
                sleep(1)
                if(59 > sec >= 0):
                    sec = sec + 1
                elif(59 > min >= 0):
                    sec = 0
                    min = min + 1
                else:
                    sec = 0
                    min = 0
                    hour = hour + 1
                clear()
        except KeyboardInterrupt:
            print()
            print("Timer has stopped")
            return datetime.now()