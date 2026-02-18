from abc import abstractmethod
import threading

_locals = threading.local()

def thread_local_command() -> 'ThreadLocalCommand':
    if not hasattr(_locals, 'command'):
        tlc = ThreadLocalCommand()
        _locals.command = tlc

        return tlc

    return _locals.command

def thread_local_logging() -> 'ThreadLocalLogging':
    if not hasattr(_locals, 'logging'):
        tll = ThreadLocalLogging()
        _locals.logging = tll

        return tll

    return _locals.logging

class ThreadLocalCommand:
    def __init__(self):
        self.raw_command = None
        self.scheduled_command = None

class ThreadLocalLogging:
    def __init__(self):
        self.ing_cnt = 0
        self.timings: Timable = None

class Timable:
    @abstractmethod
    def line(self):
        pass

    @abstractmethod
    def set_line(self, line: str):
        pass