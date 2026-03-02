from PyQt6 import QtCore, QtGui, QtWidgets
import os, sys, shlex, logging
from logging.handlers import RotatingFileHandler

# ---------------- shared rotating logger ----------------
LOG_DIR = os.path.join(os.path.expanduser("~"), ".cache", "abstract_finder")
LOG_FILE = os.path.join(LOG_DIR, "finder.log")
os.makedirs(LOG_DIR, exist_ok=True)

root_logger = logging.getLogger("launcher")
if not root_logger.handlers:
    root_logger.setLevel(logging.DEBUG)
    fh = RotatingFileHandler(LOG_FILE, maxBytes=5_000_000, backupCount=5, encoding="utf-8")
    fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s:%(lineno)d - %(message)s"))
    root_logger.addHandler(fh)
# add near the top of the module
import shutil, os, shlex, sys
from typing import Tuple, List
from PyQt6.QtWidgets import QApplication,QTextEdit
from PyQt6 import QtWidgets, QtGui, QtCore, QtGui, QtWidgets
from pathlib import Path
import traceback, sys, logging, os,threading
from logging.handlers import RotatingFileHandler
from PyQt6.QtCore import QObject,pyqtSignal
logger = logging
# Setup robust logging
LOG_DIR = os.path.join(os.path.expanduser("~"), ".cache", "abstract_finder")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "finder.log")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
def get_log_file_path():
    return LOG_FILE
import clipboard,os, logging, traceback, threading, io, sys, faulthandler, traceback, signal
from typing import *
from dataclasses import dataclass
from logging.handlers import RotatingFileHandler
from PyQt6 import *
