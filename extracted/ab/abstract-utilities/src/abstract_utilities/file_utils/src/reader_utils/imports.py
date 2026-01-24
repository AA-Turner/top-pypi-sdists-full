from ...imports import *
# file_reader.py
from ..file_filters import *
from ....read_write_utils import read_from_file
from ....log_utils import get_logFile
import os,tempfile,shutil,logging,ezodf,fnmatch
from typing import Union
import pandas as pd
import geopandas as gpd
from datetime import datetime
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from datetime import datetime
from typing import Dict, Union, List
import pdfplumber
from pdf2image import convert_from_path   # only used for OCR fallback
import pytesseract
from pathlib import Path
