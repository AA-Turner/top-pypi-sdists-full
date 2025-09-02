from .initFuncs import *
import logging

class QTextEditLogger(logging.Handler):
    def __init__(self, widget):
        super().__init__()                 # ← fixed
        self.widget = widget
        self.widget.setReadOnly(True)
        self.api_prefix = "/api"

QTextEditLogger = initFuncs(QTextEditLogger)
