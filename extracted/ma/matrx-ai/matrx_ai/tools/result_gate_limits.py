"""The tool-result gate's limits, as the ORG's rows rather than this file's numbers.

Every cap at the size-gate seam used to be a module constant in
:mod:`matrx_ai.tools.output_caps` (explicitly "never env vars"). They are now
rows of the ``tools.result_gate`` knob feature, seeded at exactly today's
constants by ``db/migrations/0974_tool_result_gate_caps_become_knobs.sql``.

matrx-ai may not import the host — the rows live in Postgres behind aidream's
scoped feature-knob resolver — so the host injects a reader
(``result_gate_limits_reader``, wired in ``aidream/package_integration.py``).
The constants stay here as the STANDALONE defaults: matrx-ai installed alone, or
a client host with no Postgres, has no rows to read and the declared numbers are
the honest answer.

One limit is deliberately NOT a knob:
:data:`matrx_ai.tools.output_caps.TOOL_RESULT_ABSOLUTE_CEILING_CHARS`. That is the
provider-boundary ceiling enforced in ``MessageList.sanitize``, source-agnostic
and fail-safe, and an org-editable provider ceiling would let one tenant raise
the one backstop protecting every other tenant's bill. It is a constant on
purpose, with the reason written beside it.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any, Literal

from matrx_utils import vcprint

from matrx_ai.tools.output_caps import (
    TOOL_LIST_DEFAULT_LIMIT,
    TOOL_RESULT_ABSOLUTE_CEILING_CHARS,
    TOOL_RESULT_CANARY_CHARS,
    TOOL_RESULT_SOFT_CAP_CHARS,
)

#: The knob feature every limit below is a row of.
RESULT_GATE_KNOB_FEATURE = "tools.result_gate"

#: How many sections one oversized result may be cut into before neighbours are
#: grouped. New with the relevance gate — it had no prior constant.
DEFAULT_MAX_SECTIONS_PER_RESULT = 200

#: Probability at or above which a judged section is KEPT. Below the platform's
#: usual 0.7 "act on it" bar on purpose: holding back a section the agent needed
#: costs a re-fetch round trip, showing one it did not costs a few thousand
#: characters.
#: KNOB MIRROR of platform.feature_knob "tools.result_gate" "section_relevance_threshold"
#: The registry row is the authority — `RESULT_GATE_KNOB_KEYS` reads it through
#: the host on every gated result — and this value must be available WITHOUT a
#: database read because it is a frozen dataclass field default that matrx-ai
#: standalone (no Postgres, no host reader) still has to answer with.
DEFAULT_SECTION_RELEVANCE_THRESHOLD = 0.6

#: field name on :class:`ResultGateLimits` → knob key. The key IS the field name;
#: the mapping is explicit so a rename cannot silently stop reading a row.
RESULT_GATE_KNOB_KEYS: dict[str, str] = {
    "soft_cap_chars": "soft_cap_chars",
    "canary_chars": "canary_chars",
    "list_default_limit": "list_default_limit",
    "overflow_stash_max_chars": "overflow_stash_max_chars",
    "max_sections_per_result": "max_sections_per_result",
    "section_relevance_threshold": "section_relevance_threshold",
}

_FLOAT_FIELDS = frozenset({"section_relevance_threshold"})


@dataclass(frozen=True)
class ResultGateLimits:
    """The caps in force for ONE gated result, and where they came from.

    ``source`` is never decoration: a result gated on package defaults when the
    host WAS configured means the knob door failed, and the gate says so out loud
    rather than quietly applying a number no admin can see.
    """

    soft_cap_chars: int = TOOL_RESULT_SOFT_CAP_CHARS
    canary_chars: int = TOOL_RESULT_CANARY_CHARS
    list_default_limit: int = TOOL_LIST_DEFAULT_LIMIT
    overflow_stash_max_chars: int = TOOL_RESULT_ABSOLUTE_CEILING_CHARS
    max_sections_per_result: int = DEFAULT_MAX_SECTIONS_PER_RESULT
    section_relevance_threshold: float = DEFAULT_SECTION_RELEVANCE_THRESHOLD
    source: Literal["knobs", "package_defaults"] = "package_defaults"

    @property
    def absolute_ceiling_chars(self) -> int:
        """The provider-boundary ceiling. A CONSTANT, never a knob — see module
        docstring. Exposed here so a caller reads every limit from one object."""
        return TOOL_RESULT_ABSOLUTE_CEILING_CHARS


async def load_result_gate_limits(
    organization_id: str | None = None,
    user_id: str | None = None,
) -> ResultGateLimits:
    """The org's effective caps, read through the host's settings door.

    With NO reader configured (matrx-ai standalone, a client host with no
    Postgres) the declared defaults are the honest answer and stay silent. A
    reader that is configured and FAILS is a different fact — the admin's rows
    exist and did not reach the run — and that announces itself.
    """
    from matrx_ai._ext import get_result_gate_limits_reader

    reader = get_result_gate_limits_reader()
    if reader is None:
        return ResultGateLimits()
    try:
        values = await reader(organization_id=organization_id, user_id=user_id)
    except Exception as exc:  # noqa: BLE001 — never let the door break a result
        vcprint(
            f"⚠️  The tool-result gate could not read its '{RESULT_GATE_KNOB_FEATURE}' "
            f"settings ({type(exc).__name__}: {exc}). Falling back to the package "
            f"defaults (soft cap {TOOL_RESULT_SOFT_CAP_CHARS:,} chars); any "
            f"organization override is NOT in force for this result.",
            "[RESULT GATE] Settings unavailable",
            color="yellow",
        )
        return ResultGateLimits()
    if not isinstance(values, dict) or not values:
        return ResultGateLimits()
    return limits_from_values(values)


def limits_from_values(values: dict[str, Any]) -> ResultGateLimits:
    """Build limits from resolved knob values, keeping the declared default for
    any key the door did not answer."""
    out = ResultGateLimits(source="knobs")
    for field_name, key in RESULT_GATE_KNOB_KEYS.items():
        if key not in values or values[key] is None:
            continue
        raw = values[key]
        try:
            value = float(raw) if field_name in _FLOAT_FIELDS else int(raw)
        except (TypeError, ValueError):
            continue
        out = replace(out, **{field_name: value})
    return out


__all__ = [
    "DEFAULT_MAX_SECTIONS_PER_RESULT",
    "DEFAULT_SECTION_RELEVANCE_THRESHOLD",
    "RESULT_GATE_KNOB_FEATURE",
    "RESULT_GATE_KNOB_KEYS",
    "ResultGateLimits",
    "limits_from_values",
    "load_result_gate_limits",
]
