from .imports import *
from ..widgets import *

def _log_exception(exc_type, exc, tb):
    logging.error("Uncaught exception",
                  exc_info=(exc_type, exc, tb))

def _threading_excepthook(args):
    # Python >= 3.8
    logging.error("Uncaught threading exception",
                  exc_info=(args.exc_type, args.exc_value, args.exc_traceback))

def _qt_message_handler(mode, context, message):
    # Pipe Qt warnings/errors into logging
    level = logging.WARNING
    if mode in (QtMsgType.QtCriticalMsg, QtMsgType.QtFatalMsg):
        level = logging.ERROR
    elif mode == QtMsgType.QtInfoMsg:
        level = logging.INFO
    logging.log(level, f"Qt: {message}")

def install_global_traps():
    sys.excepthook = _log_exception
    if hasattr(threading, "excepthook"):
        threading.excepthook = _threading_excepthook
    qInstallMessageHandler(_qt_message_handler)
def get_combo_text(combo):
    return combo.currentText().rstrip("/")

def get_combo_index(combo, text):
    for i in range(combo.count()):
        if combo.itemText(i) == text:
            return i

def on_changed(widget, *args):
    # widget is guaranteed to be first
    if hasattr(widget, "currentText") and hasattr(widget, "itemData"):
        txt = get_combo_text(widget)
        val = get_combo_value(widget, txt)
        print("combo change:", txt, val)
    else:
        print("changed:", widget, args)
def get_combo_value(combo, text=None):
    text = text or get_combo_text(combo)
    i = get_combo_index(combo, text)
    if i is not None and 0 <= i < combo.count():
        return combo.itemData(i)
