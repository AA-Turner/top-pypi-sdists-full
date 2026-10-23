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

import json

from matrx_utils.raw_capture import record_cut
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
    record_cut(where="tool self-cap", before=total, after=len(capped), limit_name="cap_text", limit=limit, original=s)
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
    record_cut(where="tool self-cap", before=total, after=len(shown), limit_name="cap_list", limit=limit,
               unit="rows", original=rows if total > len(shown) else None)
    return shown, ListCapInfo(
        total=total, shown=len(shown), truncated=total > len(shown), limit=limit
    )


def cap_json_list(rows: list, *, max_chars: int) -> tuple[list, ListCapInfo]:
    """Return the largest JSON-safe prefix that fits ``max_chars``.

    Count caps alone are insufficient when list fields are user-controlled: a
    directory listing, for example, can contain hundreds of long paths. Measure
    with ASCII JSON escaping so the estimate is a conservative bound for the
    serialized result that will be sent to a provider.
    """
    if max_chars < 0:
        max_chars = 0
    shown: list = []
    used = 2  # JSON list brackets
    for row in rows:
        encoded_chars = len(json.dumps(row, ensure_ascii=True, separators=(",", ":")))
        separator_chars = 1 if shown else 0
        if used + separator_chars + encoded_chars > max_chars:
            break
        shown.append(row)
        used += separator_chars + encoded_chars
    record_cut(where="tool self-cap", before=len(rows), after=len(shown), limit_name="cap_json_list", limit=max_chars,
               unit="rows", original=rows if len(shown) < len(rows) else None)
    return shown, ListCapInfo(
        total=len(rows), shown=len(shown), truncated=len(shown) < len(rows), limit=max_chars
    )


#: Opens the notice of a STRUCTURAL cut — whole items/values dropped, kept
#: JSON valid. The relevance gate reads it to word its own note truthfully.
STRUCTURAL_NOTICE_HEAD = "⚠️ TOOL RESULT SHORTENED BY THE PLATFORM SIZE GATE"


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
    structural = truncate_json_structurally(content, limit=limit)
    if structural is not None:
        text, cuts, offset, standard = structural
        cut_lines = "; ".join(cuts)
        if offset is not None:
            where = f"offset={offset} (where the first dropped content starts in the full text)"
        elif not standard:
            where = (
                "offset=0 (the position of the dropped content in the full text is unknown — "
                "it is not laid out the way it is shown here, so read from the start)"
            )
        else:
            where = "offset=0 (the position of the dropped content is unknown)"
        return text + (
            "\n\n[" + STRUCTURAL_NOTICE_HEAD
            + (f" — tool {tool_name!r}" if tool_name else "")
            + f". The JSON above is complete and valid, but not everything: {cut_lines}. "
            f"The full result ({total_chars:,} characters) is cached: to read the rest, "
            f'call the `fetch_tool_result` tool with call_id="{call_id}", {where}, and '
            "max_chars=<how many characters you want>. Request only what you need.]"
        )
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


_DUMPS_KW: dict = {"ensure_ascii": False}
_MIN_STRING_KEEP = 200
_SENTINEL = "\u0000matrx-cut\u0000"


def _dumps(value: object) -> str:
    return json.dumps(value, **_DUMPS_KW)


def _path_label(path: tuple) -> str:
    label = ""
    for part in path:
        label += f"[{part}]" if isinstance(part, int) else (f".{part}" if label else str(part))
    return label or "(top level)"


def _get(root: object, path: tuple) -> object:
    node = root
    for part in path:
        node = node[part]  # type: ignore[index]
    return node


def _set(root: object, path: tuple, value: object) -> object:
    if not path:
        return value
    _get(root, path[:-1])[path[-1]] = value  # type: ignore[index]
    return root


def _walk(node: object, path: tuple = ()):
    yield path, node
    if isinstance(node, dict):
        for k, v in node.items():
            yield from _walk(v, (*path, k))
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from _walk(v, (*path, i))


def _top_lists(node: object, path: tuple = ()):
    """Non-empty lists with no list above them — the rows a result is made of."""
    if isinstance(node, list):
        if node:
            yield path, node
        return
    if isinstance(node, dict):
        for k, v in node.items():
            yield from _top_lists(v, (*path, k))


def _offset_of_cut(content: str, original: object, path: tuple, keep: int) -> int | None:
    """Where, in the ORIGINAL text, the first content dropped at ``path`` starts."""
    probe = json.loads(content)
    node = _get(probe, path)
    if isinstance(node, list):
        probe = _set(probe, path, [*node[:keep], _SENTINEL])
        needle = _dumps(_SENTINEL)
    else:
        probe = _set(probe, path, f"{node[:keep]}{_SENTINEL}")
        needle = _dumps(_SENTINEL)[1:-1]
    at = _dumps(probe).find(needle)
    return at if at >= 0 else None


def truncate_json_structurally(
    content: str, *, limit: int
) -> tuple[str, list[str], int | None, bool] | None:
    """Shorten a JSON result to ``limit`` characters WITHOUT breaking it.

    A positional cut hands the model half an object and an unterminated string.
    Here the result's row lists (lists with no list above them, each at least
    5% of the text) give up trailing items IN PROPORTION — one shared fraction,
    so equal siblings keep equal shares. When emptying them all still would not
    fit, the lists are left alone and the longest string values are shortened
    instead, with an explicit marker inside the value.

    Returns ``(json_text, cuts, offset, standard)``: ``cuts`` names each cut and
    how much was dropped; ``offset`` is where the earliest dropped content starts
    in the ORIGINAL text (what ``fetch_tool_result`` pages through); ``standard``
    is False when the original was not serialized the standard way, in which
    case ``offset`` is None and unknown. Returns None for non-JSON content or
    when the result cannot be brought under the limit.
    """
    try:
        original = json.loads(content)
    except (ValueError, TypeError):
        return None
    if not isinstance(original, dict | list):
        return None
    standard = _dumps(original) == content
    work = json.loads(content)
    total = len(_dumps(work))
    if total <= limit:
        return None
    cuts: list[str] = []
    cut_points: list[tuple[tuple, int]] = []

    lists = [(p, n) for p, n in _top_lists(work) if len(_dumps(n)) >= total * 0.05]

    def with_fraction(frac: float) -> object:
        trial = json.loads(content)
        for path, items in lists:
            trial = _set(trial, path, items[: int(len(items) * frac)])
        return trial

    if lists and len(_dumps(with_fraction(0.0))) <= limit:
        lo, hi = 0.0, 1.0
        for _ in range(30):
            mid = (lo + hi) / 2
            if len(_dumps(with_fraction(mid))) <= limit:
                lo = mid
            else:
                hi = mid
        work = with_fraction(lo)
        for path, items in lists:
            keep = int(len(items) * lo)
            if keep < len(items):
                cuts.append(
                    f"{_path_label(path)} shows {keep} of {len(items)} items "
                    f"({len(items) - keep} more not shown)"
                )
                cut_points.append((path, keep))
    else:
        for _ in range(64):
            total = len(_dumps(work))
            if total <= limit:
                break
            strings = [
                (len(node), path)
                for path, node in _walk(work)
                if isinstance(node, str) and len(node) > _MIN_STRING_KEEP and path
                and path not in {c[0] for c in cut_points}
            ]
            if not strings:
                return None
            size, path = max(strings, key=lambda t: t[0])
            keep = max(_MIN_STRING_KEEP, size - (total - limit) - 80)
            text = _get(work, path)
            work = _set(work, path, f"{text[:keep]}… [{size - keep:,} more characters not shown]")
            cuts.append(f"{_path_label(path)} shows {keep:,} of {size:,} characters")
            cut_points.append((path, keep))
        else:
            return None
    if len(_dumps(work)) > limit:
        return None
    offset: int | None = None
    if standard:
        found = [o for p, k in cut_points if (o := _offset_of_cut(content, original, p, k)) is not None]
        offset = min(found) if found else None
    return _dumps(work), cuts, offset, standard


def _path_exists(root: object, path: tuple) -> bool:
    try:
        _get(root, path)
    except (KeyError, IndexError, TypeError):
        return False
    return True


def without_fetch_pointer(content: str, *, tool_name: str) -> str:
    """Replace every size-gate instruction to use ``fetch_tool_result`` with a step
    the model can take when that tool cannot be offered in this run."""
    import re

    instead = (
        f"call `{tool_name}` again asking for less at a time (a smaller limit, the next "
        "page or offset, or a narrower filter) — `fetch_tool_result` is not available "
        "in this run"
    )
    content = re.sub(r"call the `fetch_tool_result` tool[^\]]*", instead, content)
    return content.replace(
        "Use `fetch_tool_result` to read further.", f"To see more, {instead}."
    )
