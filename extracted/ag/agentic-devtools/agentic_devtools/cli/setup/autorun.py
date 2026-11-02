"""Autorun orchestration for the generated ``setup-dev-tools.py``.

This module provides ``_autorun_setup_dev_tools``, a helper that invokes the
freshly-generated root entry-point script as the final phase of ``agdt-setup``,
enabling one-command setup. A recursion guard (the ``AGDT_SETUP_AUTORUN``
environment marker) prevents unbounded re-entry if the generated script ever
calls back into ``agdt-setup``.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from ..subprocess_utils import run_safe
from .autorun_resolution import get_workflow_suppression_reason
from .phase_markers import EXECUTION_END, EXECUTION_START, emit_phase_marker
from .phases import AUTORUN_SETUP_PHASE
from .report import PhaseResult, SetupReport
from .script_generators.constants import ORCHESTRATOR_MARKER, ROOT_ENTRY_POINT_FILENAME

_AUTORUN_MARKER = "AGDT_SETUP_AUTORUN"
_TARGET_REPO_ROOT_ENV = "AGDT_SETUP_TARGET_REPO_ROOT"
_PHASE_NAME = AUTORUN_SETUP_PHASE
_MANUAL_COMMAND_HINT = "run `python setup-dev-tools.py` manually once the workflow step is complete"


def _run_generated_script(script_path: Path, child_env: dict[str, str]) -> subprocess.CompletedProcess:
    """Run the generated setup script, bracketed by the execution phase markers.

    The child inherits the parent's stdout/stderr, so its output is streamed in
    real time between the ``execution:start`` and ``execution:end`` markers.
    ``execution:end`` is emitted even when the invocation raises, keeping the
    markers balanced for log parsers.
    """
    emit_phase_marker(EXECUTION_START)
    try:
        return run_safe(
            [sys.executable, str(script_path), "--foreground"],
            shell=False,
            env=child_env,
            check=True,
        )
    finally:
        emit_phase_marker(EXECUTION_END)


def _autorun_setup_dev_tools(
    *,
    autorun_enabled: bool,
    git_root: Path | None,
    system_only: bool,
    skip_repo_steps: bool,
    report: SetupReport,
    branch_created: str | None = None,
    explicit_run: bool = False,
) -> bool:
    """Invoke the generated ``setup-dev-tools.py`` as a child process.

    Returns ``True`` when the child process was actually invoked (regardless of
    its exit code) and ``False`` when invocation was skipped or aborted before
    the child started. The return value lets callers gate post-invocation
    checks (such as a version comparison) on child invocation rather than on
    the phase status alone, because a pre-invocation failure (e.g. a worktree
    creation error) still records ``failed`` in the report without having run
    the child.

    The helper refuses to run when the ``AGDT_SETUP_AUTORUN`` marker is already
    present in the current environment (recursion guard). It also skips when any
    of the standard skip conditions hold, including when a scaffolding workflow
    step is active or when ``branch_created`` is a non-empty string (indicating
    the PR workflow committed changes to a review branch). Those two suppression
    signals — and only those — are overridden by *explicit_run* (``--run``),
    which downgrades the skip to a stderr warning. On success or failure the
    outcome is recorded in the setup report; exceptions are never propagated.

    When *explicit_run* overrides the ``branch_created`` suppression, the
    freshly-generated script is run from a temporary detached worktree of
    ``branch_created`` (see :func:`_run_from_created_branch`), because the PR
    workflow committed the new files to that branch and restored the user's
    original branch — so the working tree no longer holds the new script.
    """
    # --- Recursion guard (FR-002) ---
    if _AUTORUN_MARKER in os.environ:
        report.record(
            PhaseResult(
                name=_PHASE_NAME,
                status="skipped",
                error="Recursion guard: AGDT_SETUP_AUTORUN already set in environment",
            )
        )
        print(
            "  ℹ Autorun skipped: recursion guard (AGDT_SETUP_AUTORUN already set)",
            file=sys.stderr,
        )
        return False

    # --- Skip conditions (FR-003) ---
    if not autorun_enabled:
        report.record(
            PhaseResult(
                name=_PHASE_NAME,
                status="skipped",
                error="autorun_enabled is false",
            )
        )
        print("  ℹ Autorun skipped: autorun is disabled", file=sys.stderr)
        return False

    if git_root is None:
        report.record(
            PhaseResult(
                name=_PHASE_NAME,
                status="skipped",
                error="git_root is None",
            )
        )
        print("  ℹ Autorun skipped: not in a git repository", file=sys.stderr)
        return False

    if system_only:
        report.record(
            PhaseResult(
                name=_PHASE_NAME,
                status="skipped",
                error="--system-only is set",
            )
        )
        print("  ℹ Autorun skipped: --system-only mode", file=sys.stderr)
        return False

    if skip_repo_steps:
        report.record(
            PhaseResult(
                name=_PHASE_NAME,
                status="skipped",
                error="skip_repo_steps is set",
            )
        )
        print("  ℹ Autorun skipped: repo steps are skipped", file=sys.stderr)
        return False

    # --- Branch-created skip (PR-workflow interaction) ---
    # When a setup branch was created, the PR workflow restored the caller's
    # original branch, so ``setup-dev-tools.py`` may be absent or stale in the
    # working tree. This suppression must be evaluated first so that non-explicit
    # runs receive the correct "review & merge" remediation hint rather than the
    # workflow-step hint (which references a possibly-missing script).
    suppression_reason = get_workflow_suppression_reason()
    if branch_created:
        if explicit_run:
            # Both suppressions may apply. Emit all relevant warnings so the
            # user understands what was overridden, then run from the created
            # branch (which holds the fresh generated files).
            if suppression_reason:
                print(
                    f"  ⚠ Auto-run forced by --run even though {suppression_reason}.",
                    file=sys.stderr,
                )
            print(
                f"  ⚠ Auto-run forced by --run even though setup branch '{branch_created}' was created.",
                file=sys.stderr,
            )
            # The PR workflow committed the freshly-generated files to
            # ``branch_created`` and restored the user's original branch, so the
            # working tree no longer contains the new script. Run it from the
            # created branch instead of the restored checkout.
            return _run_from_created_branch(branch_created, git_root, report)
        else:
            _msg = (
                f"Auto-run skipped: setup branch '{branch_created}' was created"
                " — review & merge the setup PR, then run `python setup-dev-tools.py`"
            )
            report.record(
                PhaseResult(
                    name=_PHASE_NAME,
                    status="skipped",
                    error=_msg,
                )
            )
            print(f"  ℹ {_msg}", file=sys.stderr)
            return False

    # --- Workflow-state suppression (PR/issue workflow interaction) ---
    if suppression_reason:
        if explicit_run:
            print(
                f"  ⚠ Auto-run forced by --run even though {suppression_reason}.",
                file=sys.stderr,
            )
        else:
            _msg = f"Auto-run skipped: {suppression_reason} — {_MANUAL_COMMAND_HINT}"
            report.record(
                PhaseResult(
                    name=_PHASE_NAME,
                    status="skipped",
                    error=_msg,
                )
            )
            print(f"  ℹ {_msg}")
            return False

    return _locate_and_run(git_root, report)


def _run_from_created_branch(branch: str, target_repo_root: Path, report: SetupReport) -> bool:
    """Run the freshly-generated entry-point from *branch* in an isolated worktree.

    Returns ``True`` when the child process was actually invoked (regardless of
    its exit code) and ``False`` when invocation was skipped or aborted before
    the child started (including worktree creation failure and entry-point
    validation skips). See :func:`_autorun_setup_dev_tools` for the semantics
    of this return value.

    The PR workflow committed the generated files to *branch* and restored the
    user's original branch, so the working tree no longer contains the fresh
    script. A temporary detached ``git worktree`` provides a complete, consistent
    checkout of the generated artifacts (orchestrator plus its sibling scripts)
    without mutating the user's working tree. The generated script still targets
    *target_repo_root* as the effective repository root so setup outputs are
    applied to the user's real checkout. The worktree is always removed
    afterwards, even when the invocation fails.
    """
    from agentic_devtools.cli.git.core import run_git

    def _phase_status() -> str | None:
        """Return the currently recorded autorun phase status, if any."""
        for phase in report.phases:
            if phase.name == _PHASE_NAME:
                return phase.status
        return None

    tmp_parent = tempfile.mkdtemp(prefix="agdt-setup-autorun-")
    worktree_dir = os.path.join(tmp_parent, "worktree")

    add_result = run_git("worktree", "add", "--detach", worktree_dir, branch, check=False)
    if add_result.returncode != 0:
        report.record(
            PhaseResult(
                name=_PHASE_NAME,
                status="failed",
                error=f"Could not create worktree for branch '{branch}': {add_result.stderr.strip()}",
            )
        )
        print(
            f"  ✗ Autorun failed: could not check out branch '{branch}' to run the generated script",
            file=sys.stderr,
        )
        shutil.rmtree(tmp_parent, ignore_errors=True)
        return False

    child_invoked = False
    try:
        child_invoked = _locate_and_run(Path(worktree_dir), report, target_repo_root=target_repo_root)
    finally:
        remove_result = run_git("worktree", "remove", "--force", worktree_dir, check=False)
        shutil.rmtree(tmp_parent, ignore_errors=True)
        if remove_result.returncode != 0:
            # ``git worktree remove`` failed, but the temporary directory was
            # deleted anyway. Git would otherwise keep a registered worktree
            # pointing at a now-missing path, so prune the stale metadata to
            # keep Git's worktree list consistent.
            prune_result = run_git("worktree", "prune", "--expire", "now", check=False)
            if prune_result.returncode != 0:
                cleanup_error = (
                    "Worktree cleanup failed after autorun: "
                    f"remove returned {remove_result.returncode}; "
                    f"prune returned {prune_result.returncode}"
                )
                print(f"  ✗ Autorun cleanup failed: {cleanup_error}", file=sys.stderr)
                # Do not overwrite an existing child-invocation failure.
                if _phase_status() != "failed":
                    report.record(
                        PhaseResult(
                            name=_PHASE_NAME,
                            status="failed",
                            error=cleanup_error,
                        )
                    )
    return child_invoked


def _locate_and_run(
    script_root: Path,
    report: SetupReport,
    *,
    target_repo_root: Path | None = None,
) -> bool:
    """Validate the generated entry-point under *script_root* and invoke it.

    Resolves ``setup-dev-tools.py`` relative to *script_root* (the repository
    root for a normal run, or a temporary worktree when ``--run`` overrides the
    branch-created suppression), validates it is a managed orchestrator, and runs
    it. All outcomes are recorded in *report*; exceptions from the child process
    are never propagated.
    """
    # --- Entry-point validation (FR-004) ---
    script_path = script_root / ROOT_ENTRY_POINT_FILENAME

    if not script_path.is_file():
        report.record(
            PhaseResult(
                name=_PHASE_NAME,
                status="skipped",
                error=f"Root entry-point missing: {script_path}",
            )
        )
        print(
            f"  ⚠ Autorun skipped: {ROOT_ENTRY_POINT_FILENAME} not found",
            file=sys.stderr,
        )
        return False

    # Check if the script is a legacy variant (no ORCHESTRATOR_MARKER)
    try:
        content = script_path.read_text(encoding="utf-8")
    except OSError as exc:
        report.record(
            PhaseResult(
                name=_PHASE_NAME,
                status="skipped",
                error=f"Root entry-point unreadable: {exc}",
            )
        )
        print(
            f"  ⚠ Autorun skipped: {ROOT_ENTRY_POINT_FILENAME} is unreadable",
            file=sys.stderr,
        )
        return False
    except UnicodeDecodeError as exc:
        report.record(
            PhaseResult(
                name=_PHASE_NAME,
                status="skipped",
                error=f"Root entry-point has non-UTF-8 content: {exc}",
            )
        )
        print(
            f"  ⚠ Autorun skipped: {ROOT_ENTRY_POINT_FILENAME} has non-UTF-8 content",
            file=sys.stderr,
        )
        return False

    if ORCHESTRATOR_MARKER not in content:
        report.record(
            PhaseResult(
                name=_PHASE_NAME,
                status="skipped",
                error="Root entry-point is a legacy variant (no orchestrator marker)",
            )
        )
        print(
            f"  ⚠ Autorun skipped: {ROOT_ENTRY_POINT_FILENAME} is a legacy script",
            file=sys.stderr,
        )
        return False

    # --- Invocation (FR-001, FR-007) ---
    child_env = os.environ.copy()
    child_env[_AUTORUN_MARKER] = "1"
    child_env["PYTHONUNBUFFERED"] = "1"
    if target_repo_root is not None:
        child_env[_TARGET_REPO_ROOT_ENV] = str(target_repo_root)

    try:
        result = _run_generated_script(script_path, child_env)
    except subprocess.CalledProcessError as exc:
        report.record(
            PhaseResult(
                name=_PHASE_NAME,
                status="failed",
                error=f"Child process exited with code {exc.returncode}",
            )
        )
        print(
            f"  ✗ Autorun failed: child process exited with code {exc.returncode}",
            file=sys.stderr,
        )
        return True
    except OSError as exc:
        report.record(
            PhaseResult(
                name=_PHASE_NAME,
                status="failed",
                error=f"OS error invoking setup script: {exc}",
            )
        )
        print(f"  ✗ Autorun failed: {exc}", file=sys.stderr)
        return True
    except Exception as exc:  # noqa: BLE001
        report.record(
            PhaseResult(
                name=_PHASE_NAME,
                status="failed",
                error=f"Unexpected error: {exc}",
            )
        )
        print(f"  ✗ Autorun failed: {exc}", file=sys.stderr)
        return True

    # Normal return path — check returncode (FR-005)
    if result.returncode != 0:
        report.record(
            PhaseResult(
                name=_PHASE_NAME,
                status="failed",
                error=f"Child process exited with code {result.returncode}",
            )
        )
        print(
            f"  ✗ Autorun failed: child process exited with code {result.returncode}",
            file=sys.stderr,
        )
        return True

    # --- Success (FR-005, FR-009) ---
    report.record(PhaseResult(name=_PHASE_NAME, status="success"))
    print("  ✓ Autorun complete: setup-dev-tools.py executed successfully")
    return True
