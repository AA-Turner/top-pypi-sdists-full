"""The tool-definition wire calls hit the sanctioned endpoints with the right body and retry transient errors."""

from __future__ import annotations

import httpx
import pytest

from matrx_ai.providers.anthropic import tool_definition_wire as wire
from matrx_ai.providers.anthropic.broker import COUNT_TOKENS_URL, MESSAGES_URL


def _resp(status: int, body: dict, url: str) -> httpx.Response:
    return httpx.Response(status, json=body, request=httpx.Request("POST", url))


def test_count_input_tokens_posts_to_count_endpoint_and_spends_nothing(monkeypatch: pytest.MonkeyPatch) -> None:
    seen: dict = {}

    def fake_post(url, *, headers, json, timeout):
        seen.update(url=url, headers=headers, json=json)
        return _resp(200, {"input_tokens": 42}, url)

    monkeypatch.setattr(wire.httpx, "post", fake_post)
    n = wire.count_input_tokens(
        api_key="k", model="m", messages=[{"role": "user", "content": "hi"}], tools=[{"name": "t"}]
    )
    assert n == 42
    assert seen["url"] == COUNT_TOKENS_URL
    assert seen["headers"]["x-api-key"] == "k"
    assert seen["json"]["tools"] == [{"name": "t"}]
    assert "max_tokens" not in seen["json"]


def test_tool_call_trial_returns_first_tool_use_and_usage_and_retries_429(monkeypatch: pytest.MonkeyPatch) -> None:
    replies = [
        _resp(429, {"error": "slow down"}, MESSAGES_URL),
        _resp(
            200,
            {
                "content": [{"type": "text", "text": "ok"}, {"type": "tool_use", "input": {"action": "edit"}}],
                "usage": {"input_tokens": 10, "output_tokens": 3},
            },
            MESSAGES_URL,
        ),
    ]
    monkeypatch.setattr(wire.httpx, "post", lambda url, **kw: replies.pop(0))
    monkeypatch.setattr(wire.time, "sleep", lambda _s: None)
    out = wire.tool_call_trial(api_key="k", model="m", system="s", prompt="p", tools=[{"name": "t"}])
    assert (out.tool_input, out.input_tokens, out.output_tokens) == ({"action": "edit"}, 10, 3)


def test_tool_call_trial_no_tool_use_is_none(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        wire.httpx, "post", lambda url, **kw: _resp(200, {"content": [{"type": "text", "text": "no"}]}, MESSAGES_URL)
    )
    assert wire.tool_call_trial(api_key="k", model="m", system="s", prompt="p", tools=[]).tool_input is None


def test_non_retryable_error_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(wire.httpx, "post", lambda url, **kw: _resp(400, {"error": "bad"}, COUNT_TOKENS_URL))
    with pytest.raises(httpx.HTTPStatusError):
        wire.count_input_tokens(api_key="k", model="m", messages=[])
