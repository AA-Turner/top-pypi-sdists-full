"""Apply phase for the audit workflow.

Reads agent evaluation output, commits instruction file changes,
creates a draft PR with full reporting, and finalizes batch labels.
"""

from __future__ import annotations

import logging
import os
import re
import shutil
import subprocess
from pathlib import Path

from agentic_devtools.cli.audit.config import batch_branch_name
from agentic_devtools.cli.audit.instruction_size import (
    InstructionFileTooLongError,
    check_instruction_file_sizes,
)
from agentic_devtools.cli.audit.labeling import cleanup_failed_batch, finalize_batch_labels
from agentic_devtools.cli.ci.provider import CIPlatformProvider
from agentic_devtools.cli.ci.scheduler import AUTO_MERGE_LABEL
from agentic_devtools.cli.git.remote_push import commit_and_push_branch

logger = logging.getLogger(__name__)

# Apply outcomes — recorded in the result dict under the "outcome" key so the
# CLI (agdt-audit-apply) can map them to a process exit code and a CI job summary.
OUTCOME_MISSING_OUTPUT = "missing_output"
OUTCOME_INVALID_OUTPUT = "invalid_output"
OUTCOME_NO_CHANGES = "no_changes"
OUTCOME_PR_READY = "pr_ready"
OUTCOME_PR_FAILED = "pr_failed"
OUTCOME_OVERSIZED_INSTRUCTIONS = "oversized_instructions"
OUTCOME_READ_ERROR = "read_error"

# Outcomes that represent a genuine failure (the apply step must exit non-zero).
_SUCCESS_OUTCOMES = frozenset({OUTCOME_NO_CHANGES, OUTCOME_PR_READY})

# File the evaluation agent must always emit. Its absence alongside *no* instruction
# changes signals incomplete/invalid agent output rather than a legitimate no-op.
SUMMARY_REPORT_NAME = "audit-summary-report.md"
# ``AGENTS.md`` is the directory-local filename GitHub reads at any depth.
INSTRUCTION_FILENAMES = ("AGENTS.md",)
# The repository-wide root instruction file is the only ``copilot-instructions.md``
# location GitHub reads. It is accepted in addition to ``AGENTS.md`` so the agent
# can still update it, but it must not be accepted at arbitrary directory depths.
ROOT_COPILOT_INSTRUCTIONS = ".github/copilot-instructions.md"
_COMMIT_SHA_RE = re.compile(r"[0-9a-fA-F]{40}")

_OUTCOME_HEADLINES = {
    OUTCOME_MISSING_OUTPUT: (
        "❌ **Failed** — no `agent-output/` directory was found (the evaluation agent may not have run)."
    ),
    OUTCOME_INVALID_OUTPUT: (
        "❌ **Failed** — `agent-output/` is present but incomplete (no summary report and no instruction changes)."
    ),
    OUTCOME_NO_CHANGES: "✅ **No changes** — the evaluation found no actionable instruction updates.",
    OUTCOME_PR_READY: "✅ **Instruction-update PR ready.**",
    OUTCOME_PR_FAILED: ("❌ **Failed** — instruction changes were detected but the pull request could not be opened."),
    OUTCOME_OVERSIZED_INSTRUCTIONS: (
        "❌ **Failed** — a proposed instruction file exceeds the line cap. Consolidate the file or "
        "move content into a path-scoped instruction file or into `docs/`."
    ),
    OUTCOME_READ_ERROR: (
        "❌ **Failed** — an instruction file could not be read or decoded; the batch has been aborted."
    ),
}


def _extract_pr_number_from_url(pr_url: str) -> int | None:
    """Extract pull request number from a GitHub PR URL."""
    match = re.search(r"/pull/([0-9]+)", pr_url)
    if not match:
        return None
    return int(match.group(1))


def _sanitize_base_sha(base_sha: str, *, batch_id: str) -> str:
    """Return a safe full commit SHA, or empty when the value is invalid.

    The apply flow records full 40-character commit SHAs in ``batch-meta.json``.
    Short SHAs are rejected here so a corrupted value cannot resolve
    ambiguously when used as a git start point.
    """
    normalized = base_sha.strip()
    if not normalized:
        return ""
    if _COMMIT_SHA_RE.fullmatch(normalized):
        return normalized
    logger.warning(
        "Audit batch %s: ignoring invalid base_sha %r; branching off current HEAD "
        "(concurrent-instruction integration disabled for this run)",
        batch_id,
        base_sha,
    )
    return ""


def _iter_instruction_outputs(agent_output_dir: Path) -> list[Path]:
    """Return the instruction files the evaluation agent wrote, sorted by path.

    Recurses for ``AGENTS.md`` at any depth.  ``copilot-instructions.md`` is
    accepted only at its single GitHub-read location
    ``<root>/.github/copilot-instructions.md``; accepting it at arbitrary
    directory depths would allow the apply step to publish guidance to paths
    that no agent reads, recreating the exact problem this PR fixes.
    Sorting keeps the resulting file lists deterministic regardless of
    filesystem iteration order.
    """
    matches: list[Path] = []
    for instruction_filename in INSTRUCTION_FILENAMES:
        matches.extend(agent_output_dir.rglob(instruction_filename))
    root_copilot = agent_output_dir / ROOT_COPILOT_INSTRUCTIONS
    if root_copilot.exists():
        matches.append(root_copilot)
    return sorted(matches)


def apply_audit_results(
    provider: CIPlatformProvider,
    batch_id: str,
    output_dir: str,
    pr_numbers: list[int],
    repo_path: str,
    tracking_issue: int | None = None,
    github_repo: str = "",
    base_sha: str = "",
    eval_pr_branch: str = "",
) -> dict:
    """Apply evaluation agent results and create instruction-update PR.

    Steps:
    1. Read agent output from the batch directory
    2. Detect modified/new instruction files
    3. If changes found: copy files, create branch, commit, and draft PR
    4. If no changes: log summary
    5. Always: finalize batch labels (mark PRs as audited)

    Args:
        provider: CI platform provider instance.
        batch_id: Audit batch identifier.
        output_dir: Path to the batch output directory with agent results.
        pr_numbers: PR numbers in the batch.
        repo_path: Absolute path to the repository root.
        tracking_issue: GitHub issue number to use as commit scope (e.g. 2029).
            When provided together with ``github_repo``, the commit message and
            PR title follow the repository's Conventional Commits convention with
            a plain ``#NNN`` issue scope and a repeated bare ``#NNN`` footer.
        github_repo: ``owner/repo`` string used to construct the authenticated
            remote URL for ``git push`` and to scope the instruction update PR
            to the correct repository. When omitted, instruction PR creation is
            skipped (requires both ``tracking_issue`` and ``github_repo``).
        base_sha: Commit SHA the evaluation was based on. When provided, the
            instruction-update PR is branched off this base so its diff is just
            the eval delta and the AI PR loop's rebase performs a 3-way merge
            that integrates concurrent instruction changes. Empty falls back to
            branching off the current HEAD.
        eval_pr_branch: Head branch of the evaluation PR. Deleted on a successful
            apply to close the (now-consumed) evaluation PR. Empty skips cleanup.

    Returns:
        Summary dict with keys: changes_found, pr_url, files_modified, files_created.
    """
    result = {
        "changes_found": False,
        "pr_url": "",
        "files_modified": [],
        "files_created": [],
        "outcome": OUTCOME_MISSING_OUTPUT,
    }

    out_path = Path(output_dir)
    agent_output_dir = out_path / "agent-output"

    if not agent_output_dir.is_dir():
        logger.warning(
            "No agent output directory found at %s — evaluation may not have run; "
            "releasing in-progress labels so the batch can be retried",
            agent_output_dir,
        )
        result["outcome"] = OUTCOME_MISSING_OUTPUT
        cleanup_failed_batch(provider, pr_numbers, [])
        return result

    # Scan for modified instruction files
    modified_files: list[str] = []
    created_files: list[str] = []
    proposed_contents: list[tuple[str, str]] = []

    agent_output_dir_resolved = agent_output_dir.resolve()
    repo_root_resolved = Path(repo_path).resolve()

    instruction_candidates = set(_iter_instruction_outputs(agent_output_dir))

    for md_file in sorted(instruction_candidates):
        # Guard against symlinks escaping the agent-output directory
        try:
            md_file_resolved = md_file.resolve()
        except OSError:
            logger.warning("Failed to resolve path %s; skipping", md_file)
            continue
        if not md_file_resolved.is_relative_to(agent_output_dir_resolved):
            logger.warning("Skipping symlinked path outside agent-output: %s", md_file)
            continue

        relative = md_file.relative_to(agent_output_dir)
        target_path = Path(repo_path) / relative

        # Guard against symlinks escaping the repository root
        try:
            target_path_resolved = target_path.resolve()
        except OSError:
            logger.warning("Failed to resolve target path %s; skipping", target_path)
            continue
        if not target_path_resolved.is_relative_to(repo_root_resolved):
            logger.warning("Skipping target path outside repo root: %s", target_path)
            continue

        if target_path.is_file():
            try:
                existing = target_path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError) as exc:
                logger.error("Failed to read instruction file (%s): %s", target_path, exc)
                result["outcome"] = OUTCOME_READ_ERROR
                result["error"] = f"Failed to read instruction file ({target_path}): {exc}"
                cleanup_failed_batch(provider, pr_numbers, [])
                return result
            try:
                new_content = md_file.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError) as exc:
                logger.error("Failed to read instruction file (%s): %s", md_file, exc)
                result["outcome"] = OUTCOME_READ_ERROR
                result["error"] = f"Failed to read instruction file ({md_file}): {exc}"
                cleanup_failed_batch(provider, pr_numbers, [])
                return result
            if existing != new_content:
                modified_files.append(relative.as_posix())
                proposed_contents.append((relative.as_posix(), new_content))
        else:
            try:
                file_content = md_file.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError) as exc:
                logger.error("Failed to read instruction file (%s): %s", md_file, exc)
                result["outcome"] = OUTCOME_READ_ERROR
                result["error"] = f"Failed to read instruction file ({md_file}): {exc}"
                cleanup_failed_batch(provider, pr_numbers, [])
                return result
            created_files.append(relative.as_posix())
            proposed_contents.append((relative.as_posix(), file_content))

    # Growth control: instruction files must stay within the line cap. A batch
    # that would push a file over it fails loudly — silently dropping the
    # finding would be worse, and raising the cap is not the remedy.
    try:
        check_instruction_file_sizes(proposed_contents)
    except InstructionFileTooLongError as exc:
        logger.error("Audit batch %s: %s", batch_id, exc)
        result["outcome"] = OUTCOME_OVERSIZED_INSTRUCTIONS
        result["error"] = str(exc)
        cleanup_failed_batch(provider, pr_numbers, [])
        return result

    if not modified_files and not created_files:
        # Distinguish a legitimate no-op (agent ran and decided nothing was
        # actionable, evidenced by its required summary report) from incomplete
        # output (no summary report) which indicates the agent failed silently.
        if not (agent_output_dir / SUMMARY_REPORT_NAME).is_file():
            logger.warning(
                "Audit batch %s: agent-output present but no instruction changes and no %s; "
                "evaluation output looks incomplete — releasing in-progress labels for retry",
                batch_id,
                SUMMARY_REPORT_NAME,
            )
            result["outcome"] = OUTCOME_INVALID_OUTPUT
            cleanup_failed_batch(provider, pr_numbers, [])
            return result
        logger.info("No instruction file changes detected — batch %s complete", batch_id)
        result["outcome"] = OUTCOME_NO_CHANGES
        finalize_batch_labels(provider, pr_numbers)
        _cleanup_batch_branch(provider, batch_id)
        _cleanup_eval_pr_branch(provider, eval_pr_branch)
        return result

    result["changes_found"] = True
    result["files_modified"] = modified_files
    result["files_created"] = created_files

    # Build PR description
    description = build_pr_description(batch_id, pr_numbers, modified_files, created_files, out_path)

    # Apply changes: copy files, create branch, commit, and open draft PR
    pr_url = ""
    try:
        pr_url = _create_instruction_pr(
            repo_path=repo_path,
            batch_id=batch_id,
            modified_files=modified_files,
            created_files=created_files,
            agent_output_dir=agent_output_dir,
            description=description,
            provider=provider,
            tracking_issue=tracking_issue,
            github_repo=github_repo,
            base_sha=base_sha,
        )
    except Exception:
        # Broad catch is intentional: _create_instruction_pr performs filesystem
        # operations (shutil.copy2, mkdir) and calls provider.create_pull_request()
        # which may raise arbitrary provider-specific exceptions. Any failure here
        # must release the in-progress labels so the batch can be retried.
        logger.exception(
            "Audit batch %s: unexpected error during instruction-update PR creation; "
            "releasing in-progress labels for retry",
            batch_id,
        )
        result["outcome"] = OUTCOME_PR_FAILED
        cleanup_failed_batch(provider, pr_numbers, [])
        return result

    result["pr_url"] = pr_url

    logger.info(
        "Audit batch %s: %d files modified, %d files created. PR: %s",
        batch_id,
        len(modified_files),
        len(created_files),
        pr_url,
    )

    if pr_url:
        # PR created (or reused) successfully — mark PRs as audited so they are not re-processed
        result["outcome"] = OUTCOME_PR_READY
        finalize_batch_labels(provider, pr_numbers)
        _cleanup_batch_branch(provider, batch_id)
        _cleanup_eval_pr_branch(provider, eval_pr_branch)
    else:
        # PR creation failed — release the in-progress lock so the batch can be retried
        result["outcome"] = OUTCOME_PR_FAILED
        logger.warning(
            "Audit batch %s: instruction-update PR creation failed; releasing in-progress labels for retry",
            batch_id,
        )
        cleanup_failed_batch(provider, pr_numbers, [])

    return result


def _cleanup_batch_branch(provider: CIPlatformProvider, batch_id: str) -> None:
    """Best-effort deletion of the staging batch branch after a successful apply.

    Deleting ``audit/batch-<id8>`` also auto-closes the evaluation agent's
    staging pull request, whose head is that branch. Failures are logged but
    never raised: the apply deliverable has already succeeded, so a cleanup
    hiccup must not turn it into a failure.

    Args:
        provider: CI platform provider instance.
        batch_id: Audit batch identifier.
    """
    branch = batch_branch_name(batch_id)
    try:
        provider.delete_branch(branch)
    except Exception:
        logger.warning(
            "Audit batch %s: failed to delete staging branch %s (manual cleanup may be needed)",
            batch_id,
            branch,
            exc_info=True,
        )


def _cleanup_eval_pr_branch(provider: CIPlatformProvider, eval_pr_branch: str) -> None:
    """Best-effort deletion of the evaluation PR's head branch after a successful apply.

    Deleting the ``copilot/**`` evaluation branch auto-closes the evaluation PR,
    whose purpose (handing the agent-output back for apply) is now complete. A
    no-op when ``eval_pr_branch`` is empty. Failures are logged but never raised:
    the apply deliverable has already succeeded, so a cleanup hiccup must not turn
    it into a failure.

    Args:
        provider: CI platform provider instance.
        eval_pr_branch: Head branch of the evaluation PR (empty to skip).
    """
    if not eval_pr_branch:
        return
    try:
        provider.delete_branch(eval_pr_branch)
    except Exception:
        logger.warning(
            "Failed to delete evaluation PR branch %s after apply (manual cleanup may be needed)",
            eval_pr_branch,
            exc_info=True,
        )


def _create_instruction_pr(
    repo_path: str,
    batch_id: str,
    modified_files: list[str],
    created_files: list[str],
    agent_output_dir: Path,
    description: str,
    provider: CIPlatformProvider,
    tracking_issue: int | None = None,
    github_repo: str = "",
    base_sha: str = "",
) -> str:
    """Copy agent output files, create a git branch, commit, and open a draft PR.

    Files are copied into the working tree only *after* the branch is created.
    This ensures that a branch-creation failure leaves the original branch clean.

    Args:
        repo_path: Absolute path to the repository root.
        batch_id: Audit batch identifier (used in branch name and commit message).
        modified_files: Repo-relative paths of instruction files to update.
        created_files: Repo-relative paths of new instruction files to create.
        agent_output_dir: Directory containing the agent output files.
        description: Markdown body for the draft PR.
        provider: CI platform provider used to create the pull request.
        tracking_issue: GitHub issue number for the commit scope (e.g. 2029).
            Required together with ``github_repo`` so the commit message
            follows the repository Conventional Commits convention with a plain
            ``#NNN`` issue scope and a repeated bare ``#NNN`` footer (GitHub
            auto-links bare issue references).
        github_repo: ``owner/repo`` string used to construct the authenticated
            remote URL for ``git push``. Required together with
            ``tracking_issue`` to push the branch and open the draft PR on
            GitHub (both are needed for the full instruction-update flow).

    Returns:
        URL of the created draft PR, or empty string if PR creation failed.
    """
    if not batch_id:
        logger.error("batch_id must not be empty")
        return ""

    # Validate required args before any filesystem or git operations
    if not tracking_issue or not github_repo:
        logger.error(
            "Missing required --tracking-issue/--repo for instruction update PR "
            "(tracking_issue is needed for the commit scope/footer; "
            "github_repo is needed to push the branch to GitHub)."
        )
        return ""

    # Validate all relative paths to prevent path traversal
    all_changed = modified_files + created_files
    repo_root = Path(repo_path).resolve()
    for rel_path in all_changed:
        p = Path(rel_path)
        if p.is_absolute() or ".." in p.parts:
            logger.error("Rejected unsafe path in agent output: %s", rel_path)
            return ""
        resolved = (repo_root / p).resolve()
        if not resolved.is_relative_to(repo_root):
            logger.error("Path escapes repository root: %s", rel_path)
            return ""

    branch_name = f"audit/instruction-update-{batch_id[:8]}"

    # SPECKIT_PR_TOKEN (exposed as GH_TOKEN in the apply workflow) is only needed
    # for PR creation, not for the push.  The push uses the ambient GITHUB_TOKEN
    # credentials persisted by actions/checkout (contents: write on the job).
    # We validate early so we fail fast before any git work.
    gh_token = (os.environ.get("GH_TOKEN") or "").strip() or (os.environ.get("SPECKIT_PR_TOKEN") or "").strip()
    if not gh_token:
        logger.error("GH_TOKEN (or SPECKIT_PR_TOKEN) is required for pull request creation in audit apply.")
        return ""
    # Always normalise GH_TOKEN to the final stripped value so `gh pr create` can
    # authenticate regardless of which variable the token came from.  This also
    # handles the edge case where GH_TOKEN was set to whitespace only: stripping
    # it above yielded "" and we fell back to SPECKIT_PR_TOKEN, so we must update
    # GH_TOKEN to reflect the resolved token.
    os.environ["GH_TOKEN"] = gh_token

    def _run_git_capture(step: str, *args: str) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            ["git", "-C", repo_path, *args],
            capture_output=True,
            text=True,
            shell=False,
        )
        if result.returncode != 0:
            logger.error(
                "git %s failed (step: %s): %s",
                args[0] if args else "",
                step,
                result.stderr.strip(),
            )
            raise subprocess.CalledProcessError(
                result.returncode,
                ["git", "-C", repo_path, *args],
                output=None,
                stderr=result.stderr,
            )
        return result

    def _run_git(step: str, *args: str) -> None:
        _run_git_capture(step, *args)

    try:
        # Intentionally synchronous git/PR creation: delegating this to a coding-agent
        # branch would risk recursive apply triggers with the widened copilot/**
        # branch filter plus audit-batches/**/agent-output/** path filter.
        # Create the branch first so that any failure here leaves the original
        # branch clean (no copied files to clean up).
        # Branch the instruction-update PR off the evaluation's base commit (when
        # known) so the commit's diff is just the eval delta. The AI PR loop then
        # rebases it onto current main, performing a git 3-way merge that
        # integrates concurrent copilot-instructions changes instead of clobbering
        # them. Fall back to the current HEAD when base_sha is absent or cannot be
        # fetched.
        start_point = ""
        sanitized_base_sha = _sanitize_base_sha(base_sha, batch_id=batch_id)
        if sanitized_base_sha:
            try:
                _run_git("fetch base", "fetch", "--depth=1", "origin", sanitized_base_sha)
                start_point = sanitized_base_sha
            except subprocess.CalledProcessError:
                logger.warning(
                    "Audit batch %s: could not fetch base_sha %s; branching off current HEAD "
                    "(concurrent-instruction integration disabled for this run)",
                    batch_id,
                    sanitized_base_sha[:8],
                )
        if start_point:
            _run_git("create branch", "checkout", "-B", branch_name, start_point)
        else:
            _run_git("create branch", "checkout", "-B", branch_name)

        # The apply workflow materializes audit-batches/** into this working tree
        # via `git checkout <ref> -- <path>`, which stages those paths in the
        # index. Clear staged audit-batches paths so the instruction-update
        # commit can only contain the intended instruction file paths, while
        # preserving worktree files used as copy sources.
        materialized_status = _run_git_capture(
            "detect materialized audit-batches",
            "diff",
            "--name-only",
            "--cached",
            "--",
            "audit-batches",
        )
        if materialized_status.stdout.strip():
            _run_git(
                "clear materialized audit-batches",
                "restore",
                "--staged",
                "--",
                "audit-batches",
            )

        # Copy agent output files to the repository only after branch creation
        # succeeds, so failures during copy or subsequent git steps are isolated
        # to the new branch.
        # Guard: reject a symlinked agent_output_dir before resolving or copying.
        # If the directory itself is a symlink, .resolve() follows it to an external
        # target; every per-file is_relative_to() check would then pass even when
        # reading files from an arbitrary runner path (the resolved target), bypassing
        # the containment check entirely.
        if agent_output_dir.is_symlink():
            logger.error("Rejected symlinked agent_output_dir: %s", agent_output_dir)
            return ""
        try:
            resolved_agent_output_dir = agent_output_dir.resolve()
        except OSError:
            logger.error("Could not resolve agent_output_dir: %s", agent_output_dir)
            return ""
        for rel_path in all_changed:
            src = agent_output_dir / rel_path
            dst = repo_root / rel_path
            # Guard against symlinks and sources that resolve outside agent_output_dir.
            # agent-output files are materialised from the untrusted eval-PR head in a
            # pull_request_target context; a malicious PR could introduce symlinks
            # pointing at arbitrary runner files (e.g. /proc/self/environ) and leak
            # secrets via shutil.copy2's symlink-following behaviour.
            if src.is_symlink():
                logger.error("Rejected symlink in agent output: %s", rel_path)
                return ""
            try:
                resolved_src = src.resolve()
            except OSError:
                logger.error("Could not resolve source path: %s", rel_path)
                return ""
            if not resolved_src.is_relative_to(resolved_agent_output_dir):
                logger.error("Source path escapes agent_output_dir: %s", rel_path)
                return ""
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(str(src), str(dst))

        scope = f"(#{tracking_issue})"
        commit_msg = (
            f"chore{scope}: update coding instructions from audit batch {batch_id[:8]}\n\n"
            f"Modified: {len(modified_files)} file(s), Created: {len(created_files)} file(s)\n\n"
            f"#{tracking_issue}"
        )
        pr_title = f"chore{scope}: update coding instructions from audit {batch_id[:8]}"

        # Branch is already checked out above; skip_checkout=True delegates only
        # the stage → config → commit → push steps to the shared helper.
        # Push authenticates using the ambient GITHUB_TOKEN credentials persisted
        # by actions/checkout (the apply-audit job has contents: write).
        commit_and_push_branch(
            repo_path=repo_path,
            branch=branch_name,
            add_paths=all_changed,
            commit_message=commit_msg,
            force=True,
            skip_checkout=True,
        )

        # `gh pr create` determines the repository from the git remote in the
        # current working directory.  Change into the repository before calling
        # the provider so the PR is created in the correct repository regardless
        # of where `agdt-audit-apply` was invoked from.
        original_cwd = os.getcwd()
        try:
            os.chdir(repo_path)
            pr_url = provider.create_pull_request(title=pr_title, body=description)
        finally:
            os.chdir(original_cwd)
        if pr_url:
            pr_number = _extract_pr_number_from_url(pr_url)
            if pr_number:
                try:
                    provider.add_label(pr_number, AUTO_MERGE_LABEL)
                except Exception as exc:
                    logger.warning(
                        "Failed to add auto-merge label to instruction PR #%d: %s",
                        pr_number,
                        exc,
                    )
        return pr_url

    except subprocess.CalledProcessError:
        return ""


def build_pr_description(
    batch_id: str,
    pr_numbers: list[int],
    modified_files: list[str],
    created_files: list[str],
    output_dir: Path,
) -> str:
    """Build a structured PR description for the instruction-update PR.

    Includes audited PR numbers, statistics, file changes, and references.

    Args:
        batch_id: Audit batch identifier.
        pr_numbers: PR numbers that were audited.
        modified_files: List of modified instruction file paths.
        created_files: List of newly created instruction file paths.
        output_dir: Path to batch output for reading summary.

    Returns:
        Formatted PR description as Markdown string.
    """
    lines = [
        "## Review Feedback Audit — Instruction Updates",
        "",
        f"**Batch ID:** `{batch_id}`",
        f"**PRs audited:** {len(pr_numbers)}",
        f"**Files modified:** {len(modified_files)}",
        f"**Files created:** {len(created_files)}",
        "",
        "### Audited PRs",
        "",
    ]

    for pr_num in pr_numbers:
        lines.append(f"- #{pr_num}")

    if modified_files:
        lines.extend(["", "### Modified Files", ""])
        for f in modified_files:
            lines.append(f"- `{f}`")

    if created_files:
        lines.extend(["", "### Newly Created Files", ""])
        for f in created_files:
            lines.append(f"- `{f}` *(new)*")

    # Read summary report if available
    summary_path = output_dir / "agent-output" / "audit-summary-report.md"
    if summary_path.is_file():
        try:
            summary_content = summary_path.read_text(encoding="utf-8")
            lines.extend(["", "### Agent Summary", "", summary_content])
        except (OSError, UnicodeDecodeError):
            pass

    lines.extend(
        [
            "",
            "---",
            "",
            "This PR is eligible for automated processing by the AI PR loop when the "
            "`ai-auto-merge-allowed` label is present.",
        ]
    )

    return "\n".join(lines)


def apply_result_is_failure(result: dict) -> bool:
    """Return True when an apply result represents a genuine failure.

    A missing ``outcome`` key is treated as a failure so that an invalid or
    partial result dict does not silently pass.  Any outcome string that is not
    one of the recognised success outcomes is also treated as a failure so that
    unknown or future outcome values fail loudly rather than silently passing.

    Args:
        result: Result dict produced by :func:`apply_audit_results`.

    Returns:
        True if the outcome key is missing, or if the outcome value is absent
        from the success set (including unknown outcome strings). False only for
        the recognised success outcomes.
    """
    outcome = result.get("outcome")
    if outcome is None:
        return True
    return outcome not in _SUCCESS_OUTCOMES


def render_apply_summary(result: dict) -> str:
    """Render a Markdown summary of an apply result for the CI job summary.

    Args:
        result: Result dict produced by :func:`apply_audit_results`.

    Returns:
        Markdown string suitable for appending to ``$GITHUB_STEP_SUMMARY``.
    """
    outcome = result.get("outcome", "")
    headline = _OUTCOME_HEADLINES.get(outcome, f"Audit apply — `{outcome or 'unknown'}`")
    lines = ["## Review Feedback Audit — Apply", "", headline, ""]

    pr_url = result.get("pr_url") or ""
    if pr_url:
        lines.append(f"- **Instruction-update PR:** {pr_url}")

    modified = result.get("files_modified") or []
    created = result.get("files_created") or []
    lines.append(f"- **Files modified:** {len(modified)}")
    lines.append(f"- **Files created:** {len(created)}")
    for path in modified:
        lines.append(f"  - `{path}` (modified)")
    for path in created:
        lines.append(f"  - `{path}` (new)")

    return "\n".join(lines) + "\n"
