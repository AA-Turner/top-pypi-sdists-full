"""Validators module."""
import re
from datetime import datetime
from re import Pattern
from typing import List, Tuple

import datefinder

from email_validator import validate_email, EmailNotValidError

from t_ocr.ocr_tools.models import DateMatch, TimeMatch, DateTimeMatch, EmailMatch, AmountMatch
from t_ocr.ocr_tools.patterns import DATE_PATTERN, TIME_PATTERN, DATE_TIME_PATTERN, EMAIL_PATTERN
from t_ocr.ocr_tools.patterns.patterns import AMOUNT_PATTERN


def _get_valid_date_times_by_pattern(text: str, pattern: Pattern) -> List[Tuple[str, datetime, int, int]]:
    matches = []
    d_f = datefinder.DateFinder()
    for match in pattern.finditer(text):
        match_str = match.group(0)
        for date_string, indices, captures in d_f.extract_date_strings(match_str):
            as_dt = d_f.parse_date_string(date_string, captures)
            if as_dt is not None:
                matches.append((match_str, as_dt, match.start(), match.end()))
            break
    return matches


def get_valid_dates(text: str) -> List[DateMatch]:
    """
    Search for all valid dates in the text.

    Returns their positions in the text, the original string, and a date object.

    Args:
        text (str): text to search

    Returns:
        List[DateMatch]: List of DateMatch objects
    """
    matches = _get_valid_date_times_by_pattern(text, DATE_PATTERN)
    return [DateMatch(match[0], match[1], match[2], match[3]) for match in matches]


def is_valid_date(date_string: str) -> bool:
    """
    Check if a string matches a valid date.

    Args:
        date_string (str): string to validate

    Returns:
        bool: True if valid else False
    """
    date_string = date_string.strip()
    if DATE_PATTERN.fullmatch(date_string):
        if len(get_valid_dates(date_string)) == 1:
            return True
    return False


def get_valid_times(text: str) -> List[TimeMatch]:
    """
    Search for all valid times in the text.

    Returns their positions in the text, the original string, and a time object.

    Args:
        text (str): text to search

    Returns:
        List[TimeMatch]: List of TimeMatch objects
    """
    matches = _get_valid_date_times_by_pattern(text, TIME_PATTERN)
    return [TimeMatch(match[0], match[1], match[2], match[3]) for match in matches]


def is_valid_time(time_string: str) -> bool:
    """
    Check if a string matches a valid time.

    Args:
        time_string (str): string to validate

    Returns:
        bool: True if valid else False
    """
    time_string = time_string.strip()
    if TIME_PATTERN.fullmatch(time_string):
        if len(get_valid_times(time_string)) == 1:
            return True
    return False


def get_valid_date_times(text: str) -> List[DateTimeMatch]:
    """
    Search for all valid date_times in the text.

    Returns their positions in the text, the original string, and a date_time object.

    Args:
        text (str): text to search

    Returns:
        List[DateTimeMatch]: List of DateTimeMatch objects
    """
    matches = _get_valid_date_times_by_pattern(text, DATE_TIME_PATTERN)
    return [DateTimeMatch(match[0], match[1], match[2], match[3]) for match in matches]


def is_valid_date_time(datetime_string: str) -> bool:
    """
    Check if a string matches a valid date_time.

    Args:
        datetime_string (str): string to validate

    Returns:
        bool: True if valid else False
    """
    datetime_string = datetime_string.strip()
    if DATE_TIME_PATTERN.fullmatch(datetime_string):
        if len(get_valid_date_times(datetime_string)) == 1:
            return True
    return False


def get_valid_emails(text: str) -> List[EmailMatch]:
    """
    Search for all valid emails in the text.

    Returns their positions in the text, the original string.

    Args:
        text (str): text to search

    Returns:
        List[EmailMatch]: List of EmailMatch objects
    """
    matches = []
    for match in EMAIL_PATTERN.finditer(text):
        try:
            validate_email(match.group(0), check_deliverability=False)
        except EmailNotValidError:
            continue
        matches.append(EmailMatch(match.group(0), match.start(), match.end()))
    return matches


def is_valid_email(email_string: str) -> bool:
    """
    Check if a string matches a valid email.

    Args:
        email_string (str): string to validate

    Returns:
        bool: True if valid else False
    """
    email_string = email_string.strip()
    if EMAIL_PATTERN.fullmatch(email_string):
        if len(get_valid_emails(email_string)) == 1:
            return True
    return False


def __text_currency_to_float(amount_string: str) -> float or int:
    amount_string = amount_string.strip()
    decimal_sep_part_match = re.search(r"[,.]\d{1,2}$", amount_string)
    if decimal_sep_part_match:
        sep_idx = decimal_sep_part_match.start()
        amount_string = amount_string[:sep_idx] + "*" + amount_string[sep_idx + 1 :]
        amount_string = amount_string.replace(",", "").replace(".", "")
        amount_string = amount_string.replace("*", ".")
        return float(amount_string)
    else:
        amount_string = amount_string.replace(",", "").replace(".", "")
        return int(amount_string)


def get_valid_amounts(text: str) -> List[AmountMatch]:
    """
    Search for all valid amounts in the text.

    Returns their positions in the text, the original string and float or int object.

    Args:
        text (str): text to search

    Returns:
        List[AmountMatch]: List of AmountMatch objects
    """
    matches = []
    for match in AMOUNT_PATTERN.finditer(text):
        try:
            number = __text_currency_to_float(match.group(0))
        except ValueError:
            continue
        matches.append(AmountMatch(match.group(0), number, match.start(), match.end()))
    return matches


def is_valid_amount(amount_string: str) -> bool:
    """
    Check if a string matches a valid amount.

    Args:
        amount_string (str): string to validate

    Returns:
        bool: True if valid else False
    """
    amount_string = amount_string.strip()
    if AMOUNT_PATTERN.fullmatch(amount_string):
        if len(get_valid_amounts(amount_string)) == 1:
            return True
    return False
