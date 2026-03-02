#!/usr/bin/env python3
from typing import *
from pathlib import Path
from functools import partial, lru_cache
from abstract_utilities import get_set_attr, is_number, make_list, safe_read_from_json, read_from_file, make_dirs, eatAll
from abstract_utilities.dynimport import import_symbols_to_parent, call_for_all_tabs
from abstract_utilities.type_utils import MIME_TYPES
from PyQt6 import QtGui, QtCore, QtWidgets
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
import time,  pydot, inspect, threading, enum, sys, requests, subprocess
import re,  os , shutil, shlex, tempfile, stat, faulthandler
import logging, json, clipboard, traceback, io, signal. faulthandler
from abstract_utilities import 
from dataclasses import dataclass
from logging.handlers import RotatingFileHandler
import_modules = [
    {"module":'abstract_gui.QT6.managers',["startConsole","windowManagerConsole","startWindowManagerConsole","appRunnerTab","startAppRunnerConsole","launcherWindowTab","startLauncherWindowConsole","logPaneTab","startLogPaneTabConsole"]},
    {"module":'abstract_react.react_analyzer',"symbol":["ImportGraphWorker","build_graph_reachable","build_graph_all","invert_to_symbol_map","invert_to_function_map","invert_to_variable_map"]},
    {"module":'abstract_paths.content_utils.file_utils',"symbols":['get_directory_map','findGlobFiles']},
    {"module":'abstract_paths.file_filtering.file_filters',"symbols":['collect_filepaths']},
    {"module":'abstract_paths.python_utils.utils.utils',"symbols":['get_py_script_paths']},
    {"module":'abstract_paths.content_utils.diff_engine',"symbols":['plan_previews','apply_diff_text','ApplyReport','write_text_atomic']},
    {"module":'abstract_paths.content_utils.find_content',"symbols":['findContent','getLineNums','findContentAndEdit','findContent','get_line_content']},
    {"module":'abstract_paths.content_utils.find_content',"symbols":['getLineNums','findContentAndEdit','findContent','get_line_content']}
     ]
import_symbols_to_parent(import_modules, update_all=True)


