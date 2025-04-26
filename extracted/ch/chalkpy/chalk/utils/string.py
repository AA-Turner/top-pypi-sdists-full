from __future__ import annotations

import re
from datetime import timedelta
from typing import Collection, Iterable, List

_snake_sub_1 = re.compile("(.)([A-Z][a-z]+)")
_snake_sub_2 = re.compile("__([A-Z])")
_snake_sub_3 = re.compile("([a-z0-9])([A-Z])")


def to_snake_case(name: str):
    name = _snake_sub_1.sub(r"\1_\2", name)
    name = _snake_sub_2.sub(r"_\1", name)
    name = _snake_sub_3.sub(r"\1_\2", name)
    return name.lower()


def comma_whitespace_split(value: str):
    return re.split(r"\s*,\s*", value)


def comma_join(value: Iterable[str]):
    return ",".join(value)


_matching_re = re.compile(r"[^0-9a-z]")


def normalize_string_for_matching(name: str) -> str:
    """
    1. Case-insensitive
    2. Strip everything except alphanumeric, so e.g. `first_name` matches `firstname`
    """
    return _matching_re.sub("", name.lower())


def to_camel_case(snake_str: str) -> str:
    components = tuple(c for c in snake_str.split("_") if c != "")
    return components[0].lower() + "".join(x.title() for x in components[1:])


def to_title_case(snake_str: str):
    cameled = to_camel_case(snake_str)
    return cameled[0].upper() + cameled[1:] if len(cameled) > 0 else cameled


def oxford_comma_list(
    lst: Iterable[str],
    quoted: bool = False,
    quote_char: str = "'",
) -> str:
    lst_l = add_quotes(lst, quot_char=quote_char) if quoted else tuple(lst)
    len_l = len(lst_l)
    if len_l == 0:
        return ""
    elif len_l == 1:
        return lst_l[0]
    elif len_l == 2:
        return f"{lst_l[0]} and {lst_l[1]}"
    return ", ".join(lst_l[:-1]) + f", and {lst_l[-1]}"


def add_quotes(lst: Iterable[str], quot_char: str = "'") -> List[str]:
    return [f"{quot_char}{x}{quot_char}" for x in lst]


def double_quoted(s: str) -> str:
    return f'"{s}"'


def single_quoted(s: str) -> str:
    return f"'{s}'"


def double_quoted_list(lst: Iterable[str]) -> str:
    return ", ".join(map(double_quoted, lst))


def single_quoted_list(lst: Iterable[str]) -> str:
    return ", ".join(map(single_quoted, lst))


def to_bool(name: str, val: str | bool):
    if isinstance(val, bool):
        return val
    if val.lower() in ("yes", "y", "1", "true", "t"):
        return True
    if val.lower() in ("no", "no", "0", "false", "f"):
        return False
    raise ValueError(f"{name} must be 'yes' or 'no'")


def resolver_name(fqn: str) -> str:
    return fqn.split(".")[-1]


def matches_regex(string: str, regex: str) -> bool:
    pattern = re.compile(regex)
    return pattern.match(string) is not None


def in_regex_set(string: str | None, regex_set: Collection[str]) -> bool:
    if string is None:
        return False
    """Returns true if string is not None and in regex set"""
    return any(matches_regex(string, regex) for regex in regex_set)


def pluralize(word: str, items: Iterable[str]) -> str:
    items_l = sorted(items)
    if len(items_l) == 0:
        return f"no {word}s"
    elif len(items_l) == 1:
        return f"{word} '{items_l[0]}'"
    elif len(items_l) == 2:
        return f"{word}s '{items_l[0]}' and '{items_l[1]}'"

    content = ", '".join(items_l[:-1])
    return f"{word}s '{content}', and '{items_l[-1]}'"


def s(length: int):
    """
    Returns an "s" if 0-count or plural.
    Helps Chalk attain perfect grammar.

    :param length: Length of variable being described.
    :return: Empty string or "s".
    """
    return "" if length == 1 else "s"


def readable_duration(td: timedelta) -> str:
    seconds = int(td.total_seconds())
    milliseconds = int((td.microseconds / 1000000) * 1000)
    weeks, remainder = divmod(seconds, 604800)
    days, remainder = divmod(remainder, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    duration = []
    if weeks > 0:
        duration.append(f"{weeks} week{s(weeks)}")
    if days > 0:
        duration.append(f"{days} day{s(days)}")
    if hours > 0:
        duration.append(f"{hours} hour{s(hours)}")
    if minutes > 0:
        duration.append(f"{minutes} minute{s(minutes)}")
    if seconds > 0:
        duration.append(f"{seconds} second{s(seconds)}")
    if milliseconds > 0:
        duration.append(f"{milliseconds} millisecond{s(milliseconds)}")
    return " ".join(duration)
