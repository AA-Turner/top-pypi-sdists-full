"""Tests for `efterlev.llm.openai_client.OpenAIClient`.

Mirrors `tests/test_anthropic_client.py` shape; mocks the openai SDK so
the tests don't need the optional dep installed. Covers:
- happy-path stream → LLMResponse with usage + served model
- truncation (`finish_reason="length"`) → AgentError
- retry on transient errors (RateLimitError etc.)
- non-retryable errors (AuthenticationError) bypass the retry loop
- fallback model used after primary exhausted
"""

from __future__ import annotations

import sys
import types
from typing import Any

import pytest

from efterlev.errors import AgentError
from efterlev.llm.base import LLMMessage
from efterlev.llm.openai_client import OpenAIClient

# --- fake openai SDK module --------------------------------------------------
# Installed into sys.modules so `import openai` in the client module resolves
# to this stub. Avoids requiring the real SDK in the test environment.


class _RateLimitError(Exception):
    pass


class _APITimeoutError(Exception):
    pass


class _APIConnectionError(Exception):
    pass


class _InternalServerError(Exception):
    pass


class _AuthenticationError(Exception):
    pass


def _install_fake_openai(call_side_effect: Any) -> types.ModuleType:
    """Install a stub `openai` module; `call_side_effect` is what
    `client.chat.completions.create(...)` returns (or raises)."""
    fake = types.ModuleType("openai")
    fake.RateLimitError = _RateLimitError
    fake.APITimeoutError = _APITimeoutError
    fake.APIConnectionError = _APIConnectionError
    fake.InternalServerError = _InternalServerError
    fake.AuthenticationError = _AuthenticationError

    class _Completions:
        def __init__(self, side_effect: Any) -> None:
            self._side_effect = side_effect
            self.calls: list[dict[str, Any]] = []

        def create(self, **kwargs: Any) -> Any:
            self.calls.append(kwargs)
            if callable(self._side_effect):
                return self._side_effect(kwargs, len(self.calls))
            if isinstance(self._side_effect, BaseException):
                raise self._side_effect
            return self._side_effect

    class _Chat:
        def __init__(self, side_effect: Any) -> None:
            self.completions = _Completions(side_effect)

    class _OpenAI:
        def __init__(self, *_args: Any, **_kwargs: Any) -> None:
            self.chat = _Chat(call_side_effect)

    fake.OpenAI = _OpenAI
    sys.modules["openai"] = fake
    return fake


@pytest.fixture(autouse=True)
def _restore_sys_modules() -> Any:
    """Each test starts with a fresh fake; tear down so other suites aren't
    affected by the stub."""
    saved = sys.modules.get("openai")
    yield
    if saved is None:
        sys.modules.pop("openai", None)
    else:
        sys.modules["openai"] = saved


def _chunk(
    content: str | None = None,
    finish_reason: str | None = None,
    model: str | None = None,
    usage: Any = None,
) -> Any:
    """Build a chunk-shaped object the client's stream loop walks."""
    delta = types.SimpleNamespace(content=content)
    choice = types.SimpleNamespace(delta=delta, finish_reason=finish_reason)
    return types.SimpleNamespace(
        choices=[choice] if (content is not None or finish_reason is not None) else [],
        model=model,
        usage=usage,
    )


def _ok_stream(
    text: str = "ok", *, model: str = "gpt-5.4", input_tok: int = 10, output_tok: int = 3
) -> list[Any]:
    return [
        _chunk(content=text, model=model),
        _chunk(finish_reason="stop", model=model),
        _chunk(usage=types.SimpleNamespace(prompt_tokens=input_tok, completion_tokens=output_tok)),
    ]


def test_happy_path_returns_text_and_usage() -> None:
    _install_fake_openai(_ok_stream("hello world", input_tok=42, output_tok=2))
    client = OpenAIClient(api_key="sk-test")
    resp = client.complete(
        system="be helpful", messages=[LLMMessage(content="hi")], model="gpt-5.4"
    )
    assert resp.text == "hello world"
    assert resp.model == "gpt-5.4"
    assert resp.input_tokens == 42
    assert resp.output_tokens == 2
    assert len(resp.prompt_hash) == 64  # sha256 hex


def test_on_chunk_receives_cumulative_text() -> None:
    _install_fake_openai(
        [
            _chunk(content="hel"),
            _chunk(content="lo"),
            _chunk(finish_reason="stop"),
            _chunk(usage=types.SimpleNamespace(prompt_tokens=1, completion_tokens=1)),
        ]
    )
    seen: list[str] = []
    client = OpenAIClient(api_key="sk-test")
    client.complete(
        system="s",
        messages=[LLMMessage(content="m")],
        model="gpt-5.4",
        on_chunk=seen.append,
    )
    assert seen == ["hel", "hello"]


def test_truncation_raises_agent_error() -> None:
    _install_fake_openai(
        [
            _chunk(content="incomplete json {"),
            _chunk(finish_reason="length"),  # truncated at max_completion_tokens
        ]
    )
    client = OpenAIClient(api_key="sk-test")
    with pytest.raises(AgentError, match="truncated at max_completion_tokens"):
        client.complete(
            system="s",
            messages=[LLMMessage(content="m")],
            model="gpt-5.4",
            max_tokens=10,
        )


def test_empty_response_raises_agent_error() -> None:
    _install_fake_openai(
        [
            _chunk(finish_reason="stop"),  # no content
        ]
    )
    client = OpenAIClient(api_key="sk-test")
    with pytest.raises(AgentError, match="no text content"):
        client.complete(system="s", messages=[LLMMessage(content="m")], model="gpt-5.4")


def test_retry_on_transient_then_success() -> None:
    calls: list[int] = []
    ok = _ok_stream("recovered")

    def side(_kwargs: dict[str, Any], n: int) -> Any:
        calls.append(n)
        if n < 3:
            raise _RateLimitError("rate limited")
        return ok

    _install_fake_openai(side)
    client = OpenAIClient(api_key="sk-test", sleeper=lambda _s: None)
    resp = client.complete(system="s", messages=[LLMMessage(content="m")], model="gpt-5.4")
    assert resp.text == "recovered"
    assert calls == [1, 2, 3]


def test_non_retryable_error_bypasses_retry_loop() -> None:
    calls: list[int] = []

    def side(_kwargs: dict[str, Any], n: int) -> Any:
        calls.append(n)
        raise _AuthenticationError("bad key")

    _install_fake_openai(side)
    client = OpenAIClient(api_key="sk-test", sleeper=lambda _s: None)
    with pytest.raises(AgentError, match="openai completion failed"):
        client.complete(system="s", messages=[LLMMessage(content="m")], model="gpt-5.4")
    assert calls == [1]  # no retry on auth error


def test_fallback_model_used_when_primary_exhausted() -> None:
    seen_models: list[str] = []

    def side(kwargs: dict[str, Any], _n: int) -> Any:
        seen_models.append(kwargs["model"])
        if kwargs["model"] == "gpt-5.4":
            raise _RateLimitError("primary out")
        return _ok_stream("from fallback", model="gpt-5-mini")

    _install_fake_openai(side)
    client = OpenAIClient(
        api_key="sk-test",
        fallback_model="gpt-5-mini",
        sleeper=lambda _s: None,
    )
    resp = client.complete(system="s", messages=[LLMMessage(content="m")], model="gpt-5.4")
    assert resp.text == "from fallback"
    assert resp.model == "gpt-5-mini"
    # 3 attempts on primary + 1 on fallback
    assert seen_models == ["gpt-5.4", "gpt-5.4", "gpt-5.4", "gpt-5-mini"]


def test_no_api_key_raises_friendly_error(monkeypatch: pytest.MonkeyPatch) -> None:
    _install_fake_openai(_ok_stream())
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    client = OpenAIClient(api_key=None)
    with pytest.raises(AgentError, match="OPENAI_API_KEY is not set"):
        client.complete(system="s", messages=[LLMMessage(content="m")], model="gpt-5.4")
