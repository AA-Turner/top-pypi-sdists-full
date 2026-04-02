"""Tests for stage tracking in durable stages and orchestrator tasks."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import ClassVar
from unittest.mock import AsyncMock, patch

import pytest
from pydantic import BaseModel, Field

from plato.worlds.durable import DurableOutputs, FromArg, durable
from plato.worlds.stage_tracking import (
    _current_stage_public_id,
    _stage_tracking_ctx,
    disable_stage_tracking,
    enable_stage_tracking,
    report_stage,
    serialize_args,
)


class Inner(BaseModel):
    value: int


class TrackingTestOutputs(DurableOutputs):
    DURABLE_PATH_TEMPLATE: ClassVar[str] = "{d}"
    results: Inner = Field(json_schema_extra={"json": "results.json"})


class TestEnableDisable:
    def test_enable_sets_context(self) -> None:
        token = enable_stage_tracking(
            session_id="test-session",
            base_url="https://test.example.com",
            api_key="test-key",
        )
        try:
            ctx = _stage_tracking_ctx.get()
            assert ctx is not None
            assert ctx.session_id == "test-session"
            assert ctx.base_url == "https://test.example.com"
            assert ctx.api_key == "test-key"
        finally:
            disable_stage_tracking(token)

    def test_disable_resets_context(self) -> None:
        token = enable_stage_tracking(session_id="s", base_url="https://test.example.com")
        disable_stage_tracking(token)
        assert _stage_tracking_ctx.get() is None

    def test_defaults_from_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("PLATO_API_KEY", "env-key")
        monkeypatch.setenv("CHRONOS_URL", "https://env.example.com")
        token = enable_stage_tracking(session_id="s")
        try:
            ctx = _stage_tracking_ctx.get()
            assert ctx is not None
            assert ctx.api_key == "env-key"
            assert ctx.base_url == "https://env.example.com"
        finally:
            disable_stage_tracking(token)


class TestSerializeArgs:
    def test_basic_types(self) -> None:
        result = serialize_args({"a": 1, "b": "hello", "c": True, "d": None})
        assert result == {"a": 1, "b": "hello", "c": True, "d": None}

    def test_path_to_str(self) -> None:
        result = serialize_args({"p": Path("/some/path")})
        assert result == {"p": "/some/path"}

    def test_complex_object_becomes_type_name(self) -> None:
        class MyWorld:
            pass

        result = serialize_args({"world": MyWorld()})
        assert result == {"world": "<MyWorld>"}

    def test_list_and_dict(self) -> None:
        result = serialize_args({"tags": ["a", "b"], "config": {"key": "val"}})
        assert result == {"tags": ["a", "b"], "config": {"key": "val"}}

    def test_non_serializable_in_list_falls_back(self) -> None:
        """Lists containing non-serializable objects should fall back to type name."""

        class Custom:
            pass

        result = serialize_args({"items": [Custom(), "ok"]})
        assert result == {"items": "<list>"}

    def test_non_serializable_in_dict_falls_back(self) -> None:
        """Dicts containing non-serializable values should fall back to type name."""

        class Custom:
            pass

        result = serialize_args({"data": {"nested": Custom()}})
        assert result == {"data": "<dict>"}

    def test_serializable_list_is_json_safe(self) -> None:
        """Returned list values must be fully JSON-serializable."""
        result = serialize_args({"items": [1, "two", None]})
        # Round-trip must succeed without error
        assert json.loads(json.dumps(result)) == result


class TestReportStage:
    @pytest.mark.asyncio
    async def test_noop_when_not_enabled(self) -> None:
        """report_stage should return None and not make HTTP calls when tracking is disabled."""
        result = await report_stage(
            stage_name="test",
            stage_type="durable",
            status="started",
            started_at=datetime.now(timezone.utc),
        )
        assert result is None

    @pytest.mark.asyncio
    async def test_sends_request_when_enabled(self) -> None:
        from plato.chronos.models import ReportStageResponse

        token = enable_stage_tracking(
            session_id="sess-123",
            base_url="https://test.example.com",
            api_key="test-key",
        )
        try:
            mock_resp = ReportStageResponse(public_id="test-public-id")
            with patch(
                "plato.worlds.stage_tracking._report_stage_api.asyncio",
                new_callable=AsyncMock,
                return_value=mock_resp,
            ) as mock_api:
                result = await report_stage(
                    stage_name="my_stage",
                    stage_type="durable",
                    status="started",
                    started_at=datetime.now(timezone.utc),
                    output_type="MyOutputs",
                )
            assert result == "test-public-id"
            mock_api.assert_called_once()
            call_kwargs = mock_api.call_args
            body = call_kwargs.kwargs["body"]
            assert body.session_public_id == "sess-123"
            assert body.stage_name == "my_stage"
            assert body.stage_type.value == "durable"
            assert body.status.value == "started"
            assert call_kwargs.kwargs["x_api_key"] == "test-key"
        finally:
            disable_stage_tracking(token)

    @pytest.mark.asyncio
    async def test_exception_does_not_propagate(self) -> None:
        token = enable_stage_tracking(
            session_id="s",
            base_url="https://test.example.com",
            api_key="k",
        )
        try:
            with patch(
                "plato.worlds.stage_tracking._report_stage_api.asyncio",
                new_callable=AsyncMock,
                side_effect=RuntimeError("network error"),
            ):
                result = await report_stage(
                    stage_name="test",
                    stage_type="durable",
                    status="started",
                    started_at=datetime.now(timezone.utc),
                )
            # Should not raise, just return None
            assert result is None
        finally:
            disable_stage_tracking(token)


class TestDurableIntegration:
    @pytest.mark.asyncio
    async def test_durable_reports_started_and_completed(self, tmp_path: Path) -> None:
        """Verify that @durable calls report_stage on cache miss."""
        calls: list[dict] = []

        async def mock_report(**kwargs):
            calls.append(kwargs)
            return "stage-pub-id" if kwargs["status"] == "started" else None

        @durable(d=FromArg("d"))
        async def my_stage(d: Path) -> TrackingTestOutputs:
            return TrackingTestOutputs(results=Inner(value=42))

        token = enable_stage_tracking(session_id="s", base_url="https://test.example.com")
        try:
            with patch("plato.worlds.stage_tracking.report_stage", side_effect=mock_report):
                # Also patch the import in durable.py
                with patch(
                    "plato.worlds.durable._report_stage_started",
                    side_effect=lambda *a, **kw: mock_report(
                        stage_name=a[0],
                        stage_type="durable",
                        status="started",
                        started_at=datetime.now(timezone.utc),
                        output_type=a[1],
                        base_path=a[2],
                        args_snapshot=a[3],
                    ),
                ):
                    with patch("plato.worlds.durable._report_stage_completed") as mock_completed:
                        result = await my_stage(d=tmp_path)
                        assert result.results.value == 42
                        mock_completed.assert_called_once()
        finally:
            disable_stage_tracking(token)

    @pytest.mark.asyncio
    async def test_started_at_consistent_across_lifecycle(self, tmp_path: Path) -> None:
        """All lifecycle reports must use the same started_at timestamp."""

        @durable(d=FromArg("d"))
        async def my_stage(d: Path) -> TrackingTestOutputs:
            return TrackingTestOutputs(results=Inner(value=1))

        token = enable_stage_tracking(session_id="s", base_url="https://test.example.com")
        try:
            with (
                patch(
                    "plato.worlds.durable._report_stage_started",
                    new_callable=AsyncMock,
                    return_value="pub-id",
                ) as mock_started,
                patch(
                    "plato.worlds.durable._report_stage_completed",
                    new_callable=AsyncMock,
                ) as mock_completed,
            ):
                await my_stage(d=tmp_path)

                # started_at is the last positional arg to _report_stage_started
                started_ts = mock_started.call_args[0][4]
                # and the last positional arg to _report_stage_completed
                completed_call_started_ts = mock_completed.call_args[0][4]
                assert started_ts == completed_call_started_ts
        finally:
            disable_stage_tracking(token)

    @pytest.mark.asyncio
    async def test_started_at_consistent_on_failure(self, tmp_path: Path) -> None:
        """Failed stage must report the same started_at as the started event."""

        @durable(d=FromArg("d"))
        async def failing_stage(d: Path) -> TrackingTestOutputs:
            raise ValueError("boom")

        token = enable_stage_tracking(session_id="s", base_url="https://test.example.com")
        try:
            with (
                patch(
                    "plato.worlds.durable._report_stage_started",
                    new_callable=AsyncMock,
                    return_value="pub-id",
                ) as mock_started,
                patch(
                    "plato.worlds.durable._report_stage_failed",
                    new_callable=AsyncMock,
                ) as mock_failed,
            ):
                with pytest.raises(ValueError, match="boom"):
                    await failing_stage(d=tmp_path)

                started_ts = mock_started.call_args[0][4]
                failed_call_started_ts = mock_failed.call_args[0][3]
                assert started_ts == failed_call_started_ts
        finally:
            disable_stage_tracking(token)

    @pytest.mark.asyncio
    async def test_durable_reports_failure(self, tmp_path: Path) -> None:
        """Verify that @durable reports stage failure on exception."""

        @durable(d=FromArg("d"))
        async def failing_stage(d: Path) -> TrackingTestOutputs:
            raise ValueError("something broke")

        token = enable_stage_tracking(session_id="s", base_url="https://test.example.com")
        try:
            with patch("plato.worlds.durable._report_stage_started", return_value="pub-id"):
                with patch("plato.worlds.durable._report_stage_failed") as mock_failed:
                    with pytest.raises(ValueError, match="something broke"):
                        await failing_stage(d=tmp_path)
                    mock_failed.assert_called_once()
                    args = mock_failed.call_args
                    assert args[0][0] == "failing_stage"  # stage_name
                    assert "something broke" in args[0][4]  # error message
        finally:
            disable_stage_tracking(token)

    @pytest.mark.asyncio
    async def test_cache_hit_does_not_report(self, tmp_path: Path) -> None:
        """On cache hit, no stage tracking should be reported."""

        @durable(d=FromArg("d"))
        async def my_stage(d: Path) -> TrackingTestOutputs:
            return TrackingTestOutputs(results=Inner(value=1))

        # Pre-populate cache
        (tmp_path / "results.json").write_text(json.dumps({"value": 1}))

        token = enable_stage_tracking(session_id="s", base_url="https://test.example.com")
        try:
            with patch("plato.worlds.durable._report_stage_started") as mock_started:
                result = await my_stage(d=tmp_path)
                assert result.results.value == 1
                mock_started.assert_not_called()
        finally:
            disable_stage_tracking(token)


class TestCurrentStagePublicId:
    @pytest.mark.asyncio
    async def test_context_var_set_during_durable(self, tmp_path: Path) -> None:
        """The _current_stage_public_id should be set inside a @durable function."""
        captured_id = None

        @durable(d=FromArg("d"))
        async def my_stage(d: Path) -> TrackingTestOutputs:
            nonlocal captured_id
            captured_id = _current_stage_public_id.get()
            return TrackingTestOutputs(results=Inner(value=1))

        token = enable_stage_tracking(session_id="s", base_url="https://test.example.com")
        try:
            with patch("plato.worlds.durable._report_stage_started", return_value="parent-pub-id"):
                with patch("plato.worlds.durable._report_stage_completed"):
                    await my_stage(d=tmp_path)
                    assert captured_id == "parent-pub-id"
        finally:
            disable_stage_tracking(token)

    def test_context_var_none_outside(self) -> None:
        assert _current_stage_public_id.get() is None


class TestBackwardCompat:
    """Verify backward compatibility of slack.py aliases."""

    def test_enable_slack_notifications_delegates(self) -> None:
        from plato.worlds.slack import disable_slack_notifications, enable_slack_notifications

        token = enable_slack_notifications(
            api_key="k",
            base_url="https://test.example.com",
            session_id="s",
        )
        try:
            ctx = _stage_tracking_ctx.get()
            assert ctx is not None
            assert ctx.session_id == "s"
        finally:
            disable_slack_notifications(token)
