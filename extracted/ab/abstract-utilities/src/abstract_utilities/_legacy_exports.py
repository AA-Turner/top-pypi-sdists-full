"""The pre-trim ``from abstract_utilities import *`` surface (<= 0.2.2.787).

Most packages in the abstract_* ecosystem were written against a star import
that also delivered the stdlib (``re``, ``shutil``, ``Path``, ``logging``,
``datetime``, ``dataclass``, the ``typing`` names, ...). The 0.2.2.788 import
trim stopped re-exporting them, so those packages still import cleanly and then
raise NameError on first use. This module restores that surface.

Stdlib names are exported eagerly (they are cheap and mostly loaded already).
Heavy third-party names (pandas, geopandas, PDF/OCR libs, requests, tiktoken,
...) stay out of the star import so the package remains dependency-free; they
resolve lazily as attributes (``abstract_utilities.pd``) via ``_lazy_attr``.
"""
from __future__ import annotations

import asyncio
import base64
import fnmatch
import functools
import glob
import hashlib
import importlib
import inspect
import json
import logging
import math
import os
import pathlib
import pkgutil
import platform
import posixpath
import queue
import re
import shlex
import shutil
import string
import subprocess
import sys
import tempfile
import textwrap
import threading
import time
import types
import uuid
from dataclasses import MISSING, asdict, dataclass, field, fields, is_dataclass
from datetime import date, datetime, timedelta
from difflib import SequenceMatcher
from functools import lru_cache, reduce
from logging.handlers import RotatingFileHandler
from pathlib import Path
from pprint import pprint
from types import MethodType, ModuleType
from typing import *  # noqa: F401,F403 — Any, Dict, List, Optional, ... (the 94 typing names)
from typing import TYPE_CHECKING, Text

tw = textwrap

# name -> (module, attribute or None for the module itself)
_LAZY = {
    "pd": ("pandas", None),
    "gpd": ("geopandas", None),
    "PyPDF2": ("PyPDF2", None),
    "pdfplumber": ("pdfplumber", None),
    "pytesseract": ("pytesseract", None),
    "convert_from_path": ("pdf2image", "convert_from_path"),
    "ezodf": ("ezodf", None),
    "pexpect": ("pexpect", None),
    "requests": ("requests", None),
    "tiktoken": ("tiktoken", None),
    "FileStorage": ("werkzeug.datastructures", "FileStorage"),
}


def _lazy_attr(name):
    """Resolve a heavy legacy name on first attribute access, or AttributeError."""
    if name not in _LAZY:
        raise AttributeError(name)
    module_name, attr = _LAZY[name]
    try:
        module = importlib.import_module(module_name)
    except ImportError as exc:
        raise AttributeError(
            f"abstract_utilities.{name} needs the optional package {module_name!r}: {exc}"
        ) from exc
    return getattr(module, attr) if attr else module
