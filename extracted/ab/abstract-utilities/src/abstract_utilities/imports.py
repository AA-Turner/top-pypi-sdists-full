from __future__ import annotations
import re,pexpect,shlex,ezodf,tiktoken,geopandas as gpd,os,PyPDF2,json,tempfile,requests
import textwrap,pdfplumber,math,hashlib,pandas as pd,platform,textwrap as tw,glob,asyncio
import fnmatch,importlib,shutil,sys,time,threading,posixpath,importlib.util,types, logging
import subprocess,pytesseract,queue,logging,functools,pathlib,pkgutil,inspect
from typing import *
from datetime import timedelta,datetime
from flask import jsonify
from logging.handlers import RotatingFileHandler
from pathlib import Path
from functools import reduce,lru_cache
from types import MethodType,ModuleType
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from pdf2image import convert_from_path # only used for OCR fallback
from dataclasses import dataclass,field,asdict
from pprint import pprint
from dotenv import load_dotenv
from types import MethodType
from datetime import datetime, date
from decimal import Decimal
