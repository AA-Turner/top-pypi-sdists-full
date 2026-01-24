"""Top-level package for T - OCR."""

__author__ = """Thoughtful"""
__email__ = "support@thoughtfulautomation.com"
__version__ = "1.5.6"

from t_ocr.textract import Textract
from t_ocr.free_ocr import FreeOCR, PSM

__all__ = [
    "Textract",
    "FreeOCR",
    "PSM",
]
