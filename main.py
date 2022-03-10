import eel
import os
from pathlib import Path

if os.name == 'nt':
    PATH = Path(f'{os.path.dirname(os.path.realpath(__file__))}\App').as_posix()
else:
    PATH = 'App'

@eel.expose
def stop():
    global stopwatch
    stopwatch = False

@eel.expose
def StopWatch():
    hour = min = sec = 0

    while stopwatch == True:
        time_elapsed = f"{hour:02d}:{min:02d}:{sec:02d}"
        eel.addText(time_elapsed)
        eel.sleep(1)
        if(59 > sec >= 0):
            sec = sec + 1
        elif(59 > min >= 0):
            sec = 0
            min = min + 1
        else:
            sec = 0
            min = 0
            hour = hour + 1


if __name__ == "__main__":

    stopwatch = True

    eel.init(PATH)
    eel.start("index.html", size=(500,350), port=8080) # This states that all code below this line will be read