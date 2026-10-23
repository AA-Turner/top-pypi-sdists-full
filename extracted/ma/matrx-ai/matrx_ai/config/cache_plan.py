"""PROMPT CACHE PLAN — which cache marks a send writes, decided ONCE at the send boundary.

A cache mark is a WRITE, and a write only pays when a LATER call reads it (Anthropic: a 5-minute
write costs 1.25x input, a 1-hour write 2x, a read 0.1x or less). A tool loop or a conversation
reads its own marks on the next round; a one-shot call (a workflow writer step, a strict-JSON
funnel call) has no next round, so its rolling mark is a pure 25% surcharge. Measured
2026-10-21 on agent build 665d38ad: five one-shot Opus writer calls wrote 37,842 tokens to
cache and read 2,669 (common-docs masterwork/agent-creation-studio/projects/rebuild/lane-3A-l.md).

The decision, per send (``decide_cache_plan``):

* not declared one-shot (every chat, every conversation door)  -> ``all`` (system, template,
  rolling), unchanged;
* declared one-shot (``one_shot_call()``) but tools are declared -> ``all``: a tool loop reads
  its rolling mark on the next iteration;
* declared one-shot, no tools -> the ``agents.prompt_cache.one_shot_marks`` knob:
    - ``when_read_expected`` (start value) -> ``prefix`` when a later read IS expected — the
      agent's long-cache setting is on (its purpose: runs spaced up to an hour apart reuse the
      stable system + template prefix), or the same prefix was sent within its cache life
      (a repeated mandate: a batch, a send-back) — else ``none``;
    - ``never`` -> ``none``;  ``prefix`` -> ``prefix``;  ``always`` -> ``all`` (the old behavior).

The doors that DECLARE a call one-shot are the ones that are one-shot by construction:
``graph_nodes.agent_action.run_step_agent`` (every workflow agent step) and the strict-JSON /
text funnel (``graph_nodes._strict_json._run_completion_measured``). A later person turn on such a
conversation comes through a chat door, outside the scope, and caches as a conversation.

Guard: ``tests/test_one_shot_calls_write_no_cache.py``.
"""

from __future__ import annotations

import hashlib
import sys
import time
from collections import OrderedDict
from collections.abc import Callable, Generator
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass
from typing import Any

#: The plan values the translators read off ``UnifiedConfig.prompt_cache_marks``.
MARKS_ALL = "all"  # system (or last tool), template, rolling
MARKS_PREFIX = "prefix"  # system (or last tool), template — no rolling history mark
MARKS_NONE = "none"  # no cache mark at all

FEATURE = "agents.prompt_cache"
ONE_SHOT_MARKS_KEY = "one_shot_marks"
POLICY_WHEN_READ_EXPECTED = "when_read_expected"
POLICY_NEVER = "never"
POLICY_PREFIX = "prefix"
POLICY_ALWAYS = "always"
POLICIES = (POLICY_WHEN_READ_EXPECTED, POLICY_NEVER, POLICY_PREFIX, POLICY_ALWAYS)
#: KNOB MIRROR of platform.feature_knob "agents.prompt_cache" "one_shot_marks"
ONE_SHOT_MARKS_MIRROR = POLICY_WHEN_READ_EXPECTED

_ONE_SHOT: ContextVar[bool] = ContextVar("matrx_ai_one_shot_call", default=False)

_reader: Callable[[str], Any] | None = None
_announced = False
_failed = False

_MAX_TRACKED = 2048
_RECENT_PREFIX: OrderedDict[str, float] = OrderedDict()


@dataclass(frozen=True)
class CachePlan:
    marks: str
    reason: str


@contextmanager
def one_shot_call() -> Generator[None]:
    """Declare every send inside this scope a one-shot call: nothing will read its history."""
    token = _ONE_SHOT.set(True)
    try:
        yield
    finally:
        _ONE_SHOT.reset(token)


def is_one_shot_call() -> bool:
    return _ONE_SHOT.get()


def configure_prompt_cache_knobs(reader: Callable[[str], Any] | None) -> None:
    """Bind the host's reader (``key -> value`` for feature ``agents.prompt_cache``).
    ``None`` unbinds it, restoring the standalone posture."""
    global _reader, _announced, _failed
    _reader = reader
    _announced = False
    _failed = False


def one_shot_marks_policy() -> str:
    """The live ``agents.prompt_cache.one_shot_marks`` value, or the announced mirror."""
    global _announced, _failed
    if _reader is None:
        if not _announced:
            _announced = True
            print(
                f"[matrx_ai] no host knob reader bound for {FEATURE!r}; using the mirrored "
                f"{ONE_SHOT_MARKS_KEY}={ONE_SHOT_MARKS_MIRROR!r} (bind one with "
                "configure_prompt_cache_knobs())",
                file=sys.stderr,
            )
        return ONE_SHOT_MARKS_MIRROR
    try:
        raw = _reader(ONE_SHOT_MARKS_KEY)
    except Exception as exc:  # noqa: BLE001 — announced, never a crashed send
        if not _failed:
            _failed = True
            print(
                f"[matrx_ai] host knob reader failed for {FEATURE!r}.{ONE_SHOT_MARKS_KEY!r}: "
                f"{exc!r}; using the mirrored {ONE_SHOT_MARKS_MIRROR!r}",
                file=sys.stderr,
            )
        return ONE_SHOT_MARKS_MIRROR
    value = str(raw).strip().strip('"') if raw is not None else ""
    return value if value in POLICIES else ONE_SHOT_MARKS_MIRROR


def _declares_tools(config: Any) -> bool:
    return bool(getattr(config, "tools", None) or getattr(config, "custom_tools", None))


def _prefix_digest(config: Any) -> str:
    system = getattr(config, "resolved_system_instruction", None)
    if system is None:
        system = getattr(config, "system_instruction", None)
    tools = getattr(config, "tools", None) or []
    raw = f"{getattr(config, 'model', '')}\x00{system!s}\x00{tools!r}"
    return hashlib.sha256(raw.encode("utf-8", "replace")).hexdigest()


def _seen_recently(config: Any, now: float) -> bool:
    """Record this prefix and say whether it was sent within its cache life."""
    digest = _prefix_digest(config)
    last = _RECENT_PREFIX.get(digest)
    _RECENT_PREFIX[digest] = now
    _RECENT_PREFIX.move_to_end(digest)
    while len(_RECENT_PREFIX) > _MAX_TRACKED:
        _RECENT_PREFIX.popitem(last=False)
    # "Recent" = the provider's default cache life (a provider fact, cache_marks.py).
    from matrx_ai.config.cache_marks import ANTHROPIC_CACHE_TIER_SECS

    return last is not None and now - last <= ANTHROPIC_CACHE_TIER_SECS["5m"]


def decide_cache_plan(config: Any, *, now: float | None = None) -> CachePlan:
    """The marks this send writes and why (module docstring)."""
    if not is_one_shot_call():
        return CachePlan(MARKS_ALL, "conversation")
    if _declares_tools(config):
        return CachePlan(MARKS_ALL, "tool_loop")
    repeated = _seen_recently(config, time.time() if now is None else now)
    policy = one_shot_marks_policy()
    if policy == POLICY_ALWAYS:
        return CachePlan(MARKS_ALL, "knob_always")
    if policy == POLICY_NEVER:
        return CachePlan(MARKS_NONE, "knob_never")
    if policy == POLICY_PREFIX:
        return CachePlan(MARKS_PREFIX, "knob_prefix")
    if getattr(config, "extended_prompt_cache", False):
        return CachePlan(MARKS_PREFIX, "long_cache")
    if repeated:
        return CachePlan(MARKS_PREFIX, "repeated_prefix")
    return CachePlan(MARKS_NONE, "one_shot")


def marks_for(config: Any) -> str:
    """What a translator places: the boundary's plan, or every mark when no plan was set."""
    value = getattr(config, "prompt_cache_marks", None)
    return value if value in (MARKS_ALL, MARKS_PREFIX, MARKS_NONE) else MARKS_ALL


def reset_for_tests() -> None:
    _RECENT_PREFIX.clear()
    configure_prompt_cache_knobs(None)


__all__ = [
    "FEATURE",
    "MARKS_ALL",
    "MARKS_NONE",
    "MARKS_PREFIX",
    "ONE_SHOT_MARKS_KEY",
    "ONE_SHOT_MARKS_MIRROR",
    "POLICIES",
    "CachePlan",
    "configure_prompt_cache_knobs",
    "decide_cache_plan",
    "is_one_shot_call",
    "marks_for",
    "one_shot_call",
    "one_shot_marks_policy",
]
