"""CLI wrapper for hierarchy detector invocation from shell scripts.

Provides a thin command-line interface that invokes the GitHubHierarchyDetector
with a configurable timeout and emits line-oriented output suitable for
consumption by Bash/PowerShell scripts without requiring ``jq`` or ``eval``.

Output format (one field per line, newline-delimited key=value):
    status=ok|error
    parent=<issue_number>|null
    level=epic|feature|task|null
    title=<issue_title>

Exit codes:
    0 - Success (status=ok)
    1 - Error or timeout (status=error, details on stderr)
"""

from __future__ import annotations

import argparse
import signal
import sys
from typing import NoReturn

# Module-level storage for the configured timeout value; set in main() before
# arming SIGALRM so the handler can report the accurate duration.
_timeout_secs: int = 10


def _timeout_handler(signum: int, frame: object) -> NoReturn:
    """Signal handler for enforcing the configured timeout."""
    print("status=error", flush=True)
    print("parent=null", flush=True)
    print("level=null", flush=True)
    print("title=null", flush=True)
    print(f"Hierarchy detection timed out after {_timeout_secs} seconds", file=sys.stderr)
    sys.exit(1)


def _normalize_title(title: str, issue_number: int) -> str:
    """Normalize title to spec format: 'Issue {N}' without '#'.

    The detector's internal fallback produces 'Issue #{N}', but the spec
    requires 'Issue {N}' (no hash) for stub titles.  Only the fallback title
    for the *current* issue is normalized; user-provided titles that happen to
    match the pattern for a different issue number are left unchanged.
    """
    if title == f"Issue #{issue_number}":
        return f"Issue {issue_number}"
    return title


class _NormalisingArgumentParser(argparse.ArgumentParser):
    """ArgumentParser that emits line-oriented status=error output on failure.

    argparse's default error handler exits with code 2 and writes to stderr.
    Shell scripts that consume this CLI expect all errors to use the documented
    line-oriented format (``status=error`` on stdout, detail on stderr) and
    exit code 1.  Overriding ``error()`` normalises argparse failures into that
    same contract so callers never see exit code 2.
    """

    def error(self, message: str) -> None:  # type: ignore[override]
        print("status=error", flush=True)
        print("parent=null", flush=True)
        print("level=null", flush=True)
        print("title=null", flush=True)
        print(f"Argument error: {message}", file=sys.stderr)
        sys.exit(1)


def _positive_int(value: str) -> int:
    """Argparse type that requires a positive (≥ 1) integer.

    Raises :class:`argparse.ArgumentTypeError` on invalid input so that
    :class:`_NormalisingArgumentParser` can translate the failure into the
    documented ``status=error`` line-oriented output.
    """
    try:
        ivalue = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"{value!r} is not an integer")
    if ivalue < 1:
        raise argparse.ArgumentTypeError(f"must be a positive integer (got {ivalue})")
    return ivalue


def main() -> None:
    """Entry point for detect_parent_cli."""
    parser = _NormalisingArgumentParser(
        description="Detect hierarchy parent for a GitHub issue",
    )
    parser.add_argument(
        "--issue",
        type=_positive_int,
        required=True,
        help="GitHub issue number to detect hierarchy for, must be a positive integer",
    )
    parser.add_argument(
        "--repo",
        type=str,
        required=True,
        help="Repository in owner/repo format",
    )
    parser.add_argument(
        "--timeout",
        type=_positive_int,
        default=10,
        help="Timeout in seconds, must be a positive integer (default: 10)",
    )
    args = parser.parse_args()

    # Validate repo format: must be exactly 'owner/repo' with non-empty segments and no extra slashes
    parts = args.repo.split("/")
    if len(parts) != 2 or not parts[0] or not parts[1]:
        print("status=error", flush=True)
        print("parent=null", flush=True)
        print("level=null", flush=True)
        print("title=null", flush=True)
        print(f"Invalid --repo format: {args.repo!r} (expected owner/repo)", file=sys.stderr)
        sys.exit(1)

    owner, repo = parts

    try:
        # Set up timeout using SIGALRM (Unix only; no enforcement on platforms without SIGALRM)
        global _timeout_secs
        _timeout_secs = args.timeout
        if hasattr(signal, "SIGALRM"):
            signal.signal(signal.SIGALRM, _timeout_handler)
            signal.alarm(args.timeout)

        from agentic_devtools.cli.speckit.hierarchy_detector import GitHubHierarchyDetector

        detector = GitHubHierarchyDetector(owner=owner, repo=repo)

        # Get parent
        parent = detector.get_parent(owner, repo, args.issue)

        # Get level
        level = detector.get_level(owner, repo, args.issue)

        # Get title
        title = detector._fetch_issue_title(owner, repo, args.issue)
        title = _normalize_title(title, args.issue)

        # Cancel alarm if still running
        if hasattr(signal, "SIGALRM"):
            signal.alarm(0)

        # Output results
        print("status=ok", flush=True)
        print(f"parent={parent if parent is not None else 'null'}", flush=True)
        print(f"level={level.value if level is not None else 'null'}", flush=True)
        # Escape newlines in title to keep output line-oriented
        safe_title = title.replace("\n", " ").replace("\r", "")
        print(f"title={safe_title}", flush=True)

    except Exception as exc:
        # Cancel alarm
        if hasattr(signal, "SIGALRM"):
            signal.alarm(0)

        print("status=error", flush=True)
        print("parent=null", flush=True)
        print("level=null", flush=True)
        print("title=null", flush=True)
        print(f"Hierarchy detection failed: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
