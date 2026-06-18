from ...imports import *
# file_reader.py
from ..file_filters import *
from ....read_write_utils import read_from_file
from ....log_utils import get_logFile
import os,tempfile,shutil,logging,fnmatch
from typing import Union
# Heavy/non-core third-party deps come in as lazy proxies from the root hub so
# importing this package does not pull pandas/geopandas/pdfplumber/pdf2image/
# pytesseract/ezodf/werkzeug until they are actually used.
from ....imports import (
    pd,
    gpd,
    ezodf,
    secure_filename,
    FileStorage,
    pdfplumber,
    convert_from_path,   # only used for OCR fallback
    pytesseract,
)
from datetime import datetime
from typing import Dict, Union, List
from pathlib import Path
