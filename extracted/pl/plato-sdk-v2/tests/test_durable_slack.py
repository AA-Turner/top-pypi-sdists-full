"""Tests for Slack notifications in durable stages."""

from __future__ import annotations

import asyncio
import json
from pathlib import Path
from typing import ClassVar
from unittest.mock import AsyncMock, patch

import pytest
from pydantic import BaseModel, Field

from plato.worlds.durable import DurableOutputs, FromArg, durable
from plato.worlds.slack import (
    _default_formatter,
    _slack_notify_ctx,
    disable_slack_notifications,
    enable_slack_notifications,
    notify_stage_complete,
)


class Inner(BaseModel):
    value: int


class SlackTestOutputs(DurableOutputs):
    DURABLE_PATH_TEMPLATE: ClassVar[str] = "{d}"
    results: Inner = Field(json_schema_extra={"json": "results.json"})


class TestDefaultFormatter:
    def test_format(self) -> None:
        msg = _default_formatter("my_stage", "MyOutputs", 12.345, "/some/path")
        assert "my_stage" in msg
        assert "12.3s" in msg
        assert "MyOutputs" in msg

    def test_format_short_time(self) -> None:
        msg = _default_formatter("fast", "Out", 0.05, "/p")
        assert "0.1s" in msg or "0.0s" in msg


class TestEnableDisable:
    def test_enable_sets_context(self) -> None:
        token = enable_slack_notifications(api_key="test-key", base_url="https://test.example.com")
        try:
            ctx = _slack_notify_ctx.get()
            assert ctx is not None
            url, key, fmt = ctx
            assert url == "https://test.example.com"
            assert key == "test-key"
            assert fmt is _default_formatter
        finally:
            disable_slack_notifications(token)

    def test_disable_resets_context(self) -> None:
        token = enable_slack_notifications(api_key="k", base_url="https://test.example.com")
        disable_slack_notifications(token)
        assert _slack_notify_ctx.get() is None

    def test_custom_formatter(self) -> None:
        def my_fmt(stage: str, out: str, elapsed: float, path: str) -> str:
            return f"custom: {stage}"

        token = enable_slack_notifications(api_key="k", base_url="https://test.example.com", formatter=my_fmt)
        try:
            ctx = _slack_notify_ctx.get()
            assert ctx is not None
            _, _, fmt = ctx
            assert fmt is my_fmt
        finally:
            disable_slack_notifications(token)


class TestNotifyStageComplete:
    @pytest.mark.asyncio
    async def test_noop_when_disabled(self) -> None:
        # Should not raise when no context is set
        await notify_stage_complete("stage", "Output", 1.0, "/path")

    @pytest.mark.asyncio
    async def test_sends_message_when_enabled(self) -> None:
        mock_send = AsyncMock()

        token = enable_slack_notifications(api_key="test-key", base_url="https://test.example.com")
        try:
            with patch("plato.worlds.slack.send_slack_message.asyncio", mock_send):
                await notify_stage_complete("my_stage", "MyOutputs", 5.0, "/base")

            mock_send.assert_called_once()
            call_args = mock_send.call_args
            body = call_args.kwargs.get("body") or call_args[0][1]
            assert "my_stage" in body.message
        finally:
            disable_slack_notifications(token)

    @pytest.mark.asyncio
    async def test_formatter_returning_none_skips(self) -> None:
        mock_send = AsyncMock()

        token = enable_slack_notifications(api_key="k", base_url="https://test.example.com", formatter=lambda *_: None)
        try:
            with patch("plato.worlds.slack.send_slack_message.asyncio", mock_send):
                await notify_stage_complete("stage", "Out", 1.0, "/p")
            mock_send.assert_not_called()
        finally:
            disable_slack_notifications(token)

    @pytest.mark.asyncio
    async def test_exception_does_not_propagate(self) -> None:
        mock_send = AsyncMock(side_effect=RuntimeError("network error"))

        token = enable_slack_notifications(api_key="k", base_url="https://test.example.com")
        try:
            with patch("plato.worlds.slack.send_slack_message.asyncio", mock_send):
                # Should not raise
                await notify_stage_complete("stage", "Out", 1.0, "/p")
        finally:
            disable_slack_notifications(token)


class TestDurableSlackIntegration:
    @pytest.mark.asyncio
    async def test_async_durable_sends_notification(self, tmp_path: Path) -> None:
        mock_send = AsyncMock()

        @durable(d=FromArg("d"))
        async def my_stage(d: Path) -> SlackTestOutputs:
            return SlackTestOutputs(results=Inner(value=1))

        token = enable_slack_notifications(api_key="k", base_url="https://test.example.com")
        try:
            with patch("plato.worlds.slack.send_slack_message.asyncio", mock_send):
                result = await my_stage(d=tmp_path)
                await asyncio.sleep(0)  # let fire-and-forget task run

                assert result.results.value == 1
                mock_send.assert_called_once()
                body = mock_send.call_args.kwargs.get("body") or mock_send.call_args[0][1]
                assert "my_stage" in body.message
        finally:
            disable_slack_notifications(token)

    @pytest.mark.asyncio
    async def test_async_durable_cache_hit_no_notification(self, tmp_path: Path) -> None:
        # Pre-populate cache
        (tmp_path / "results.json").write_text(json.dumps({"value": 99}))

        mock_send = AsyncMock()

        @durable(d=FromArg("d"))
        async def my_stage(d: Path) -> SlackTestOutputs:
            raise AssertionError("should not run")

        token = enable_slack_notifications(api_key="k", base_url="https://test.example.com")
        try:
            with patch("plato.worlds.slack.send_slack_message.asyncio", mock_send):
                result = await my_stage(d=tmp_path)
                await asyncio.sleep(0)

                assert result.results.value == 99
                mock_send.assert_not_called()
        finally:
            disable_slack_notifications(token)

    @pytest.mark.asyncio
    async def test_slack_failure_does_not_crash_durable(self, tmp_path: Path) -> None:
        mock_send = AsyncMock(side_effect=Exception("slack is down"))

        @durable(d=FromArg("d"))
        async def my_stage(d: Path) -> SlackTestOutputs:
            return SlackTestOutputs(results=Inner(value=42))

        token = enable_slack_notifications(api_key="k", base_url="https://test.example.com")
        try:
            with patch("plato.worlds.slack.send_slack_message.asyncio", mock_send):
                result = await my_stage(d=tmp_path)
                await asyncio.sleep(0)  # let fire-and-forget task run

                # Stage should succeed despite slack failure
                assert result.results.value == 42
                assert (tmp_path / "results.json").exists()
        finally:
            disable_slack_notifications(token)

    def test_sync_durable_no_notification_without_loop(self, tmp_path: Path) -> None:
        """Sync durable without an event loop just skips notifications."""

        @durable(d=FromArg("d"))
        def my_stage(d: Path) -> SlackTestOutputs:
            return SlackTestOutputs(results=Inner(value=7))

        # No slack enabled, should just work
        result = my_stage(d=tmp_path)
        assert result.results.value == 7

    def test_sync_durable_sends_notification_via_new_loop(self, tmp_path: Path) -> None:
        """Sync durable without a running loop creates one and sends the notification."""
        mock_send = AsyncMock()

        @durable(d=FromArg("d"))
        def my_stage(d: Path) -> SlackTestOutputs:
            return SlackTestOutputs(results=Inner(value=8))

        token = enable_slack_notifications(api_key="k", base_url="https://test.example.com")
        try:
            with patch("plato.worlds.slack.send_slack_message.asyncio", mock_send):
                result = my_stage(d=tmp_path)

            assert result.results.value == 8
            mock_send.assert_called_once()
            body = mock_send.call_args.kwargs.get("body") or mock_send.call_args[0][1]
            assert "my_stage" in body.message
        finally:
            disable_slack_notifications(token)
