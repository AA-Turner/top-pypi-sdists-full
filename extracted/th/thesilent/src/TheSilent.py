import subprocess
import sys
import threading

class Threading:
    def __init__(self, func):
        self.func = func
    def __call__(self, *args, **kwargs):
        threading.Thread(target=self.func, args=args, kwargs=kwargs).start()

if __name__ == "__main__":
    try:
        subprocess.Popen(sys.argv[1:])
    
    except IndexError:
        pass