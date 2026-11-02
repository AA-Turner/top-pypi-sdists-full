"""Helpers used by the central imports package."""

from .lazy_load import _LazyCallable, _lazy_module, _lazy_type
from .load_dotenv import load_dotenv as _fallback_load_dotenv
from .secure_filename import secure_filename as _fallback_secure_filename
from .jsonify import jsonify as _fallback_jsonify


def load_dotenv(*args, **kwargs):
    """Use python-dotenv when available, otherwise use the bundled parser."""
    try:
        from dotenv import load_dotenv as load
    except ImportError:
        load = _fallback_load_dotenv
    return load(*args, **kwargs)


def secure_filename(filename):
    """Use Werkzeug when available, otherwise use the bundled sanitizer."""
    try:
        from werkzeug.utils import secure_filename as sanitize
    except ImportError:
        sanitize = _fallback_secure_filename
    return sanitize(filename)


def jsonify(*args, **kwargs):
    """Use Flask when available, otherwise return a bundled JSON string."""
    try:
        from flask import jsonify as serialize
    except ImportError:
        serialize = _fallback_jsonify
    return serialize(*args, **kwargs)
