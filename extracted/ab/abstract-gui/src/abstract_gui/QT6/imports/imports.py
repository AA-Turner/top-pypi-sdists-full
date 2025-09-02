#!/usr/bin/env python3
from typing import *
from pathlib import Path
from dataclasses import dataclass
from functools import partial, lru_cache
from .abstract_utils import (
    get_set_attr, is_number, make_list, safe_read_from_json, read_from_file, make_dirs, eatAll,
    import_symbols_to_parent, call_for_all_tabs, MIME_TYPES,write_to_file
    )
from .general_imports import (
    time,  pydot, inspect, threading, enum, sys, requests, subprocess, re,  os , shutil, shlex,
    tempfile, stat, faulthandler, logging, json, clipboard, traceback, io, signal, faulthandler
    )
from logging.handlers import RotatingFileHandler
from PyQt6 import QtGui,QtCore,QtWidgets
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
