"""Filesystem audit log parsing and local JSONL spooling.

Parses Linux auditd logs via ``ausearch --format raw`` using the ``auparse``
library into structured events and stores them in JSONL spool files for later
upload to Chronos.
"""

from __future__ import annotations

import logging
import posixpath
from collections.abc import Iterator
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING
from uuid import uuid4

import pathspec
from pydantic import BaseModel, Field

from plato.chronos.models import AttributionKind, AuditEventInput, Operation

if TYPE_CHECKING:
    import auparse

logger = logging.getLogger(__name__)

_VALID_OPERATIONS = {op.value for op in Operation}


@dataclass
class AuditScopeContext:
    """Context for one audited workspace scope on one agent run."""

    session_id: str = ""
    step_name: str = ""
    agent_name: str = ""
    display_name: str = ""
    agent_id: str = ""
    workspace_name: str = ""
    audit_run_id: str = ""
    audit_key: str = ""
    trace_id: str = ""
    span_id: str = ""

    def __post_init__(self) -> None:
        if not self.audit_run_id:
            self.audit_run_id = new_audit_run_id()
        if not self.audit_key:
            self.audit_key = build_audit_key(self.audit_run_id)

    def to_event_metadata(self) -> dict[str, str]:
        """Scope metadata to persist alongside each event."""
        metadata: dict[str, str] = {}
        if self.session_id:
            metadata["session_id"] = self.session_id
        if self.step_name:
            metadata["step_name"] = self.step_name
        if self.agent_id:
            metadata["agent_id"] = self.agent_id
        if self.workspace_name:
            metadata["workspace_name"] = self.workspace_name
        if self.audit_run_id:
            metadata["audit_run_id"] = self.audit_run_id
        if self.audit_key:
            metadata["audit_key"] = self.audit_key
        return metadata


class AuditSpoolRecord(BaseModel):
    """Typed local JSONL spool record for one audited filesystem event."""

    timestamp: datetime
    operation: Operation
    path: str
    new_path: str | None = None
    size_bytes: int | None = None
    uid: int | None = None
    exe: str | None = None
    pid: int | None = None
    ppid: int | None = None
    comm: str | None = None
    trace_id: str | None = None
    span_id: str | None = None
    tool_name: str | None = None
    attribution_kind: AttributionKind | None = None
    agent_name: str | None = None
    display_name: str | None = None
    session_id: str | None = None
    step_name: str | None = None
    agent_id: str | None = None
    workspace_name: str | None = None
    audit_run_id: str | None = None
    audit_key: str | None = None
    metadata: dict[str, str] = Field(default_factory=dict)

    def to_audit_event_input(self) -> AuditEventInput:
        """Project the local spool record to the Chronos audit ingest shape."""
        return AuditEventInput(
            timestamp=self.timestamp,
            operation=self.operation,
            path=self.path,
            new_path=self.new_path,
            size_bytes=self.size_bytes,
            uid=self.uid,
            exe=self.exe,
            pid=self.pid,
            ppid=self.ppid,
            comm=self.comm,
            trace_id=self.trace_id,
            span_id=self.span_id,
            agent_id=self.agent_id,
            agent_name=self.agent_name,
            display_name=self.display_name,
            audit_run_id=self.audit_run_id,
            tool_name=self.tool_name,
            attribution_kind=self.attribution_kind,
            metadata=self.metadata or None,
        )


def new_audit_run_id() -> str:
    """Create a unique audit run ID suitable for filenames and audit scope keys."""
    return uuid4().hex


def build_audit_key(audit_run_id: str) -> str:
    """Build a deterministic Linux audit key for one scope."""
    return f"plato_{audit_run_id}"


def audit_spool_path(plato_dir: Path, context: AuditScopeContext) -> Path:
    """Return the JSONL spool path for an audit scope."""
    workspace_name = context.workspace_name or "unknown-workspace"
    return plato_dir / "audit" / workspace_name / f"{context.audit_run_id}.jsonl"


@dataclass
class ResolvedAuditPaths:
    """Resolved primary and secondary paths for one audit event."""

    path: str | None = None
    new_path: str | None = None


@dataclass
class ParsedSyscallInfo:
    """Process identity extracted from the SYSCALL record for one audit event."""

    pid: int | None = None
    ppid: int | None = None
    comm: str | None = None
    exe: str | None = None


def _make_absolute_path(name: str, parent_path: str | None, cwd: str | None) -> str:
    """Resolve one PATH record name into an absolute path when possible."""
    if posixpath.isabs(name):
        return name

    base = parent_path or cwd
    if base:
        return posixpath.join(base, name)

    return name


def _resolve_paths(au: auparse.AuParser) -> ResolvedAuditPaths:
    """Extract full paths from PATH records in the current auparse event.

    Rename syscalls carry both DELETE (old path) and CREATE (new path) PATH
    records. Other filesystem events typically carry one relevant target path.
    """
    cwd: str | None = None
    parent_paths: list[str] = []
    deleted_path: str | None = None
    created_path: str | None = None
    normal_path: str | None = None

    au.first_record()
    while True:
        rtype = au.get_type_name()

        if rtype == "CWD":
            if au.find_field("cwd"):
                cwd = au.interpret_field()

        elif rtype == "PATH":
            au.first_field()
            fields: dict[str, str] = {}
            while True:
                fields[au.get_field_name()] = au.interpret_field()
                if not au.next_field():
                    break

            nametype = fields.get("nametype", "")
            name = fields.get("name", "")

            if nametype == "PARENT":
                parent_paths.append(name)
            elif nametype == "DELETE":
                deleted_path = _make_absolute_path(
                    name,
                    parent_paths[0] if parent_paths else None,
                    cwd,
                )
            elif nametype == "CREATE":
                created_path = _make_absolute_path(
                    name,
                    parent_paths[-1] if parent_paths else None,
                    cwd,
                )
            elif nametype == "NORMAL":
                normal_path = _make_absolute_path(
                    name,
                    parent_paths[-1] if parent_paths else None,
                    cwd,
                )

        if not au.next_record():
            break

    if deleted_path and created_path:
        return ResolvedAuditPaths(path=deleted_path, new_path=created_path)

    return ResolvedAuditPaths(path=created_path or deleted_path or normal_path)


def _extract_syscall_info(au: auparse.AuParser) -> ParsedSyscallInfo:
    """Extract PID / PPID / command metadata from the current audit event."""
    syscall_info = ParsedSyscallInfo()

    au.first_record()
    while True:
        if au.get_type_name() == "SYSCALL":
            au.first_field()
            fields: dict[str, str] = {}
            while True:
                fields[au.get_field_name()] = au.interpret_field()
                if not au.next_field():
                    break

            for field_name in ("pid", "ppid"):
                field_value = fields.get(field_name)
                if field_value is None:
                    continue
                try:
                    setattr(syscall_info, field_name, int(field_value))
                except (TypeError, ValueError):
                    continue

            syscall_info.comm = fields.get("comm") or None
            syscall_info.exe = fields.get("exe") or None
            break

        if not au.next_record():
            break

    return syscall_info


def parse_audit_raw(raw_output: str) -> Iterator[AuditEventInput]:
    """Parse ``ausearch --format raw`` output into AuditEventInput objects.

    Yields events one at a time to avoid materialising the full list in memory
    (150K+ events can cause significant memory pressure on the world VM).

    Uses the ``auparse`` library (from ``python3-audit``) to parse raw audit
    log records. This handles event grouping, hex-encoded paths, and extracts
    full paths for all event types including ``created-directory`` (which
    ``ausearch --format csv`` omits from ``OBJ_PRIME``).
    """
    import auparse  # Imported at call time because the C extension may be built at runtime

    if not raw_output or not raw_output.strip():
        return

    au = auparse.AuParser(auparse.AUSOURCE_BUFFER, raw_output)

    while au.parse_next_event():
        au.aup_normalize(auparse.NORM_OPT_ALL)

        action = au.aup_normalize_get_action()
        if not action or action not in _VALID_OPERATIONS:
            continue

        if not au.aup_normalize_get_results():
            continue

        how = au.aup_normalize_how()
        ts = au.get_timestamp()
        timestamp = datetime.fromtimestamp(ts.sec + ts.milli / 1000, tz=UTC)

        # Get uid from subject
        uid: int | None = None
        if au.aup_normalize_subject_primary():
            uid_str = au.get_field_str()
            try:
                uid = int(uid_str)
            except (ValueError, TypeError):
                pass

        resolved_paths = _resolve_paths(au)
        syscall_info = _extract_syscall_info(au)
        if not resolved_paths.path:
            continue

        yield AuditEventInput(
            timestamp=timestamp,
            operation=action,
            path=resolved_paths.path,
            new_path=resolved_paths.new_path,
            exe=syscall_info.exe or how,
            uid=uid,
            pid=syscall_info.pid,
            ppid=syscall_info.ppid,
            comm=syscall_info.comm,
        )


def _event_to_record(
    event: AuditEventInput,
    context: AuditScopeContext | None = None,
) -> AuditSpoolRecord:
    """Convert an audit event to the JSONL record shape."""
    ctx = context or AuditScopeContext()
    metadata = dict(event.metadata or {})
    metadata.update(ctx.to_event_metadata())
    return AuditSpoolRecord(
        timestamp=event.timestamp,
        operation=event.operation,
        path=event.path,
        new_path=event.new_path,
        size_bytes=event.size_bytes,
        uid=event.uid,
        exe=event.exe,
        pid=event.pid,
        ppid=event.ppid,
        comm=event.comm,
        trace_id=event.trace_id or ctx.trace_id or None,
        span_id=event.span_id or ctx.span_id or None,
        tool_name=event.tool_name,
        attribution_kind=event.attribution_kind,
        agent_name=event.agent_name or ctx.agent_name or None,
        display_name=event.display_name or ctx.display_name or None,
        step_name=ctx.step_name or None,
        session_id=ctx.session_id or None,
        agent_id=event.agent_id or ctx.agent_id or None,
        workspace_name=ctx.workspace_name or None,
        audit_run_id=event.audit_run_id or ctx.audit_run_id or None,
        audit_key=ctx.audit_key or None,
        metadata=metadata,
    )


_DEFAULT_AUDIT_IGNORE_PATTERNS = [
    ".git/",
]


def load_audit_ignore(workspace_path: str) -> pathspec.PathSpec:
    """Load a ``.auditignore`` file from a workspace directory.

    Always includes built-in default patterns (e.g. ``.git/``) even when no
    ``.auditignore`` file exists. User patterns from the file are appended
    after the defaults.
    """
    lines = list(_DEFAULT_AUDIT_IGNORE_PATTERNS)
    ignore_file = Path(workspace_path) / ".auditignore"
    if ignore_file.is_file():
        lines.extend(ignore_file.read_text(encoding="utf-8").splitlines())
        logger.debug(
            "Loaded .auditignore from %s (%d user patterns)",
            workspace_path,
            len(lines) - len(_DEFAULT_AUDIT_IGNORE_PATTERNS),
        )
    spec = pathspec.PathSpec.from_lines("gitwildmatch", lines)
    return spec


def audit_ignore_filter(
    events: Iterator[AuditEventInput],
    ignore_spec: pathspec.PathSpec,
    workspace_prefix: str | None = None,
) -> Iterator[AuditEventInput]:
    """Filter audit events through an auditignore spec, yielding non-ignored events."""
    prefix = (workspace_prefix.rstrip("/") + "/") if workspace_prefix else ""
    for event in events:
        rel = event.path[len(prefix) :] if prefix and event.path.startswith(prefix) else event.path
        if ignore_spec.match_file(rel):
            continue
        yield event


def write_audit_jsonl(
    jsonl_path: Path,
    events: list[AuditEventInput],
    context: AuditScopeContext | None = None,
) -> None:
    """Write audit events to a JSONL spool file."""
    jsonl_path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with jsonl_path.open("w", encoding="utf-8") as f:
        for event in events:
            f.write(_event_to_record(event, context).model_dump_json())
            f.write("\n")
            count += 1
    logger.info("Wrote %d audit events to %s", count, jsonl_path)


def read_audit_records(spool_path: Path) -> list[AuditSpoolRecord]:
    """Read all audit spool records from a JSONL spool file."""
    if not spool_path.exists():
        return []
    events: list[AuditSpoolRecord] = []
    with spool_path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            events.append(AuditSpoolRecord.model_validate_json(line))
    return events


def merge_audit_jsonl(source_paths: list[Path], target_path: Path) -> None:
    """Merge multiple JSONL spool files into one."""
    target_path.parent.mkdir(parents=True, exist_ok=True)
    with target_path.open("w", encoding="utf-8") as out:
        for source in source_paths:
            if not source.exists():
                continue
            with source.open(encoding="utf-8") as src:
                for line in src:
                    if line.strip():
                        out.write(line if line.endswith("\n") else line + "\n")
    logger.info("Merged %d audit spools into %s", len(source_paths), target_path)
