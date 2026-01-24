# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations

from contrast_vendor import structlog as logging
from contrast.utils.locale import DEFAULT_ENCODING

logger = logging.getLogger("contrast")


def truncate(value, default="", length=256):
    """
    Truncate to `length` characters
    """
    if value is None:
        return default

    return value[:length]


def truncated_signature(value):
    """
    Get a log-friendly representation of a potentially long string. This function
    will truncate the string if necessary.

    First, we truncate the input to 60 characters - if this does happen, we'll also add
    `[TRUNCATED]` to the output. We then append the string's `id`. The string is
    converted to its most readable form using __repr__, which means that any newlines
    or invisible chars (like BEL) will be converted to something nice and readable.

    examples:
    'This is some string' (id=4443462824)
    'Here is a very long string that is longer th' [TRUNCATED] (id=4443294816)

    :param value: string whose truncated signature we want
    :return: string representation of the input value, truncated to 60 chars with
        its `id` appended as well. On any failure, return only the id.
    """
    try:
        append_truncate = ""

        if isinstance(value, bytearray):
            value = bytes(value)

        if len(value) > 60:
            value = value[:60]
            append_truncate = " [TRUNCATED]"

        value = ensure_string(value, errors="ignore")
        return f"{value!r}{append_truncate} (id={id(value)})"
    except Exception as e:
        logger.debug("Failed to truncate string: %s", e)
        return f"(id={id(value)})"


def index_of_any(value, search_chars):
    """
    Find the first index of a char in a string
    :param value: string to search
    :param search_chars: strings to search for
    :return: index if found else -1
    """

    for sc in search_chars:
        index = value.find(sc)

        if index != -1:
            return index

    return -1


def ends_with_any(value, strings):
    """
    Returns True if any of the strings are at the end of the value
    """
    return any(value.endswith(item) for item in strings)


def equals_ignore_case(this: str, that: str) -> bool:
    # PERF: this function is hot. Pre-checking str lengths is an optimization that
    # often prevents unnecessary (and slower) calls to lower().
    return len(this) == len(that) and this.lower() == that.lower()


def ensure_string(value: object, encoding=DEFAULT_ENCODING, errors="ignore") -> str:
    """
    Convert `value` of any type to a string, even if empty string.

    On failure given a custom encoding or using DEFAULT_ENCODING we
    return None and log a debug warning given the encoding that was used
    """
    if isinstance(value, str):
        return value
    if isinstance(value, bytes):
        try:
            return value.decode(encoding, errors)
        except Exception:
            logger.debug(
                "WARNING: Failed to decode value using the encoding %s", encoding
            )
            return ""

    # Check to see if value can be made a str
    try:
        return str(value)
    except Exception:
        pass
    return ""


def ensure_binary(s: str | bytes, encoding="utf-8", errors="ignore") -> bytes:
    return s if isinstance(s, bytes) else s.encode(encoding, errors)
