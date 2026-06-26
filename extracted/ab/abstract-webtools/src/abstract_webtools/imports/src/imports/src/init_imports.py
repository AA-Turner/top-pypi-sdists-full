from __future__ import annotations

# ── core / light deps: eager ────────────────────────────────────────────────
# stdlib + the two universally-used third-party libs (bs4, requests). All cheap
# and pip-installable on lean targets, so they stay eager.
import time, ipaddress, argparse, logging, re, tempfile, hashlib, subprocess, threading, importlib, socket
import requests, shutil, os, sys, unicodedata, urllib.request, json, glob, math, mimetypes
import ssl, certifi
import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup
from typing import *
from pathlib import Path
from datetime import datetime, timedelta
from urllib.parse import urljoin, quote, parse_qs, urlparse, urlencode, ParseResult
from collections import Counter
from urllib3.util import ssl_ as urllib3_ssl
from dataclasses import dataclass, field

# ── heavy / native / optional deps: LAZY ─────────────────────────────────────
# These were the bottleneck: the whole package shares this hub via
# `from ..imports import *`, so eagerly importing opencv / moviepy / pytesseract /
# pdf2image / pydub / speech_recognition / numpy / PIL / tiktoken / wordsegment
# here forced every leaf module (and `import abstract_webtools` itself) to require
# them — even though almost nothing references them. They are now lazy proxies:
# the names below import exactly as before, but the real module loads only on first
# attribute access / call, and need not be installed otherwise. See _lazy.py.
from abstract_webtools._lazy import LazyModule as _LazyModule, LazyAttr as _LazyAttr

cv2 = _LazyModule("cv2")
np = _LazyModule("numpy")
tiktoken = _LazyModule("tiktoken")
Image = _LazyModule("PIL.Image")
pytesseract = _LazyModule("pytesseract")
sr = _LazyModule("speech_recognition")
mp = _LazyModule("moviepy.editor")  # used qualified (mp.<Clip>); moviepy stays optional

AudioSegment = _LazyAttr("pydub", "AudioSegment")
detect_nonsilent = _LazyAttr("pydub.silence", "detect_nonsilent")
split_on_silence = _LazyAttr("pydub.silence", "split_on_silence")
convert_from_path = _LazyAttr("pdf2image", "convert_from_path")
load = _LazyAttr("wordsegment", "load")


def segment(text):
    """Lazy word-segmentation. Imports wordsegment and loads its corpus on first
    use — previously the corpus was loaded eagerly at package import (constants.py
    called ``load()`` at module level), which is needless cost for most callers."""
    import wordsegment
    if not getattr(wordsegment, "WORDS", None):
        wordsegment.load()
    return wordsegment.segment(text)
