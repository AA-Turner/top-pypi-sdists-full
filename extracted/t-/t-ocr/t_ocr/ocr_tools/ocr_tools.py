"""This module contains OCR tools (in dev)."""
import difflib
import re
from typing import List

__OCR_REPLACEMENTS = {
    "0": ["8", "9", "o", "O", "D"],
    "1": ["4", "7", "l", "I", "|", "L"],
    "2": ["z", "Z"],
    "8": ["s", "S", "@", "&", "0", "5"],
    "6": ["b"],
    "9": ["g", "q"],
    "o": ["u"],
    "r": ["k"],
    "C": ["G"],
    "O": ["U"],
    "E": ["B"],
    "R": ["A", "P"],
}


def does_strings_match_by_fuzzy(string_1: str, string_2: str, percentage: float) -> bool:
    """First string must match second string for given percentage."""
    if percentage < 0 or percentage > 1:
        raise ValueError("Argument 'percentage' must be a number between 0 and 1")
    return difflib.SequenceMatcher(None, string_1, string_2).ratio() >= percentage


def does_text_contains_string_by_fuzzy(string: str, text: str, percentage: float) -> bool:
    """Text must contains string with matching for given percentage."""
    if percentage < 0 or percentage > 1:
        raise ValueError("Argument 'percentage' must be a number between 0 and 1")
    try:
        find_string_in_text_by_fuzzy(string, text, percentage)
        return True
    except ValueError:
        return False


def find_string_in_text_by_fuzzy(string: str, text: str, percentage: float) -> int:
    """Find position where text contains string with matching for given percentage."""
    all_same_len_strings: List = []

    for index in range(len(text) - len(string) + 1):
        all_same_len_strings.append(text[index : index + len(string)])
    try:
        best_match = str(difflib.get_close_matches(string, all_same_len_strings, n=1, cutoff=percentage)[0])
    except IndexError:
        raise ValueError(f"Substring '{string}' not found in text with possibility score {percentage}")

    return text.index(best_match)


def __convert_ocr_string(string: str) -> str:
    for replacement, chars in __OCR_REPLACEMENTS.items():
        for char in chars:
            string = string.replace(char, replacement)
    return re.sub(r"[,:.]", "", string).strip()


def does_strings_match_by_ocr_search(string_1: str, string_2: str) -> bool:
    """
    First string must match the second string.

    considering that some characters may not be read correctly with the OCR.
    """
    return __convert_ocr_string(string_1) == __convert_ocr_string(string_2)


def does_text_contains_string_by_ocr_search(string: str, text: str) -> bool:
    """
    Text must contains string with matching.

    Considering that some characters may not be read correctly with the OCR.
    """
    try:
        find_string_in_text_by_ocr_search(string, text)
        return True
    except ValueError:
        return False


def find_string_in_text_by_ocr_search(string: str, text: str) -> int:
    """
    Find position where text contains string with matching.

    Considering that some characters may not be read correctly with the OCR.
    """
    try:
        return __convert_ocr_string(text).index(__convert_ocr_string(string))
    except ValueError:
        raise ValueError(f"Substring '{string}' not found in text")
