"""The warning for an experimental keyword of a stable call.

The names of ``mistralai.agents.experimental`` give no warning: importing that namespace says it.
A keyword of a stable call does not, so it warns once per process the first time it is given.
"""

from __future__ import annotations

import os
import threading
import warnings

__all__ = ["EXPERIMENTAL_WARNINGS_ENV", "ExperimentalWarning", "warn_experimental"]

EXPERIMENTAL_WARNINGS_ENV = "AGENTS_SDK_EXPERIMENTAL_WARNINGS"
# The values that turn the warnings off; any other value, or none, leaves them on.
_OFF = frozenset({"0", "false", "no", "off"})

_warned: set[str] = set()
_warned_lock = threading.Lock()


class ExperimentalWarning(UserWarning):
    """A call was given an experimental keyword: a minor release may change or remove it.

    Each keyword warns once per process. Hide them all with ``AGENTS_SDK_EXPERIMENTAL_WARNINGS=0``,
    or in code with ``warnings.filterwarnings("ignore", category=agents.ExperimentalWarning)``.
    """


def warn_experimental(keyword: str, *, stacklevel: int) -> None:
    """Warn that ``keyword`` is experimental, the first time in this process.

    ``stacklevel`` counts from the caller of this function, as ``warnings.warn`` does from its own.
    """
    if os.environ.get(EXPERIMENTAL_WARNINGS_ENV, "").strip().lower() in _OFF:
        return
    with _warned_lock:
        if keyword in _warned:
            return
        _warned.add(keyword)
    warnings.warn(
        f"{keyword} is experimental: a minor release may change or remove it. "
        f"Set {EXPERIMENTAL_WARNINGS_ENV}=0 to hide experimental warnings.",
        ExperimentalWarning,
        stacklevel=stacklevel + 1,
    )
