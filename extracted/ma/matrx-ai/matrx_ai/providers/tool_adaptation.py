"""THE call-time tool adaptation — the ONE place a model/provider limit removes a tool.

Owner rule (Arman, 2026-10-03; common-docs ``systems/agents/agent-tools/TOOL-SOURCES.md``
rule L): the core prepares a call without concern for the specific model (L1). A separate
late layer (L2, here, at the provider boundary) adapts it to the model/provider. It may
remove or translate, never add for a core reason, and **every removal is announced** to the
person/creator — one typed ``WarningPayload`` per removal, with a stable code per reason —
and recorded on the turn's request snapshot.

The reasons a tool is removed, each with its stable code:

* ``tools_removed_no_function_calling`` — the model does not accept tools
  (``supports_function_calling`` is the ONLY model fact that removes tools);
* ``tools_removed_search_unsupported`` — a provider-hosted search the model does not host;
* ``tools_removed_search_json_mode`` — OpenAI hosted web search refused beside JSON mode;
* ``tools_removed_schema_conflict`` — an endpoint that refuses tools combined with
  structured output (Cerebras / Groq);
* ``tools_removed_grammar_budget`` — Anthropic's compiled grammar (schema + tools) over budget.

The gates that decide are sync (``unified_client.apply_capability_gates``); they return
:class:`ToolAdaptation` records and the async dispatch calls :func:`announce_tool_adaptations`.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

from matrx_utils import vcprint

NO_FUNCTION_CALLING = "tools_removed_no_function_calling"
SEARCH_UNSUPPORTED = "tools_removed_search_unsupported"
SEARCH_JSON_MODE = "tools_removed_search_json_mode"
SCHEMA_CONFLICT = "tools_removed_schema_conflict"
GRAMMAR_BUDGET = "tools_removed_grammar_budget"
#: A TRANSLATION, not a removal (TOOL-SOURCES.md "the request is never denied"): the
#: provider's built-in web search became our ``web`` tool for a model that has none.
WEB_SEARCH_TRANSLATED = "tools_translated_web_search"

#: Our registered server tool that carries web search + page reading.
WEB_TOOL = "web"

#: The provider-hosted tool flags the call-time layer may translate or drop. The live config
#: keeps the AUTHORED values (restored right after the wire copy is built), so a later call on
#: a model that hosts them uses them again.
INTERNAL_TOOL_FLAGS = ("internal_web_search", "internal_x_search", "internal_url_context")

TOOL_ADAPTATION_CODES = frozenset(
    {
        NO_FUNCTION_CALLING,
        SEARCH_UNSUPPORTED,
        SEARCH_JSON_MODE,
        SCHEMA_CONFLICT,
        GRAMMAR_BUDGET,
        WEB_SEARCH_TRANSLATED,
    }
)


def authored_tool_flags(config: Any) -> dict[str, Any]:
    """The hosted-tool flags as authored, before the call-time layer adapts them."""
    return {flag: getattr(config, flag, None) for flag in INTERNAL_TOOL_FLAGS}


def apply_wire_additions(wire_config: Any, adaptations: list[ToolAdaptation] | None) -> None:
    """Put each translation's added tools on the PROVIDER copy only (never the live config)."""
    added = [name for a in adaptations or [] for name in a.added]
    if not added:
        return
    tools = list(getattr(wire_config, "tools", None) or [])
    for name in added:
        if name not in tools:
            tools.append(name)
    wire_config.tools = tools


def restore_tool_flags(config: Any, flags: dict[str, Any]) -> None:
    """Put the authored flags back on the LIVE config once the wire copy carries the adapted ones."""
    for flag, value in flags.items():
        if hasattr(config, flag):
            setattr(config, flag, value)

#: Field on the turn's ``chat.request_snapshot.metadata`` (staged under
#: ``matrx_ai.orchestrator.snapshot_metadata.REQUEST_SNAPSHOT_METADATA_KEY``).
SNAPSHOT_FIELD = "tool_adaptations"

_USER_MESSAGES = {
    NO_FUNCTION_CALLING: "This model can't use tools, so its tools were off for this reply.",
    SEARCH_UNSUPPORTED: "This model has no built-in search, so search was off for this reply.",
    SEARCH_JSON_MODE: "Web search was off for this reply so the structured answer could run.",
    SCHEMA_CONFLICT: "Tools were off for this reply so the structured answer could run.",
    GRAMMAR_BUDGET: "Tools were off for this reply so the structured answer could fit.",
    WEB_SEARCH_TRANSLATED: "This model has no built-in search, so it searched with our web tool.",
}


@dataclass(frozen=True)
class ToolAdaptation:
    """One removal the late layer made, and why."""

    code: str
    model: str | None
    wire_format: str | None
    removed: list[str]
    reason: str
    detail: dict[str, Any] = field(default_factory=dict)
    #: Tools added in place of what was removed (a translation), e.g. ``["web"]``.
    added: list[str] = field(default_factory=list)

    def as_record(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "model": self.model,
            "wire_format": self.wire_format,
            "removed": list(self.removed),
            "reason": self.reason,
            **({"added": list(self.added)} if self.added else {}),
            **({"detail": self.detail} if self.detail else {}),
        }


#: ``AppContext.metadata`` key: what context this turn's model can take (``context_reach``),
#: stamped by the host's tool funnel so the context receipt says what reaches the model.
CONTEXT_REACH_KEY = "model_context_reach"


@dataclass(frozen=True)
class ContextReach:
    """What prepared context a model can take, as the call-time layer will deliver it.

    ``reads_turn_context`` — the per-turn context channel reaches the model: a chat/text
    model renders it; an image / audio / video model folds its prompt from the person's
    text alone, so per-turn context is never spoken or drawn.
    ``fetches`` — the model can call the ``context`` tool, so on-request values reach it.
    """

    reads_turn_context: bool
    fetches: bool

    def as_metadata(self) -> dict[str, bool]:
        return {"reads_turn_context": self.reads_turn_context, "fetches": self.fetches}


def context_reach(caps: Any) -> ContextReach:
    reads = bool(getattr(caps, "produces_text", True)) and not any(
        getattr(caps, flag, False) for flag in ("produces_image", "produces_audio", "produces_video")
    )
    return ContextReach(
        reads_turn_context=reads,
        fetches=bool(getattr(caps, "supports_function_calling", True)),
    )


#: The context-tool instructions inside the per-turn context channel — meaningless (and
#: misleading) to a model that cannot call tools, so the call-time strip removes them.
_FETCH_INSTRUCTION_ELEMENTS = re.compile(
    r"[ \t]*<(deferred_context_available|retrieval)\b[^>]*>.*?</\1>[ \t]*\n?", re.DOTALL
)


def strip_fetch_instructions(messages: Any) -> bool:
    """Remove the context-tool instructions from this turn's context channel. True if any went."""
    blocks = getattr(messages, "_turn_context_blocks", None)
    if not isinstance(blocks, dict):
        return False
    changed = False
    for slot, text in list(blocks.items()):
        if not isinstance(text, str):
            continue
        stripped = _FETCH_INSTRUCTION_ELEMENTS.sub("", text)
        if stripped != text:
            changed = True
            if stripped.strip():
                blocks[slot] = stripped
            else:
                blocks.pop(slot)
    return changed


def tool_surface_names(config: Any) -> list[str]:
    """The registered, inline and MCP tools on a config, named — what a tool-surface strip removes."""
    names: list[str] = []
    for tool in getattr(config, "tools", None) or []:
        names.append(str(tool if isinstance(tool, str) else getattr(tool, "name", tool)))
    for tool in getattr(config, "custom_tools", None) or []:
        names.append(str(getattr(tool, "name", None) or (tool.get("name") if isinstance(tool, dict) else tool)))
    for server in getattr(config, "mcp_servers", None) or []:
        label = server.get("name") or server.get("url") if isinstance(server, dict) else server
        names.append(f"mcp:{label}")
    return names


def _stage_on_snapshot(record: dict[str, Any]) -> None:
    """Append the record to the turn's staged request-snapshot metadata (iteration 1 writes it)."""
    from matrx_connect.context.app_context import try_get_app_context

    from matrx_ai.orchestrator.snapshot_metadata import REQUEST_SNAPSHOT_METADATA_KEY

    ctx = try_get_app_context()
    metadata = getattr(ctx, "metadata", None) if ctx is not None else None
    if not isinstance(metadata, dict):
        return
    staged = dict(metadata.get(REQUEST_SNAPSHOT_METADATA_KEY) or {})
    staged[SNAPSHOT_FIELD] = [*(staged.get(SNAPSHOT_FIELD) or []), record]
    metadata[REQUEST_SNAPSHOT_METADATA_KEY] = staged


_ANNOUNCED_KEY = "_tool_adaptations_announced"


def _already_announced(record: dict[str, Any]) -> bool:
    """Once per request: a tool loop re-adapts every round; the person hears it once."""
    from matrx_connect.context.app_context import try_get_app_context

    ctx = try_get_app_context()
    metadata = getattr(ctx, "metadata", None) if ctx is not None else None
    if not isinstance(metadata, dict):
        return False
    key = "|".join(
        [
            str(getattr(ctx, "request_id", None)),
            record["code"],
            str(record.get("model")),
            ",".join(record.get("removed") or ()),
        ]
    )
    seen = metadata.get(_ANNOUNCED_KEY)
    if not isinstance(seen, list):
        seen = metadata[_ANNOUNCED_KEY] = []
    if key in seen:
        return True
    seen.append(key)
    return False


#: Issue-class prefix for adaptations nobody could be told about live.
ISSUE_CLASS_PREFIX = "tool_adaptation"


async def _record_durably(adaptation: ToolAdaptation) -> None:
    try:
        from matrx_ai.ops.issue_capture import capture_issue

        await capture_issue(
            f"{ISSUE_CLASS_PREFIX}.{adaptation.code}",
            error_type=adaptation.code,
            provider=str(adaptation.wire_format or "unknown").split("_")[0],
            model=adaptation.model,
            is_retryable=False,
            was_recovered=True,
            severity="low",
            detail=adaptation.as_record(),
        )
    except Exception as exc:  # noqa: BLE001 — a broken sink never breaks the call
        vcprint(f"[tool_adaptation] durable record failed: {exc!r}", color="red")


async def announce_tool_adaptations(
    adaptations: list[ToolAdaptation] | None, *, emitter: Any = None
) -> None:
    """Say every removal: one stream warning each, plus a snapshot record and a console line.

    Never raises — an announcement failure must not fail the call, and the console line
    below fires first so a broken emitter still leaves a trace.
    """
    for adaptation in adaptations or []:
        record = adaptation.as_record()
        if _already_announced(record):
            continue  # the same adaptation on a later round of this request's tool loop
        vcprint(
            data=record,
            title=f"⚠️  TOOL ADAPTATION [{adaptation.model}]: {adaptation.reason}",
            color="yellow",
            verbose=True,
        )
        try:
            _stage_on_snapshot(record)
        except Exception as exc:  # noqa: BLE001
            vcprint(f"[tool_adaptation] snapshot record not staged: {exc!r}", color="yellow")
        try:
            from matrx_connect.context.app_context import try_get_app_context
            from matrx_connect.context.events import WarningPayload

            ctx = try_get_app_context()
            target = emitter or (getattr(ctx, "emitter", None) if ctx is not None else None)
            if target is None:
                # No one to tell (a batch build, a background run): the adaptation is still
                # recorded durably, never left as a console line.
                await _record_durably(adaptation)
                continue
            await target.send_warning(
                WarningPayload(
                    code=adaptation.code,
                    system_message=(
                        f"{adaptation.reason} Removed: {', '.join(adaptation.removed) or 'none'}."
                        + (f" Added: {', '.join(adaptation.added)}." if adaptation.added else "")
                    ),
                    user_message=_USER_MESSAGES.get(adaptation.code),
                    level="low",
                    recoverable=True,
                    metadata={
                        "model": adaptation.model,
                        "wire_format": adaptation.wire_format,
                        "removed": list(adaptation.removed),
                        **({"added": list(adaptation.added)} if adaptation.added else {}),
                    },
                )
            )
        except Exception as exc:  # noqa: BLE001
            vcprint(f"[tool_adaptation] warning not emitted: {exc!r}", color="yellow")


__all__ = [
    "apply_wire_additions",
    "INTERNAL_TOOL_FLAGS",
    "WEB_SEARCH_TRANSLATED",
    "WEB_TOOL",
    "authored_tool_flags",
    "restore_tool_flags",
    "CONTEXT_REACH_KEY",
    "ContextReach",
    "context_reach",
    "strip_fetch_instructions",
    "GRAMMAR_BUDGET",
    "NO_FUNCTION_CALLING",
    "SCHEMA_CONFLICT",
    "SEARCH_JSON_MODE",
    "SEARCH_UNSUPPORTED",
    "SNAPSHOT_FIELD",
    "TOOL_ADAPTATION_CODES",
    "ToolAdaptation",
    "announce_tool_adaptations",
    "tool_surface_names",
]
