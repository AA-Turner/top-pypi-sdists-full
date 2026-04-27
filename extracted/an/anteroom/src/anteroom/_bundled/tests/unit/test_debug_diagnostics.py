from __future__ import annotations

from anteroom.services.debug_diagnostics import DebugDiagnosticsCollector, sanitize_diagnostic_text


class _Clock:
    def __init__(self) -> None:
        self.value = 100.0
        self.wall = 0

    def monotonic(self) -> float:
        current = self.value
        self.value += 0.5
        return current

    def wall_clock(self) -> str:
        self.wall += 1
        return f"2026-04-25T00:00:0{self.wall}.000Z"


def test_debug_summary_tracks_phases_tools_usage_and_stop_reason() -> None:
    clock = _Clock()
    collector = DebugDiagnosticsCollector(
        provider="openai",
        model="gpt-test",
        turn_id="cli_abc123",
        interface="cli",
        conversation_id="conv-1",
        clock=clock.monotonic,
        wall_clock=clock.wall_clock,
    )

    collector.observe("phase", {"phase": "connecting", "attempt": 1, "max_attempts": 2})
    collector.observe("phase", {"phase": "waiting", "elapsed_seconds": 1.25})
    collector.observe("retrying", {"attempt": 2, "max_attempts": 2, "delay": 1.0, "reason": "transient_error"})
    collector.observe("tool_call_start", {"id": "tc-1", "tool_name": "bash", "arguments": {"command": "secret"}})
    collector.observe(
        "tool_call_end",
        {"id": "tc-1", "tool_name": "bash", "status": "success", "output": {"stdout": "secret output"}},
    )
    collector.observe("usage", {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15})
    collector.observe("done", {"stop_reason": "completed"})

    summary = collector.finish()

    assert summary["stop_reason"] == "completed"
    assert summary["version"] == 2
    assert summary["turn_id"] == "cli_abc123"
    assert summary["request_id"] == "cli_abc123"
    assert summary["interface"] == "cli"
    assert summary["conversation_id"] == "conv-1"
    assert summary["model"] == {"provider": "openai", "name": "gpt-test"}
    assert summary["usage"]["total_tokens"] == 15
    assert [phase["phase"] for phase in summary["phases"][:3]] == ["connecting", "waiting", "retrying"]
    assert summary["retries"][0]["attempt"] == 2
    assert summary["tools"][0]["name"] == "bash"
    assert summary["tools"][0]["status"] == "success"
    assert summary["tools"][0]["argument_shape"] == {"type": "object", "keys": ["command"], "key_count": 1}


def test_debug_summary_omits_raw_tokens_tool_arguments_and_outputs() -> None:
    collector = DebugDiagnosticsCollector(provider="openai", model="gpt-test")
    secret_prompt = "sk-testsecret1234567890"
    raw_args = {"command": f"echo {secret_prompt}", "password": "hunter2"}
    raw_output = {"stdout": f"token={secret_prompt}", "stderr": "<script>alert(1)</script>"}

    collector.observe("token", {"content": f"raw token {secret_prompt}"})
    collector.observe("tool_call_start", {"id": "tc-1", "tool_name": "bash", "arguments": raw_args})
    collector.observe("tool_call_end", {"id": "tc-1", "tool_name": "bash", "status": "error", "output": raw_output})
    collector.observe("assistant_message", {"content": f"assistant said {secret_prompt}"})
    collector.observe("error", {"code": "provider_error", "message": f"failed with {secret_prompt}"})

    rendered = str(collector.finish("error"))

    assert secret_prompt not in rendered
    assert "hunter2" not in rendered
    assert "raw token" not in rendered
    assert "echo" not in rendered
    assert "alert(1)" not in rendered
    assert "raw_tool_arguments': 'omitted" in rendered
    assert "raw_tool_output': 'omitted" in rendered


def test_debug_summary_tracks_active_tool_on_terminal_error() -> None:
    collector = DebugDiagnosticsCollector()
    collector.observe(
        "tool_call_start",
        {
            "id": "tc-active",
            "tool_name": "read_file",
            "arguments": {"path": "a.py"},
            "timeout_seconds": 30,
        },
    )
    collector.observe(
        "error",
        {
            "code": "timeout",
            "message": "stream timed out",
            "timeout_type": "stream_stall",
            "elapsed_seconds": 30.4,
            "timeout_seconds": 30,
        },
    )

    summary = collector.finish("timeout")

    assert summary["stop_reason"] == "timeout"
    assert summary["active_tools"][0]["id"] == "tc-active"
    assert summary["active_tools"][0]["status"] == "running"
    assert summary["active_tools"][0]["timeout_seconds"] == 30
    assert summary["errors"][0]["timeout_type"] == "stream_stall"
    assert summary["errors"][0]["elapsed_seconds"] == 30.4


def test_public_diagnostic_sanitizer_redacts_secret_patterns() -> None:
    rendered = sanitize_diagnostic_text("api_key=supersecret Authorization: Bearer abc123", max_chars=200)

    assert "supersecret" not in rendered
    assert "Bearer abc123" not in rendered
    assert "[redacted]" in rendered


def test_debug_summary_preserves_richer_compaction_metadata() -> None:
    collector = DebugDiagnosticsCollector(turn_id="web_1", interface="web")

    collector.observe(
        "compaction",
        {
            "reason": "context_error_recovery",
            "strategy": "drop_old_turn_groups",
            "estimated_tokens": 125000,
            "message_count": 90,
            "new_message_count": 12,
            "message_threshold": 80,
            "token_threshold": 100000,
            "messages_compacted": 78,
            "tail_preserved": 10,
            "dropped_messages": 8,
            "bytes_saved": 4096,
            "in_memory_only": True,
            "no_op": False,
        },
    )

    event = collector.finish("completed")["runtime_events"][0]

    assert event["kind"] == "compaction"
    assert event["strategy"] == "drop_old_turn_groups"
    assert event["estimated_tokens"] == 125000
    assert event["message_threshold"] == 80
    assert event["messages_compacted"] == 78
    assert event["tail_preserved"] == 10
    assert event["in_memory_only"] is True


def test_debug_snapshot_is_redacted_and_live() -> None:
    clock = _Clock()
    collector = DebugDiagnosticsCollector(
        turn_id="web_live",
        interface="web",
        clock=clock.monotonic,
        wall_clock=clock.wall_clock,
    )
    secret = "sk-testsecret1234567890"

    collector.observe("phase", {"phase": "waiting", "timeout_seconds": 10, "timeout_type": "first_token"})
    collector.observe("tool_call_start", {"id": "tc-1", "tool_name": "bash", "arguments": {"command": secret}})

    snapshot = collector.snapshot()
    rendered = str(snapshot)

    assert snapshot["turn_id"] == "web_live"
    assert snapshot["current_phase"]["phase"] == "tool_exec"
    assert snapshot["current_phase"]["age_seconds"] is not None
    assert snapshot["active_tools"][0]["argument_shape"] == {"type": "object", "keys": ["command"], "key_count": 1}
    assert secret not in rendered
    assert snapshot["redaction"]["raw_messages"] == "omitted"
