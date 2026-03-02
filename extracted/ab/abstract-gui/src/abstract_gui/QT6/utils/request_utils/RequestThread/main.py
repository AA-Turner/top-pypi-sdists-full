from .initFuncs import *
from PyQt6.QtCore import QThread, pyqtSignal

class requestThread(QThread):
    response_signal = pyqtSignal(str, str)  # payload, log_msg
    error_signal    = pyqtSignal(str)       # error text

    def __init__(self, method: str, url: str, headers: dict, params: dict,
                 is_fetch_endpoints: bool = False, is_detect: bool = False, timeout: int = 10):
        super().__init__()
        self.method = method
        self.url = url
        self.headers = headers or {}
        self.params = params or {}
        self.is_fetch_endpoints = is_fetch_endpoints
        self.is_detect = is_detect
        self.timeout = timeout

requestThread = initFuncs(requestThread)
