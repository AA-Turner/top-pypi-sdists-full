"""Tests for backward-compatible Slack notification aliases.

The original Slack notification system has been replaced by stage tracking.
These tests verify that the backward-compatible aliases in ``slack.py``
still work and delegate correctly to ``stage_tracking.py``.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import ClassVar
from unittest.mock import patch

import pytest
from pydantic import BaseModel, Field

from plato.worlds.durable import DurableOutputs, FromArg, durable
from plato.worlds.slack import (
    disable_slack_notifications,
    enable_slack_notifications,
)
from plato.worlds.stage_tracking import _stage_tracking_ctx


class Inner(BaseModel):
    value: int


class SlackTestOutputs(DurableOutputs):
    DURABLE_PATH_TEMPLATE: ClassVar[str] = "{d}"
    results: Inner = Field(json_schema_extra={"json": "results.json"})


class TestEnableDisable:
    def test_enable_sets_context(self) -> None:
        token = enable_slack_notifications(api_key="test-key", base_url="https://test.example.com")
        try:
            ctx = _stage_tracking_ctx.get()
            assert ctx is not None
            assert ctx.base_url == "https://test.example.com"
            assert ctx.api_key == "test-key"
        finally:
            disable_slack_notifications(token)

    def test_disable_resets_context(self) -> None:
        token = enable_slack_notifications(api_key="k", base_url="https://test.example.com")
        disable_slack_notifications(token)
        assert _stage_tracking_ctx.get() is None

    def test_session_id_passed_through(self) -> None:
        token = enable_slack_notifications(
            api_key="k",
            base_url="https://test.example.com",
            session_id="abc-123",
        )
        try:
            ctx = _stage_tracking_ctx.get()
            assert ctx is not None
            assert ctx.session_id == "abc-123"
        finally:
            disable_slack_notifications(token)

    def test_chronos_url_used_as_base_url(self) -> None:
        token = enable_slack_notifications(
            api_key="k",
            chronos_url="https://chronos.plato.so",
            session_id="s",
        )
        try:
            ctx = _stage_tracking_ctx.get()
            assert ctx is not None
            assert ctx.base_url == "https://chronos.plato.so"
        finally:
            disable_slack_notifications(token)

    def test_formatter_accepted_but_ignored(self) -> None:
        """The formatter parameter is accepted for backward compatibility but ignored."""

        def my_fmt(stage: str, out: str, elapsed: float, path: str) -> str:
            return f"custom: {stage}"

        token = enable_slack_notifications(api_key="k", base_url="https://test.example.com", formatter=my_fmt)
        try:
            ctx = _stage_tracking_ctx.get()
            assert ctx is not None
        finally:
            disable_slack_notifications(token)


class TestDurableSlackIntegration:
    @pytest.mark.asyncio
    async def test_async_durable_reports_stage_tracking(self, tmp_path: Path) -> None:
        """Durable stages now report via stage tracking, not Slack directly."""

        @durable(d=FromArg("d"))
        async def my_stage(d: Path) -> SlackTestOutputs:
            return SlackTestOutputs(results=Inner(value=1))

        token = enable_slack_notifications(api_key="k", base_url="https://test.example.com")
        try:
            with patch("plato.worlds.durable._report_stage_started", return_value="pub-id") as mock_started:
                with patch("plato.worlds.durable._report_stage_completed") as mock_completed:
                    result = await my_stage(d=tmp_path)
                    assert result.results.value == 1
                    mock_started.assert_called_once()
                    mock_completed.assert_called_once()
        finally:
            disable_slack_notifications(token)

    @pytest.mark.asyncio
    async def test_async_durable_cache_hit_no_tracking(self, tmp_path: Path) -> None:
        # Pre-populate cache
        (tmp_path / "results.json").write_text(json.dumps({"value": 99}))

        @durable(d=FromArg("d"))
        async def my_stage(d: Path) -> SlackTestOutputs:
            raise AssertionError("should not run")

        token = enable_slack_notifications(api_key="k", base_url="https://test.example.com")
        try:
            with patch("plato.worlds.durable._report_stage_started") as mock_started:
                result = await my_stage(d=tmp_path)
                assert result.results.value == 99
                mock_started.assert_not_called()
        finally:
            disable_slack_notifications(token)

    @pytest.mark.asyncio
    async def test_tracking_failure_does_not_crash_durable(self, tmp_path: Path) -> None:
        @durable(d=FromArg("d"))
        async def my_stage(d: Path) -> SlackTestOutputs:
            return SlackTestOutputs(results=Inner(value=42))

        token = enable_slack_notifications(api_key="k", base_url="https://test.example.com")
        try:
            # Patch the underlying report_stage to fail — _report_stage_started
            # catches this internally and returns None
            with patch("plato.worlds.stage_tracking.report_stage", side_effect=Exception("tracking down")):
                result = await my_stage(d=tmp_path)
                assert result.results.value == 42
                assert (tmp_path / "results.json").exists()
        finally:
            disable_slack_notifications(token)

    def test_sync_durable_no_notification_without_context(self, tmp_path: Path) -> None:
        """Sync durable without tracking enabled should just work."""

        @durable(d=FromArg("d"))
        def my_stage(d: Path) -> SlackTestOutputs:
            return SlackTestOutputs(results=Inner(value=7))

        result = my_stage(d=tmp_path)
        assert result.results.value == 7
