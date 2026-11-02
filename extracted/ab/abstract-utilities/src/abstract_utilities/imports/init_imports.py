from __future__ import annotations
# ============================================================
# abstract_utilities/imports/imports.py
# Global imports hub.
#
# Core / cheap standard-library modules are imported eagerly.
# The "bulk" of the heavy, non-core third-party dependencies
# (pandas, geopandas, tiktoken, PyPDF2, pdfplumber, pdf2image,
#  pytesseract, pexpect, ezodf, requests, flask, werkzeug, ...)
# are bound to LAZY proxies so that importing abstract_utilities
# no longer pulls in those packages until they are actually used.
#
# The lazy helpers are defined inline (depending only on the std
# lib) so this module stays at the very bottom of the dependency
# graph and never triggers a circular import.
# ============================================================

# ---- core standard library (eager) -------------------------------------
import re, shlex, os, json, tempfile,decimal,uuid
import textwrap, math, hashlib, glob,dataclasses,unicodedata
import fnmatch, importlib, importlib.util, shutil, sys, time, threading, posixpath, types, logging
import uuid, string, subprocess, queue, functools, pkgutil, inspect
from typing import (
    Any,
    Callable,
    Literal,
    Optional,
    Protocol,
    Tuple,
    Union,
    Iterable,
    Iterator,
    Mapping,
    Dict,
    List,
    Set,
    get_args,
)
from datetime import (
    datetime,
    date,
    timezone
)
from pathlib import Path
from functools import reduce, lru_cache
from types import MethodType, ModuleType
from dataclasses import (
    dataclass,
    field,
)
from difflib import SequenceMatcher
from email.utils import format_datetime


