"""Privacy-aware diagnostic collection and portable bug-report bundles."""

import base64
import contextlib
import hashlib
import io
import json
import os
import platform
import re
import typing as t
import zipfile
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath

from dreadnode.app import paths
from dreadnode.core.log import LogEntry
from dreadnode.version import VERSION

MAX_BUNDLE_BYTES = 2 * 1024 * 1024
MAX_CATEGORY_BYTES = 384 * 1024
MAX_TOTAL_CONTENT_BYTES = 1536 * 1024

_REDACTED = "[REDACTED]"
_SECRET_ASSIGNMENT_RE = re.compile(
    r"""(?ix)
    (?P<prefix>
        ["']?\b
        (?:[a-z0-9]+[_-])*
        (?:authorization|proxy-authorization|x-api-key|api[_-]?key|
           access[_-]?token|refresh[_-]?token|id[_-]?token|password|
           passwd|client[_-]?secret|secret)
        \b["']?\s*[=:]\s*
    )
    (?:
        (?P<double_quote>") (?:\\.|[^"\\\r\n])* "
        |
        (?P<single_quote>') (?:\\.|[^'\\\r\n])* '
        |
        (?:Bearer\s+)?[^\s,;}\]"']+
    )
    """
)
_BEARER_RE = re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/=-]+")
_KNOWN_TOKEN_RE = re.compile(
    r"\b(?:sk-[A-Za-z0-9_-]{12,}|dn_[A-Za-z0-9_-]{12,}|"
    r"ghp_[A-Za-z0-9]{12,}|github_pat_[A-Za-z0-9_]{12,}|"
    r"xox[baprs]-[A-Za-z0-9-]{12,})\b"
)
_URL_CREDENTIAL_RE = re.compile(r"(?i)(https?://[^\s/:@]+:)([^\s@]+)(@)")


def redact_sensitive_text(value: str) -> str:
    """Redact common credentials without dumping or inspecting environment state."""

    def redact_assignment(match: re.Match[str]) -> str:
        quote = match.group("double_quote") or match.group("single_quote") or ""
        return f"{match.group('prefix')}{quote}{_REDACTED}{quote}"

    value = _SECRET_ASSIGNMENT_RE.sub(redact_assignment, value)
    value = _BEARER_RE.sub(f"Bearer {_REDACTED}", value)
    value = _KNOWN_TOKEN_RE.sub(_REDACTED, value)
    return _URL_CREDENTIAL_RE.sub(
        lambda match: f"{match.group(1)}{_REDACTED}{match.group(3)}", value
    )


@dataclass(frozen=True, slots=True)
class BugReportDraft:
    """Customer-authored fields collected by the report form."""

    title: str
    steps_to_reproduce: str
    expected_result: str
    actual_result: str
    additional_context: str = ""
    contact_consent: bool = False

    def description(self) -> str:
        """Render the report body shared by the bundle and platform submission."""

        sections = [
            ("Steps to reproduce", self.steps_to_reproduce),
            ("Expected result", self.expected_result),
            ("Actual result", self.actual_result),
        ]
        if self.additional_context.strip():
            sections.append(("Additional context", self.additional_context))
        return "\n\n".join(f"## {heading}\n\n{body.strip()}" for heading, body in sections)


@dataclass(frozen=True, slots=True)
class BugReportContext:
    """Safe runtime metadata captured without serializing raw environment state."""

    runtime_mode: str
    deployment_mode: str
    active_screen: str
    session_id: str | None
    agent: str | None
    model: str | None
    capabilities: tuple[tuple[str, str | None], ...] = ()
    runtime_version: str | None = None
    terminal: str | None = None
    term_program: str | None = None
    ssh: bool = False
    multiplexer: str | None = None

    @classmethod
    def collect(
        cls,
        *,
        runtime_mode: str,
        deployment_mode: str = "unknown",
        active_screen: str,
        session_id: str | None,
        agent: str | None,
        model: str | None,
        capabilities: t.Iterable[tuple[str, str | None]],
        runtime_version: str | None = None,
    ) -> "BugReportContext":
        """Collect allowlisted platform and terminal indicators."""

        multiplexer = None
        if os.environ.get("TMUX"):
            multiplexer = "tmux"
        elif os.environ.get("STY"):
            multiplexer = "screen"
        return cls(
            runtime_mode=runtime_mode,
            deployment_mode=deployment_mode,
            active_screen=active_screen,
            session_id=session_id,
            agent=agent,
            model=model,
            capabilities=tuple(capabilities),
            runtime_version=runtime_version,
            terminal=os.environ.get("TERM"),
            term_program=os.environ.get("TERM_PROGRAM"),
            ssh=bool(os.environ.get("SSH_CONNECTION") or os.environ.get("SSH_TTY")),
            multiplexer=multiplexer,
        )

    def as_dict(self) -> dict[str, t.Any]:
        """Return the human-readable, allowlisted system manifest."""

        now = datetime.now(tz=UTC).astimezone()
        return {
            "dreadnode_version": VERSION,
            "runtime_version": self.runtime_version,
            "os": platform.system(),
            "os_release": platform.release(),
            "architecture": platform.machine(),
            "terminal": self.terminal,
            "terminal_program": self.term_program,
            "ssh": self.ssh,
            "multiplexer": self.multiplexer,
            "timestamp": now.isoformat(),
            "timezone": str(now.tzinfo),
            "runtime_mode": self.runtime_mode,
            "deployment_mode": self.deployment_mode,
            "active_screen": self.active_screen,
            "session_id": self.session_id,
            "selected_agent": self.agent,
            "selected_model": self.model,
            "capabilities": [
                {"name": name, "version": version} for name, version in self.capabilities
            ],
        }


@dataclass(frozen=True, slots=True)
class DiagnosticCategory:
    """One reviewable diagnostic category."""

    category_id: str
    label: str
    description: str
    filename: str
    content: str
    selected_by_default: bool
    requires_explicit_consent: bool = False

    @property
    def size_bytes(self) -> int:
        """Return the UTF-8 payload size shown on the review screen."""

        return len(self.content.encode("utf-8", errors="replace"))


@dataclass(frozen=True, slots=True)
class DiagnosticBundle:
    """Bounded ZIP archive ready for local save or platform submission."""

    filename: str
    content: bytes
    sha256: str
    categories: tuple[str, ...]

    def as_upload(self) -> dict[str, t.Any]:
        """Serialize the archive for the JSON feedback endpoint."""

        return {
            "filename": self.filename,
            "content_base64": base64.b64encode(self.content).decode("ascii"),
            "sha256": self.sha256,
            "size_bytes": len(self.content),
        }


def _format_entries(entries: t.Iterable[LogEntry]) -> str:
    return "\n".join(
        f"{entry.timestamp.isoformat()} {entry.level:<8} {entry.source}  {entry.message}"
        for entry in entries
    )


def _read_log_tail(path: Path, limit: int = MAX_CATEGORY_BYTES) -> str:
    """Read a bounded tail, returning a visible marker for unreadable files."""

    try:
        with path.open("rb") as handle:
            handle.seek(0, os.SEEK_END)
            size = handle.tell()
            handle.seek(max(0, size - limit))
            data = handle.read(limit)
    except OSError as exc:
        return f"[{path.name} unavailable: {type(exc).__name__}]"
    prefix = "[older content omitted]\n" if size > limit else ""
    return prefix + data.decode("utf-8", errors="replace")


def _collect_component_logs(pattern: str, logs_dir: Path) -> str:
    sections: list[str] = []
    remaining = MAX_CATEGORY_BYTES
    for log_path in sorted(logs_dir.glob(pattern)):
        if not log_path.is_file() or log_path.name in {"config.yaml", "mcp-auth.json"}:
            continue
        content = _read_log_tail(log_path, min(remaining, MAX_CATEGORY_BYTES // 2))
        section = f"===== {log_path.name} =====\n{content}"
        encoded_size = len(section.encode("utf-8", errors="replace"))
        if encoded_size > remaining:
            # Skip only this file — smaller files later in the glob still fit.
            continue
        sections.append(section)
        remaining -= encoded_size
        if remaining <= 0:
            break
    return "\n\n".join(sections)


def _collect_persistent_logs(logs_dir: Path) -> str:
    """Collect the persistent TUI self-log and two newest rotations."""

    candidates = list(logs_dir.glob("*.log.prev"))
    candidates.extend(logs_dir.glob("tui.*.log"))
    existing = [path for path in candidates if path.is_file()]
    try:
        rotations = sorted(existing, key=lambda path: path.stat().st_mtime, reverse=True)
    except OSError:
        rotations = sorted(existing, reverse=True)

    selected_paths: list[Path] = []
    tui_log = logs_dir / "tui.log"
    if tui_log.is_file():
        selected_paths.append(tui_log)
    selected_paths.extend(rotations[:2])

    sections: list[str] = []
    remaining = MAX_CATEGORY_BYTES
    per_file_limit = MAX_CATEGORY_BYTES // max(1, len(selected_paths))
    for log_path in selected_paths:
        content = _read_log_tail(log_path, min(remaining, per_file_limit))
        section = f"===== {log_path.name} =====\n{content}"
        encoded_size = len(section.encode("utf-8", errors="replace"))
        if encoded_size > remaining:
            continue
        sections.append(section)
        remaining -= encoded_size
    return "\n\n".join(sections)


def collect_diagnostic_categories(
    *,
    context: BugReportContext,
    log_entries: t.Iterable[LogEntry],
    conversation: str = "",
    logs_dir: Path | None = None,
) -> list[DiagnosticCategory]:
    """Collect bounded categories with privacy-preserving defaults."""

    entries = list(log_entries)
    resolved_logs_dir = logs_dir or paths.LOGS_DIR
    info_debug = [
        entry
        for entry in entries
        if entry.level in {"DEBUG", "INFO", "SUCCESS", "WARNING", "ERROR", "CRITICAL"}
    ]
    trace_entries = [entry for entry in entries if entry.level == "TRACE"]
    exception_entries = [entry for entry in entries if entry.level in {"ERROR", "CRITICAL"}]

    return [
        DiagnosticCategory(
            category_id="system",
            label="System and runtime",
            description="Version, OS, terminal indicators, active session, model, and capabilities",
            filename="diagnostics/system.json",
            content=json.dumps(context.as_dict(), indent=2, sort_keys=True),
            selected_by_default=True,
        ),
        DiagnosticCategory(
            category_id="recent_logs",
            label="Recent logs (INFO/DEBUG)",
            description="Bounded recent TUI and runtime logs without TRACE entries",
            filename="diagnostics/recent.log",
            content=_format_entries(info_debug),
            selected_by_default=True,
        ),
        DiagnosticCategory(
            category_id="exception",
            label="Latest exception",
            description="Most recent error or traceback, when available",
            filename="diagnostics/exception.log",
            content=_format_entries(exception_entries[-1:]),
            selected_by_default=bool(exception_entries),
        ),
        DiagnosticCategory(
            category_id="trace_logs",
            label="TRACE logs",
            description="Verbose runtime events that may contain prompts or model payloads",
            filename="diagnostics/trace.log",
            content=_format_entries(trace_entries),
            selected_by_default=False,
            requires_explicit_consent=True,
        ),
        DiagnosticCategory(
            category_id="conversation",
            label="Conversation content",
            description="The active session transcript, including model and tool content",
            filename="diagnostics/conversation.md",
            content=conversation,
            selected_by_default=False,
            requires_explicit_consent=True,
        ),
        DiagnosticCategory(
            category_id="worker_logs",
            label="Worker logs",
            description="Current capability worker logs",
            filename="diagnostics/workers.log",
            content=_collect_component_logs("worker-*.log", resolved_logs_dir),
            selected_by_default=False,
            requires_explicit_consent=True,
        ),
        DiagnosticCategory(
            category_id="mcp_logs",
            label="MCP logs",
            description="Current MCP server logs",
            filename="diagnostics/mcp.log",
            content=_collect_component_logs("mcp-*.log", resolved_logs_dir),
            selected_by_default=False,
            requires_explicit_consent=True,
        ),
        DiagnosticCategory(
            category_id="previous_logs",
            label="Persistent and previous logs",
            description="The persistent TUI self-log and two newest TUI, worker, or MCP rotations",
            filename="diagnostics/previous.log",
            content=_collect_persistent_logs(resolved_logs_dir),
            selected_by_default=False,
            requires_explicit_consent=True,
        ),
    ]


def _truncate_utf8(value: str, limit: int) -> tuple[str, bool]:
    encoded = value.encode("utf-8", errors="replace")
    if len(encoded) <= limit:
        return value, False
    marker = b"\n[content truncated to bundle limit]\n"
    if limit <= len(marker):
        return "", True
    available = max(0, limit - len(marker))
    return encoded[-available:].decode("utf-8", errors="ignore") + marker.decode(), True


def build_diagnostic_bundle(
    draft: BugReportDraft,
    categories: t.Iterable[DiagnosticCategory],
    selected_category_ids: t.Collection[str],
) -> DiagnosticBundle:
    """Build a redacted, human-readable archive under the hard size cap."""

    selected = set(selected_category_ids)
    report_markdown = redact_sensitive_text(
        f"# {draft.title.strip()}\n\n{draft.description()}\n\n"
        f"Contact consent: {'yes' if draft.contact_consent else 'no'}\n"
    )
    content_budget = MAX_TOTAL_CONTENT_BYTES - len(report_markdown.encode("utf-8"))
    manifest_categories: list[dict[str, t.Any]] = []
    files: list[tuple[str, str]] = [("REPORT.md", report_markdown)]
    seen_filenames = {"manifest.json", "REPORT.md"}

    for category in categories:
        if category.category_id not in selected:
            continue
        path = PurePosixPath(category.filename)
        if (
            path.is_absolute()
            or ".." in path.parts
            or "\\" in category.filename
            or category.filename in seen_filenames
        ):
            raise ValueError("Diagnostic category has an unsafe or duplicate filename")
        seen_filenames.add(category.filename)
        redacted = redact_sensitive_text(category.content)
        allowed = max(0, min(MAX_CATEGORY_BYTES, content_budget))
        bounded, truncated = _truncate_utf8(redacted, allowed)
        content_budget -= len(bounded.encode("utf-8", errors="replace"))
        files.append((category.filename, bounded))
        manifest_categories.append(
            {
                "id": category.category_id,
                "label": category.label,
                "path": category.filename,
                "size_bytes": len(bounded.encode("utf-8", errors="replace")),
                "sha256": hashlib.sha256(bounded.encode("utf-8")).hexdigest(),
                "truncated": truncated,
                "explicit_consent": category.requires_explicit_consent,
            }
        )

    manifest = {
        "format_version": 1,
        "created_at": datetime.now(tz=UTC).isoformat(),
        "redaction": "Client-side credential patterns replaced with [REDACTED].",
        "bundle_limit_bytes": MAX_BUNDLE_BYTES,
        "categories": manifest_categories,
    }
    files.insert(0, ("manifest.json", json.dumps(manifest, indent=2, sort_keys=True)))

    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for filename, content in files:
            archive.writestr(filename, content)
    bundle_content = output.getvalue()
    if len(bundle_content) > MAX_BUNDLE_BYTES:
        raise ValueError("Diagnostic bundle exceeds the 2 MiB compressed size limit")

    timestamp = datetime.now(tz=UTC).strftime("%Y%m%d-%H%M%S")
    digest = hashlib.sha256(bundle_content).hexdigest()
    return DiagnosticBundle(
        filename=f"dreadnode-report-{timestamp}-{digest[:8]}.zip",
        content=bundle_content,
        sha256=digest,
        categories=tuple(item["id"] for item in manifest_categories),
    )


def save_diagnostic_bundle(
    bundle: DiagnosticBundle,
    output_dir: Path | None = None,
) -> Path:
    """Save a bundle locally without requiring authentication or network access."""

    destination = output_dir or paths.LOGS_DIR
    destination.mkdir(mode=0o700, parents=True, exist_ok=True)
    base_path = destination / bundle.filename
    for copy_number in range(1000):
        output_path = (
            base_path
            if copy_number == 0
            else base_path.with_stem(f"{base_path.stem}-{copy_number}")
        )
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
        flags |= getattr(os, "O_NOFOLLOW", 0)
        try:
            file_descriptor = os.open(output_path, flags, 0o600)
        except FileExistsError:
            continue
        try:
            with os.fdopen(file_descriptor, "wb") as output:
                output.write(bundle.content)
        except Exception:
            with contextlib.suppress(OSError):
                output_path.unlink()
            raise
        return output_path
    raise FileExistsError("Unable to choose a unique diagnostic bundle filename")
