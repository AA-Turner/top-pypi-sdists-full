"""Prompt-cache observability guard — the loud, layered defense that makes a
silent caching failure impossible.

Prompt caching is worth 5–10x on input cost across a tool loop. When it
silently stops working (a breakpoint dropped, a provider change, or — the
cardinal sin — the SYSTEM PROMPT mutating between rounds), the only symptom is
a bigger bill weeks later. Nobody watches token-usage dashboards. So this
module turns that silent failure into a screaming one.

Two independent layers, each sufficient alone, each SCREAMING when it fires
(the doctrine in /PRINCIPLES.md and root CLAUDE.md — "extinction is layered,
and loud"):

  Layer 1 — PREFIX STABILITY. The cacheable prefix of a request is
  ``tools + system``. Within one agent/tool loop it MUST be byte-stable across
  rounds. If the SYSTEM PROMPT changes between rounds → RED banner (this
  violates the "never modify the system prompt between rounds" rule AND it
  busts the cache). If only the TOOL SET changes → orange notice (legitimate
  when dynamic tool injection ran, but it still invalidates the provider cache
  for that turn, so it's worth surfacing).

  Layer 1b — THE WHOLE WIRE PREFIX. The literal SDK body, part by part in its
  own key order (tools, system, cache key, structured-output format, history up
  to the last stable item), must repeat byte for byte; whatever moved is NAMED
  (``prompt_cache_prefix_drift``). The stored snapshot cannot show this: jsonb
  re-sorts keys.

  Layer 2 — CACHE EFFECTIVENESS. Ground truth from the provider's own usage
  block. On any call after the first in a loop, when the prefix was stable and
  the prompt was large enough to cache, ``cache_read`` MUST be > 0. Zero cache
  read on a stable, large prefix → RED banner: caching is broken.

The stability layer is provider-agnostic. The effectiveness alarm is narrower:
it only covers providers whose cache contract makes a hit mandatory for the
request shape. Google implicit caching is opportunistic (and its minimum input
varies by model), so a zero Google cache read is telemetry, not an ERROR.
OpenAI's automatic cache is routed, not promised: a zero read in a loop whose
wire prefix Layer 1b proved byte-stable is a yellow routing-miss line, every
time (a direct replay missed 4 of 18 call-2s) until one provider + model
reaches OPENAI_STABLE_MISS_STREAK_TO_FILE in a row with no hit, which is filed;
one with no wire proof is filed, and a moved prefix files as prompt_cache_prefix_drift.

``PROMPT_CACHING_ENABLED`` also lives here — it is the SINGLE flag that both
(a) makes the Anthropic translator emit ``cache_control`` breakpoints and
(b) makes Layer 2 expect Anthropic cache reads. They can never drift.
"""

from __future__ import annotations

import asyncio
import hashlib
import inspect
import json
import re
import threading
import time
from collections import OrderedDict
from dataclasses import dataclass
from typing import Any

from matrx_utils import detached_task, vcprint

# ─────────────────────────────────────────────────────────────────────────────
# Config — CAPS constants (a code push to change; NEVER a silent env default).
# ─────────────────────────────────────────────────────────────────────────────

# The single switch for Anthropic prompt caching. When True the Anthropic
# translator emits cache_control breakpoints AND this guard expects Anthropic
# cache reads. Flip both off together by flipping this one flag.
PROMPT_CACHING_ENABLED = True

# Master switch for the guard itself. Leave on — a broken cache is expensive
# and invisible without it.
CACHE_GUARD_ENABLED = True

# Providers where a stable, large prefix MUST yield cache reads after the first
# call in a loop. Anthropic only when we're actually sending breakpoints.
_AUTO_CACHE_PROVIDERS = {"openai"}

# OpenAI Responses rejects prompt_cache_key values longer than 64 characters.
# Keep the human-recognizable namespace while leaving the remaining bytes to a
# collision-resistant digest.  This is a wire-contract limit, not a tuning
# knob.
OPENAI_PROMPT_CACHE_KEY_MAX_CHARS = 64
_PROMPT_CACHE_KEY_PREFIX = "matrx_"
_PROMPT_CACHE_KEY_DIGEST_CHARS = (
    OPENAI_PROMPT_CACHE_KEY_MAX_CHARS - len(_PROMPT_CACHE_KEY_PREFIX)
)


def _expected_cache_providers() -> set[str]:
    providers = set(_AUTO_CACHE_PROVIDERS)
    if PROMPT_CACHING_ENABLED:
        providers.add("anthropic")
    return providers


# Default floor for providers/models without a stricter documented minimum.
CACHE_MIN_CACHEABLE_INPUT_TOKENS = 1024

# Anthropic silently declines cache writes below the model-specific floor.
# Keep these checks broad enough to match dated provider model names.
_ANTHROPIC_CACHE_MINIMUMS: tuple[tuple[tuple[str, ...], int], ...] = (
    (("haiku-4-5", "haiku-4.5"), 4096),
    (("haiku-3-5", "haiku-3.5"), 2048),
    (("opus-4-7", "opus-4.7"), 2048),
    (("opus-4-6", "opus-4.6", "opus-4-5", "opus-4.5"), 4096),
    (("opus-5", "fable-5", "mythos-5"), 512),
)


def cacheable_input_threshold(provider: str, model: str) -> int:
    """Return the provider/model minimum at which a cache hit is mandatory."""
    normalized = model.lower().replace("_", "-")
    if provider == "anthropic":
        for aliases, threshold in _ANTHROPIC_CACHE_MINIMUMS:
            if any(alias in normalized for alias in aliases):
                return threshold
    return CACHE_MIN_CACHEABLE_INPUT_TOKENS

# If the gap since the previous call in a loop exceeds the provider cache TTL,
# a zero cache read is legitimate expiry, not a bug — don't scream. Anthropic's
# default ephemeral TTL is 5 minutes; OpenAI/Google are longer, so this bound
# is conservative (fewer false alarms).
CACHE_TTL_GRACE_SECONDS = 300

# LRU cap on tracked loops — prevents unbounded memory on a long-lived process.
_MAX_TRACKED_LOOPS = 512

#: KNOB MIRROR ai.prompt_cache.stable_miss_streak_to_file (the starting value; the row is what an admin changes,
#: read live through matrx_ai.knobs). Consecutive zero reads on a proven byte-stable wire prefix,
#: across every loop of one provider + model in this process, with no cache hit between them, before one is
#: filed. Why 12: a direct replay missed 4 of 18 call-2s (up to 3 of 6 in one batch, 2026-11-15); even at a 50%
#: miss rate a chance run of 12 is about one in 8,000 eligible calls, while a cache that never hits files in 12.
OPENAI_STABLE_MISS_STREAK_TO_FILE = 12
PROMPT_CACHE_KNOB_FEATURE = "ai.prompt_cache"
STABLE_MISS_STREAK_KNOB_KEY = "stable_miss_streak_to_file"


def stable_miss_streak_to_file() -> int:
    """KNOB ai.prompt_cache.stable_miss_streak_to_file — stable-wire misses in a row before one is filed."""
    from matrx_ai.knobs import package_knob_number

    return int(package_knob_number(
        PROMPT_CACHE_KNOB_FEATURE, STABLE_MISS_STREAK_KNOB_KEY, OPENAI_STABLE_MISS_STREAK_TO_FILE, low=2, high=1000
    ))
_STABLE_MISS_STREAKS: dict[tuple[str, str], int] = {}
_STREAK_LOCK = threading.Lock()


def reset_stable_miss_streaks() -> None:
    """Forget every provider/model routing-miss streak (tests; a host that rotates its key)."""
    with _STREAK_LOCK:
        _STABLE_MISS_STREAKS.clear()


def _bump_stable_miss_streak(provider: str, model: str) -> int:
    with _STREAK_LOCK:
        streak = _STABLE_MISS_STREAKS.get((provider, model), 0) + 1
        _STABLE_MISS_STREAKS[(provider, model)] = streak
        return streak


def _clear_stable_miss_streak(provider: str, model: str) -> None:
    with _STREAK_LOCK:
        _STABLE_MISS_STREAKS.pop((provider, model), None)


# ─────────────────────────────────────────────────────────────────────────────
# Layer 1b — THE WHOLE WIRE PREFIX (PB-03 copy O, 2026-11-08)
# ─────────────────────────────────────────────────────────────────────────────
#
# Layer 1 compares the config's system text and tool NAMES, so a byte wobble
# anywhere else in the prefix (a clock inside a context block, a tool schema
# re-serialized with its keys in another order, a changing prompt_cache_key, a
# reordered or re-rendered history item) was invisible, and the stored snapshot
# cannot show it either (jsonb re-sorts keys). This layer fingerprints the
# literal wire body the SDK received, in ITS key order, part by part: each tool,
# the system/instructions, the cache key, the structured-output format, and each
# history item. Round N+1 must repeat round N's parts byte for byte up to the
# last stable item (everything before the item that ended round N, which may be
# a trailing host turn that moves after the cache line). Rolling Anthropic
# ``cache_control`` marks are not content and are ignored. Only digests and
# sizes are kept, never prompt text.

#: Wire keys whose value heads the prefix (compared whole, by key). ``tool_choice``, Anthropic
#: ``thinking`` and Chat Completions ``response_format`` change what the provider caches too.
_WIRE_HEAD_KEYS: tuple[str, ...] = (
    "instructions", "system", "system_instruction", "prompt_cache_key",
    "tool_choice", "thinking", "response_format",
    # The model owns the cache, and a Responses call's reasoning / include / store settings shape what is
    # sent and kept: a change in any of them is not a "stable" prefix (R2 review 2026-11-15).
    "model", "reasoning", "include", "store",
)
#: Wire keys holding the conversation history, in prefix order.
_WIRE_HISTORY_KEYS: tuple[str, ...] = ("input", "messages", "contents")


@dataclass(frozen=True)
class WirePrefix:
    """Digests of one request's wire prefix: ``heads`` (label -> digest), ``tools``
    ((name, exact digest, key-order-blind digest)), ``items`` ((label, digest, bytes)).

    ``stable_sha`` is one streaming digest over every item but the last (what the next round
    must repeat) and ``tools_sha`` one digest of the whole tools block: the next round proves
    its old items and tools unchanged against them and digests only what is new."""

    heads: tuple[tuple[str, str], ...]
    tools: tuple[tuple[str, str, str], ...]
    items: tuple[tuple[str, str, int], ...]
    stable_sha: str = ""
    tools_sha: str = ""
    #: The system head's digest with every declared seal-break span removed (``platform_parts.
    #: without_declared_seal_breaks``): equal across two rounds whose system differs only inside them.
    system_outside_breaks: str = ""

    def sha(self, upto_items: int | None = None) -> str:
        items = self.items if upto_items is None else self.items[:upto_items]
        raw = repr((self.heads, [t[1] for t in self.tools], [i[1] for i in items]))
        return hashlib.sha256(raw.encode()).hexdigest()[:16]


def _without_cache_marks(value: Any) -> Any:
    if isinstance(value, dict):
        return {k: _without_cache_marks(v) for k, v in value.items() if k != "cache_control"}
    if isinstance(value, list | tuple):
        return [_without_cache_marks(v) for v in value]
    return value


def _wire_bytes(value: Any, *, sort_keys: bool = False) -> bytes:
    import json

    return json.dumps(
        _without_cache_marks(value), sort_keys=sort_keys, ensure_ascii=False, separators=(",", ":"), default=str
    ).encode("utf-8", "replace")


#: An Anthropic mark as serialized: a flat object under an unescaped key (inside a JSON string the
#: quotes would be escaped, so this can only match a real key).
_CACHE_MARK = re.compile(r',"cache_control":\{[^{}]*\}|"cache_control":\{[^{}]*\},?')


class _NotPlainJson(TypeError):
    pass


def _fast_bytes(value: Any, *, sort_keys: bool = False) -> bytes:
    """``_wire_bytes`` for plain JSON (C encoder, no Python walk); marks dropped from the text.

    Raises ``_NotPlainJson`` for a value json cannot encode natively (an SDK object), so the
    caller falls back to ``wire_json`` + ``_wire_bytes``."""
    import json

    try:
        text = json.dumps(value, sort_keys=sort_keys, ensure_ascii=False, separators=(",", ":"))
    except (TypeError, ValueError) as exc:
        raise _NotPlainJson(str(exc)) from exc
    if '"cache_control":' in text:
        text = _CACHE_MARK.sub("", text)
        if '"cache_control":' in text:  # a nested mark shape: take the exact walk
            return _wire_bytes(value, sort_keys=sort_keys)
    return text.encode("utf-8", "replace")


def _short_digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()[:16]


def _item_label(index: int, item: Any) -> str:
    kind = None
    if isinstance(item, dict):
        kind = item.get("role") or item.get("type")
    return f"[{index}] ({kind})" if kind else f"[{index}]"


def wire_prefix(payload: Any, prev: WirePrefix | None = None) -> WirePrefix | None:
    """Fingerprint the wire body's prefix; None when the payload has no readable shape.

    With ``prev`` (the previous round of the same loop) the old items are proven unchanged by
    one streaming digest and keep their previous digests; only new items, and every item when
    the proof fails, are digested one by one. The result is the same either way."""
    if isinstance(payload, dict):
        try:
            return _wire_prefix_of(payload, prev, _fast_bytes)
        except _NotPlainJson:
            pass
    from matrx_ai.providers.snapshot import wire_json

    return _wire_prefix_of(wire_json(payload), prev, _wire_bytes)


def _wire_prefix_of(body: Any, prev: WirePrefix | None, to_bytes: Any) -> WirePrefix | None:
    if not isinstance(body, dict):
        return None
    raw_config = body.get("config")
    if raw_config is not None and not isinstance(raw_config, dict):
        # Google's ``config`` is an SDK object holding the system text and the tools. Read
        # through the fast path it was skipped: a round whose history was plain JSON saw no
        # system and no tools, and the next round (an SDK Part in the history sends it down
        # ``wire_json``) read "system added" on every Gemini child (PB-02, PB-06 2026-11-09).
        if to_bytes is _fast_bytes:
            raise _NotPlainJson(f"config is {type(raw_config).__name__}")
        vcprint(
            f"[cache_guard] wire config of type {type(raw_config).__name__} is unreadable; "
            "its system text and tools are not compared",
            color="red",
        )
        _capture_unreadable_config(type(raw_config).__name__)
    config = raw_config if isinstance(raw_config, dict) else {}
    heads: list[tuple[str, str]] = []
    system_outside_breaks = ""
    for key in _WIRE_HEAD_KEYS:
        for source in (body, config):
            if source.get(key) not in (None, "", []):
                label = "system" if key in ("instructions", "system", "system_instruction") else key
                heads.append((label, _short_digest(to_bytes(source[key]))))
                if label == "system":
                    system_outside_breaks = _short_digest(to_bytes(_without_declared_breaks(source[key])))
    text = body.get("text")
    if isinstance(text, dict) and text.get("format") is not None:
        heads.append(("text.format", _short_digest(to_bytes(text["format"]))))

    raw_tools = body.get("tools") if isinstance(body.get("tools"), list) else config.get("tools")
    raw_tools = raw_tools if isinstance(raw_tools, list) else []
    tools_sha = hashlib.sha256(to_bytes(raw_tools)).hexdigest()[:16] if raw_tools else ""
    tools: list[tuple[str, str, str]] | tuple[tuple[str, str, str], ...]
    if prev is not None and prev.tools_sha and prev.tools_sha == tools_sha:
        tools = prev.tools
    else:
        tools = []
        for decl in raw_tools:
            identity = _declaration_identity(decl) if isinstance(decl, dict) else None
            name = identity[0] if identity else "<tool>"
            tools.append((name, _short_digest(to_bytes(decl)), _short_digest(to_bytes(decl, sort_keys=True))))

    history: list[Any] = []
    history_key = ""
    for key in _WIRE_HISTORY_KEYS:
        if isinstance(body.get(key), list):
            history, history_key = body[key], key
            break
    count = len(history)
    # Items the previous round's stable digest covers (all but the item that ended it).
    known = max(len(prev.items) - 1, 0) if prev is not None and prev.stable_sha else 0
    known = known if known <= count else 0
    rolling = hashlib.sha256()
    proof = ""
    stable_sha = ""
    old_raw: list[bytes] = []
    items: list[tuple[str, str, int]] = []
    for index, item in enumerate(history):
        raw = to_bytes(item)
        rolling.update(len(raw).to_bytes(8, "big"))
        rolling.update(raw)
        label = f"{history_key}{_item_label(index, item)}"
        if index < known:
            old_raw.append(raw)
            items.append((label, "", len(raw)))
            if index == known - 1:
                proof = rolling.copy().hexdigest()[:16]
        else:
            items.append((label, _short_digest(raw), len(raw)))
        if index == count - 2:
            stable_sha = rolling.copy().hexdigest()[:16]
    if known:
        if prev is not None and proof == prev.stable_sha:
            for index in range(known):
                items[index] = (items[index][0], prev.items[index][1], items[index][2])
        else:
            for index, raw in enumerate(old_raw):
                items[index] = (items[index][0], _short_digest(raw), items[index][2])
    if count == 1:
        stable_sha = hashlib.sha256().hexdigest()[:16]
    return WirePrefix(
        heads=tuple(heads),
        tools=tuple(tools),
        items=tuple(items),
        stable_sha=stable_sha,
        tools_sha=tools_sha,
        system_outside_breaks=system_outside_breaks,
    )


def _without_declared_breaks(value: Any) -> Any:
    """``value`` (a wire system head: text, or blocks of text) with every declared seal-break span removed."""
    from matrx_ai.config.platform_parts import without_declared_seal_breaks

    if isinstance(value, str):
        return without_declared_seal_breaks(value)
    if isinstance(value, list):
        return [_without_declared_breaks(v) for v in value]
    if isinstance(value, dict):
        return {k: _without_declared_breaks(v) for k, v in value.items()}
    return value


@dataclass(frozen=True)
class TrimDeclaration:
    """What the send boundary DECLARED it rewrote this round: call ids whose tool RESULT was
    rewritten, call ids whose tool-call ARGUMENTS were rewritten, and rewrites recorded only as
    counts (make-it-fit passes), which can never be placed on the wire."""

    results: frozenset[str] = frozenset()
    calls: frozenset[str] = frozenset()
    unkeyed: int = 0
    #: assistant messages whose earlier thinking was dropped: ``(message_text_fingerprint, n)``,
    #: the n-th assistant message with that text (None: an older record that named no n).
    messages: frozenset[tuple[str, int | None]] = frozenset()
    #: thinking / reasoning blocks the make-it-fit passes dropped (a Responses wire loses whole
    #: reasoning items, which shifts every later item: a declared break, ``compare_wire_prefix``).
    thinking_dropped: int = 0
    #: earlier message texts the last-resort fit replaced with ``STUB_TEXT``: no id names them, so
    #: each is placed by the stub's own words in an item that changed (``place_trim_on_wire``).
    text_stubs: int = 0
    #: wire head labels (``_WIRE_HEAD_KEYS``) a ONE-CALL setting changed on purpose this round — the
    #: empty-reply retry sends reasoning off once (``SendPrep.one_call_settings``).
    heads: frozenset[str] = frozenset()

    def __bool__(self) -> bool:
        return bool(
            self.results or self.calls or self.unkeyed or self.messages or self.thinking_dropped or self.text_stubs
            or self.heads
        )


def declared_history_rewrites(prep: Any) -> TrimDeclaration:
    """The send boundary's declaration for this round (``SendPrep``): the cache-gated trim's
    ``rewritten_blocks`` and every make-it-fit pass's ``rewritten_blocks`` (by call id /
    tool_use_id), plus what a pass could not name (``unplaced_blocks``). Never raises."""
    results: set[str] = set()
    calls: set[str] = set()
    messages: set[tuple[str, int | None]] = set()
    unkeyed = 0
    thinking_dropped = 0
    text_stubs = 0
    heads: set[str] = set()

    def _read(blocks: Any) -> int:
        nonlocal text_stubs
        missing = 0
        for block in blocks or ():
            if not isinstance(block, dict):
                missing += 1
                continue
            if block.get("block") in ("text_stub", "text_cut"):
                text_stubs += 1
                continue
            if block.get("message"):
                n = block.get("occurrence")
                messages.add((str(block["message"]), int(n) if isinstance(n, int) else None))
                continue
            ids = {str(block[k]) for k in ("call_id", "tool_use_id") if block.get(k)}
            if not ids:
                missing += 1
            elif block.get("block") == "tool_call":
                calls.update(ids)
            else:
                results.update(ids)
        return missing

    try:
        one_call = getattr(prep, "one_call_settings", None)
        if isinstance(one_call, dict) and _REASONING_SETTINGS & set(one_call):
            heads.add("thinking")
        unkeyed += _read(getattr(getattr(prep, "trim_report", None), "rewritten_blocks", None))
        fit = getattr(prep, "fit", None)
        for applied in (fit or {}).get("passes", ()) if isinstance(fit, dict) else ():
            if not isinstance(applied, dict):
                continue
            thinking_dropped += int(applied.get("thinking_blocks_dropped") or 0)
            if "rewritten_blocks" in applied:  # a pass that names its blocks
                unkeyed += _read(applied["rewritten_blocks"]) + int(applied.get("unplaced_blocks") or 0)
            else:  # an older record: counts only, never placeable
                for key in ("blocks_rewritten", "stubbed_blocks", "thinking_blocks_dropped"):
                    unkeyed += int(applied.get(key) or 0)
    except Exception:  # noqa: BLE001 — a malformed report declares only what was read
        pass
    return TrimDeclaration(
        results=frozenset(results),
        calls=frozenset(calls),
        unkeyed=unkeyed,
        messages=frozenset(messages),
        thinking_dropped=thinking_dropped,
        text_stubs=text_stubs,
        heads=frozenset(heads),
    )


#: One-call settings that move the wire's ``thinking`` head.
_REASONING_SETTINGS = frozenset({"reasoning_effort", "thinking_budget", "thinking_level"})


_TEXT_TYPES = frozenset({"text", "output_text", "input_text"})
_THINKING_TYPES = frozenset({"thinking", "redacted_thinking", "reasoning"})


def message_text_fingerprint(texts: list[str]) -> str:
    """A position-free name for a message: the digest of its text parts, in order."""
    return hashlib.sha256("\x1f".join(texts).encode("utf-8", "replace")).hexdigest()[:16]


def _wire_texts(item: Any) -> list[str] | None:
    """The text parts of an assistant wire item (thinking excluded), or None for any other item."""
    if not isinstance(item, dict) or item.get("role") not in ("assistant", "model"):
        return None
    content = item.get("content", item.get("parts"))
    if isinstance(content, str):
        return [content]
    texts: list[str] = []
    for part in content if isinstance(content, list) else ():
        if not isinstance(part, dict) or part.get("type") in _THINKING_TYPES or part.get("thought"):
            continue
        if part.get("type") in _TEXT_TYPES or ("type" not in part and isinstance(part.get("text"), str)):
            texts.append(str(part.get("text") or ""))
    return texts


_RESULT_TYPES = frozenset({"tool_result", "function_call_output"})
_CALL_TYPES = frozenset({"tool_use", "function_call"})


def _ids_in(value: Any, results: set[str], calls: set[str]) -> None:
    """Collect the call ids of every tool result and tool call inside one wire item, across the
    Anthropic, Responses, Chat Completions and Gemini shapes."""
    if isinstance(value, list):
        for v in value:
            _ids_in(v, results, calls)
        return
    if not isinstance(value, dict):
        return
    kind = value.get("type")
    if kind in _RESULT_TYPES:
        for key in ("tool_use_id", "call_id"):
            if value.get(key):
                results.add(str(value[key]))
    elif kind in _CALL_TYPES:
        for key in ("id", "call_id"):
            if value.get(key):
                calls.add(str(value[key]))
    # Chat Completions writes ``role: tool`` / ``tool_call_id`` / ``tool_calls``; the xAI proto wire (read
    # through ``wire_json``) writes ``ROLE_TOOL`` / ``toolCallId`` / ``toolCalls``. Unread, every declared
    # large-output trim on grok was filed as drift (C116: conversation 6c62a26b, 2026-11-10 00:14Z).
    tool_result_id = value.get("tool_call_id") or value.get("toolCallId")
    if value.get("role") in ("tool", "ROLE_TOOL") and tool_result_id:
        results.add(str(tool_result_id))
    tool_calls = value.get("tool_calls")
    if not isinstance(tool_calls, list):
        tool_calls = value.get("toolCalls")
    if isinstance(tool_calls, list):
        for call in tool_calls:
            if isinstance(call, dict) and call.get("id"):
                calls.add(str(call["id"]))
    for key, target in (
        ("function_response", results), ("functionResponse", results),
        ("function_call", calls), ("functionCall", calls),
    ):
        inner = value.get(key)
        if isinstance(inner, dict) and inner.get("id"):
            target.add(str(inner["id"]))
    for v in value.values():
        if isinstance(v, dict | list):
            _ids_in(v, results, calls)


def _trim_marked_idless_parts(item: Any) -> tuple[int, int]:
    """How many id-less Gemini ``functionResponse`` / ``functionCall`` parts in one wire item carry
    a trim marker: (results, calls). Gemini's wire names no call id on either, so a declared trim
    there is placed by the words the trim itself wrote."""
    if not isinstance(item, dict) or not isinstance(item.get("parts"), list):
        return 0, 0
    from matrx_ai.config.context_trim import TRIMMED_ARGUMENT_MARKER
    from matrx_ai.config.input_fit import STUB_TOOL_INPUT, STUB_TOOL_RESULT

    # ``context_trim._DEFAULT_SUBSTITUTE`` opens with the first; ``_already_trimmed`` reads the same words.
    result_marks = ("[tool result cleared]", STUB_TOOL_RESULT)
    call_marks = (TRIMMED_ARGUMENT_MARKER, STUB_TOOL_INPUT, "[tool arguments cleared]")
    results = calls = 0
    for part in item["parts"]:
        if not isinstance(part, dict):
            continue
        for key, marks in (("functionResponse", result_marks), ("function_response", result_marks),
                           ("functionCall", call_marks), ("function_call", call_marks)):
            inner = part.get(key)
            if not isinstance(inner, dict) or inner.get("id"):
                continue
            text = json.dumps(inner, default=str, ensure_ascii=False)
            if any(m in text for m in marks):
                if marks is result_marks:
                    results += 1
                else:
                    calls += 1
    return results, calls


def changed_item_positions(prev: WirePrefix, new: WirePrefix) -> frozenset[int]:
    """Positions of the items both rounds carry whose digest differs."""
    return frozenset(
        i for i, (a, b) in enumerate(zip(prev.items, new.items, strict=False)) if a[1] and b[1] and a[1] != b[1]
    )


def place_trim_on_wire(
    payload: Any, trim: TrimDeclaration, *, changed_at: frozenset[int] | None = None
) -> tuple[frozenset[int], int]:
    """Wire item positions holding a block the trim declared, and how many declared rewrites
    could not be placed (no call id, or an id no wire item carries).

    Placed by call id, not by ``message_position``: canonical messages and wire items differ per
    provider (a Responses assistant turn is several items; a system message leaves the list).
    Gemini's wire carries no call id, so a declared rewrite no id placed is matched to an id-less
    function part carrying the trim's own marker — only in an item that changed (``changed_at``,
    when given), and never more items than were declared."""
    body = payload if isinstance(payload, dict) else None
    if body is None or any(
        isinstance(body.get(key), list) and any(not isinstance(item, dict) for item in body[key])
        for key in _WIRE_HISTORY_KEYS
    ):
        # An SDK object, or a dict whose history holds SDK messages (the xAI translator's proto
        # messages): read it the way the snapshot and ``wire_prefix`` read it, or no id is found
        # and every declared trim on that wire is filed as drift (C116, grok conversation 6c62a26b).
        from matrx_ai.providers.snapshot import wire_json

        body = wire_json(payload)
    history: list[Any] = []
    if isinstance(body, dict):
        for key in _WIRE_HISTORY_KEYS:
            if isinstance(body.get(key), list):
                history = body[key]
                break
    positions: set[int] = set()
    found_results: set[str] = set()
    found_calls: set[str] = set()
    # A dropped-thinking message is matched to exactly ONE wire item: the n-th assistant item with
    # its text. An older record with no n is placed only when exactly one item has that text.
    # Never more items than were declared (probe P3: a second "Let me check." that gained a
    # tool_use is filed, not whitelisted by the first one's text).
    by_text: dict[str, list[int]] = {}
    if trim.messages:
        for index, item in enumerate(history):
            texts = _wire_texts(item)
            if texts is not None:
                by_text.setdefault(message_text_fingerprint(texts), []).append(index)
    unplaced_messages = 0
    for fingerprint, n in trim.messages:
        holders = by_text.get(fingerprint, [])
        if n is None:
            at = holders[0] if len(holders) == 1 else None
        else:
            at = holders[n] if n < len(holders) else None
        if at is None:
            unplaced_messages += 1
        else:
            positions.add(at)
    for index, item in enumerate(history):
        results: set[str] = set()
        calls: set[str] = set()
        _ids_in(item, results, calls)
        hit_results = results & trim.results
        hit_calls = calls & trim.calls
        if hit_results or hit_calls:
            positions.add(index)
            found_results |= hit_results
            found_calls |= hit_calls
    missing_results = len(trim.results - found_results)
    missing_calls = len(trim.calls - found_calls)
    if missing_results or missing_calls:
        for index, item in enumerate(history):
            if index in positions or (changed_at is not None and index not in changed_at):
                continue
            marked_results, marked_calls = _trim_marked_idless_parts(item)
            take_results = min(marked_results, missing_results)
            take_calls = min(marked_calls, missing_calls)
            if take_results or take_calls:
                positions.add(index)
                missing_results -= take_results
                missing_calls -= take_calls
    missing_stubs = trim.text_stubs
    if missing_stubs:
        # A stubbed message text names no id: placed by the stub's own words, only in an item that
        # changed this round (an item stubbed in an earlier round did not), never more than declared.
        for index, item in enumerate(history):
            if not missing_stubs:
                break
            if index in positions or (changed_at is not None and index not in changed_at):
                continue
            take = min(_stub_text_parts(item), missing_stubs)
            if take:
                positions.add(index)
                missing_stubs -= take
    unplaced = trim.unkeyed + missing_results + missing_calls + unplaced_messages + missing_stubs
    return frozenset(positions), unplaced


_TEXT_CUT_TAIL = __import__("re").compile(r"\[Cut to fit this call: [\d,]+ of [\d,]+ characters kept\]$")


def _is_fit_rewrite(text: Any) -> bool:
    """The last-resort fit's ``STUB_TEXT``, or a text the cut-to-fit pass ended with its marker."""
    from matrx_ai.config.input_fit import STUB_TEXT

    return isinstance(text, str) and (text == STUB_TEXT or bool(_TEXT_CUT_TAIL.search(text[-120:])))


def _stub_text_parts(item: Any) -> int:
    """How many text parts of one wire item the make-it-fit passes rewrote (stubbed or cut)."""
    if not isinstance(item, dict):
        return 0
    content = item.get("content", item.get("parts"))
    if isinstance(content, str):
        return int(_is_fit_rewrite(content))
    return sum(
        1 for part in content if isinstance(part, dict) and _is_fit_rewrite(part.get("text"))
    ) if isinstance(content, list) else 0


@dataclass(frozen=True)
class WireDrift:
    """What moved between two rounds: ``changed`` breaks the cached prefix and is filed;
    ``lawful`` is a change the send boundary DECLARED for this round (the context trim's
    rewritten blocks; moved Anthropic cache marks never reach the digests at all);
    ``tools_by_content`` is a tool change Layer 0b already reports."""

    compared_items: int
    changed: tuple[str, ...]
    lawful: tuple[str, ...]
    tools_by_content: tuple[str, ...]

    @property
    def stable(self) -> bool:
        return not (self.changed or self.lawful or self.tools_by_content)


def compare_wire_prefix(
    prev: WirePrefix,
    new: WirePrefix,
    *,
    trimmed_positions: frozenset[int] = frozenset(),
    trim_note: str = "",
    reasoning_dropped: bool = False,
    declared_heads: frozenset[str] = frozenset(),
) -> WireDrift:
    """Compare round N (``prev``) with round N+1 (``new``) up to the last stable item.

    ``trimmed_positions``: wire items holding a block this round's trim declared it rewrote
    (``place_trim_on_wire``); a changed item there is lawful. Every other change before the
    previous round's last item is drift, and ``trim_note`` (a declared rewrite that could not be
    placed on the wire) is named on it as a possible cause. Neither size nor a count decides.

    ``reasoning_dropped``: this round's fit declared dropped thinking. On a Responses wire a
    reasoning block is its own item, so dropping it shifts every later item; the reasoning items
    are then compared apart (each kept one must be an old one) and every other item is compared
    in order, so the shift is one declared break and unrelated drift is still filed."""
    changed: list[str] = []
    lawful: list[str] = []
    tools_by_content: list[str] = []
    prev_heads, new_heads = dict(prev.heads), dict(new.heads)
    for label in [*prev_heads, *(k for k in new_heads if k not in prev_heads)]:
        if prev_heads.get(label) != new_heads.get(label):
            if label in declared_heads:
                lawful.append(f"{label} changed: a one-call setting (declared)")
                continue
            if (
                label == "system"
                and label in prev_heads
                and label in new_heads
                and prev.system_outside_breaks
                and prev.system_outside_breaks == new.system_outside_breaks
            ):
                lawful.append("system changed only inside a declared seal break (platform_parts known_seal_break)")
                continue
            changed.append(f"{label} changed" if label in prev_heads and label in new_heads
                           else f"{label} {'removed' if label in prev_heads else 'added'}")
    for index, (name, exact, blind) in enumerate(prev.tools):
        if index >= len(new.tools):
            tools_by_content.append(f"tools[{index}] ({name}) removed")
            continue
        new_name, new_exact, new_blind = new.tools[index]
        if new_exact == exact:
            continue
        if new_name == name and new_blind == blind:
            changed.append(f"tools[{index}] ({name}) same content, different key order")
        else:
            tools_by_content.append(f"tools[{index}] ({name}) is now {new_name}")
    stable_items = max(len(prev.items) - 1, 0)
    if reasoning_dropped:
        shifted = _compare_without_dropped_reasoning(
            prev.items[:stable_items], new.items, trim_note, trimmed_positions
        )
        if shifted is not None:
            moved, declared, compared = shifted
            return WireDrift(
                compared_items=compared,
                changed=(*changed, *moved),
                lawful=(*lawful, *declared),
                tools_by_content=tuple(tools_by_content),
            )
    if len(new.items) < stable_items:
        changed.append(f"history window moved: {len(prev.items)} -> {len(new.items)} items")
    for index, ((label, digest, size), (_, new_digest, new_size)) in enumerate(
        zip(prev.items[:stable_items], new.items, strict=False)
    ):
        if digest == new_digest:
            continue
        note = f"{label} changed ({size:,} -> {new_size:,} bytes)"
        if index in trimmed_positions:
            lawful.append(f"{note}: context trim rewrite")
        else:
            changed.append(f"{note} (possible cause: {trim_note})" if trim_note else note)
    return WireDrift(
        compared_items=min(stable_items, len(new.items)),
        changed=tuple(changed),
        lawful=tuple(lawful),
        tools_by_content=tuple(tools_by_content),
    )


def _is_reasoning(item: tuple[str, str, int]) -> bool:
    return item[0].endswith("(reasoning)")


def _compare_without_dropped_reasoning(
    old: tuple[tuple[str, str, int], ...],
    new: tuple[tuple[str, str, int], ...],
    trim_note: str,
    trimmed_positions: frozenset[int],
) -> tuple[list[str], list[str], int] | None:
    """(changed, declared break, compared) when reasoning items left the old range, else None."""
    old_other = [item for item in old if not _is_reasoning(item)]
    old_reasoning = {item[1] for item in old if _is_reasoning(item)}
    if not old_reasoning:
        return None
    new_other: list[tuple[int, tuple[str, str, int]]] = []
    kept_reasoning: list[tuple[str, str, int]] = []
    for index, item in enumerate(new):
        if len(new_other) >= len(old_other):
            break
        if _is_reasoning(item):
            kept_reasoning.append(item)
        else:
            new_other.append((index, item))
    dropped = len(old) - len(old_other) - len(kept_reasoning)
    if dropped <= 0:
        return None
    changed: list[str] = []
    for item in kept_reasoning:
        if item[1] not in old_reasoning:
            changed.append(f"{item[0]} changed")
    if len(new_other) < len(old_other):
        changed.append(f"history window moved: {len(old) + 1} -> {len(new)} items")
    declared: list[str] = []
    for (label, digest, size), (index, (new_label, new_digest, new_size)) in zip(
        old_other, new_other, strict=False
    ):
        if digest != new_digest:
            note = f"{label} -> {new_label} changed ({size:,} -> {new_size:,} bytes)"
            if index in trimmed_positions:
                declared.append(f"{note}: context trim rewrite")
            else:
                changed.append(f"{note} (possible cause: {trim_note})" if trim_note else note)
    declared += [
        f"declared break: the make-it-fit pass dropped {dropped} reasoning item(s); every later item "
        "shifted position (compared in order without them)"
    ]
    return changed, declared, len(new_other) + len(kept_reasoning)


# ─────────────────────────────────────────────────────────────────────────────
# Per-loop state
# ─────────────────────────────────────────────────────────────────────────────


@dataclass
class _LoopCacheState:
    provider: str
    model: str
    call_count: int = 0
    last_call_ts: float = 0.0
    system_hash: str | None = None
    system_text: str = ""
    tool_names: tuple[str, ...] = ()
    ever_cache_read: bool = False
    miss_count: int = 0
    miss_banner_shown: bool = False
    #: Automatic-cache routing misses seen on a proven-stable wire in this loop (see Layer 2).
    routing_miss_count: int = 0
    system_drift_count: int = 0
    wire_prefix: WirePrefix | None = None
    wire_drift_reported: bool = False
    one_call_heads: frozenset[str] = frozenset()


_LOOPS: OrderedDict[str, _LoopCacheState] = OrderedDict()


def _loop_key(
    provider: str,
    conversation_id: str | None,
    request_id: str | None,
    loop_id: str | None = None,
) -> str:
    # One persisted conversation spans many independent user requests. The
    # request id is the actual provider/tool-loop identity: it remains stable
    # across rounds of one run and changes for the next user turn. Using the
    # conversation id first falsely compared separate turns and reported
    # legitimate frozen-prefix/context differences as mid-loop mutation.
    # Child agents intentionally inherit the root request id so cost and
    # persistence aggregate across the whole execution tree. Each child still
    # owns an independent provider/tool loop (and therefore its own stable
    # system prefix), identified by its conversation id. Key on both: request
    # alone conflates sibling agents, while conversation alone conflates
    # separate user turns in one durable conversation.
    # ``request_id`` names the user action and intentionally spans its child
    # executions.  When the executor gives us its per-invocation loop id,
    # prefer it: otherwise independent one-shot calls in the same durable
    # conversation look like consecutive rounds and produce a false drift.
    if loop_id:
        return f"{provider}:execution:{loop_id}"
    request_scope = request_id or "unknown-request"
    conversation_scope = conversation_id or "unknown-conversation"
    return f"{provider}:{request_scope}:{conversation_scope}"


def provider_prompt_cache_key(
    conversation_id: str | None, request_id: str | None
) -> str | None:
    """Return a stable, opaque cache-routing key for one CONVERSATION.

    🚨 THE CACHE LINE LAW, routing half (2026-10-17). OpenAI routes a request to a
    prompt cache by the prefix hash plus ``prompt_cache_key`` ("separates cache
    reuse between groups of requests"; guidance: about 15 requests per minute per
    key; keys route, they never pin). The key used to hash request id +
    conversation id, so EVERY TURN of one conversation carried a different key and
    turn N+1 was routed by chance, away from the cache turn N wrote. The group that
    shares a prefix across turns is the conversation, so the key is the
    conversation alone; the request id is only the fallback for a call with no
    conversation (an ephemeral run), whose prefix is not reused across turns
    anyway. Guard: ``tests/test_prompt_cache_key_is_stable_across_turns.py``.
    """
    if not conversation_id and not request_id:
        return None
    group = f"conversation:{conversation_id}" if conversation_id else f"request:{request_id}"
    digest = hashlib.sha256(group.encode()).hexdigest()
    return _PROMPT_CACHE_KEY_PREFIX + digest[:_PROMPT_CACHE_KEY_DIGEST_CHARS]


def normalize_openai_prompt_cache_key(value: str) -> str:
    """Enforce OpenAI's cache-key wire contract for every request source.

    The orchestrator normally supplies an already-bounded opaque key, but
    ``UnifiedConfig`` is public and other callers may set one directly. Hashing
    an oversized value preserves stable cache routing without leaking it or
    creating collisions through plain truncation.
    """
    if len(value) <= OPENAI_PROMPT_CACHE_KEY_MAX_CHARS:
        return value
    digest = hashlib.sha256(value.encode()).hexdigest()
    return _PROMPT_CACHE_KEY_PREFIX + digest[:_PROMPT_CACHE_KEY_DIGEST_CHARS]


def _get_or_create(key: str, provider: str, model: str) -> _LoopCacheState:
    state = _LOOPS.get(key)
    if state is None:
        state = _LoopCacheState(provider=provider, model=model)
        _LOOPS[key] = state
        while len(_LOOPS) > _MAX_TRACKED_LOOPS:
            _LOOPS.popitem(last=False)
    else:
        _LOOPS.move_to_end(key)
    return state


def reset_loop(conversation_id: str | None = None, request_id: str | None = None) -> None:
    """Drop tracked state for a finished loop (optional housekeeping). The LRU
    cap makes this unnecessary for correctness, but a caller that knows a loop
    is done may call it to free memory sooner."""
    for provider in list(_AUTO_CACHE_PROVIDERS | {"anthropic", "google"}):
        _LOOPS.pop(_loop_key(provider, conversation_id, request_id), None)


# ─────────────────────────────────────────────────────────────────────────────
# Provider-agnostic cache-metric extraction
# ─────────────────────────────────────────────────────────────────────────────


@dataclass
class CacheMetrics:
    provider: str
    uncached_input: int = 0
    cache_read: int = 0
    cache_write: int = 0
    output: int = 0
    fields_present: bool = False

    @property
    def total_input(self) -> int:
        return self.uncached_input + self.cache_read + self.cache_write


def extract_cache_metrics(provider: str, raw_usage: dict[str, Any] | None) -> CacheMetrics:
    """Pull cache read/write + uncached input out of a provider usage block.

    Each provider spells it differently and counts ``input_tokens`` differently
    (Anthropic EXCLUDES cache read/write from input_tokens; OpenAI/Google
    INCLUDE cached in the prompt total). Normalize to one shape so the guard —
    and any future consumer — reasons about caching identically everywhere.
    """
    raw = raw_usage or {}
    m = CacheMetrics(provider=provider)
    if provider == "anthropic":
        m.cache_read = int(raw.get("cache_read_input_tokens") or 0)
        m.cache_write = int(raw.get("cache_creation_input_tokens") or 0)
        # Anthropic input_tokens already excludes cache read + write.
        m.uncached_input = int(raw.get("input_tokens") or 0)
        m.output = int(raw.get("output_tokens") or 0)
        m.fields_present = "cache_read_input_tokens" in raw or "cache_creation_input_tokens" in raw
    elif provider == "openai":
        details = raw.get("input_tokens_details") or {}
        m.cache_read = int(details.get("cached_tokens") or 0)
        total = int(raw.get("input_tokens") or raw.get("prompt_tokens") or 0)
        m.uncached_input = max(total - m.cache_read, 0)
        m.output = int(raw.get("output_tokens") or raw.get("completion_tokens") or 0)
        m.fields_present = "input_tokens_details" in raw
    elif provider == "google":
        m.cache_read = int(raw.get("cached_content_token_count") or 0)
        total = int(raw.get("prompt_token_count") or 0)
        m.uncached_input = max(total - m.cache_read, 0)
        m.output = int(raw.get("candidates_token_count") or 0)
        m.fields_present = "prompt_token_count" in raw
    else:
        m.uncached_input = int(raw.get("input_tokens") or raw.get("prompt_tokens") or 0)
        m.output = int(raw.get("output_tokens") or raw.get("completion_tokens") or 0)
    return m


# ─────────────────────────────────────────────────────────────────────────────
# The public entry — call once per provider response inside a loop
# ─────────────────────────────────────────────────────────────────────────────


def observe_cache_usage(
    *,
    provider: str,
    model: str,
    conversation_id: str | None,
    request_id: str | None,
    loop_id: str | None = None,
    system_text: str,
    tool_names: tuple[str, ...] | list[str] | None,
    raw_usage: dict[str, Any] | None,
    prefix_frozen: bool = False,
    marks_withheld: bool = False,
    wire_payload: Any = None,
    trimmed_blocks: TrimDeclaration | None = None,
) -> None:
    """Record one provider call and SCREAM if caching drifted or failed.

    ``wire_payload`` must be the body captured for THIS round (``send_once`` clears the previous
    one before every provider call). ``trimmed_blocks``: this round's ``declared_history_rewrites``
    — the one lawful change to old history items, placed on the wire by call id.

    ``marks_withheld``: the send boundary's cache plan sent NO mark on this call
    (``config/cache_plan.py``), so a zero read on an explicit-mark wire is the plan, not a bug.

    Safe to call unconditionally after every provider response — it self-gates
    on provider, prompt size, and loop position, and never raises into the
    caller (a guard must never break the request it protects).
    """
    if not CACHE_GUARD_ENABLED:
        return
    if prefix_frozen and conversation_id:
        try:
            _observe_across_turns(
                provider=provider,
                model=model,
                conversation_id=conversation_id,
                request_id=request_id,
                loop_id=loop_id,
                system_text=system_text or "",
            )
        except Exception as exc:  # noqa: BLE001 — the guard must never break the loop
            vcprint(f"[cache_guard] cross-turn layer failed (non-fatal): {exc}", color="yellow")
    try:
        _observe(
            provider=provider,
            model=model,
            conversation_id=conversation_id,
            request_id=request_id,
            loop_id=loop_id,
            system_text=system_text or "",
            tool_names=tuple(tool_names or ()),
            raw_usage=raw_usage or {},
            marks_withheld=marks_withheld,
            wire_payload=wire_payload,
            trimmed_blocks=trimmed_blocks,
        )
    except Exception as exc:  # noqa: BLE001 — the guard must never break the loop
        vcprint(
            f"[cache_guard] guard itself failed (non-fatal, caching NOT affected): "
            f"{type(exc).__name__}: {exc}",
            color="yellow",
        )


# ─────────────────────────────────────────────────────────────────────────────
# Layer 0 — THE CACHE LINE ACROSS TURNS (Arman, 2026-10-16)
# ─────────────────────────────────────────────────────────────────────────────
#
# "NOTHING, other than the removal of LARGE tool outputs should ever modify
# text behind the cache line." Layer 1 compares rounds of ONE request only (its
# loop key is the request), so a frozen system prompt that changed between two
# TURNS of one conversation never screamed: the clock in the system channel and
# the org catalog flipping 8,764 -> 3,676 -> 8,764 chars (conversation 88a134af)
# both went unseen. This layer remembers the last frozen system text per
# (provider, conversation) and screams when a LATER request sends different
# text. Only frozen prompts are compared — and since 2026-10-16 a mandate-held
# conversation's held system text counts as frozen once the send boundary has
# settled it (``send_boundary._settle_held_prompt``; the executor passes
# ``prefix_frozen``). Its one lawful change, a Holder or catalog change, goes
# through ``deliberate_cache_break``, which resets this memory so it is
# reported once, as deliberate, never as a violation.

_CONVERSATION_PREFIX: OrderedDict[str, tuple[str, str, str]] = OrderedDict()
#: (conversation_id, kind) already alarmed by ``scream_cache_line_violation``.
_ALARMED: OrderedDict[tuple[str, str], None] = OrderedDict()
_MAX_ALARMED = 4096
_ALARM_LOCK = threading.Lock()


def _observe_across_turns(
    *,
    provider: str,
    model: str,
    conversation_id: str,
    request_id: str | None,
    loop_id: str | None,
    system_text: str,
) -> None:
    key = f"{provider}:{conversation_id}"
    this_loop = _loop_key(provider, conversation_id, request_id, loop_id)
    digest = hashlib.sha256(system_text.encode("utf-8", "replace")).hexdigest()
    previous = _CONVERSATION_PREFIX.get(key)
    _CONVERSATION_PREFIX[key] = (this_loop, digest, system_text)
    _CONVERSATION_PREFIX.move_to_end(key)
    while len(_CONVERSATION_PREFIX) > _MAX_TRACKED_LOOPS:
        _CONVERSATION_PREFIX.popitem(last=False)
    if previous is None:
        return
    prev_loop, prev_digest, prev_text = previous
    if prev_loop == this_loop or prev_digest == digest:
        return  # same request (Layer 1 owns it) or unchanged
    scream_cache_line_violation(
        kind="system_prompt_changed_between_turns",
        provider=provider,
        model=model,
        conversation_id=conversation_id,
        request_id=request_id,
        prev_text=prev_text,
        new_text=system_text,
        where="matrx_ai.providers.cache_guard.observe_cache_usage",
    )


# ─────────────────────────────────────────────────────────────────────────────
# Layer 0b — THE TOOLS BLOCK ACROSS THE WHOLE CONVERSATION (2026-10-16)
# ─────────────────────────────────────────────────────────────────────────────
#
# Tools head the provider cache prefix (tools -> system -> messages on
# Anthropic): a removal, reorder or byte change at tool position N re-writes the
# entire conversation at the cache-write price. Real jobs lost 980 cents this way
# across 14 conversations (common-docs systems/agents/projects/agent-evaluation/reports/
# tool-list-cache-stability.md). The declaration ledger
# (matrx_ai/tools/declaration_ledger.py) makes the array append-only; this layer
# is the INDEPENDENT check on the literal SDK payload: it remembers the last tools
# block per (provider, conversation) and SCREAMS (red banner + capture_error) when
# a later request's block is anything but the previous one with tools appended.

_CONVERSATION_TOOLS: OrderedDict[str, tuple[tuple[str, str], ...]] = OrderedDict()


def _declaration_identity(decl: Any) -> tuple[str, str] | None:
    """``(name, digest)`` for one provider declaration; ``cache_control`` excluded
    (a breakpoint marker is not tool content)."""
    if not isinstance(decl, dict):
        return None
    name = decl.get("name")
    if not isinstance(name, str):
        fn = decl.get("function")
        name = fn.get("name") if isinstance(fn, dict) else None
    if not isinstance(name, str):
        # Gemini: one Tool block carries its functions (``function_declarations``; camelCase on
        # the raw wire) or names a built-in tool by its one key (``google_search``, ``url_context``).
        fns = decl.get("function_declarations") or decl.get("functionDeclarations")
        if isinstance(fns, list) and fns:
            names = [str(f.get("name")) for f in fns if isinstance(f, dict) and f.get("name")]
            name = ",".join(names) if names else None
        elif not decl.get("type"):
            keys = [k for k, v in decl.items() if v is not None and k != "cache_control"]
            name = f"<{keys[0]}>" if len(keys) == 1 else None
    if not isinstance(name, str):
        name = f"<{decl.get('type') or 'nameless'}>"
    body = {k: v for k, v in decl.items() if k != "cache_control"}
    import json

    digest = hashlib.sha256(
        json.dumps(body, sort_keys=True, default=str).encode("utf-8", "replace")
    ).hexdigest()[:16]
    return name, digest


def payload_tool_declarations(payload: Any) -> list[Any] | None:
    """The literal ``tools`` list of an SDK-ready payload, or None when the
    payload shape carries none we can read (dict ``tools`` key or attribute)."""
    tools = payload.get("tools") if isinstance(payload, dict) else getattr(payload, "tools", None)
    return list(tools) if isinstance(tools, list | tuple) else None


def wire_tool_names(payload: Any) -> tuple[str, ...] | None:
    decls = payload_tool_declarations(payload)
    if decls is None:
        return None
    return tuple(i[0] for i in (_declaration_identity(d) for d in decls) if i is not None)


def _is_lawful_sorted_addition(
    previous: tuple[tuple[str, str], ...],
    current: tuple[tuple[str, str], ...],
    authored: frozenset[str] = frozenset(),
) -> bool:
    """A change that only ADDS tools, each at its place in the one name order: every earlier
    declaration still there, byte-identical, in the same relative order, and every tool added
    BETWEEN two others sorts between its neighbours in THE ONE ORDER (authored tier first, then
    platform-added, by name in each; ``authored`` = the ledger's authored wire names). Since P0.2 the ledger adds a tool at its
    sorted place (``matrx_ai.config.canonical_order``), not only at the end, so that is not a break
    to scream about; a removal, a re-description, a reorder or an out-of-order insert still is.
    (Provider-hosted tools a translator appends after the ledger, B10, ride at the end, so the
    check is per neighbour, not "the whole block is sorted".)"""
    from matrx_ai.tools.declaration_ledger import order_key

    cur_names = [n for n, _ in current]
    current_set = set(current)
    if not all(item in current_set for item in previous):
        return False
    prev_names = {n for n, _ in previous}
    if [n for n in cur_names if n in prev_names] != [n for n, _ in previous]:
        return False
    for i, name in enumerate(cur_names):
        if name in prev_names:
            continue
        before = cur_names[i - 1] if i > 0 else None
        after = cur_names[i + 1] if i + 1 < len(cur_names) else None
        # Two tiers (authored, then platform-added; ``declaration_ledger.order_key``), each by name.
        key = lambda n: order_key(n, authored)  # noqa: E731
        if after is not None and (key(name) > key(after) or (before is not None and key(before) > key(name))):
            return False
    return True


def observe_tool_declarations(
    *,
    provider: str | None,
    conversation_id: str | None,
    payload: Any,
    model: str = "",
) -> str | None:
    """Compare this request's tools block with the conversation's previous one.

    Returns the violation kind when it screamed (for tests), else None. Never
    raises. Rules: an empty block (a model/provider limit removed every tool)
    is not compared and not recorded. A block sharing NO tool with the previous
    one (a whole-belt swap, e.g. an agent switch) is recorded and screams
    ``tool_belt_replaced_mid_conversation`` unless the ledger already made and
    captured it as a deliberate break (adversarial I2, 2026-10-18).
    """
    if not CACHE_GUARD_ENABLED or not conversation_id:
        return None
    try:
        decls = payload_tool_declarations(payload)
        if not decls:
            return None
        current = tuple(i for i in (_declaration_identity(d) for d in decls) if i is not None)
        key = f"{provider or '?'}:{conversation_id}"
        previous = _CONVERSATION_TOOLS.get(key)
        disjoint = bool(previous) and not ({n for n, _ in current} & {n for n, _ in previous})
        _CONVERSATION_TOOLS[key] = current
        _CONVERSATION_TOOLS.move_to_end(key)
        while len(_CONVERSATION_TOOLS) > _MAX_TRACKED_LOOPS:
            _CONVERSATION_TOOLS.popitem(last=False)
        if previous is None or current[: len(previous)] == previous:
            return None  # first sight, unchanged, or a pure append
        from matrx_ai.tools.declaration_ledger import authored_names

        if _is_lawful_sorted_addition(previous, current, authored_names(provider or "", conversation_id)):
            return None  # new tools added at their sorted place (THE ONE ORDER, P0.2)
        from matrx_ai.tools.declaration_ledger import _NO_BREAK, consume_deliberate_scope

        scope = consume_deliberate_scope(conversation_id, provider)

        prev_names = [n for n, _ in previous]
        cur_names = [n for n, _ in current]
        removed = [n for n in prev_names if n not in cur_names]
        prev_digest = dict(previous)
        changed = [n for n, d in current if n in prev_digest and prev_digest[n] != d]
        kept = [n for n in cur_names if n in prev_digest]
        reordered = kept != [n for n in prev_names if n in cur_names]
        inserted = [
            n for i, n in enumerate(cur_names) if n not in prev_digest and i < len(prev_names)
        ]
        if scope is not _NO_BREAK:
            # The ledger recorded a break. Excuse it only when this request's change is
            # confined to the names that break covers (None = the whole belt); any
            # other change riding along is a second, unrecorded break (adversarial M5).
            touched = set(removed) | set(changed) | set(inserted)
            if scope is None or (not reordered and touched <= scope):
                return None
        kind = (
            "tool_belt_replaced_mid_conversation" if disjoint
            else "tool_removed_mid_conversation" if removed
            else "tool_definition_changed_mid_conversation" if changed
            else "tool_reordered_mid_conversation" if reordered
            else "tool_inserted_before_existing_tools"
        )
        first_diff = next(
            (i for i, (a, b) in enumerate(zip(previous, current, strict=False)) if a != b),
            min(len(previous), len(current)),
        )
        _scream_tool_list_change(
            kind=kind,
            provider=provider or "",
            model=model,
            conversation_id=conversation_id,
            removed=removed,
            changed=changed,
            reordered=reordered,
            inserted=inserted,
            first_diff=first_diff,
            previous_count=len(previous),
            current_count=len(current),
        )
        return kind
    except Exception as exc:  # noqa: BLE001 — a guard must never break the request
        vcprint(f"[cache_guard] tools-block layer failed (non-fatal): {exc}", color="yellow")
        return None


def _scream_tool_list_change(**details: Any) -> None:
    vcprint(
        f"\n{_BAR}\n"
        f"🚨🚨🚨  PROMPT CACHE KILLED — TOOLS BLOCK CHANGED MID-CONVERSATION  🚨🚨🚨\n"
        f"{_BAR}\n"
        f"kind={details['kind']} conversation={details['conversation_id']} "
        f"provider={details['provider']} model={details['model']}\n"
        f"Tools head the cache prefix: everything after tool #{details['first_diff'] + 1} "
        f"(system + the whole history) is re-written at the cache-write price.\n"
        f"A tool once sent must stay declared, in place, byte-identical; new tools are\n"
        f"added at their place in the one name order (matrx_ai/tools/declaration_ledger.py).\n"
        f"  removed  : {details['removed'] or '—'}\n"
        f"  changed  : {details['changed'] or '—'}\n"
        f"  inserted : {details['inserted'] or '—'}\n"
        f"  reordered: {details['reordered']}\n"
        f"  count    : {details['previous_count']} -> {details['current_count']}\n"
        f"{_BAR}\n",
        color="red",
        log_level="error",
    )
    _schedule_tool_list_capture(details)


def _schedule_tool_list_capture(details: dict[str, Any]) -> None:
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return
    detached_task(_capture_tool_list_change(details), name="tool_list_change_capture")


async def _capture_tool_list_change(details: dict[str, Any]) -> None:
    try:
        from matrx_connect.streaming.error_capture import capture_error

        await capture_error(
            RuntimeError(f"prompt cache: tools block changed mid-conversation ({details['kind']})"),
            kind="prompt_cache_tool_list_changed",
            error_type=details["kind"],
            route="matrx_ai.providers.cache_guard.observe_tool_declarations",
            payload={k: v for k, v in details.items() if k != "kind"},
        )
    except Exception:
        pass


def forget_tool_declarations(conversation_id: str | None) -> None:
    """Drop this worker's memory of a conversation's tools block (every provider).

    Called when the declaration ledger adopts a NEWER durable record than this worker holds: another worker
    sent the conversation's last turns (and recorded any break there), so this worker's own last block is no
    longer what the provider last saw. Comparing against it screamed a change the provider had already been
    sent (``ask_person``, conversation d0a43827, 2026-11-06)."""
    if not conversation_id:
        return
    suffix = f":{conversation_id}"
    for key in [k for k in _CONVERSATION_TOOLS if k.endswith(suffix)]:
        _CONVERSATION_TOOLS.pop(key, None)


def reset_tool_declarations_for_tests() -> None:
    _CONVERSATION_TOOLS.clear()
    with _ALARM_LOCK:
        _ALARMED.clear()


def scream_cache_line_violation(
    *,
    kind: str,
    conversation_id: str | None,
    request_id: str | None,
    prev_text: str,
    new_text: str,
    where: str,
    provider: str = "",
    model: str = "",
) -> None:
    """RED banner + a captured ``system_error`` for text changed behind the cache line.

    One function for every layer that detects it (the cross-turn guard here,
    the send boundary's frozen-prompt check), so the capture always has the
    same kind and shape. Never raises.

    ONE alarm per (conversation, kind) per process: the first sighting gets the
    banner and the captured row (with ``conversation_id`` on the row itself, so
    the queue groups it); repeats print one line. One conversation raised 297
    identical rows in 48 minutes (adversarial I6, 2026-10-18) and buried real ones.
    """
    if conversation_id:
        alarm_key = (str(conversation_id), kind)
        with _ALARM_LOCK:
            repeat = alarm_key in _ALARMED
            if not repeat:
                _ALARMED[alarm_key] = None
                while len(_ALARMED) > _MAX_ALARMED:
                    _ALARMED.popitem(last=False)
        if repeat:
            vcprint(
                f"[cache_guard] {kind} again on conversation {conversation_id} "
                f"(already alarmed once in this process; not re-captured)",
                color="yellow",
            )
            return
    banner = (
        f"\n{_BAR}\n"
        f"🚨🚨🚨  CACHE LINE LAW BROKEN — TEXT BEHIND THE CACHE LINE CHANGED  🚨🚨🚨\n"
        f"{_BAR}\n"
        f"kind={kind} conversation={conversation_id} request={request_id}\n"
        f"provider={provider} model={model}\n"
        f"Nothing but the removal of LARGE tool outputs may change text behind the\n"
        f"cache line between turns. Per-turn material belongs in the trailing\n"
        f"channel (MessageList.attach_turn_context), never in the system prompt.\n"
        f"\n{_short_diff(prev_text, new_text)}\n"
        f"{_BAR}\n"
    )
    vcprint(banner, color="red", log_level="error")
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return
    detached_task(
        _record_cache_line_violation(
            kind=kind,
            provider=provider,
            model=model,
            conversation_id=conversation_id,
            request_id=request_id,
            prev_text=prev_text,
            new_text=new_text,
            where=where,
        ),
        name="cache_line_violation_capture",
    )


def forget_conversation_prefix(conversation_id: str | None) -> None:
    """Drop the cross-turn memory for one conversation (every provider)."""
    if not conversation_id:
        return
    suffix = f":{conversation_id}"
    for key in [k for k in _CONVERSATION_PREFIX if k.endswith(suffix)]:
        _CONVERSATION_PREFIX.pop(key, None)


def deliberate_cache_break(
    *,
    kind: str,
    reason: str,
    conversation_id: str | None,
    prev_text: str,
    new_text: str,
    where: str,
) -> None:
    """A LAWFUL change behind the cache line, said out loud.

    The one change the law allows on a held system text is the Holder itself
    or the org catalog changing. It still re-writes the whole cached history
    at the cache-write price, so it is never silent: a banner, a captured
    record (kind ``prompt_cache_deliberate_break``, severity info: a log line, never an open
    error row — not a violation), and the
    cross-turn memory reset so Layer 0 does not report it a second time.
    Never raises.
    """
    banner = (
        f"\n{_BAR}\n"
        f"⚠️  DELIBERATE PROMPT-CACHE BREAK — {reason}\n"
        f"{_BAR}\n"
        f"kind={kind} conversation={conversation_id}\n"
        f"The held system text was re-rendered and frozen again; the cached\n"
        f"history is re-written once at the cache-write price.\n"
        f"\n{_short_diff(prev_text, new_text)}\n"
        f"{_BAR}\n"
    )
    vcprint(banner, color="yellow", log_level="warning")
    forget_conversation_prefix(conversation_id)
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return
    detached_task(
        _record_deliberate_break(
            kind=kind,
            reason=reason,
            conversation_id=conversation_id,
            prev_len=len(prev_text),
            new_len=len(new_text),
            where=where,
        ),
        name="deliberate_cache_break_capture",
    )


_UNREADABLE_CONFIG_SEEN: set[str] = set()


def _capture_unreadable_config(type_name: str) -> None:
    """A wire config the guard cannot read means its system text and tools go uncompared: a
    blind spot, never a console-only line. Recorded once per config type per process."""
    if type_name in _UNREADABLE_CONFIG_SEEN:
        return
    _UNREADABLE_CONFIG_SEEN.add(type_name)
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return
    detached_task(_record_unreadable_config(type_name), name="cache_guard_unreadable_config_capture")


async def _record_unreadable_config(type_name: str) -> None:
    try:
        from matrx_ai._ext import get_ext

        record_error = get_ext("record_error")
    except Exception:
        return
    if record_error is None:
        return
    try:
        pending = record_error(
            RuntimeError(f"cache guard cannot read a wire config of type {type_name}"),
            kind="prompt_cache_guard_blind",
            error_type="unreadable_wire_config",
            error_text="The cache guard could not read a provider config; its system text and tools are not compared",
            route="cache_guard.wire_prefix",
            payload={"config_type": type_name},
        )
        if inspect.isawaitable(pending):
            await pending
    except Exception:
        pass


async def _record_deliberate_break(
    *, kind: str, reason: str, conversation_id: str | None, prev_len: int, new_len: int, where: str
) -> None:
    try:
        from matrx_ai._ext import get_ext

        record_error = get_ext("record_error")
    except Exception:
        return
    if record_error is None:
        return
    try:
        pending = record_error(
            RuntimeError(f"deliberate prompt-cache break: {reason}"),
            kind="prompt_cache_deliberate_break",
            error_type=kind,
            error_text=f"Held system text re-rendered: {reason}",
            route=where,
            payload={
                "conversation_id": conversation_id,
                "reason": reason,
                "previous_length": prev_len,
                "current_length": new_len,
            },
            # A LAWFUL event (the Holder was edited or rebound, or the org catalog changed),
            # never a defect: it is recorded as an info notice (a log line in ops.app_log),
            # not an open ops.system_error row nobody can fix (2026-11-17: every Chief of
            # Staff save filed one). Real breaks stay violations: scream_cache_line_violation.
            context={"severity": "info"},
        )
        if inspect.isawaitable(pending):
            await pending
    except Exception:
        pass


def _uuid_or_none(value: str | None) -> str | None:
    """The value when it is a UUID (the ``system_error.conversation_id`` column is one)."""
    if not value:
        return None
    try:
        import uuid

        return str(uuid.UUID(str(value)))
    except (ValueError, TypeError):
        return None


async def _record_cache_line_violation(
    *,
    kind: str,
    provider: str,
    model: str,
    conversation_id: str | None,
    request_id: str | None,
    prev_text: str,
    new_text: str,
    where: str,
) -> None:
    try:
        from matrx_ai._ext import get_ext

        record_error = get_ext("record_error")
    except Exception:
        return
    if record_error is None:
        return
    divergence = 0
    shared = min(len(prev_text), len(new_text))
    while divergence < shared and prev_text[divergence] == new_text[divergence]:
        divergence += 1
    try:
        pending = record_error(
            RuntimeError(f"cache line law broken: {kind}"),
            kind="prompt_cache_line_violation",
            error_type=kind,
            error_text="Text behind the prompt-cache line changed between turns",
            route=where,
            conversation_id=_uuid_or_none(conversation_id),
            payload={
                "provider": provider,
                "model": model,
                "conversation_id": conversation_id,
                "request_id": request_id,
                "previous_length": len(prev_text),
                "current_length": len(new_text),
                "first_divergence": divergence,
            },
        )
        if inspect.isawaitable(pending):
            await pending
    except Exception:
        pass


def _observe(
    *,
    provider: str,
    model: str,
    conversation_id: str | None,
    request_id: str | None,
    loop_id: str | None,
    system_text: str,
    tool_names: tuple[str, ...],
    raw_usage: dict[str, Any],
    marks_withheld: bool = False,
    wire_payload: Any = None,
    trimmed_blocks: TrimDeclaration | None = None,
) -> None:
    key = _loop_key(provider, conversation_id, request_id, loop_id)
    state = _get_or_create(key, provider, model)

    call_index = state.call_count  # 0 for the first call in this loop
    now = time.time()
    elapsed = now - state.last_call_ts if state.last_call_ts else 0.0

    system_hash = hashlib.sha256(system_text.encode("utf-8", "replace")).hexdigest()
    prev_system_hash = state.system_hash
    prev_system_text = state.system_text
    prev_tool_names = state.tool_names

    metrics = extract_cache_metrics(provider, raw_usage)
    if metrics.cache_read > 0:
        state.ever_cache_read = True

    system_changed = (
        call_index > 0 and prev_system_hash is not None and system_hash != prev_system_hash
    )
    tools_changed = call_index > 0 and tool_names != prev_tool_names

    # ── Layer 1b: THE WHOLE WIRE PREFIX — names any byte that moved. ─────────
    # Its own try: a bug here is captured and can never skip Layer 1, Layer 2 (the miss
    # alarm) or the state update below.
    wire: WirePrefix | None = None
    wire_drift: WireDrift | None = None
    round_heads = trimmed_blocks.heads if isinstance(trimmed_blocks, TrimDeclaration) else frozenset()
    try:
        if wire_payload is not None:
            wire = wire_prefix(wire_payload, state.wire_prefix if call_index > 0 else None)
        if call_index > 0 and wire is not None and state.wire_prefix is not None:
            trimmed_positions: frozenset[int] = frozenset()
            trim_note = ""
            if isinstance(trimmed_blocks, TrimDeclaration) and trimmed_blocks:
                trimmed_positions, unplaced = place_trim_on_wire(
                    wire_payload, trimmed_blocks, changed_at=changed_item_positions(state.wire_prefix, wire)
                )
                if unplaced:
                    trim_note = f"the send boundary rewrote {unplaced} block(s) it could not place on the wire"
            wire_drift = compare_wire_prefix(
                state.wire_prefix,
                wire,
                trimmed_positions=trimmed_positions,
                trim_note=trim_note,
                reasoning_dropped=isinstance(trimmed_blocks, TrimDeclaration)
                and trimmed_blocks.thinking_dropped > 0,
                # A one-call head change is declared on the round that sends it and on the round
                # after, which restores the authored setting.
                declared_heads=round_heads | state.one_call_heads,
            )
            if not wire_drift.stable:
                _notice_wire_drift(
                    provider=provider,
                    model=model,
                    conversation_id=conversation_id,
                    request_id=request_id,
                    call_index=call_index,
                    drift=wire_drift,
                    file=bool(wire_drift.changed) and not system_changed and not state.wire_drift_reported,
                    prefix_sha=state.wire_prefix.sha(wire_drift.compared_items),
                )
                if wire_drift.changed and not system_changed:
                    state.wire_drift_reported = True
    except Exception as exc:  # noqa: BLE001 — announced and captured, never fatal
        wire_drift = None
        try:
            _wire_layer_failed(exc, provider=provider, model=model, conversation_id=conversation_id, call_index=call_index)
        except Exception:  # noqa: BLE001 — the failure report itself must not skip Layer 2
            pass

    # ── Layer 1: SYSTEM PROMPT DRIFT — the cardinal rule violation. ──────────
    if system_changed:
        state.system_drift_count += 1
        _scream_system_drift(
            provider=provider,
            model=model,
            conversation_id=conversation_id,
            request_id=request_id,
            call_index=call_index,
            prev_system=prev_system_text,
            new_system=system_text,
            drift_count=state.system_drift_count,
        )
    elif tools_changed:
        _notice_tool_drift(
            provider=provider,
            model=model,
            conversation_id=conversation_id,
            call_index=call_index,
            prev_tools=prev_tool_names,
            new_tools=tool_names,
        )

    # ── Layer 2: CACHE EFFECTIVENESS — ground truth from provider usage. ─────
    # Only meaningful when: caching is expected for this provider, we're past
    # the first call, the prefix DID NOT change (so a read was legitimately
    # expected), the prompt is big enough to cache, the cache hasn't expired
    # by the best timing evidence we have, and the provider did not create a
    # fresh cache entry. A cache write proves the breakpoint reached Anthropic;
    # zero read + a full write near the five-minute boundary is an ordinary TTL
    # refresh, not a broken producer. Observation happens after the response,
    # so response-to-response elapsed time can understate wire-to-wire age by
    # the previous call's latency.
    prefix_stable = not system_changed and not tools_changed
    cacheable_threshold = cacheable_input_threshold(provider, model)
    if (
        provider in _expected_cache_providers()
        # Anthropic caches only behind explicit marks; with none sent a read is not expected.
        and not (marks_withheld and provider not in _AUTO_CACHE_PROVIDERS)
        and call_index > 0
        and prefix_stable
        and metrics.total_input >= cacheable_threshold
        and metrics.cache_read == 0
        and metrics.cache_write == 0
        and (elapsed == 0.0 or elapsed <= CACHE_TTL_GRACE_SECONDS)
    ):
        if (
            provider in _AUTO_CACHE_PROVIDERS
            and wire_drift is not None
            and wire_drift.stable
        ):
            # AUTOMATIC CACHING IS ROUTED, NOT PROMISED (2026-11-14, widened 2026-11-15). OpenAI caches by
            # routing the request to a machine holding the prefix (hash + prompt_cache_key); a request that
            # lands elsewhere reads nothing even when every byte matches. Layer 1b PROVED this round's wire
            # prefix repeated byte for byte, so the zero read is the provider's routing, not our prefix.
            # Proof: the PB-03 copy-O 2-call loop replayed straight at the Responses API (nothing of ours in
            # the path) read zero on call 2 in 4 of 18 runs (3 of 6 in one streamed batch); our server read zero
            # in 3 of 5. Misses in one loop are ordinary, so a single loop files none; a streak across loops
            # does (OPENAI_STABLE_MISS_STREAK_TO_FILE). What IS ours stays loud: a moved prefix files
            # prompt_cache_prefix_drift, and a miss with no wire proof or on an explicit-mark provider
            # (Anthropic) screams below.
            state.routing_miss_count += 1
            streak = _bump_stable_miss_streak(provider, model)
            streak_to_file = stable_miss_streak_to_file()
            vcprint(
                f"[cache_guard] {provider} read nothing from cache on a byte-stable prefix "
                f"(call #{call_index + 1}, {metrics.total_input:,} input tokens, model={model}) — "
                f"automatic cache routing miss #{state.routing_miss_count} this loop, {streak} in a row "
                f"for this model (filed at {streak_to_file}).",
                color="yellow",
                log_level="warning",
            )
            if streak >= streak_to_file:
                # NOTHING FAILS SILENTLY: chance misses are ordinary, a cache that never hits is not. The
                # streak spans loops and resets on any hit, so a permanent miss from a cause outside the
                # compared bytes (account, SDK, provider contract) files here, then re-arms.
                _clear_stable_miss_streak(provider, model)
                state.miss_count += 1
                _scream_cache_miss(
                    provider=provider,
                    model=model,
                    conversation_id=conversation_id,
                    request_id=request_id,
                    call_index=call_index,
                    metrics=metrics,
                    raw_usage=raw_usage,
                    elapsed=elapsed,
                    miss_count=state.miss_count,
                    first_banner=True,
                    cacheable_threshold=cacheable_threshold,
                    wire_drift=wire_drift,
                    stable_miss_streak=streak,
                )
                state.miss_banner_shown = True
        else:
            state.miss_count += 1
            _scream_cache_miss(
                provider=provider,
                model=model,
                conversation_id=conversation_id,
                request_id=request_id,
                call_index=call_index,
                metrics=metrics,
                raw_usage=raw_usage,
                elapsed=elapsed,
                miss_count=state.miss_count,
                first_banner=not state.miss_banner_shown,
                cacheable_threshold=cacheable_threshold,
                wire_drift=wire_drift,
            )
            state.miss_banner_shown = True

    if provider in _AUTO_CACHE_PROVIDERS and metrics.cache_read > 0:
        _clear_stable_miss_streak(provider, model)

    # ── Advance state ────────────────────────────────────────────────────────
    state.call_count += 1
    state.last_call_ts = now
    state.system_hash = system_hash
    state.system_text = system_text
    state.tool_names = tool_names
    if wire is not None:
        state.wire_prefix = wire
    state.one_call_heads = round_heads


# ─────────────────────────────────────────────────────────────────────────────
# The screaming
# ─────────────────────────────────────────────────────────────────────────────

_BAR = "█" * 78


def _short_diff(prev: str, new: str, limit: int = 900) -> str:
    """A compact, human-readable diff of two system prompts — the first point
    they diverge plus a window around it, so the log shows WHAT changed."""
    if prev == new:
        return "(identical)"
    # Find first divergence.
    i = 0
    n = min(len(prev), len(new))
    while i < n and prev[i] == new[i]:
        i += 1
    start = max(0, i - 80)
    prev_win = prev[start : i + 160]
    new_win = new[start : i + 160]
    out = [
        f"first divergence at char {i} (prev_len={len(prev)}, new_len={len(new)})",
        f"  PREV …{prev_win!r}…",
        f"  NEW  …{new_win!r}…",
    ]
    text = "\n".join(out)
    return text[:limit] + ("… (truncated)" if len(text) > limit else "")


def _scream_system_drift(
    *,
    provider: str,
    model: str,
    conversation_id: str | None,
    request_id: str | None,
    call_index: int,
    prev_system: str,
    new_system: str,
    drift_count: int,
) -> None:
    banner = (
        f"\n{_BAR}\n"
        f"🚨🚨🚨  PROMPT CACHE KILLED — SYSTEM PROMPT MUTATED BETWEEN ROUNDS  🚨🚨🚨\n"
        f"{_BAR}\n"
        f"The system prompt CHANGED between call #{call_index} and call #{call_index + 1}\n"
        f"of the SAME loop. This is strictly forbidden: it violates the "
        f"'never modify the\nsystem prompt between rounds' rule AND it destroys "
        f"the provider prompt cache —\nevery subsequent round re-pays FULL input "
        f"price (this is why cached_input_tokens=0).\n"
        f"\n"
        f"  provider        : {provider}\n"
        f"  model           : {model}\n"
        f"  conversation_id : {conversation_id}\n"
        f"  request_id      : {request_id}\n"
        f"  drift #         : {drift_count} in this loop\n"
        f"\n"
        f"WHAT CHANGED (system prompt):\n{_short_diff(prev_system, new_system)}\n"
        f"\n"
        f"LIKELY CAUSE: something is re-injecting per-turn content into the SYSTEM\n"
        f"instruction inside the loop (a timestamp/date line, a re-attached context\n"
        f"block, dynamic instructions). Move per-turn content OUT of the system\n"
        f"prompt (into a user/ephemeral message) so the system prefix stays byte-stable.\n"
        f"{_BAR}\n"
    )
    vcprint(banner, color="red", log_level="error")
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return
    detached_task(
        _record_system_drift(
            provider=provider,
            model=model,
            conversation_id=conversation_id,
            request_id=request_id,
            call_index=call_index,
            prev_system=prev_system,
            new_system=new_system,
        ),
        name="prompt_cache_system_drift_capture",
    )


async def _record_system_drift(
    *,
    provider: str,
    model: str,
    conversation_id: str | None,
    request_id: str | None,
    call_index: int,
    prev_system: str,
    new_system: str,
) -> None:
    """Capture genuine within-request drift without retaining prompt contents."""
    try:
        from matrx_ai._ext import get_ext

        record_error = get_ext("record_error")
    except Exception:
        return
    if record_error is None:
        return

    divergence = 0
    shared = min(len(prev_system), len(new_system))
    while divergence < shared and prev_system[divergence] == new_system[divergence]:
        divergence += 1

    try:
        pending = record_error(
            RuntimeError("system prompt mutated between provider rounds"),
            kind="prompt_cache_system_drift",
            error_type="prompt_cache_system_drift",
            error_text="System prompt mutated between rounds of one provider request",
            route="matrx_ai.providers.cache_guard.observe_cache_usage",
            payload={
                "provider": provider,
                "model": model,
                "conversation_id": conversation_id,
                "request_id": request_id,
                "previous_call": call_index,
                "current_call": call_index + 1,
                "previous_length": len(prev_system),
                "current_length": len(new_system),
                "first_divergence": divergence,
            },
        )
        if inspect.isawaitable(pending):
            await pending
    except Exception:
        # Observability must never break a paid provider call.
        pass


def _notice_tool_drift(
    *,
    provider: str,
    model: str,
    conversation_id: str | None,
    call_index: int,
    prev_tools: tuple[str, ...],
    new_tools: tuple[str, ...],
) -> None:
    added = [t for t in new_tools if t not in prev_tools]
    removed = [t for t in prev_tools if t not in new_tools]
    vcprint(
        f"\n{'▓' * 78}\n"
        f"⚠️  PROMPT CACHE PREFIX INVALIDATED — TOOL SET CHANGED MID-LOOP\n"
        f"{'▓' * 78}\n"
        f"Between call #{call_index} and #{call_index + 1} the tool set changed, which\n"
        f"invalidates the provider cache prefix for THIS turn (tools sit ahead of the\n"
        f"system prompt in the cache order, so any tool change busts everything after it).\n"
        f"This is expected IF dynamic tool injection legitimately ran; if the tool set\n"
        f"should have been stable, this is the caching bug.\n"
        f"  provider={provider} model={model} conversation_id={conversation_id}\n"
        f"  added  : {added or '—'}\n"
        f"  removed: {removed or '—'}\n"
        f"{'▓' * 78}\n",
        color="yellow",
        log_level="warning",
    )


def _scream_cache_miss(
    *,
    provider: str,
    model: str,
    conversation_id: str | None,
    request_id: str | None,
    call_index: int,
    metrics: CacheMetrics,
    raw_usage: dict[str, Any],
    elapsed: float,
    miss_count: int,
    first_banner: bool,
    cacheable_threshold: int,
    wire_drift: WireDrift | None = None,
    stable_miss_streak: int | None = None,
) -> None:
    if not first_banner:
        # Keep the log bleeding without burying the detail: one compact red line
        # per subsequent miss, pointing back at the first banner.
        vcprint(
            f"🚨 [cache_guard] STILL ZERO CACHE READ on a stable prefix "
            f"(miss #{miss_count} this loop, call #{call_index + 1}, provider={provider}, "
            f"total_input={metrics.total_input:,} tokens) — see the first banner above.",
            color="red",
            log_level="error",
        )
        return

    marker_hint = (
        "we DID request cache_control breakpoints (PROMPT_CACHING_ENABLED=True) but the\n"
        "provider reported no cache read"
        if provider == "anthropic"
        else "this provider caches automatically but reported no cache read"
    )
    banner = (
        f"\n{_BAR}\n"
        f"🚨🚨🚨  PROMPT CACHE NOT WORKING — ZERO CACHE READ ON A STABLE PREFIX  🚨🚨🚨\n"
        f"{_BAR}\n"
        f"Call #{call_index + 1} of this loop sent a prefix identical to the previous\n"
        f"round and large enough to cache ({metrics.total_input:,} input tokens ≥ "
        f"{cacheable_threshold:,}),\n"
        f"yet the provider read NOTHING from cache. {marker_hint}.\n"
        f"Every round is re-paying full input price — this is a real, expensive bug.\n"
        f"\n"
        f"  provider        : {provider}\n"
        f"  model           : {model}\n"
        f"  conversation_id : {conversation_id}\n"
        f"  request_id      : {request_id}\n"
        f"  seconds since prev call: {elapsed:.1f}  (TTL grace {CACHE_TTL_GRACE_SECONDS}s)\n"
        f"\n"
        f"  cache_read  : {metrics.cache_read:,}   ← EXPECTED > 0\n"
        f"  cache_write : {metrics.cache_write:,}\n"
        f"  uncached_in : {metrics.uncached_input:,}\n"
        f"  output      : {metrics.output:,}\n"
        f"  raw usage   : {raw_usage}\n"
        f"\n"
        f"LIKELY CAUSES (in order):\n"
        f"  1. cache_control breakpoints were dropped from the request "
        f"(check the translator).\n"
        f"  2. The prefix is subtly unstable each round (a date/timestamp, re-ordered\n"
        f"     tools, re-serialized JSON with unsorted keys) — Layer 1 catches gross\n"
        f"     drift but a byte-level wobble under the breakpoint still zeroes the cache.\n"
        f"  3. Provider/SDK/beta-header change altered the caching contract.\n"
        f"  WIRE PREFIX (every byte up to the last stable item): {_wire_verdict(wire_drift)}\n"
        f"{_BAR}\n"
    )
    vcprint(banner, color="red", log_level="error")
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return
    detached_task(
        _record_cache_miss(
            provider=provider,
            model=model,
            conversation_id=conversation_id,
            request_id=request_id,
            call_index=call_index,
            metrics=metrics,
            cacheable_threshold=cacheable_threshold,
            wire_drift=wire_drift,
            stable_miss_streak=stable_miss_streak,
        ),
        name="prompt_cache_miss_capture",
    )


async def _record_cache_miss(
    *,
    provider: str,
    model: str,
    conversation_id: str | None,
    request_id: str | None,
    call_index: int,
    metrics: CacheMetrics,
    cacheable_threshold: int,
    wire_drift: WireDrift | None = None,
    stable_miss_streak: int | None = None,
) -> None:
    """Capture a genuine cache miss without retaining prompts or raw usage."""
    try:
        from matrx_ai._ext import get_ext

        record_error = get_ext("record_error")
    except Exception:
        return
    if record_error is None:
        return

    try:
        pending = record_error(
            RuntimeError("stable cacheable provider prefix produced zero cache read"),
            kind="prompt_cache_read_missing",
            error_type="prompt_cache_read_missing",
            error_text="Stable cacheable provider prefix produced zero cache read",
            route="matrx_ai.providers.cache_guard.observe_cache_usage",
            payload={
                "provider": provider,
                "model": model,
                "conversation_id": conversation_id,
                "request_id": request_id,
                "call_index": call_index + 1,
                "total_input_tokens": metrics.total_input,
                "cacheable_threshold": cacheable_threshold,
                "cache_read_input_tokens": metrics.cache_read,
                "cache_creation_input_tokens": metrics.cache_write,
                # None = no wire body reached the guard; True = every byte up to the last
                # stable item repeated, so the zero read is the provider's, not the prefix's.
                "wire_prefix_stable": None if wire_drift is None else wire_drift.stable,
                "wire_prefix_compared_items": None if wire_drift is None else wire_drift.compared_items,
                "wire_prefix_changed": None
                if wire_drift is None
                else [*wire_drift.changed, *wire_drift.tools_by_content, *wire_drift.lawful],
                # Set when the row is an escalation: this many zero reads in a row on a proven-stable prefix.
                "stable_miss_streak": stable_miss_streak,
            },
        )
        if inspect.isawaitable(pending):
            await pending
    except Exception:
        # Observability must never break a paid provider call.
        pass


def _wire_layer_failed(
    exc: Exception, *, provider: str, model: str, conversation_id: str | None, call_index: int
) -> None:
    """The wire layer raised: say so, and capture it, without touching the other layers."""
    vcprint(
        f"[cache_guard] wire prefix layer failed (non-fatal, miss alarm unaffected): {type(exc).__name__}: {exc}",
        color="yellow",
        log_level="warning",
    )
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return

    async def _capture() -> None:
        try:
            from matrx_connect.streaming.error_capture import capture_error

            await capture_error(
                exc,
                kind="prompt_cache_wire_layer_failed",
                error_type=type(exc).__name__,
                route="matrx_ai.providers.cache_guard.observe_cache_usage",
                payload={"provider": provider, "model": model, "conversation_id": conversation_id, "call_index": call_index},
            )
        except Exception:
            pass

    detached_task(_capture(), name="prompt_cache_wire_layer_failed_capture")


def _wire_verdict(drift: WireDrift | None) -> str:
    if drift is None:
        return "not compared (no wire body reached the guard)"
    if drift.stable:
        return f"byte-identical across {drift.compared_items} history item(s), tools, system and cache key"
    return "; ".join([*drift.changed, *drift.tools_by_content, *drift.lawful])


def _notice_wire_drift(
    *,
    provider: str,
    model: str,
    conversation_id: str | None,
    request_id: str | None,
    call_index: int,
    drift: WireDrift,
    file: bool,
    prefix_sha: str,
) -> None:
    """Say what moved in the wire prefix; file it once per loop when it breaks the cache."""
    vcprint(
        f"[cache_guard] WIRE PREFIX MOVED between call #{call_index} and #{call_index + 1} "
        f"(provider={provider}, model={model}, conversation={conversation_id}): {_wire_verdict(drift)}",
        color="red" if drift.changed else "yellow",
        log_level="error" if drift.changed else "warning",
    )
    if not file:
        return
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return
    detached_task(
        _record_wire_drift(
            provider=provider,
            model=model,
            conversation_id=conversation_id,
            request_id=request_id,
            call_index=call_index,
            drift=drift,
            prefix_sha=prefix_sha,
        ),
        name="prompt_cache_prefix_drift_capture",
    )


async def _record_wire_drift(
    *,
    provider: str,
    model: str,
    conversation_id: str | None,
    request_id: str | None,
    call_index: int,
    drift: WireDrift,
    prefix_sha: str,
) -> None:
    """Capture a within-loop wire-prefix change: labels, sizes and digests, never prompt text."""
    try:
        from matrx_ai._ext import get_ext

        record_error = get_ext("record_error")
    except Exception:
        return
    if record_error is None:
        return
    try:
        pending = record_error(
            RuntimeError("provider wire prefix changed between rounds of one loop"),
            kind="prompt_cache_prefix_drift",
            error_type="prompt_cache_prefix_drift",
            error_text="Wire prefix changed between rounds of one provider loop: " + "; ".join(drift.changed)[:400],
            route="matrx_ai.providers.cache_guard.observe_cache_usage",
            payload={
                "provider": provider,
                "model": model,
                "conversation_id": conversation_id,
                "request_id": request_id,
                "previous_call": call_index,
                "current_call": call_index + 1,
                "compared_items": drift.compared_items,
                "previous_prefix_sha": prefix_sha,
                "changed": list(drift.changed),
                "also_moved": [*drift.tools_by_content, *drift.lawful],
            },
        )
        if inspect.isawaitable(pending):
            await pending
    except Exception:
        # Observability must never break a paid provider call.
        pass
