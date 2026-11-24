"""ALWAYS-WARM PROMPT CACHE — keep an enrolled agent's stable prompt cached on Anthropic.

For an agent the host enrolls (``configure_prompt_warm``), the Anthropic translator lays the
system channel out so the agent's OWN authored text is a byte-stable leading block that
every conversation shares, and caches it for an hour:

* block A = the agent's authored system text, cut at its first ``{{`` (``shared_text``),
  marked ``ttl: "1h"``;
* block B = the rest of the system text (date line, skills preamble, filled tail), with
  ``shared_text`` removed once, keeping its own mark when the 4-mark ceiling allows;
* when platform-added tools (surface/app, bundle, discovery, sandbox, inline) follow the authored
  tools, a 1h mark on the last authored tool, so the authored tool block is read across every
  conversation and surface too (the ledger puts the authored tools first).

Anthropic takes at most 4 marks and every 1h mark must precede every 5m mark. B's mark is
dropped first, then the tool mark. When ``shared_text`` is not in the system text nothing is
changed and the outcome is ``layout_miss``.

The REPLAYABLE PREFIX — ``{model, tools (exactly as sent), system: [block A], thinking,
output_config.effort}`` — is serialized once to text (never re-sorted: ``jsonb`` would re-sort
keys and change the bytes) and keyed by sha256 (``variant_key``). After every send the
observer receives the agent id, the key, the prefix text and the cache usage; the host
records it and may replay the prefix with ``send_keepalive`` (``max_tokens: 0``: a cache read
that refreshes the 1h timer, no output).

Nothing here ever blocks or breaks a send: every failure is announced once and the send
proceeds unchanged.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Callable
from contextvars import ContextVar
from dataclasses import dataclass, field
from typing import Any

from matrx_utils import vcprint

from matrx_ai.config.cache_marks import MAX_ANTHROPIC_CACHE_MARKS, cache_control

OUTCOME_HIT = "hit"
OUTCOME_COLD = "cold"
OUTCOME_BREAK = "break"
OUTCOME_LAYOUT_MISS = "layout_miss"
OUTCOME_ERROR = "error"

KIND_LIVE = "live"
KIND_KEEPALIVE = "keepalive"

KEEPALIVE_TEXT = "Keep-alive."


@dataclass(frozen=True, slots=True)
class WarmProfile:
    """What the host knows about one enrolled agent."""

    shared_text: str
    #: The authored prompt's full length (shared_text is its leading slice before any ``{{``).
    prompt_chars: int = 0
    #: Enrolled, but its prompt is not loaded on this process yet: the send goes out unwarmed and is
    #: RECORDED as a layout miss with this reason, never skipped in silence.
    pending_reason: str = ""


@dataclass(slots=True)
class WarmLayout:
    """What the translator did for one send (read back by the send path)."""

    agent_id: str
    model: str
    applied: bool
    shared_chars: int
    prompt_chars: int
    prefix_text: str = ""
    variant_key: str = ""
    marks_dropped: list[str] = field(default_factory=list)
    #: Why the layout was not applied (empty when applied, or when the text simply was not found).
    miss_reason: str = ""


@dataclass(frozen=True, slots=True)
class WarmObservation:
    """One send's facts for the host's ledger."""

    kind: str
    agent_id: str
    model: str
    variant_key: str
    prefix_text: str
    applied: bool
    shared_chars: int
    prompt_chars: int
    conversation_id: str | None
    organization_id: str | None
    input_tokens: int
    output_tokens: int
    cache_read_tokens: int
    cache_write_5m_tokens: int
    cache_write_1h_tokens: int
    error: str | None = None
    miss_reason: str = ""


ProfileReader = Callable[[str], "WarmProfile | None"]
Observer = Callable[[WarmObservation], Any]

_PROFILE_READER: ProfileReader | None = None
_OBSERVER: Observer | None = None
_ANNOUNCED: set[str] = set()
_LAYOUT: ContextVar[WarmLayout | None] = ContextVar("prompt_warm_layout", default=None)


def configure_prompt_warm(profile_reader: ProfileReader | None, observer: Observer | None) -> None:
    """Host seam: who is enrolled (and their shared text), and where observations go."""
    global _PROFILE_READER, _OBSERVER
    _PROFILE_READER = profile_reader
    _OBSERVER = observer


def _announce_once(key: str, message: str) -> None:
    if key in _ANNOUNCED:
        return
    _ANNOUNCED.add(key)
    vcprint(f"[prompt warm] {message}", color="red")


def shared_text_from_authored(text: str | None, declared: Any = ()) -> str:
    """The shareable leading slice of an authored system prompt, AS IT IS SENT.

    THE VARIABLE RULE decides it (``config/template_substitution.py``, the one implementation): only a DECLARED
    slot ``{{name}}`` (or its section ``{{#name}}`` / ``{{^name}}``, or a declared block ``{{<name>}}``) changes
    per run, so the slice stops at the first of those; every other ``{{...}}`` is left exactly as written, and an
    escape ``{{!name}}`` is sent as ``{{name}}`` — so the slice is unescaped the same way. Cutting at the first
    ``{{`` of any kind made a prompt that TEACHES the variable syntax (Agent Structure Builder) share only its
    first 1,387 of 14,626 characters."""
    from matrx_ai.config.template_substitution import first_declared_slot, substitute_authored

    if not text:
        return ""
    names = sorted({str(n) for n in declared or () if str(n)}, key=len, reverse=True)
    start = first_declared_slot(text, names)
    cut = len(text) if start is None else start
    head = text[:cut]
    shared = substitute_authored(head, head, {n: "" for n in names}, str, unescape=True, sections=False)
    return shared.rstrip()


def _loop_pins() -> dict[str, Any] | None:
    """The running provider loop's pinned warm answers (``ExecutionState.warm_profile_pins``), or None
    outside an executor loop (a direct translator call decides per send, as before)."""
    try:
        from matrx_ai.orchestrator.execution_state import try_get_execution_state

        state = try_get_execution_state()
    except Exception:
        return None
    return state.warm_profile_pins if state is not None else None


def profile_for(agent_id: str | None) -> WarmProfile | None:
    """The agent's warm profile for this send — decided ONCE per provider loop.

    The layout this answer chooses IS the system channel's shape on the wire, so it may not change
    between rounds of one loop: the first round's answer (loaded, pending, or None) is pinned on the
    loop's ``ExecutionState`` and every later round reuses it. A profile that finishes loading or
    refreshes mid-loop takes effect on the next loop, never by re-laying out a prefix the provider
    has already cached (live 2026-11-18, three loops: round 1 unwarmed while loading, round 2 warm,
    0 read and 37k-42k tokens re-written at the 1h price)."""
    if not agent_id or _PROFILE_READER is None:
        return None
    pins = _loop_pins()
    if pins is not None and agent_id in pins:
        return pins[agent_id]
    profile: WarmProfile | None
    try:
        profile = _PROFILE_READER(agent_id)
    except Exception as exc:  # never break a send
        _announce_once(f"reader:{type(exc).__name__}", f"profile reader failed ({exc!r}); sends proceed unwarmed")
        profile = None
    if profile is not None and not (profile.shared_text or profile.pending_reason):
        profile = None
    if pins is not None:
        pins[agent_id] = profile
    return profile


def current_agent_id() -> str | None:
    try:
        from matrx_connect import get_app_context

        ctx = get_app_context()
    except Exception:
        return None
    return (getattr(ctx, "agent_id", None) or None) if ctx is not None else None


def _ctx_value(name: str) -> str | None:
    try:
        from matrx_connect import get_app_context

        ctx = get_app_context()
    except Exception:
        return None
    value = getattr(ctx, name, None) if ctx is not None else None
    return str(value) if value else None


# ── layout (called by the Anthropic translator) ────────────────────────────────────────────


def _tool_name(decl: Any) -> str | None:
    return decl.get("name") if isinstance(decl, dict) else None


def authored_tool_run(tools: list[dict[str, Any]], authored_wire_names: set[str]) -> int:
    """How many leading tool declarations are the agent's own: the run of authored names at the head
    of the array (the ledger puts them first, ``declaration_ledger.order_key``). Stops at the first
    platform-added tool — before the tiers it stopped at the first dynamic one, so a surface tool that
    sorted early cut the run to a few tools and the mark cached almost nothing."""
    run = 0
    for decl in tools:
        if _tool_name(decl) not in authored_wire_names:
            break
        run += 1
    return run


def _count_marks(request: dict[str, Any], messages: list[dict[str, Any]]) -> int:
    def marked(blocks: Any) -> int:
        return sum(1 for b in blocks or [] if isinstance(b, dict) and "cache_control" in b)

    system = request.get("system") if isinstance(request.get("system"), list) else []
    total = marked(system) + marked(request.get("tools"))
    for m in messages:
        content = m.get("content")
        if isinstance(content, list):
            total += marked(content)
    return total


def apply_warm_layout(
    request: dict[str, Any],
    messages: list[dict[str, Any]],
    *,
    agent_id: str,
    profile: WarmProfile,
    system_text: str,
    authored_run: int,
) -> WarmLayout:
    """Lay out ``request['system']`` / ``request['tools']`` for an enrolled agent (in place).

    Called after the platform's own marks (system, template, rolling) are placed and BEFORE
    the request's params are resolved; ``finish_warm_layout`` computes the replayable prefix.
    """
    model = str(request.get("model") or "")
    shared = profile.shared_text
    layout = WarmLayout(
        agent_id=agent_id,
        model=model,
        applied=False,
        shared_chars=len(shared),
        prompt_chars=profile.prompt_chars or len(shared),
    )
    if profile.pending_reason:
        layout.miss_reason = profile.pending_reason
        return layout
    if not system_text or shared not in system_text:
        return layout

    rest = system_text.replace(shared, "", 1).strip()
    block_a = {"type": "text", "text": shared, "cache_control": cache_control(long=True)}
    blocks: list[dict[str, Any]] = [block_a]
    if rest:
        blocks.append({"type": "text", "text": rest, "cache_control": cache_control(long=True)})
    request["system"] = blocks

    tools = request.get("tools")
    if isinstance(tools, list) and tools and 0 < authored_run < len(tools):
        out = list(tools)
        out[authored_run - 1] = {**out[authored_run - 1], "cache_control": cache_control(long=True)}
        request["tools"] = out

    # Every 1h mark must precede every 5m mark: tools and system come first on the wire, so
    # the only 5m mark is the rolling one in messages. Ceiling: drop B's mark, then the tool mark.
    while _count_marks(request, messages) > MAX_ANTHROPIC_CACHE_MARKS:
        if len(request["system"]) > 1 and "cache_control" in request["system"][1]:
            request["system"][1] = {k: v for k, v in request["system"][1].items() if k != "cache_control"}
            layout.marks_dropped.append("system_rest")
            continue
        raw_tools = request.get("tools")
        tool_list: list[Any] = raw_tools if isinstance(raw_tools, list) else []
        marked = [i for i, t in enumerate(tool_list) if isinstance(t, dict) and "cache_control" in t]
        if marked:
            i = marked[0]
            tool_list[i] = {k: v for k, v in tool_list[i].items() if k != "cache_control"}
            layout.marks_dropped.append("authored_tools")
            continue
        break  # the translator's own ceiling handles anything left (message marks)
    layout.applied = True
    return layout


def replayable_prefix(request: dict[str, Any]) -> dict[str, Any]:
    """The part of a laid-out request every conversation of this variant shares."""
    prefix: dict[str, Any] = {"model": request.get("model")}
    if request.get("tools"):
        prefix["tools"] = request["tools"]
    system = request.get("system")
    prefix["system"] = [system[0]] if isinstance(system, list) and system else []
    if "thinking" in request:
        prefix["thinking"] = request["thinking"]
    output_config = request.get("output_config")
    if isinstance(output_config, dict) and "effort" in output_config:
        prefix["output_config"] = {"effort": output_config["effort"]}
    return prefix


def prefix_text_of(prefix: dict[str, Any]) -> str:
    """Byte-stable serialization (insertion order kept, never sorted)."""
    return json.dumps(prefix, ensure_ascii=False, separators=(",", ":"), default=str)


def variant_key_of(prefix_text: str) -> str:
    return hashlib.sha256(prefix_text.encode("utf-8")).hexdigest()


def finish_warm_layout(layout: WarmLayout, request: dict[str, Any]) -> WarmLayout:
    """After params are resolved: compute the replayable prefix and park the layout for the send."""
    if layout.applied:
        layout.prefix_text = prefix_text_of(replayable_prefix(request))
        layout.variant_key = variant_key_of(layout.prefix_text)
    _LAYOUT.set(layout)
    return layout


def take_layout() -> WarmLayout | None:
    """The layout of the request this context just built (cleared on read)."""
    layout = _LAYOUT.get()
    _LAYOUT.set(None)
    return layout


# ── observation (called by the Anthropic send path) ───────────────────────────────────────


def usage_numbers(raw: Any) -> dict[str, int]:
    raw = raw if isinstance(raw, dict) else {}
    creation = raw.get("cache_creation") if isinstance(raw.get("cache_creation"), dict) else {}
    write_total = int(raw.get("cache_creation_input_tokens") or 0)
    w5 = int(creation.get("ephemeral_5m_input_tokens") or 0)
    w1 = int(creation.get("ephemeral_1h_input_tokens") or 0)
    if write_total and not (w5 or w1):
        w5 = write_total  # no split reported: the API's default tier
    return {
        "input_tokens": int(raw.get("input_tokens") or 0),
        "output_tokens": int(raw.get("output_tokens") or 0),
        "cache_read_tokens": int(raw.get("cache_read_input_tokens") or 0),
        "cache_write_5m_tokens": w5,
        "cache_write_1h_tokens": w1,
    }


def _raw_usage(usage: Any) -> dict[str, Any]:
    raw = getattr(usage, "raw_usage", None)
    if isinstance(raw, dict):
        return raw
    if hasattr(usage, "model_dump"):
        try:
            return usage.model_dump()
        except Exception:
            return {}
    return usage if isinstance(usage, dict) else {}


def observe(layout: WarmLayout | None, *, kind: str, usage: Any = None, error: str | None = None) -> None:
    """Hand one send's facts to the host observer. Never raises."""
    if layout is None or _OBSERVER is None:
        return
    try:
        numbers = usage_numbers(_raw_usage(usage))
        observation = WarmObservation(
            kind=kind,
            agent_id=layout.agent_id,
            model=layout.model,
            variant_key=layout.variant_key,
            prefix_text=layout.prefix_text,
            applied=layout.applied,
            shared_chars=layout.shared_chars,
            prompt_chars=layout.prompt_chars,
            conversation_id=_ctx_value("conversation_id"),
            organization_id=_ctx_value("organization_id"),
            error=error,
            miss_reason=layout.miss_reason,
            **numbers,
        )
        _OBSERVER(observation)
    except Exception as exc:
        _announce_once(f"observer:{type(exc).__name__}", f"observer failed ({exc!r}); sends are unaffected")


# ── keep-alive ────────────────────────────────────────────────────────────────────────────


def keepalive_payload(prefix_text: str) -> dict[str, Any]:
    """The prefix replayed as a ``max_tokens: 0`` request (rejected shapes removed)."""
    prefix = json.loads(prefix_text)
    payload: dict[str, Any] = dict(prefix)
    thinking = payload.get("thinking")
    if isinstance(thinking, dict) and thinking.get("type") == "enabled":
        payload.pop("thinking")  # max_tokens 0 refuses a thinking budget
    payload["messages"] = [{"role": "user", "content": KEEPALIVE_TEXT}]
    payload["max_tokens"] = 0
    return payload


_KEEPALIVE_CHAT: Any = None


async def send_keepalive(prefix_text: str) -> dict[str, int]:
    """Replay one prefix with ``max_tokens: 0``; returns the cache usage numbers."""
    from matrx_ai.providers.anthropic.anthropic_api import AnthropicChat
    from matrx_ai.providers.guardrail_gate import admit_call_spend_cap

    # THE PER-CALL SPEND CAP: this send goes straight to the vendor SDK, beside the unified
    # client's seam, so it asks the cap itself (config-less: refused under any open cap).
    admit_call_spend_cap(None, None)

    from matrx_ai.providers.keys import begin_dispatch_key_scope, prepare_provider_clients

    global _KEEPALIVE_CHAT
    if _KEEPALIVE_CHAT is None:
        _KEEPALIVE_CHAT = AnthropicChat()
    # The same preflight every unified dispatch runs (unified_client): keys resolve and the SDK client is built
    # OFF the event loop; touching ``.client`` cold on the loop raises (live 2026-11-15: every keep-alive failed).
    begin_dispatch_key_scope()
    await prepare_provider_clients(_KEEPALIVE_CHAT)
    payload = keepalive_payload(prefix_text)
    response = await _KEEPALIVE_CHAT.client.messages.create(**payload)
    usage: Any = getattr(response, "usage", None)
    raw = usage.model_dump() if usage is not None and hasattr(usage, "model_dump") else {}
    return usage_numbers(raw)


__all__ = [
    "KEEPALIVE_TEXT",
    "KIND_KEEPALIVE",
    "KIND_LIVE",
    "OUTCOME_BREAK",
    "OUTCOME_COLD",
    "OUTCOME_ERROR",
    "OUTCOME_HIT",
    "OUTCOME_LAYOUT_MISS",
    "WarmLayout",
    "WarmObservation",
    "WarmProfile",
    "apply_warm_layout",
    "authored_tool_run",
    "configure_prompt_warm",
    "current_agent_id",
    "finish_warm_layout",
    "keepalive_payload",
    "observe",
    "prefix_text_of",
    "profile_for",
    "replayable_prefix",
    "send_keepalive",
    "shared_text_from_authored",
    "take_layout",
    "usage_numbers",
    "variant_key_of",
]
