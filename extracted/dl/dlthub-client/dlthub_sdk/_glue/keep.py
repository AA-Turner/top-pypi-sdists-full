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


#: Leave the field as it is. The default of every optional update argument.
KEEP: Final = _Keep.KEEP

#: The type of :data:`KEEP`, to sit in a union: ``str | None | Keep``.
Keep = Literal[_Keep.KEEP]
