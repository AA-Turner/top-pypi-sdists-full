from .functions import *
def initFuncs(self):
    try:
        self.run = run
    except Exception as e:
        print(f"{e}")
    return self
