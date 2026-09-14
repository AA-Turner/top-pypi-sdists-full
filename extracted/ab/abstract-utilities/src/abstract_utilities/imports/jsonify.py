"""Flask's jsonify semantics, without Flask. Stdlib only.

Mirrors flask.json.provider.DefaultJSONProvider: the same default=
type coercions, the same dumps options, the same *args/**kwargs shorthand.
"""

from __future__ import annotations

import dataclasses
import decimal
import json
import uuid
from datetime import date, datetime, timezone
from email.utils import format_datetime

__all__ = ["jsonify", "dumps", "default"]


def _http_date(value: date) -> str:
    """RFC 822 / HTTP date, e.g. 'Sun, 13 Sep 2026 00:00:00 GMT'.

    Same output as werkzeug.http.http_date, which is what Flask uses.
    Naive datetimes are assumed UTC; dates become midnight UTC.
    """
    if isinstance(value, datetime):
        dt = value
    else:
        dt = datetime(value.year, value.month, value.day)

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = dt.astimezone(timezone.utc)

    return format_datetime(dt, usegmt=True)


def default(o):
    """Serializer for types json.dumps can't handle. Pass as default=."""
    # datetime is a subclass of date, so this covers both.
    if isinstance(o, date):
        return _http_date(o)

    if isinstance(o, (decimal.Decimal, uuid.UUID)):
        return str(o)

    if dataclasses.is_dataclass(o) and not isinstance(o, type):
        return dataclasses.asdict(o)

    if hasattr(o, "__html__"):
        return str(o.__html__())

    raise TypeError(f"Object of type {type(o).__name__} is not JSON serializable")


def dumps(obj, **kwargs) -> str:
    kwargs.setdefault("default", default)
    kwargs.setdefault("ensure_ascii", True)
    kwargs.setdefault("sort_keys", True)
    return json.dumps(obj, **kwargs)


def _prepare(args, kwargs):
    if args and kwargs:
        raise TypeError("jsonify() takes either args or kwargs, not both")
    if not args and not kwargs:
        return None
    if len(args) == 1:
        return args[0]
    return args or kwargs


def jsonify(*args, indent: int | None = None, **kwargs) -> str:
    """Serialize to a JSON string.

    jsonify(obj)        -> obj
    jsonify(a=1, b=2)   -> {"a": 1, "b": 2}
    jsonify(1, 2, 3)    -> [1, 2, 3]

    Compact by default, like Flask outside debug mode. Pass indent=2 for
    the pretty form. The trailing newline matches Flask's response body.
    """
    obj = _prepare(args, kwargs)

    if indent is None:
        body = dumps(obj, separators=(",", ":"))
    else:
        body = dumps(obj, indent=indent)

    return f"{body}\n"
