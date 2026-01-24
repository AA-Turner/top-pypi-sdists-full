from __future__ import annotations
from bs4 import BeautifulSoup
from wordsegment import load, segment

import time, argparse, logging, re, tempfile, hashlib, cv2, subprocess, threading, importlib, socket, tiktoken
import pytesseract, requests, shutil, os, sys, unicodedata, urllib.request, json, glob, math, mimetypes 

from typing import *
from pathlib import Path
from datetime import datetime, timedelta 
from urllib.parse import urljoin,quote, parse_qs, urlparse
from collections import Counter

from PIL import Image
import numpy as np

from moviepy.editor import VideoFileClip
import moviepy.editor as mp

import speech_recognition as sr
from pydub.silence import detect_nonsilent,split_on_silence
from pydub import AudioSegment

from urllib3.util import ssl_ as urllib3_ssl
import ssl, certifi

from urllib.parse import urlparse, urljoin

import xml.etree.ElementTree as ET

from pdf2image import convert_from_path

