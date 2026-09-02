"""Tool-result output-size caps — the shared primitive behind the size gate.

The platform bounds how many characters a single tool result may place in front
of the model. The danger is not one large read — it is that a tool result is
**re-sent to the provider on every subsequent iteration of the tool loop**, so a
1.8 MB note dump pulled once gets re-billed four more times (a real ~$25 incident).

Two truths shape this module:

1. **A blunt generic truncation DESTROYS a structured result.** Cutting
   ``json.dumps(rows)`` at 50 000 chars hands the model invalid JSON. So the
   real mechanism is **tool self-responsibility**: a tool that knows its domain
   truncates *surgically* (trim the one long ``content`` field, keep ``id`` /
   ``label`` / ``created_at`` intact) and declares it did via
   ``ToolResult.output_self_capped``. ``cap_text`` is the helper it uses.

2. **The generic gate is the ALARM, not the mechanism.** When the generic soft
   cap fires, a tool failed to manage itself (or it is an external/MCP tool we
   do not own and cannot teach). Either way the firing is recorded so the gap
   becomes visible — a tool defect for tools we own, an expected event for ones
   we do not.

Constants here are code CAPS (a behavior change is a code push — fine; that beats
a silent prod failure), never env vars.
"""

from __future__ import annotations

from pydantic import BaseModel

# ── The three tiers ──────────────────────────────────────────────────────────────────
#
# Numbers are deliberately GENEROUS. Set them too low and every legitimate large
# read (a web page, a big search) truncates → the agent fetches more → one click
# becomes two requests → cost balloons the OTHER way. These thresholds exist to
# catch the crazy cases (a 1.8 MB blob), not to nickel-and-dime normal results.

TOOL_RESULT_SOFT_CAP_CHARS = 50_000
"""Layer 1 — the soft cap applied at production. A result over this that did NOT
self-manage (``output_self_capped``) is truncated for the model and recorded as a
tool defect. ~12K tokens — a generous single result; a normal big web page passes."""

TOOL_RESULT_CANARY_CHARS = 25_000
"""Shadow / what-if tier. A result that lands in [CANARY, SOFT) passed the real
gate but is recorded to ops-triage so we can replay the scenario and decide,
empirically, whether the soft cap should move. The full payload is still in
``cx_tool_call.output`` (≤100K storage cap) for that replay."""

TOOL_RESULT_ABSOLUTE_CEILING_CHARS = 500_000
"""Layer 2 — the hard ceiling enforced at the provider boundary (MessageList.sanitize),
source-agnostic. Nothing crosses this silently. A tool may authorize a higher value
for ONE result via ``ToolResult.approved_max_chars`` (the effective ceiling becomes
``max(ABSOLUTE, approved_max_chars)``); absent that, even a self-capped result is
bounded here — fail-safe."""


class CapInfo(BaseModel):
    """The outcome of one ``cap_text`` call — sibling metadata a tool attaches next
    to a truncated field so the model knows the true size and that it was trimmed."""

    total_chars: int
    """True length of the field BEFORE truncation (so the model sees what it's missing)."""
    shown_chars: int
    """Length actually returned."""
    truncated: bool
    limit: int
    """The cap that was applied."""


def cap_text(text: str | None, *, limit: int) -> tuple[str, CapInfo]:
    """Surgically truncate ONE text field to ``limit`` characters.

    Returns the (possibly truncated) text plus a ``CapInfo`` the caller attaches as
    sibling metadata (``content_chars`` / ``content_truncated``). This is the
    building block for a tool's own domain-aware truncation — it trims exactly one
    field and never touches the surrounding structure, so ``id`` / ``label`` /
    timestamps survive intact (the opposite of a blunt blob truncation).
    """
    s = text or ""
    total = len(s)
    if limit < 0:
        limit = 0
    if total <= limit:
        return s, CapInfo(total_chars=total, shown_chars=total, truncated=False, limit=limit)
    capped = s[:limit]
    return capped, CapInfo(
        total_chars=total, shown_chars=len(capped), truncated=True, limit=limit
    )


TOOL_LIST_DEFAULT_LIMIT = 200
"""Default row cap for a list-shaped tool result (``cap_list``). A list tool that
returns compact rows is bounded by COUNT, not by a per-field length; this is the
generous default number of rows an unfiltered ``*_list`` returns before it tells
the agent to narrow. Small metadata rows × 200 stays well under the soft cap."""


class ListCapInfo(BaseModel):
    """The outcome of one ``cap_list`` call — sibling metadata a tool attaches so
    the model knows the true count and that the list was capped."""

    total: int
    """True number of rows BEFORE capping."""
    shown: int
    """Number of rows actually returned."""
    truncated: bool
    limit: int


def cap_list(rows: list, *, limit: int = TOOL_LIST_DEFAULT_LIMIT) -> tuple[list, ListCapInfo]:
    """Cap a list-shaped result to ``limit`` rows and report the true total.

    The count-side counterpart to ``cap_text``: a ``*_list`` tool projects each
    row to a compact shape itself (domain knowledge), then calls this to bound the
    ROW COUNT and get honest ``total`` / ``truncated`` siblings. When the projected
    rows are small and the count is capped, the whole result is bounded — so the
    tool can honestly set ``ToolResult.output_self_capped=True``. Keeps ordering.
    """
    if limit < 0:
        limit = 0
    total = len(rows)
    shown = rows[:limit]
    return shown, ListCapInfo(
        total=total, shown=len(shown), truncated=total > len(shown), limit=limit
    )


def truncate_with_notice(
    content: str,
    *,
    limit: int,
    total_chars: int,
    call_id: str,
    tool_name: str = "",
) -> str:
    """Blunt-truncate a serialized tool-result blob and append an inline notice.

    This is what the GENERIC gate uses when a tool did not self-manage — there is
    no structured sibling to carry the metadata, so the notice is appended to the
    text itself. The notice names the ``call_id`` and tells the model exactly how to
    retrieve the rest via the ``fetch_tool_result`` tool (a deliberate, args-driven
    fetch — the good agent is never punished, it just asks for what it wants).
    """
    head = content[: max(0, limit)]
    notice = (
        "\n\n[⚠️ TOOL RESULT TRUNCATED BY THE PLATFORM SIZE GATE"
        + (f" — tool {tool_name!r}" if tool_name else "")
        + f". Showing the first {len(head):,} of {total_chars:,} characters. "
        f"The full result is cached: to read more, call the `fetch_tool_result` tool with "
        f'call_id="{call_id}", offset={len(head)}, and max_chars=<how many more characters '
        f"you want>. Request only what you actually need.]"
    )
    return head + notice
