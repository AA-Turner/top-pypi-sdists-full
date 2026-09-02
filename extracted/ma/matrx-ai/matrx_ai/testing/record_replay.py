"""Record / replay wrapper around ``execute_ai_request`` for deterministic LLM tests.

Why this exists
---------------
CI can't hit real LLM providers on every run (cost, flakiness, rate limits,
secret management). The workflow test harness needs the *graph* to execute
for real — scheduler, channels, checkpointer, actions, tool dispatch — but
with the LLM calls replaying a previously captured response.

Design
------
The seam is ``matrx_ai.orchestrator.executor.execute_ai_request`` — every
matrx-graph LLM action funnels through it, so a single monkeypatch covers
``ai.llm.chat``, ``ai.agent.start``, ``ai.conversation.continue`` and
``ai.chat`` at once.

Call-shape stability: ``normalize_completed()`` in ``matrx_ai.graph_nodes.shared``
reads CompletedRequest with defensive ``getattr`` for every field. That means
replay doesn't need a perfect CompletedRequest — it needs an object that
*quacks* like one on the specific attributes the normalizer reads. We use a
``_ReplayStub`` that exposes exactly those attributes.

Three modes
-----------
- ``record`` — always hit the real provider, write ``<key>.json`` next to
  where replays would live. Overwrites on match.
- ``replay`` — never hit the network; load ``<key>.json``. Raises ``ReplayMiss``
  if the recording doesn't exist.
- ``auto`` — replay if file exists, record if it doesn't. Useful for
  "run the test once, commit the fixture, CI replays forever after."

Programmatic stubs
------------------
For tests that want synthetic responses without files, ``stub_response(...)``
registers a (model, prompt-substring) → response matcher consulted BEFORE
record/replay. Match wins → stub is returned. Perfect for unit tests where
you don't care what the LLM would actually say, only that the node passed
*some* text downstream.

Keying
------
SHA256 over (model, messages, system_instruction, temperature, max_tokens,
tools) gives a 16-char hex key. Stable across runs, changes if the prompt
changes — which is the right cache-bust behavior for tests.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from matrx_ai.config import UnifiedConfig


class ReplayMiss(LookupError):
    """Raised in replay mode when no recording matches the request."""


# ---------------------------------------------------------------------------
# Stub objects that quack like CompletedRequest to the defensive normalizer
# ---------------------------------------------------------------------------


@dataclass
class _ResponseStub:
    finish_reason: str | None = None
    text: str = ""
    content: Any = None
    message: Any = None


@dataclass
class _ConfigStub:
    messages: list = field(default_factory=list)


@dataclass
class _RequestStub:
    conversation_id: str = ""
    request_id: str = ""
    config: _ConfigStub = field(default_factory=_ConfigStub)


@dataclass
class _UsageStub:
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    cost_usd: float = 0.0

    @property
    def totals(self):
        return self


@dataclass
class _CompletedStub:
    iterations: int = 1
    final_response: _ResponseStub = field(default_factory=_ResponseStub)
    request: _RequestStub = field(default_factory=_RequestStub)
    total_usage: _UsageStub = field(default_factory=_UsageStub)
    timing_stats: dict = field(default_factory=dict)
    tool_call_stats: dict = field(default_factory=dict)
    metadata: dict = field(default_factory=dict)


def _stub_from_dict(data: dict) -> _CompletedStub:
    """Rehydrate a recording dict into a _CompletedStub.

    Only the fields normalize_completed reads are populated; everything
    else returns zero/empty defaults.
    """
    final_text = data.get("final_text", "")
    messages = data.get("messages") or []

    final_response = _ResponseStub(
        finish_reason=data.get("finish_reason"),
        text=final_text,
        content=final_text,
    )
    if final_text:
        final_response.message = {
            "role": "assistant",
            "content": final_text,
        }

    return _CompletedStub(
        iterations=int(data.get("iterations", 1) or 1),
        final_response=final_response,
        request=_RequestStub(
            conversation_id=data.get("conversation_id", ""),
            request_id=data.get("request_id", ""),
            config=_ConfigStub(messages=messages),
        ),
        total_usage=_UsageStub(
            input_tokens=int(data.get("input_tokens", 0) or 0),
            output_tokens=int(data.get("output_tokens", 0) or 0),
            total_tokens=int(data.get("total_tokens", 0) or 0),
            cost_usd=float(data.get("cost_usd", 0.0) or 0.0),
        ),
        timing_stats={"total_duration_ms": int(data.get("duration_ms", 0) or 0)},
        tool_call_stats={"total_calls": int(data.get("tool_calls_made", 0) or 0)},
        metadata=dict(data.get("metadata") or {}),
    )


# ---------------------------------------------------------------------------
# Keying
# ---------------------------------------------------------------------------


def _messages_to_json(messages: Any) -> list[dict]:
    """Normalize any messages representation into a stable JSON list."""
    if messages is None:
        return []
    if hasattr(messages, "to_dict_list"):
        try:
            return messages.to_dict_list()
        except Exception:
            pass
    if hasattr(messages, "to_list"):
        try:
            raw = messages.to_list()
            return [_message_to_json(m) for m in raw]
        except Exception:
            pass
    if isinstance(messages, list):
        return [_message_to_json(m) for m in messages]
    return []


def _message_to_json(m: Any) -> dict:
    if isinstance(m, dict):
        return m
    for attr in ("to_dict", "model_dump", "dict"):
        method = getattr(m, attr, None)
        if callable(method):
            try:
                dumped = method()
                if isinstance(dumped, dict):
                    return dumped
            except Exception:
                pass
    return {
        "role": getattr(m, "role", "unknown"),
        "content": str(getattr(m, "content", "")),
    }


def _make_key(config: UnifiedConfig) -> str:
    payload = {
        "model": getattr(config, "model", None),
        "messages": _messages_to_json(getattr(config, "messages", None)),
        "system_instruction": getattr(config, "system_instruction", None),
        "temperature": getattr(config, "temperature", None),
        "max_tokens": getattr(config, "max_tokens", None),
        "tools": [
            t if isinstance(t, str) else getattr(t, "name", str(t))
            for t in (getattr(config, "tools", None) or [])
        ],
    }
    serialized = json.dumps(payload, sort_keys=True, default=str)
    return hashlib.sha256(serialized.encode()).hexdigest()[:16]


# ---------------------------------------------------------------------------
# Programmatic stubs
# ---------------------------------------------------------------------------


@dataclass
class _Stub:
    model_match: str | None
    prompt_contains: str | None
    response: str
    metadata: dict = field(default_factory=dict)


_STUBS: list[_Stub] = []


def stub_response(
    *,
    response: str,
    model: str | None = None,
    prompt_contains: str | None = None,
    metadata: dict | None = None,
) -> None:
    """Register a synthetic response matched against later requests.

    Match is ANDed: ``model`` must equal ``config.model`` (substring match
    allowed), and any user message in ``config.messages`` must contain
    ``prompt_contains``. Pass ``None`` to any to mean "any".

    Stubs are consulted BEFORE record/replay — so tests that don't care
    about a recording can drop in a stub inline.
    """
    _STUBS.append(
        _Stub(
            model_match=model,
            prompt_contains=prompt_contains,
            response=response,
            metadata=metadata or {},
        )
    )


def clear_stubs() -> None:
    """Drop every registered stub. Call in pytest fixture teardown."""
    _STUBS.clear()


def _match_stub(config: UnifiedConfig) -> _Stub | None:
    if not _STUBS:
        return None
    model = getattr(config, "model", "") or ""
    messages = _messages_to_json(getattr(config, "messages", None))
    prompts: list[str] = []
    for m in messages:
        content = m.get("content")
        if isinstance(content, str):
            prompts.append(content)
        elif isinstance(content, list):
            for c in content:
                if isinstance(c, dict):
                    text = c.get("text") or c.get("content")
                    if isinstance(text, str):
                        prompts.append(text)
                elif isinstance(c, str):
                    prompts.append(c)
    combined = "\n".join(prompts)

    for stub in _STUBS:
        if stub.model_match and stub.model_match not in model:
            continue
        if stub.prompt_contains and stub.prompt_contains not in combined:
            continue
        return stub
    return None


def _stub_to_completed(stub: _Stub, config: UnifiedConfig) -> _CompletedStub:
    original = _messages_to_json(getattr(config, "messages", None))
    full_messages = [*original, {"role": "assistant", "content": stub.response}]
    return _stub_from_dict(
        {
            "final_text": stub.response,
            "messages": full_messages,
            "iterations": 1,
            "metadata": {"source": "record_replay_stub", **stub.metadata},
        }
    )


# ---------------------------------------------------------------------------
# The executor
# ---------------------------------------------------------------------------


class RecordReplayExecutor:
    """Drop-in replacement for ``execute_ai_request``.

    Install with :func:`install_record_replay` or call directly in tests.
    Stubs always win; otherwise record/replay based on ``mode``.
    """

    def __init__(self, recordings_dir: str | Path, mode: str = "auto"):
        if mode not in ("record", "replay", "auto"):
            raise ValueError(
                f"mode must be 'record', 'replay', or 'auto'; got {mode!r}"
            )
        self.recordings_dir = Path(recordings_dir)
        self.recordings_dir.mkdir(parents=True, exist_ok=True)
        self.mode = mode

    def _path(self, key: str) -> Path:
        return self.recordings_dir / f"{key}.json"

    async def __call__(
        self,
        config: UnifiedConfig,
        max_iterations: int = 100,
        max_retries_per_iteration: int = 2,
        metadata: dict[str, Any] | None = None,
    ) -> Any:
        stub = _match_stub(config)
        if stub is not None:
            return _stub_to_completed(stub, config)

        key = _make_key(config)
        path = self._path(key)

        if self.mode == "replay" or (self.mode == "auto" and path.exists()):
            if not path.exists():
                raise ReplayMiss(
                    f"No recording for key {key} (model={getattr(config, 'model', '?')}). "
                    f"Run with mode='record' or 'auto' to capture it."
                )
            with path.open() as f:
                data = json.load(f)
            return _stub_from_dict(data)

        from matrx_ai.orchestrator.executor import execute_ai_request

        result = await execute_ai_request(
            config, max_iterations, max_retries_per_iteration, metadata
        )
        self._persist(path, result, config)
        return result

    @staticmethod
    def _persist(path: Path, result: Any, config: UnifiedConfig) -> None:
        from matrx_ai.graph_nodes.shared import normalize_completed

        snapshot = normalize_completed(result)
        data = snapshot.model_dump(mode="json")
        data["_key_inputs"] = {
            "model": getattr(config, "model", None),
            "system_instruction": getattr(config, "system_instruction", None),
        }
        with path.open("w") as f:
            json.dump(data, f, indent=2, default=str)


# ---------------------------------------------------------------------------
# Install / uninstall
# ---------------------------------------------------------------------------


def install_record_replay(
    recordings_dir: str | Path,
    mode: str = "auto",
) -> Callable[[], None]:
    """Monkeypatch ``execute_ai_request`` globally with a RecordReplayExecutor.

    Returns an uninstaller — call it in pytest fixture teardown. Safe to call
    multiple times; each install stacks an uninstaller and the returned one
    only reverses the most recent install.
    """
    from matrx_ai.orchestrator import executor as _executor_mod

    original = _executor_mod.execute_ai_request
    replacement = RecordReplayExecutor(recordings_dir, mode)
    _executor_mod.execute_ai_request = replacement  # type: ignore[assignment]

    def _uninstall() -> None:
        _executor_mod.execute_ai_request = original  # type: ignore[assignment]

    return _uninstall
