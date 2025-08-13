from __future__ import annotations

import datetime as dt
from enum import Enum
from typing import Any, Literal, Mapping, TypeVar, Union

import pyarrow as pa

from chalk.features._encoding.pyarrow import rich_to_pyarrow
from chalk.features.underscore import Underscore, UnderscoreCast, UnderscoreFunction
from chalk.functions.holidays import DayOfWeek
from chalk.functions.http import http_delete, http_get, http_post, http_put, http_request
from chalk.functions.proto import proto_deserialize, proto_serialize
from chalk.utils.duration import parse_chalk_duration

########################################################################################################################
# String Functions                                                                                                     #
########################################################################################################################


_SUPPORTED_UNDERSCORE_STRING_TO_BYTES = {
    "base64": "string_to_bytes_base64",
    "hex": "string_to_bytes_hex",
    "utf-8": "string_to_bytes_utf8",
}

_SUPPORTED_UNDERSCORE_BYTES_TO_STRING = {
    "base64": "bytes_to_string_base64",
    "hex": "bytes_to_string_hex",
    "utf-8": "bytes_to_string_utf8",
}


def replace(expr: Underscore | Any, old: str, new: str):
    """Replace all occurrences of a substring in a string with another substring.

    Parameters
    ----------
    expr
        The string to replace the substring in.
    old
        The substring to replace.
    new
        The substring to replace the old substring with.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    name: str
    ...    normalized_name: str = F.replace(_.name, " ", "_")
    """
    return UnderscoreFunction("replace", expr, old, new)


def like(expr: Underscore | Any, pattern: str):
    """
    Evaluates if the string matches the pattern.

    Patterns can contain regular characters as well as wildcards.
    Wildcard characters can be escaped using the single character
    specified for the escape parameter. Matching is case-sensitive.

    Note: The wildcard `%` represents 0, 1 or multiple characters
    and the wildcard `_` represents exactly one character.

    For example, the pattern `John%` will match any string that starts
    with `John`, such as `John`, `JohnDoe`, `JohnSmith`, etc.

    The pattern `John_` will match any string that starts with `John`
    and is followed by exactly one character, such as `JohnD`, `JohnS`, etc.
    but not `John`, `JohnDoe`, `JohnSmith`, etc.

    Parameters
    ----------
    expr
        The string to check against the pattern.
    pattern
        The pattern to check the string against.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    name: str
    ...    is_john: bool = F.like(_.name, "John%")
    """
    return UnderscoreFunction("like", expr, pattern)


def regexp_replace(expr: Underscore | Any, pattern: str, replacement: str | None = None):
    """
    Replaces every instance of `expr` matched by the regular expression pattern in
    `pattern` with `replacement`. Capturing groups can be referenced in replacement
    using `$1`, `$2`, etc. for a numbered group or `${name}` for a named group.
    A dollar sign (`$`) may be included in the replacement by escaping it with a
    backslash. If a backslash is followed by any character other than
    a digit or another backslash in the replacement, the preceding backslash
    will be ignored.

    If no replacement is provided, the matched pattern will be removed from the string.

    Parameters
    ----------
    expr
        The string to replace the pattern in.
    pattern
        The regular expression pattern to replace.
    replacement
        The string to replace the pattern with.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    name: str
    ...    normalize_regex: str
    ...    normalized_name: str = F.regexp_replace(_.name, _.normalize_regex, " ")
    """
    if replacement is not None:
        return UnderscoreFunction("regexp_replace", expr, pattern, replacement)
    return UnderscoreFunction("regexp_replace", expr, pattern)


def regexp_like(expr: Underscore | Any, pattern: Underscore | str | Any):
    """
    Evaluates the regular expression pattern and determines if it is contained within string.

    This function is similar to the `like` function, except that the pattern only needs to be
    contained within string, rather than needing to match all the string.
    In other words, this performs a contains operation rather than a match operation.
    You can match the entire string by anchoring the pattern using `^` and `$`.

    Parameters
    ----------
    expr
        The string to check against the pattern.
    pattern
        The regular expression pattern to check the string against.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    name: str
    ...    is_john: bool = F.regexp_like(_.name, "^John.*$")
    """
    return UnderscoreFunction("regexp_like", expr, pattern)


def regexp_extract(expr: Underscore | Any, pattern: str, group: int):
    """
    Finds the first occurrence of the regular expression pattern in the string and
    returns the capturing group number group.

    Parameters
    ----------
    expr
        The string to check against the pattern.
    pattern
        The regular expression pattern to check the string against.
    group
        The number of the capturing group to extract from the string.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class HiddenNumber:
    ...    id: str
    ...    hidden_number: str = "O0OOO",
    ...    number: str = F.regexp_extract(_.time,  r"([0-9]+)", 1)
    """
    return UnderscoreFunction("regexp_extract", expr, pattern, group)


def regexp_extract_all(expr: Underscore | Any, pattern: str, group: int):
    """
    Finds all occurrences of the regular expression pattern in string and
    returns the capturing group number group.

    Parameters
    ----------
    expr
        The string to check against the pattern.
    pattern
        The regular expression pattern to check the string against.
    group
        The number of the capturing group to extract from the string.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Time:
    ...    id: str
    ...    time: str = "1y 342d 20h 60m 6s",
    ...    processed_time: list[str] = F.regexp_extract_all(_.time, "([0-9]+)([ydhms])", 2)
    """
    return UnderscoreFunction("regexp_extract_all", expr, pattern, group)


def trim(expr: Underscore | Any):
    """
    Remove leading and trailing whitespace from a string.

    Parameters
    ----------
    expr
        The string to trim.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    name: str
    ...    trimmed_name: str = F.trim(_.name)
    """
    return UnderscoreFunction("trim", expr)


def ltrim(expr: Underscore | Any):
    """
    Remove leading whitespace from a string.

    Parameters
    ----------
    expr
        The string to left trim.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    name: str
    ...    left_trimmed_name: str = F.ltrim(_.name)
    """
    return UnderscoreFunction("ltrim", expr)


def rtrim(expr: Underscore | Any):
    """
    Remove trailing whitespace from a string.

    Parameters
    ----------
    expr
        The string to right trim.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    name: str
    ...    right_trimmed_name: str = F.rtrim(_.name)
    """
    return UnderscoreFunction("rtrim", expr)


def starts_with(expr: Underscore | Any, prefix: Underscore | Any):
    """
    Evaluates if the string starts with the specified prefix.

    Parameters
    ----------
    expr
        The string to check against the prefix.
    prefix
        The prefix or feature to check if the string starts with.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Transaction:
    ...    id: str
    ...    category: str
    ...    is_food: bool = F.starts_with(_.name, "Food")
    """
    return UnderscoreFunction("starts_with", expr, prefix)


def ends_with(expr: Underscore | Any, suffix: Underscore | Any):
    """
    Evaluates if the string ends with the specified suffix.

    Parameters
    ----------
    expr
        The string to check against the suffix.
    suffix
        The suffix or feature to check if the string ends with.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Transaction:
    ...    id: str
    ...    category: str
    ...    is_food: bool = F.ends_with(_.name, "Food")
    """
    return UnderscoreFunction("ends_with", expr, suffix)


def substr(expr: Underscore | Any, start: int, length: int | None = None):
    """
    Extract a substring from a string.

    Parameters
    ----------
    expr
        The string to extract the substring from.
    start
        The starting index of the substring (0-indexed).
    length
        The length of the substring. If None, the substring will extend to the end of the string.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Transaction:
    ...    id: str
    ...    category: str
    ...    cat_first_three: str = F.substr(_.category, 0, 3)
    """
    if length is None:
        return UnderscoreFunction("substr", expr, start + 1)
    return UnderscoreFunction("substr", expr, start + 1, length)


def reverse(expr: Underscore | Any):
    """
    Reverse the order of a string.

    Parameters
    ----------
    expr
        The string to reverse.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    name: str
    ...    reversed_name: str = F.reverse(_.name)
    """
    return UnderscoreFunction("reverse", expr)


def length(expr: Underscore | Any):
    """
    Compute the length of a string.

    Parameters
    ----------
    expr
        The string to compute the length of.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Transaction
    ...    id: str
    ...    category: str
    ...    category_length: int = F.length(_.category)
    """
    return UnderscoreFunction("length", expr)


def levenshtein_distance(a: Underscore | Any, b: Underscore | Any):
    """
    Compute the Levenshtein distance between two strings.

    Parameters
    ----------
    a
        The first string.
    b
        The second string.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    name: str
    ...    email: str
    ...    name_email_sim: int = F.levenshtein_distance(_.name, _.email)
    """
    return UnderscoreFunction("levenshtein_distance", a, b)


def jaro_winkler_distance(a: Underscore | Any, b: Underscore | Any, prefix_weight: float = 0.1):
    """
    Compute the Jaro-Winkler distance between two strings.

    Parameters
    ----------
    a
        The first string.
    b
        The second string.
    prefix_weight
        The prefix weight parameter for the distance calculation. Should be between `0.0` and `0.25`.
        `0.1` by default.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    name: str
    ...    email: str
    ...    name_email_sim: int = F.jaro_winkler_distance(_.name, _.email)
    """
    return UnderscoreFunction("jaro_winkler_distance", a, b, prefix_weight)


def jaccard_similarity(a: Underscore | Any, b: Underscore | Any):
    """
    Compute the Jaccard similarity, character by character, between two strings.
    Returns a float in the range `[0, 1]`.

    Parameters
    ----------
    a
        The first string.
    b
        The second string.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    name: str
    ...    email: str
    ...    name_email_sim: int = F.jaccard_similarity(_.name, _.email)
    """
    return UnderscoreFunction("jaccard_similarity", a, b)


def partial_ratio(a: Underscore | Any, b: Underscore | Any):
    """
    Compute the Fuzzy Wuzzy partial ratio between two strings. Returns a value in the range `[0, 100]`.

    Parameters
    ----------
    a
        The first string.
    b
        The second string.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    name: str
    ...    email: str
    ...    name_email_sim: int = F.partial_ratio(_.name, _.email)
    """
    return UnderscoreFunction("partial_ratio", a, b)


def token_set_ratio(a: Underscore | Any, b: Underscore | Any):
    """
    Compute the Fuzzy Wuzzy token set ratio between two strings. Returns a value in the range `[0, 100]`.

    Parameters
    ----------
    a
        The first string.
    b
        The second string.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    name: str
    ...    email: str
    ...    name_email_sim: int = F.token_set_ratio(_.name, _.email)
    """
    return UnderscoreFunction("token_set_ratio", a, b)


def token_sort_ratio(a: Underscore | Any, b: Underscore | Any):
    """
    Compute the Fuzzy Wuzzy token sort ratio between two strings. Returns a value in the range `[0, 100]`.

    Parameters
    ----------
    a
        The first string.
    b
        The second string.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    name: str
    ...    email: str
    ...    name_email_sim: int = F.token_sort_ratio(_.name, _.email)
    """
    return UnderscoreFunction("token_sort_ratio", a, b)


def unidecode_normalize(a: Underscore | Any):
    """
    Normalizes an input utf8 string using NFKD normalization. Returns a normalized utf8 string.

    Parameters
    ----------
    a
        utf8 string.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    input_string: str
    ...    normalized_string: str = F.unidecode_normalize(_.input_string)
    """
    return UnderscoreFunction("unidecode_normalize", a)


def unidecode_to_ascii(a: Underscore | Any):
    """
    Normalizes and transliterates an input utf8 string to ASCII. Returns a normalized string with only ASCII characters.

    Parameters
    ----------
    a
        utf8 string.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    input_string: str
    ...    normalized_ascii_string: str = F.unidecode_to_ascii(_.input_string)
    """
    return UnderscoreFunction("unidecode_to_ascii", a)


def sequence_matcher_ratio(a: Underscore | Any, b: Underscore | Any):
    """
    Measure the similarity of two strings as by Python `difflib`.
    Equivalent to `difflib.SequenceMatcher(None, a, b).ratio()`.
    Returns a value in the range [0, 1].

    Parameters
    ----------
    a
        The first string.
    b
        The second string.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    name: str
    ...    email: str
    ...    name_email_sim: int = F.sequence_matcher_ratio(_.name, _.email)
    """
    return UnderscoreFunction("sequence_matcher_ratio", a, b)


def lower(expr: Underscore | Any):
    """
    Convert a string to lowercase.

    Parameters
    ----------
    expr
        The string to convert to lowercase.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    name: str
    ...    normalized: str = F.trim(F.lower(_.name))
    """
    return UnderscoreFunction("lower", expr)


def upper(expr: Underscore | Any):
    """
    Convert a string to uppercase.

    Parameters
    ----------
    expr
        The string to convert to uppercase.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Transaction:
    ...    id: str
    ...    category: str
    ...    normalized: str = F.trim(F.upper(_.category))
    """
    return UnderscoreFunction("upper", expr)


def string_to_bytes(expr: Any, encoding: Literal["utf-8", "hex", "base64"]):
    """
    Convert a string to bytes using the specified encoding.

    Parameters
    ----------
    expr
        An underscore expression for a feature to a
        string feature that should be converted to bytes.
    encoding
        The encoding to use when converting the string to bytes.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    name: str
    ...    hashed_name: bytes = F.string_to_bytes(_.name, encoding="utf-8")
    """
    return UnderscoreFunction(_SUPPORTED_UNDERSCORE_STRING_TO_BYTES[encoding], expr)


def bytes_to_string(expr: Any, encoding: Literal["utf-8", "hex", "base64"]):
    """
    Convert bytes to a string using the specified encoding.

    Parameters
    ----------
    expr
        A bytes feature to convert to a string.
    encoding
        The encoding to use when converting the bytes to a string.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    name: str
    ...    hashed_name: bytes
    ...    decoded_name: str = F.bytes_to_string(_.hashed_name, encoding="utf-8")
    """
    return UnderscoreFunction(_SUPPORTED_UNDERSCORE_BYTES_TO_STRING[encoding], expr)


def from_big_endian_64(expr: Any):
    """
    Convert a 64-bit big-endian bytes value to an integer.

    Parameters
    ----------
    expr
        A bytes feature to convert.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class ByteData:
    ...    id: str
    ...    raw_bytes: bytes
    ...    value: int = F.from_big_endian_64(_.raw_bytes)
    """
    return UnderscoreFunction("from_big_endian_64", expr)


def from_big_endian_32(expr: Any):
    """
    Convert a 32-bit big-endian bytes value to an integer.

    Parameters
    ----------
    expr
        A bytes feature to convert.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class ByteData:
    ...    id: str
    ...    raw_bytes: bytes
    ...    value: int = F.from_big_endian_32(_.raw_bytes)
    """
    return UnderscoreFunction("from_big_endian_32", expr)


def split(expr: Any, delimiter: str, maxsplit: int | None = None):
    """
    Splits string by delimiter, returning a list of strings.
    If maxsplit is set, at most maxsplit splits are performed.

    Parameters
    ----------
    expr:
        The string to split.
    delimiter:
        The delimiter to split the string on.
    maxsplit:
        The maximum number of times to split the string. Once the string has been split "maxsplit" times (starting from the left), the rest of the string is left untouched.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class CSVRow:
    ...    id: str
    ...    data: str
    ...    data: list[str] = F.split(_.data, delimiter=",")
    """
    if maxsplit is None:
        return UnderscoreFunction("split", expr, delimiter)

    return UnderscoreFunction("split", expr, delimiter, maxsplit + 1)


def split_part(expr: Any, delimiter: str, index: int):
    """
    Splits string by delimiter and returns the index'th element (0-indexed).
    If the index is larger than the number of fields, returns None.

    Parameters
    ----------
    expr:
        The string to split.
    delimiter:
        The delimiter to split the string on.
    index:
        The index of the the split to return.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class CSVRow:
    ...    id: str
    ...    data: str
    ...    first_element: str = F.split_part(_.data, delimiter=",", index=0)
    """
    return UnderscoreFunction("split_part", expr, delimiter, index + 1)


def strpos(expr: Any, substring: Any):
    """
    Returns the position of the first occurrence of substring in string.
    Returns -1 if substring is not found.

    Parameters
    ----------
    expr:
        The string to search for the substring in.
    substring:
        The substring to search for in the string.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Email:
    ...   email: str
    ...   username_length: int = F.strpos(_.email, "@")
    """
    return UnderscoreFunction("strpos", expr, substring) - 1


def strrpos(expr: Any, substring: Any):
    """
    Returns the position of the last occurrence of substring in string.
    Returns -1 if substring is not found.

    Parameters
    ----------
    expr:
        The string to search for the substring in.
    substring:
        The substring to search for in the string.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Email:
    ...   email: str
    ...   domain_length: int = F.strrpos(_.email, "@")
    """
    return UnderscoreFunction("strrpos", expr, substring) - 1


def chr(code: Underscore | Any):
    """
    Convert Unicode code point to character.

    Parameters
    ----------
    code
        The Unicode code point as integer.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Unicode:
    ...    id: str
    ...    code_point: int
    ...    character: str = F.chr(_.code_point)
    """
    return UnderscoreFunction("chr", code)


def lpad(string: Underscore | Any, size: Underscore | Any, padstring: Underscore | Any):
    """
    Left-pad string to specified length with pad string.

    Parameters
    ----------
    string
        The string to pad.
    size
        The target length.
    padstring
        The string to pad with.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class AccountID:
    ...    id: str
    ...    account_number: str
    ...    padded_id: str = F.lpad(_.account_number, 10, "0")
    """
    return UnderscoreFunction("lpad", string, size, padstring)


def rpad(string: Underscore | Any, size: Underscore | Any, padstring: Underscore | Any):
    """
    Right-pad string to specified length with pad string.

    Parameters
    ----------
    string
        The string to pad.
    size
        The target length.
    padstring
        The string to pad with.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class ProductCode:
    ...    id: str
    ...    base_code: str
    ...    formatted_code: str = F.rpad(_.base_code, 15, "-")
    """
    return UnderscoreFunction("rpad", string, size, padstring)


def word_stem(string: Underscore | Any):
    """
    Extract the stem of a word using basic stemming rules.

    Parameters
    ----------
    string
        The word to stem.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class TextProcessing:
    ...    id: str
    ...    word: str
    ...    stemmed_word: str = F.word_stem(_.word)
    """
    return UnderscoreFunction("word_stem", string)


########################################################################################################################
# URLs                                                                                                                 #
########################################################################################################################


def url_extract_protocol(expr: Any):
    """
    Extract the protocol from a URL.

    For example, the protocol of `https://www.google.com/cats` is `https`.

    Parameters
    ----------
    expr
        The URL to extract the protocol from.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Company:
    ...     id: int
    ...     website: str
    ...     protocol: str = F.url_extract_protocol(_.website)
    """
    return UnderscoreFunction("url_extract_protocol", expr)


def url_extract_host(expr: Any):
    """
    Extract the host from a URL.

    For example, the host of `https://www.google.com/cats` is `www.google.com`.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Company:
    ...     id: int
    ...     website: str
    ...     host: str = F.url_extract_host(_.website)
    """
    return UnderscoreFunction("url_extract_host", expr)


def url_extract_path(expr: Any):
    """Extract the path from a URL.

    For example, the host of `https://www.google.com/cats` is `/cats`.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Company:
    ...     id: int
    ...     website: str
    ...     path: str = F.url_extract_path(_.website)
    """
    return UnderscoreFunction("url_extract_path", expr)


########################################################################################################################
# Hash functions                                                                                                       #
########################################################################################################################


def spooky_hash_v2_32(expr: Any):
    """
    Compute the SpookyHash V2 32-bit hash of a string.
    This hash function is not cryptographically secure,
    but it is deterministic and fast.

    Parameters
    ----------
    expr
        A string feature to hash.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    name: str
    ...    name_hash: bytes = F.spooky_hash_v2_32(
    ...        F.string_to_bytes(_.name, "utf-8")
    ...    )
    """
    return UnderscoreFunction("spooky_hash_v2_32", expr)


def spooky_hash_v2_64(expr: Any):
    """
    Compute the SpookyHash V2 64-bit hash of a string.
    This hash function is not cryptographically secure,
    but it is deterministic and fast.

    Parameters
    ----------
    expr
        A string feature to hash.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    name: str
    ...    name_hash: bytes = F.spooky_hash_v2_64(
    ...        F.string_to_bytes(_.name, "utf-8")
    ...    )
    """
    return UnderscoreFunction("spooky_hash_v2_64", expr)


def md5(expr: Any):
    """
    Compute the MD5 hash of some bytes.

    Parameters
    ----------
    expr
        A bytes feature to hash.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    bytes_feature: bytes
    ...    md5_bytes: bytes = F.md5(_.bytes_feature)
    """
    return UnderscoreFunction("md5", expr)


def sha1(expr: Any):
    """
    Compute the SHA-1 hash of some bytes.

    Parameters
    ----------
    expr
        A bytes feature to hash.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    bytes_feature: bytes
    ...    sha1_bytes: bytes = F.sha1(_.bytes_feature)
    """
    return UnderscoreFunction("sha1", expr)


def sha256(expr: Any):
    """
    Compute the SHA-256 hash of some bytes.

    Parameters
    ----------
    expr
        A bytes feature to hash.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    bytes_feature: bytes
    ...    sha256_bytes: bytes = F.sha256(_.bytes_feature)
    """
    return UnderscoreFunction("sha256", expr)


def sha512(expr: Any):
    """
    Compute the SHA-512 hash of some bytes.

    Parameters
    ----------
    expr
        A bytes feature to hash.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    bytes_feature: bytes
    ...    sha512_bytes: bytes = F.sha512(_.bytes_feature)
    """
    return UnderscoreFunction("sha512", expr)


########################################################################################################################
# Misc                                                                                                                 #
########################################################################################################################


def coalesce(*vals: Any):
    """
    Return the first non-null entry

    Parameters
    ----------
    vals
        Expressions to coalesce. They can be a combination of underscores and literals,
        though types must be compatible (ie do not coalesce int and string).

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    nickname: str | None
    ...    name: str | None
    ...    name_or_nickname: str = F.coalesce(_.name, _.nickname, "")
    """
    return UnderscoreFunction("coalesce", *vals)


def recover(*vals: Any):
    """
    Return the first valid entry. Functions like coalesce, but allows recovering from an upstream failure

    Parameters
    ----------
    vals
        Expressions to recover. They can be a combination of underscores and literals,
        though types must be compatible (ie do not recover int and string).

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    potentially_error_causing_name: str | None
    ...    fallback_name: str
    ...    name: str = F.recover(_.potentially_error_causing_name, _.fallback_name)
    """
    return UnderscoreFunction("recover", *vals)


def is_null(expr: Any):
    """
    Check if a value is null.

    Parameters
    ----------
    expr
        The value to check if it is null.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    nickname: str | None
    ...    missing_nickname: bool = F.is_null(_.nickname)
    """
    return UnderscoreFunction("is_null", expr)


class When:
    def __init__(self, parent: Then | None, condition: Any):
        super().__init__()
        self._then = parent
        self._condition = condition

    def then(self, value: Any) -> "Then":
        """The value to return if the condition is met.
        This method *must* be called after `.when(...)`.

        Parameters
        ----------
        value
            The value to return if the condition is met.
        """
        return Then(parent=self, value=value)


class Then:
    def __init__(self, parent: When, value: Any):
        super().__init__()
        self._when = parent
        self._value = value

    def when(self, condition: Any) -> When:
        """Add another condition to the conditional expression.

        After this method is called, it is expected that you will
        call `.then(...)` to specify the value to return if the
        condition is met.

        Parameters
        ----------
        condition
            The condition to evaluate.
        """
        return When(parent=self, condition=condition)

    def otherwise(self, default: Any) -> Any:
        """The default value to return if no conditions are met.

        Parameters
        ----------
        default
            The default value to return if no conditions are met.

        Returns
        -------
        Any
            The underscore expression. After this method has been called,
            you cannot add more conditions to the conditional expression.
        """
        result = default
        current: Then | None = self
        while current is not None:
            result = if_then_else(
                condition=current._when._condition,  # pyright: ignore[reportPrivateUsage]
                if_true=current._value,
                if_false=result,
            )
            current = current._when._then  # pyright: ignore[reportPrivateUsage]
        return result


def when(condition: Any) -> When:
    """Build a conditional expression.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    age: float
    ...    age_group: str = (
    ...      F.when(_.age < 1)
    ...       .then("baby")
    ...       .when(_.age < 3)
    ...       .then("toddler")
    ...       .when(_.age < 13)
    ...       .then("child")
    ...       .when(_.age < 18)
    ...       .then("teen")
    ...       .otherwise(F.cast(F.cast(F.floor(_.age / 10), int), str) + "0s")
    ...   )
    """
    return When(parent=None, condition=condition)


def if_then_else(condition: Underscore, if_true: Any, if_false: Any) -> Underscore:
    """
    Create a conditional expression, roughly equivalent to:

    ```
    if condition:
        return if_true
    else:
        return if_false
    ```

    Unlike a Python if/else, all three inputs `(condition, if_true, if_false)` are evaluated
    in parallel for all rows, and then the correct side is selected based on the result of
    the condition expression.

    Examples
    --------
    >>> from chalk import _
    >>> from chalk.features import features
    >>> @features
    ... class Transaction:
    ...    id: int
    ...    amount: int
    ...    risk_score: float = _.if_then_else(
    ...      _.amount > 10_000,
    ...      _.amount * 0.1,
    ...      _.amount * 0.05,
    ...    )
    """
    return UnderscoreFunction("if_else", condition, if_true, if_false)


KeyType = TypeVar("KeyType")
ValueType = TypeVar("ValueType")


def map_dict(
    d: dict[KeyType, ValueType],
    key: Underscore,
    *,
    default: ValueType | None,
):
    """
    Map a key to a value in a dictionary.

    Parameters
    ----------
    d
        The dictionary to map the key to a value in.
    key
        The key to look up in the dictionary.
    default
        The default value to return if the key is not found in the dictionary.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Transaction:
    ...    id: int
    ...    merchant: str
    ...    merchant_risk_score: float = F.map_dict(
    ...        {"Amazon": 0.1, "Walmart": 0.08},
    ...        _.merchant,
    ...        default=0.,
    ...    )
    """
    if default is not None:
        return coalesce(map_get(d, key), default)
    return map_get(d, key)


def map_get(mapping: Mapping[KeyType, ValueType], key: Any):
    """
    Get the value for a key in a mapping.

    Parameters
    ----------
    mapping
        The mapping to get the value from.
    key
        The key to get the value for.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Transaction:
    ...    id: int
    ...    merchant: str
    ...    merchant_risk_score: float = F.map_get(
    ...        {"Amazon": 0.1, "Walmart": 0.08},
    ...        _.merchant,
    ...    )
    """
    if isinstance(mapping, Underscore):
        return UnderscoreFunction("map_get", mapping, key)

    key_type = pa.scalar([k for k in mapping.keys()]).type.value_type
    value_type = pa.scalar([v for v in mapping.values()]).type.value_type
    map_type = pa.map_(key_type, value_type)
    return UnderscoreFunction("map_get", pa.scalar(mapping, type=map_type), key)


def struct_pack(mapping: Mapping[str, Underscore | Any]):
    """
    Construct a struct from a mapping of field names to values.

    Parameters
    ----------
    mapping
        The mapping of names to features to construct the struct from.

    Examples
    --------
    >>> import dataclasses
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @dataclasses.dataclass
    ... class TransactionInfo:
    ...    id: int
    ...    merchant: str
    >>> @features
    ... class Transaction:
    ...    id: int
    ...    merchant: str
    ...    transaction_info: TransactionInfo = F.struct_pack({
    ...        "id": _.id,
    ...        "merchant": _.merchant,
    ...    })
    """
    return UnderscoreFunction("struct_pack", list(mapping.keys()), *mapping.values())


def sagemaker_predict(
    body: Underscore | Any,
    *,
    endpoint: str,
    content_type: str | None = None,
    target_model: str | None = None,
    target_variant: str | None = None,
    aws_access_key_id_override: str | None = None,
    aws_secret_access_key_override: str | None = None,
    aws_session_token_override: str | None = None,
    aws_role_arn_override: str | None = None,
    aws_region_override: str | None = None,
    aws_profile_name_override: str | None = None,
):
    """
    Runs a sagemaker prediction on the specified endpoint, passing in the serialized bytes as a feature.

    Parameters
    ----------
    body
        Bytes feature to be passed as the serialized input to the sagemaker endpoint.
    endpoint
        The name of the sagemaker endpoint.
    content_type
        The content type of the input data. If not specified, the content type will be inferred from the endpoint.
    target_model
        An optional argument which specifies the target model for the prediction.
        This should only be used for multimodel sagemaker endpoints.
    target_variant
        An optional argument which specifies the target variant for the prediction.
        This should only be used for multi variant sagemaker endpoints.
    aws_access_key_id_override
        An optional argument which specifies the AWS access key ID to use for the prediction.
    aws_secret_access_key_override
        An optional argument which specifies the AWS secret access key to use for the prediction.
    aws_session_token_override
        An optional argument which specifies the AWS session token to use for the prediction.
    aws_role_arn_override
        An optional argument which specifies a AWS role ARN that will be assumed to generate credentials for the prediction.
    aws_region_override
        An optional argument which specifies the AWS region to use for the prediction.
    aws_profile_name_override
        An optional argument which specifies the AWS profile name to use for the prediction

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    encoded_sagemaker_data: bytes
    ...    prediction: float = F.sagemaker_predict(
    ...        _.encoded_sagemaker_data,
    ...        endpoint="prediction-model_1.0.1_2024-09-16",
    ...        target_model="model_v2.tar.gz",
    ...        target_variant="blue"
    ...    )
    """
    return UnderscoreFunction(
        "sagemaker_predict",
        body,
        endpoint=endpoint,
        content_type=content_type,
        target_model=target_model,
        target_variant=target_variant,
        aws_access_key_id_override=aws_access_key_id_override,
        aws_secret_access_key_override=aws_secret_access_key_override,
        aws_session_token_override=aws_session_token_override,
        aws_role_arn_override=aws_role_arn_override,
        aws_region_override=aws_region_override,
        aws_profile_name_override=aws_profile_name_override,
    )


def json_value(expr: Underscore, path: Union[str, Underscore]):
    """
    Extract structured data from a JSON string feature using a JSONPath expression.

    Parameters
    ----------
    expr
        The JSON string feature to query.
    path
        The JSONPath-like expression to extract the scalar from the JSON feature.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> from dataclasses import dataclass
    >>> @dataclass
    ... class Message:
    ...    content: str
    ...    sender: str
    ...    comments: List[str]
    ...
    >>> @features
    ... class User:
    ...    id: str
    ...    profile: str
    ...    favorite_color: str = F.json_value(_.profile, "$.prefs.color")
    ...    messages: List[Message] = F.json_value(_.profile, "$.messages")
    """

    return UnderscoreFunction("get_json_value", expr, path)


def json_extract_array(expr: Underscore, path: Union[str, Underscore]):
    """
    Extract an array from a JSON string feature using a JSONPath expression. The value of the referenced path must be a JSON
    node containing an array, or a wildcard object match like: $some_path[*].some_object_property.

    Only arrays of strings, bools, numbers, and nulls are supported. If the array contains objects, the function will
    return 'null'.

    Parameters
    ----------
    expr
        The JSON string feature to query.
    path
        The JSONPath-like expression to extract the array from the JSON feature.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    profile: str
    ...    favorite_categories: list[str] = F.json_extract_array(_.profile, "$.prefs.favorite_categories")
    """

    return UnderscoreFunction("json_extract_array", expr, path)


def gunzip(expr: Underscore):
    """
    Decompress a GZIP-compressed bytes feature.

    Parameters
    ----------
    expr
        The GZIP-compressed bytes feature to decompress.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    compressed_data: bytes
    ...    decompressed_data: bytes = F.gunzip(_.compressed_data)
    """
    return UnderscoreFunction("gunzip", expr)


def cosine_similarity(a: Underscore, b: Underscore):
    """
    Compute the cosine similarity between two vectors.

    Parameters
    ----------
    a
        The first vector.
    b
        The second vector.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    embedding: Vector[1536]
    >>> @features
    ... class Merchant:
    ...    id: str
    ...    embedding: Vector[1536]
    >>> @features
    ... class UserMerchant:
    ...    id: str
    ...    user_id: User.id
    ...    user: User
    ...    merchant_id: Merchant.id
    ...    merchant: Merchant
    ...    similarity: float = F.cosine_similarity(_.user.embedding, _.merchant.embedding)
    """
    return UnderscoreFunction("cosine_similarity_vector", a, b)


########################################################################################################################
# Mathematical Functions                                                                                               #
########################################################################################################################


def power(a: Underscore | Any, b: Underscore | Any):
    """
    Raise a to the power of b. Alias for `a ** b`.

    Parameters
    ----------
    a
        The base.
    b
        The exponent.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Merchant:
    ...    id: str
    ...    amount_std: float
    ...    amount_var: float = F.power(_.amount_std, 2)
    """
    return UnderscoreFunction("power", a, b)


def sqrt(expr: Underscore | Any):
    """
    Compute the square root of a number.

    Parameters
    ----------
    expr
        The number to compute the square root of.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Merchant:
    ...    id: str
    ...    amount_var: float
    ...    amount_std: float = F.sqrt(_.amount_var)
    """
    return UnderscoreFunction("sqrt", expr)


def safe_divide(x: Underscore | Any, y: Underscore | Any):
    """
    Computes x / y, returning None if y is 0.

    Parameters
    ----------
    x
        The numerator.
    y
        The denominator.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Merchant:
    ...    id: str
    ...    a: float
    ...    b: float
    ...    amount_std: float = F.safe_divide(_.a, _.b)
    """

    return if_then_else(
        condition=y == 0,
        if_true=None,
        if_false=x / y,
    )


def floor(expr: Underscore | Any):
    """
    Compute the floor of a number.

    Parameters
    ----------
    expr
        The number to compute the floor of.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Transaction:
    ...    id: str
    ...    amount: float
    ...    amount_floor: float = F.floor(_.amount)
    """
    return UnderscoreFunction("floor", expr)


def ceil(expr: Underscore | Any):
    """
    Compute the ceiling of a number.

    Parameters
    ----------
    expr
        The number to compute the ceiling of.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Transaction:
    ...    id: str
    ...    amount: float
    ...    amount_ceil: float = F.ceil(_.amount)
    """
    return UnderscoreFunction("ceil", expr)


def mod(dividend: Underscore | Any, divisor: Underscore | Any):
    """
    Compute the remainder of a division.

    Parameters
    ----------
    dividend
        The dividend.
    divisor
        The divisor.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Transaction:
    ...    id: str
    ...    date: datetime
    ...    day_of_week_monday: int = F.day_of_week(_.date)
    ...    day_of_week_sunday: int = F.mod(_.day_of_week_monday, 7) + 1
    """
    return UnderscoreFunction("%", dividend, divisor)


def abs(expr: Underscore | Any):
    """
    Compute the absolute value of a number.

    Parameters
    ----------
    expr
        The number to compute the absolute value of.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Transaction:
    ...    id: str
    ...    amount: float
    ...    amount_abs: float = F.abs(_.amount)
    """
    return UnderscoreFunction("abs", expr)


def radians(expr: Underscore | Any):
    """
    Convert degrees to radians.

    Parameters
    ----------
    expr
        The number to convert to radians.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class FullCircle:
    ...    id: str
    ...    degrees: float
    ...    radians: float = F.radians(_.degrees)
    """
    return UnderscoreFunction("radians", expr)


def sin(expr: Underscore | Any):
    """
    Compute the sine of an angle in radians.

    Parameters
    ----------
    expr
        The angle in radians.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Triangle:
    ...    id: str
    ...    angle: float
    ...    sin_angle: float = F.sin(_.angle)
    """
    return UnderscoreFunction("sin", expr)


def asin(expr: Underscore | Any):
    """
    Compute the arcsine of an angle in radians.

    Parameters
    ----------
    expr
        The angle in radians.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Triangle:
    ...    id: str
    ...    sin_angle: float
    ...    angle: float = F.asin(_.sin_angle)
    """
    return UnderscoreFunction("asin", expr)


def cos(expr: Underscore | Any):
    """
    Compute the cosine of an angle in radians.

    Parameters
    ----------
    expr
        The angle in radians.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Triangle:
    ...    id: str
    ...    angle: float
    ...    cos_angle: float = F.cos(_.angle)
    """
    return UnderscoreFunction("cos", expr)


def acos(expr: Underscore | Any):
    """
    Compute the arccosine of an angle in radians.

    Parameters
    ----------
    expr
        The angle in radians.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Triangle:
    ...    id: str
    ...    cos_angle: float
    ...    angle: float = F.acos(_.cos_angle)
    """
    return UnderscoreFunction("acos", expr)


def ln(expr: Underscore | Any):
    """
    Compute the natural logarithm of a number.

    Parameters
    ----------
    expr
        The number to compute the natural logarithm of.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Triangle:
    ...    id: str
    ...    hypotenuse: float
    ...    log_hypotenuse: float = F.ln(_.hypotenuse)
    """
    return UnderscoreFunction("ln", expr)


def exp(expr: Underscore | Any):
    """
    Returns Euler’s number raised to the power of x.

    Parameters
    ----------
    expr
        The exponent to raise Euler's number to.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class CompoundGrowth:
    ...    id: str
    ...    growth_rate: float
    ...    compound_factor: float = F.exp(_.growth_rate)
    """
    return UnderscoreFunction("exp", expr)


def atan(expr: Underscore | Any):
    """
    Compute the arctangent of a number.

    Parameters
    ----------
    expr
        The number to compute the arctangent of.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class TradingSignal:
    ...    id: str
    ...    momentum: float
    ...    angle: float = F.atan(_.momentum)
    """
    return UnderscoreFunction("atan", expr)


def atan2(y: Underscore | Any, x: Underscore | Any):
    """
    Compute the arctangent of y/x using the signs of the arguments to determine the quadrant.

    Parameters
    ----------
    y
        The y-coordinate.
    x
        The x-coordinate.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class MarketPosition:
    ...    id: str
    ...    profit: float
    ...    risk: float
    ...    portfolio_angle: float = F.atan2(_.profit, _.risk)
    """
    return UnderscoreFunction("atan2", y, x)


def cbrt(expr: Underscore | Any):
    """
    Compute the cube root of a number.

    Parameters
    ----------
    expr
        The number to compute the cube root of.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class RiskMetric:
    ...    id: str
    ...    volume: float
    ...    volatility_factor: float = F.cbrt(_.volume)
    """
    return UnderscoreFunction("cbrt", expr)


def cosh(expr: Underscore | Any):
    """
    Compute the hyperbolic cosine of a number.

    Parameters
    ----------
    expr
        The number to compute the hyperbolic cosine of.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class InterestRate:
    ...    id: str
    ...    rate: float
    ...    hyperbolic_growth: float = F.cosh(_.rate)
    """
    return UnderscoreFunction("cosh", expr)


def degrees(expr: Underscore | Any):
    """
    Convert angle from radians to degrees.

    Parameters
    ----------
    expr
        The angle in radians to convert.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class TrendAnalysis:
    ...    id: str
    ...    slope_radians: float
    ...    slope_degrees: float = F.degrees(_.slope_radians)
    """
    return UnderscoreFunction("degrees", expr)


def tanh(expr: Underscore | Any):
    """
    Compute the hyperbolic tangent of a number.

    Parameters
    ----------
    expr
        The number to compute the hyperbolic tangent of.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class ActivationFunction:
    ...    id: str
    ...    input_score: float
    ...    normalized_score: float = F.tanh(_.input_score)
    """
    return UnderscoreFunction("tanh", expr)


def sign(expr: Underscore | Any):
    """
    Compute the sign of a number (-1, 0, or 1).

    Parameters
    ----------
    expr
        The number to compute the sign of.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class PriceMovement:
    ...    id: str
    ...    price_change: float
    ...    direction: float = F.sign(_.price_change)
    """
    return UnderscoreFunction("sign", expr)


def pow(base: Underscore | Any, exponent: Underscore | Any):
    """
    Raise base to the power of exponent.

    Parameters
    ----------
    base
        The base number.
    exponent
        The exponent.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Portfolio:
    ...    id: str
    ...    initial_value: float
    ...    growth_rate: float
    ...    final_value: float = F.pow(_.initial_value, _.growth_rate)
    """
    return UnderscoreFunction("pow", base, exponent)


def sigmoid(expr: Underscore | Any):
    """
    Compute the sigmoid of a number.

    Parameters
    ----------
    expr
        The number to compute the sigmoid of.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Sigmoid:
    ...    id: str
    ...    x: float
    ...    sigmoid_of_x: float = F.sigmoid(_.x)
    """
    return 1 / (1 + exp(-1 * expr))


def clamp(expr: Underscore | Any, min_val: Underscore | Any, max_val: Underscore | Any):
    """
    Clamp a value between a minimum and maximum range.

    Parameters
    ----------
    expr
        The value to clamp.
    min_val
        The minimum value.
    max_val
        The maximum value.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class RiskModel:
    ...    id: str
    ...    raw_score: float
    ...    risk_score: float = F.clamp(_.raw_score, 0.0, 1.0)
    """
    return UnderscoreFunction("clamp", expr, min_val, max_val)


def e():
    """
    Return Euler's number (e ≈ 2.718).

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class CompoundInterest:
    ...    id: str
    ...    rate: float
    ...    time: float
    ...    e_constant: float = F.e()
    """
    return UnderscoreFunction("e")


def greatest(*args: Underscore | Any):
    """
    Return the greatest value among the arguments, ignoring null values.

    Parameters
    ----------
    *args
        The values to compare.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Portfolio:
    ...    id: str
    ...    return_1y: float
    ...    return_3y: float
    ...    return_5y: float
    ...    best_return: float = F.greatest(_.return_1y, _.return_3y, _.return_5y)
    """
    return UnderscoreFunction("greatest", *args)


def least(*args: Underscore | Any):
    """
    Return the smallest value among the arguments, ignoring null values.

    Parameters
    ----------
    *args
        The values to compare.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Portfolio:
    ...    id: str
    ...    return_1y: float
    ...    return_3y: float
    ...    return_5y: float
    ...    worst_return: float = F.least(_.return_1y, _.return_3y, _.return_5y)
    """
    return UnderscoreFunction("least", *args)


def pi():
    """
    Return the value of π (pi ≈ 3.14159).

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Geometry:
    ...    id: str
    ...    radius: float
    ...    circumference: float = 2 * F.pi() * _.radius
    """
    return UnderscoreFunction("pi")


def rand():
    """
    Return a random number between 0 and 1.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Sampling:
    ...    id: str
    ...    random_weight: float = F.rand()
    """
    return UnderscoreFunction("rand")


def to_base(number: Underscore | Any, base: Underscore | Any):
    """
    Convert a number to its string representation in the specified base.

    Parameters
    ----------
    number
        The number to convert.
    base
        The base to convert to (2-36).

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Encoding:
    ...    id: str
    ...    decimal_id: int
    ...    hex_id: str = F.to_base(_.decimal_id, 16)
    """
    return UnderscoreFunction("to_base", number, base)


def width_bucket(
    operand: Underscore | Any, bound1: Underscore | Any, bound2: Underscore | Any, bucket_count: Underscore | Any
):
    """
    Assign a bucket number to a value based on histogram buckets.

    Parameters
    ----------
    operand
        The value to assign to a bucket.
    bound1
        The lower bound of the range.
    bound2
        The upper bound of the range.
    bucket_count
        The number of buckets.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class CustomerSegmentation:
    ...    id: str
    ...    transaction_amount: float
    ...    amount_bucket: int = F.width_bucket(_.transaction_amount, 0.0, 1000.0, 10)
    """
    return UnderscoreFunction("width_bucket", operand, bound1, bound2, bucket_count)


def log2(expr: Underscore | Any):
    """
    Compute the base-2 logarithm of a number.

    Parameters
    ----------
    expr
        The number to compute the base-2 logarithm of.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class EntropyCalculation:
    ...    id: str
    ...    probability: float
    ...    information_content: float = F.log2(_.probability)
    """
    return UnderscoreFunction("log2", expr)


def log10(expr: Underscore | Any):
    """
    Compute the base-10 logarithm of a number.

    Parameters
    ----------
    expr
        The number to compute the base-10 logarithm of.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class PhScaleCalculation:
    ...    id: str
    ...    hydrogen_concentration: float
    ...    ph_value: float = -F.log10(_.hydrogen_concentration)
    """
    return UnderscoreFunction("log10", expr)


def normal_cdf(x: Underscore | Any, mean: Underscore | Any, std_dev: Underscore | Any):
    """
    Compute the cumulative distribution function of the normal distribution.

    Parameters
    ----------
    x
        The value at which to evaluate the CDF.
    mean
        The mean of the normal distribution.
    std_dev
        The standard deviation of the normal distribution.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class RiskAssessment:
    ...    id: str
    ...    score: float
    ...    mean_score: float
    ...    std_score: float
    ...    percentile: float = F.normal_cdf(_.score, _.mean_score, _.std_score)
    """
    return UnderscoreFunction("normal_cdf", x, mean, std_dev)


########################################################################################################################
# Date and Time Functions                                                                                              #
########################################################################################################################


def format_datetime(input_dt: Any, format: str | Any):
    """Format a datetime feature using a Joda-Time format string.

    ```
    | Symbol | Meaning                      | Examples                           |
    |--------|------------------------------|------------------------------------|
    | G      | era                          | AD                                 |
    | C      | century of era (>=0)         | 20                                 |
    | Y      | year of era (>=0)            | 1996                               |
    | x      | weekyear                     | 1996                               |
    | w      | week of weekyear             | 27                                 |
    | e      | day of week                  | 2                                  |
    | E      | day of week                  | Tuesday; Tue                       |
    | y      | year                         | 1996                               |
    | D      | day of year                  | 189                                |
    | M      | month of year                | July; Jul; 07                      |
    | d      | day of month                 | 10                                 |
    | a      | halfday of day               | PM                                 |
    | K      | hour of halfday (0~11)       | 0                                  |
    | h      | clockhour of halfday (1~12)  | 12                                 |
    | H      | hour of day (0~23)           | 0                                  |
    | k      | clockhour of day (1~24)      | 24                                 |
    | m      | minute of hour               | 30                                 |
    | s      | second of minute             | 55                                 |
    | S      | fraction of second           | 978                                |
    | z      | time zone                    | Pacific Standard Time; PST         |
    | Z      | time zone offset/id          | -0800; -08:00; America/Los_Angeles |
    | '      | escape for text              |                                    |
    | ''     | single quote                 | '                                  |
    ```

    Examples
    --------
    >>> from datetime import datetime
    >>> from chalk.features import _, features
    >>> @features
    >>> class Iso8601:
    ...   id: int
    ...   dt: datetime
    ...   formatted_datetime: str = F.format_datetime(_.dt, "YYYY-MM-DD HH:mm:ss")
    ...   other_formatted_datetime: str = F.format_datetime(_.dt, "YY-MM-DD HH:mm:ss.S")
    """
    return UnderscoreFunction("format_datetime", input_dt, format)


def total_seconds(delta: Underscore) -> Underscore:
    """
    Compute the total number of seconds covered in a duration.

    Parameters
    ----------
    delta
        The duration to convert to seconds.

    Examples
    --------
    >>> from datetime import date
    >>> from chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Transaction:
    ...    id: str
    ...    signup: date
    ...    last_login: date
    ...    signup_to_last_login_days: float = F.total_seconds(_.last_login - _.signup) / (60 * 60 * 24)
    """
    return UnderscoreFunction("total_seconds", delta)


def unix_seconds(expr: Underscore | Any):
    """
    Extract the number of seconds since the Unix epoch.
    Returned as a float.

    Parameters
    ----------
    expr
        The datetime to extract the number of seconds since the Unix epoch from.

    Examples
    --------
    >>> from datetime import datetime
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Transaction:
    ...    id: str
    ...    date: datetime
    ...    unix_seconds: float = F.unix_seconds(_.date)
    """
    return UnderscoreFunction("to_unixtime", expr)


def unix_milliseconds(expr: Underscore | Any):
    """
    Extract the number of milliseconds since the Unix epoch.
    Returned as a float.

    Parameters
    ----------
    expr
        The datetime to extract the number of milliseconds since the Unix epoch from.

    Examples
    --------
    >>> from datetime import datetime
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Transaction:
    ...    id: str
    ...    date: datetime
    ...    unix_milliseconds: float = F.unix_milliseconds(_.date)
    """
    return UnderscoreFunction("to_unixtime", expr) * 1000.0


def from_unix_seconds(expr: Underscore | Any):
    """
    Converts a Unix timestamp (in seconds) to a utc timestamp.

    Parameters
    ----------
    expr
        The Unix timestamp to convert.

    Examples
    --------
    >>> from datetime import datetime
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Linux:
    ...    id: str
    ...    unixtime_s: int = 0
    ...    unix: int = F.unix_milliseconds(_.date)
    """
    return UnderscoreFunction("from_unixtime", expr)


def from_unix_milliseconds(expr: Underscore | Any):
    """
    Converts a Unix timestamp (in milliseconds) to a utc timestamp.

    Parameters
    ----------
    expr
        A date represented as the number of millisecods since the Unix timestamp.

    Examples
    --------
    >>> from datetime import datetime
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Linux:
    ...    id: int
    ...    unixtime_ms: int = 0
    ...    unixtime: datetime = F.from_unix_milliseconds(_.unix)
    """
    return UnderscoreFunction("from_unixtime", (expr / 1000))


def day(expr: Underscore | Any):
    """
    Extract the day of the month from a date. Alias for day_of_month.

    The supported types for x are date and datetime.

    Ranges from 1 to 31 inclusive.

    Parameters
    ----------
    expr
        The date to extract the day of the month from.

    Examples
    --------
    >>> from datetime import date
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Transaction:
    ...    id: str
    ...    date: date
    ...    day: int = F.day(_.date)
    """
    return UnderscoreFunction("day", expr)


def day_of_month(expr: Underscore | Any):
    """
    Extract the day of the month from a date.

    The supported types for x are date and datetime.

    Ranges from 1 to 31 inclusive.

    Parameters
    ----------
    expr
        The date to extract the day of the month from.

    Examples
    --------
    >>> from datetime import date
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Transaction
    ...    id: str
    ...    date: date
    ...    day: int = F.day_of_month(_.date)
    """
    return UnderscoreFunction("day_of_month", expr)


def day_of_week(
    expr: Underscore | Any,
    start_of_week: DayOfWeek = DayOfWeek.MONDAY,
):
    """
    Returns the ISO day of the week from x. The value ranges from 1 (`start_of_week`, default `MONDAY`)
    to 7 (`start_of_week + 6`, default `SUNDAY`).

    Parameters
    ----------
    expr
        The date to extract the day of the week from.
    start_of_week
        The day of the week that the week starts on. Defaults to Monday.

    Examples
    --------
    >>> from datetime import date
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Transaction
    ...    id: str
    ...    date: date
    ...    day: int = F.day_of_week(_.date)
    """
    if start_of_week == DayOfWeek.MONDAY == 1:
        return UnderscoreFunction("day_of_week", expr)
    return ((UnderscoreFunction("day_of_week", expr) - int(start_of_week)) + 7) % 7 + 1


def day_of_year(expr: Underscore | Any):
    """
    Extract the day of the year from a date.

    The value ranges from 1 to 366.

    Parameters
    ----------
    expr
        The date to extract the day of the year from.

    Examples
    --------
    >>> from datetime import date
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Transaction:
    ...    id: str
    ...    date: date
    ...    day: int = F.day_of_year(_.date)
    """
    return UnderscoreFunction("day_of_year", expr)


def month_of_year(expr: Underscore | Any):
    """
    Extract the month of the year from a date.

    The value ranges from 1 to 12.

    Parameters
    ----------
    expr
        The date to extract the month of the year from.

    Examples
    --------
    >>> from datetime import date
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Transaction:
    ...    id: str
    ...    date: date
    ...    month: int = F.month_of_year(_.date)
    """
    return UnderscoreFunction("month", expr)


def year(expr: Underscore | Any):
    """
    Extract the year from the date.

    Parameters
    ----------
    expr
        The date to extract the year from.

    Examples
    --------
    >>> from datetime import date
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Transaction:
    ...    id: str
    ...    date: date
    ...    year: int = F.year(_.date)
    """
    return UnderscoreFunction("year", expr)


def quarter(expr: Underscore | Any):
    """
    Extract the quarter from the date.

    The value ranges from 1 to 4.

    Parameters
    ----------
    expr
        The date to extract the quarter from.

    Examples
    --------
    >>> from datetime import date
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Transaction:
    ...    id: str
    ...    date: date
    ...    quarter: int = F.quarter(_.date)
    """
    return UnderscoreFunction("quarter", expr)


def date_trunc(
    expr: Underscore | Any,
    unit: Literal[
        "second",
        "minute",
        "hour",
        "day",
        "week",
        "month",
        "quarter",
        "year",
    ],
):
    """

    For example, the following table shows the result of truncating the input datetime
    `2024-09-17 12:34:56.789` with the various units:

    | Unit     | Result                   |
    |----------|--------------------------|
    | second   | 2024-09-17 12:34:56      |
    | minute   | 2024-09-17 12:34         |
    | hour     | 2024-09-17 12:00         |
    | day      | 2024-09-17               |
    | week     | 2024-09-16               |
    | month    | 2024-09-01               |
    | quarter  | 2024-07-01               |
    | year     | 2024-01-01               |
    """
    return UnderscoreFunction("date_trunc", unit, expr)


def is_leap_year(expr: Underscore | Any):
    """
    Determine whether the given date is in a leap year.

    Parameters
    ----------
    expr
        The date to test.

    Examples
    --------
    >>> from datetime import date
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Transaction:
    ...    id: str
    ...    date: date
    ...    leap_year: bool = F.is_leap_year(_.date)
    """
    return ((mod(year(expr), 4) == 0) & (mod(year(expr), 100) != 0)) | (mod(year(expr), 400) == 0)


def last_day_of_month(expr: Underscore | Any):
    """
    Given a date, returns the last day in that date's month.

    Parameters
    ----------
    expr
        The date whose corresponding month (and year) will be used to determine the last day of the month.

    Examples
    --------
    >>> from datetime import date
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Transaction:
    ...    id: str
    ...    date: date
    ...    last_day_of_month: int = F.last_day_of_month(_.date)
    """
    return UnderscoreFunction("last_day_of_month", expr)


def is_month_end(expr: Underscore | Any):
    """
    Determine whether the provided date is the last day of the month.

    Parameters
    ----------
    expr
        The date to test.

    Examples
    --------
    >>> from datetime import date
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Transaction:
    ...    id: str
    ...    date: date
    ...    month_end: bool= F.is_month_end(_.date)
    """
    return day_of_month(last_day_of_month(expr)) == day_of_month(expr)


def week_of_year(expr: Underscore | Any):
    """
    Extract the week of the year from a date.

    The value ranges from 1 to 53.

    Parameters
    ----------
    expr
        The date to extract the week of the year from.

    Examples
    --------
    >>> from datetime import date
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Transaction:
    ...    id: str
    ...    date: date
    ...    week: int = F.week_of_year(_.date)
    """
    return UnderscoreFunction("week_of_year", expr)


def hour_of_day(expr: Underscore | Any, tz: dt.timezone | None = None):
    """
    Extract the hour of the day from a datetime.

    The value ranges from 0 to 23.

    Parameters
    ----------
    expr
        The datetime to extract the hour of the day from.

    tz
        The timezone to use for the hour. By default, UTC is used.

    Examples
    --------
    >>> from datetime import datetime
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Transaction:
    ...    id: str
    ...    date: datetime
    ...    hour: int = F.hour_of_day(_.date)
    """
    if tz is None:
        return UnderscoreFunction("hour", expr)
    offset = tz.utcoffset(None)
    if offset is None:  #  pyright: ignore[reportUnnecessaryComparison]
        raise ValueError("TZ must be a timezone with a fixed offset (likely the provide timezone is a DST timezone).")

    return UnderscoreFunction("hour", from_unix_seconds(unix_seconds(expr) + offset.total_seconds()))


def to_iso8601(expr: Underscore | Any):
    """
    Formats input datetime as an ISO 8601 string

    Parameters
    ----------
    expr
        The datetime to convert into ISO 8601 string.

    Examples
    --------
    >>> from datetime import datetime
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class IsoStr:
    ...    id: str
    ...    iso_str: str = F.to_iso8601(_.iso_date)
    ...    iso_date: datetime
    """
    return UnderscoreFunction("to_iso8601", expr)


def from_iso8601_timestamp(expr: Underscore | Any):
    """
    Converts an ISO 8601 string into a datetime.

    Parameters
    ----------
    expr
        The ISO 8601 string to convert into a datetime.


    """
    return UnderscoreFunction("from_iso8601_timestamp", expr)


def parse_datetime(expr: Underscore | Any, format: str | None = None):
    """
    Converts an ISO 8601 string into a datetime.

    Parameters
    ----------
    expr
        The ISO 8601 string to convert into a datetime.


    """
    return UnderscoreFunction("parse_datetime", expr, format)


def is_us_federal_holiday(expr: Underscore | Any):
    """
    Returns `True` if the given date or datetime is a US Federal Holiday, else `False`

    Parameters
    ----------
    expr
        The date or datetime to be tested

    Examples
    --------
    >>> from datetime import datetime
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Event:
    ...    id: str
    ...    event_date: datetime
    ...    is_us_federal_holiday: F.is_us_federal_holiday(_.event_date)

    Notes
    -----
    Here is a list of the US Federal Holidays:
    - New Year's Day (January 1)*
    - Martin Luther King's Birthday (3rd Monday in January)
    - Washington's Birthday (3rd Monday in February)**
    - Memorial Day (last Monday in May)
    - Juneteenth National Independence Day (June 19)*
    - Independence Day (July 4)*
    - Labor Day (1st Monday in September)
    - Columbus Day (2nd Monday in October)
    - Veterans' Day (November 11)*
    - Thanksgiving Day (4th Thursday in November)
    - Christmas Day (December 25)*

    * If one of these dates would fall on a Saturday/Sunday, the federal holiday will
      be observed on the proceeding Friday/following Monday, respectively

    ** More commonly known as "Presidents' Day"

    *** Every four years, Inaguration Day (January 20) is recognized as a federal holiday
        exclusively in Washington D.C. Inaguration days are *not* accounted for in this underscore
    """
    return UnderscoreFunction.with_f_dot_repr("is_federal_holiday", expr, display_name="is_us_federal_holiday")


########################################################################################################################
# DataFrame Aggregations                                                                                               #
########################################################################################################################


def max_by(dataframe: Underscore | Any, sort: Underscore | Any):
    """
    Returns the row in a dataframe or has-many relationship with the maximum value in a given column.

    Parameters
    ----------
    dataframe
        The `DataFrame` or has-many relationship to find the maximum value in.
        This `DataFrame` should refer to *exactly* one result column, which
        should reference the returned value. The `DataFrame` can include any
        necessary filters.
    sort
        The column on which to sort.

    Returns
    -------
    The maximum value row, or a transformed representation based on the columns provided.

    Examples
    --------
    >>> from chalk import DataFrame, _
    >>> from chalk.features import features, has_one
    >>> import chalk.functions as F
    >>> @features
    ... class Transaction:
    ...     id: int
    ...     amount: float
    ...     user_id: int
    >>> @features
    ... class User:
    ...     id: int
    ...     transactions: DataFrame[Transaction] = has_many(lambda: User.id == Transaction.user_id)
    ...     biggest_transfer_id: int = F.max_by(
    ...         _.transactions[_.category == "ach", _.id],
    ...         _.amount,
    ...     )
    ...     biggest_transfer: Transaction = has_one(
    ...         lambda: Transaction.id == User.biggest_transfer_id
    ...     )
    """
    return UnderscoreFunction("max_by", dataframe, sort)


def max_by_n(dataframe: Underscore | Any, sort: Underscore | Any, n: int):
    """
    Returns the rows in a dataframe or has-many relationship with the maximum n values in a given column.
    This is equivalent to `sort_by(sort_col, DESC).head(n)[result_col]`

    Parameters
    ----------
    dataframe
        The `DataFrame` or has-many relationship to find the maximum value in.
        This `DataFrame` should refer to *exactly* one result column, which
        should reference the returned value. The `DataFrame` can include any
        necessary filters.
    sort
        The column on which to sort.
    n
        The number of rows to return.

    Returns
    -------
    The n maximum value rows, or a transformed representation based on the columns provided,
    in descending order

    Examples
    --------
    >>> from datetime import datetime
    >>> from chalk import DataFrame, _
    >>> from chalk.features import features, has_one
    >>> import chalk.functions as F
    >>> @features
    ... class Transaction:
    ...     id: int
    ...     processed_date: datetime
    ...     amount: float
    ...     user_id: "User.id"
    >>> @features
    ... class User:
    ...     id: int
    ...     transactions: DataFrame[Transaction]
    ...     last_3_txns_avg: float = F.array_average(
    ...         F.max_by_n(
    ...             _.transactions[_.amount],
    ...             _.processed_date,
    ...             3,
    ...         )
    ...     )
    """
    return UnderscoreFunction("max_by_n", dataframe, sort, n)


def min_by(dataframe: Underscore | Any, sort: Underscore | Any):
    """
    Returns the row in a dataframe or has-many relationship with the minimum value in a given column.

    Parameters
    ----------
    dataframe
        The `DataFrame` or has-many relationship to find the minimum value in.
        This `DataFrame` should refer to *exactly* one result column, which
        should reference the returned value. The `DataFrame` can include any
        necessary filters.
    sort
        The column on which to sort.

    Returns
    -------
    The minimum value row, or a transformed representation based on the columns provided.

    Examples
    --------
    >>> from chalk import DataFrame, _
    >>> from chalk.features import features, has_one
    >>> import chalk.functions as F
    >>> @features
    ... class Transaction:
    ...     id: int
    ...     amount: float
    ...     user_id: int
    >>> @features
    ... class User:
    ...     id: int
    ...     transactions: DataFrame[Transaction] = has_many(lambda: User.id == Transaction.user_id)
    ...     smallest_transfer_id: int = F.min_by(
    ...         _.transactions[_.category == "ach", _.id],
    ...         _.amount,
    ...     )
    ...     smallest_transfer: Transaction = has_one(
    ...         lambda: Transaction.id == User.smallest_transfer_id
    ...     )
    """
    return UnderscoreFunction("min_by", dataframe, sort)


def min_by_n(dataframe: Underscore | Any, sort: Underscore | Any, n: int):
    """
    Returns the rows in a dataframe or has-many relationship with the minimum n values in a given column.
    This is equivalent to `sort_by(sort_col, ASC).head(n)[result_col]`

    Parameters
    ----------
    dataframe
        The `DataFrame` or has-many relationship to find the minimum value in.
        This `DataFrame` should refer to *exactly* one result column, which
        should reference the returned value. The `DataFrame` can include any
        necessary filters.
    sort
        The column on which to sort.
    n
        The number of rows to return.

    Returns
    -------
    The n minimum value rows, or a transformed representation based on the columns provided,
    in ascending order

    Examples
    --------
    >>> from datetime import datetime
    >>> from chalk import DataFrame, _
    >>> from chalk.features import features, has_one
    >>> import chalk.functions as F
    >>> @features
    ... class Transaction:
    ...     id: int
    ...     processed_date: datetime
    ...     amount: float
    ...     user_id: "User.id"
    >>> @features
    ... class User:
    ...     id: int
    ...     transactions: DataFrame[Transaction]
    ...     earliest_3_txns_avg: float = F.array_average(
    ...         F.min_by_n(
    ...             _.transactions[_.amount],
    ...             _.processed_date,
    ...             3,
    ...         )
    ...     )
    """
    return UnderscoreFunction("min_by_n", dataframe, sort, n)


def head(dataframe: Underscore | Any, n: Underscore | int):
    """
    Returns the first n items from a dataframe or has-many

    Parameters
    ----------
    dataframe
        the has-many from which the first n items are taken
    n
        how many items to take

    Examples
    --------
    >>> from datetime import datetime
    >>> import chalk.functions as F
    >>> from chalk import windowed, DataFrame, Windowed
    >>> from chalk.features import _, features, Primary
    >>> @features
    >>> class Merchant:
    ...     id: str
    >>> @features
    >>> class ConfirmedFraud:
    ...     id: int
    ...     trn_dt: datetime
    ...     is_fraud: int
    ...     mer_id: Merchant.id
    >>> @features
    >>> class MerchantFraud:
    ...     mer_id: Primary[Merchant.id]
    ...     merchant: Merchant
    ...     confirmed_fraud: DataFrame[ConfirmedFraud] = dataframe(
    ...         lambda: ConfirmedFraud.mer_id == MerchantFraud.mer_id,
    ...     )
    ...     first_five_merchant_window_fraud: Windowed[list[int]] = windowed(
    ...         "1d",
    ...         "30d",
    ...         expression=F.head(_.confirmed_fraud[_.trn_dt > _.chalk_window, _.id, _.is_fraud == 1], 5)
    ...     )
    """
    return slice(UnderscoreFunction("array_agg", dataframe), 0, n)


########################################################################################################################
# Array Functions                                                                                                      #
########################################################################################################################
def _convert_to_0_index(index: Underscore | int):
    if isinstance(index, int):
        return index if index < 0 else index + 1
    else:
        return UnderscoreFunction(
            "if_else", UnderscoreFunction("<", index, 0), index, UnderscoreFunction("+", index, 1)
        )


def slice(arr: Underscore | list[Any], offset: Underscore | int, length: Underscore | int):
    """
    Returns a subset of the original array.

    Parameters
    ----------
    arr
        The array to slice
    offset
        Starting index of the slice (0-indexed). If negative, slice starts from the end of the array
    length
        The length of the slice.

    Examples
    --------
    >>> from datetime import datetime
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Wordle:
    ...    id: str
    ...    words: list[str] = ["crane", "kayak", "plots", "fight", "exact", "zebra", "hello", "world"]
    ...    three_most_recent_words: list[str] = F.slice(_.words, -3, 3) # computes ["zebra", "hello", "world"]
    """

    start = _convert_to_0_index(offset)
    return UnderscoreFunction("slice", arr, start, length)


def concat(first: Underscore | Any, second: Underscore | Any):
    """
    Concatenate two arrays into a single array.
    """
    return UnderscoreFunction("concat", first, second)


def array_sort(expr: Underscore | Any, descending: bool = False):
    """
    Returns an array which has the sorted order of the input
    array. Null elements will be placed at the end of the
    returned array.

    Parameters
    ----------
    expr
        The array to sort
    descending
        Whether to sort the array in descending order. Defaults to False.
    """
    if descending:
        return UnderscoreFunction("array_sort_desc", expr)
    return UnderscoreFunction("array_sort", expr)


def array_stddev(expr: Underscore | Any):
    """
    Calculates the standard deviation of the numerical values of an array.

    Parameters
    ----------
    expr
        The array to calculate the standard deviation
    """
    return UnderscoreFunction("array_stddev", expr, False)


def array_sample_stddev(expr: Underscore | Any):
    """
    Calculates the sample standard deviation of the numerical values of an array.
    Divides square difference from means by N-1 as opposed to N

    Parameters
    ----------
    expr
        The array to calculate the sample standard deviation
    """
    return UnderscoreFunction("array_stddev", expr, True)


def array_sum(expr: Underscore | Any):
    """
    Calculates the sum of the numerical values of an array.

    Parameters
    ----------
    expr
        The array to sum
    """
    return UnderscoreFunction("array_sum", expr)


def array_average(expr: Underscore | Any):
    """
    Calculates the arithmetic mean of the numerical values of an array.

    Parameters
    ----------
    expr
        The array to average
    """
    return UnderscoreFunction("array_average", expr)


def array_median(expr: Underscore | Any):
    """
    Calculates the median of the numerical values of an array.

    Parameters
    ----------
    expr
        The array to take the median of
    """
    return UnderscoreFunction.with_f_dot_repr("array_median", expr)


def array_mode(expr: Underscore | Any, tiebreak: Literal["FIRST", "MAX", "MIN"] = "FIRST"):
    """
    Calculates the mode of the numerical values of an array.

    Parameters
    ----------
    expr
        The array to take the mode of; if there are multiple modes, undefined which one is returned
    tiebreak
        If there are multiple modes, which mode to select. Take the example list `[0, 2, 1, 2, 3, 3, 1, 4]` with multimodes 1, 2, 3:

            ``"FIRST"`` will return 2, as 2 occurs before 1 and 3 in the list;

            ``"MAX"`` will return 3, the max of the multimodes;

            ``"MIN"`` will return 1, the min of the multimodes;

        Defaults to ``"FIRST"`` (the behavior of python's ``statistics.mode()``)
    """
    int_mode = 0 if tiebreak == "FIRST" else 1 if tiebreak == "MAX" else 2 if tiebreak == "MIN" else -1
    if int_mode == -1:
        raise ValueError("Tiebreak field for array_mode must be one of FIRST, MAX, or MIN")
    return UnderscoreFunction(
        "array_mode", expr, int_mode, _chalk__repr_override=f'F.array_mode({expr}, tiebreak="{tiebreak}")'
    )


def array_agg(expr: Underscore | Any):
    """Extract a single-column `DataFrame` into a list of values for that column.

    Parameters
    ----------
    expr
        The expression to extract into a list.

    Examples
    --------
    >>> from datetime import datetime
    >>> import chalk.functions as F
    >>> from chalk import DataFrame
    >>> from chalk.features import _, features
    >>> @features
    >>> class Merchant:
    ...     id: str
    ...     events: "DataFrame[FraudEvent]"
    ...     fraud_codes: list[str] = F.array_agg(_.events[_.is_fraud == True, _.tag])
    >>> @features
    >>> class FraudEvent:
    ...     id: int
    ...     tag: str
    ...     is_fraud: bool
    ...     mer_id: Merchant.id
    """
    return UnderscoreFunction("array_agg", expr)


def array_join(arr: Underscore | list[Any], delimiter: str):
    """
    Concatenate the elements of an array into a single string with a delimiter.

    Parameters
    ----------
    arr
        The array to join. The values will be casted to strings if they are not already strings.
    delimiter
        The delimiter to use to join the elements of the array.

    Examples
    --------
    >>> from datetime import datetime
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    >>> class Wordle:
    ...    id: str
    ...    words: list[str]
    ...    words_str: str = F.array_join(_.words, ", ")
    """
    return UnderscoreFunction("array_join", arr, delimiter)


def element_at(arr: Underscore | list[Any], index: int | Underscore):
    """
    Returns the element of an array at the given index.

    Parameters
    ----------
    arr
        The array.
    index
        The index to extract the element from (0-indexed).

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Wordle:
    ...    id: str
    ...    words: list[str] = ["crane", "kayak", "plots", "fight", "exact", "zebra", "hello", "world"]
    ...    first_word: str = F.element_at(_.words, 0)
    """
    return UnderscoreFunction("element_at", arr, _convert_to_0_index(index))


def array_count_value(expr: Underscore, value: Union[str, Underscore]):
    """
    Returns the count of a string value in an array.

    Parameters
    ----------
    expr
        The string array.
    value
        The value to count in the array

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Bookstore:
    ...    id: str
    ...    inventory_types: list[str] = ["fiction", "non-fiction", "fiction", "fiction", "non-fiction"]
    ...    books: str = F.array_count_value(_.inventory_types, "fiction")
    """
    return UnderscoreFunction(
        "cardinality",
        UnderscoreFunction(
            "array_filter",
            expr,
            UnderscoreFunction(
                "lambda",
                "x",
                pa.large_string(),
                UnderscoreFunction("lambda_parameter", "x", pa.large_string()) == value,
            ),
        ),
    )


def array_max(arr: Underscore):
    """
    Returns the maximum value in an array.

    Parameters
    ----------
    arr
        The array to find the maximum value in.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Wordle:
    ...    id: str
    ...    words: list[str] = ["crane", "kayak", "plots", "fight", "exact", "zebra", "hello", "world"]
    ...    longest_word: str = F.array_max(_.words)
    """
    return UnderscoreFunction("array_max", arr)


def array_min(arr: Underscore):
    """
    Returns the minimum value in an array.

    Parameters
    ----------
    arr
        The array to find the minimum value in.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Wordle:
    ...    id: str
    ...    words: list[str] = ["crane", "kayak", "plots", "fight", "exact", "zebra", "hello", "world"]
    ...    shortest_word: str = F.array_min(_.words)
    """
    return UnderscoreFunction("array_min", arr)


def array_distinct(arr: Underscore):
    """
    Returns an array with distinct elements from the input array.

    Parameters
    ----------
    arr
        The array to extract distinct elements from.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    tags: list[str]
    ...    unique_tags: list[str] = F.array_distinct(_.tags)
    """
    return UnderscoreFunction("array_distinct", arr)


def contains(arr: Underscore | list[Any] | set[Any], value: Any):
    """
    Returns whether the array contains the value.

    Parameters
    ----------
    arr
        The array to check for the value.
    value
        The value to check for in the array.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class APIRequest:
    ...    id: str
    ...    headers: list[str]
    ...    has_user_agent: bool = F.contains(_.headers, "User-Agent")
    """
    return UnderscoreFunction("contains", arr, value)


def cardinality(arr: Underscore):
    """
    Returns the number of elements in an array.

    Parameters
    ----------
    arr
        The array to count the number of elements in.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Wordle:
    ...    id: str
    ...    words: list[str]
    ...    num_words: int = F.cardinality(_.words)
    """
    return UnderscoreFunction("cardinality", arr)


########################################################################################################################
# Additional Aggregations                                                                                              #
########################################################################################################################


def haversine(
    lat1: Underscore | Any,
    lon1: Underscore | Any,
    lat2: Underscore | Any,
    lon2: Underscore | Any,
    unit: Literal["degrees", "radians"] = "radians",
):
    """
    Compute the haversine distance (in kilometers) between two points on Earth. By default
    the inputs should be in radians, but alternate input units can be specified through the
    `unit` parameter.

    Parameters
    ----------
    lat1
        The latitude of the first point in radians.
    lon1
        The longitude of the first point in radians.
    lat2
        The latitude of the second point in radians.
    lon2
        The longitude of the second point in radians.
    unit:
        The unit of the input [lat1, lon1, lat2, lon2].
        The default is radians.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Location:
    ...    id: str
    ...    lat1: float
    ...    lon1: float
    ...    lat2: float
    ...    lon2: float
    ...    distance: float = F.haversine(_.lat1, _.lon1, _.lat2, _.lon2, unit="degrees")
    """
    if unit == "degrees":
        lat1 = radians(lat1)
        lon1 = radians(lon1)
        lat2 = radians(lat2)
        lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = power(sin(dlat / 2), 2) + cos(lat1) * cos(lat2) * power(sin(dlon / 2), 2)
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers.
    return if_then_else(
        is_null(lat1) | is_null(lon1) | is_null(lat2) | is_null(lon2),
        None,
        c * r,
    )


def h3_lat_lon_to_cell(
    lat: Underscore | Any,
    lon: Underscore | Any,
    resolution: Underscore | int,
    unit: Literal["degrees", "radians"] = "radians",
):
    """
    Convert latitude and longitude to an H3 cell at the specified resolution.

    Parameters
    ----------
    lat
        The latitude of the point.
    lon
        The longitude of the point.
    resolution
        The H3 resolution (integer).
    unit
        The unit of the input latitude and longitude. Either "degrees" or "radians".
        The default is "radians".

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Location:
    ...    id: str
    ...    lat: float
    ...    lon: float
    ...    h3_cell: int = F.h3_lat_lon_to_cell(_.lat, _.lon, 9, unit="degrees")
    """
    if unit == "degrees":
        lat = radians(lat)
        lon = radians(lon)

    return UnderscoreFunction("h3_lat_lon_to_cell", lat, lon, resolution)


def cast(expr: Any, dtype: pa.DataType | type[Any]):
    """Cast an expression to a different type.

    Parameters
    ----------
    expr
        The expression to cast.
    dtype
        The type to cast the expression to.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Transaction:
    ...    id: str
    ...    user_id: "User.id"
    ...    merchant_id: "Merchant.id"
    ...    user_merchant_id: "UserMerchant.id" = (
    ...        F.cast(_.user_id, str) + "_" +
    ...        F.cast(_.merchant_id, str)
    ...    )
    """
    if isinstance(dtype, type) and issubclass(dtype, Enum):
        return if_then_else(contains([member.value for member in dtype], expr), expr, None)
    return UnderscoreCast(expr, dtype if isinstance(dtype, pa.DataType) else rich_to_pyarrow(dtype, "underscore cast"))


def from_base(value: Any, base: int | Underscore):
    """Convert a number in a base to an integer.

    Parameters
    ----------
    value
        The number to convert.
    base
        The base of the number. Must be between 2 and 36.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Transaction:
    ...    id: str
    ...    base_16: str
    ...    base_10: int = F.from_base(_.base_16, 16)
    """
    if isinstance(base, int) and (base < 2 or base > 36):
        raise ValueError(f"Base must be between 2 and 36. Got {base}.")
    return UnderscoreFunction("from_base", value, base)


def round(value: Any, digits: int | None = None):
    """Round a number to the nearest integer.

    Parameters
    ----------
    value
        The number to round.
    digits
        The number of significant digits to round to. If None, the number is rounded to the nearest integer.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Transaction:
    ...    id: str
    ...    amount: float
    ...    rounded_amount: int = F.round(_.amount)
    """
    if digits is not None:
        return UnderscoreFunction("round", value, digits)
    return UnderscoreFunction("round", value)


def bankers_round(value: Any, digits: int | None = None):
    """Round a number to the nearest integer. Values exactly halfway round to the nearest even integer.

    Parameters
    ----------
    value
        The number to round.
    digits
        The number of significant digits to round to. If None, the number is banker's rounded to the nearest integer.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Transaction:
    ...    id: str
    ...    amount: float
    ...    rounded_amount: int = F.bankers_round(_.amount)
    """
    if digits is not None:
        return UnderscoreFunction("bankers_round", value, digits)
    return UnderscoreFunction("bankers_round", value)


def max(*values: Any):
    """
    Returns the maximum value in a list of values.
    This function is meant to be supplied with several
    columns, not with a single has-many or `DataFrame`.

    Input `None` values are ignored. If all inputs are `None`, then `None` is returned.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    score_1: float
    ...    score_2: float
    ...    max_score: float = F.max(_.score_1, _.score_2)
    """
    if len(values) == 0:
        return None
    if len(values) == 1:
        return values[0]
    return UnderscoreFunction(
        "scalar_max",
        values[0],
        max(*values[1:]),
        _chalk__repr_override=f"F.max({', '.join(str(value) for value in values)})",
    )


def min(*values: Any):
    """
    Returns the minimum value in a list of values.
    This function is meant to be supplied with several
    columns, not with a single has-many or `DataFrame`.

    Input `None` values are ignored. If all inputs are `None`, then `None` is returned.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    score_1: float
    ...    score_2: float
    ...    min_score: float = F.min(_.score_1, _.score_2)
    """
    if len(values) == 0:
        return None
    if len(values) == 1:
        return values[0]
    return UnderscoreFunction(
        "scalar_min",
        values[0],
        min(*values[1:]),
        _chalk__repr_override=f"F.min({', '.join(str(value) for value in values)})",
    )


def jinja(template: str):
    """
    Runs a Jinja template on the input columns.
    Supports a subset of Jinja features, specifically: variables and for loops.
    Inputs to the jinja should appear as feature fqns in the template.

    Parameters
    ----------
    template
        The Jinja template to run.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import features, DataFrame
    >>> @features
    ... class User:
    ...    id: str
    ...    score: float
    ...    transactions: "DataFrame[Transaction]"
    ...    description: str = F.jinja("User {{User.id}}. Score: {{User.score}}. Transactions: {% for txn in User.transactions %}{{txn.description}},{% endfor %}")
    """
    return UnderscoreFunction("jinja", template=template)


########################################################################################################################
# Matagg Bucket Helper Functions                                                                                       #
########################################################################################################################


def _get_chalk_bucket_n(value: Underscore, bucket_duration: str, initial_bucket_start: dt.datetime | None, n: int):
    if bucket_duration in {"all", "infinity"}:
        raise ValueError(f"Invalid bucket duration for `current_bucket_start`: {bucket_duration}")

    bucket_duration_seconds = parse_chalk_duration(bucket_duration).total_seconds()

    if bucket_duration_seconds <= 0:
        raise ValueError("Bucket duration must be greater than 0.")

    now_us = UnderscoreFunction("to_unixtime", value)
    bucket_start_us = (
        initial_bucket_start.replace(tzinfo=initial_bucket_start.tzinfo or dt.timezone.utc).timestamp()
        if initial_bucket_start
        else 0
    )
    seconds_from_start = now_us - bucket_start_us
    bucket_index = UnderscoreFunction("floor", seconds_from_start / bucket_duration_seconds)
    return bucket_index * bucket_duration_seconds + bucket_start_us + n * bucket_duration_seconds


def current_bucket_start(value: Underscore, bucket_duration: str, initial_bucket_start: dt.datetime | None = None):
    """
    Given a bucket duration, determines the start time of the currently active bucket. The currently active bucket is
    the bucket in which the feature `value` falls into. `value` should be a datetime feature and will often be
    set to `_.chalk_now`.  If `initial_bucket_start` is passed this overrides the initial bucket startime, which
    otherwise defaults to unixtime 0: 1970-01-01. This function is typically used in conjunction with materialized
    aggs.

    Parameters
    ----------
    value
        The datetime feature for which the current bucket end time is determined (likely _.chalk_now).
    initial_bucket_start
        The start time of the bucket.
    bucket_duration
        The duration of the bucket (as a chalk duration): "1d", "12h", etc.

    Examples
    --------
    >>> import chalk.functions as F
    >>> @features
    ... class MataggFeature:
    ...    id: str
    ...    current_bucket_start: float = F.current_bucket_start(_.chalk_now, "1d")
    """
    return UnderscoreFunction(
        "from_unixtime",
        _get_chalk_bucket_n(value, bucket_duration=bucket_duration, initial_bucket_start=initial_bucket_start, n=0),
    )


def current_bucket_end(value: Underscore, bucket_duration: str, initial_bucket_start: dt.datetime | None = None):
    """
    Given a bucket duration, determines the end time of the currently active bucket. The currently active bucket is
    the bucket in which the feature `value` falls into. `value` should be a datetime feature and will often be
    set to `_.chalk_now`.  If `initial_bucket_start` is passed this overrides the initial bucket startime, which
    otherwise defaults to unixtime 0: 1970-01-01. This function is typically used in conjunction with materialized
    aggs.

    Parameters
    ----------
    value
        The datetime feature for which the current bucket end time is determined (likely _.chalk_now).
    initial_bucket_start
        The start time of the bucket.
    bucket_duration
        The duration of the bucket (as a chalk duration): "1d", "12h", etc.

    Examples
    --------
    >>> import chalk.functions as F
    >>> @features
    ... class MataggFeature:
    ...    id: str
    ...    current_bucket_end: float = F.current_bucket_end(_.chalk_now, "1d")
    """
    return UnderscoreFunction(
        "from_unixtime",
        _get_chalk_bucket_n(value, bucket_duration=bucket_duration, initial_bucket_start=initial_bucket_start, n=1),
    )


def nth_bucket_start(value: Underscore, bucket_duration: str, n: int, initial_bucket_start: dt.datetime | None = None):
    """
    Given a bucket duration, determines the start time of the bucket n positions away from the currently active bucket.
    The currently active bucket is the bucket in which the feature `value` falls into. `value` should be a datetime feature and will often be
    set to `_.chalk_now`. If n is positive this will return buckets in the future and if n is negative this will return buckets in the past.
    For instance, an n of -1 will return the previous buckets start time.

    If `initial_bucket_start` is passed this overrides the initial bucket startime, which otherwise defaults to unixtime 0: 1970-01-01. This
    function is typically used in conjunction with materialized aggs.

    Parameters
    ----------
    value
        The datetime feature for which the current bucket end time is determined (likely _.chalk_now).
    initial_bucket_start
        The start time of the bucket.
    n
        The nth bucket to calculate the absolute end time for.
    bucket_duration
        The duration of the bucket (as a chalk duration): "1d", "12h", etc.

    Examples
    --------
    >>> import chalk.functions as F
    >>> import datetime as dt
    >>> @features
    ... class MataggFeature:
    ...    id: str
    ...    previous_bucket_start: dt.datetime=  F.nth_bucket_start(_.chalk_now, bucket_duration="1d", n=-1)
    """
    return UnderscoreFunction(
        "from_unixtime",
        _get_chalk_bucket_n(value, bucket_duration=bucket_duration, initial_bucket_start=initial_bucket_start, n=n),
    )


def nth_bucket_end(value: Underscore, bucket_duration: str, n: int, initial_bucket_start: dt.datetime | None = None):
    """
    Given a bucket duration, determines the end time of the bucket n positions away from the currently active bucket.
    The currently active bucket is the bucket in which the feature `value` falls into. `value` should be a datetime feature and will often be
    set to `_.chalk_now`. If n is positive this will return buckets in the future and if n is negative this will return buckets in the past.
    For instance, an n of -1 will return the previous buckets end time (which is equivalent to the current buckets start time).

    If `initial_bucket_start` is passed this overrides the initial bucket startime, which otherwise defaults to unixtime 0: 1970-01-01. This
    function is typically used in conjunction with materialized aggs.

    Parameters
    ----------
    value
        The datetime feature for which the current bucket end time is determined (likely _.chalk_now).
    bucket_duration
        The duration of the bucket (as a chalk duration): "1d", "12h", etc.
    n
        The nth bucket to calculate the absolute end time for.
    initial_bucket_start
        The start time of the bucket.

    Examples
    --------
    >>> import chalk.functions as F
    >>> @features
    ... class MataggFeature:
    ...    id: str
    ...    next_bucket_end: float = F.current_bucket_end(_.chalk_now, "1d", n=1)
    """
    return UnderscoreFunction(
        "from_unixtime",
        _get_chalk_bucket_n(value, bucket_duration=bucket_duration, initial_bucket_start=initial_bucket_start, n=1 + n),
    )


########################################################################################################################
# ML Models                                                                                                            #
########################################################################################################################


def ordinal_encode(feature: Underscore, options: list[Any], default: int | None = None) -> Underscore:
    """
    Encode a categorical feature into an ordinal integer value.

    Parameters
    ----------
    feature
        The feature to encode.
    options
        The options to encode. The order of the values determines the encoding.
        The type must be hashable, orderable and consistent with the feature
        type.
    default
        The value to use for any values not in the list of values.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...     id: str
    ...     category: str
    ...     category_ord: str = F.ordinal_encode(_.category, options=["A", "B", "C"], default_value="A")
    """
    return map_dict({v: i for i, v in enumerate(sorted(options))}, feature, default=default)


def sklearn_decision_tree_regressor(
    *features: Underscore,
    model_path: str,
):
    """
    Load scikit-learn decision tree regressor into an expression from a joblib or pickle file.

    The model must be trained on the same version of scikit-learn that is deployed in your
    Chalk environment.

    Parameters
    ----------
    features
        A list of features which were used to train the model.
    model_path
        A filepath to the scikit-learn logistic regression model.

    Examples
    --------
    >>> import chalk.functions as F
    >>> @features
    ... class User:
    ...    id: str
    ...    a: float
    ...    b: float
    ...    c: float
    ...    d: float
    ...    e: float
    ...    prediction: bool = F.sklearn_decision_tree_regressor(
    ...       _.a, _.b, _.c, _.d, _.e,
    ...       model_path=os.path.join(os.environ.get("TARGET_ROOT", "."), "models", "./dt_regressor.joblib")
    ...    )
    """
    return UnderscoreFunction(
        "decision_tree_regressor",
        *features,
        model_path=model_path,
    )


def sklearn_decision_tree_classifier(
    *features: Underscore,
    model_path: str,
    return_probability: bool = False,
    threshold: float | Underscore = 0.5,
):
    """
    Load scikit-learn decision tree classifier into an expression from a joblib or pickle file.

    The model must be trained on the same version of scikit-learn that is deployed in your
    Chalk environment.

    Only binary classification is supported.

    Parameters
    ----------
    features
        A list of features which were used to train the model.
    model_path
        A filepath to the scikit-learn logistic regression model.
    return_probability:
        Whether to return the prediction probability or the predicted class.
    threshold:
        The decision threshold for the model (ignored if probability = True).

    Examples
    --------
    >>> import chalk.functions as F
    >>> @features
    ... class User:
    ...    id: str
    ...    a: float
    ...    b: float
    ...    c: float
    ...    d: float
    ...    e: float
    ...    prediction: bool = F.sklearn_decision_tree_classifier(
    ...       _.a, _.b, _.c, _.d, _.e,
    ...       model_path=os.path.join(os.environ.get("TARGET_ROOT", "."), "models", "./dt_classifier.joblib")
    ...       probabiliy=True, threshold=0.7,
    ...    )
    """
    return UnderscoreFunction(
        "decision_tree_classifier",
        *features,
        model_path=model_path,
        return_probability=return_probability,
        threshold=threshold,
    )


def sklearn_random_forest_regressor(
    *features: Underscore,
    model_path: str,
):
    """
    Load scikit-learn random forest regressor into an expression from a joblib or pickle file.

    The model must be trained on the same version of scikit-learn that is deployed in your
    Chalk environment.

    Parameters
    ----------
    features
        A list of features which were used to train the model.
    model_path
        A filepath to the scikit-learn logistic regression model.

    Examples
    --------
    >>> import chalk.functions as F
    >>> @features
    ... class User:
    ...    id: str
    ...    a: float
    ...    b: float
    ...    c: float
    ...    d: float
    ...    e: float
    ...    prediction: float = F.sklearn_random_forest_regressor(
    ...       _.a, _.b, _.c, _.d, _.e,
    ...       model_path=os.path.join(os.environ.get("TARGET_ROOT", "."), "models", "./rf_regressor.joblib")
    ...    )
    """
    return UnderscoreFunction(
        "random_forest_regressor",
        *features,
        model_path=model_path,
    )


def sklearn_random_forest_classifier(
    *features: Underscore,
    model_path: str,
    return_probability: bool = False,
    threshold: float = 0.5,
):
    """
    Load scikit-learn random forest classifier into an expression from a joblib or pickle file.

    The model must be trained on the same version of scikit-learn that is deployed in your
    Chalk environment.

    Only binary classification is supported.

    Parameters
    ----------
    features
        A list of features which were used to train the model.
    model_path
        A filepath to the scikit-learn logistic regression model.
    return_probability:
        Whether to return the prediction probability or the predicted class.
    threshold:
        The decision threshold for the model (ignored if probability = True).

    Examples
    --------
    >>> import chalk.functions as F
    >>> @features
    ... class User:
    ...    id: str
    ...    a: float
    ...    b: float
    ...    c: float
    ...    d: float
    ...    e: float
    ...    prediction: float = F.sklearn_random_forest_classifier(
    ...       _.a, _.b, _.c, _.d, _.e,
    ...       model_path=os.path.join(os.environ.get("TARGET_ROOT", "."), "models", "./rf_classifier.joblib"),
    ...       probabiliy=True, threshold=0.7,
    ...    )
    """
    return UnderscoreFunction(
        "random_forest_classifier",
        *features,
        model_path=model_path,
        return_probability=return_probability,
        threshold=threshold,
    )


def sklearn_gradient_boosting_regressor(
    *features: Underscore,
    model_path: str,
):
    """
    Load scikit-learn gradient boosting regressor into an expression from a joblib or pickle file.

    The model must be trained on the same version of scikit-learn that is deployed in your
    Chalk environment.

    Parameters
    ----------
    features
        A list of features which were used to train the model.
    model_path
        A filepath to the scikit-learn logistic regression model.

    Examples
    --------
    >>> import chalk.functions as F
    >>> @features
    ... class User:
    ...    id: str
    ...    a: float
    ...    b: float
    ...    c: float
    ...    d: float
    ...    e: float
    ...    prediction: float = F.sklearn_gradient_boosting_regressor(
    ...       _.a, _.b, _.c, _.d, _.e,
    ...       model_path=os.path.join(os.environ.get("TARGET_ROOT", "."), "models", "./gb_regressor.joblib"),
    ...    )
    """
    return UnderscoreFunction(
        "gradient_boosting_regressor",
        *features,
        model_path=model_path,
    )


def sklearn_logistic_regression(
    *features: Underscore,
    model_path: str,
    return_probability: bool = False,
    threshold: float | Underscore = 0.5,
):
    """
    Load scikit-learn logistic regression into an expression from a joblib or pickle file.

    The model must be trained on the same version of scikit-learn that is deployed in your
    Chalk environment.

    Only binary classification is supported.

    Parameters
    ----------
    features
        A list of features which were used to train the model.
    model_path
        A filepath to the scikit-learn logistic regression model.
    return_probability:
        Whether to return the prediction probability or the predicted class.
    threshold:
        The decision threshold for the model (ignored if probability = True).

    Examples
    --------
    >>> import chalk.functions as F
    >>> @features
    ... class User:
    ...    id: str
    ...    a: float
    ...    b: float
    ...    c: float
    ...    d: float
    ...    e: float
    ...    prediction: float = F.sklearn_logistic_regression(
    ...       _.a, _.b, _.c, _.d, _.e,
    ...       model_path=os.path.join(os.environ.get("TARGET_ROOT", "."), "models", "./logistic.joblib"),
    ...       probabiliy=True, threshold=0.7,
    ...    )
    """
    return UnderscoreFunction(
        "logistic_regression",
        *features,
        model_path=model_path,
        return_probability=return_probability,
        threshold=threshold,
    )


def xgboost_regressor(
    *features: Underscore,
    model_path: str,
):
    """
    Load xgboost regressor into an expression from a joblib or pickle file.

    The model must be trained on the same version of xgboost that is deployed in your
    Chalk environment. The joblib dependency also needs to be included in your
    python requirements.

    Currently, only non-null float features are supported.

    Parameters
    ----------
    features
        A list of the features which were used to train the model.
    model_path
        A filepath to the xgboost resgressor model.

    Examples
    --------
    >>> import chalk.functions as F
    >>> @features
    ... class User:
    ...    id: str
    ...    a: float
    ...    b: float
    ...    c: float
    ...    d: float
    ...    e: float
    ...    prediction: float = F.xgboost_regressor(
    ...       _.a, _.b, _.c, _.d, _.e,
    ...       model_path=os.path.join(os.environ.get("TARGET_ROOT", "."), "models", "./xgb_regressor.joblib"),
    ...    )
    """
    return UnderscoreFunction(
        "xgb_regressor",
        *features,
        model_path=model_path,
    )


def random(n: int | None = None):
    """
    Generate a random number.

    If no arguments are provided, a random float between `[0.0, 1.0)` is returned.
    If `n` is provided, a random integer between `[0, n)` is returned.

    Parameters
    ----------
    n
        The upper bound for the random integer. If `None`, a random float is returned.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class RandomExample:
    ...    id: int
    ...    random_float: float = F.random()
    ...    random_int_bounded: int = F.random(10)
    """
    if n is None:
        return UnderscoreFunction("random")
    return UnderscoreFunction("random", n)


def between(value: Underscore | Any, low: Underscore | Any, high: Underscore | Any):
    """
    Check if a value is between two bounds (inclusive).

    Parameters
    ----------
    value
        The value to check.
    low
        The lower bound (inclusive).
    high
        The upper bound (inclusive).

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class RiskAssessment:
    ...    id: str
    ...    score: float
    ...    is_moderate_risk: bool = F.between(_.score, 0.3, 0.7)
    """
    return UnderscoreFunction("between", value, low, high)


def distinct_from(value1: Underscore | Any, value2: Underscore | Any):
    """
    Check if two values are distinct from each other (including null semantics).

    Parameters
    ----------
    value1
        First value to compare.
    value2
        Second value to compare.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class DataComparison:
    ...    id: str
    ...    current_value: float | None
    ...    previous_value: float | None
    ...    has_changed: bool = F.distinct_from(_.current_value, _.previous_value)
    """
    return UnderscoreFunction("distinct_from", value1, value2)


def secure_random(min_val: Any = None, max_val: Any = None):
    """
    Generate a cryptographically secure random number.

    If no arguments are provided, a random float between `[0.0, 1.0)` is returned.
    If two arguments are provided, a random number between `[min_val, max_val)` is returned.

    Parameters
    ----------
    min_val
        The minimum bound for the random number. If `None`, returns float in [0.0, 1.0).
    max_val
        The maximum bound for the random number. Required if min_val is provided.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class SecurityToken:
    ...    id: str
    ...    token_seed: float = F.secure_random()
    ...    random_score: int = F.secure_random(1, 100)
    """
    if min_val is None and max_val is None:
        return UnderscoreFunction("secure_random")
    elif min_val is not None and max_val is not None:
        return UnderscoreFunction("secure_random", min_val, max_val)
    else:
        raise ValueError("Both min_val and max_val must be provided together")


########################################################################################################################
# Bitwise Functions                                                                                                   #
########################################################################################################################


def bitwise_and(left: Underscore, right: Underscore):
    """
    Perform bitwise AND operation on two integer values.

    Parameters
    ----------
    left
        The left integer operand.
    right
        The right integer operand.

    Returns
    -------
    The result of bitwise AND operation.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class PermissionCheck:
    ...     id: str
    ...     user_permissions: int
    ...     required_permissions: int
    ...     has_permission: int = F.bitwise_and(_.user_permissions, _.required_permissions)
    """
    return UnderscoreFunction("bitwise_and", left, right)


def bitwise_arithmetic_shift_right(value: Underscore, shift: Underscore):
    """
    Perform arithmetic right bit shift operation on an integer value.
    Preserves the sign bit by filling with the sign bit.

    Parameters
    ----------
    value
        The integer value to shift.
    shift
        The number of positions to shift right.

    Returns
    -------
    The result of arithmetic right shift operation.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class DataCompression:
    ...     id: str
    ...     encoded_value: int
    ...     level_shift: int
    ...     decoded_value: int = F.bitwise_arithmetic_shift_right(_.encoded_value, _.level_shift)
    """
    return UnderscoreFunction("bitwise_arithmetic_shift_right", value, shift)


def bitwise_not(value: Underscore):
    """
    Perform bitwise NOT operation on an integer value (one's complement).

    Parameters
    ----------
    value
        The integer value to invert.

    Returns
    -------
    The result of bitwise NOT operation.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class FeatureToggle:
    ...     id: str
    ...     enabled_features: int
    ...     disabled_features: int = F.bitwise_not(_.enabled_features)
    """
    return UnderscoreFunction("bitwise_not", value)


def bitwise_or(left: Underscore, right: Underscore):
    """
    Perform bitwise OR operation on two integer values.

    Parameters
    ----------
    left
        The left integer operand.
    right
        The right integer operand.

    Returns
    -------
    The result of bitwise OR operation.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class PermissionMerge:
    ...     id: str
    ...     base_permissions: int
    ...     additional_permissions: int
    ...     combined_permissions: int = F.bitwise_or(_.base_permissions, _.additional_permissions)
    """
    return UnderscoreFunction("bitwise_or", left, right)


def bitwise_xor(left: Underscore, right: Underscore):
    """
    Perform bitwise XOR operation on two integer values.

    Parameters
    ----------
    left
        The left integer operand.
    right
        The right integer operand.

    Returns
    -------
    The result of bitwise XOR operation.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class DataEncryption:
    ...     id: str
    ...     plaintext: int
    ...     encryption_key: int
    ...     ciphertext: int = F.bitwise_xor(_.plaintext, _.encryption_key)
    """
    return UnderscoreFunction("bitwise_xor", left, right)


def bitwise_left_shift(value: Underscore, shift: Underscore):
    """
    Perform left bit shift operation on an integer value.

    Parameters
    ----------
    value
        The integer value to shift.
    shift
        The number of positions to shift left.

    Returns
    -------
    The result of left shift operation.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class BinaryOperations:
    ...     id: str
    ...     base_value: int
    ...     shift_amount: int
    ...     shifted_value: int = F.bitwise_left_shift(_.base_value, _.shift_amount)
    """
    return UnderscoreFunction("bitwise_left_shift", value, shift)


def bitwise_right_shift(value: Underscore, shift: Underscore):
    """
    Perform logical right bit shift operation on an integer value.

    Parameters
    ----------
    value
        The integer value to shift.
    shift
        The number of positions to shift right.

    Returns
    -------
    The result of logical right shift operation.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class BinaryOperations:
    ...     id: str
    ...     base_value: int
    ...     shift_amount: int
    ...     shifted_value: int = F.bitwise_right_shift(_.base_value, _.shift_amount)
    """
    return UnderscoreFunction("bitwise_right_shift", value, shift)


########################################################################################################################
# Array Functions                                                                                                     #
########################################################################################################################


def array_cum_sum(array: Underscore):
    """
    Calculate cumulative sum of array elements.

    Parameters
    ----------
    array
        The numeric array to calculate cumulative sum for.

    Returns
    -------
    Array where each element is the sum of all preceding elements including itself.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class MetricsAnalysis:
    ...     id: str
    ...     daily_revenues: list[float]
    ...     cumulative_revenues: list[float] = F.array_cum_sum(_.daily_revenues)
    """
    return UnderscoreFunction("array_cum_sum", array)


def array_duplicates(array: Underscore):
    """
    Returns duplicate elements in the array.

    Parameters
    ----------
    array
        The array to find duplicates in.

    Returns
    -------
    Array containing all duplicate elements.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class CustomerAnalysis:
    ...     id: str
    ...     purchase_categories: list[str]
    ...     repeat_categories: list[str] = F.array_duplicates(_.purchase_categories)
    """
    return UnderscoreFunction("array_duplicates", array)


def array_except(left_array: Underscore, right_array: Underscore):
    """
    Returns elements in left array that are not in right array.

    Parameters
    ----------
    left_array
        The array to subtract from.
    right_array
        The array containing elements to remove.

    Returns
    -------
    Array containing elements from left_array not present in right_array.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class FeatureComparison:
    ...     id: str
    ...     all_features: list[str]
    ...     active_features: list[str]
    ...     disabled_features: list[str] = F.array_except(_.all_features, _.active_features)
    """
    return UnderscoreFunction("array_except", left_array, right_array)


def array_has_duplicates(array: Underscore):
    """
    Checks if the array contains duplicate elements.

    Parameters
    ----------
    array
        The array to check for duplicates.

    Returns
    -------
    True if the array contains duplicates, False otherwise.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class DataQuality:
    ...     id: str
    ...     user_ids: list[int]
    ...     has_duplicate_users: bool = F.array_has_duplicates(_.user_ids)
    """
    return UnderscoreFunction("array_has_duplicates", array)


def array_intersect(left_array: Underscore, right_array: Underscore):
    """
    Returns common elements between two arrays.

    Parameters
    ----------
    left_array
        The first array.
    right_array
        The second array.

    Returns
    -------
    Array containing elements present in both arrays.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class CustomerSegmentation:
    ...     id: str
    ...     current_interests: list[str]
    ...     past_purchases: list[str]
    ...     relevant_interests: list[str] = F.array_intersect(_.current_interests, _.past_purchases)
    """
    return UnderscoreFunction("array_intersect", left_array, right_array)


def array_normalize(array: Underscore):
    """
    Normalize array values so they sum to 1.

    Parameters
    ----------
    array
        The numeric array to normalize.

    Returns
    -------
    Array where each element is divided by the sum of all elements.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class ProbabilityModel:
    ...     id: str
    ...     raw_scores: list[float]
    ...     probabilities: list[float] = F.array_normalize(_.raw_scores)
    """
    return UnderscoreFunction("array_normalize", array)


def array_position(array: Underscore, element: Underscore):
    """
    Find the position of an element in the array (1-based indexing).

    Parameters
    ----------
    array
        The array to search in.
    element
        The element to find.

    Returns
    -------
    1-based position of the element, or 0 if not found.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class RankingAnalysis:
    ...     id: str
    ...     ranked_products: list[str]
    ...     target_product: str
    ...     product_rank: int = F.array_position(_.ranked_products, _.target_product)
    """
    return UnderscoreFunction("array_position", array, element)


def array_remove(array: Underscore, element: Underscore):
    """
    Remove all occurrences of an element from the array.

    Parameters
    ----------
    array
        The array to remove elements from.
    element
        The element to remove.

    Returns
    -------
    Array with all occurrences of element removed.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class DataCleaning:
    ...     id: str
    ...     transaction_types: list[str]
    ...     filtered_types: list[str] = F.array_remove(_.transaction_types, "test")
    """
    return UnderscoreFunction("array_remove", array, element)


def arrays_overlap(left_array: Underscore, right_array: Underscore):
    """
    Check if two arrays have common elements.

    Parameters
    ----------
    left_array
        The first array.
    right_array
        The second array.

    Returns
    -------
    True if arrays have at least one common element, False otherwise.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class UserCompatibility:
    ...     id: str
    ...     user_interests: list[str]
    ...     recommended_interests: list[str]
    ...     has_overlap: bool = F.arrays_overlap(_.user_interests, _.recommended_interests)
    """
    return UnderscoreFunction("arrays_overlap", left_array, right_array)


def flatten(array: Underscore):
    """
    Flatten nested arrays into a single-level array.

    Parameters
    ----------
    array
        The nested array to flatten.

    Returns
    -------
    Single-level array containing all elements from nested arrays.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class DataProcessing:
    ...     id: str
    ...     nested_categories: list[list[str]]
    ...     all_categories: list[str] = F.flatten(_.nested_categories)
    """
    return UnderscoreFunction("flatten", array)


def remove_nulls(array: Underscore):
    """
    Remove all null values from the array.

    Parameters
    ----------
    array
        The array to remove nulls from.

    Returns
    -------
    Array with all null values removed.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class DataCleaning:
    ...     id: str
    ...     raw_scores: list[float | None]
    ...     clean_scores: list[float] = F.remove_nulls(_.raw_scores)
    """
    return UnderscoreFunction("remove_nulls", array)


def sequence(start: Underscore | int, stop: Underscore | int, step: Underscore | int = 1):
    """
    Generate a sequence of integers.

    Parameters
    ----------
    start
        The starting value (inclusive).
    stop
        The ending value (inclusive).
    step
        The increment between values (default: 1).

    Returns
    -------
    Array of integers from start to stop.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class IndexGeneration:
    ...     id: str
    ...     batch_size: int
    ...     indices: list[int] = F.sequence(1, _.batch_size)
    """
    if step == 1:
        return UnderscoreFunction("sequence", start, stop)
    return UnderscoreFunction("sequence", start, stop, step)


def shuffle(array: Underscore):
    """
    Randomly shuffle array elements.

    Parameters
    ----------
    array
        The array to shuffle.

    Returns
    -------
    Array with elements in random order.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class RecommendationSystem:
    ...     id: str
    ...     product_list: list[str]
    ...     shuffled_recommendations: list[str] = F.shuffle(_.product_list)
    """
    return UnderscoreFunction("shuffle", array)


__all__ = (
    "DayOfWeek",
    "Then",
    "When",
    "abs",
    "acos",
    "array_agg",
    "array_average",
    "array_count_value",
    "array_cum_sum",
    "array_distinct",
    "array_duplicates",
    "array_except",
    "array_has_duplicates",
    "array_intersect",
    "array_join",
    "array_max",
    "array_median",
    "array_min",
    "array_mode",
    "array_normalize",
    "array_position",
    "array_remove",
    "array_sample_stddev",
    "array_sort",
    "array_stddev",
    "array_sum",
    "arrays_overlap",
    "asin",
    "bankers_round",
    "between",
    "bitwise_and",
    "bitwise_arithmetic_shift_right",
    "bitwise_left_shift",
    "bitwise_not",
    "bitwise_or",
    "bitwise_right_shift",
    "bitwise_xor",
    "bytes_to_string",
    "cardinality",
    "cast",
    "ceil",
    "chr",
    "clamp",
    "coalesce",
    "contains",
    "cos",
    "cosine_similarity",
    "current_bucket_end",
    "current_bucket_start",
    "date_trunc",
    "day",
    "day_of_month",
    "day_of_week",
    "day_of_year",
    "distinct_from",
    "e",
    "element_at",
    "ends_with",
    "exp",
    "flatten",
    "floor",
    "format_datetime",
    "from_base",
    "from_big_endian_32",
    "from_big_endian_64",
    "from_iso8601_timestamp",
    "from_unix_milliseconds",
    "from_unix_seconds",
    "greatest",
    "gunzip",
    "haversine",
    "head",
    "hour_of_day",
    "http_delete",
    "http_get",
    "http_post",
    "http_put",
    "http_request",
    "h3_lat_lon_to_cell",
    "if_then_else",
    "is_leap_year",
    "is_month_end",
    "is_null",
    "is_us_federal_holiday",
    "jaccard_similarity",
    "jaro_winkler_distance",
    "jinja",
    "json_extract_array",
    "json_value",
    "last_day_of_month",
    "least",
    "length",
    "levenshtein_distance",
    "like",
    "ln",
    "log2",
    "log10",
    "lower",
    "lpad",
    "ltrim",
    "map_dict",
    "map_get",
    "max",
    "max_by",
    "max_by_n",
    "md5",
    "min",
    "min_by",
    "min_by_n",
    "mod",
    "month_of_year",
    "normal_cdf",
    "nth_bucket_end",
    "nth_bucket_start",
    "parse_datetime",
    "partial_ratio",
    "pi",
    "power",
    "proto_deserialize",
    "proto_serialize",
    "quarter",
    "radians",
    "rand",
    "random",
    "recover",
    "remove_nulls",
    "regexp_extract",
    "regexp_extract_all",
    "regexp_like",
    "regexp_replace",
    "replace",
    "reverse",
    "round",
    "rpad",
    "rtrim",
    "safe_divide",
    "sagemaker_predict",
    "secure_random",
    "sequence",
    "sequence_matcher_ratio",
    "shuffle",
    "sha1",
    "sha256",
    "sha512",
    "sigmoid",
    "sin",
    "sklearn_decision_tree_classifier",
    "sklearn_decision_tree_regressor",
    "sklearn_gradient_boosting_regressor",
    "sklearn_logistic_regression",
    "sklearn_random_forest_classifier",
    "sklearn_random_forest_regressor",
    "slice",
    "split",
    "split_part",
    "spooky_hash_v2_32",
    "spooky_hash_v2_64",
    "sqrt",
    "starts_with",
    "string_to_bytes",
    "strpos",
    "strrpos",
    "struct_pack",
    "substr",
    "to_base",
    "to_iso8601",
    "token_set_ratio",
    "token_sort_ratio",
    "total_seconds",
    "trim",
    "unidecode_normalize",
    "unidecode_to_ascii",
    "unix_milliseconds",
    "unix_seconds",
    "upper",
    "url_extract_host",
    "url_extract_path",
    "url_extract_protocol",
    "week_of_year",
    "when",
    "width_bucket",
    "word_stem",
    "xgboost_regressor",
    "year",
)
