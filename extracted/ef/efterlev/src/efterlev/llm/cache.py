"""LLM response cache (v0.1.147 / #352).

Opt-in cache that wraps any `LLMClient` to skip the network on prompt-hash
hits. First run pays full API cost; subsequent runs on the same workspace
(same evidence, same KSIs, same prompts) replay from disk for free.

Designed for **repeated test runs against the same workspace**, where the
underlying evidence (scan results) doesn't change between iterations and
the agents re-issue identical prompts. Not designed for production —
caching real customer pipeline runs would mask drift in scanner output
and produce stale classifications.

Opt in via the `EFTERLEV_LLM_CACHE` env var:

    EFTERLEV_LLM_CACHE=on      # read + write
    EFTERLEV_LLM_CACHE=off     # default; no caching
    EFTERLEV_LLM_CACHE=record  # write-only (populate cache, never read)
    EFTERLEV_LLM_CACHE=replay  # read-only (fail rather than call API)

Cache location: `<workspace>/.efterlev/llm-cache/`. Sharded by hash prefix
(`ab/cd/<hash>.json`) the same way the provenance blob store is. Already
gitignored under the existing `.efterlev/*` rule.

Cache entries record the full LLMResponse plus the call metadata (system
prompt hash, model, max_tokens) so a future cache-invalidation feature can
filter by any of those.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from efterlev.llm.base import LLMClient, LLMMessage, LLMResponse

# Per-run anti-injection nonce embedded in evidence fences by
# `efterlev.agents.base.format_evidence_for_prompt`. Shape:
# `<evidence_<8hex> id="sha256:...">` and `</evidence_<8hex>>`. Each
# agent.run() generates a fresh nonce via `new_fence_nonce()`, which
# means two otherwise-identical runs produce different prompt text
# even when the evidence and indicators are the same. Caching keyed
# on the raw prompt would miss on every retry — the whole reason
# someone enables the cache (cost reduction across iterations) gets
# defeated. v0.1.148 / #353: normalize the nonce to a fixed token
# before hashing so identical-modulo-nonce prompts share a cache
# entry. The validator that reads the cached response uses the LIVE
# nonce from the prompt, not the original — and the response cites
# evidence_id sha256 hashes (which are nonce-independent) — so this
# is safe.
_EVIDENCE_FENCE_NONCE_PATTERN = re.compile(r"evidence_[0-9a-f]{8}")


def _normalize_for_cache(text: str) -> str:
    """Replace per-run nonces in fence tags with a fixed token so the
    cache key is stable across runs. See `_EVIDENCE_FENCE_NONCE_PATTERN`
    docstring for why."""
    return _EVIDENCE_FENCE_NONCE_PATTERN.sub("evidence_NONCE", text)


def _hash(*parts: str | int) -> str:
    h = hashlib.sha256()
    for p in parts:
        h.update(str(p).encode("utf-8"))
        h.update(b"\x00")  # separator so "ab" + "c" doesn't collide with "a" + "bc"
    return h.hexdigest()


def _cache_key(*, system: str, messages: list[LLMMessage], model: str, max_tokens: int) -> str:
    """Stable hash over the full call shape — system, messages, model, max_tokens.

    v0.1.148 / #353: nonce-normalize the prompt before hashing so the
    cache key is stable across runs even though `format_evidence_for_prompt`
    generates a fresh nonce per agent run. Without this normalization the
    cache always missed because the user message text changed between
    runs (different `<evidence_<8hex>>` fences).

    `max_tokens` is included because Anthropic streams differently at
    different ceilings; cache hit on one shouldn't replay output that
    would have been truncated at another.
    """
    return _hash(
        model,
        max_tokens,
        _normalize_for_cache(system),
        *(_normalize_for_cache(m.content) for m in messages),
    )


def _shard_path(digest: str) -> Path:
    return Path(digest[:2]) / digest[2:4] / f"{digest}.json"


@dataclass
class _CacheMode:
    read: bool
    write: bool

    @classmethod
    def from_env(cls, value: str | None) -> _CacheMode | None:
        if value is None or value.lower() in ("", "off", "0", "false"):
            return None
        v = value.lower()
        if v in ("on", "1", "true", "yes"):
            return cls(read=True, write=True)
        if v == "record":
            return cls(read=False, write=True)
        if v == "replay":
            return cls(read=True, write=False)
        # Unknown value: treat as off rather than raising — agent code paths
        # shouldn't blow up on a typo'd env var.
        return None


@dataclass
class CachingLLMClient:
    """Wraps an underlying `LLMClient` with a prompt-hash → response cache.

    Stub behaviors (`StubLLMClient` in tests) work fine wrapped, but there
    is no point caching test stubs — only wrap real backends.

    Cache directory is created lazily on first write so install-time setup
    doesn't need to know about it.
    """

    inner: LLMClient
    cache_dir: Path
    mode: _CacheMode
    # Counters for the run summary; instrumented agents can read these.
    hits: int = 0
    misses: int = 0

    def complete(
        self,
        *,
        system: str,
        messages: list[LLMMessage],
        model: str,
        max_tokens: int = 4096,
        on_chunk: Callable[[str], None] | None = None,
    ) -> LLMResponse:
        key = _cache_key(system=system, messages=messages, model=model, max_tokens=max_tokens)
        path = self.cache_dir / _shard_path(key)

        if self.mode.read and path.is_file():
            try:
                blob = json.loads(path.read_text(encoding="utf-8"))
                response = LLMResponse(
                    text=blob["response"]["text"],
                    model=blob["response"]["model"],
                    prompt_hash=blob["response"]["prompt_hash"],
                    input_tokens=blob["response"].get("input_tokens", 0),
                    output_tokens=blob["response"].get("output_tokens", 0),
                )
            except (OSError, json.JSONDecodeError, KeyError, TypeError):
                # Treat a corrupt cache entry as a miss — fall through to
                # the underlying call. We don't delete the bad file
                # automatically; a stale or malformed entry is rare and
                # the user can `rm -rf .efterlev/llm-cache/` if needed.
                pass
            else:
                self.hits += 1
                # Mimic streaming so progress reporters that depend on
                # on_chunk firing don't go silent on cache hits.
                if on_chunk is not None and response.text:
                    on_chunk(response.text)
                return response

        # Cache miss — call the real backend.
        if self.mode == _CacheMode(read=True, write=False):
            raise RuntimeError(
                "EFTERLEV_LLM_CACHE=replay set but no cache entry found for this prompt "
                "(hash prefix " + key[:12] + "). Run once with EFTERLEV_LLM_CACHE=on or "
                "record to populate the cache."
            )
        self.misses += 1
        response = self.inner.complete(
            system=system,
            messages=messages,
            model=model,
            max_tokens=max_tokens,
            on_chunk=on_chunk,
        )

        if self.mode.write:
            self._write(path, key, system, messages, model, max_tokens, response)

        return response

    def _write(
        self,
        path: Path,
        key: str,
        system: str,
        messages: list[LLMMessage],
        model: str,
        max_tokens: int,
        response: LLMResponse,
    ) -> None:
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            entry: dict[str, Any] = {
                "version": 1,
                "cached_at": datetime.now(UTC).isoformat(),
                "key": key,
                "request": {
                    "model": model,
                    "max_tokens": max_tokens,
                    "system_sha256": _hash(system),
                    "messages_sha256": _hash(*(m.content for m in messages)),
                },
                "response": {
                    "text": response.text,
                    "model": response.model,
                    "prompt_hash": response.prompt_hash,
                    "input_tokens": response.input_tokens,
                    "output_tokens": response.output_tokens,
                },
            }
            tmp = path.with_suffix(".json.tmp")
            tmp.write_text(json.dumps(entry, indent=2), encoding="utf-8")
            tmp.rename(path)
        except OSError:
            # Cache failures must never break a real LLM call.
            pass


def maybe_wrap_with_cache(
    inner: LLMClient,
    *,
    workspace_root: Path,
    default_mode: str | None = None,
) -> LLMClient:
    """Return `inner` wrapped with `CachingLLMClient` when a cache mode
    resolves; return `inner` unchanged when the resolved mode is "off".

    Resolution precedence (v0.1.151 / #356):
      1. `EFTERLEV_LLM_CACHE` env var if set — wins, lets users override
         workspace config per-shell-session.
      2. `default_mode` arg (from `Config.cache.mode` at call site) —
         the workspace's persisted choice.
      3. None given → fall through to "off" (legacy v0.1.147 behavior
         for callers that don't know about cache config).

    Centralized here so factory + any future per-agent wiring use the
    same precedence.
    """
    env_value = os.environ.get("EFTERLEV_LLM_CACHE")
    resolved = env_value if env_value is not None else default_mode
    if resolved is None:
        return inner
    mode = _CacheMode.from_env(resolved)
    if mode is None:
        return inner
    cache_dir = workspace_root / ".efterlev" / "llm-cache"
    return CachingLLMClient(inner=inner, cache_dir=cache_dir, mode=mode)
