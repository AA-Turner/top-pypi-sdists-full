"""What each tool may touch, in the form dlt's MCP server prunes on.

dlt refuses to serve a tool whose requirement exceeds the caller's grant, and
treats a tool that declares nothing as needing everything — so an unannotated
tool reaches no agent. The declaration must be dlt's own class, which released
dlt does not carry yet, so it is looked up rather than imported. A dlt that
cannot read the declaration cannot prune on it either, which is what makes the
stand-in inert rather than a downgrade.

Declared in the return annotation, never through a decorator that rewrites
``__annotations__``: a rewritten one is not carried through ``functools.wraps``
on 3.14.
"""

from __future__ import annotations

# Python internals
import importlib
from dataclasses import dataclass
from typing import Any, Sequence, cast


@dataclass(frozen=True)
class _RequiresAccess:
    """Dlt's field names, so the annotation reads the same either way.

    Attributes:
        local: Verbs the tool needs on the developer's own machine.
        data: Verbs it needs on the workspace's data.
        context: Verbs it needs on the context graph — runs, jobs, telemetry.
    """

    local: Sequence[str] = ()
    data: Sequence[str] = ()
    context: Sequence[str] = ()


def _requires_access() -> type[Any]:
    """Return the class dlt prunes on, or the stand-in when dlt has none.

    Returns:
        ``dlt._workspace.access.RequiresAccess``, or :class:`_RequiresAccess`.
    """
    try:
        module = importlib.import_module("dlt._workspace.access")
    except ImportError:
        return _RequiresAccess
    return cast("type[Any]", getattr(module, "RequiresAccess", _RequiresAccess))


RequiresAccess = _requires_access()

#: Reads the context graph — telemetry, runs and job definitions — and nothing
#: else. Verbs are tuples: an ``Annotated`` alias carrying a list is unhashable.
CONTEXT_READ = RequiresAccess(context=("read",))

__all__ = ["CONTEXT_READ", "RequiresAccess"]
