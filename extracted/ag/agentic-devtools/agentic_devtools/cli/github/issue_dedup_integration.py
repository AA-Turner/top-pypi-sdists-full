"""Integration module bridging the dedup engine and I/O layer with issue commands.

Provides the same-session ledger for dedup consistency and the orchestrator
function ``dedupe_or_create()`` that wires dedup decision logic into
issue creation.
"""

from __future__ import annotations

import json
import sys
import warnings
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from agentic_devtools.file_locking import FileLockError, locked_file
from agentic_devtools.state import get_state_dir

from ..subprocess_utils import run_safe
from .issue_dedup import build_signature, decide, embed_marker
from .issue_dedup_io import add_augment_comment, add_thumbs_up, search_by_marker

# Ledger configuration constants
LEDGER_FILENAME = "setup-dedup-ledger.json"
LEDGER_LOCK_TIMEOUT = 10.0
LEDGER_MAX_ENTRIES = 100
LEDGER_MAX_AGE_HOURS = 24

# Target repository (local constant avoids circular import with issue_commands)
_AGDT_REPO = "swai-factory/agentic-devtools"


def validate_dedupe_preconditions(error_class: str | None) -> str:
    """Validate that error_class is non-blank after trimming whitespace.

    Args:
        error_class: The error class string to validate.

    Returns:
        The stripped, non-empty error class string.

    Raises:
        ValueError: If error_class is None, empty, or whitespace-only.
    """
    if error_class is None:
        raise ValueError(
            'issue.error_class is required for --dedupe mode. Set it with: agdt-set issue.error_class "<error-class>"'
        )
    if not isinstance(error_class, str):
        raise ValueError(
            f"issue.error_class must be a string for --dedupe mode, got {type(error_class).__name__!r}. "
            'Set it with: agdt-set issue.error_class "<error-class>"'
        )
    stripped = error_class.strip()
    if not stripped:
        raise ValueError(
            "issue.error_class must not be blank for --dedupe mode. "
            'Set it with: agdt-set issue.error_class "<error-class>"'
        )
    return stripped


def _get_ledger_path() -> Path:
    """Return the path to the same-session dedup ledger file."""
    return get_state_dir() / LEDGER_FILENAME


def _get_session_id() -> str:
    """Return a session identifier based on the state directory path."""
    return str(get_state_dir())


def _is_ledger_stale(data: dict) -> bool:
    """Check whether the ledger data is stale.

    A ledger is stale if:
    - Its session_id is missing or does not match the current session, OR
    - Its created_utc is missing, unparseable, offset-naive, OR older than
      LEDGER_MAX_AGE_HOURS (24 hours)

    Any unverifiable field is treated conservatively as stale to prevent a
    corrupted or malformed ledger from short-circuiting GitHub search.

    Args:
        data: The parsed ledger dict.

    Returns:
        True if the ledger is stale and should be treated as empty.
    """
    session_id = data.get("session_id")
    if session_id is None or session_id != _get_session_id():
        return True

    created_utc = data.get("created_utc")
    if created_utc is None:
        return True

    try:
        created_dt = datetime.fromisoformat(created_utc.replace("Z", "+00:00"))
        if created_dt.tzinfo is None:
            return True
        age = datetime.now(timezone.utc) - created_dt
        return age.total_seconds() > LEDGER_MAX_AGE_HOURS * 3600
    except (ValueError, AttributeError):
        return True


def _evict_oldest(entries: dict) -> dict:
    """Trim entries to LEDGER_MAX_ENTRIES by evicting oldest by created_utc.

    Ties are broken by ascending lexicographic key.

    Args:
        entries: Dict mapping signature → entry dict (with created_utc field).

    Returns:
        Dict with at most LEDGER_MAX_ENTRIES entries.
    """
    if len(entries) <= LEDGER_MAX_ENTRIES:
        return entries

    def sort_key(item: tuple[str, Any]) -> tuple[str, str]:
        key, val = item
        if isinstance(val, dict):
            raw_ts = val.get("created_utc", "")
            ts = raw_ts if isinstance(raw_ts, str) else ""
        else:
            ts = ""
        return (ts, key)

    sorted_entries = sorted(entries.items(), key=sort_key)
    keep = sorted_entries[len(sorted_entries) - LEDGER_MAX_ENTRIES :]
    return dict(keep)


def read_ledger() -> dict:
    """Read the dedup ledger, handling missing files and corruption gracefully.

    When the file does not exist, returns {} immediately without creating it.
    Handles JSON corruption by warning and returning empty dict.
    Handles stale ledgers by returning empty dict.

    Returns:
        The parsed ledger dict, or {} on any error condition.

    Raises:
        FileLockError: When the lock cannot be acquired within timeout.
    """
    path = _get_ledger_path()

    if not path.exists():
        return {}

    try:
        with locked_file(path, mode="r", exclusive=False, timeout=LEDGER_LOCK_TIMEOUT) as f:
            content = f.read()
    except FileNotFoundError:
        return {}
    except FileLockError:
        raise

    if not content.strip():
        return {}

    try:
        data = json.loads(content)
    except (json.JSONDecodeError, ValueError):
        warnings.warn(
            f"Dedup ledger at {path} contains invalid JSON; treating as empty.",
            stacklevel=2,
        )
        return {}

    if not isinstance(data, dict):
        warnings.warn(
            f"Dedup ledger at {path} has unexpected format; treating as empty.",
            stacklevel=2,
        )
        return {}

    if _is_ledger_stale(data):
        return {}

    return data


def write_ledger(data: dict) -> None:
    """Write the dedup ledger with file locking and eviction enforcement.

    Creates the file if it does not exist. Enforces the 100-entry cap
    by calling _evict_oldest on the entries before writing.

    Args:
        data: The ledger dict to write.

    Raises:
        FileLockError: When the lock cannot be acquired within timeout.
    """
    path = _get_ledger_path()
    path.parent.mkdir(parents=True, exist_ok=True)

    # Enforce eviction on entries
    if "entries" in data and isinstance(data["entries"], dict):
        data["entries"] = _evict_oldest(data["entries"])

    # Use "r+" unconditionally; locked_file creates the file when missing,
    # avoiding the truncation-before-lock race that "w" mode introduces.
    with locked_file(path, mode="r+", exclusive=True, timeout=LEDGER_LOCK_TIMEOUT) as f:
        f.seek(0)
        f.write(json.dumps(data, indent=2))
        f.truncate()


def lookup_ledger(sig: str) -> int | None:
    """Look up a signature in the ledger.

    Args:
        sig: The dedup signature to look up.

    Returns:
        The issue number if found, None otherwise.
    """
    data = read_ledger()
    entries = data.get("entries", {})
    if not isinstance(entries, dict):
        return None
    entry = entries.get(sig)
    if isinstance(entry, dict):
        issue_number = entry.get("issue_number")
        if isinstance(issue_number, int):
            return issue_number
    return None


def record_in_ledger(sig: str, issue_number: int, *, action: str = "create") -> None:
    """Record a dedup result in the ledger (atomic read-modify-write).

    Sets created_utc only on first write for a signature (immutable
    first-seen timestamp). Updates last_action on subsequent writes.

    Args:
        sig: The dedup signature.
        issue_number: The GitHub issue number.
        action: The action taken ("create" or "augment").
    """
    path = _get_ledger_path()
    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    with locked_file(path, mode="r+", exclusive=True, timeout=LEDGER_LOCK_TIMEOUT) as f:
        content = f.read()

        if not content.strip():
            data: dict[str, Any] = {}
        else:
            try:
                parsed = json.loads(content)
            except (json.JSONDecodeError, ValueError):
                warnings.warn(
                    f"Dedup ledger at {path} contains invalid JSON; treating as empty.",
                    stacklevel=2,
                )
                data = {}
            else:
                if isinstance(parsed, dict):
                    data = parsed
                else:
                    warnings.warn(
                        f"Dedup ledger at {path} has unexpected format; treating as empty.",
                        stacklevel=2,
                    )
                    data = {}

        if _is_ledger_stale(data):
            data = {}

        if not data:
            data = {
                "session_id": _get_session_id(),
                "created_utc": now_utc,
                "entries": {},
            }

        if "entries" not in data or not isinstance(data.get("entries"), dict):
            data["entries"] = {}

        existing = data["entries"].get(sig)
        if isinstance(existing, dict):
            existing["issue_number"] = issue_number
            existing["last_action"] = action
        else:
            data["entries"][sig] = {
                "issue_number": issue_number,
                "created_utc": now_utc,
                "last_action": action,
            }

        data["entries"] = _evict_oldest(data["entries"])
        f.seek(0)
        f.write(json.dumps(data, indent=2))
        f.truncate()


def dedupe_or_create(
    *,
    title: str,
    body: str,
    labels: list[str] | None,
    issue_type: str | None,
    assignees: list[str] | None,
    milestone: str | None,
    error_class: str | None,
    dry_run: bool,
    repo: str = _AGDT_REPO,
) -> str | None:
    """Orchestrate dedup-aware issue creation.

    Computes signature, embeds marker, checks ledger, searches GitHub,
    and either creates a new issue or augments an existing one.

    Args:
        title: Issue title.
        body: Issue body (markdown).
        labels: List of label names.
        issue_type: GitHub issue type (Bug, Feature, Task).
        assignees: List of GitHub usernames.
        milestone: Milestone name or number.
        error_class: The error class for dedup signature computation.
        dry_run: If True, preview actions without mutating.
        repo: Target repository (owner/repo).

    Returns:
        The created or selected issue URL for live create/augment paths, else None.

    Raises:
        ValueError: If error_class is invalid.
        RuntimeError: If search_by_marker fails (fail-fast).
    """
    # Validate and compute signature
    validated_error_class = validate_dedupe_preconditions(error_class)
    sig = build_signature(validated_error_class)
    marker_body = embed_marker(body, sig)

    print(f"Dedup signature: {sig}")

    if dry_run:
        # Check ledger for preview
        ledger_hit = lookup_ledger(sig)
        if ledger_hit is not None:
            print("=== PREVIEW (not submitted) ===")
            print("Dedup mode: active")
            print(f"Dedup signature: {sig}")
            print(f"Action: would upvote and augment #{ledger_hit}")
            return None

        # Search even in dry-run (read-only operation)
        matches = search_by_marker(sig, repo=repo)
        open_matches = [m for m in matches if m.get("state") == "open"]
        decision = decide(open_matches, sig)

        print("=== PREVIEW (not submitted) ===")
        print("Dedup mode: active")
        print(f"Dedup signature: {sig}")

        if decision["action"] == "create":
            print("Action: would create issue")
            print(f"Repository: {repo}")
            print(f"Title: {title}")
            print(f"Body (with marker):\n{marker_body}")
        else:
            issue_num = decision.get("issue_number")
            print(f"Action: would upvote and augment #{issue_num}")
        return None

    # Live path: check ledger first
    ledger_hit = lookup_ledger(sig)
    if ledger_hit is not None:
        issue_url = f"https://github.com/{repo}/issues/{ledger_hit}"
        print(f"Existing issue found: #{ledger_hit} (via ledger)")
        print("Action: upvote-augment")
        add_thumbs_up(ledger_hit, repo=repo)
        augment_body = f"Duplicate report encountered.\n\nTitle: {title}\n\n{body}"
        add_augment_comment(ledger_hit, augment_body, repo=repo)
        record_in_ledger(sig, ledger_hit, action="augment")
        print(f"Issue augmented: {issue_url}")
        return issue_url

    # Search GitHub
    matches = search_by_marker(sig, repo=repo)
    open_matches = [m for m in matches if m.get("state") == "open"]
    decision = decide(open_matches, sig)

    if decision["action"] == "upvote-augment":
        issue_num = decision["issue_number"]
        assert isinstance(issue_num, int)
        issue_url = f"https://github.com/{repo}/issues/{issue_num}"
        print(f"Existing issue found: #{issue_num} (via search)")
        print("Action: upvote-augment")
        add_thumbs_up(issue_num, repo=repo)
        augment_body = f"Duplicate report encountered.\n\nTitle: {title}\n\n{body}"
        add_augment_comment(issue_num, augment_body, repo=repo)
        record_in_ledger(sig, issue_num, action="augment")
        print(f"Issue augmented: {issue_url}")
        return issue_url
    else:
        # Create new issue
        print(f"Creating issue in {repo}...")
        from .issue_commands import _build_gh_create_args

        gh_args = _build_gh_create_args(
            title=title,
            body=marker_body,
            labels=labels,
            issue_type=issue_type,
            assignees=assignees,
            milestone=milestone,
            repo=repo,
        )

        result = run_safe(gh_args, capture_output=True, text=True, shell=False)
        if result.returncode != 0:
            print(f"Error creating issue: {result.stderr.strip()}", file=sys.stderr)
            sys.exit(result.returncode)

        issue_url = result.stdout.strip()
        print(f"Issue created: {issue_url}")

        # Extract issue number from URL
        try:
            issue_number = int(issue_url.rstrip("/").rsplit("/", 1)[-1])
            record_in_ledger(sig, issue_number, action="create")
        except (ValueError, IndexError):
            warnings.warn(
                f"Could not extract issue number from URL: {issue_url!r}; ledger will not record this issue.",
                stacklevel=2,
            )
        return issue_url
