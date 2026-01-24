"""Package for OCR patterns."""

__author__ = """Thoughtful"""
__email__ = "support@thoughtfulautomation.com"
__version__ = "1.5.6"

from t_ocr.ocr_tools.patterns.patterns import (
    EMAIL_PATTERN,
    ADDRESS_PATTERN,
    AMOUNT_PATTERN,
    DATE_PATTERN,
    TIME_PATTERN,
    DATE_TIME_PATTERN,
)

__all__ = [
    "DATE_PATTERN",
    "TIME_PATTERN",
    "DATE_TIME_PATTERN",
    "EMAIL_PATTERN",
    "ADDRESS_PATTERN",
    "AMOUNT_PATTERN",
]
