"""The sentinel for an argument the caller did not pass.

A leaf module: it imports nothing else from the package, so ``transport`` and
``domain`` can both name :data:`KEEP` without a cycle.
"""

from __future__ import annotations

# Python internals
from enum import Enum
from typing import Final, Literal


class _Keep(Enum):
    """One member, so :data:`Keep` can type the sentinel and mypy can narrow it."""

    KEEP = "keep"


KEEP: Final = _Keep.KEEP
"""Leave this field as it is: the default of every optional update argument.

Pass `None` to clear a field instead.
"""

Keep = Literal[_Keep.KEEP]
"""The type of :data:`KEEP`, for annotating an update argument: `str | None | Keep`."""
