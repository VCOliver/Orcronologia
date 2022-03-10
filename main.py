import eel
import os
from pathlib import Path

PATH = Path(f'{os.path.dirname(os.path.realpath(__file__))}\App').as_posix()

@eel.expose
def hello():
    print("Hello world!")

if __name__ == "__main__":
    eel.init(PATH)
    eel.start("index.html", size=(1000,600), block=False) # This states that all code below this line will be read

    hour = min = sec = 0

    while True:
        time_elapsed = f"{hour:02d}:{min:02d}:{sec:02d}"
        eel.addText(f"Time elapsed: {time_elapsed}")
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
