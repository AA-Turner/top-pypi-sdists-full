"""Structured setup report for agdt-setup.

Provides ``SetupReport`` and ``PhaseResult`` dataclasses for machine-readable
output, and ``write_report()`` for atomic persistence to
``~/.agdt/last-setup-report.json``.
"""

from __future__ import annotations

import json
import os
import stat
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .exit_codes import name_for
from .refresh_outcome import RefreshOutcome
from .script_generators.atomic_write import atomic_write

REPORT_PATH: Path = Path.home() / ".agdt" / "last-setup-report.json"
SCHEMA_VERSION: int = 1
VALID_MODES: tuple[str, ...] = ("setup", "check", "check-fix", "dry-run")


@dataclass
class PhaseResult:
    """Outcome of a single setup phase."""

    name: str
    status: str  # "success", "failed", "skipped"
    duration_ms: int = 0
    error: str | None = None


@dataclass
class SetupReport:
    """Complete structured report for a single agdt-setup invocation."""

    schema_version: int
    timestamp: str
    exit_code: int
    exit_code_name: str
    phases: list[PhaseResult] = field(default_factory=list)
    details: dict[str, Any] = field(default_factory=dict)
    mode: str = "setup"
    git_root: str | None = None
    autorun_enabled: bool | None = None
    _phase_index: dict[str, int] = field(default_factory=dict, init=False, repr=False)

    def __post_init__(self) -> None:
        """Normalize any constructor-provided phases into the dedup index."""
        if self.mode not in VALID_MODES:
            allowed = ", ".join(VALID_MODES)
            raise ValueError(f"Invalid setup report mode: {self.mode!r}. Expected one of: {allowed}")
        if not self.phases:
            return
        existing_phases = self.phases
        self.phases = []
        for phase in existing_phases:
            self.record(phase)

    def record(self, phase: PhaseResult) -> None:
        """Record a phase result with ordered-dict dedup semantics.

        First observation of a ``phase.name`` appends to ``phases``.
        Subsequent observations update the existing entry in place.
        """
        if phase.name in self._phase_index:
            self.phases[self._phase_index[phase.name]] = phase
        else:
            self._phase_index[phase.name] = len(self.phases)
            self.phases.append(phase)

    def set_refresh_outcome(self, outcome: RefreshOutcome) -> None:
        """Record the standalone refresh outcome under ``details.refresh_outcome``.

        Stores the serialized ``RefreshOutcome`` so the setup report exposes a
        machine-readable ``{"status", "reason", "error"}`` object for the
        ``--refresh-issue-types`` standalone path.
        """
        self.details["refresh_outcome"] = outcome.to_dict()

    def to_dict(self) -> dict[str, Any]:
        """Serialize the report to a JSON-compatible dictionary.

        Builds the top-level dict manually to include computed summary counts
        and control field ordering. Phase entries are serialized via
        ``dataclasses.asdict``.
        """
        passed = sum(1 for p in self.phases if p.status == "success")
        failed = sum(1 for p in self.phases if p.status == "failed")
        skipped = sum(1 for p in self.phases if p.status == "skipped")

        return {
            "schema_version": self.schema_version,
            "mode": self.mode,
            "git_root": self.git_root,
            "timestamp": self.timestamp,
            "exit_code": self.exit_code,
            "exit_code_name": self.exit_code_name,
            "autorun_enabled": self.autorun_enabled,
            "total_phases": len(self.phases),
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "phases": [asdict(p) for p in self.phases],
            "details": self.details,
        }

    def write(self, path: Path | None = None) -> bool:
        """Persist this report atomically.

        Path resolution precedence:
          1. Explicit *path* argument
          2. ``AGDT_SETUP_REPORT_PATH`` environment variable
          3. Default ``~/.agdt/last-setup-report.json``

        Creates parent directories and attempts POSIX chmod 0o700
        (best-effort). Returns ``True`` on success, ``False`` on
        ``Exception`` (with deterministic stderr message). Re-raises
        ``BaseException`` subclasses after cleanup.
        """
        resolved = _resolve_report_path(path)

        try:
            report_dir = resolved.parent
            report_dir.mkdir(parents=True, exist_ok=True)

            # Best-effort chmod 0o700 on POSIX
            try:
                if os.name != "nt" and report_dir == REPORT_PATH.parent:
                    report_dir.chmod(stat.S_IRWXU)
            except OSError:
                pass

            content = json.dumps(self.to_dict(), indent=2) + "\n"
            atomic_write(resolved, content)
            return True
        except Exception as exc:  # noqa: BLE001
            print(
                f"agdt-setup: failed to write setup report to {resolved}: {type(exc).__name__}: {exc}",
                file=sys.stderr,
            )
            return False


def _resolve_report_path(path: Path | None) -> Path:
    """Resolve the report output path with precedence rules."""
    if path is not None:
        return path.expanduser()
    env_path = os.environ.get("AGDT_SETUP_REPORT_PATH")
    if env_path:
        return Path(env_path).expanduser()
    return REPORT_PATH


def make_report(
    exit_code: int,
    phases: list[PhaseResult] | None = None,
    details: dict[str, Any] | None = None,
    *,
    mode: str = "setup",
    git_root: str | None = None,
) -> SetupReport:
    """Construct a ``SetupReport`` with current timestamp and derived name."""
    return SetupReport(
        schema_version=SCHEMA_VERSION,
        timestamp=datetime.now(tz=timezone.utc).isoformat(),
        exit_code=exit_code,
        exit_code_name=name_for(exit_code),
        phases=phases or [],
        details=details or {},
        mode=mode,
        git_root=git_root,
    )


def write_report(report: SetupReport) -> bool:
    """Persist *report* atomically to the resolved report path.

    Thin wrapper that delegates to :meth:`SetupReport.write`.
    """
    return report.write()
