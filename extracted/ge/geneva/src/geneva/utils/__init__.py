# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

# dumping ground for utility functions
from __future__ import annotations

import contextlib
import datetime
import functools
import getpass
import logging
import os
import threading
from contextlib import contextmanager
from typing import TYPE_CHECKING, TypeVar

import pyarrow as pa
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential_jitter,
)

if TYPE_CHECKING:
    from collections.abc import Callable, Iterator

_LOG = logging.getLogger(__name__)

F = TypeVar("F", bound="Callable[..., object]")

RETRY_LANCE_ATTEMPTS = int(os.environ.get("GENEVA_RETRY_LANCE_ATTEMPTS", "7"))
RETRY_LANCE_INITIAL_SECS = float(
    os.environ.get("GENEVA_RETRY_LANCE_INITIAL_SECS", "0.5")
)
RETRY_LANCE_MAX_SECS = float(os.environ.get("GENEVA_RETRY_LANCE_MAX_SECS", "120.0"))


def _should_retry_lance_runtime_error(exception: BaseException) -> bool:
    """Check if RuntimeError is a known retryable Lance error.

    Covers both:
      - "Too many concurrent writers" — Lance backpressure on commit fan-in.
      - "lance error: Retryable" — Lance's RetryableCommitConflict variant,
        which the conflict resolver explicitly tags for caller retry (e.g.
        Merge preempted by concurrent Delete at the same version).
    """
    if not isinstance(exception, RuntimeError):
        return False
    msg = str(exception)
    return "Too many concurrent writers" in msg or "lance error: Retryable" in msg


def retry_lance(fn: F) -> F:
    """
    Tenacity retry for Lance/GCS I/O:
      - Exceptions: OSError, ValueError, RuntimeError("Too many concurrent
        writers"), RuntimeError("lance error: Retryable ...").
      - Attempts: 7 total
      - Backoff: exponential with full jitter (0.5s .. 20s)
      - Logs: warning before each retry, error on final failure
    """
    # TODO make OSError and ValueError exception retrys more precise.
    wrapped = retry(
        retry=(
            retry_if_exception_type((OSError, ValueError))
            | retry_if_exception(_should_retry_lance_runtime_error)
        ),
        wait=wait_exponential_jitter(
            initial=RETRY_LANCE_INITIAL_SECS, max=RETRY_LANCE_MAX_SECS
        ),
        stop=stop_after_attempt(RETRY_LANCE_ATTEMPTS),
        reraise=True,
        before_sleep=before_sleep_log(_LOG, logging.WARNING),
    )(fn)

    @functools.wraps(fn)
    def wrapper(*args, **kwargs) -> object:
        try:
            return wrapped(*args, **kwargs)
        except Exception:
            _LOG.error(
                "%r failed after %d attempts; giving up.",
                fn.__qualname__,
                RETRY_LANCE_ATTEMPTS,
                exc_info=True,
            )
            raise

    return wrapper  # type: ignore[return-value]


def parse_data_storage_version(version: str) -> tuple[int, int]:
    """Parse a data_storage_version string like '2.0' into (major, minor)."""
    major, minor = version.split(".")
    return int(major), int(minor)


def dt_now_utc() -> datetime.datetime:
    """Return the current UTC datetime."""
    return datetime.datetime.now(datetime.timezone.utc)


def current_user() -> str:
    """Return the current user"""
    return getpass.getuser()


def redact_dict_values(d: dict[str, object] | None) -> str:
    """Redact sensitive dictionary values for logging.

    Shows keys but replaces all values with '[REDACTED]' to prevent
    credentials from leaking into logs and repr output.
    """
    if d is None:
        return "None"
    return "{" + ", ".join(f"'{k}': '[REDACTED]'" for k in d) + "}"


def escape_sql_string(value: str) -> str:
    """Escape a string value for safe use in SQL WHERE clauses.

    Uses SQL standard escaping (doubling single quotes) to prevent SQL injection.
    This should be used when constructing SQL WHERE clauses with user-provided strings.

    Parameters
    ----------
    value : str
        The string value to escape

    Returns
    -------
    str
        The escaped string value

    Examples
    --------
    >>> escape_sql_string("test'OR'1'='1")
    "test''OR''1''=''1"
    >>> escape_sql_string("normal_string")
    "normal_string"
    """
    # Escape single quotes by doubling them (SQL standard)
    return value.replace("'", "''")


class _PeriodicCaller(threading.Thread):
    def __init__(self, fn: Callable[[], None], interval_secs: float) -> None:
        super().__init__(daemon=True)
        self._fn = fn
        self._interval = interval_secs
        self._stop_evt = threading.Event()

    def stop(self) -> None:
        self._stop_evt.set()

    def run(self) -> None:
        # call once immediately for quick “proof of life”, then on the cadence
        with contextlib.suppress(Exception):
            self._fn()

        while not self._stop_evt.wait(self._interval):
            with contextlib.suppress(Exception):
                self._fn()


@contextmanager
def status_updates(
    get_status: Callable[[], None], interval_secs: float
) -> Iterator[None]:
    t = _PeriodicCaller(get_status, interval_secs)
    t.start()
    try:
        yield
    finally:
        t.stop()
        t.join(timeout=5)


def deep_merge(base: dict, override: dict) -> dict:
    """Deep merge two dictionaries, with override taking precedence.

    Recursively merges nested dictionaries. For lists, appends override items to base.
    For other types, override values replace base values.

    Parameters
    ----------
    base : dict
        The base dictionary to merge into
    override : dict
        The dictionary containing values to merge/override

    Returns
    -------
    dict
        A new dictionary with merged values

    Examples
    --------
    >>> base = {"a": 1, "b": {"c": 2, "d": 3}}
    >>> override = {"b": {"d": 4, "e": 5}, "f": 6}
    >>> deep_merge(base, override)
    {'a': 1, 'b': {'c': 2, 'd': 4, 'e': 5}, 'f': 6}

    >>> base = {"containers": [{"name": "ray", "image": "ray:2.54.0"}]}
    >>> override = {"containers": [{"env": [{"name": "FOO", "value": "bar"}]}]}
    >>> result = deep_merge(base, override)
    >>> len(result["containers"])
    2
    """
    result = base.copy()

    for key, override_value in override.items():
        if key not in result:
            # Key only in override, add it
            result[key] = override_value
        elif isinstance(result[key], dict) and isinstance(override_value, dict):
            # Both are dicts, recurse
            result[key] = deep_merge(result[key], override_value)
        elif isinstance(result[key], list) and isinstance(override_value, list):
            # Both are lists, append override items to base
            result[key] = result[key] + override_value
        else:
            # Override replaces base for other types or type mismatches
            result[key] = override_value

    return result


def get_null_value_for_type(dtype: pa.DataType) -> dict | None:
    """Get a single null value representation for the given type.

    For struct types, returns a dict with None values for all fields.
    This is important for Lance 2.1 compatibility where struct nulls
    are represented differently from structs with null fields.

    For other types, returns None.
    """
    if pa.types.is_struct(dtype):
        return {field.name: get_null_value_for_type(field.type) for field in dtype}
    else:
        return None


def make_null_array(n: int, dtype: pa.DataType) -> pa.Array:
    """Create an array of n 'null' values for the given type.

    For struct types, creates valid structs with all-null fields rather than
    null structs. This distinction matters in Lance 2.1 where the representation
    differs.

    For other types, creates null values using pa.nulls().
    """
    if pa.types.is_struct(dtype):
        # Create structs with null fields instead of null structs
        # This is important for Lance 2.1 compatibility
        child_arrays = [make_null_array(n, field.type) for field in dtype]
        return pa.StructArray.from_arrays(
            child_arrays,
            names=[field.name for field in dtype],
        )
    else:
        return pa.nulls(n, type=dtype)  # type: ignore[call-overload]
