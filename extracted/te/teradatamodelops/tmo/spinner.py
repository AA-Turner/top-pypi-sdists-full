import os
import sys
import threading

os.system("")  # enables ansi escape characters in terminal

CODE = {
    "CYAN": "\033[36m",
    "END": "\033[0m",
    "RM_LINE": "\033[2K\r",
    "HIDE_CURSOR": "\033[?25l",
    "SHOW_CURSOR": "\033[?25h",
    "CURSOR_NEXT_LINE": "\033[1E",
    "CURSOR_INIT": "\033[0G",
}


class ProgressBase(threading.Thread):
    inplace = None
    stopFlag = None

    def __init__(self):
        self.rlock = threading.RLock()
        self.cv = threading.Condition()
        threading.Thread.__init__(self)
        self.daemon = True

    def __call__(self):
        self.start()

    def back_step(self):
        if self.inplace:
            sys_print(CODE["CURSOR_NEXT_LINE"])

    def remove_line(self):
        if self.inplace:
            sys_print(CODE["RM_LINE"])

    def start(self):
        self.stopFlag = 0
        threading.Thread.start(self)

    def stop(self):
        self.stopFlag = 1
        sys_print(CODE["SHOW_CURSOR"])
        self.cv.acquire()
        self.cv.notify()
        self.cv.release()
        self.rlock.acquire()


class Spinner(ProgressBase):

    def __init__(self, msg="", speed=0.1):
        self.__seq = ["⣾", "⣷", "⣯", "⣟", "⡿", "⢿", "⣻", "⣽"]
        self.__speed = speed
        self.__msg = msg
        self.inplace = 1
        ProgressBase.__init__(self)

    def run(self):
        self.rlock.acquire()
        self.cv.acquire()
        sys_print(CODE["HIDE_CURSOR"])
        while 1:
            for char in self.__seq:
                self.cv.wait(self.__speed)
                if self.stopFlag:
                    self.back_step()
                    try:
                        return
                    finally:
                        self.rlock.release()
                if self.inplace:
                    sys_print(
                        f"{CODE['RM_LINE']}{CODE['CYAN']}{char}{CODE['END']} {self.__msg}{CODE['CURSOR_INIT']}"
                    )


def sys_print(msg):
    sys.stdout.write(msg)
    sys.stdout.flush()


def spin_it(function, msg, speed=0.25, *args, **kwargs):
    indicator = Spinner(msg, speed)
    indicator.start()
    result = function(*args, **kwargs)
    indicator.stop()
    indicator.remove_line()
    return result
