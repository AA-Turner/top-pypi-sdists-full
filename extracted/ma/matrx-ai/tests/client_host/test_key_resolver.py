"""KeyResolver seam: resolver precedence over env, and rotation re-keying."""

from __future__ import annotations

import pytest

from matrx_ai._ext import configure_ext
from matrx_ai.providers.keys import (
    ApiKeyNotFoundError,
    keyed_provider_client,
    resolve_api_key,
)

pytestmark = pytest.mark.usefixtures("client_host_sandbox")


def test_resolver_wins_over_env(monkeypatch):
    monkeypatch.setenv("KEYTEST_API_KEY", "from-env")
    configure_ext(api_key_resolver=lambda name: "from-resolver")
    assert resolve_api_key("KEYTEST_API_KEY") == "from-resolver"


def test_env_fallback_when_resolver_returns_none(monkeypatch):
    monkeypatch.setenv("KEYTEST_API_KEY", "from-env")
    configure_ext(api_key_resolver=lambda name: None)
    assert resolve_api_key("KEYTEST_API_KEY") == "from-env"


def test_ambient_request_key_precedes_environment(monkeypatch):
    from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context
    from matrx_connect.emitters import SilentEmitter

    monkeypatch.setenv("ANTHROPIC_API_KEY", "from-env")
    configure_ext(api_key_resolver=lambda name: None)
    token = set_app_context(
        AppContext(emitter=SilentEmitter(), api_keys={"anthropic": "from-request"})
    )
    try:
        assert resolve_api_key("ANTHROPIC_API_KEY") == "from-request"
    finally:
        clear_app_context(token)


def test_dual_name_order(monkeypatch):
    monkeypatch.delenv("KEYTEST_PRIMARY", raising=False)
    monkeypatch.setenv("KEYTEST_SECONDARY", "secondary")
    assert resolve_api_key("KEYTEST_PRIMARY", "KEYTEST_SECONDARY") == "secondary"

    keys = {"KEYTEST_PRIMARY": "primary"}
    configure_ext(api_key_resolver=lambda name: keys.get(name))
    assert resolve_api_key("KEYTEST_PRIMARY", "KEYTEST_SECONDARY") == "primary"


def test_required_raises_when_missing(monkeypatch):
    monkeypatch.delenv("KEYTEST_MISSING", raising=False)
    with pytest.raises(ApiKeyNotFoundError):
        resolve_api_key("KEYTEST_MISSING", required=True)
    assert resolve_api_key("KEYTEST_MISSING") is None


def test_rotation_rebuilds_memoized_client():
    """A keyed_provider_client memoizes ON THE RESOLVED KEY VALUE — rotating
    the key via the host resolver yields a fresh client on the next access,
    with no process restart and no instance rebuild."""
    built: list[str | None] = []

    class _FakeSdkClient:
        def __init__(self, api_key: str | None) -> None:
            self.api_key = api_key
            built.append(api_key)

    class Provider:
        client = keyed_provider_client(
            "KEYTEST_ROTATE",
            factory=lambda api_key: _FakeSdkClient(api_key),
        )

    current = {"key": "key-one"}
    configure_ext(api_key_resolver=lambda name: current["key"])

    provider = Provider()
    first = provider.client
    assert first.api_key == "key-one"
    assert provider.client is first  # same key → same memoized client
    assert built == ["key-one"]

    current["key"] = "key-two"  # host rotates the key
    second = provider.client
    assert second is not first
    assert second.api_key == "key-two"
    assert built == ["key-one", "key-two"]

    # Assignment pins: an injected stub disables re-keying for that instance.
    stub = object()
    provider.client = stub
    current["key"] = "key-three"
    assert provider.client is stub


def test_rotation_rebuilds_real_provider_chat_client():
    """End-to-end through a real provider class: OpenAIChat.client re-keys."""
    from matrx_ai.providers.openai.openai_api import OpenAIChat

    current = {"key": "sk-first"}
    configure_ext(api_key_resolver=lambda name: current["key"])

    chat = OpenAIChat()
    first = chat.client
    assert first.api_key == "sk-first"
    assert chat.client is first

    current["key"] = "sk-second"
    second = chat.client
    assert second is not first
    assert second.api_key == "sk-second"
