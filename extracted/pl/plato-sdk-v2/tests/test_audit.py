"""Tests for the filesystem audit log parser and JSONL spooling."""

from __future__ import annotations

from pathlib import Path

import pytest

from plato.chronos.models import AttributionKind, AuditEventInput, Operation
from plato.utils.audit import (
    AuditScopeContext,
    audit_ignore_filter,
    audit_spool_path,
    build_audit_key,
    load_audit_ignore,
    merge_audit_jsonl,
    new_audit_run_id,
    parse_audit_raw,
    read_audit_records,
    write_audit_jsonl,
)
from plato.utils.audit_resolution import resolve_audit_events_for_scope
from plato.utils.tool_execution import ToolExecutionRecord, ToolExecutionStatus

_has_auparse: bool
try:
    import auparse  # noqa: F401

    _has_auparse = True
except ImportError:
    _has_auparse = False

needs_auparse = pytest.mark.skipif(not _has_auparse, reason="python3-audit (auparse) not available")

# Raw ausearch output samples (ausearch --format raw)
_SAMPLE_RAW_OPEN_DELETE = """\
type=SYSCALL msg=audit(1709985600.100:100): arch=c000003e syscall=257 success=yes exit=3 a0=ffffff9c a1=7ffd0000 a2=241 a3=1b6 items=2 ppid=1000 pid=1001 auid=1000 uid=1000 gid=1000 euid=1000 suid=1000 fsuid=1000 egid=1000 sgid=1000 fsgid=1000 tty=(none) ses=1 comm="python3" exe="/usr/bin/python3" subj=kernel key="plato_workspace"
type=CWD msg=audit(1709985600.100:100): cwd="/workspace/code"
type=PATH msg=audit(1709985600.100:100): item=0 name="/workspace/code" inode=1 dev=00:25 mode=040777 ouid=1000 ogid=1000 rdev=00:00 obj=unlabeled nametype=PARENT cap_fp=0 cap_fi=0 cap_fe=0 cap_fver=0 cap_frootid=0
type=PATH msg=audit(1709985600.100:100): item=1 name="main.py" inode=2 dev=00:25 mode=0100644 ouid=1000 ogid=1000 rdev=00:00 obj=unlabeled nametype=CREATE cap_fp=0 cap_fi=0 cap_fe=0 cap_fver=0 cap_frootid=0
type=PROCTITLE msg=audit(1709985600.100:100): proctitle=707974686F6E33

type=SYSCALL msg=audit(1709985601.200:101): arch=c000003e syscall=263 success=yes exit=0 a0=ffffff9c a1=7ffd0000 a2=0 a3=0 items=2 ppid=1000 pid=1001 auid=1000 uid=1000 gid=1000 euid=1000 suid=1000 fsuid=1000 egid=1000 sgid=1000 fsgid=1000 tty=(none) ses=1 comm="rm" exe="/usr/bin/rm" subj=kernel key="plato_workspace"
type=CWD msg=audit(1709985601.200:101): cwd="/workspace/code"
type=PATH msg=audit(1709985601.200:101): item=0 name="/workspace/code" inode=1 dev=00:25 mode=040777 ouid=1000 ogid=1000 rdev=00:00 obj=unlabeled nametype=PARENT cap_fp=0 cap_fi=0 cap_fe=0 cap_fver=0 cap_frootid=0
type=PATH msg=audit(1709985601.200:101): item=1 name="old.py" inode=3 dev=00:25 mode=0100644 ouid=1000 ogid=1000 rdev=00:00 obj=unlabeled nametype=DELETE cap_fp=0 cap_fi=0 cap_fe=0 cap_fver=0 cap_frootid=0
type=PROCTITLE msg=audit(1709985601.200:101): proctitle=726D
"""

_SAMPLE_RAW_RENAME = """\
type=SYSCALL msg=audit(1709985602.300:102): arch=c000003e syscall=264 success=yes exit=0 a0=ffffff9c a1=7ffd0000 a2=ffffff9c a3=7ffd0001 items=4 ppid=1000 pid=1001 auid=1000 uid=1000 gid=1000 euid=1000 suid=1000 fsuid=1000 egid=1000 sgid=1000 fsgid=1000 tty=(none) ses=1 comm="mv" exe="/usr/bin/mv" subj=kernel key="plato_workspace"
type=CWD msg=audit(1709985602.300:102): cwd="/workspace/code"
type=PATH msg=audit(1709985602.300:102): item=0 name="/workspace/code" inode=1 dev=00:25 mode=040777 ouid=1000 ogid=1000 rdev=00:00 obj=unlabeled nametype=PARENT cap_fp=0 cap_fi=0 cap_fe=0 cap_fver=0 cap_frootid=0
type=PATH msg=audit(1709985602.300:102): item=1 name="/workspace/code" inode=1 dev=00:25 mode=040777 ouid=1000 ogid=1000 rdev=00:00 obj=unlabeled nametype=PARENT cap_fp=0 cap_fi=0 cap_fe=0 cap_fver=0 cap_frootid=0
type=PATH msg=audit(1709985602.300:102): item=2 name="old_name.py" inode=4 dev=00:25 mode=0100644 ouid=1000 ogid=1000 rdev=00:00 obj=unlabeled nametype=DELETE cap_fp=0 cap_fi=0 cap_fe=0 cap_fver=0 cap_frootid=0
type=PATH msg=audit(1709985602.300:102): item=3 name="new_name.py" inode=4 dev=00:25 mode=0100644 ouid=1000 ogid=1000 rdev=00:00 obj=unlabeled nametype=CREATE cap_fp=0 cap_fi=0 cap_fe=0 cap_fver=0 cap_frootid=0
type=PROCTITLE msg=audit(1709985602.300:102): proctitle=6D76
"""

_SAMPLE_RAW_MKDIR = """\
type=SYSCALL msg=audit(1709985603.400:103): arch=c000003e syscall=83 success=yes exit=0 a0=7ffd0000 a1=1ff a2=0 a3=0 items=2 ppid=1000 pid=1001 auid=0 uid=0 gid=0 euid=0 suid=0 fsuid=0 egid=0 sgid=0 fsgid=0 tty=(none) ses=1 comm="mkdir" exe="/usr/bin/mkdir" subj=kernel key="plato_workspace"
type=CWD msg=audit(1709985603.400:103): cwd="/workspace/code"
type=PATH msg=audit(1709985603.400:103): item=0 name="/workspace/code" inode=1 dev=00:25 mode=040777 ouid=1000 ogid=1000 rdev=00:00 obj=unlabeled nametype=PARENT cap_fp=0 cap_fi=0 cap_fe=0 cap_fver=0 cap_frootid=0
type=PATH msg=audit(1709985603.400:103): item=1 name="src" inode=5 dev=00:25 mode=040755 ouid=1000 ogid=1000 rdev=00:00 obj=unlabeled nametype=CREATE cap_fp=0 cap_fi=0 cap_fe=0 cap_fver=0 cap_frootid=0
type=PROCTITLE msg=audit(1709985603.400:103): proctitle=6D6B646972
"""

_SAMPLE_RAW_FAILED = """\
type=SYSCALL msg=audit(1709985604.500:104): arch=c000003e syscall=257 success=no exit=-13 a0=ffffff9c a1=7ffd0000 a2=0 a3=0 items=1 ppid=1000 pid=1001 auid=1000 uid=1000 gid=1000 euid=1000 suid=1000 fsuid=1000 egid=1000 sgid=1000 fsgid=1000 tty=(none) ses=1 comm="python3" exe="/usr/bin/python3" subj=kernel key="plato_workspace"
type=CWD msg=audit(1709985604.500:104): cwd="/workspace/code"
type=PATH msg=audit(1709985604.500:104): item=0 name="nope.py" inode=6 dev=00:25 mode=0100644 ouid=1000 ogid=1000 rdev=00:00 obj=unlabeled nametype=NORMAL cap_fp=0 cap_fi=0 cap_fe=0 cap_fver=0 cap_frootid=0
type=PROCTITLE msg=audit(1709985604.500:104): proctitle=707974686F6E33
"""

_SAMPLE_RAW_NON_FILESYSTEM = """\
type=CONFIG_CHANGE msg=audit(1709985605.600:105): auid=0 ses=1 subj=kernel op=add_rule key="plato_workspace" list=4 res=1
type=SYSCALL msg=audit(1709985605.600:105): arch=c000003e syscall=321 success=yes exit=0 a0=5 a1=7ffd0000 a2=0 a3=0 items=0 ppid=1000 pid=1001 auid=0 uid=0 gid=0 euid=0 suid=0 fsuid=0 egid=0 sgid=0 fsgid=0 tty=(none) ses=1 comm="auditctl" exe="/sbin/auditctl" subj=kernel key=(null)
type=PROCTITLE msg=audit(1709985605.600:105): proctitle=61756469746374
"""

_SAMPLE_RAW_ABSOLUTE_PATH = """\
type=SYSCALL msg=audit(1709985606.700:106): arch=c000003e syscall=257 success=yes exit=3 a0=ffffff9c a1=7ffd0000 a2=241 a3=1b6 items=2 ppid=1000 pid=1001 auid=1000 uid=1000 gid=1000 euid=1000 suid=1000 fsuid=1000 egid=1000 sgid=1000 fsgid=1000 tty=(none) ses=1 comm="bash" exe="/usr/bin/bash" subj=kernel key="plato_workspace"
type=CWD msg=audit(1709985606.700:106): cwd="/"
type=PATH msg=audit(1709985606.700:106): item=0 name="/workspace" inode=1 dev=00:25 mode=040777 ouid=1000 ogid=1000 rdev=00:00 obj=unlabeled nametype=PARENT cap_fp=0 cap_fi=0 cap_fe=0 cap_fver=0 cap_frootid=0
type=PATH msg=audit(1709985606.700:106): item=1 name="/workspace/abs_file.txt" inode=7 dev=00:25 mode=0100644 ouid=1000 ogid=1000 rdev=00:00 obj=unlabeled nametype=CREATE cap_fp=0 cap_fi=0 cap_fe=0 cap_fver=0 cap_frootid=0
type=PROCTITLE msg=audit(1709985606.700:106): proctitle=62617368
"""


@needs_auparse
class TestParseAuditRaw:
    """Tests for parse_audit_raw."""

    def test_parse_basic(self) -> None:
        """Parse sample raw output and verify events."""
        events = list(parse_audit_raw(_SAMPLE_RAW_OPEN_DELETE))
        assert len(events) == 2
        assert isinstance(events[0], AuditEventInput)
        assert events[0].operation == Operation.opened_file
        assert events[0].path == "/workspace/code/main.py"
        assert events[0].exe == "/usr/bin/python3"
        assert events[0].pid == 1001
        assert events[0].ppid == 1000
        assert events[0].comm == "python3"
        assert events[1].operation == Operation.deleted
        assert events[1].path == "/workspace/code/old.py"

    def test_parse_rename(self) -> None:
        """Rename events should preserve both old and new paths."""
        events = list(parse_audit_raw(_SAMPLE_RAW_RENAME))
        assert len(events) == 1
        assert events[0].operation == Operation.renamed
        assert events[0].path == "/workspace/code/old_name.py"
        assert events[0].new_path == "/workspace/code/new_name.py"

    def test_parse_create_directory(self) -> None:
        """Directory creation has created-directory operation with full path."""
        events = list(parse_audit_raw(_SAMPLE_RAW_MKDIR))
        assert len(events) == 1
        assert events[0].operation == Operation.created_directory
        assert events[0].path == "/workspace/code/src"
        assert events[0].exe == "/usr/bin/mkdir"

    def test_parse_empty(self) -> None:
        """Empty or blank input returns no events."""
        assert list(parse_audit_raw("")) == []
        assert list(parse_audit_raw("   ")) == []

    def test_parse_filters_failures(self) -> None:
        """Failed operations are filtered out."""
        events = list(parse_audit_raw(_SAMPLE_RAW_FAILED))
        assert len(events) == 0

    def test_parse_filters_non_filesystem(self) -> None:
        """Non-filesystem actions like added-audit-rule are filtered out."""
        events = list(parse_audit_raw(_SAMPLE_RAW_NON_FILESYSTEM))
        assert len(events) == 0

    def test_timestamp_is_datetime(self) -> None:
        """Timestamp should be a timezone-aware datetime."""
        events = list(parse_audit_raw(_SAMPLE_RAW_OPEN_DELETE))
        ts = events[0].timestamp
        assert ts.tzinfo is not None
        assert ts.year == 2024
        assert ts.month == 3
        assert ts.day == 9

    def test_uid_parsed(self) -> None:
        """UID should be extracted from subject."""
        events = list(parse_audit_raw(_SAMPLE_RAW_OPEN_DELETE))
        assert events[0].uid == 1000

    def test_absolute_path_preserved(self) -> None:
        """Absolute paths in PATH records should be used directly."""
        events = list(parse_audit_raw(_SAMPLE_RAW_ABSOLUTE_PATH))
        assert len(events) == 1
        assert events[0].path == "/workspace/abs_file.txt"


def _make_test_events() -> list[AuditEventInput]:
    """Create test events without requiring auparse."""
    from datetime import datetime, timezone

    return [
        AuditEventInput(
            timestamp=datetime(2024, 3, 9, 16, 0, 0, tzinfo=timezone.utc),
            operation="opened-file",
            path="/workspace/code/main.py",
            exe="/usr/bin/python3",
            uid=1000,
        ),
        AuditEventInput(
            timestamp=datetime(2024, 3, 9, 16, 0, 1, tzinfo=timezone.utc),
            operation="deleted",
            path="/workspace/code/old.py",
            exe="/usr/bin/rm",
            uid=1000,
        ),
    ]


class TestWriteAndReadAuditDb:
    """Tests for JSONL write/read round-trip."""

    def test_write_and_read_audit_jsonl(self, tmp_path: Path) -> None:
        """Write events and read them back as typed records."""
        events = _make_test_events()

        ctx = AuditScopeContext(
            session_id="sess-123",
            step_name="step_1",
            agent_name="claude-code",
            display_name="Claude Code",
            agent_id="job-123",
            workspace_name="code",
            audit_run_id="run-123",
            audit_key="audit-key-123",
            trace_id="trace-abc",
            span_id="span-def",
        )
        jsonl_path = tmp_path / "audit.jsonl"
        write_audit_jsonl(jsonl_path, events, ctx)

        rows = read_audit_records(jsonl_path)
        assert len(rows) == 2
        assert rows[0].agent_name == "claude-code"
        assert rows[0].operation == Operation.opened_file
        assert rows[0].path == "/workspace/code/main.py"
        assert rows[0].metadata["audit_run_id"] == "run-123"
        assert rows[0].metadata["workspace_name"] == "code"
        assert rows[0].audit_run_id == "run-123"
        assert rows[0].agent_id == "job-123"

    def test_read_audit_records_nonexistent(self, tmp_path: Path) -> None:
        """Reading from a nonexistent spool returns empty list."""
        spool_path = tmp_path / "nonexistent.jsonl"
        assert read_audit_records(spool_path) == []

    def test_round_trip_preserves_process_fields(self, tmp_path: Path) -> None:
        """Spool round-trip should preserve pid / ppid / comm fields."""
        event = AuditEventInput(
            timestamp=_make_test_events()[0].timestamp,
            operation="opened-file",
            path="/workspace/code/main.py",
            exe="/usr/bin/python3",
            uid=1000,
            pid=1234,
            ppid=1200,
            comm="python3",
            agent_id="agent-1",
            tool_name="Read",
        )
        jsonl_path = tmp_path / "audit.jsonl"
        write_audit_jsonl(jsonl_path, [event], AuditScopeContext(workspace_name="code"))

        row = read_audit_records(jsonl_path)[0]
        assert row.pid == 1234
        assert row.ppid == 1200
        assert row.comm == "python3"
        assert row.tool_name == "Read"

        uploaded = row.to_audit_event_input()
        assert uploaded.pid == 1234
        assert uploaded.ppid == 1200
        assert uploaded.comm == "python3"
        assert uploaded.tool_name == "Read"


class TestMergeAuditDbs:
    """Tests for merging multiple audit spools."""

    def test_merge_audit_jsonl(self, tmp_path: Path) -> None:
        """Merge three JSONL files and verify combined count."""
        events = _make_test_events()

        spools: list[Path] = []
        for i in range(3):
            ctx = AuditScopeContext(agent_name=f"agent-{i}", workspace_name="code", audit_run_id=f"run-{i}")
            spool_path = tmp_path / f"audit_{i}.jsonl"
            write_audit_jsonl(spool_path, events, ctx)
            spools.append(spool_path)

        merged = tmp_path / "merged.jsonl"
        merge_audit_jsonl(spools, merged)

        rows = read_audit_records(merged)
        assert len(rows) == 6

        agent_names = {r.agent_name for r in rows}
        assert agent_names == {"agent-0", "agent-1", "agent-2"}


class TestAuditScopeContext:
    """Tests for audit scope IDs and spool layout."""

    def test_new_audit_run_id_is_unique(self) -> None:
        """Generated audit run IDs should be unique."""
        assert new_audit_run_id() != new_audit_run_id()

    def test_build_audit_key_is_stable_for_same_inputs(self) -> None:
        """Audit keys should be deterministic for the same run ID."""
        key_1 = build_audit_key("run-1")
        key_2 = build_audit_key("run-1")
        key_3 = build_audit_key("run-2")

        assert key_1 == key_2
        assert key_1 != key_3

    def test_context_generates_defaults(self) -> None:
        """Context should auto-populate audit_run_id and audit_key."""
        ctx = AuditScopeContext(agent_id="job-1", workspace_name="code")

        assert ctx.audit_run_id
        assert ctx.audit_key
        assert ctx.audit_key == build_audit_key(ctx.audit_run_id)

    def test_same_name_contexts_get_unique_scope_identity(self, tmp_path: Path) -> None:
        """Same-name agents should still receive unique spool identities."""
        ctx_1 = AuditScopeContext(agent_name="claude-code", workspace_name="code")
        ctx_2 = AuditScopeContext(agent_name="claude-code", workspace_name="code")

        assert ctx_1.audit_run_id != ctx_2.audit_run_id
        assert ctx_1.audit_key != ctx_2.audit_key
        assert audit_spool_path(tmp_path, ctx_1) != audit_spool_path(tmp_path, ctx_2)

    def test_audit_spool_path_layout(self, tmp_path: Path) -> None:
        """Spool paths should follow .plato/audit/<workspace>/<audit_run_id>.jsonl."""
        ctx = AuditScopeContext(workspace_name="code", audit_run_id="run-123")
        path = audit_spool_path(tmp_path, ctx)

        assert path == tmp_path / "audit" / "code" / "run-123.jsonl"


class TestAuditResolution:
    """Tests for resolving filesystem audit events to tool spans."""

    def test_resolves_by_pid(self) -> None:
        event = _make_test_events()[0].model_copy(update={"pid": 222})
        tool_record = ToolExecutionRecord(
            trace_id="tool-trace",
            span_id="tool-span",
            tool_name="run_shell_command",
            started_at=event.timestamp.replace(microsecond=0),
            ended_at=event.timestamp.replace(microsecond=0, second=event.timestamp.second + 1),
            status=ToolExecutionStatus.COMPLETED,
            pid=222,
        )

        resolved = resolve_audit_events_for_scope(
            [event],
            scope_context=AuditScopeContext(
                trace_id="agent-trace",
                span_id="agent-span",
                agent_id="agent-1",
                agent_name="claude-code",
                display_name="Claude Code",
                workspace_name="code",
                audit_run_id="run-123",
            ),
            tool_records=[tool_record],
        )

        assert resolved[0].trace_id == "tool-trace"
        assert resolved[0].span_id == "tool-span"
        assert resolved[0].tool_name == "run_shell_command"
        assert resolved[0].attribution_kind == AttributionKind.pid

    def test_resolves_by_time_window_when_unique(self) -> None:
        event = _make_test_events()[0]
        tool_record = ToolExecutionRecord(
            trace_id="tool-trace",
            span_id="tool-span",
            tool_name="Read",
            started_at=event.timestamp.replace(microsecond=0),
            ended_at=event.timestamp.replace(microsecond=0, second=event.timestamp.second + 1),
            status=ToolExecutionStatus.COMPLETED,
            path_hints=["main.py"],
            working_directory="/workspace/code",
        )

        resolved = resolve_audit_events_for_scope(
            [event],
            scope_context=AuditScopeContext(
                trace_id="agent-trace",
                span_id="agent-span",
                agent_id="agent-1",
                agent_name="claude-code",
                display_name="Claude Code",
                workspace_name="code",
                audit_run_id="run-123",
            ),
            tool_records=[tool_record],
        )

        assert resolved[0].trace_id == "tool-trace"
        assert resolved[0].span_id == "tool-span"
        assert resolved[0].tool_name == "Read"
        assert resolved[0].attribution_kind == AttributionKind.time_window

    def test_falls_back_to_agent_span_when_ambiguous(self) -> None:
        event = _make_test_events()[0]
        first_record = ToolExecutionRecord(
            trace_id="tool-trace-1",
            span_id="tool-span-1",
            tool_name="Read",
            started_at=event.timestamp.replace(microsecond=0),
            ended_at=event.timestamp.replace(microsecond=0, second=event.timestamp.second + 1),
            status=ToolExecutionStatus.COMPLETED,
        )
        second_record = ToolExecutionRecord(
            trace_id="tool-trace-2",
            span_id="tool-span-2",
            tool_name="Read",
            started_at=event.timestamp.replace(microsecond=0),
            ended_at=event.timestamp.replace(microsecond=0, second=event.timestamp.second + 1),
            status=ToolExecutionStatus.COMPLETED,
        )

        resolved = resolve_audit_events_for_scope(
            [event],
            scope_context=AuditScopeContext(
                trace_id="agent-trace",
                span_id="agent-span",
                agent_id="agent-1",
                agent_name="claude-code",
                display_name="Claude Code",
                workspace_name="code",
                audit_run_id="run-123",
            ),
            tool_records=[first_record, second_record],
        )

        # Event is duplicated across both overlapping tool spans
        assert len(resolved) == 2
        span_ids = {r.span_id for r in resolved}
        assert span_ids == {"tool-span-1", "tool-span-2"}
        assert all(r.attribution_kind == AttributionKind.time_window for r in resolved)

    def test_overlapping_windows_wide_and_narrow_picks_narrow(self) -> None:
        """A wide and narrow overlapping window: only the narrow one wins."""
        event = _make_test_events()[0]
        base = event.timestamp.replace(microsecond=0)

        wide = ToolExecutionRecord(
            trace_id="trace-wide",
            span_id="span-wide",
            tool_name="Bash",
            started_at=base,
            ended_at=base.replace(second=30),
            status=ToolExecutionStatus.COMPLETED,
        )
        narrow = ToolExecutionRecord(
            trace_id="trace-narrow",
            span_id="span-narrow",
            tool_name="Write",
            started_at=base,
            ended_at=base.replace(second=3),
            status=ToolExecutionStatus.COMPLETED,
        )

        resolved = resolve_audit_events_for_scope(
            [event],
            scope_context=AuditScopeContext(
                trace_id="agent-trace",
                span_id="agent-span",
                agent_id="agent-1",
                agent_name="claude-code",
                display_name="Claude Code",
                workspace_name="code",
                audit_run_id="run-123",
            ),
            tool_records=[wide, narrow],
        )

        assert len(resolved) == 1
        assert resolved[0].span_id == "span-narrow"
        assert resolved[0].attribution_kind == AttributionKind.time_window

    def test_overlapping_parallel_windows_duplicate_across_all(self) -> None:
        """Two tools with similar-duration overlapping windows: event appears under both."""
        event = _make_test_events()[0]
        base = event.timestamp.replace(microsecond=0)

        tool_a = ToolExecutionRecord(
            trace_id="trace-a",
            span_id="span-a",
            tool_name="Read",
            started_at=base,
            ended_at=base.replace(second=3),
            status=ToolExecutionStatus.COMPLETED,
        )
        tool_b = ToolExecutionRecord(
            trace_id="trace-b",
            span_id="span-b",
            tool_name="Read",
            started_at=base,
            ended_at=base.replace(second=4),
            status=ToolExecutionStatus.COMPLETED,
        )

        resolved = resolve_audit_events_for_scope(
            [event],
            scope_context=AuditScopeContext(
                trace_id="agent-trace",
                span_id="agent-span",
                agent_id="agent-1",
                agent_name="claude-code",
                display_name="Claude Code",
                workspace_name="code",
                audit_run_id="run-123",
            ),
            tool_records=[tool_a, tool_b],
        )

        assert len(resolved) == 2
        span_ids = {r.span_id for r in resolved}
        assert span_ids == {"span-a", "span-b"}
        assert all(r.attribution_kind == AttributionKind.time_window for r in resolved)

    def test_single_unique_window_match(self) -> None:
        """When only one tool's window contains the event, it gets that tool."""
        from datetime import datetime, timezone

        base = datetime(2024, 3, 9, 16, 0, 5, tzinfo=timezone.utc)
        event = AuditEventInput(
            timestamp=base,
            operation="opened-file",
            path="/workspace/code/file.py",
            exe="/usr/bin/python3",
            uid=1000,
        )

        early_tool = ToolExecutionRecord(
            trace_id="trace-early",
            span_id="span-early",
            tool_name="Read",
            started_at=base.replace(second=0),
            ended_at=base.replace(second=3),
            status=ToolExecutionStatus.COMPLETED,
        )
        matching_tool = ToolExecutionRecord(
            trace_id="trace-match",
            span_id="span-match",
            tool_name="Write",
            started_at=base.replace(second=4),
            ended_at=base.replace(second=10),
            status=ToolExecutionStatus.COMPLETED,
        )

        resolved = resolve_audit_events_for_scope(
            [event],
            scope_context=AuditScopeContext(
                trace_id="agent-trace",
                span_id="agent-span",
                agent_id="agent-1",
                agent_name="claude-code",
                display_name="Claude Code",
                workspace_name="code",
                audit_run_id="run-123",
            ),
            tool_records=[early_tool, matching_tool],
        )

        assert len(resolved) == 1
        assert resolved[0].span_id == "span-match"
        assert resolved[0].tool_name == "Write"
        assert resolved[0].attribution_kind == AttributionKind.time_window

    def test_cross_workspace_tool_resolves_for_both_scopes(self) -> None:
        """A single tool touching two workspaces should resolve for both scopes."""
        event_a = _make_test_events()[0].model_copy(update={"path": "/workspace/code-a/file.py"})
        event_b = _make_test_events()[0].model_copy(update={"path": "/workspace/code-b/file.py"})

        shared_tool = ToolExecutionRecord(
            trace_id="shared-trace",
            span_id="shared-span",
            tool_name="Bash",
            started_at=event_a.timestamp.replace(microsecond=0),
            ended_at=event_a.timestamp.replace(microsecond=0, second=event_a.timestamp.second + 5),
            status=ToolExecutionStatus.COMPLETED,
        )

        scope_ctx_a = AuditScopeContext(
            trace_id="agent-trace",
            span_id="agent-span",
            agent_id="agent-1",
            agent_name="claude-code",
            display_name="Claude Code",
            workspace_name="code-a",
            audit_run_id="run-123",
        )
        scope_ctx_b = AuditScopeContext(
            trace_id="agent-trace",
            span_id="agent-span",
            agent_id="agent-1",
            agent_name="claude-code",
            display_name="Claude Code",
            workspace_name="code-b",
            audit_run_id="run-123",
        )

        resolved_a = resolve_audit_events_for_scope(
            [event_a],
            scope_context=scope_ctx_a,
            tool_records=[shared_tool],
        )
        resolved_b = resolve_audit_events_for_scope(
            [event_b],
            scope_context=scope_ctx_b,
            tool_records=[shared_tool],
        )

        assert resolved_a[0].span_id == "shared-span"
        assert resolved_b[0].span_id == "shared-span"
        assert resolved_a[0].attribution_kind == AttributionKind.time_window
        assert resolved_b[0].attribution_kind == AttributionKind.time_window

    def test_parallel_tool_calls_attributed_by_pid(self) -> None:
        """Two concurrent tools with distinct PIDs get correct per-event attribution."""
        from datetime import datetime, timezone

        base = datetime(2024, 3, 9, 16, 0, 0, tzinfo=timezone.utc)

        tool_a = ToolExecutionRecord(
            trace_id="trace-a",
            span_id="span-a",
            tool_name="Bash",
            started_at=base,
            ended_at=base.replace(second=10),
            status=ToolExecutionStatus.COMPLETED,
            pid=100,
        )
        tool_b = ToolExecutionRecord(
            trace_id="trace-b",
            span_id="span-b",
            tool_name="Bash",
            started_at=base,
            ended_at=base.replace(second=10),
            status=ToolExecutionStatus.COMPLETED,
            pid=200,
        )

        event_from_a = AuditEventInput(
            timestamp=base.replace(second=3),
            operation="opened-file",
            path="/workspace/code/a.py",
            exe="/bin/bash",
            uid=1000,
            pid=100,
        )
        event_from_b = AuditEventInput(
            timestamp=base.replace(second=5),
            operation="opened-file",
            path="/workspace/code/b.py",
            exe="/bin/bash",
            uid=1000,
            pid=200,
        )

        scope_ctx = AuditScopeContext(
            trace_id="agent-trace",
            span_id="agent-span",
            agent_id="agent-1",
            agent_name="claude-code",
            display_name="Claude Code",
            workspace_name="code",
            audit_run_id="run-1",
        )

        resolved = resolve_audit_events_for_scope(
            [event_from_a, event_from_b],
            scope_context=scope_ctx,
            tool_records=[tool_a, tool_b],
        )

        assert resolved[0].span_id == "span-a"
        assert resolved[0].attribution_kind == AttributionKind.pid
        assert resolved[1].span_id == "span-b"
        assert resolved[1].attribution_kind == AttributionKind.pid

    def test_parallel_tools_no_pid_duplicated_across_all(self) -> None:
        """Two concurrent tools without PID: event appears under both."""
        from datetime import datetime, timezone

        base = datetime(2024, 3, 9, 16, 0, 0, tzinfo=timezone.utc)

        tool_read = ToolExecutionRecord(
            trace_id="trace-read",
            span_id="span-read",
            tool_name="Read",
            started_at=base,
            ended_at=base.replace(second=10),
            status=ToolExecutionStatus.COMPLETED,
        )
        tool_write = ToolExecutionRecord(
            trace_id="trace-write",
            span_id="span-write",
            tool_name="Write",
            started_at=base,
            ended_at=base.replace(second=10),
            status=ToolExecutionStatus.COMPLETED,
        )

        event = AuditEventInput(
            timestamp=base.replace(second=3),
            operation="opened-file",
            path="/workspace/code/config.yaml",
            exe="/usr/bin/python3",
            uid=1000,
        )

        scope_ctx = AuditScopeContext(
            trace_id="agent-trace",
            span_id="agent-span",
            agent_id="agent-1",
            agent_name="claude-code",
            display_name="Claude Code",
            workspace_name="code",
            audit_run_id="run-1",
        )

        resolved = resolve_audit_events_for_scope(
            [event],
            scope_context=scope_ctx,
            tool_records=[tool_read, tool_write],
        )

        assert len(resolved) == 2
        span_ids = {r.span_id for r in resolved}
        assert span_ids == {"span-read", "span-write"}
        assert all(r.attribution_kind == AttributionKind.time_window for r in resolved)


class TestAuditUploadPayload:
    """Verify the payload shape sent to the bulk ingest API."""

    def test_cross_workspace_upload_payloads_carry_correct_attribution(self, tmp_path: Path) -> None:
        """A tool touching two workspaces produces correct per-scope upload payloads."""
        from datetime import datetime, timezone

        base = datetime(2024, 3, 9, 16, 0, 0, tzinfo=timezone.utc)

        shared_tool = ToolExecutionRecord(
            trace_id="tool-trace",
            span_id="tool-span",
            tool_name="Bash",
            started_at=base,
            ended_at=base.replace(second=10),
            status=ToolExecutionStatus.COMPLETED,
            pid=300,
        )

        events_ws_a = [
            AuditEventInput(
                timestamp=base.replace(second=2),
                operation="opened-file",
                path="/workspace/alpha/file.py",
                exe="/bin/bash",
                uid=1000,
                pid=300,
            ),
        ]
        events_ws_b = [
            AuditEventInput(
                timestamp=base.replace(second=4),
                operation="opened-file",
                path="/workspace/beta/data.csv",
                exe="/bin/bash",
                uid=1000,
                pid=300,
            ),
        ]

        tool_records = [shared_tool]

        scope_a = AuditScopeContext(
            trace_id="run-trace",
            span_id="run-span",
            agent_id="agent-1",
            agent_name="claude-code",
            display_name="Claude Code",
            workspace_name="alpha",
            audit_run_id="run-1",
        )
        scope_b = AuditScopeContext(
            trace_id="run-trace",
            span_id="run-span",
            agent_id="agent-1",
            agent_name="claude-code",
            display_name="Claude Code",
            workspace_name="beta",
            audit_run_id="run-1",
        )

        resolved_a = resolve_audit_events_for_scope(
            events_ws_a,
            scope_context=scope_a,
            tool_records=tool_records,
        )
        resolved_b = resolve_audit_events_for_scope(
            events_ws_b,
            scope_context=scope_b,
            tool_records=tool_records,
        )

        # Both scopes attribute to the same tool span
        assert resolved_a[0].trace_id == "tool-trace"
        assert resolved_a[0].span_id == "tool-span"
        assert resolved_a[0].tool_name == "Bash"
        assert resolved_a[0].attribution_kind == AttributionKind.pid

        assert resolved_b[0].trace_id == "tool-trace"
        assert resolved_b[0].span_id == "tool-span"
        assert resolved_b[0].tool_name == "Bash"
        assert resolved_b[0].attribution_kind == AttributionKind.pid

        # Verify payload shape matches BulkRefAuditEventsRequest
        from plato.chronos.models import BulkRefAuditEventsRequest

        payload_a = BulkRefAuditEventsRequest(events=resolved_a)
        payload_b = BulkRefAuditEventsRequest(events=resolved_b)

        dumped_a = payload_a.model_dump()
        dumped_b = payload_b.model_dump()

        assert len(dumped_a["events"]) == 1
        assert dumped_a["events"][0]["tool_name"] == "Bash"
        assert dumped_a["events"][0]["span_id"] == "tool-span"
        assert dumped_a["events"][0]["attribution_kind"] == AttributionKind.pid
        assert dumped_a["events"][0]["path"] == "/workspace/alpha/file.py"

        assert len(dumped_b["events"]) == 1
        assert dumped_b["events"][0]["tool_name"] == "Bash"
        assert dumped_b["events"][0]["span_id"] == "tool-span"
        assert dumped_b["events"][0]["attribution_kind"] == AttributionKind.pid
        assert dumped_b["events"][0]["path"] == "/workspace/beta/data.csv"

    def test_parallel_tools_produce_distinct_payloads(self) -> None:
        """Parallel tool calls produce events with distinct tool spans in the upload payload."""
        from datetime import datetime, timezone

        base = datetime(2024, 3, 9, 16, 0, 0, tzinfo=timezone.utc)

        tool_a = ToolExecutionRecord(
            trace_id="trace-a",
            span_id="span-a",
            tool_name="Read",
            started_at=base,
            ended_at=base.replace(second=5),
            status=ToolExecutionStatus.COMPLETED,
            pid=100,
        )
        tool_b = ToolExecutionRecord(
            trace_id="trace-b",
            span_id="span-b",
            tool_name="Write",
            started_at=base.replace(second=1),
            ended_at=base.replace(second=6),
            status=ToolExecutionStatus.COMPLETED,
            pid=200,
        )

        events = [
            AuditEventInput(
                timestamp=base.replace(second=2),
                operation="opened-file",
                path="/workspace/code/input.txt",
                exe="/bin/cat",
                uid=1000,
                pid=100,
            ),
            AuditEventInput(
                timestamp=base.replace(second=3),
                operation="opened-file",
                path="/workspace/code/output.txt",
                exe="/usr/bin/python3",
                uid=1000,
                pid=200,
            ),
            AuditEventInput(
                timestamp=base.replace(second=4),
                operation="opened-file",
                path="/workspace/code/log.txt",
                exe="/bin/bash",
                uid=1000,
            ),
        ]

        scope_ctx = AuditScopeContext(
            trace_id="run-trace",
            span_id="run-span",
            agent_id="agent-1",
            agent_name="claude-code",
            display_name="Claude Code",
            workspace_name="code",
            audit_run_id="run-1",
        )

        resolved = resolve_audit_events_for_scope(
            events,
            scope_context=scope_ctx,
            tool_records=[tool_a, tool_b],
        )

        from plato.chronos.models import BulkRefAuditEventsRequest

        payload = BulkRefAuditEventsRequest(events=resolved)
        dumped = payload.model_dump()

        # 3 input events → 4 output events (third event duplicated across both tools)
        assert len(dumped["events"]) == 4

        # Event from pid=100 → tool_a
        assert dumped["events"][0]["span_id"] == "span-a"
        assert dumped["events"][0]["attribution_kind"] == AttributionKind.pid

        # Event from pid=200 → tool_b
        assert dumped["events"][1]["span_id"] == "span-b"
        assert dumped["events"][1]["attribution_kind"] == AttributionKind.pid

        # Event with no PID: duplicated across both overlapping tools
        no_pid_span_ids = {dumped["events"][2]["span_id"], dumped["events"][3]["span_id"]}
        assert no_pid_span_ids == {"span-a", "span-b"}
        assert dumped["events"][2]["attribution_kind"] == AttributionKind.time_window
        assert dumped["events"][3]["attribution_kind"] == AttributionKind.time_window


class TestAuditIgnore:
    """Tests for .auditignore loading and filtering."""

    def test_load_defaults_without_file(self, tmp_path: Path) -> None:
        """Without .auditignore file, still returns spec with default patterns (.git/)."""
        spec = load_audit_ignore(str(tmp_path))
        assert spec.match_file(".git/config")
        assert spec.match_file(".git/objects/abc123")
        assert not spec.match_file("main.py")

    def test_load_audit_ignore_merges_with_defaults(self, tmp_path: Path) -> None:
        """User patterns are merged with built-in defaults."""
        (tmp_path / ".auditignore").write_text("node_modules/\n*.pyc\n")
        spec = load_audit_ignore(str(tmp_path))
        # User patterns
        assert spec.match_file("node_modules/foo.js")
        assert spec.match_file("bar.pyc")
        # Default patterns still present
        assert spec.match_file(".git/HEAD")
        # Non-matching
        assert not spec.match_file("main.py")

    def test_audit_ignore_filter_drops_matching(self) -> None:
        """Filter removes events whose paths match the ignore spec."""
        events = _make_test_events()
        import pathspec

        spec = pathspec.PathSpec.from_lines("gitwildmatch", ["old.*"])
        result = list(audit_ignore_filter(iter(events), spec, workspace_prefix="/workspace/code"))
        assert len(result) == 1
        assert result[0].path == "/workspace/code/main.py"

    def test_audit_ignore_filter_drops_git_by_default(self) -> None:
        """Default ignore spec filters out .git/ paths."""
        from datetime import datetime, timezone

        events = [
            AuditEventInput(
                timestamp=datetime(2024, 3, 9, 16, 0, 0, tzinfo=timezone.utc),
                operation="opened-file",
                path="/workspace/code/.git/objects/abc123",
                exe="/usr/bin/git",
                uid=1000,
            ),
            AuditEventInput(
                timestamp=datetime(2024, 3, 9, 16, 0, 1, tzinfo=timezone.utc),
                operation="opened-file",
                path="/workspace/code/main.py",
                exe="/usr/bin/python3",
                uid=1000,
            ),
        ]
        import pathspec

        spec = pathspec.PathSpec.from_lines("gitwildmatch", [".git/"])
        result = list(audit_ignore_filter(iter(events), spec, workspace_prefix="/workspace/code"))
        assert len(result) == 1
        assert result[0].path == "/workspace/code/main.py"
