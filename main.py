import eel

@eel.expose
def hello():
    print("Hello world!")

if __name__ == "__main__":
    eel.init("App")
    eel.start("index.html")