"""
Tests for Claude API client (Anthropic SDK wrapper).
"""

import json
import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.api.claude_api import ClaudeAPI


@pytest.fixture
def api_key():
    return "sk-ant-test-key"


@pytest.fixture
def claude_api(api_key):
    with patch("src.api.claude_api.AsyncAnthropic"):
        return ClaudeAPI(api_key=api_key)


class TestClaudeAPIInit:
    def test_init_with_explicit_key(self, api_key):
        with patch("src.api.claude_api.AsyncAnthropic"):
            api = ClaudeAPI(api_key=api_key)
        assert api.model == "claude-sonnet-4-6"
        assert api.max_tokens == 4096

    def test_init_from_env(self, api_key):
        with patch.dict(os.environ, {"CLAUDE_API_KEY": api_key}):
            with patch("src.api.claude_api.AsyncAnthropic"):
                api = ClaudeAPI()
        assert api.is_configured()

    def test_init_without_key_raises(self):
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="CLAUDE_API_KEY"):
                ClaudeAPI()

    def test_is_configured(self, claude_api):
        assert claude_api.is_configured() is True


class TestClaudeAPIComplete:
    @pytest.mark.asyncio
    async def test_generate_response(self, claude_api):
        mock_msg = MagicMock()
        mock_msg.content = [MagicMock(text="Hello!")]
        claude_api._client.messages.create = AsyncMock(return_value=mock_msg)

        result = await claude_api.generate_response("Say hello")
        assert result == "Hello!"

    @pytest.mark.asyncio
    async def test_generate_completion(self, claude_api):
        mock_msg = MagicMock()
        mock_msg.content = [MagicMock(text="Done.")]
        claude_api._client.messages.create = AsyncMock(return_value=mock_msg)

        result = await claude_api.generate_completion(
            "Do a task", system_prompt="You are helpful."
        )
        assert result == "Done."
        call_kwargs = claude_api._client.messages.create.call_args.kwargs
        assert call_kwargs["system"] == "You are helpful."

    @pytest.mark.asyncio
    async def test_summarize_text(self, claude_api):
        mock_msg = MagicMock()
        mock_msg.content = [MagicMock(text="Short summary.")]
        claude_api._client.messages.create = AsyncMock(return_value=mock_msg)

        result = await claude_api.summarize_text("Long text here...")
        assert result == "Short summary."

    @pytest.mark.asyncio
    async def test_chat(self, claude_api):
        mock_msg = MagicMock()
        mock_msg.content = [MagicMock(text="Chat response.")]
        claude_api._client.messages.create = AsyncMock(return_value=mock_msg)

        messages = [{"role": "user", "content": "Hi"}]
        result = await claude_api.chat(messages)
        assert result == "Chat response."
        call_kwargs = claude_api._client.messages.create.call_args.kwargs
        assert call_kwargs["messages"] == messages


class TestSummarizeConversation:
    @pytest.mark.asyncio
    async def test_returns_parsed_json(self, claude_api):
        payload = {
            "summary": "Team discussed project.",
            "key_points": ["Point A"],
            "action_items": ["Do X"],
            "unresolved_items": [],
        }
        mock_msg = MagicMock()
        mock_msg.content = [MagicMock(text=json.dumps(payload))]
        claude_api._client.messages.create = AsyncMock(return_value=mock_msg)

        messages = [{"role": "user", "content": "Let's ship it"}]
        result = await claude_api.summarize_conversation(messages)
        assert result["summary"] == "Team discussed project."
        assert result["action_items"] == ["Do X"]

    @pytest.mark.asyncio
    async def test_falls_back_on_non_json(self, claude_api):
        mock_msg = MagicMock()
        mock_msg.content = [MagicMock(text="Just plain text, no JSON here.")]
        claude_api._client.messages.create = AsyncMock(return_value=mock_msg)

        result = await claude_api.summarize_conversation(
            [{"role": "user", "content": "Hi"}]
        )
        assert "summary" in result
        assert result["key_points"] == []

    @pytest.mark.asyncio
    async def test_strips_markdown_fences(self, claude_api):
        payload = {
            "summary": "Good.",
            "key_points": [],
            "action_items": [],
            "unresolved_items": [],
        }
        wrapped = f"```json\n{json.dumps(payload)}\n```"
        mock_msg = MagicMock()
        mock_msg.content = [MagicMock(text=wrapped)]
        claude_api._client.messages.create = AsyncMock(return_value=mock_msg)

        result = await claude_api.summarize_conversation([])
        assert result["summary"] == "Good."

    @pytest.mark.asyncio
    async def test_accepts_plain_string_messages(self, claude_api):
        """board summarize (src/routers/boards.py) builds a List[str] of
        log-line-style messages, not List[Dict] -- summarize_conversation
        must handle both shapes without crashing."""
        payload = {
            "summary": "Board is on track.",
            "key_points": [],
            "action_items": [],
            "unresolved_items": [],
        }
        mock_msg = MagicMock()
        mock_msg.content = [MagicMock(text=json.dumps(payload))]
        claude_api._client.messages.create = AsyncMock(return_value=mock_msg)

        result = await claude_api.summarize_conversation(
            messages=["Board: Example", "\n=== CURRENTLY ACTIVE TICKETS ==="],
            prompt="Summarize board status",
        )
        assert result["summary"] == "Board is on track."
