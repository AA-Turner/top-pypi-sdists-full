"""Provider prompt-caching: Bedrock cachePoint injection + Tokens cache fields."""

from agno.models.message import Message

from xpander_sdk.models.shared import Tokens
from xpander_sdk.modules.backend.frameworks._bedrock_cache import CachingAwsBedrock


def _system_and_user():
    # System block must be large enough that agno keeps it; content value is irrelevant here.
    return [
        Message(role="system", content="You are a helpful agent. " * 50),
        Message(role="user", content="hi"),
    ]


class TestCachingAwsBedrock:
    def test_agno_base_methods_exist(self):
        # CachingAwsBedrock overrides agno's private _format_messages /
        # _format_tools_for_request. If a future agno bump renames them, the
        # overrides silently stop running and caching regresses with no error.
        # This test fails loudly on the base class so a version bump is caught.
        from agno.models.aws.bedrock import AwsBedrock

        assert hasattr(AwsBedrock, "_format_messages")
        assert hasattr(AwsBedrock, "_format_tools_for_request")
        assert CachingAwsBedrock._format_messages is not AwsBedrock._format_messages
        assert (
            CachingAwsBedrock._format_tools_for_request
            is not AwsBedrock._format_tools_for_request
        )

    def test_cache_point_injected_for_claude_system_and_tools(self):
        model = CachingAwsBedrock(id="global.anthropic.claude-sonnet-4-6")
        _, system_message = model._format_messages(_system_and_user())
        assert system_message[-1] == {"cachePoint": {"type": "default"}}

        tools = [
            {
                "function": {
                    "name": "foo",
                    "description": "d",
                    "parameters": {"type": "object", "properties": {}},
                }
            }
        ]
        formatted_tools = model._format_tools_for_request(tools)
        assert formatted_tools[-1] == {"cachePoint": {"type": "default"}}

    def test_cache_point_injected_on_last_message(self):
        # Rolling breakpoint: the last message's content carries a cachePoint so the
        # growing conversation prefix is cached too, not just system + tools.
        model = CachingAwsBedrock(id="global.anthropic.claude-sonnet-4-6")
        formatted, _ = model._format_messages(_system_and_user())
        assert formatted[-1]["content"][-1] == {"cachePoint": {"type": "default"}}
        # earlier messages must NOT carry a cachePoint (only the last one rolls)
        for earlier in formatted[:-1]:
            assert all("cachePoint" not in b for b in earlier["content"])

    def test_no_message_cache_point_for_unsupported_model(self):
        model = CachingAwsBedrock(id="meta.llama3-70b-instruct-v1:0")
        formatted, _ = model._format_messages(_system_and_user())
        for msg in formatted:
            assert all("cachePoint" not in b for b in msg["content"])

    def test_nova_model_also_cached(self):
        model = CachingAwsBedrock(id="amazon.nova-pro-v1:0")
        formatted, system_message = model._format_messages(_system_and_user())
        assert system_message[-1] == {"cachePoint": {"type": "default"}}
        assert formatted[-1]["content"][-1] == {"cachePoint": {"type": "default"}}

    def test_no_cache_point_for_unsupported_model(self):
        model = CachingAwsBedrock(id="meta.llama3-70b-instruct-v1:0")
        _, system_message = model._format_messages(_system_and_user())
        assert all("cachePoint" not in block for block in system_message)
        tools = [
            {
                "function": {
                    "name": "foo",
                    "description": "d",
                    "parameters": {"type": "object", "properties": {}},
                }
            }
        ]
        assert all(
            "cachePoint" not in t for t in model._format_tools_for_request(tools)
        )

    def test_no_tools_no_cache_point(self):
        model = CachingAwsBedrock(id="global.anthropic.claude-sonnet-4-6")
        assert model._format_tools_for_request(None) == []


class TestEmptyTextBlockSanitation:
    """Bedrock rejects {"text": ""} blocks — _format_messages must repair them."""

    @staticmethod
    def _texts(content):
        return [b["text"] for b in content if isinstance(b, dict) and "text" in b]

    def test_empty_text_dropped_siblings_kept(self):
        # Message with empty content + tool_calls. agno emits a toolUse-only
        # block here, but a list content carrying an empty text would leak — feed
        # that shape directly to prove the empty text is dropped, toolUse kept.
        model = CachingAwsBedrock(id="global.anthropic.claude-sonnet-4-6")
        msg = Message(
            role="assistant",
            content=[{"text": ""}, {"toolUse": {"toolUseId": "t1", "name": "foo"}}],
        )
        formatted, _ = model._format_messages([Message(role="user", content="hi"), msg])
        assistant = next(m for m in formatted if m["role"] == "assistant")
        assert {"text": ""} not in assistant["content"]
        assert {"toolUse": {"toolUseId": "t1", "name": "foo"}} in assistant["content"]

    def test_lone_empty_text_replaced_with_placeholder(self):
        model = CachingAwsBedrock(id="global.anthropic.claude-sonnet-4-6")
        formatted, _ = model._format_messages([Message(role="user", content="")])
        content = formatted[0]["content"]
        assert content  # not an empty array
        assert all(b.get("text", "x").strip() != "" for b in content)

    def test_whitespace_only_treated_as_empty(self):
        model = CachingAwsBedrock(id="global.anthropic.claude-sonnet-4-6")
        formatted, _ = model._format_messages([Message(role="user", content="   ")])
        content = formatted[0]["content"]
        assert content
        assert all(b.get("text", "x").strip() != "" for b in content)

    def test_non_empty_text_untouched(self):
        model = CachingAwsBedrock(id="global.anthropic.claude-sonnet-4-6")
        formatted, _ = model._format_messages([Message(role="user", content="hi")])
        assert {"text": "hi"} in formatted[0]["content"]

    def test_empty_system_block_repaired_and_cached(self):
        model = CachingAwsBedrock(id="global.anthropic.claude-sonnet-4-6")
        _, system_message = model._format_messages(
            [Message(role="system", content=""), Message(role="user", content="hi")]
        )
        assert {"text": ""} not in system_message
        assert system_message[-1] == {"cachePoint": {"type": "default"}}


class TestTokensCacheFields:
    def test_cache_fields_default_zero_and_serialize(self):
        t = Tokens(prompt_tokens=100, completion_tokens=20)
        dumped = t.model_dump()
        assert dumped["cache_read_tokens"] == 0
        assert dumped["cache_write_tokens"] == 0

    def test_total_excludes_cache_tokens(self):
        t = Tokens(
            prompt_tokens=100,
            completion_tokens=20,
            cache_read_tokens=900,
            cache_write_tokens=80,
        )
        # total is prompt + completion only — cache counts never folded in
        assert t.total_tokens == 120


class TestWireBudgetOrdering:
    """The wire line must report tools, which agno formats AFTER messages."""

    @staticmethod
    def _capture(monkeypatch):
        from xpander_sdk.modules.backend.utils import prompt_budget as pb

        pb._WIRE_SEEN.clear()
        lines: list[str] = []
        monkeypatch.setattr(pb.logger, "info", lambda msg: lines.append(msg))
        return lines

    @staticmethod
    def _tool(name: str):
        return {
            "function": {
                "name": name,
                "description": "d" * 400,
                "parameters": {"type": "object", "properties": {"payload": {}}},
            }
        }

    def test_formatting_messages_alone_emits_nothing(self, monkeypatch):
        lines = self._capture(monkeypatch)
        model = CachingAwsBedrock(id="global.anthropic.claude-sonnet-4-6")
        model._format_messages(_system_and_user())
        assert not [ln for ln in lines if "wire" in ln]

    def test_wire_line_counts_tools_in_agno_call_order(self, monkeypatch):
        import json

        lines = self._capture(monkeypatch)
        model = CachingAwsBedrock(id="global.anthropic.claude-sonnet-4-6")
        # agno formats messages first, then tools — reproduce that order exactly.
        model._format_messages(_system_and_user())
        model._format_tools_for_request(
            [self._tool("xpworkspace-bash"), self._tool("xpschedule-create")]
        )

        wire = [ln for ln in lines if "[prompt-budget] wire" in ln]
        assert len(wire) == 1
        payload = json.loads(wire[0].split("wire ", 1)[1])
        assert payload["tools"]["count"] == 2
        assert payload["tools"]["xpworkspace"] > 0
        assert payload["system_tok"] > 0
        # The total is what reconciles against the turn's cache_write.
        assert payload["total_tok"] == payload["system_tok"] + payload["tools"]["total_tok"]
