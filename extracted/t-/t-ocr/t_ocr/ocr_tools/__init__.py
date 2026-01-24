"""Package for OCR tools."""

__author__ = """Thoughtful"""
__email__ = "support@thoughtfulautomation.com"
__version__ = "1.5.6"

from t_ocr.ocr_tools.address import get_valid_addresses, is_valid_address
from t_ocr.ocr_tools.fields_search import (
    get_email_by_field_name,
    get_date_by_field_name,
    get_time_by_field_name,
    get_date_time_by_field_name,
    get_address_by_field_name,
    get_amount_by_field_name,
)
from t_ocr.ocr_tools.ocr_tools import (
    does_strings_match_by_fuzzy,
    does_text_contains_string_by_fuzzy,
    find_string_in_text_by_fuzzy,
    does_strings_match_by_ocr_search,
    does_text_contains_string_by_ocr_search,
    find_string_in_text_by_ocr_search,
)
from t_ocr.ocr_tools.validators import (
    get_valid_dates,
    is_valid_date,
    get_valid_times,
    is_valid_time,
    get_valid_date_times,
    is_valid_date_time,
    get_valid_emails,
    is_valid_email,
    get_valid_amounts,
    is_valid_amount,
)

__all__ = [
    "does_strings_match_by_fuzzy",
    "does_text_contains_string_by_fuzzy",
    "find_string_in_text_by_fuzzy",
    "does_strings_match_by_ocr_search",
    "does_text_contains_string_by_ocr_search",
    "find_string_in_text_by_ocr_search",
    "get_valid_dates",
    "is_valid_date",
    "get_valid_times",
    "is_valid_time",
    "get_valid_date_times",
    "is_valid_date_time",
    "get_valid_emails",
    "is_valid_email",
    "get_valid_amounts",
    "is_valid_amount",
    "get_valid_addresses",
    "is_valid_address",
    "get_email_by_field_name",
    "get_date_by_field_name",
    "get_time_by_field_name",
    "get_date_time_by_field_name",
    "get_address_by_field_name",
    "get_amount_by_field_name",
    "models",
    "patterns",
]
