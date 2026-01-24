"""Module for methods for searching by field name."""
import re
from typing import List

from t_ocr.ocr_tools.address import get_valid_addresses
from t_ocr.ocr_tools.models import _Match, EmailMatch, DateMatch, TimeMatch, DateTimeMatch, AddressMatch, AmountMatch
from t_ocr.ocr_tools.validators import (
    get_valid_date_times,
    get_valid_dates,
    get_valid_times,
    get_valid_emails,
    get_valid_amounts,
)


def __get_nearest_match(matches: List[_Match], first_idx: int):
    return sorted(filter(lambda x: x.start >= first_idx, matches), key=lambda x: x.start)[0]


def __get_line_start_end_positions(string: str, symbol_index: int) -> (int, int):
    # find end index
    end_idx = string.find("\n", symbol_index)
    if end_idx == -1:
        last_idx = len(string) - 1
        if last_idx > symbol_index:
            end_idx = last_idx + 1

    # find start index
    start_idx = string.rfind("\n", None, symbol_index)

    start_idx = 0 if start_idx == -1 else start_idx + 1
    end_idx = 0 if end_idx == -1 else end_idx - 1
    return start_idx, end_idx


def __get_match_by_field_name(
    field_name: str, text: str, value_matches: List[_Match], in_same_line: bool = True, in_next_line: bool = True
):
    _field_name = field_name.rstrip(":-").strip()
    if not _field_name:
        raise ValueError("Field name is empty")

    field_pattern = re.compile(rf"(?:(?<=\W)|(?<=^)){_field_name}(?:(?=\W)|(?=$))", re.I)
    field_matches = list(field_pattern.finditer(text))

    if in_same_line:
        # Search values in one line
        for field_match in field_matches:
            try:
                nearest_match = __get_nearest_match(value_matches, first_idx=field_match.end())
            except IndexError:
                continue
            # Check delimiter between field name and value
            delimiter_text = text[field_match.end() : nearest_match.start]
            if re.fullmatch(r"[ \t]*[-:_]{0,2}[ \t]*", delimiter_text):
                return nearest_match

    if in_next_line:
        # Search value in next line
        for field_match in field_matches:
            next_line_idx = text.find("\n", field_match.end()) + 1
            if next_line_idx == 0:  # next line not exist
                continue
            try:
                nearest_match = __get_nearest_match(value_matches, first_idx=next_line_idx)
            except IndexError:
                continue
            # If value occupies the whole line or lines
            before_value = text[next_line_idx : nearest_match.start]
            after_value = text[nearest_match.end : text.find("\n", nearest_match.end)]
            if re.fullmatch(r"\W*", before_value + after_value):
                return nearest_match

            # If the position of the field and value is approximately the same in both lines
            lines_between_field_and_value = text[next_line_idx : nearest_match.start].split("\n")[:-1]
            if len(lines_between_field_and_value) and not all(
                re.fullmatch(r"\W*", line) for line in lines_between_field_and_value
            ):
                # If lines between field name and value contain any text
                continue

            start_field_line, _ = __get_line_start_end_positions(text, field_match.start())
            start_value_line, _ = __get_line_start_end_positions(text, nearest_match.start)
            if abs((field_match.start() - start_field_line) - (nearest_match.start - start_value_line)) < 10:
                return nearest_match
    raise ValueError(f"Valid value for field '{field_name}' not found")


def get_email_by_field_name(field_name: str, text: str, in_same_line: bool = True, in_next_line: bool = True):
    """
    Search for field value and check for matching value with email pattern.

    Args:
        field_name (str): field name for search
        text (str): text that contains the field name and value
        in_same_line (bool): True if you need to look for a value in the same line as the field name. Defaults to True.
        in_next_line (bool): True if you need to look for a value in the next line as the field name. Defaults to True.

    Returns:
        EmailMatch: match of suitable value
    """
    value_matches: List[EmailMatch] = get_valid_emails(text)
    try:
        return __get_match_by_field_name(field_name, text, value_matches, in_same_line, in_next_line)
    except ValueError:
        raise ValueError(f"Valid email for field '{field_name}' not found")


def get_date_by_field_name(field_name: str, text: str, in_same_line: bool = True, in_next_line: bool = True):
    """
    Search for field value and check for matching value with date pattern.

    Args:
        field_name (str): field name for search
        text (str): text that contains the field name and value
        in_same_line (bool): True if you need to look for a value in the same line as the field name. Defaults to True.
        in_next_line (bool): True if you need to look for a value in the next line as the field name. Defaults to True.

    Returns:
        DateMatch: match of suitable value
    """
    value_matches: List[DateMatch] = get_valid_dates(text)
    try:
        return __get_match_by_field_name(field_name, text, value_matches, in_same_line, in_next_line)
    except ValueError:
        raise ValueError(f"Valid date for field '{field_name}' not found")


def get_time_by_field_name(field_name: str, text: str, in_same_line: bool = True, in_next_line: bool = True):
    """
    Search for field value and check for matching value with time pattern.

    Args:
        field_name (str): field name for search
        text (str): text that contains the field name and value
        in_same_line (bool): True if you need to look for a value in the same line as the field name. Defaults to True.
        in_next_line (bool): True if you need to look for a value in the next line as the field name. Defaults to True.

    Returns:
        TimeMatch: match of suitable value
    """
    value_matches: List[TimeMatch] = get_valid_times(text)
    try:
        return __get_match_by_field_name(field_name, text, value_matches, in_same_line, in_next_line)
    except ValueError:
        raise ValueError(f"Valid time for field '{field_name}' not found")


def get_date_time_by_field_name(field_name: str, text: str, in_same_line: bool = True, in_next_line: bool = True):
    """
    Search for field value and check for matching value with date time pattern.

    Args:
        field_name (str): field name for search
        text (str): text that contains the field name and value
        in_same_line (bool): True if you need to look for a value in the same line as the field name. Defaults to True.
        in_next_line (bool): True if you need to look for a value in the next line as the field name. Defaults to True.

    Returns:
        DateTimeMatch: match of suitable value
    """
    value_matches: List[DateTimeMatch] = get_valid_date_times(text)
    try:
        return __get_match_by_field_name(field_name, text, value_matches, in_same_line, in_next_line)
    except ValueError:
        raise ValueError(f"Valid date time for field '{field_name}' not found")


def get_address_by_field_name(field_name: str, text: str, in_same_line: bool = True, in_next_line: bool = True):
    """
    Search for field value and check for matching value with address pattern.

    Args:
        field_name (str): field name for search
        text (str): text that contains the field name and value
        in_same_line (bool): True if you need to look for a value in the same line as the field name. Defaults to True.
        in_next_line (bool): True if you need to look for a value in the next line as the field name. Defaults to True.

    Returns:
        AddressMatch: match of suitable value
    """
    value_matches: List[AddressMatch] = get_valid_addresses(text)
    try:
        return __get_match_by_field_name(field_name, text, value_matches, in_same_line, in_next_line)
    except ValueError:
        raise ValueError(f"Valid address for field '{field_name}' not found")


def get_amount_by_field_name(field_name: str, text: str, in_same_line: bool = True, in_next_line: bool = True):
    """
    Search for field value and check for matching value with amount pattern.

    Args:
        field_name (str): field name for search
        text (str): text that contains the field name and value
        in_same_line (bool): True if you need to look for a value in the same line as the field name. Defaults to True.
        in_next_line (bool): True if you need to look for a value in the next line as the field name. Defaults to True.

    Returns:
        AmountMatch: match of suitable value
    """
    value_matches: List[AmountMatch] = get_valid_amounts(text)
    try:
        return __get_match_by_field_name(field_name, text, value_matches, in_same_line, in_next_line)
    except ValueError:
        raise ValueError(f"Valid address for field '{field_name}' not found")
