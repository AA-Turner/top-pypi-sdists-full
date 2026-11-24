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
#: LATE TOOLS (``providers/late_tools.py``): tools that join a conversation after its first send ride
#: AFTER the cache line as text, run through the declared gateway, never in the wire ``tools`` list.
LATE_TOOLS_ENABLED_KEY = "late_tools_enabled"
#: KNOB MIRROR of platform.feature_knob "agents.prompt_cache" "late_tools_enabled"
LATE_TOOLS_ENABLED_MIRROR = False
LATE_TOOLS_SCOPE_KEY = "late_tools_scope"
LATE_TOOLS_SCOPE_ENROLLED = "enrolled"  # only agents enrolled in the always-warm prompt cache
LATE_TOOLS_SCOPE_ALL = "all"
LATE_TOOLS_SCOPES = (LATE_TOOLS_SCOPE_ENROLLED, LATE_TOOLS_SCOPE_ALL)
#: KNOB MIRROR of platform.feature_knob "agents.prompt_cache" "late_tools_scope"
LATE_TOOLS_SCOPE_MIRROR = LATE_TOOLS_SCOPE_ENROLLED

_ONE_SHOT: ContextVar[bool] = ContextVar("matrx_ai_one_shot_call", default=False)

_reader: Callable[[str], Any] | None = None
_announced = False
_failed = False
_announced_keys: set[str] = set()
_failed_keys: set[str] = set()

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
    _announced_keys.clear()
    _failed_keys.clear()


def _read_knob(key: str, mirror: Any) -> Any:
    """One ``agents.prompt_cache`` knob through the bound reader, or ``mirror`` — announced once per
    key when no reader is bound or the read fails (a row not seeded yet reads as a failure)."""
    global _announced, _failed
    if _reader is None:
        if key not in _announced_keys:
            _announced_keys.add(key)
            _announced = True
            print(
                f"[matrx_ai] no host knob reader bound for {FEATURE!r}; using the mirrored "
                f"{key}={mirror!r} (bind one with configure_prompt_cache_knobs())",
                file=sys.stderr,
            )
        return mirror
    from matrx_utils.knob_fallback import knob_or_declared_default_sync

    try:
        return knob_or_declared_default_sync(
            lambda: _reader(key), feature=FEATURE, key=key, declared_default=mirror,
            consequence="the mirrored value governs until the row is seeded")
    except Exception as exc:  # noqa: BLE001 — announced, never a crashed send
        if key not in _failed_keys:
            _failed_keys.add(key)
            _failed = True
            print(
                f"[matrx_ai] host knob reader failed for {FEATURE!r}.{key!r}: "
                f"{exc!r}; using the mirrored {mirror!r}",
                file=sys.stderr,
            )
        return mirror


def one_shot_marks_policy() -> str:
    """The live ``agents.prompt_cache.one_shot_marks`` value, or the announced mirror."""
    raw = _read_knob(ONE_SHOT_MARKS_KEY, ONE_SHOT_MARKS_MIRROR)
    value = str(raw).strip().strip('"') if raw is not None else ""
    return value if value in POLICIES else ONE_SHOT_MARKS_MIRROR


def late_tools_enabled() -> bool:
    """The live ``agents.prompt_cache.late_tools_enabled`` value; a missing row is OFF (announced)."""
    raw = _read_knob(LATE_TOOLS_ENABLED_KEY, LATE_TOOLS_ENABLED_MIRROR)
    if isinstance(raw, bool):
        return raw
    return str(raw).strip().strip('"').lower() == "true" if raw is not None else False


def late_tools_scope() -> str:
    """The live ``agents.prompt_cache.late_tools_scope`` value (``enrolled`` | ``all``)."""
    raw = _read_knob(LATE_TOOLS_SCOPE_KEY, LATE_TOOLS_SCOPE_MIRROR)
    value = str(raw).strip().strip('"') if raw is not None else ""
    return value if value in LATE_TOOLS_SCOPES else LATE_TOOLS_SCOPE_MIRROR


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


# ── PREFIX EVIDENCE: what ONE send's cache prefix positively was (a stopped call's estimate) ──────────────
#
# Lead rulings 2026-11-16/17 (made in Arman's absence; he may overrule them), read by
# ``providers/stopped_usage.py``: a stopped call's cached prefix is a READ only when an ACCEPTED send of the
# same provider cache scope was recorded within the cache life before THIS send began; a WRITE only when none
# was AND this send was accepted (its stream started); otherwise UNKNOWN, priced at 1x uncached.
#
# * Scope = exactly the provider's cache scope: vendor + a non-secret fingerprint of the API
#   key the call used + model + prefix (system + tools). Anthropic isolates prompt caches per WORKSPACE on the
#   Claude API (per organization on Bedrock / Google Cloud); an API key belongs to one workspace, so the key
#   fingerprint is that scope or narrower. No fingerprint -> no evidence (unknown).
# * Per send: each dispatch holds its own :class:`PrefixEvidence`; another send never changes it.
# * The shared record (``matrx_utils.cache``, the existing shared tier; key life = the cache life) is written
#   only after the provider ACCEPTED the call. Both store calls run detached: a send never waits on them.

PREFIX_READ = "read"
PREFIX_WRITE = "write"
PREFIX_UNKNOWN = "unknown"
_ABSENT = "absent"  # the store answered: no accepted send of this scope within the cache life
SHARED_PREFIX_KEY = "mx:prompt-cache:accepted:{digest}"


def prefix_scope_digest(config: Any, *, vendor: str, key_fingerprint: str | None) -> str | None:
    """The provider cache scope of ``config``'s prefix, hashed — None without a key fingerprint."""
    if not key_fingerprint:
        return None
    # No stage/environment (cost adversary pass 3): the provider's cache is the key's workspace, so a dev and a
    # prod process on ONE key share it; a stage in the digest made prod read "absent" for a prefix dev warmed and
    # price a warm read as a 1.25x write. Distinct keys already give distinct fingerprints.
    raw = f"{vendor}\x00{key_fingerprint}\x00{_prefix_digest(config)}"
    return hashlib.sha256(raw.encode("utf-8", "replace")).hexdigest()


def _cache_life_ms() -> int:
    from matrx_ai.config.cache_marks import ANTHROPIC_CACHE_TIER_SECS

    return int(ANTHROPIC_CACHE_TIER_SECS["5m"] * 1000)


class PrefixEvidence:
    """One send's prefix evidence. :meth:`begin` asks the store (detached); :meth:`accepted` records."""

    def __init__(self, scope: str | None) -> None:
        self.scope = scope
        self._seen: str | None = None  # PREFIX_READ | _ABSENT once the store answered
        self._accepted = False

    @property
    def state(self) -> str:
        if self._seen == PREFIX_READ:
            return PREFIX_READ
        if self._seen == _ABSENT and self._accepted:
            return PREFIX_WRITE
        return PREFIX_UNKNOWN

    def begin(self) -> None:
        if self.scope is not None:
            _detach(self._ask(), "prompt_cache_prefix_ask")

    def accepted(self) -> None:
        """The provider accepted this call (its stream started or it answered): record the scope."""
        if self._accepted:
            return
        self._accepted = True
        if self.scope is not None:
            _detach(self._record(), "prompt_cache_prefix_record")

    async def _ask(self) -> None:
        try:
            from matrx_utils.cache.backend import current_backend, l2_call

            backend = current_backend()
            if backend is None:
                return
            ok, raw = await l2_call("prompt_cache_prefix_get", backend.get(SHARED_PREFIX_KEY.format(digest=self.scope)))
            if ok:
                self._seen = PREFIX_READ if raw else _ABSENT
        except Exception as exc:  # noqa: BLE001 — stays unknown; announced
            print(f"[matrx_ai] prompt-cache prefix lookup failed: {exc!r}", file=sys.stderr)

    async def _record(self) -> None:
        try:
            from matrx_utils.cache.backend import current_backend, l2_call

            backend = current_backend()
            if backend is None:
                return
            key = SHARED_PREFIX_KEY.format(digest=self.scope)
            await l2_call("prompt_cache_prefix_set", backend.set(key, b"1", _cache_life_ms()))
        except Exception as exc:  # noqa: BLE001 — announced; the next send reads unknown
            print(f"[matrx_ai] prompt-cache prefix record failed: {exc!r}", file=sys.stderr)


def _detach(coro: Any, name: str) -> None:
    try:
        from matrx_utils import detached_task

        detached_task(coro, name=name)
    except Exception as exc:  # noqa: BLE001 — no running loop: no evidence, announced
        coro.close()
        print(f"[matrx_ai] could not schedule {name}: {exc!r}", file=sys.stderr)


def begin_prefix_evidence(config: Any, *, vendor: str, key_fingerprint: str | None) -> PrefixEvidence:
    """Start one send's evidence (never waits on the store)."""
    evidence = PrefixEvidence(prefix_scope_digest(config, vendor=vendor, key_fingerprint=key_fingerprint))
    evidence.begin()
    return evidence


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
    "LATE_TOOLS_ENABLED_KEY",
    "LATE_TOOLS_SCOPE_KEY",
    "CachePlan",
    "configure_prompt_cache_knobs",
    "decide_cache_plan",
    "is_one_shot_call",
    "late_tools_enabled",
    "late_tools_scope",
    "marks_for",
    "one_shot_call",
    "one_shot_marks_policy",
    "PREFIX_READ",
    "PREFIX_UNKNOWN",
    "PREFIX_WRITE",
    "PrefixEvidence",
    "begin_prefix_evidence",
    "prefix_scope_digest",
]
