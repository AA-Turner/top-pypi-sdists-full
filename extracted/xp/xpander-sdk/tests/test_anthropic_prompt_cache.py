"""Anthropic prompt-caching: CachingClaude cache_control on tools + rolling message."""

from agno.models.message import Message

from xpander_sdk.modules.backend.frameworks._anthropic_cache import (
    CachingClaude,
    _inject_message_cache,
    _inject_tools_cache,
)

_EPHEMERAL = {"type": "ephemeral"}


def _system_and_user():
    # System block large enough that agno keeps it; content value is irrelevant here.
    return [
        Message(role="system", content="You are a helpful agent. " * 50),
        Message(role="user", content="hello there"),
    ]


def _tools():
    return [{"name": "foo", "description": "d", "parameters": {"type": "object", "properties": {}}}]


class TestAgnoBaseContract:
    def test_base_methods_exist(self):
        # CachingClaude reimplements agno's four invoke entrypoints. If a future agno
        # bump renames them or _prepare_request_kwargs / _has_beta_features, the
        # overrides drift silently. Fail loudly so a version bump is caught.
        from agno.models.anthropic import Claude

        for name in ("invoke", "invoke_stream", "ainvoke", "ainvoke_stream",
                     "_prepare_request_kwargs", "_has_beta_features"):
            assert hasattr(Claude, name), name
        # format_messages must remain importable from the same path.
        from agno.utils.models.claude import format_messages  # noqa: F401


class TestSupportsCache:
    def test_supported_families(self):
        for model_id in ("claude-3-5-sonnet", "claude-fable-5", "claude-opus-4-8", "claude-opus-5", "claude-sonnet-4-6", "claude-sonnet-5", "claude-haiku-4-5"):
            assert CachingClaude(id=model_id, api_key="x")._supports_cache(), model_id

    def test_unsupported_model(self):
        assert not CachingClaude(id="claude-2", api_key="x")._supports_cache()


class TestHelpers:
    def test_tools_cache_marks_last_tool_only(self):
        rk = {"tools": [{"name": "a"}, {"name": "b"}]}
        _inject_tools_cache(rk)
        assert "cache_control" not in rk["tools"][0]
        assert rk["tools"][-1]["cache_control"] == _EPHEMERAL

    def test_tools_cache_no_tools_noop(self):
        rk = {}
        _inject_tools_cache(rk)
        assert rk == {}

    def test_message_cache_promotes_string_content(self):
        cm = [{"role": "user", "content": "hi"}]
        _inject_message_cache(cm)
        assert cm[-1]["content"] == [{"type": "text", "text": "hi", "cache_control": _EPHEMERAL}]

    def test_message_cache_marks_last_block_of_list(self):
        cm = [{"role": "user", "content": [{"type": "tool_result", "content": "x"}]}]
        _inject_message_cache(cm)
        assert cm[-1]["content"][-1]["cache_control"] == _EPHEMERAL

    def test_message_cache_empty_string_noop(self):
        cm = [{"role": "user", "content": ""}]
        _inject_message_cache(cm)
        assert cm[-1]["content"] == ""

    def test_message_cache_empty_list_noop(self):
        cm = [{"role": "user", "content": []}]
        _inject_message_cache(cm)
        assert cm[-1]["content"] == []


class TestBuildCachedRequest:
    def test_supported_model_caches_system_tools_and_last_message(self):
        model = CachingClaude(id="claude-sonnet-4-6", api_key="x", cache_system_prompt=True)
        chat_messages, request_kwargs = model._build_cached_request(
            _system_and_user(), _tools(), None, False
        )
        assert request_kwargs["system"][-1].get("cache_control") == _EPHEMERAL
        assert request_kwargs["tools"][-1].get("cache_control") == _EPHEMERAL
        assert chat_messages[-1]["content"][-1].get("cache_control") == _EPHEMERAL

    def test_unsupported_model_marks_nothing_on_tools_or_messages(self):
        model = CachingClaude(id="claude-2", api_key="x", cache_system_prompt=False)
        chat_messages, request_kwargs = model._build_cached_request(
            _system_and_user(), _tools(), None, False
        )
        assert all("cache_control" not in t for t in request_kwargs.get("tools", []))
        last = chat_messages[-1]["content"]
        blocks = last if isinstance(last, list) else []
        assert all("cache_control" not in b for b in blocks)
