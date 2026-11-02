"""Separate non-blocking drift and template-compliance check."""

from __future__ import annotations

import sys
from pathlib import Path

from agentic_devtools.cli.phase0_review.commands import run_review
from agentic_devtools.cli.phase0_review.report import parse_serialized_finding


def run_drift_check(
    *,
    repo_root: Path | None = None,
    input_path: str | Path | None = None,
    integrity_path: str | Path | None = None,
) -> tuple[str, int]:
    """Return severity-tagged informational output and its independent status."""
    report = run_review(
        repo_root=repo_root,
        input_path=input_path,
        integrity_path=integrity_path,
    )
    lines: list[str] = []
    has_error = False
    for line in report.splitlines():
        parsed = parse_serialized_finding(line)
        if parsed is None:
            continue
        passed, text = parsed
        lines.append(f"{'info' if passed else 'error'}: {text}")
        if not passed:
            has_error = True
    if not lines:
        lines.append("info: no drift findings")
    return "\n".join(lines), 1 if has_error else 0


def main() -> int:
    """Print drift output and return 1 only for error-level mismatches."""
    output, status = run_drift_check()
    print(output)
    return status


if __name__ == "__main__":  # pragma: no cover - direct module entry point
    sys.exit(main())
