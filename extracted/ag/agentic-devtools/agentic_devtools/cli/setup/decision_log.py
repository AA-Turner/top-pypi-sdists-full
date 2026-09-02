"""Append-only decision/questions log module.

Provides ``append_decision`` and ``show_log`` for a per-worktree
append-only Markdown file at
``.agdt/workflows/{identity}/{worktree_key}/setup/run-setup-decision-log.md``.

CLI entry point: ``agdt-setup-decision-log`` with ``append`` and ``show``
subcommands.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from agentic_devtools.file_locking import locked_file
from agentic_devtools.state import get_state_dir

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

LOG_FILENAME = "run-setup-decision-log.md"  # Name of the decision log file within the ``setup/`` subdirectory.

MAX_FIELD_BYTES = 2000  # Maximum allowed UTF-8 byte length for any single text field.

_START_MARKER_RE = re.compile(r"<!-- agdt-decision-entry:start id:(\d+) -->")
_END_MARKER_RE = re.compile(r"<!-- agdt-decision-entry:end -->")
_MARKER_RE = re.compile(
    r"(?P<start><!-- agdt-decision-entry:start id:\d+ -->)|"
    r"(?P<end><!-- agdt-decision-entry:end -->)"
)

_START_MARKER_SUBSTR = "<!-- agdt-decision-entry:start"
# Partial prefix (not the full marker) so that both valid markers
# and truncated marker-like substrings are detected — symmetric with
# _START_MARKER_SUBSTR.
_END_MARKER_SUBSTR = "<!-- agdt-decision-entry:end"


# ---------------------------------------------------------------------------
# Data Model
# ---------------------------------------------------------------------------


@dataclass
class DecisionEntry:
    """A single decision log entry (without id/timestamp — assigned on append)."""

    step: str
    question: str
    decision: str
    rationale: str
    auto_resolved: bool


# ---------------------------------------------------------------------------
# Internal Helpers
# ---------------------------------------------------------------------------


def _get_log_path() -> Path:
    """Resolve the per-worktree decision log file path."""
    state_dir = get_state_dir()
    return state_dir / "setup" / LOG_FILENAME


def _parse_bool(value: str) -> bool:
    """Argparse type converter for boolean string values.

    Accepts ``"true"``/``"false"`` case-insensitive.
    Raises ``argparse.ArgumentTypeError`` for anything else.
    """
    lower = value.lower()
    if lower == "true":
        return True
    if lower == "false":
        return False
    raise argparse.ArgumentTypeError(f"Invalid boolean value: {value!r}. Must be 'true' or 'false'.")


def _validate_entry(entry: DecisionEntry) -> None:
    """Validate a ``DecisionEntry`` before appending.

    Raises:
        TypeError: If ``auto_resolved`` is not a bool.
        ValueError: If any text field is empty, contains newlines,
            exceeds ``MAX_FIELD_BYTES``, or contains marker substrings.
    """
    if not isinstance(entry.auto_resolved, bool):
        raise TypeError(f"auto_resolved must be a bool, got {type(entry.auto_resolved).__name__}")

    text_fields = {
        "step": entry.step,
        "question": entry.question,
        "decision": entry.decision,
        "rationale": entry.rationale,
    }

    for name, value in text_fields.items():
        if not isinstance(value, str):
            raise ValueError(f"{name} must be a string, got {type(value).__name__}")
        if not value.strip():
            raise ValueError(f"{name} must not be empty or whitespace-only")
        if "\n" in value or "\r" in value:
            raise ValueError(f"{name} must not contain newline characters")
        if len(value.encode("utf-8")) > MAX_FIELD_BYTES:
            raise ValueError(f"{name} exceeds maximum of {MAX_FIELD_BYTES} UTF-8 bytes")
        if _START_MARKER_SUBSTR in value or _END_MARKER_SUBSTR in value:
            raise ValueError(f"{name} must not contain marker substrings")


def _parse_existing_markers(content: str) -> int:
    """Parse existing start/end markers and return the count of complete entries.

    Validates:
    - IDs are sequential ``[1..N]`` with no gaps or duplicates.
    - Every start marker has a matching end marker (no incomplete trailing entry).

    Returns:
        The number of complete entries found (0 if content is empty).

    Raises:
        ValueError: If markers are malformed, have gaps/duplicates, or an
            incomplete trailing entry is detected.
    """
    if not content:
        return 0

    start_ids = [int(m.group(1)) for m in _START_MARKER_RE.finditer(content)]
    start_marker_like_count = content.count(_START_MARKER_SUBSTR)
    end_count = len(_END_MARKER_RE.findall(content))
    end_marker_like_count = content.count(_END_MARKER_SUBSTR)

    if not start_ids and end_count == 0:
        if start_marker_like_count > 0:
            raise ValueError("Malformed marker sequence: found truncated or incomplete start marker")
        if end_marker_like_count > 0:
            raise ValueError("Malformed marker sequence: found truncated or incomplete end marker")
        return 0

    if start_marker_like_count != len(start_ids):
        raise ValueError(
            "Malformed marker sequence: "
            f"found {start_marker_like_count} marker-like start substrings but {len(start_ids)} valid markers"
        )

    if end_marker_like_count != end_count:
        raise ValueError(
            "Malformed marker sequence: "
            f"found {end_marker_like_count} marker-like end substrings but {end_count} valid markers"
        )

    # Check for stray end marker (more ends than starts)
    if end_count > len(start_ids):
        raise ValueError("Malformed marker sequence: stray end marker detected")

    # Check for incomplete trailing entry (more starts than ends)
    if len(start_ids) > end_count:
        raise ValueError("Incomplete trailing entry detected: start marker without matching end marker")

    # Validate strict start/end alternation in marker order.
    in_entry = False
    for match in _MARKER_RE.finditer(content):
        is_start = match.group("start") is not None
        if is_start:
            if in_entry:
                raise ValueError("Malformed marker sequence: nested start marker detected")
            in_entry = True
            continue

        if not in_entry:
            raise ValueError("Malformed marker sequence: stray end marker detected")
        in_entry = False

    # Validate sequential IDs [1..N].
    # sorted(start_ids) == expected means the IDs are the correct set but in the
    # wrong order (pure reordering, no missing/extra IDs); any other mismatch
    # means there is a gap or an unexpected ID — report as a gap in both cases
    # since the gap is the more fundamental problem even when also out-of-order.
    expected = list(range(1, len(start_ids) + 1))
    if start_ids != expected:
        if len(start_ids) != len(set(start_ids)):
            raise ValueError("Duplicate entry IDs detected in decision log")
        if sorted(start_ids) == expected:
            raise ValueError("Out-of-order entry IDs detected in decision log")
        raise ValueError("Gap in entry ID sequence detected in decision log")

    return len(start_ids)


def _render_entry(entry: DecisionEntry, entry_id: int, timestamp: str) -> str:
    """Render a single decision entry as a Markdown block with HTML markers.

    Args:
        entry: The validated decision entry.
        entry_id: The sequential ID to assign.
        timestamp: An ISO-8601 UTC timestamp string.

    Returns:
        The formatted Markdown block (with trailing newline).
    """
    auto_str = str(entry.auto_resolved).lower()
    return (
        f"<!-- agdt-decision-entry:start id:{entry_id} -->\n"
        f"### Decision #{entry_id} ({timestamp})\n"
        f"- Step: {entry.step}\n"
        f"- Question: {entry.question}\n"
        f"- Decision: {entry.decision}\n"
        f"- Rationale: {entry.rationale}\n"
        f"- Auto-resolved: {auto_str}\n"
        f"<!-- agdt-decision-entry:end -->\n"
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def append_decision(entry: DecisionEntry) -> int:
    """Append a validated decision entry to the per-worktree log.

    Creates the log file and parent directories if they do not exist.
    Assigns a sequential ID based on existing entries.

    Args:
        entry: The decision entry to append.

    Returns:
        The assigned entry ID.

    Raises:
        TypeError: If ``auto_resolved`` is not a bool.
        ValueError: If validation fails or log integrity is compromised.
    """
    _validate_entry(entry)

    log_path = _get_log_path()
    log_path.parent.mkdir(parents=True, exist_ok=True)

    # Use "a+" (not "r+") so locked open can safely create a missing file
    # without injecting JSON bootstrap content in deletion-race windows.
    with locked_file(log_path, mode="a+", exclusive=True) as f:
        f.seek(0)
        content = f.read()

        # Parse and validate existing markers
        existing_count = _parse_existing_markers(content)

        # Assign next ID and generate timestamp
        entry_id = existing_count + 1
        timestamp = datetime.now(timezone.utc).isoformat()

        # Render and append
        rendered = _render_entry(entry, entry_id, timestamp)

        # Ensure separation from previous content
        if content and not content.endswith("\n"):
            rendered = "\n" + rendered

        f.seek(0, 2)  # seek to end of file for appending
        f.write(rendered)
        f.flush()
        os.fsync(f.fileno())

    return entry_id


def show_log() -> str:
    """Read and return the full decision log contents.

    Returns:
        The raw file contents (including HTML markers), or ``""`` if the
        file is missing, empty, or unreadable (permission denied, I/O
        error, encoding error, etc.). Never creates the file and never
        raises an exception.
    """
    log_path = _get_log_path()
    try:
        content = log_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""
    return content


# ---------------------------------------------------------------------------
# CLI Entry Point
# ---------------------------------------------------------------------------


def decision_log_command() -> None:
    """CLI entry point for ``agdt-setup-decision-log``."""
    parser = argparse.ArgumentParser(
        prog="agdt-setup-decision-log",
        description="Append-only decision/questions log for setup runs.",
    )
    subparsers = parser.add_subparsers(dest="subcommand")

    # append subcommand
    append_parser = subparsers.add_parser("append", help="Append a decision entry.")
    append_parser.add_argument("--step", required=True, help="Setup step name.")
    append_parser.add_argument("--question", required=True, help="Question that was faced.")
    append_parser.add_argument("--decision", required=True, help="Decision that was made.")
    append_parser.add_argument("--rationale", required=True, help="Rationale for the decision.")
    append_parser.add_argument(
        "--auto-resolved",
        required=True,
        type=_parse_bool,
        help="Whether the decision was auto-resolved (true/false).",
    )

    # show subcommand
    subparsers.add_parser("show", help="Display the decision log.")

    args = parser.parse_args()

    if args.subcommand is None:
        parser.print_help()
        sys.exit(1)

    if args.subcommand == "append":
        entry = DecisionEntry(
            step=args.step,
            question=args.question,
            decision=args.decision,
            rationale=args.rationale,
            auto_resolved=args.auto_resolved,
        )
        try:
            entry_id = append_decision(entry)
        except (ValueError, TypeError) as exc:
            print(f"Error: {exc}", file=sys.stderr)
            sys.exit(1)
        print(f"Decision #{entry_id} recorded.")
    else:  # show
        content = show_log()
        if content:
            sys.stdout.write(content)
        else:
            print("No decisions recorded yet.")
