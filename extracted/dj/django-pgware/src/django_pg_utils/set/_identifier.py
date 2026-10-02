"""GUC identifier validation.

PostgreSQL GUC names are SQL identifiers and cannot be passed as bind
parameters, so they are interpolated directly into ``SET`` / ``SHOW`` /
``RESET`` text. Names normally come from developer config, but validating them
keeps a user-derived name from injecting SQL — psycopg's ``execute`` permits
multiple ``;``-separated statements, so an unvalidated name like
``x = 'a'; DROP TABLE t; SET y`` would otherwise run. This mirrors the
function-name whitelist in ``locks/_lock.py`` (``VALID_LOCK_FUNCTIONS``); the
set/hush side previously had no equivalent guard.
"""

from __future__ import annotations

import re

# An identifier, optionally one extension namespace
# (e.g. ``auto_explain.log_min_duration``). Deliberately strict: no quoting,
# whitespace, or multi-level dotting — a legitimate GUC name never needs them.
_GUC_NAME_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*(\.[A-Za-z_][A-Za-z0-9_]*)?$")


def validate_guc_name(name: str) -> str:
    """Return ``name`` unchanged if it is a valid GUC identifier, else raise."""
    if not isinstance(name, str) or not _GUC_NAME_RE.match(name):
        raise ValueError(f"Invalid GUC name: {name!r}")
    return name
