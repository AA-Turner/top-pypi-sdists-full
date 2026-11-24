"""LATE TOOLS: a tool that joins a conversation after it started rides AFTER the cache line.

On every provider the wire ``tools`` list is the FIRST thing in the cached prefix, so a tool added
mid-conversation (``UnifiedConfig.dynamic_tools``: find_tools results, a bundle opened mid-loop,
page/surface tools, context tools) re-wrote the whole cached system prompt and history. Behind knob
``agents.prompt_cache.late_tools_enabled`` (ships OFF; scope ``late_tools_scope``: ``enrolled`` =
only agents in the always-warm prompt cache, or ``all``) such a tool is taken out of the wire list
and its full definition is delivered as ONE text block in the trailing channel (after the last
cache mark). The model runs it through the declared gateway ``use_tool`` (job_key + inputs) or,
where the model does it natively (Anthropic, Gemini), by its own name — the executor's allowlist is
built from ``config.tools``, so a late tool is exactly as callable as a declared one.

Measured facts this rests on: common-docs/systems/agents/projects/agent-evaluation/research/provider-caching.md
§ "Tool definitions and calls" (every provider accepts history calls to tools not in ``tools``;
OpenAI never calls an announced-only tool by name; Groq and Cohere reject undeclared names).

Never silent: a split is noted on the send (``note_capture``) and kept for the send path
(``take_late_tools``); a knob that is on where the split cannot happen (no gateway offered, a
translator without the trailing channel) is said once per process.
"""

from __future__ import annotations

import json
from contextvars import ContextVar
from dataclasses import dataclass
from typing import Any

from matrx_utils import vcprint

#: The declared gateway a late tool runs through (a registered native tool the host provides —
#: aidream ``services/tool_catalog/discovery.py::use_tool``). A split never happens without it.
GATEWAY_TOOL = "use_tool"

#: The turn-context slot prefix (``late_tools:<wire name>``, one per tool) late tools ride in when the send boundary places this turn's
#: platform block before the person's typed text (``send_boundary.order_for_wire``): THE REQUEST
#: ENDS WITH WHAT THE PERSON TYPED (Arman, 2026-10-19). The block is frozen with the turn's other
#: slots, so every send of the turn replays it byte for byte (the cache line holds), and a tool that
#: turns late mid-loop rides the tail as the slot's current copy, after the tool result.
LATE_TOOLS_SLOT = "late_tools"

#: The chat translator families that deliver late tools (their ``SUPPORTS_LATE_TOOLS``), so the
#: send boundary decides exactly what the translator would. Guard:
#: ``tests/test_late_tools_ride_before_the_typed_text.py`` (this set equals the translators' flags).
LATE_TOOLS_PROVIDERS: frozenset[str] = frozenset({"anthropic", "google", "openai"})

#: The families whose models never call an announced-only (late) tool by its name, only through the gateway
#: (OpenAI's Responses API, measured: provider-caching.md § "Tool definitions and calls"; on 2026-11-19 its models
#: also wrote ``job_key="functions.skill"`` or left job_key out). A host that tells a model how to call late tools
#: tells these families to use ``use_tool`` (aidream ``tooling/chat_mode.py``, item ``chat_core_gateway``).
GATEWAY_ONLY_PROVIDERS: frozenset[str] = frozenset({"openai"})

#: What this process already said once (knob on where the split cannot happen).
_ANNOUNCED: set[str] = set()


@dataclass(frozen=True, slots=True)
class LateToolSend:
    """What one send moved out of the wire ``tools`` list (wire names, first-added order)."""

    provider: str
    names: tuple[str, ...]


_LAST: ContextVar[LateToolSend | None] = ContextVar("matrx_ai_late_tools", default=None)


def _announce_once(key: str, message: str) -> None:
    if key in _ANNOUNCED:
        return
    _ANNOUNCED.add(key)
    # A degraded-but-correct send (the tools stay in the list), so a once-per-process yellow notice, never red/ERROR:
    # feedback 0154af1e filed the no-gateway case as an error though nothing was lost.
    vcprint(f"[late tools] {message}", color="yellow")
    try:
        from matrx_ai.providers.request_capture import note_capture

        note_capture(f"Late tools: {message}")
    except Exception:  # noqa: BLE001 — an observer never breaks a send
        pass


#: ``AppContext.metadata`` key a HOST sets True on a run whose added tools must ride late whatever the scope
#: knob says (aidream chat conversion, ``aidream/services/tooling/chat_mode.py``: a non-chat agent's conversation
#: that gains the chat tools on a later turn — on the wire list they would rewrite its cached prompt every
#: conversation). The host refuses that run where late tools cannot be delivered; the knob itself still gates.
FORCED_KEY = "late_tools_forced"


def _forced() -> bool:
    from matrx_connect.context.app_context import try_get_app_context

    ctx = try_get_app_context()
    metadata = getattr(ctx, "metadata", None) if ctx is not None else None
    return isinstance(metadata, dict) and metadata.get(FORCED_KEY) is True


def _in_scope() -> bool:
    from matrx_ai.config.cache_plan import LATE_TOOLS_SCOPE_ALL, late_tools_scope

    if late_tools_scope() == LATE_TOOLS_SCOPE_ALL or _forced():
        return True
    from matrx_ai.providers import prompt_warm

    return prompt_warm.profile_for(prompt_warm.current_agent_id()) is not None


def _resolved(names: Any) -> list[str]:
    from matrx_ai.tools.registry import ToolRegistry

    registry = ToolRegistry.get_instance()
    out: list[str] = []
    for entry in names or []:
        if not isinstance(entry, str) or not entry:
            continue
        try:
            resolved = registry._resolve_tool_name(entry)
        except Exception:  # noqa: BLE001 — an unresolvable name keeps its spelling
            resolved = None
        out.append(resolved or entry)
    return out


def late_tool_names(config: Any, *, provider: str, supported: bool) -> list[str]:
    """The internal names this send delivers as late tools (first-added order), or ``[]``.

    Late = in ``dynamic_tools``, offered this send (``config.tools``), not one of the agent's own
    authored tools, and never the gateway itself. Pure and deterministic for one config, so the
    wire split (``build_provider_tools``) and the trailing block always agree.
    """
    dynamic = getattr(config, "dynamic_tools", None) or []
    if not dynamic or not getattr(config, "messages", None) or not getattr(config, "tools", None):
        return []
    from matrx_ai.config.cache_plan import late_tools_enabled

    if not late_tools_enabled() or not _in_scope():
        return []
    from matrx_ai.config.wire_names import to_wire_name

    offered = {to_wire_name(name): name for name in _resolved(config.tools)}
    authored = {to_wire_name(name) for name in _resolved(getattr(config, "authored_tools", None))}
    gateway = to_wire_name(GATEWAY_TOOL)
    # A name this conversation already sent in its tools list stays there (declaration_ledger: the list
    # is stable for the conversation's life), so it is never ALSO delivered as a late tool.
    from matrx_ai.tools.declaration_ledger import held_names

    held = held_names(provider)
    late: list[str] = []
    for name in _resolved(dynamic):
        wire = to_wire_name(name)
        if wire in offered and wire not in authored and wire != gateway and wire not in held and offered[wire] not in late:
            late.append(offered[wire])
    if not late:
        return []
    if gateway not in offered:
        _announce_once(
            "no_gateway",
            f"knob agents.prompt_cache.late_tools_enabled is on, but {GATEWAY_TOOL!r} is not offered "
            "on this run, so tools added mid-conversation stay in the tools list (attach "
            f"{GATEWAY_TOOL!r} to the agent to move them after the cache line).",
        )
        return []
    if not supported:
        _announce_once(
            f"unsupported:{provider}",
            f"knob agents.prompt_cache.late_tools_enabled is on, but the {provider!r} translator does "
            "not place late tools after its cache line; tools added mid-conversation stay in its "
            "tools list.",
        )
        return []
    return late


def record_split(provider: str, wire_names: list[str]) -> None:
    """Say that this send moved ``wire_names`` out of the tools list (snapshot note + send state)."""
    _LAST.set(LateToolSend(provider=provider, names=tuple(wire_names)))
    try:
        from matrx_ai.providers.request_capture import note_capture

        note_capture(
            f"Late tools: {len(wire_names)} tool(s) added mid-conversation ride after the cache line "
            f"as text, not in the tools list ({', '.join(wire_names)}); the model runs them through "
            f"{GATEWAY_TOOL} or by name (knob agents.prompt_cache.late_tools_enabled)."
        )
    except Exception:  # noqa: BLE001 — an observer never breaks a send
        pass


def take_late_tools() -> LateToolSend | None:
    """The newest send's split in this context (read by the send path / prompt-warm observer)."""
    value = _LAST.get()
    _LAST.set(None)
    return value


def _schema_of(decl: dict[str, Any]) -> Any:
    for key in ("input_schema", "parameters"):
        if key in decl:
            return decl[key]
    fn = decl.get("function")
    if isinstance(fn, dict):
        return fn.get("parameters")
    return None


#: The header of a late-tools block delivered as THIS send's offer (the translator's trailing channel, the system
#: fallback): there the block is the whole offer, so it says the tools are available. A definition staged in turn
#: context carries no header (``late_tools_slots``): it may be replayed on later turns, where only the newest
#: turn's names slot says what is available (``CARRIED_SLOT``).
OFFER_HEADER = (
    "These tools are available now. Call one by its name if you can; otherwise "
    f"call {GATEWAY_TOOL} with job_key=<name> and inputs=<object>."
)


def _canonical_schema(schema: Any) -> Any:
    """``schema`` with every ``required`` name list sorted (a set in JSON Schema; its order follows the parameters'
    order, which a database round trip changes)."""
    if isinstance(schema, dict):
        out = {key: _canonical_schema(value) for key, value in schema.items()}
        required = out.get("required")
        if isinstance(required, list) and all(isinstance(name, str) for name in required):
            out["required"] = sorted(required)
        return out
    if isinstance(schema, list):
        return [_canonical_schema(value) for value in schema]
    return schema


def _render_entry(name: str, description: str, schema: Any) -> str:
    # Canonical: key order never varies between processes or sends (a varying order read as "changed" every turn).
    rendered = json.dumps(_canonical_schema(schema), ensure_ascii=False, sort_keys=True)
    return f"### {name}\n{description.strip()}\n{_SCHEMA_LINE}{rendered}"


def render_late_tools_block(declarations: list[dict[str, Any]], *, header: bool = True) -> str | None:
    """ONE text block: the offer header (``header=False``: none), then each tool's name, description and input JSON
    schema (canonical JSON)."""
    from matrx_ai.config.wire_names import to_wire_name

    entries: list[str] = []
    for decl in declarations:
        if not isinstance(decl, dict):
            continue
        name = decl.get("name")
        if not isinstance(name, str) and isinstance(decl.get("function"), dict):
            name = decl["function"].get("name")
        if not isinstance(name, str) or not name:
            continue
        description = decl.get("description")
        if description is None and isinstance(decl.get("function"), dict):
            description = decl["function"].get("description")
        schema = _schema_of(decl) or {"type": "object", "properties": {}}
        entries.append(_render_entry(to_wire_name(name), description or "", schema))
    if not entries:
        return None
    opening = f"<late_tools>\n{OFFER_HEADER}\n\n" if header else "<late_tools>\n"
    return opening + "\n\n".join(entries) + "\n</late_tools>"


class _NamesConfig:
    """The only two fields ``build_provider_tools`` reads for a plain list of registered names."""

    def __init__(self, names: list[str]):
        self.tools = list(names)
        self.custom_tools: list[Any] = []


def _declarations_for(names: list[str]) -> list[dict[str, Any]]:
    """Anthropic-shaped declarations for ``names``, through the one boundary (the one order and
    wire names), untracked so the conversation's declaration ledger is never written."""
    from matrx_ai.providers.anthropic.translator import AnthropicTranslator

    return AnthropicTranslator().build_provider_tools(_NamesConfig(names), "anthropic", tracked=False)


def late_tools_text(config: Any, *, provider: str, supported: bool) -> str | None:
    """The late-tools block this send delivers (``late_tool_names`` rendered), or None."""
    names = late_tool_names(config, provider=provider, supported=supported)
    if not names:
        return None
    return render_late_tools_block(_declarations_for(names))


def late_tools_slots(config: Any, *, provider: str, supported: bool) -> dict[str, str]:
    """One turn-context slot per late tool (``late_tools:<wire name>`` → its own block), or ``{}``.

    One slot per tool, so a tool that turns late mid-loop rides the tail alone (the turn's frozen
    block already holds the others) instead of re-sending every definition as the slot's new copy."""
    names = late_tool_names(config, provider=provider, supported=supported)
    if not names:
        return {}
    from matrx_ai.config.wire_names import to_wire_name
    slots: dict[str, str] = {}
    for name in names:
        block = render_late_tools_block(_declarations_for([name]), header=False)
        if block:
            slots[f"{LATE_TOOLS_SLOT}:{to_wire_name(name)}"] = block
    return slots


def is_late_tools_slot(slot: Any) -> bool:
    return isinstance(slot, str) and (slot == LATE_TOOLS_SLOT or slot.startswith(f"{LATE_TOOLS_SLOT}:"))


# ---------------------------------------------------------------------------------------------------------------
# A WARM SEND ONLY APPENDS (2026-11-19, staff thread 3af9e95c: 30 late tools = 67,286 chars re-sent uncached on
# every ask, inside the newest turn's block, after the rolling cache mark). A late tool's definition stays on the
# person turn whose send first placed it (``typed_text_last.STORED_LATE_TOOLS_KEY``, or inside that turn's kept
# whole block); every later send replays it there, inside the cached prefix, and a later turn's block carries only
# the definitions that are new or changed (``delta_slots``) plus ONE short slot naming which of the earlier ones
# are available now (``CARRIED_SLOT``). The send boundary decides it (``send_boundary._stage_late_tools``).
# ---------------------------------------------------------------------------------------------------------------

#: THE ONE STATEMENT OF WHICH LATE TOOLS ARE AVAILABLE: staged in the newest turn whenever late tools ride turn
#: context, naming exactly this send's offered late tools (new ones defined beside it, the rest defined on the
#: earlier turns that carry them). A definition never claims availability itself (review of c8a79d95939: a revoked
#: tool kept "These tools are available now" in its old carrier). A late-tools slot (it rides and clears with them,
#: and tells the translator the boundary carried them), never a definition. The key keeps its first spelling:
#: stored kept slots name it.
CARRIED_SLOT = f"{LATE_TOOLS_SLOT}:~carried"

#: The frame of a carrier: an earlier turn's late tool definitions, replayed where that turn's send placed them.
CARRIER_OPEN = '<turn_context source="platform" slot="late_tools">'
CARRIER_NOTE = (
    "Tool definitions the platform added on this turn. The newest turn's context says which tools are "
    "available now."
)


def definition_slots(slots: Any) -> dict[str, str]:
    """The late tool DEFINITION slots of ``slots`` (``late_tools:<wire name>`` → block), never the names slot."""
    if not isinstance(slots, dict):
        return {}
    return {
        str(slot): block
        for slot, block in slots.items()
        if is_late_tools_slot(slot) and slot != CARRIED_SLOT and isinstance(block, str) and block
    }


def _wire_name_of(slot: str) -> str:
    return slot.split(":", 1)[1] if ":" in slot else slot


def render_available_names(available: list[str]) -> str:
    """The names slot (``CARRIED_SLOT``): exactly the late tools this send offers (wire names, sorted)."""
    names = sorted(_wire_name_of(slot) for slot in available)
    body = (
        "Late tools you can call on this turn: " + ", ".join(names) + ". Call one by its name if you can; "
        f"otherwise call {GATEWAY_TOOL} with job_key=<name> and inputs=<object>. A tool defined in a late tools block "
        "block and not named here cannot be called now."
    )
    return f"<late_tools_available>\n{body}\n</late_tools_available>"


def delta_slots(live: dict[str, str], carried: dict[str, str]) -> dict[str, str]:
    """This turn's late-tools slots given what earlier turns on the wire already carry.

    A definition an earlier turn carries (same canonical digest, ``definition_digest``) is not sent again; a new or
    changed one is. ``CARRIED_SLOT`` names every late tool this send offers. Deterministic for one
    ``(live, carried)``; ``{}`` when nothing is offered."""
    if not live:
        return {}
    out = {
        slot: block for slot, block in live.items()
        if slot not in carried or definition_digest(carried[slot]) != definition_digest(block)
    }
    out[CARRIED_SLOT] = render_available_names(list(live))
    return out


def declared_wire_names(config: Any, live: dict[str, str]) -> frozenset[str]:
    """The wire names this send declares in its tools list (offered and not late): a carrier never defines one of
    them a second time."""
    from matrx_ai.config.wire_names import to_wire_name

    late = {_wire_name_of(slot) for slot in live}
    offered = {to_wire_name(name) for name in _resolved(getattr(config, "tools", None))}
    return frozenset(offered - late)


def retire_offer_header(text: str) -> str:
    """``text`` with the offer header taken out of every late-tools block in it: a REPLAYED definition (a kept
    block or a carrier stamped before 2026-11-19) never claims availability; the newest turn's names slot does."""
    return text.replace(f"<late_tools>\n{OFFER_HEADER}\n\n", "<late_tools>\n") if OFFER_HEADER in text else text


def canonical_definition(block: str) -> str:
    """A one-tool definition block rendered the canonical way (no header, canonical JSON); unchanged when it is not
    one whole definition."""
    entries = _entries(block) if isinstance(block, str) else []
    if len(entries) != 1:
        return block
    name, entry = entries[0]
    head, sep, schema_text = entry.rpartition("\n" + _SCHEMA_LINE)
    if not sep:
        return retire_offer_header(block)
    try:
        schema = json.loads(schema_text.strip())
    except ValueError:
        return retire_offer_header(block)
    return f"<late_tools>\n{_render_entry(name, head, schema)}\n</late_tools>"


_SCHEMA_LINE = "Input JSON schema: "


def _entries(text: str) -> list[tuple[str, str]]:
    """``(wire name, entry text)`` of every WHOLE definition in ``text`` (inside a closed ``<late_tools>`` block)."""
    import re

    found: list[tuple[str, str]] = []
    for block in re.findall(r"<late_tools>\n(.*?)\n</late_tools>", text, flags=re.S):
        parts = re.split(r"^### (\S+)$", block, flags=re.M)
        for at in range(1, len(parts) - 1, 2):
            found.append((parts[at], parts[at + 1]))
    return found


def _digest_of(name: str, entry: str) -> str:
    """The canonical digest of one definition: its name, description and input schema (key order and JSON spacing
    do not count), so the same definition rendered by another process or an older format compares equal."""
    import hashlib

    head, sep, schema_text = entry.rpartition("\n" + _SCHEMA_LINE)
    if not sep and entry.lstrip("\n").startswith(_SCHEMA_LINE):
        head, schema_text = "", entry.lstrip("\n")[len(_SCHEMA_LINE) :]
    try:
        schema: Any = json.loads(schema_text.strip()) if (sep or schema_text) else None
    except ValueError:
        schema = schema_text.strip()
    canonical = json.dumps(
        [name, head.strip(), _canonical_schema(schema)], sort_keys=True, separators=(",", ":"), ensure_ascii=False
    )
    return hashlib.sha256(canonical.encode("utf-8", "replace")).hexdigest()


def definition_digest(block: str) -> str | None:
    """The canonical digest of a one-tool definition block (``late_tools_slots`` value), or None when it holds no
    whole definition."""
    entries = _entries(block) if isinstance(block, str) else []
    if len(entries) != 1:
        return None
    return _digest_of(*entries[0])


def wire_definitions(texts: Any) -> list[tuple[str, str]]:
    """``(wire name, canonical digest)`` of every whole late tool definition in ``texts`` (one per occurrence)."""
    found: list[tuple[str, str]] = []
    for text in texts or []:
        if isinstance(text, str) and "<late_tools>" in text:
            found.extend((name, _digest_of(name, entry)) for name, entry in _entries(text))
    return found


def render_late_tools_carrier(slots: Any) -> str | None:
    """ONE text: the late tool definitions an earlier turn's send placed (slot order: by name), framed."""
    from matrx_ai.config.message_config import TURN_CONTEXT_CLOSE, turn_context_slot_order

    defined = definition_slots(slots)
    if not defined:
        return None
    body = "\n\n".join(canonical_definition(defined[slot]) for slot in turn_context_slot_order(defined))
    return "\n".join((CARRIER_OPEN, CARRIER_NOTE, "", body, TURN_CONTEXT_CLOSE))


def boundary_carries_late_tools(config: Any) -> bool:
    """True when the send boundary staged this send's late tools in turn-context slots."""
    messages = getattr(config, "messages", None)
    staged = getattr(messages, "_turn_context_blocks", None)
    return isinstance(staged, dict) and any(is_late_tools_slot(k) and v for k, v in staged.items())


def reset_for_tests() -> None:
    _ANNOUNCED.clear()
    _LAST.set(None)


__all__ = [
    "CARRIED_SLOT",
    "FORCED_KEY",
    "OFFER_HEADER",
    "canonical_definition",
    "declared_wire_names",
    "definition_digest",
    "definition_slots",
    "delta_slots",
    "render_available_names",
    "render_late_tools_carrier",
    "retire_offer_header",
    "wire_definitions",
    "GATEWAY_ONLY_PROVIDERS",
    "GATEWAY_TOOL",
    "LATE_TOOLS_PROVIDERS",
    "LATE_TOOLS_SLOT",
    "boundary_carries_late_tools",
    "is_late_tools_slot",
    "late_tools_slots",
    "late_tools_text",
    "LateToolSend",
    "late_tool_names",
    "record_split",
    "render_late_tools_block",
    "reset_for_tests",
    "take_late_tools",
]
