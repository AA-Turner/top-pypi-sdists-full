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
    '1.3.0'
    >>> __author__
    'Aaron Mildenstein'

Note:
    Configure a logger with `TieredDebug.add_handler` to enable logging
    output. See `_base.py` for implementation details and `debug.py` for
    a sample usage with a global debug instance and decorator.
"""

from datetime import datetime
from ._base import TieredDebug, DebugLevel

FIRST_YEAR = 2025
now = datetime.now()
if now.year == FIRST_YEAR:
    COPYRIGHT_YEARS = "2025"
else:
    COPYRIGHT_YEARS = f"2025-{now.year}"

__version__ = "1.4.0"
__author__ = "Aaron Mildenstein"
__copyright__ = f"{COPYRIGHT_YEARS}, Aaron Mildenstein"
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
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: PyPy",
]

__all__ = ["TieredDebug", "DebugLevel", "__author__", "__copyright__", "__version__"]
