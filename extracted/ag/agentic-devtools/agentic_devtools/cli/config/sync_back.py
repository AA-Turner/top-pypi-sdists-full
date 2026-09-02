"""
One-time sync-back from per-worktree state to project.json.

Provides a synchronous CLI command ``agdt-sync-back`` that copies eligible
configuration values from the current worktree's ``state.json`` into the
team-shared ``.agdt/config/project.json``, with validation and merge semantics.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


def _cross_field_validate(
    merged: dict[str, Any],
    keys_being_synced: list[str],
) -> list[str]:
    """Run cross-field validators on the merged config.

    Returns a list of error messages (empty if all pass).

    Validators are only applied when at least one of their involved keys is
    present in *keys_being_synced*, so pre-existing violations in
    ``project.json`` do not block unrelated sync operations.
    """
    errors: list[str] = []

    # Invariant: defaultCommitIssueType must be in availableCommitIssueTypes.
    # Only check when this sync operation is touching one of the commit-type keys.
    _commit_type_keys = {"defaultCommitIssueType", "availableCommitIssueTypes"}
    if _commit_type_keys & set(keys_being_synced):
        if "defaultCommitIssueType" in merged and "availableCommitIssueTypes" in merged:
            default_type = merged["defaultCommitIssueType"]
            available_types = merged["availableCommitIssueTypes"]
            if isinstance(default_type, str) and isinstance(available_types, list):
                # Normalize both sides to match runtime consumer behavior in
                # commit_type_resolution.read_available_commit_types, which strips
                # each element and ignores non-string list entries.
                normalized_default = default_type.strip()
                normalized_available = {item.strip() for item in available_types if isinstance(item, str)}
                if normalized_default not in normalized_available:
                    errors.append(
                        f"Cross-field validation error: 'defaultCommitIssueType' value "
                        f"'{default_type}' must appear in 'availableCommitIssueTypes' "
                        f"({available_types})"
                    )

    return errors


def _count_missing_state_skips(skipped: list[dict[str, Any]]) -> int:
    """Count skipped keys omitted because their source state value was not set."""
    return sum("not set in current worktree state" in s.get("reason", "") for s in skipped)


def _no_changes_message(
    *,
    all_eligible: bool,
    skipped: list[dict[str, Any]],
    unchanged_count: int = 0,
) -> str:
    """Return the user-facing message for a no-op sync result."""
    missing_count = _count_missing_state_skips(skipped)

    if all_eligible:
        if missing_count and unchanged_count:
            return "No changes to sync — eligible values already match project.json or are not set in state"
        if missing_count:
            return "No values were synced — no sync-eligible source values are set in the current worktree state"
        return "No changes to sync — all eligible values already match project.json"

    if missing_count and missing_count == len(skipped):
        return "No values were synced — all requested keys were skipped (source values not set in state)"
    if missing_count:
        return (
            "No changes to sync — requested values already match project.json or were "
            "skipped because source values are not set in state"
        )
    return "No changes to sync — all requested values already match project.json"


def sync_back(
    *,
    keys: list[str] | None = None,
    all_eligible: bool = False,
    dry_run: bool = False,
    git_root: Path | None = None,
) -> dict[str, Any]:
    """Sync eligible state values back to project.json.

    Args:
        keys: Specific project.json keys to sync. Mutually exclusive with *all_eligible*.
        all_eligible: When True, sync all eligible keys that differ.
        dry_run: When True, compute changes without writing to disk.
        git_root: Override git root for config path resolution.

    Returns:
        A dict with ``synced_keys`` (list), ``skipped_keys`` (list of dicts),
        ``warnings`` (list of str), and ``errors`` (list of str).

    Raises:
        ValueError: When project.json cannot be read or contains malformed JSON.
        RuntimeError: When git root cannot be determined.
    """
    from agentic_devtools.cli.config.project_config import (
        SYNC_ELIGIBLE_KEYS,
        _get_config_path,
    )
    from agentic_devtools.state import get_value

    result: dict[str, Any] = {
        "synced_keys": [],
        "skipped_keys": [],
        "warnings": [],
        "errors": [],
        "unchanged_count": 0,
    }

    # Determine which keys to sync
    if all_eligible:
        target_keys = list(SYNC_ELIGIBLE_KEYS.keys())
    elif keys:
        target_keys = keys
    else:
        result["errors"].append("Must specify --keys or --all-eligible")
        return result

    # Validate all requested keys are eligible
    for key in target_keys:
        if key not in SYNC_ELIGIBLE_KEYS:
            result["errors"].append(
                f"Key '{key}' is not sync-eligible. Eligible keys: {', '.join(sorted(SYNC_ELIGIBLE_KEYS.keys()))}"
            )

    if result["errors"]:
        return result

    # Load existing project.json (strict parsing — no fallback to {})
    config_path = _get_config_path(git_root)
    if config_path is None:
        raise RuntimeError("Cannot determine git repository root. Run from inside a git repo.")

    existing_config: dict[str, Any] = {}
    file_exists = config_path.exists()

    if file_exists:
        try:
            raw_text = config_path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as e:
            raise ValueError(
                f"Could not read {config_path}: {e}. Fix the file manually before running sync-back."
            ) from e
        try:
            parsed = json.loads(raw_text)
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Malformed JSON in {config_path}: {e}. Fix the file manually before running sync-back."
            ) from e
        if not isinstance(parsed, dict):
            raise ValueError(
                f"Expected JSON object in {config_path}, got {type(parsed).__name__}. "
                f"Fix the file manually before running sync-back."
            )
        existing_config = parsed

    # Collect values to sync from state
    merged = dict(existing_config)
    changes: list[dict[str, Any]] = []
    unchanged_count = 0

    for key in target_keys:
        mapping = SYNC_ELIGIBLE_KEYS[key]
        state_key = mapping["state_key"]
        validator = mapping["validator"]

        # Read source value from state
        source_value = get_value(state_key)

        if source_value is None:
            result["skipped_keys"].append(
                {
                    "key": key,
                    "reason": f"source key '{state_key}' is not set in current worktree state",
                }
            )
            result["warnings"].append(
                f"Skipping '{key}': source key '{state_key}' is not set in current worktree state"
            )
            continue

        # Validate value
        validation_error = validator(source_value)
        if validation_error:
            result["errors"].append(
                f"Validation failed for '{key}': {validation_error} (source: '{state_key}' = {source_value!r})"
            )
            continue

        # Check if value differs
        current_value = existing_config.get(key)
        if current_value == source_value:
            unchanged_count += 1
            if all_eligible:
                # Silently skip unchanged keys in --all-eligible mode
                continue
            result["skipped_keys"].append(
                {
                    "key": key,
                    "reason": "value already matches project.json",
                }
            )
            continue

        # Stage the change
        merged[key] = source_value
        changes.append(
            {
                "key": key,
                "old_value": current_value,
                "new_value": source_value,
            }
        )

    if result["errors"]:
        return result

    result["unchanged_count"] = unchanged_count

    # Cross-field validation on the merged result
    cross_errors = _cross_field_validate(merged, [c["key"] for c in changes])
    if cross_errors:
        result["errors"].extend(cross_errors)
        return result

    # No changes case
    if not changes:
        result["warnings"].append(
            _no_changes_message(
                all_eligible=all_eligible,
                skipped=result["skipped_keys"],
                unchanged_count=unchanged_count,
            )
        )
        return result

    # Record synced keys
    result["synced_keys"] = changes

    if dry_run:
        return result

    # Write with file locking
    from agentic_devtools.file_locking import locked_file

    if not file_exists:
        # project.json will be created lazily by locked_file() if it still does
        # not exist at lock time, and if another process creates it first the
        # locked read/write path will reuse that file instead of overwriting it.
        # Only the gitignore negation setup belongs here.
        # Ensure gitignore negations for .agdt/config/
        try:
            from agentic_devtools.cli.setup.gitignore_negations import (
                ensure_root_gitignore_negations,
            )
            from agentic_devtools.state import _get_git_repo_root

            root = git_root or _get_git_repo_root()
            if root:
                ensure_root_gitignore_negations(root)
        except Exception as exc:
            result["warnings"].append(f"Could not update .gitignore negations: {exc}")

    with locked_file(config_path, mode="r+", exclusive=True) as f:
        # Re-read under lock for safety.  The file could have been modified or
        # truncated between the initial read and lock acquisition, so parse
        # defensively and fall back to the pre-lock snapshot on any error.
        f.seek(0)
        content = f.read()
        current: dict[str, Any] = {}
        if content.strip():
            try:
                locked_parsed = json.loads(content)
            except json.JSONDecodeError:
                locked_parsed = None
            if isinstance(locked_parsed, dict):
                current = locked_parsed
            else:
                # Corrupted or non-object JSON under the lock; preserve the
                # pre-lock parsed state to avoid data loss.
                current = dict(existing_config)
        else:
            # Empty file under lock; preserve the pre-lock snapshot to avoid data loss.
            current = dict(existing_config)
        # Apply changes
        for change in changes:
            current[change["key"]] = change["new_value"]

        # Re-validate against the locked snapshot to prevent races where
        # project.json changes between pre-lock read and lock acquisition.
        locked_cross_errors = _cross_field_validate(current, [c["key"] for c in changes])
        if locked_cross_errors:
            result["errors"].extend(locked_cross_errors)
            result["synced_keys"] = []
            return result

        # Write sorted output
        f.seek(0)
        f.write(json.dumps(current, indent=2, sort_keys=True) + "\n")
        f.truncate()

    return result


def sync_back_cmd() -> None:
    """CLI entry point for ``agdt-sync-back``.

    Synchronous command for one-time manual sync-back operation.
    """
    import argparse

    parser = argparse.ArgumentParser(
        prog="agdt-sync-back",
        description="Sync eligible configuration values from worktree state to project.json.",
    )
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        "--keys",
        nargs="+",
        help="Specific project.json keys to sync back.",
    )
    group.add_argument(
        "--all-eligible",
        action="store_true",
        help="Sync all eligible keys that differ from project.json.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show proposed changes without writing to disk.",
    )
    args = parser.parse_args()

    # Expand comma-separated values so both `--keys a,b` and `--keys a b` work.
    keys: list[str] | None = None
    if args.keys is not None:
        keys = []
        seen: set[str] = set()
        for token in args.keys:
            for key in (k.strip() for k in token.split(",") if k.strip()):
                if key in seen:
                    continue
                seen.add(key)
                keys.append(key)
        if not keys:
            parser.error("--keys must include at least one non-empty key")

    if args.all_eligible:
        all_eligible = True
    elif args.keys is None:
        all_eligible = True
    else:
        all_eligible = False

    try:
        result = sync_back(
            keys=keys,
            all_eligible=all_eligible,
            dry_run=args.dry_run,
        )
    except (ValueError, RuntimeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        raise SystemExit(1)

    # Print warnings (suppress the summary warning when synced_keys is empty
    # since that case is reprinted as a dedicated stdout message below).
    synced = result.get("synced_keys", [])
    for warning in result.get("warnings", []):
        if not synced and (warning.startswith("No changes to sync") or warning.startswith("No values were synced")):
            continue
        print(f"Warning: {warning}", file=sys.stderr)

    # Print errors and exit
    if result.get("errors"):
        for error in result["errors"]:
            print(f"Error: {error}", file=sys.stderr)
        raise SystemExit(1)

    # Print results
    if not synced:
        print(
            _no_changes_message(
                all_eligible=all_eligible,
                skipped=result.get("skipped_keys", []),
                unchanged_count=int(result.get("unchanged_count", 0)),
            )
        )
        return

    if args.dry_run:
        print("Dry run — proposed changes (not written):")
    else:
        print("Synced the following keys to project.json:")

    for change in synced:
        old = change.get("old_value")
        new = change.get("new_value")
        old_display = repr(old) if old is not None else "(absent)"
        print(f"  {change['key']}: {old_display} → {new!r}")

    if args.dry_run:
        print("\nRe-run without --dry-run to apply changes.")
