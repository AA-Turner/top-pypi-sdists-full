"""Tests for `efterlev.llm.cache` — opt-in LLM response cache.

The cache is the v0.1.147 / #352 cost-reduction feature: identical
prompts on subsequent runs replay from disk instead of hitting the
real API. First run pays; later runs are free for the cached scope.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

import pytest

from efterlev.llm.base import LLMMessage, LLMResponse
from efterlev.llm.cache import (
    CachingLLMClient,
    _cache_key,
    _CacheMode,
    maybe_wrap_with_cache,
)


@dataclass
class _CountingClient:
    """Stub backend that returns a canned response and counts calls."""

    response_text: str = '{"ok": true}'
    model: str = "stub-model"
    call_count: int = 0

    def complete(
        self,
        *,
        system: str,
        messages: list[LLMMessage],
        model: str,
        max_tokens: int = 4096,
        on_chunk: Callable[[str], None] | None = None,
    ) -> LLMResponse:
        self.call_count += 1
        return LLMResponse(
            text=self.response_text,
            model=self.model,
            prompt_hash="stub-prompt-hash",
            input_tokens=10,
            output_tokens=20,
        )


def _make_cache(tmp_path: Path, mode: _CacheMode) -> tuple[_CountingClient, CachingLLMClient]:
    backend = _CountingClient()
    cache = CachingLLMClient(inner=backend, cache_dir=tmp_path / "llm-cache", mode=mode)
    return backend, cache


def test_cache_miss_then_hit_same_prompt(tmp_path: Path) -> None:
    """First call pays (miss), second call with identical prompt replays
    from cache (hit). The backend is only invoked once."""
    backend, cache = _make_cache(tmp_path, _CacheMode(read=True, write=True))
    msg = [LLMMessage(content="classify this evidence")]
    r1 = cache.complete(system="be helpful", messages=msg, model="claude-haiku-4-5")
    r2 = cache.complete(system="be helpful", messages=msg, model="claude-haiku-4-5")
    assert backend.call_count == 1
    assert cache.hits == 1
    assert cache.misses == 1
    assert r1.text == r2.text


def test_cache_normalizes_evidence_fence_nonces(tmp_path: Path) -> None:
    """v0.1.148 / #353: per-run nonces in `<evidence_<8hex>>` fences must
    NOT bust the cache. Customer enabled EFTERLEV_LLM_CACHE=on and
    every `/report` re-run still paid full LLM cost — root cause was
    that the gap agent generates a fresh nonce each run, so the user
    message text differs even when the underlying evidence is identical.
    """
    backend, cache = _make_cache(tmp_path, _CacheMode(read=True, write=True))
    # Same evidence content, different per-run nonces.
    msg1 = [
        LLMMessage(content='look at <evidence_abc12345 id="sha256:xyz">data</evidence_abc12345>')
    ]
    msg2 = [
        LLMMessage(content='look at <evidence_deadbeef id="sha256:xyz">data</evidence_deadbeef>')
    ]
    cache.complete(system="s", messages=msg1, model="m")
    cache.complete(system="s", messages=msg2, model="m")
    # Second call should hit cache despite the different nonce — both
    # prompts describe the same evidence record.
    assert backend.call_count == 1
    assert cache.hits == 1


def test_cache_busts_on_any_input_change(tmp_path: Path) -> None:
    """Cache key includes system, messages, model, max_tokens. Any change
    misses."""
    backend, cache = _make_cache(tmp_path, _CacheMode(read=True, write=True))
    msg = [LLMMessage(content="m")]
    cache.complete(system="s", messages=msg, model="m1")
    cache.complete(system="s'", messages=msg, model="m1")  # system change
    cache.complete(system="s", messages=[LLMMessage(content="m'")], model="m1")  # msg change
    cache.complete(system="s", messages=msg, model="m2")  # model change
    cache.complete(system="s", messages=msg, model="m1", max_tokens=100)  # max_tokens change
    assert backend.call_count == 5


def test_record_mode_writes_but_never_reads(tmp_path: Path) -> None:
    """`record` mode always calls the backend (no cache reads) and
    populates the cache for later use."""
    backend, cache = _make_cache(tmp_path, _CacheMode(read=False, write=True))
    msg = [LLMMessage(content="x")]
    cache.complete(system="s", messages=msg, model="m")
    cache.complete(system="s", messages=msg, model="m")
    cache.complete(system="s", messages=msg, model="m")
    assert backend.call_count == 3  # No reads, so every call hits backend.
    assert cache.hits == 0
    # Verify the cache file was written.
    cache_files = list((tmp_path / "llm-cache").rglob("*.json"))
    assert len(cache_files) == 1


def test_replay_mode_misses_raise(tmp_path: Path) -> None:
    """`replay` mode (read-only) raises on cache miss rather than calling
    the backend. Useful for tests that should never hit the network."""
    backend, cache = _make_cache(tmp_path, _CacheMode(read=True, write=False))
    msg = [LLMMessage(content="not in cache")]
    with pytest.raises(RuntimeError, match="no cache entry"):
        cache.complete(system="s", messages=msg, model="m")
    assert backend.call_count == 0


def test_replay_mode_hits_dont_raise(tmp_path: Path) -> None:
    """Pre-populated cache should be readable in replay mode."""
    # First, populate the cache with read+write.
    backend1, writer = _make_cache(tmp_path, _CacheMode(read=True, write=True))
    msg = [LLMMessage(content="prep")]
    writer.complete(system="s", messages=msg, model="m")
    # Now switch to replay-only with a separate cache instance.
    backend2 = _CountingClient()
    reader = CachingLLMClient(
        inner=backend2, cache_dir=tmp_path / "llm-cache", mode=_CacheMode(read=True, write=False)
    )
    r = reader.complete(system="s", messages=msg, model="m")
    assert r.text == backend1.response_text
    assert backend2.call_count == 0  # No backend call — pure replay.


def test_corrupt_cache_entry_falls_through_to_backend(tmp_path: Path) -> None:
    """A garbled cache file shouldn't crash the run — treat as a miss
    and call the backend. (Robust to manual edits, partial writes from
    a killed process, etc.)"""
    backend, cache = _make_cache(tmp_path, _CacheMode(read=True, write=True))
    msg = [LLMMessage(content="x")]
    # Pre-write a malformed cache entry at the exact key the call will hash to.
    key = _cache_key(system="s", messages=msg, model="m", max_tokens=4096)
    bad = tmp_path / "llm-cache" / key[:2] / key[2:4] / f"{key}.json"
    bad.parent.mkdir(parents=True, exist_ok=True)
    bad.write_text("not valid json {{{", encoding="utf-8")
    # The call should succeed (backend invoked, miss recorded).
    cache.complete(system="s", messages=msg, model="m")
    assert backend.call_count == 1


def test_on_chunk_fires_on_cache_hit_so_progress_reporters_dont_go_silent(
    tmp_path: Path,
) -> None:
    """A cache hit should still invoke `on_chunk` with the cached text,
    matching the contract real streams provide. Otherwise the gap-agent
    progress reporter would print nothing when replaying from cache."""
    _backend, cache = _make_cache(tmp_path, _CacheMode(read=True, write=True))
    msg = [LLMMessage(content="x")]
    # First call populates.
    cache.complete(system="s", messages=msg, model="m")
    # Second call: cache hit — make sure on_chunk fires.
    received: list[str] = []
    cache.complete(system="s", messages=msg, model="m", on_chunk=received.append)
    assert received == ['{"ok": true}']


# --- env-mode parsing -----------------------------------------------------


def test_cache_mode_from_env_off_returns_none() -> None:
    assert _CacheMode.from_env(None) is None
    assert _CacheMode.from_env("") is None
    assert _CacheMode.from_env("off") is None
    assert _CacheMode.from_env("false") is None
    assert _CacheMode.from_env("0") is None
    # Unknown values also degrade to None rather than raising.
    assert _CacheMode.from_env("yolo") is None


def test_cache_mode_from_env_on() -> None:
    m = _CacheMode.from_env("on")
    assert m is not None
    assert m.read and m.write


def test_cache_mode_from_env_record_and_replay() -> None:
    r = _CacheMode.from_env("record")
    assert r is not None
    assert r.write and not r.read

    p = _CacheMode.from_env("replay")
    assert p is not None
    assert p.read and not p.write


# --- maybe_wrap_with_cache (factory hook) --------------------------------


def test_maybe_wrap_returns_inner_when_env_unset(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv("EFTERLEV_LLM_CACHE", raising=False)
    inner = _CountingClient()
    wrapped = maybe_wrap_with_cache(inner, workspace_root=tmp_path)
    assert wrapped is inner  # Identity check — no wrapping.


def test_maybe_wrap_wraps_when_default_mode_on(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """v0.1.151 / #356: workspace config's `cache.mode = "on"` (the
    default) causes wrapping even without the env var."""
    monkeypatch.delenv("EFTERLEV_LLM_CACHE", raising=False)
    inner = _CountingClient()
    wrapped = maybe_wrap_with_cache(inner, workspace_root=tmp_path, default_mode="on")
    assert wrapped is not inner
    assert isinstance(wrapped, CachingLLMClient)


def test_maybe_wrap_env_var_overrides_default_mode(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """v0.1.151 / #356: env var precedence — env=off should disable
    even when workspace config says on."""
    monkeypatch.setenv("EFTERLEV_LLM_CACHE", "off")
    inner = _CountingClient()
    wrapped = maybe_wrap_with_cache(inner, workspace_root=tmp_path, default_mode="on")
    assert wrapped is inner  # env=off wins; no wrap.


def test_maybe_wrap_returns_inner_when_both_unset(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """No env, no default_mode → no wrap. Preserves legacy v0.1.147
    behavior for callers that don't pass a default_mode."""
    monkeypatch.delenv("EFTERLEV_LLM_CACHE", raising=False)
    inner = _CountingClient()
    wrapped = maybe_wrap_with_cache(inner, workspace_root=tmp_path)
    assert wrapped is inner


def test_maybe_wrap_wraps_when_env_on(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("EFTERLEV_LLM_CACHE", "on")
    inner = _CountingClient()
    wrapped = maybe_wrap_with_cache(inner, workspace_root=tmp_path)
    assert wrapped is not inner
    assert isinstance(wrapped, CachingLLMClient)
    assert wrapped.cache_dir == tmp_path / ".efterlev" / "llm-cache"
