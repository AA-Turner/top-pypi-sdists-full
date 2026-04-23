"""Unit tests for hook snapshot audit emission."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from unittest.mock import MagicMock

from anteroom.services.audit import AuditEntry
from anteroom.services.lineage import emit_hook_snapshot


def _capture_writer() -> tuple[Any, list[AuditEntry]]:
    captured: list[AuditEntry] = []
    writer = MagicMock()
    writer.emit.side_effect = captured.append
    return writer, captured


@dataclass
class _Matcher:
    tool_name: str = "*"
    arguments: dict[str, str] = field(default_factory=dict)


@dataclass
class _Runner:
    type: str = "command"
    command: str = ""
    url: str = ""
    timeout: int = 5


@dataclass
class _Entry:
    id: str = "hook-1"
    event: str = "pre_tool"
    matcher: _Matcher = field(default_factory=_Matcher)
    runner: _Runner = field(default_factory=_Runner)
    message: str = ""
    trust_source: str = "personal"

    @property
    def is_executable(self) -> bool:
        return self.trust_source in ("personal", "team")


@dataclass
class _HooksConfig:
    pre_tool: list[_Entry] = field(default_factory=list)
    post_tool: list[_Entry] = field(default_factory=list)


class TestEmitHookSnapshot:
    def test_none_writer_is_noop(self) -> None:
        emit_hook_snapshot(None, _HooksConfig())

    def test_emits_hook_snapshot_event(self) -> None:
        writer, captured = _capture_writer()
        hooks = _HooksConfig(pre_tool=[_Entry(id="pre-1", runner=_Runner(type="command", command="echo hi"))])

        emit_hook_snapshot(writer, hooks)

        assert len(captured) == 1
        entry = captured[0]
        assert entry.event_type == "hook.snapshot"
        assert entry.severity == "info"
        assert entry.details["hook_count"] == 1
        assert entry.details["entries"][0]["id"] == "pre-1"
        assert entry.details["entries"][0]["event"] == "pre_tool"
        assert entry.details["entries"][0]["runner_type"] == "command"

    def test_hash_is_stable_for_same_payload(self) -> None:
        writer, captured = _capture_writer()
        hooks = _HooksConfig(
            pre_tool=[
                _Entry(
                    id="stable",
                    matcher=_Matcher(tool_name="bash", arguments={"command": "ls"}),
                    runner=_Runner(type="command", command="echo guard", timeout=7),
                    message="guard",
                )
            ]
        )

        emit_hook_snapshot(writer, hooks)
        emit_hook_snapshot(writer, hooks)

        first = captured[0].details["entries"][0]["entry_sha256"]
        second = captured[1].details["entries"][0]["entry_sha256"]
        assert first == second

    def test_pack_entry_records_non_executable_status(self) -> None:
        writer, captured = _capture_writer()
        hooks = _HooksConfig(post_tool=[_Entry(id="pack-1", event="post_tool", trust_source="pack")])

        emit_hook_snapshot(writer, hooks)

        payload = captured[0].details["entries"][0]
        assert payload["trust_source"] == "pack"
        assert payload["is_executable"] is False
