"""THE RESIDUAL CHECK — request text no registered block accounts for (report only).

Plan: ``common-docs/systems/agents/agent-harness/projects/prompt-blocks-static-seal/PLAN.md`` §5.4 ("residual check on the final
outbound snapshot") and §9 P1a. Owner rule (``VISION.md``, 2026-11-13): a real request must never
fail, slow meaningfully or change because of this project.

What it does: take the chat body that actually left for the provider (the final outbound snapshot's
parsed body), keep only the text the PLATFORM could have written into — the system text and the
text of person-side turns — and subtract every span the registry recognises:

* tool I/O: the tool array, tool calls and tool results (structural: never read as text);
* history: model turns (assistant / model roles; structural);
* the agent's authored text, the person's text and every message the send boundary rendered: the
  texts of the exact list the translator rendered (``note_wire_source``, recorded by
  ``BaseTranslator.messages_for_wire``) and the wire config's system text and Custom Dictionary;
* registered blocks' recognisable frames: ``platform_parts.without_platform_parts`` (the per-turn
  ``<turn_context>``, date, identity, person context, organization catalog, skills, Kind
  Directives, inherited history, open tasks), then registered WRAPPER frames left empty
  (``without_empty_wrapper_frames``: the ``<system_note>`` around a carried history system message).

A known span is matched with its whitespace free and also without its platform-part frames, because the
always-warm layout re-cuts the Anthropic system channel (trims the cut, moves the date line behind the
authored text). What is left is text that reached the model with no registered block behind it. It is reported as
ONE ``app_log`` WARNING ``unregistered_request_content`` per conversation per seal window (lengths,
a digest, the wire location and a short preview), never a ``system_error`` and never a change.

Where it runs: ONLY in the static seal's worker PROCESS (``final_outbound_snapshot`` /
``seal_worker``), after the segment parse — never on the event loop, never in the server process's
threads, never in the send's path. The server side computes the known texts and the frame patterns
(``platform_patterns``) as plain data; the worker subtracts; the server reports (``report_residual``).
Every failure is caught and said once per process; the send never sees it. Knob: ``agents.prompt_cache.residual_check``.

Known gaps (P1a, until each producer records its span): text the provider client adds after the
translator (the JSON answer contract for a model that cannot enforce a schema, the prefill note),
picklist / reference fences resolved on the wire, and xAI
(proto bodies are not read). Text glued into a rendered message BEFORE the translator counts as that
message's text — this layer sees what was added between the rendered config and the wire.
"""

from __future__ import annotations

import hashlib
import logging
import threading
import time
from collections import OrderedDict
from contextvars import ContextVar
from typing import Any

logger = logging.getLogger(__name__)

FEATURE = "agents.prompt_cache"
#: KNOB MIRROR of platform.feature_knob "agents.prompt_cache" "residual_check".
RESIDUAL_CHECK_MIRROR = True
#: Leftovers shorter than this many non-space characters (separators, joiners) are not reported.
MIN_RESIDUAL_CHARS = 8
_PREVIEW_CHARS = 120
_MAX_CONVERSATIONS = 512
REPORT_KIND = "unregistered_request_content"

#: The rendered source of the send in flight: ``(wire config, rendered message list)``. A reference,
#: never a copy (set on the send path; read only in the worker).
_wire_source_var: ContextVar[tuple[Any, Any] | None] = ContextVar("matrx_ai_residual_wire_source", default=None)

_REPORTED: OrderedDict[str, float] = OrderedDict()
_REPORTED_LOCK = threading.Lock()


def residual_check_enabled() -> bool:
    from matrx_ai.knobs import package_knob

    value = package_knob(FEATURE, "residual_check", RESIDUAL_CHECK_MIRROR)
    return value if isinstance(value, bool) else RESIDUAL_CHECK_MIRROR


def _will_be_checked(provider: str) -> bool:
    """Whether this send's body can reach the residual check: never xAI (proto bodies are not read),
    only inside an agent loop with a conversation (the seal fingerprints nothing else), and only
    while the seal check and this knob are on. Cheapest test first; any doubt is no."""
    if provider == "xai":
        return False
    from matrx_ai.providers import final_outbound_snapshot as fos

    if not fos._in_agent_loop():
        return False
    ctx = fos._app_context()
    if ctx is None or not getattr(ctx, "conversation_id", None):
        return False
    return fos.seal_check_on() and residual_check_enabled()


def note_wire_source(config: Any, messages: Any, *, provider: str = "") -> None:
    """Record the config and the message list a chat translator renders (one ContextVar set) — only
    when the residual check will read it; otherwise clear any earlier source, so no reference to a
    config or its messages outlives a send that is never checked. Never raises."""
    try:
        if _will_be_checked(provider):
            _wire_source_var.set((config, messages))
        elif _wire_source_var.get() is not None:
            _wire_source_var.set(None)
    except Exception:  # noqa: BLE001 — the observer never breaks a send
        try:
            _wire_source_var.set(None)
        except Exception:  # noqa: BLE001
            pass


def take_wire_source() -> tuple[Any, Any] | None:
    """The recorded source of this send, cleared (it belongs to this send only)."""
    source = _wire_source_var.get()
    if source is not None:
        _wire_source_var.set(None)
    return source


def reset_for_tests() -> None:
    with _REPORTED_LOCK:
        _REPORTED.clear()
    _wire_source_var.set(None)


# ---------------------------------------------------------------------------
# Known texts — what the rendered config holds
# ---------------------------------------------------------------------------


def _message_texts(message: Any) -> list[str]:
    content = message.get("content") if isinstance(message, dict) else getattr(message, "content", None)
    if isinstance(content, str):
        return [content]
    out: list[str] = []
    for part in content or []:
        text = part.get("text") if isinstance(part, dict) else getattr(part, "text", None)
        if isinstance(text, str) and text:
            out.append(text)
    return out


def known_texts(source: tuple[Any, Any] | None) -> list[str]:
    """Every text the rendered config holds: system text, Custom Dictionary, each rendered message's
    text parts. Longest first (a long span is removed before a short one inside it)."""
    if source is None:
        return []
    config, messages = source
    texts: list[str] = []
    for attr in ("resolved_system_instruction", "system_instruction"):
        try:
            value = getattr(config, attr, None)
        except Exception:  # noqa: BLE001
            value = None
        if isinstance(value, str) and value:
            texts.append(value)
    try:
        raw = getattr(config, "dictionary", None)
        if raw is not None:
            from matrx_ai.config.dictionary_config import DictionaryConfig

            dictionary = DictionaryConfig.coerce(raw)
            if dictionary is not None and not dictionary.is_empty:
                texts.append(dictionary.render_for_system(supports_tools=getattr(config, "supports_tools", True)))
    except Exception:  # noqa: BLE001
        pass
    for message in list(messages or getattr(config, "messages", None) or []):
        texts.extend(_message_texts(message))
    return sorted({t for t in texts if t and t.strip()}, key=len, reverse=True)


# ---------------------------------------------------------------------------
# Wire texts — the platform-writable text of the body, per wire shape
# ---------------------------------------------------------------------------

_MODEL_ROLES = frozenset({"assistant", "model", "tool", "function"})


def _parts_text(parts: Any, label: str) -> list[tuple[str, str]]:
    if isinstance(parts, str):
        return [(label, parts)]
    out: list[tuple[str, str]] = []
    for index, part in enumerate(parts or []):
        if not isinstance(part, dict):
            continue
        kind = part.get("type")
        if kind is not None and kind not in ("text", "input_text"):
            continue  # tool_use / tool_result / image / document / thinking …: not platform text
        text = part.get("text")
        if isinstance(text, str):
            out.append((f"{label} part {index}", text))
    return out


def wire_texts(shape: str, body: dict[str, Any]) -> list[tuple[str, str]]:
    """``(where, text)`` of every system and person-side text in a chat body (model turns and tool
    I/O are structural, never read)."""
    from matrx_ai.providers import final_outbound_snapshot as fos

    out: list[tuple[str, str]] = []
    if shape == fos.SHAPE_ANTHROPIC:
        # The system channel is ONE text the translator cuts into blocks only to place cache marks
        # (``cache_marks.system_blocks_with_shared_lead``, ``prompt_warm``): read it whole, so a
        # known span is never missed because a cache mark sits inside it.
        system_parts = _parts_text(body.get("system"), "system")
        if len(system_parts) > 1:
            system_parts = [("system", "".join(text for _where, text in system_parts))]
        out.extend(system_parts)
        messages = body.get("messages") or []
    elif shape == fos.SHAPE_RESPONSES:
        if isinstance(body.get("instructions"), str):
            out.append(("system", body["instructions"]))
        messages = body.get("input") or []
        if isinstance(messages, str):
            return [*out, ("message 0", messages)]
    elif shape == fos.SHAPE_CHAT:
        messages = body.get("messages") or []
    elif shape == fos.SHAPE_GOOGLE:
        for key in ("systemInstruction", "system_instruction"):
            system = body.get(key)
            if isinstance(system, dict):
                out.extend(_parts_text(system.get("parts"), "system"))
        for index, content in enumerate(body.get("contents") or []):
            if isinstance(content, dict) and content.get("role") not in _MODEL_ROLES:
                for part_index, part in enumerate(content.get("parts") or []):
                    if isinstance(part, dict) and isinstance(part.get("text"), str):
                        out.append((f"message {index} part {part_index}", part["text"]))
        return out
    else:
        return out
    for index, message in enumerate(messages):
        if not isinstance(message, dict) or message.get("role") in _MODEL_ROLES:
            continue
        if message.get("type") not in (None, "message"):
            continue  # function_call / function_call_output / reasoning items
        out.extend(_parts_text(message.get("content"), f"message {index}"))
    return out


# ---------------------------------------------------------------------------
# The check
# ---------------------------------------------------------------------------


def platform_patterns() -> dict[str, list[tuple[str, Any]]]:
    """The registered frames as plain data, for the static seal's worker process (it compiles them
    itself and never imports the config package): ``frames`` — ``(pattern, flags)`` of every
    platform-part frame (``without_platform_parts``); ``wrappers`` — ``(open, close)`` of every
    wrapper frame (``without_empty_wrapper_frames``)."""
    from matrx_ai.config.platform_parts import _patterns, _wrapper_frames

    return {
        "frames": [(pattern.pattern, int(pattern.flags)) for _part_id, pattern in _patterns()],
        "wrappers": [(open_tag, close_tag) for open_tag, close_tag in _wrapper_frames().values()],
    }


def _strippers(patterns: dict[str, list[tuple[str, Any]]]) -> tuple[Any, Any]:
    """``without_platform_parts`` and ``without_empty_wrapper_frames`` rebuilt from ``platform_patterns()``."""
    import re

    frames = [re.compile(pattern, flags) for pattern, flags in patterns.get("frames") or []]
    wrappers = [
        (open_tag, re.compile(re.escape(open_tag) + r"\s*" + re.escape(close_tag)))
        for open_tag, close_tag in patterns.get("wrappers") or []
    ]

    def without_platform_parts(text: str) -> str:
        for pattern in frames:
            text = pattern.sub("", text)
        return text

    def without_empty_wrapper_frames(text: str) -> str:
        for open_tag, pattern in wrappers:
            if open_tag in text:
                text = pattern.sub("", text)
        return text

    return without_platform_parts, without_empty_wrapper_frames


def _subtract_span(rest: str, span: str) -> str:
    """``rest`` with every copy of ``span`` replaced by a newline. Exact first; failing that, the span
    is matched with its whitespace runs free: a translator may trim or drop the whitespace around a
    piece it cuts (the always-warm layout sends ``[shared.rstrip(), rest.strip()]``), so a known text
    is the same text on the wire without being byte-identical. Only whitespace is tolerated — a
    different word is still a residual."""
    if len(span) <= len(rest) and span in rest:
        return rest.replace(span, "\n")
    tokens = span.split()
    if len(tokens) < 2 or len(span.replace(" ", "")) > len(rest) + len(tokens):
        return rest
    import re

    return re.sub(r"\s*".join(re.escape(t) for t in tokens), "\n", rest)


def residual_of(
    shape: str, body: dict[str, Any], known: list[str], *, patterns: dict[str, list[tuple[str, Any]]] | None = None
) -> list[tuple[str, str]]:
    """``(where, leftover)`` for every wire text with at least ``MIN_RESIDUAL_CHARS`` non-space
    characters no registered span accounts for. ``patterns`` (``platform_patterns()``, handed to the
    seal's worker process) stands in for ``platform_parts``' two strippers, with the same frames."""
    if patterns is None:
        from matrx_ai.config.platform_parts import (
            without_empty_wrapper_frames,
            without_platform_parts,
        )
    else:
        without_platform_parts, without_empty_wrapper_frames = _strippers(patterns)

    left: list[tuple[str, str]] = []
    for where, text in wire_texts(shape, body):
        rest = text
        for span in known:
            rest = _subtract_span(rest, span)
            # The rendered system text leads with platform parts (the date line, skills...) that the
            # always-warm layout moves BEHIND the authored text: the whole span is then not contiguous
            # on the wire. The same span without those frames is (they are subtracted on their own).
            bare = without_platform_parts(span)
            if bare != span and bare.strip():
                rest = _subtract_span(rest, bare)
        rest = without_empty_wrapper_frames(without_platform_parts(rest))
        if sum(1 for ch in rest if not ch.isspace()) >= MIN_RESIDUAL_CHARS:
            left.append((where, rest.strip()))
    return left


def _first_report_in_window(conversation_id: str, now: float, window: float) -> bool:
    with _REPORTED_LOCK:
        at = _REPORTED.get(conversation_id)
        if at is not None and now - at < window:
            return False
        _REPORTED[conversation_id] = now
        _REPORTED.move_to_end(conversation_id)
        while len(_REPORTED) > _MAX_CONVERSATIONS:
            _REPORTED.popitem(last=False)
        return True


def check_residual(
    *,
    shape: str,
    body: dict[str, Any],
    source: tuple[Any, Any] | None,
    conversation_id: str | None,
    request_id: str | None = None,
    provider: str = "",
    model: str = "",
) -> list[tuple[str, str]]:
    """Run the check on one parsed body; report once per conversation per window. Returns the
    residual (empty when every text is accounted for). Pure CPU: call it in a worker thread."""
    if source is None or not conversation_id:
        return []  # nothing recorded what the translator rendered: never guess
    residual = residual_of(shape, body, known_texts(source))
    report_residual(residual, conversation_id=conversation_id, request_id=request_id, provider=provider, model=model)
    return residual


def report_residual(
    residual: list[tuple[str, str]],
    *,
    conversation_id: str | None,
    request_id: str | None = None,
    provider: str = "",
    model: str = "",
) -> None:
    """Report a residual (computed here or by the static seal's worker process) once per
    conversation per seal window. Server side: it holds the per-conversation memory."""
    if not residual or not conversation_id:
        return
    from matrx_ai.providers.final_outbound_snapshot import seal_window_seconds

    if not _first_report_in_window(str(conversation_id), time.time(), seal_window_seconds()):
        return
    joined = "\n".join(text for _, text in residual)
    logger.warning(
        "%s: %s text span(s) reached the model with no registered block behind them "
        "(conversation %s, request %s, provider %s, model %s, where %s, %s chars, sha256 %s, preview %r)",
        REPORT_KIND,
        len(residual),
        conversation_id,
        request_id,
        provider,
        model,
        ", ".join(where for where, _ in residual),
        len(joined),
        hashlib.sha256(joined.encode("utf-8", "replace")).hexdigest()[:16],
        joined[:_PREVIEW_CHARS],
        extra={"kind": REPORT_KIND, "conversation_id": conversation_id, "where": [w for w, _ in residual]},
    )


__all__ = [
    "MIN_RESIDUAL_CHARS",
    "REPORT_KIND",
    "check_residual",
    "known_texts",
    "note_wire_source",
    "platform_patterns",
    "report_residual",
    "reset_for_tests",
    "residual_check_enabled",
    "residual_of",
    "take_wire_source",
    "wire_texts",
]
