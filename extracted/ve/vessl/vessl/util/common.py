import secrets
import string
from datetime import datetime, timezone
from importlib import import_module

from vessl.util import logger
from vessl.util.exception import ImportPackageError


def parse_time_to_ago(dt: datetime):
    if not dt:
        return "N/A"

    delta = datetime.now(timezone.utc) - dt

    n = delta.total_seconds()
    units = [("second", 60), ("minute", 60), ("hour", 24), ("day", 365), ("year", 9999)]
    for unit_name, unit_size in units:
        if n < unit_size:
            n_int = int(n)
            return f"{n_int} {unit_name}{'s' if n_int != 1 else ''} ago"
        n /= unit_size

    return "ages ago"


def safe_cast(val, to_type, default=None):
    try:
        return to_type(val)
    except (ValueError, TypeError):
        return default


def get_module(name, required=None):
    try:
        return import_module(name)
    except ImportError:
        msg = f"Error importing optional module {name}"
        if required:
            logger.warn(msg)
            raise ImportPackageError(f"{required}")


def generate_uuid(n: int = 8):
    lowercase_alphanumeric = string.ascii_lowercase + string.digits
    return "".join(secrets.choice(lowercase_alphanumeric) for _ in range(n))


def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix) :]
    return text
