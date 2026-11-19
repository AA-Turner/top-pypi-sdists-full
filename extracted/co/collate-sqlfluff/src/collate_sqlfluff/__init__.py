"""Sqlfluff is a SQL linter for humans."""

import sys
from importlib import metadata

# Expose the public API.
from collate_sqlfluff.api import fix, lint, list_dialects, list_rules, parse

__all__ = (
    "lint",
    "fix",
    "parse",
    "list_rules",
    "list_dialects",
)

# Get the current version
__version__ = metadata.version("collate-sqlfluff")

# Check major python version
if sys.version_info[0] < 3:
    raise Exception("Sqlfluff does not support Python 2. Please upgrade to Python 3.")
# Check minor python version
elif sys.version_info[1] < 8:
    raise Exception(
        "Sqlfluff %s only supports Python 3.9 and beyond. "
        "Use an earlier version of sqlfluff or a later version of Python" % __version__
    )

# Register helper functions to support variable introspection on failure. pytest is only
# needed by the testing helpers, so a library install does not have to carry it.
try:
    import pytest
except ImportError:  # pragma: no cover
    pass
else:
    pytest.register_assert_rewrite("collate_sqlfluff.utils.testing")
