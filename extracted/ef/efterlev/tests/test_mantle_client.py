"""Tests for `efterlev.llm.mantle_client.BedrockOpenAIClient`.

Mocks the openai SDK's Responses API so the tests don't need the optional
dep or a live Bedrock Mantle endpoint. Covers: base-URL derivation + env
override, happy-path responses.create → LLMResponse with usage, truncation
(status=incomplete / reason=max_output_tokens) → AgentError, missing key →
AgentError, retry on transient errors, on_chunk fires once with final text,
and that the request shape (instructions/input/max_output_tokens) is correct.
"""

from __future__ import annotations

import sys
import types
from typing import Any

import pytest

from efterlev.errors import AgentError
from efterlev.llm.base import LLMMessage
from efterlev.llm.mantle_client import BedrockOpenAIClient, mantle_base_url


class _RateLimitError(Exception):
    pass


class _APITimeoutError(Exception):
    pass


class _APIConnectionError(Exception):
    pass


class _InternalServerError(Exception):
    pass


def _install_fake_openai(create_side_effect: Any) -> Any:
    """Install a stub `openai` module whose `responses.create(...)` returns
    (or raises) `create_side_effect`. Returns the _Responses recorder."""
    fake = types.ModuleType("openai")
    fake.RateLimitError = _RateLimitError
    fake.APITimeoutError = _APITimeoutError
    fake.APIConnectionError = _APIConnectionError
    fake.InternalServerError = _InternalServerError

    class _Responses:
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

    recorder = _Responses(create_side_effect)

    class _OpenAI:
        def __init__(self, *_args: Any, **kwargs: Any) -> None:
            self.responses = recorder
            self.init_kwargs = kwargs

    fake.OpenAI = _OpenAI
    sys.modules["openai"] = fake
    return recorder


@pytest.fixture(autouse=True)
def _restore_sys_modules() -> Any:
    saved = sys.modules.get("openai")
    yield
    if saved is None:
        sys.modules.pop("openai", None)
    else:
        sys.modules["openai"] = saved


def _response(
    text: str = "ok",
    *,
    model: str = "openai.gpt-5.4",
    input_tok: int = 10,
    output_tok: int = 3,
    status: str = "completed",
    incomplete_reason: str | None = None,
) -> Any:
    details = (
        types.SimpleNamespace(reason=incomplete_reason) if incomplete_reason is not None else None
    )
    return types.SimpleNamespace(
        output_text=text,
        model=model,
        usage=types.SimpleNamespace(input_tokens=input_tok, output_tokens=output_tok),
        status=status,
        incomplete_details=details,
    )


# --- base URL ---------------------------------------------------------------


def test_mantle_base_url_derives_from_region(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("EFTERLEV_MANTLE_BASE_URL", raising=False)
    assert mantle_base_url("us-east-2") == "https://bedrock-mantle.us-east-2.api.aws/openai/v1"


def test_mantle_base_url_env_override(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("EFTERLEV_MANTLE_BASE_URL", "https://example.test/custom/v1")
    assert mantle_base_url("us-west-2") == "https://example.test/custom/v1"


# --- happy path / request shape ---------------------------------------------


def test_happy_path_returns_text_and_usage() -> None:
    _install_fake_openai(_response("hello", input_tok=42, output_tok=2))
    client = BedrockOpenAIClient(region="us-east-2", api_key="bedrock-key")
    resp = client.complete(
        system="be helpful", messages=[LLMMessage(content="hi")], model="openai.gpt-5.4"
    )
    assert resp.text == "hello"
    assert resp.model == "openai.gpt-5.4"
    assert resp.input_tokens == 42
    assert resp.output_tokens == 2
    assert len(resp.prompt_hash) == 64


def test_request_uses_responses_api_shape() -> None:
    """system → instructions, user → input, cap → max_output_tokens."""
    rec = _install_fake_openai(_response("x"))
    client = BedrockOpenAIClient(region="us-east-2", api_key="k")
    client.complete(
        system="SYS", messages=[LLMMessage(content="USER")], model="openai.gpt-5.4", max_tokens=999
    )
    call = rec.calls[0]
    assert call["model"] == "openai.gpt-5.4"
    assert call["instructions"] == "SYS"
    assert call["input"] == "USER"
    assert call["max_output_tokens"] == 999
    # No temperature (GPT-5 reasoning family rejects it).
    assert "temperature" not in call


def test_on_chunk_fires_once_with_final_text() -> None:
    _install_fake_openai(_response("the whole answer"))
    client = BedrockOpenAIClient(region="us-east-2", api_key="k")
    seen: list[str] = []
    client.complete(
        system="s",
        messages=[LLMMessage(content="u")],
        model="openai.gpt-5.4",
        on_chunk=seen.append,
    )
    assert seen == ["the whole answer"]


# --- error paths ------------------------------------------------------------


def test_truncation_raises_agent_error() -> None:
    _install_fake_openai(
        _response("partial", status="incomplete", incomplete_reason="max_output_tokens")
    )
    client = BedrockOpenAIClient(region="us-east-2", api_key="k")
    with pytest.raises(AgentError, match="truncated at max_output_tokens"):
        client.complete(system="s", messages=[LLMMessage(content="u")], model="openai.gpt-5.4")


def test_empty_text_raises_agent_error_listing_item_types() -> None:
    # status=completed, output_text empty, output items are reasoning-only.
    resp = types.SimpleNamespace(
        output_text="",
        model="openai.gpt-5.5",
        usage=types.SimpleNamespace(input_tokens=5, output_tokens=5),
        status="completed",
        incomplete_details=None,
        output=[types.SimpleNamespace(type="reasoning", content=[])],
    )
    _install_fake_openai(resp)
    client = BedrockOpenAIClient(region="us-east-2", api_key="k")
    with pytest.raises(AgentError, match=r"no text content.*output item types=\['reasoning'\]"):
        client.complete(system="s", messages=[LLMMessage(content="u")], model="openai.gpt-5.5")


def test_extracts_text_from_output_items_when_output_text_empty() -> None:
    """Regression for the gpt-5.5 'no text content (status=completed)' failure
    on Bedrock Mantle (2026-06-03): output_text comes back empty but the text
    is present in the structured output[].content[].text message items."""
    msg_item = types.SimpleNamespace(
        type="message",
        content=[
            types.SimpleNamespace(type="output_text", text="hello "),
            types.SimpleNamespace(type="output_text", text="world"),
        ],
    )
    resp = types.SimpleNamespace(
        output_text="",  # empty convenience aggregation
        model="openai.gpt-5.5",
        usage=types.SimpleNamespace(input_tokens=5, output_tokens=2),
        status="completed",
        incomplete_details=None,
        output=[types.SimpleNamespace(type="reasoning", content=[]), msg_item],
    )
    _install_fake_openai(resp)
    client = BedrockOpenAIClient(region="us-east-2", api_key="k")
    out = client.complete(system="s", messages=[LLMMessage(content="u")], model="openai.gpt-5.5")
    assert out.text == "hello world"


def test_missing_bedrock_key_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    _install_fake_openai(_response("x"))
    monkeypatch.delenv("AWS_BEARER_TOKEN_BEDROCK", raising=False)
    client = BedrockOpenAIClient(region="us-east-2")  # no api_key, no env
    with pytest.raises(AgentError, match="AWS_BEARER_TOKEN_BEDROCK is not set"):
        client.complete(system="s", messages=[LLMMessage(content="u")], model="openai.gpt-5.4")


def test_key_resolved_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    _install_fake_openai(_response("ok"))
    monkeypatch.setenv("AWS_BEARER_TOKEN_BEDROCK", "from-env")
    client = BedrockOpenAIClient(region="us-east-2")
    resp = client.complete(system="s", messages=[LLMMessage(content="u")], model="openai.gpt-5.4")
    assert resp.text == "ok"


def test_retries_on_transient_then_succeeds() -> None:
    def side_effect(_kwargs: dict[str, Any], n: int) -> Any:
        if n == 1:
            raise _RateLimitError("slow down")
        return _response("recovered")

    _install_fake_openai(side_effect)
    client = BedrockOpenAIClient(region="us-east-2", api_key="k", sleeper=lambda _s: None)
    resp = client.complete(system="s", messages=[LLMMessage(content="u")], model="openai.gpt-5.4")
    assert resp.text == "recovered"


def test_fallback_model_used_after_primary_exhausted() -> None:
    def side_effect(kwargs: dict[str, Any], _n: int) -> Any:
        if kwargs["model"] == "openai.gpt-5.4":
            raise _InternalServerError("boom")
        return _response("from fallback", model="openai.gpt-5.5")

    _install_fake_openai(side_effect)
    client = BedrockOpenAIClient(
        region="us-east-2", api_key="k", fallback_model="openai.gpt-5.5", sleeper=lambda _s: None
    )
    resp = client.complete(system="s", messages=[LLMMessage(content="u")], model="openai.gpt-5.4")
    assert resp.text == "from fallback"
