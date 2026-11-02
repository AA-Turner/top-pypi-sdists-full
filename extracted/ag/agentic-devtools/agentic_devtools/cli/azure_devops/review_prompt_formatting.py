"""Format review prompt files and console instructions."""

import json
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .review_state import FileEntry


def _write_file_prompt(directory: Path, file_detail: dict, threads_for_file: list) -> Path:
    """Write a file review prompt to disk."""
    from .review_helpers import (
        build_full_file_content_section,
        convert_to_prompt_filename,
        resolve_repository_root,
    )

    filename = convert_to_prompt_filename(file_detail.get("path", ""))
    prompt_path = directory / filename

    file_json = json.dumps(file_detail, indent=2, ensure_ascii=False)
    threads_json = json.dumps(threads_for_file, indent=2, ensure_ascii=False) if threads_for_file else "[]"

    lines = [
        f"# File Review: {file_detail.get('path', 'unknown')}",
        "",
        "## File Diff Object",
        "",
        "```json",
        file_json,
        "```",
        "",
        "## Existing Threads",
        "",
        "```json",
        threads_json,
        "```",
    ]

    lines.extend(
        build_full_file_content_section(
            file_path=file_detail.get("path", ""),
            change_type=file_detail.get("changeType", "edit"),
            repo_root=resolve_repository_root(),
        )
    )

    prompt_path.write_text("\n".join(lines), encoding="utf-8")
    return prompt_path


def _write_unchanged_file_prompt(directory: Path, file_detail: dict, prior_entry: FileEntry | None) -> Path:
    """Write a simplified file review prompt for an unchanged file.

    For files with no changes since the last review and a valid prior state,
    this produces a minimal prompt instructing the AI agent to only submit
    a review if their assessment differs from the prior review.

    Args:
        directory: Directory to write the prompt file.
        file_detail: File detail dictionary from the PR payload.
        prior_entry: The prior FileEntry with review state, or None.

    Returns:
        Path to the written prompt file.
    """
    from .review_helpers import convert_to_prompt_filename

    filename = convert_to_prompt_filename(file_detail.get("path", ""))
    prompt_path = directory / filename

    file_path = file_detail.get("path", "unknown")
    prior_status = prior_entry.status if prior_entry else "unknown"
    prior_summary = prior_entry.summary if prior_entry else None

    lines = [
        f"# File Review: {file_path}",
        "",
        "## Status",
        "",
        "no changes since last review",
        "",
        f"**Prior review status:** {prior_status}",
    ]

    if prior_summary:
        lines.extend(["", f"**Prior review summary:** {prior_summary}"])

    lines.extend(
        [
            "",
            "## Instructions",
            "",
            "This file has not changed since the last review. The prior review outcome is shown above.",
            "Still perform an independent review of this file, but **only submit** a review",
            "(via `agdt-file-review-write`) if your assessment **differs** from the prior review.",
            "If your assessment matches the prior review, skip submission — the file is already correctly reviewed.",
        ]
    )

    prompt_path.write_text("\n".join(lines), encoding="utf-8")
    return prompt_path


def print_review_instructions(
    pull_request_id: int,
    prompts_dir: Path,
    prompts_generated: int,
    skipped_not_on_branch_count: int = 0,
) -> None:
    """Print instructions for the AI agent to follow."""
    _print_review_summary(pull_request_id, prompts_dir, prompts_generated, skipped_not_on_branch_count)
    _print_shared_context()
    _print_console_checklist()
    _print_delegation_instructions()
    _print_important_notes(prompts_generated)


def _print_review_summary(
    pull_request_id: int,
    prompts_dir: Path,
    prompts_generated: int,
    skipped_not_on_branch_count: int,
) -> None:
    """Print the run summary shown before the review instructions."""
    from ..workflows.base import _safe_print

    print("")
    print("=" * 60)
    print("PULL REQUEST REVIEW WORKFLOW")
    print("=" * 60)
    print("")
    print(f"PR ID: {pull_request_id}")
    print(f"Prompts generated: {prompts_generated}")
    if skipped_not_on_branch_count > 0:
        print(f"Skipped (not on branch, from merged PRs): {skipped_not_on_branch_count}")
    _safe_print(f"Prompts directory: {prompts_dir}")


def _print_shared_context() -> None:
    """List the generated artifacts available to every file reviewer."""
    from ..workflows.base import _safe_print

    print("")
    print("=" * 60)
    print("SHARED CONTEXT FOR THIS REVIEW")
    print("=" * 60)
    print("")
    print("Review snapshots are saved in the prompts folder:")
    _safe_print("  • pull-request-files.json - All files in the PR diff")
    _safe_print("  • pull-request-threads.json - Existing comment threads")
    _safe_print("  • pull-request-jira-issue.json - Linked Jira issue details")
    print("")
    print("Keep analysis scoped to one file at a time; use shared artifacts for background context.")
    print("")


def _print_console_checklist() -> None:
    """Print the steps that reviewers should follow for each file."""
    print("=" * 60)
    print("CONSOLE CHECKLIST (for each file)")
    print("=" * 60)
    print("")
    print("1. Open the file prompt and analyze the diff + any existing threads.")
    print("2. Verify repository conventions/invariants for that file and capture concrete feedback.")
    print("3. Post the review with the appropriate command; let the queue advance automatically.")
    print("")


def _print_delegation_instructions() -> None:
    """Print the handoff instructions for the file review queue."""
    print("=" * 60)
    print("NEXT STEP: FILE REVIEW DELEGATION")
    print("=" * 60)
    print("")
    print("The file review queue and per-file prompts are ready.")
    print("")
    print("Hand off to the PR review orchestrator to synthesize PR context,")
    print("triage review depth, and delegate each file to a file-reviewer subagent.")
    print("Each file-reviewer records its verdict with the atomic answer write:")
    print("")
    print("    agdt-file-review-write --file-key <fileKey> --answer-file <path-to-draft.json>")
    print("")


def _print_important_notes(prompts_generated: int) -> None:
    """Print final queue and completion guidance."""
    from ..workflows.base import _safe_print

    print("=" * 60)
    print("IMPORTANT NOTES")
    print("=" * 60)
    print("")
    _safe_print("• After reviewing the final file, the overarching PR comments will be")
    print("  generated automatically. This may take up to 30 seconds.")
    _safe_print("• DO NOT RUN ANY COMMANDS after submitting the final file review!")
    print("  Wait for the process to complete.")
    _safe_print("• After all files are reviewed, provide a summary of your findings.")
    print("")

    if prompts_generated == 0:
        print("WARNING: No prompts were generated. All files may have been skipped (not on branch).")
    else:
        print("Ready to begin review. Process the queue starting with the first pending file.")
