#!/usr/bin/env python3
# gui_frontend.py (with a toggleable log console)
from __future__ import annotations

# ─── Standard library ─────────────────────────────────────────────────────────
import ast,datetime,json,os,glob,re,sys,traceback
from pathlib import Path

from typing import *

# ─── Third-party ──────────────────────────────────────────────────────────────
from PyQt5 import(QtCore,
                  QtGui,
                  QtWidgets,
                  QtWebChannel,
                  QtWebEngineWidgets
                  )
import pytesseract
from pdf2image import convert_from_path

# ─── Local application ─────────────────────────────────────────────────────────
from abstract_pandas import get_df
from abstract_utilities import (SingletonMeta,
                                get_logFile,
                                read_from_file,
                                make_list
                                )
from abstract_utilities.robust_reader import (
    collect_filepaths,
    DEFAULT_EXCLUDE_DIRS,
    DEFAULT_EXCLUDE_FILE_PATTERNS,
    read_file_as_text,
)

from PyQt5 import(QtCore,
                  QtGui,
                  QtWidgets,
                  QtWebChannel,
                  QtWebEngineWidgets
                  )
