"""The destructive-operations register (D-28) — read `side_effect_class` through here.

WHY THIS MODULE EXISTS

`tool.definition.side_effect_class` classifies what a tool's REAL execution can
destroy. It is the INVERTED safe-list ratified by Arman 2026-08-15: we do not
enumerate what is safe, we enumerate destructive potential — because the destructive
surface is *generated* (269 active tools, 22 live MCP servers, a 378-noun action
grid), so any hand-written safe-list is stale the moment someone adds a tool.

The column is nullable, and a NULL is NOT "unknown, therefore fine". A NULL means
UNCLASSIFIED, and unclassified is read as the MOST destructive class in the ordering
below. That is the entire point: a tool that nobody classified must not be able to
enter replay wearing a safe label.

So no consumer may read the raw column. Every consumer calls
``effective_side_effect_class(...)``, which maps NULL to the maximum.

It lives in matrx-ai because the tool executor is its first RUNTIME consumer
(mandate-candidate containment, ``matrx_ai.tools.candidate_containment``) and a
package may never import aidream. ``aidream.services.tooling.side_effect_class``
re-exports this module so there is exactly one ranking.

Contract: aidream/services/tooling/FEATURE.md §Destructive-operations register.
"""

from __future__ import annotations

from typing import Any, Final

READ_ONLY: Final = "read_only"
PAID_READ: Final = "paid_read"
DB_WRITE: Final = "db_write"
DB_DESTRUCTIVE: Final = "db_destructive"
MACHINE: Final = "machine"
BROWSER_SESSION: Final = "browser_session"
EXTERNAL_WRITE: Final = "external_write"
SENDS_TO_HUMAN: Final = "sends_to_human"
MOVES_MONEY: Final = "moves_money"
PLATFORM_META: Final = "platform_meta"

# Ascending severity. The LAST entry is what an unclassified tool is read as.
#
# The ordering is a containment ordering, not a moral one: it answers "how much
# machinery must exist before this may run for real?" Money movement sits at the top
# among effects on the outside world; platform_meta sits above it because a tool that
# rewrites our own agent/workflow/kind definitions can mint arbitrary new capability
# — including the capability to do everything below it.
SEVERITY_ORDER: Final[tuple[str, ...]] = (
    READ_ONLY,
    PAID_READ,
    DB_WRITE,
    MACHINE,
    BROWSER_SESSION,
    EXTERNAL_WRITE,
    DB_DESTRUCTIVE,
    SENDS_TO_HUMAN,
    MOVES_MONEY,
    PLATFORM_META,
)

VALID_CLASSES: Final[frozenset[str]] = frozenset(SEVERITY_ORDER)

# What an unclassified tool is read as. Deliberately the maximum.
UNCLASSIFIED_AS: Final[str] = SEVERITY_ORDER[-1]

_RANK: Final[dict[str, int]] = {name: i for i, name in enumerate(SEVERITY_ORDER)}

# Action-dispatched tools declare the most destructive thing they can do on the
# definition row, but a concrete invocation can be narrower.  Refinements are
# explicit by tool AND action; an unknown/missing action always falls back to
# the definition-level class rather than guessing safe.
_INVOCATION_ACTION_CLASSES: Final[dict[str, tuple[str, dict[str, str]]]] = {
    "data": (
        "action",
        {
            "catalog": READ_ONLY,
            "query": READ_ONLY,
            "count": READ_ONLY,
            "get": READ_ONLY,
            "create": DB_WRITE,
            "update": DB_WRITE,
            "delete": DB_WRITE,
        },
    ),
}


def effective_side_effect_class(row: Any) -> str:
    """The class to ACT on for a tool.definition row (or a raw class string / mapping).

    NULL / missing / unrecognized ⇒ ``UNCLASSIFIED_AS`` (the most destructive class).
    An unrecognized non-null value is treated the same way rather than raising: a
    guard that kills a live request over a spelling is worse than one that contains
    it maximally and lets ``scripts/check_side_effect_class.py`` scream about it.
    """
    if isinstance(row, str):
        raw: Any = row
    elif isinstance(row, dict):
        raw = row.get("side_effect_class")
    else:
        raw = getattr(row, "side_effect_class", None)

    if isinstance(raw, str) and raw in VALID_CLASSES:
        return raw
    return UNCLASSIFIED_AS


def effective_invocation_side_effect_class(
    row: Any,
    arguments: Any,
    *,
    tool_name: str | None = None,
) -> str:
    """Return the explicit effect of one invocation, falling back fail-closed.

    Definition-level classes describe a tool's maximum capability. For an
    action-dispatched tool, a reviewed action map may narrow a concrete call.
    Missing, malformed, or unrecognized arguments keep the definition class.
    """
    fallback = effective_side_effect_class(row)
    name = tool_name
    if name is None:
        if isinstance(row, dict):
            raw_name = row.get("name")
        else:
            raw_name = getattr(row, "name", None)
        name = raw_name if isinstance(raw_name, str) else None

    refinement = _INVOCATION_ACTION_CLASSES.get(name or "")
    if refinement is None or not isinstance(arguments, dict):
        return fallback

    field, classes = refinement
    raw_action = arguments.get(field)
    if not isinstance(raw_action, str):
        return fallback
    return classes.get(raw_action.strip().lower(), fallback)


def severity_rank(cls: str) -> int:
    """Position in ``SEVERITY_ORDER``; unknown values rank at the maximum."""
    return _RANK.get(cls, _RANK[UNCLASSIFIED_AS])


def is_at_least(cls: str, floor: str) -> bool:
    """True when ``cls`` is at least as destructive as ``floor``."""
    return severity_rank(cls) >= severity_rank(floor)


def max_side_effect_class(classes: object) -> str:
    """The most destructive class in an iterable. Empty ⇒ ``READ_ONLY``."""
    ranked = [severity_rank(c) for c in classes]  # type: ignore[union-attr]
    if not ranked:
        return READ_ONLY
    return SEVERITY_ORDER[max(ranked)]
