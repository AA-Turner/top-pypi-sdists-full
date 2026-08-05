"""Tiered Debugging Module.

The `tiered_debug` package provides tools for multi-level debug logging
with configurable stack tracing. It is designed for projects requiring
detailed debugging, such as Elasticsearch workflows. The main class,
`TieredDebug`, supports logging at levels 1-5 with adjustable stack
levels for accurate caller reporting. The `DebugLevel` type hint defines
valid debug levels (1-5).

Examples:
    >>> from tiered_debug import TieredDebug, DebugLevel
    >>> debug = TieredDebug(level=2)
    >>> debug.level
    2
    >>> isinstance(DebugLevel(1), int)
    True
    >>> __version__
    '1.5.1'
    >>> __author__
    'Aaron Mildenstein'

Note:
    Configure a logger with `TieredDebug.add_handler` to enable logging
    output. See `_base.py` for implementation details and `debug.py` for
    a sample usage with a global debug instance and decorator.
"""


# When we go to 3.11+, this will change to
# from datetime import UTC, datetime
# And we can remove the timezone.utc fallback
from datetime import datetime, timezone

from ._base import DebugLevel, TieredDebug

FIRST_YEAR = 2025
UTC = getattr(datetime, "UTC", timezone.utc)

def get_copyright_years() -> str:
    now = datetime.now(UTC)
    if now.year == FIRST_YEAR:
        return f"{FIRST_YEAR}"
    return f"{FIRST_YEAR}-{now.year}"

__version__ = "1.5.1"
__author__ = "Aaron Mildenstein"
__copyright__ = f"{get_copyright_years()}, Aaron Mildenstein"
__license__ = "Apache 2.0"
__status__ = "Development"
__description__ = "Tiered debug logging for multiple levels with stack tracing."
__url__ = "https://github.com/untergeek/tiered-debug"
__email__ = "aaron@mildensteins.com"
__maintainer__ = "Aaron Mildenstein"
__maintainer_email__ = __email__
__keywords__ = ["debug", "logging", "tiered-debug"]
__classifiers__ = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: Apache Software License",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Programming Language :: Python :: 3.14",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: PyPy",
]

__all__ = ["DebugLevel", "TieredDebug", "__author__", "__copyright__", "__version__"]
