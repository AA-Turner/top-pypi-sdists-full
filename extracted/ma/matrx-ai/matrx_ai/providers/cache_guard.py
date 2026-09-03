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

  Layer 2 — CACHE EFFECTIVENESS. Ground truth from the provider's own usage
  block. On any call after the first in a loop, when the prefix was stable and
  the prompt was large enough to cache, ``cache_read`` MUST be > 0. Zero cache
  read on a stable, large prefix → RED banner: caching is broken.

The stability layer is provider-agnostic. The effectiveness alarm is narrower:
it only covers providers whose cache contract makes a hit mandatory for the
request shape. Google implicit caching is opportunistic (and its minimum input
varies by model), so a zero Google cache read is telemetry, not an ERROR.

``PROMPT_CACHING_ENABLED`` also lives here — it is the SINGLE flag that both
(a) makes the Anthropic translator emit ``cache_control`` breakpoints and
(b) makes Layer 2 expect Anthropic cache reads. They can never drift.
"""

from __future__ import annotations

import asyncio
import hashlib
import inspect
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
    system_drift_count: int = 0


_LOOPS: OrderedDict[str, _LoopCacheState] = OrderedDict()


def _loop_key(provider: str, conversation_id: str | None, request_id: str | None) -> str:
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
    request_scope = request_id or "unknown-request"
    conversation_scope = conversation_id or "unknown-conversation"
    return f"{provider}:{request_scope}:{conversation_scope}"


def provider_prompt_cache_key(
    conversation_id: str | None, request_id: str | None
) -> str | None:
    """Return a stable, opaque cache-routing key for one provider/tool loop."""
    if not conversation_id and not request_id:
        return None
    loop_identity = f"{request_id or 'unknown-request'}:{conversation_id or 'unknown-conversation'}"
    digest = hashlib.sha256(loop_identity.encode()).hexdigest()
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
    INCLUDE cached in the prompt total). Normalise to one shape so the guard —
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
    system_text: str,
    tool_names: tuple[str, ...] | list[str] | None,
    raw_usage: dict[str, Any] | None,
) -> None:
    """Record one provider call and SCREAM if caching drifted or failed.

    Safe to call unconditionally after every provider response — it self-gates
    on provider, prompt size, and loop position, and never raises into the
    caller (a guard must never break the request it protects).
    """
    if not CACHE_GUARD_ENABLED:
        return
    try:
        _observe(
            provider=provider,
            model=model,
            conversation_id=conversation_id,
            request_id=request_id,
            system_text=system_text or "",
            tool_names=tuple(tool_names or ()),
            raw_usage=raw_usage or {},
        )
    except Exception as exc:  # noqa: BLE001 — the guard must never break the loop
        vcprint(
            f"[cache_guard] guard itself failed (non-fatal, caching NOT affected): "
            f"{type(exc).__name__}: {exc}",
            color="yellow",
        )


def _observe(
    *,
    provider: str,
    model: str,
    conversation_id: str | None,
    request_id: str | None,
    system_text: str,
    tool_names: tuple[str, ...],
    raw_usage: dict[str, Any],
) -> None:
    key = _loop_key(provider, conversation_id, request_id)
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
        and call_index > 0
        and prefix_stable
        and metrics.total_input >= cacheable_threshold
        and metrics.cache_read == 0
        and metrics.cache_write == 0
        and (elapsed == 0.0 or elapsed <= CACHE_TTL_GRACE_SECONDS)
    ):
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
        )
        state.miss_banner_shown = True

    # ── Advance state ────────────────────────────────────────────────────────
    state.call_count += 1
    state.last_call_ts = now
    state.system_hash = system_hash
    state.system_text = system_text
    state.tool_names = tool_names


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
            },
        )
        if inspect.isawaitable(pending):
            await pending
    except Exception:
        # Observability must never break a paid provider call.
        pass
