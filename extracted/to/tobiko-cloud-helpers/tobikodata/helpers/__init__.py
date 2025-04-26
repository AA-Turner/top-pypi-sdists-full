from __future__ import annotations

import itertools
import random
import re
import string
import sys
import traceback
import typing as t
import uuid
from collections.abc import Collection
from typing import Iterable, Iterator

T = t.TypeVar("T")
ALPHANUMERIC = string.ascii_lowercase + string.digits


def seq_get(seq: t.Sequence[T], index: int) -> t.Optional[T]:
    """Returns the value in `seq` at position `index`, or `None` if `index` is out of bounds."""
    try:
        return seq[index]
    except IndexError:
        return None


@t.overload
def ensure_list(value: t.Collection[T]) -> t.List[T]: ...


@t.overload
def ensure_list(value: T) -> t.List[T]: ...


def ensure_list(value: t.Union[T, t.Collection[T]]) -> t.List[T]:
    """
    Ensures that a value is a list, otherwise casts or wraps it into one.

    Args:
        value: The value of interest.

    Returns:
        The value cast as a list if it's a list or a tuple, or else the value wrapped in a list.
    """
    if value is None:
        return []
    if isinstance(value, (list, tuple)):
        return list(value)

    return [t.cast(T, value)]


@t.overload
def ensure_collection(value: t.Collection[T]) -> t.Collection[T]: ...


@t.overload
def ensure_collection(value: T) -> t.Collection[T]: ...


def ensure_collection(value: t.Union[T, t.Collection[T]]) -> t.Collection[T]:
    """
    Ensures that a value is a collection (excluding `str` and `bytes`), otherwise wraps it into a list.

    Args:
        value: The value of interest.

    Returns:
        The value if it's a collection, or else the value wrapped in a list.
    """
    if value is None:
        return []

    if isinstance(value, Collection) and not isinstance(value, (str, bytes)):
        return value

    return [t.cast(T, value)]


def first(it: t.Iterable[T]) -> T:
    """Returns the first element from an iterable (useful for sets)."""
    return next(i for i in it)


def major_minor_patch_dev(version: str) -> t.Tuple[int, int, int, int]:
    """Returns a tuple of the major.minor.patch.dev (dev is optional) for a version string (major.minor.patch-devXXX)."""
    version = version.split("+")[0]
    version_parts = version.split(".")
    # Check for legacy major.minor.patch.devXX format
    if len(version_parts) not in (3, 4):
        raise ValueError(f"Invalid version: {version}")
    if len(version_parts) == 4:
        major, minor, patch, dev = version_parts
        dev = dev.replace("dev", "")
    else:
        major, minor, patch = version_parts[0:3]
        dev_info = patch.split("-")
        if len(dev_info) == 1:
            patch, dev = patch, sys.maxsize  # type: ignore
        else:
            patch, dev = dev_info  # type: ignore
            dev = dev.replace("dev", "")  # type: ignore
    return t.cast(
        t.Tuple[int, int, int, int],
        tuple(int(part) for part in [major, minor, patch, dev]),  # type: ignore
    )


def share_major_minor_dev(version: str, new_version: str) -> bool:
    old_major, old_minor, _, old_dev = major_minor_patch_dev(version)
    new_major, new_minor, _, new_dev = major_minor_patch_dev(new_version)

    return old_major == new_major and old_minor == new_minor and old_dev == new_dev


def urljoin(*args: str) -> str:
    from urllib.parse import urljoin, uses_netloc, uses_relative

    if "oci" not in uses_relative:
        uses_relative.append("oci")

    if "oci" not in uses_netloc:
        uses_netloc.append("oci")

    if not args:
        return ""

    if len(args) == 1:
        return args[0]
    base = args[0]
    for part in args[1:]:
        if base:
            base = base.rstrip("/") + "/"
            part = part.lstrip("/")
        base = urljoin(base, part)

    return base


def str_to_bool(s: t.Optional[str]) -> bool:
    """
    Convert a string to a boolean. disutils is being deprecated and it is recommended to implement your own version:
    https://peps.python.org/pep-0632/

    Unlike disutils, this actually returns a bool and never raises. If a value cannot be determined to be true
    then false is returned.
    """
    if not s:
        return False
    return s.lower() in ("true", "1", "t", "y", "yes", "on")


def random_id(short: bool = False) -> str:
    if short:
        return "".join(random.choices(ALPHANUMERIC, k=8))

    return uuid.uuid4().hex


def format_exception(exception: BaseException) -> t.List[str]:
    if sys.version_info < (3, 10):
        return traceback.format_exception(type(exception), exception, exception.__traceback__)  # type: ignore
    else:
        return traceback.format_exception(exception)  # type: ignore


def get_base_package(requirement_string: str) -> t.Optional[str]:
    """
    Extract the base package name from a requirement string (removes version and extras)
    """
    match = re.match(r"^[a-zA-Z0-9_.\-]+", requirement_string)
    return match.group(0) if match else None


def batched(iterable: Iterable[T], n: int) -> Iterator[tuple[T, ...]]:
    """Reimplementation of itertools.batched introduced in Python 3.12.

    batched('ABCDEFG', 3) --> ABC DEF G
    """
    if n < 1:
        raise ValueError("n must be at least one")
    it = iter(iterable)
    while True:
        batch = tuple(itertools.islice(it, n))
        if not batch:
            break
        yield batch
