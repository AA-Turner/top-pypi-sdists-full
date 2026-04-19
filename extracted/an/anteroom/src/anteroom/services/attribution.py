"""Runtime context attribution (#923).

Builds a bounded, safety-scanned summary of what fed into an assistant turn:
recent turns, recalled memories, RAG sources, tool calls, and attached packs.
Used to populate the ``attribution`` SSE event and the persisted
``messages.metadata["attribution"]`` field.

Design contract (per the senior-approved plan):

* **Only ids + labels** in the snapshot — never content, never raw prompt
  text. Every user-derived string flows through the runtime's live
  ``DlpScanner.apply()`` and ``OutputContentFilter.apply()`` instances
  (not through invented helper functions) so that whatever redaction
  policy the installation has for responses applies identically here.
* **Tool-call source** is the stored assistant message's ``tool_calls``
  list (``list_messages`` / ``list_tool_calls``), NOT the expanded
  ``ai_messages`` list from ``_load_conversation_messages`` — the latter
  emits one extra ``role="tool"`` entry per tool call, so a positional
  mapping would over-count.
* **Pack source** is ``services.packs.list_packs()`` plus the current
  ``prompt_meta["pack_attachments"]`` list. No invented helpers.
* **Section cap** of 20 entries each, with a single ``{"truncated": N}``
  marker appended when the cap is hit. Total serialised snapshot fits
  well under 8 KB.
"""

from __future__ import annotations

import logging
from dataclasses import asdict, dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .dlp import DlpScanner
    from .output_filter import OutputContentFilter

logger = logging.getLogger(__name__)

# Per-section item cap. Additional items are collapsed into a single
# "+N more" marker so the serialised snapshot stays under ~8KB even on
# turns with huge tool-call fan-outs or many attached packs.
SECTION_CAP = 20

_DLP_BLOCK_LABEL = "[DLP blocked]"
_OUTPUT_FILTER_BLOCK_LABEL = "[output filter blocked]"


@dataclass(frozen=True)
class AttributionSnapshot:
    """Frozen, JSON-serialisable attribution for one assistant turn."""

    turns: list[dict[str, Any]] = field(default_factory=list)
    memory: list[dict[str, Any]] = field(default_factory=list)
    sources: list[dict[str, Any]] = field(default_factory=list)
    tools: list[dict[str, Any]] = field(default_factory=list)
    packs: list[dict[str, Any]] = field(default_factory=list)
    # Section-level counters so the UI can surface "N DLP redactions" /
    # "N output-filter warnings" without embedding raw matches.
    dlp_match_count: int = 0
    output_filter_match_count: int = 0


def _apply_safety(
    label: str,
    dlp_scanner: DlpScanner | None,
    output_filter: OutputContentFilter | None,
    counters: dict[str, int],
) -> str:
    """Run a label through DLP then output-filter, honouring each action.

    * ``DlpScanner.apply(text, direction="output")`` → ``(processed, result)``.
    * ``OutputContentFilter.apply(text)`` → ``(processed, result)``.

    For each scanner:
      - ``redact`` → processed text replaces the label
      - ``block``  → label becomes a fixed sentinel (empty string would
        render as a blank cell and hide the fact that redaction
        happened)
      - ``warn``   → label is unchanged, but the ``*_match_count``
        counter is bumped so the snapshot surfaces that the scanner
        fired.

    When a scanner is ``None`` (unit tests without the full runtime, or
    the corresponding config is disabled) that stage no-ops and the
    label passes through.
    """
    text = label
    if dlp_scanner is not None:
        dlp_processed, dlp_result = dlp_scanner.apply(text, direction="output")
        if dlp_result.matched:
            counters["dlp"] = counters.get("dlp", 0) + 1
            if dlp_result.action == "block":
                text = _DLP_BLOCK_LABEL
            else:
                text = dlp_processed
    if output_filter is not None:
        of_processed, of_result = output_filter.apply(text)
        if of_result.matched:
            counters["output_filter"] = counters.get("output_filter", 0) + 1
            if of_result.action == "block":
                text = _OUTPUT_FILTER_BLOCK_LABEL
            else:
                text = of_processed
    return text


def _cap(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Apply the section cap and append a single truncation marker."""
    if len(items) <= SECTION_CAP:
        return list(items)
    kept = list(items[:SECTION_CAP])
    kept.append({"truncated": len(items) - SECTION_CAP})
    return kept


def _build_turns(prompt_meta: dict[str, Any]) -> list[dict[str, Any]]:
    """Build the 'turns' section from prompt_meta['context_turns']."""
    raw = prompt_meta.get("context_turns") or []
    out: list[dict[str, Any]] = []
    for entry in raw:
        if isinstance(entry, dict):
            message_id = entry.get("id") or entry.get("message_id") or ""
            role = entry.get("role", "")
        elif isinstance(entry, str):
            message_id = entry
            role = ""
        else:
            continue
        if not message_id:
            continue
        out.append({"message_id": str(message_id), "role": str(role)})
    return out


def _build_memory(
    prompt_meta: dict[str, Any],
    dlp_scanner: DlpScanner | None,
    output_filter: OutputContentFilter | None,
    counters: dict[str, int],
) -> list[dict[str, Any]]:
    """Memory from #921's prompt_meta['memory_recall_items']."""
    raw = prompt_meta.get("memory_recall_items") or []
    out: list[dict[str, Any]] = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        fqn = item.get("fqn") or ""
        if not fqn:
            continue
        out.append(
            {
                "fqn": _apply_safety(str(fqn), dlp_scanner, output_filter, counters),
                "scope": str(item.get("scope", "")),
                "category": str(item.get("category", "")),
                "distance": item.get("distance"),
            }
        )
    return out


def _build_sources(
    prompt_meta: dict[str, Any],
    dlp_scanner: DlpScanner | None,
    output_filter: OutputContentFilter | None,
    counters: dict[str, int],
) -> list[dict[str, Any]]:
    """Sources from prompt_meta['rag_sources'] (shape: {label, type, source_id})."""
    raw = prompt_meta.get("rag_sources") or []
    out: list[dict[str, Any]] = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        label = item.get("label") or ""
        out.append(
            {
                "label": _apply_safety(str(label), dlp_scanner, output_filter, counters),
                "type": str(item.get("type", "")),
                "source_id": str(item.get("source_id", "") or ""),
            }
        )
    return out


def _build_tools(
    stored_assistant_message: dict[str, Any] | None,
    dlp_scanner: DlpScanner | None,
    output_filter: OutputContentFilter | None,
    counters: dict[str, int],
) -> list[dict[str, Any]]:
    """Tools come from the STORED message's `tool_calls` list.

    Reading from `ai_messages` would over-count because
    `_load_conversation_messages` at ``cli/repl.py`` emits one extra
    ``role="tool"`` entry per stored tool call.
    """
    if not stored_assistant_message:
        return []
    raw = stored_assistant_message.get("tool_calls") or []
    out: list[dict[str, Any]] = []
    for tc in raw:
        if not isinstance(tc, dict):
            continue
        tc_id = tc.get("id") or ""
        name = tc.get("tool_name") or tc.get("name") or ""
        if not tc_id and not name:
            continue
        out.append(
            {
                "id": str(tc_id),
                "name": _apply_safety(str(name), dlp_scanner, output_filter, counters),
            }
        )
    return out


def _build_packs(
    pack_list: list[dict[str, Any]] | None,
    prompt_meta: dict[str, Any],
    dlp_scanner: DlpScanner | None,
    output_filter: OutputContentFilter | None,
    counters: dict[str, int],
) -> list[dict[str, Any]]:
    """Surface only packs that actually contributed to the current turn.

    ``pack_list`` is the full inventory (``packs.list_packs(db)``).
    ``prompt_meta["pack_attachments"]`` is the per-turn attachment
    decision emitted by the router (namespace/name pairs). The
    intersection is what this turn actually saw.
    """
    attachments = prompt_meta.get("pack_attachments") or []
    attached_keys: set[tuple[str, str]] = set()
    scope_by_key: dict[tuple[str, str], str] = {}
    for att in attachments:
        if not isinstance(att, dict):
            continue
        ns = att.get("namespace") or ""
        name = att.get("name") or ""
        if ns and name:
            key = (str(ns), str(name))
            attached_keys.add(key)
            scope_by_key[key] = str(att.get("scope", "") or "")
    out: list[dict[str, Any]] = []
    for pack in pack_list or []:
        if not isinstance(pack, dict):
            continue
        ns = pack.get("namespace") or ""
        name = pack.get("name") or ""
        key = (str(ns), str(name))
        if key not in attached_keys:
            continue
        label = f"{ns}/{name}"
        out.append(
            {
                "namespace": str(ns),
                "name": _apply_safety(str(name), dlp_scanner, output_filter, counters),
                "label": _apply_safety(label, dlp_scanner, output_filter, counters),
                "scope": scope_by_key.get(key, ""),
            }
        )
    return out


def build_attribution(
    prompt_meta: dict[str, Any] | None,
    stored_assistant_message: dict[str, Any] | None,
    pack_list: list[dict[str, Any]] | None,
    *,
    dlp_scanner: DlpScanner | None = None,
    output_filter: OutputContentFilter | None = None,
) -> AttributionSnapshot:
    """Build the per-turn attribution snapshot.

    Pure function; all I/O lives in the callers. Accepts the live
    request-scoped safety scanners when the runtime has them; tests
    (and paths where redaction is disabled) pass ``None`` to get
    pass-through behaviour.
    """
    pm = prompt_meta or {}
    counters: dict[str, int] = {"dlp": 0, "output_filter": 0}

    turns = _cap(_build_turns(pm))
    memory = _cap(_build_memory(pm, dlp_scanner, output_filter, counters))
    sources = _cap(_build_sources(pm, dlp_scanner, output_filter, counters))
    tools = _cap(_build_tools(stored_assistant_message, dlp_scanner, output_filter, counters))
    packs = _cap(_build_packs(pack_list, pm, dlp_scanner, output_filter, counters))

    return AttributionSnapshot(
        turns=turns,
        memory=memory,
        sources=sources,
        tools=tools,
        packs=packs,
        dlp_match_count=counters.get("dlp", 0),
        output_filter_match_count=counters.get("output_filter", 0),
    )


def serialize_attribution(snapshot: AttributionSnapshot) -> dict[str, Any]:
    """Convert the snapshot to a plain dict suitable for JSON wire transport."""
    return asdict(snapshot)
