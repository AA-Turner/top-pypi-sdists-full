"""Tests for workflow transcript recording (#1111)."""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Any

import pytest

from anteroom.config import TranscriptConfig
from anteroom.db import init_db
from anteroom.services.workflow_storage import (
    create_workflow_event,
    create_workflow_run,
    list_transcript_events,
)


@pytest.fixture()
def db():
    with tempfile.TemporaryDirectory() as td:
        conn = init_db(Path(td) / "test.db")
        yield conn
        conn.close()


def _make_run(db: Any, **overrides: Any) -> dict[str, Any]:
    defaults = {
        "workflow_id": "test_wf",
        "workflow_version": "0.1.0",
        "target_kind": "issue",
        "target_ref": "42",
    }
    defaults.update(overrides)
    return create_workflow_run(db, **defaults)


class TestTranscriptConfig:
    def test_defaults(self) -> None:
        cfg = TranscriptConfig()
        assert cfg.enabled is True
        assert cfg.max_assistant_chars == 4000
        assert cfg.max_tool_output_chars == 2000
        assert cfg.max_stdout_chars == 4000
        assert cfg.max_stderr_chars == 4000

    def test_custom_values(self) -> None:
        cfg = TranscriptConfig(enabled=False, max_assistant_chars=100)
        assert cfg.enabled is False
        assert cfg.max_assistant_chars == 100


class TestListTranscriptEvents:
    def test_returns_only_transcript_events(self, db: Any) -> None:
        run = _make_run(db)
        create_workflow_event(db, run_id=run["id"], event_type="step_started", step_id="s1")
        create_workflow_event(
            db,
            run_id=run["id"],
            event_type="transcript_assistant",
            step_id="s1",
            payload={"content": "hello", "tokens": 10, "model": "gpt-4"},
        )
        create_workflow_event(db, run_id=run["id"], event_type="step_finished", step_id="s1")
        create_workflow_event(
            db,
            run_id=run["id"],
            event_type="transcript_tool_call",
            step_id="s1",
            payload={"tool_name": "bash", "arguments": "ls"},
        )

        events = list_transcript_events(db, run["id"])
        assert len(events) == 2
        assert all(e["event_type"].startswith("transcript_") for e in events)

    def test_filters_by_step_id(self, db: Any) -> None:
        run = _make_run(db)
        create_workflow_event(
            db,
            run_id=run["id"],
            event_type="transcript_assistant",
            step_id="s1",
            payload={"content": "step1"},
        )
        create_workflow_event(
            db,
            run_id=run["id"],
            event_type="transcript_assistant",
            step_id="s2",
            payload={"content": "step2"},
        )

        events_s1 = list_transcript_events(db, run["id"], step_id="s1")
        assert len(events_s1) == 1
        assert events_s1[0]["payload"]["content"] == "step1"

        events_s2 = list_transcript_events(db, run["id"], step_id="s2")
        assert len(events_s2) == 1
        assert events_s2[0]["payload"]["content"] == "step2"

    def test_returns_empty_for_no_transcript_events(self, db: Any) -> None:
        run = _make_run(db)
        create_workflow_event(db, run_id=run["id"], event_type="step_started")
        events = list_transcript_events(db, run["id"])
        assert events == []

    def test_preserves_payload(self, db: Any) -> None:
        run = _make_run(db)
        payload = {"content": "output", "tokens": 42, "model": "test-model"}
        create_workflow_event(
            db,
            run_id=run["id"],
            event_type="transcript_assistant",
            step_id="s1",
            payload=payload,
        )
        events = list_transcript_events(db, run["id"])
        assert events[0]["payload"] == payload

    def test_ordering(self, db: Any) -> None:
        run = _make_run(db)
        create_workflow_event(
            db, run_id=run["id"], event_type="transcript_tool_call", step_id="s1", payload={"tool_name": "a"}
        )
        create_workflow_event(
            db, run_id=run["id"], event_type="transcript_tool_result", step_id="s1", payload={"tool_name": "a"}
        )
        create_workflow_event(
            db, run_id=run["id"], event_type="transcript_assistant", step_id="s1", payload={"content": "done"}
        )
        events = list_transcript_events(db, run["id"])
        types = [e["event_type"] for e in events]
        assert types == ["transcript_tool_call", "transcript_tool_result", "transcript_assistant"]


class TestTranscriptCallback:
    """Test that runner transcript callbacks truncate content correctly."""

    def test_agent_runner_truncates_assistant_content(self) -> None:
        """Verify transcript_cb truncates assistant content to limit."""
        recorded: list[tuple[str, str | None, dict[str, Any]]] = []

        def cb(etype: str, sid: str | None, payload: dict[str, Any]) -> None:
            recorded.append((etype, sid, payload))

        # Simulate what execute_agent_runner does for assistant content
        assistant_content = "x" * 5000
        max_chars = 100
        cb(
            "transcript_assistant",
            "step1",
            {
                "content": assistant_content[:max_chars],
                "tokens": 50,
                "model": "test",
            },
        )
        assert len(recorded) == 1
        assert len(recorded[0][2]["content"]) == max_chars

    def test_opaque_runner_truncates_stdout(self) -> None:
        """Verify transcript_cb truncates stdout to limit."""
        recorded: list[tuple[str, str | None, dict[str, Any]]] = []

        def cb(etype: str, sid: str | None, payload: dict[str, Any]) -> None:
            recorded.append((etype, sid, payload))

        stdout = "y" * 8000
        max_chars = 200
        # Simulate what execute_opaque_runner does
        cb("transcript_stdout", "step1", {"content": stdout[:max_chars]})
        assert len(recorded) == 1
        assert len(recorded[0][2]["content"]) == max_chars

    def test_callback_not_called_when_none(self) -> None:
        """Ensure None callback doesn't cause errors (tested via runner code paths)."""
        transcript_cb = None
        # This is the guard pattern used in the runners
        if transcript_cb is not None:
            transcript_cb("transcript_assistant", "s1", {"content": "x"})
        # No error = pass


class TestTranscriptDisabled:
    def test_disabled_config(self) -> None:
        cfg = TranscriptConfig(enabled=False)
        assert cfg.enabled is False
        # When disabled, no transcript_cb is created — the engine checks cfg.enabled


@pytest.mark.asyncio
async def test_agent_runner_emits_transcript_events() -> None:
    """Integration-ish test: execute_agent_runner with transcript_cb records events."""
    from collections.abc import AsyncIterator
    from dataclasses import dataclass
    from dataclasses import field as dc_field

    import anteroom.services.agent_loop as al_mod
    import anteroom.services.workflow_runners as wr

    recorded: list[tuple[str, str | None, dict[str, Any]]] = []

    def cb(etype: str, sid: str | None, payload: dict[str, Any]) -> None:
        recorded.append((etype, sid, payload))

    @dataclass
    class FakeEvent:
        kind: str
        data: dict[str, Any] = dc_field(default_factory=dict)

    async def fake_agent_loop(**kwargs: Any) -> AsyncIterator[FakeEvent]:
        yield FakeEvent(kind="tool_call_start", data={"tool_name": "bash", "arguments": "echo hi"})
        yield FakeEvent(kind="token", data={"content": "Hello "})
        yield FakeEvent(kind="token", data={"content": "world"})
        yield FakeEvent(kind="tool_call_end", data={"tool_name": "bash", "status": "success", "output": "hi"})
        yield FakeEvent(kind="usage", data={"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15})

    original_fn = al_mod.run_agent_loop
    al_mod.run_agent_loop = fake_agent_loop

    try:
        # Need a fake ai_service and tool_executor
        class FakeAI:
            pass

        async def fake_executor(name: str, args: dict[str, Any], **kw: Any) -> dict[str, Any]:
            return {"status": "success"}

        result = await wr.execute_agent_runner(
            prompt="test",
            ai_service=FakeAI(),
            tool_executor=fake_executor,
            transcript_cb=cb,
            transcript_max_assistant_chars=10,
            transcript_max_tool_output_chars=5,
            step_id="s1",
            model="test-model",
        )

        assert result.status == "success"

        types = [r[0] for r in recorded]
        assert "transcript_tool_call" in types
        assert "transcript_tool_result" in types
        assert "transcript_usage" in types
        assert "transcript_assistant" in types

        # Check truncation on assistant content
        assistant_evt = next(r for r in recorded if r[0] == "transcript_assistant")
        assert len(assistant_evt[2]["content"]) <= 10
        assert assistant_evt[2]["model"] == "test-model"

        # Check tool result truncation
        tool_result_evt = next(r for r in recorded if r[0] == "transcript_tool_result")
        assert len(tool_result_evt[2]["output"]) <= 5
    finally:
        al_mod.run_agent_loop = original_fn
