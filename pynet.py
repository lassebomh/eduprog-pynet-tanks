import atexit
import __main__

def on_exit():
    
    __main__.once()

    for x in range(10):
        __main__.loop()


atexit.register(on_exit)

