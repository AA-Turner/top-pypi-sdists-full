"""
Orchestrator Commands - CLI commands for the generalized feature decomposition
and Trio orchestrator workflow.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import shutil
from pathlib import Path

from agentic_devtools.cli.git.branch_naming import build_branch_name, normalize_issue_key, sanitize_branch_description
from agentic_devtools.cli.subprocess_utils import run_safe
from agentic_devtools.cli.workflows.worktree_setup import propagate_agdt_cache
from agentic_devtools.epic_tree import EpicTreeLoadError, load_epic_tree

from ...background_tasks import run_function_in_background
from ...state import (
    STATE_FILENAME,
    _resolve_identity,
    delete_pin_file,
    get_bootstrap_state,
    get_repo_root,
    get_state_dir,
    get_value,
    get_workflow_state,
    is_safe_dir_segment,
    set_bootstrap_state,
    set_value,
    set_workflow_state,
    write_pin_file,
)

# --- Shared Implementation ---


_APPROVED_PAYLOAD_DIGEST_CONTEXT_KEY = "approved_payload_digest"


def _get_feature_slug() -> str:
    """Gets the feature slug from workflow state, sanitized for branch/path safety."""
    workflow = get_workflow_state() or {}
    context = workflow.get("context") if isinstance(workflow, dict) else None
    if not isinstance(context, dict):
        context = {}
    raw = context.get("feature_slug", "")
    slug = sanitize_branch_description(str(raw))[:40]
    return slug or "default-feature"


def _get_scratch_dir() -> Path:
    """Returns the path to the scratch directory for the current feature."""
    slug = _get_feature_slug()
    repo_root = get_repo_root()
    if not repo_root:
        repo_root = Path.cwd()
    return repo_root / ".agdt" / "scratch" / slug


def _error(message: str) -> int:
    """Print a CLI-friendly error message and return a non-zero status."""
    print(message)
    return 1


def _record_approval_payload_digest(context: dict[str, object]) -> int:
    """Capture the current scratch payload digest in workflow context."""
    try:
        context[_APPROVED_PAYLOAD_DIGEST_CONTEXT_KEY] = _compute_payload_digest(_get_scratch_dir())
    except ValueError as exc:
        return _error(f"Error: unable to record approval payload digest: {exc}")
    return 0


def _first_symlink(paths: tuple[Path, ...]) -> Path | None:
    """Return the first symlink among candidate paths, if any."""
    for candidate in paths:
        if candidate.is_symlink():
            return candidate
    return None


def _compute_payload_digest(root: Path) -> str:
    """Return a deterministic digest for the scratch payload tree."""
    if not root.exists() or not root.is_dir():
        raise ValueError(f"scratch payload directory does not exist: {root}")

    digest = hashlib.sha256()
    for entry in sorted(root.rglob("*")):
        relative_path = entry.relative_to(root).as_posix()
        if entry.is_symlink():
            raise ValueError(f"scratch payload contains symlink: {relative_path}")
        if entry.is_dir():
            digest.update(b"D\0")
            digest.update(relative_path.encode("utf-8"))
            digest.update(b"\0")
            continue
        if not entry.is_file():
            raise ValueError(f"scratch payload contains unsupported path type: {relative_path}")
        stat_result = entry.stat()
        digest.update(b"F\0")
        digest.update(relative_path.encode("utf-8"))
        digest.update(b"\0")
        digest.update(str(stat_result.st_size).encode("utf-8"))
        digest.update(b"\0")
        digest.update(b"1" if stat_result.st_mode & 0o111 else b"0")
        digest.update(b"\0")
        with entry.open("rb") as handle:
            for chunk in iter(lambda: handle.read(8192), b""):
                digest.update(chunk)
        digest.update(b"\0")
    return digest.hexdigest()


def _read_workflow_state_for_scope(repo_root: Path, worktree_key: str) -> dict[str, object]:
    """Return the workflow record for a specific scoped state directory, if present."""
    bootstrap = get_bootstrap_state()
    identity = bootstrap.get("identity", "")
    if not isinstance(identity, str) or not identity:
        identity = _resolve_identity(repo_root)

    if isinstance(identity, str) and identity and is_safe_dir_segment(identity) and is_safe_dir_segment(worktree_key):
        state_file = repo_root / ".agdt" / "workflows" / identity / worktree_key / STATE_FILENAME
    else:
        state_file = repo_root / ".agdt" / "workflows" / "_unscoped" / STATE_FILENAME

    try:
        state = json.loads(state_file.read_text(encoding="utf-8"))
    except (FileNotFoundError, OSError, UnicodeDecodeError, json.JSONDecodeError):
        return {}
    if not isinstance(state, dict):
        return {}
    workflow = state.get("workflow")
    return workflow if isinstance(workflow, dict) else {}


def _is_expected_retry_path(path_text: str, expected_prefix: str) -> bool:
    """Return whether a porcelain path operand stays within the allowed retry payload."""
    return path_text == expected_prefix or path_text.startswith(expected_prefix + "/")


def _has_non_standard_float(obj: object) -> bool:
    """Return True if *obj* or any nested value contains a NaN or Infinity float.

    Python's ``json.loads`` silently accepts the non-standard JSON literals
    ``NaN``, ``Infinity``, and ``-Infinity``, converting them to Python floats.
    This helper detects those values after parsing so they can be rejected.
    """
    if isinstance(obj, float) and (math.isnan(obj) or math.isinf(obj)):
        return True
    if isinstance(obj, dict):
        return any(_has_non_standard_float(v) for v in obj.values())
    if isinstance(obj, list):
        return any(_has_non_standard_float(item) for item in obj)
    return False


def _status_line_within_retry_payload(status_line: str, expected_prefix: str) -> bool:
    """Validate a `git status --porcelain` line against the allowed retry payload path."""
    stripped_line = status_line.strip()
    if not stripped_line:
        return True
    if len(status_line) < 4:
        return False
    path_text = status_line[3:]
    status_code = status_line[:2]
    is_rename_or_copy = status_code[0] in {"R", "C"} or status_code[1] in {"R", "C"}
    if not is_rename_or_copy:
        return _is_expected_retry_path(path_text, expected_prefix)
    old_new = path_text.split(" -> ", 1)
    if len(old_new) != 2:
        return False
    return all(_is_expected_retry_path(candidate, expected_prefix) for candidate in old_new)


def _get_issue_key_candidate() -> str:
    """Resolve the configured issue key from scoped state or bootstrap fallback."""
    raw_issue_key = get_value("issue_key", required=False)
    if raw_issue_key not in (None, ""):
        return str(raw_issue_key)
    bootstrap = get_bootstrap_state()
    return bootstrap.get("worktree_key", "")


def _get_required_issue_id(action: str) -> str | None:
    """Return the normalized issue identifier required for orchestration commands."""
    raw_issue_key = _get_issue_key_candidate()
    if not raw_issue_key:
        print(f"Error: issue_key must be set and valid before {action}.")
        return None
    try:
        return normalize_issue_key(raw_issue_key)
    except ValueError as e:
        print(f"Error: invalid issue_key — {e}")
        return None


def orchestrate_init_cmd() -> int:
    """Initiates Task 0 decomposition and primes trio state."""
    issue_id = _get_required_issue_id("initializing orchestrate-feature")
    if issue_id is None:
        return 1

    # Read existing workflow state *before* scoping the bootstrap to issue_id;
    # set_bootstrap_state changes the state directory, so a subsequent
    # get_workflow_state() would read from the new scope and miss any active
    # workflow recorded under the prior scope (e.g. unscoped "#42" vs "42").
    workflow = get_workflow_state() or {}
    workflow_dict = workflow if isinstance(workflow, dict) else {}
    context = workflow_dict.get("context")
    if not isinstance(context, dict):
        context = {}
    active = "orchestrate-feature"
    status = "running"
    step = "decomposition"

    # Fail closed if any workflow is already active — the repository stores a single shared
    # _workflow record, and re-initializing here would overwrite another workflow's progress.
    if workflow_dict.get("active"):
        return _error(
            f"Error: workflow {workflow_dict['active']!r} is already active at step {workflow_dict.get('step')!r}. "
            "Clear the workflow state (agdt-clear-workflow) before re-initializing."
        )

    # Capture the sanitized slug from the already-read workflow context *before*
    # set_bootstrap_state() changes the state scope: after the scope switch the
    # workflow state is read from the new directory, and any pre-existing
    # feature_slug recorded under the prior scope (e.g. "#42" vs "42") would be
    # lost, causing _get_feature_slug() to fall back to "default-feature".
    raw_slug = context.get("feature_slug", "")
    slug = sanitize_branch_description(str(raw_slug))[:40] or "default-feature"

    # Generate epic-tree.json stub conforming to schema version 1.0
    repo_root = get_repo_root() or Path.cwd()
    dest_workflow_dict = _read_workflow_state_for_scope(repo_root, issue_id)
    if dest_workflow_dict.get("active"):
        return _error(
            f"Error: workflow {dest_workflow_dict['active']!r} is already active at step "
            f"{dest_workflow_dict.get('step')!r} in the destination scope for issue {issue_id!r}. "
            "Clear the workflow state (agdt-clear-workflow) before re-initializing."
        )
    scratch_dir = repo_root / ".agdt" / "scratch" / slug
    epic_tree_path = scratch_dir / "epic-tree.json"
    symlink_path = _first_symlink((repo_root / ".agdt", repo_root / ".agdt" / "scratch", scratch_dir, epic_tree_path))
    if symlink_path is not None:
        return _error(f"Error: destination path is a symlink: {symlink_path}")
    if epic_tree_path.exists():
        return _error(
            f"Error: {epic_tree_path} already exists. Clear the scratch directory "
            "or remove the file before re-initializing to avoid overwriting reviewed artifacts."
        )

    previous_bootstrap = get_bootstrap_state()
    previous_worktree_key = previous_bootstrap.get("worktree_key") if isinstance(previous_bootstrap, dict) else None
    set_bootstrap_state(worktree_key=issue_id)

    # Pin the resolved state directory so subsequent agdt-orchestrate-step and
    # agdt-orchestrate-finalize calls always resolve to this scope, regardless
    # of any intervening context-key updates or stale pins from prior workflows.
    _pin_env_override = os.environ.get("AGENTIC_DEVTOOLS_STATE_DIR", "").strip()
    _pin_was_written = False
    if not _pin_env_override:
        delete_pin_file()
        _resolved_state_dir = get_state_dir()
        write_pin_file(_resolved_state_dir, workflow="orchestrate-feature")
        os.environ["AGENTIC_DEVTOOLS_STATE_DIR"] = str(_resolved_state_dir)
        _pin_was_written = True

    # Re-read workflow state from the *destination* scope (post-normalization).
    # set_bootstrap_state() may have switched the state directory (e.g. "#42" → "42"),
    # so the pre-switch guard could have missed an active workflow already recorded there.
    dest_workflow = get_workflow_state()
    dest_workflow_dict = dest_workflow if isinstance(dest_workflow, dict) else {}
    if dest_workflow_dict.get("active"):
        set_bootstrap_state(worktree_key=previous_worktree_key if isinstance(previous_worktree_key, str) else "")
        if _pin_was_written:
            delete_pin_file()
            os.environ.pop("AGENTIC_DEVTOOLS_STATE_DIR", None)
        return _error(
            f"Error: workflow {dest_workflow_dict['active']!r} is already active at step "
            f"{dest_workflow_dict.get('step')!r} in the destination scope for issue {issue_id!r}. "
            "Clear the workflow state (agdt-clear-workflow) before re-initializing."
        )

    scratch_dir.mkdir(parents=True, exist_ok=True)
    epic_tree = {
        "schemaVersion": "1.0",
        "epic": {"ref": "epic-1", "title": "Generated Epic", "body": "", "features": []},
    }
    epic_tree_path.write_text(json.dumps(epic_tree, indent=2))
    set_value("issue_key", issue_id)

    # Prime trio state
    context["trio_state"] = "primed"

    set_workflow_state(active, status, step=step, context=context)
    print("Initiated Task 0 decomposition and primed trio state.")
    return 0


_STEP_TRANSITIONS: dict[str, str] = {
    "decomposition": "doer_execution",
    "doer_execution": "duck_reviews",
    "duck_reviews": "adjudicator_decision",
    "adjudicator_decision": "AWAITING_HUMAN_APPROVAL",
}

_ALLOWED_TRIO_EVENTS: set[str] = {
    # Lifecycle / workflow-step events (state-machine transitions)
    "decomposition",
    "doer_execution",
    "duck_reviews",
    "adjudicator_decision",
    "AWAITING_HUMAN_APPROVAL",
    "finalizing",
    "completed",
    # Artifact event types (discriminated union declared in the events.jsonl schema)
    "review",
    "response",
    "adjudication",
    "promotion",
    "audit",
    "state_verify",
    "invocation_failure",
    "issue_reconciled",
    "state_transition",
    "assignment",
}

_LIFECYCLE_TRIO_EVENTS: tuple[str, ...] = (
    "decomposition",
    "doer_execution",
    "duck_reviews",
    "adjudicator_decision",
    "AWAITING_HUMAN_APPROVAL",
    "finalizing",
    "completed",
)

_ARTIFACT_EVENT_PAYLOAD_KEYS: dict[str, str] = {
    event: event for event in _ALLOWED_TRIO_EVENTS if event not in _LIFECYCLE_TRIO_EVENTS
}


def orchestrate_step_cmd() -> int:
    """Advance the Trio scaffold or refresh the approval digest at the approval gate."""
    workflow = get_workflow_state() or {}
    if not isinstance(workflow, dict):
        return _error("Error: workflow state is malformed; expected an object.")
    active = workflow.get("active")

    if active != "orchestrate-feature":
        return _error(
            f"Error: no active orchestrate-feature workflow (active={active!r}). Run agdt-orchestrate-init first."
        )

    status = workflow.get("status", "running")
    context = workflow.get("context", {})
    if not isinstance(context, dict):
        return _error("Error: workflow context is malformed; expected an object.")
    step = workflow.get("step", "")

    if step == "AWAITING_HUMAN_APPROVAL":
        digest_result = _record_approval_payload_digest(context)
        if digest_result != 0:
            return digest_result
        set_workflow_state(active, status, step=step, context=context)
        print("Refreshed review summary/plan digest: Approval required.")
        return 0

    if step not in _STEP_TRANSITIONS:
        return _error(
            f"Error: step {step!r} is not a valid orchestrate-feature transition. "
            f"Expected one of: {list(_STEP_TRANSITIONS)}"
        )

    next_step = _STEP_TRANSITIONS[step]
    if next_step == "AWAITING_HUMAN_APPROVAL":
        digest_result = _record_approval_payload_digest(context)
        if digest_result != 0:
            return digest_result
        print("Review summary/plan digest: Approval required.")

    set_workflow_state(active, status, step=next_step, context=context)
    print(f"Transitioned Trio state to: {next_step}")
    return 0


def orchestrate_finalize_cmd() -> int:
    """Unlocks the AWAITING_HUMAN_APPROVAL gate and runs the automated finalization sequence."""
    workflow = get_workflow_state() or {}
    if not isinstance(workflow, dict):
        return _error("Error: workflow state is malformed; expected an object.")
    if workflow.get("step") not in ("AWAITING_HUMAN_APPROVAL", "finalizing"):
        return _error("Workflow is not ready for finalization.")

    active = workflow.get("active")
    if active != "orchestrate-feature":
        return _error(f"Error: no active orchestrate-feature workflow (active={active!r}).")
    status = workflow.get("status", "running")
    context = workflow.get("context", {})
    if not isinstance(context, dict):
        return _error("Error: workflow context is malformed; expected an object.")

    # Validate issue_key before any destructive operations
    issue_id = _get_required_issue_id("finalizing")
    if not issue_id:
        return 1

    slug = _get_feature_slug()

    # Build branch and worktree names using safe branch-naming helpers
    branch = build_branch_name(issue_id, slug)
    worktree = f"{issue_id}-{slug}"

    # Dirty-tree preflight check: abort if there are uncommitted changes or not in a git repo
    repo_root = get_repo_root() or Path.cwd()
    status_result = run_safe(["git", "status", "--porcelain"], capture_output=True, text=True, shell=False)
    if status_result.returncode != 0:
        return _error("Error: git status failed. Ensure finalization is run inside a git repository.")
    if status_result.stdout.strip():
        return _error("Error: Working tree has uncommitted changes. Commit or stash them before finalizing.")

    approved_payload_digest = context.get(_APPROVED_PAYLOAD_DIGEST_CONTEXT_KEY)
    if not isinstance(approved_payload_digest, str) or not approved_payload_digest:
        return _error(
            "Error: approval payload digest is missing from workflow state. "
            "Re-run agdt-orchestrate-step while awaiting approval to refresh the approval digest before finalizing."
        )

    scratch_dir = _get_scratch_dir()
    if not scratch_dir.exists() or not scratch_dir.is_dir():
        return _error(f"Error: required scratch directory does not exist: {scratch_dir}")
    ancestor_symlink = _first_symlink((scratch_dir.parent.parent, scratch_dir.parent, scratch_dir))
    if ancestor_symlink is not None:
        return _error(f"Error: source path is a symlink: {ancestor_symlink}")
    child_symlinks = [p for p in scratch_dir.rglob("*") if p.is_symlink()]
    if child_symlinks:
        return _error(
            "Error: scratch directory contains symlinks; refusing to copy potentially unsafe payload: "
            + ", ".join(str(p.relative_to(scratch_dir.parent.parent)) for p in child_symlinks)
        )
    required_artifacts = ("epic-tree.json",)
    missing_artifacts = [name for name in required_artifacts if not (scratch_dir / name).is_file()]
    if missing_artifacts:
        return _error(
            "Error: required orchestration artifacts are missing from scratch directory: "
            + ", ".join(missing_artifacts)
        )
    # Validate epic-tree.json against the schema and semantic rules before publishing.
    try:
        load_epic_tree(scratch_dir / "epic-tree.json", config_path=get_repo_root())
    except EpicTreeLoadError as exc:
        return _error(f"Error: epic-tree.json failed schema validation:\n{exc}")
    except Exception as exc:
        return _error(f"Error: epic-tree.json could not be loaded: {exc}")
    try:
        source_payload_digest = _compute_payload_digest(scratch_dir)
    except ValueError as exc:
        return _error(f"Error: unable to hash approval payload: {exc}")
    if source_payload_digest != approved_payload_digest:
        return _error(
            "Error: scratch payload changed after approval. "
            "Re-run agdt-orchestrate-step while awaiting approval to refresh the approval digest before finalizing."
        )

    # Transition to finalizing only when we're about to begin work (idempotent on retry)
    if workflow.get("step") == "AWAITING_HUMAN_APPROVAL":
        set_workflow_state(active, status, step="finalizing", context=context)

    worktree_path = repo_root.parent / worktree

    # 1. Create or reuse worktree — idempotent on retry after a partial failure
    if worktree_path.exists():
        repo_root_str = str(repo_root)
        from agentic_devtools.cli.git.worktree import _is_valid_worktree_dir  # noqa: PLC0415

        if not _is_valid_worktree_dir(worktree_path, repo_root_str):
            return _error(
                f"Error: {worktree_path} exists but is not a valid worktree of this repository. "
                "Remove or rename it before retrying finalization."
            )
        branch_check = run_safe(
            ["git", "-C", str(worktree_path), "branch", "--show-current"],
            capture_output=True,
            text=True,
            shell=False,
        )
        if branch_check.returncode != 0:
            return _error(f"Error: failed to determine current branch in existing worktree:\n{branch_check.stderr}")
        current_branch = branch_check.stdout.strip()
        if current_branch != branch:
            return _error(
                f"Error: existing worktree is on branch {current_branch!r}, expected {branch!r}. "
                "Use the correct worktree or remove this one before retrying."
            )
        print(f"Reusing existing worktree at {worktree_path}.")
        # Fail closed: refuse to reuse a worktree that has staged or unstaged changes
        # outside the expected retry payload path (.agdt/scratch/<slug>). An unrestricted
        # `git commit` later would bundle those unrelated files into the published branch.
        wt_status = run_safe(
            ["git", "-C", str(worktree_path), "status", "--porcelain"],
            capture_output=True,
            text=True,
            shell=False,
        )
        if wt_status.returncode != 0:
            return _error(f"Error: git status failed in existing worktree:\n{wt_status.stderr}")
        expected_prefix = f".agdt/scratch/{slug}"
        unexpected_changes = [
            line
            for line in wt_status.stdout.splitlines()
            if not _status_line_within_retry_payload(line, expected_prefix)
        ]
        if unexpected_changes:
            return _error(
                "Error: existing worktree has changes outside the expected retry payload path "
                f"({expected_prefix}). Commit or stash them before retrying finalization:\n"
                + "\n".join(unexpected_changes)
            )
    else:
        print(f"Creating git branch {branch} and worktree directory {worktree}...")
        # Detect whether the branch already exists locally (e.g. a previous attempt that created
        # the branch but failed before provisioning the worktree). When it does, attach the
        # existing branch instead of using -b which would fail with "branch already exists".
        branch_list = run_safe(
            ["git", "branch", "--list", branch],
            capture_output=True,
            text=True,
            shell=False,
        )
        if branch_list.returncode != 0:
            return _error(f"Error: git branch lookup failed:\n{branch_list.stderr}")
        branch_exists = branch_list.returncode == 0 and branch_list.stdout.strip() != ""
        if branch_exists:
            return _error(
                "Error: target branch already exists without a matching worktree path; "
                "refusing to attach to potentially unrelated history. "
                f"Delete local branch {branch!r} or restore the existing worktree before retrying finalization."
            )
        wt_result = run_safe(
            ["git", "worktree", "add", "-b", branch, str(worktree_path), "origin/main"],
            capture_output=True,
            text=True,
            shell=False,
        )
        if wt_result.returncode != 0:
            return _error(f"Error: git worktree add failed:\n{wt_result.stderr}")

    # Guard against symlinked .agdt directory or cache files in the worktree
    # before writing: propagate_agdt_cache writes to .agdt/ and would follow
    # symlinks before the ancestor guards below have a chance to fire.
    _agdt_cache_paths = [
        worktree_path / ".agdt",
        worktree_path / ".agdt" / "identity.json",
        worktree_path / ".agdt" / "runtime-bootstrap.json",
    ]
    for _p in _agdt_cache_paths:
        if _p.is_symlink():
            return _error(f"Error: cannot propagate AGDT cache — destination path is a symlink: {_p}")

    # Propagate identity.json and runtime-bootstrap.json so the worktree
    # resolves the correct issue-scoped state directory when agdt-* commands run.
    try:
        propagate_agdt_cache(str(worktree_path), worktree_key=issue_id)
    except (OSError, ValueError) as exc:
        return _error(f"Error: failed to propagate AGDT cache to worktree: {exc}")

    # 2. Copy prompt package and briefs, then stage and commit them in the new worktree
    print("Copying prompt package and briefs...")
    target_scratch = worktree_path / ".agdt" / "scratch" / slug
    if scratch_dir.resolve() == target_scratch.resolve():
        return _error(
            "Error: source and target scratch directories resolve to the same path. "
            "Run finalization from the source checkout, not from the target worktree."
        )
    # Guard against symlinked ancestors in the worktree's .agdt tree; on retry they could
    # redirect mkdir/rmtree/copytree writes to a path outside the worktree root.
    for _dest_ancestor in (worktree_path / ".agdt", worktree_path / ".agdt" / "scratch"):
        if _dest_ancestor.is_symlink():
            return _error(f"Error: destination path ancestor is a symlink: {_dest_ancestor}")
    target_scratch.parent.mkdir(parents=True, exist_ok=True)
    # Verify the resolved target still lives inside the worktree after mkdir.
    try:
        target_scratch.resolve().relative_to(worktree_path.resolve())
    except ValueError:
        return _error(f"Error: resolved target scratch path escapes the worktree root: {target_scratch.resolve()}")
    if target_scratch.exists():
        if target_scratch.is_symlink():
            return _error(f"Error: existing target scratch path is a symlink: {target_scratch}")
        if not target_scratch.is_dir():
            return _error(f"Error: existing target scratch path is not a directory: {target_scratch}")
        try:
            shutil.rmtree(target_scratch)
        except OSError as exc:
            return _error(f"Error: failed to replace existing target scratch directory: {exc}")
    shutil.copytree(scratch_dir, target_scratch)
    try:
        copied_payload_digest = _compute_payload_digest(target_scratch)
    except ValueError as exc:
        return _error(f"Error: unable to hash copied payload: {exc}")
    if copied_payload_digest != approved_payload_digest:
        return _error(
            "Error: copied payload digest does not match the approved scratch payload. Aborting before commit."
        )
    # Stage the migrated artifacts; use -f to bypass .gitignore rules for .agdt/scratch.
    add_result = run_safe(
        ["git", "-C", str(worktree_path), "add", "-f", str(target_scratch.relative_to(worktree_path))],
        capture_output=True,
        text=True,
        shell=False,
    )
    if add_result.returncode != 0:
        return _error(f"Error: git add failed:\n{add_result.stderr}")
    # Build a conformant commit message: chore(<scope>): ... with footer repeating scope.
    scope = f"#{issue_id}" if issue_id.isdigit() else issue_id
    commit_msg = f"chore({scope}): add orchestration prompt package\n\n{scope}"
    commit_result = run_safe(
        ["git", "-C", str(worktree_path), "commit", "-m", commit_msg],
        capture_output=True,
        text=True,
        shell=False,
    )
    if commit_result.returncode != 0:
        diff_cached = run_safe(
            ["git", "-C", str(worktree_path), "diff", "--cached", "--quiet"],
            capture_output=True,
            text=True,
            shell=False,
        )
        clean_status = run_safe(
            ["git", "-C", str(worktree_path), "status", "--porcelain"],
            capture_output=True,
            text=True,
            shell=False,
        )
        if not (diff_cached.returncode == 0 and clean_status.returncode == 0 and not clean_status.stdout.strip()):
            return _error(f"Error: git commit failed:\n{commit_result.stderr}")
        print("Note: git commit had nothing new to commit; continuing with existing committed artifacts.")

    # 3. Perform single upstream publish — fail before reporting success
    print(f"git push -u origin {branch}")
    push_result = run_safe(
        ["git", "push", "-u", "origin", branch],
        capture_output=True,
        text=True,
        shell=False,
    )
    if push_result.returncode != 0:
        return _error(f"Error: git push failed:\n{push_result.stderr}")

    # 4. Mark workflow completed only after every step has succeeded, then deactivate it
    # so a future orchestrate-feature run can reuse the issue scope without manual cleanup.
    completed_workflow: dict[str, object] = {
        "active": "",
        "status": "completed",
        "step": "completed",
        "context": context,
    }
    started_at = workflow.get("started_at")
    if isinstance(started_at, str):
        completed_workflow["started_at"] = started_at
    set_value("workflow", completed_workflow)

    # Release the state-directory pin only after the completed record is safely
    # written to the currently pinned workflow scope.
    delete_pin_file()
    os.environ.pop("AGENTIC_DEVTOOLS_STATE_DIR", None)

    # 5. Print paste-ready handover summary with artifact paths and continuation instructions
    target_scratch_path = worktree_path / ".agdt" / "scratch" / slug
    print(
        f"\nHandover complete.\n"
        f"  Branch:    {branch}\n"
        f"  Worktree:  {worktree_path}\n"
        f"  Artifacts: {target_scratch_path}\n"
        f"\nThe orchestrate-feature workflow is complete.\n"
        f"To inspect the published artifacts in the new worktree:\n"
        f"  cd {worktree_path}\n"
        f"  ls {target_scratch_path}\n"
        f"\nNo further agdt-orchestrate-step call is required.\n"
    )

    # 6. Launch VS Code (best effort; publication is already complete)
    print("Attempting to open the new worktree in VS Code (best effort)...")
    try:
        code_result = run_safe(["code", str(worktree_path)], capture_output=True, text=True, shell=False)
    except OSError as exc:
        print(f"Note: VS Code launch failed (best-effort): {exc}")
    else:
        if code_result.returncode != 0:
            detail = code_result.stderr.strip()
            suffix = f":\n{detail}" if detail else "."
            print(f"Note: VS Code launch failed (best-effort){suffix}")
    return 0


def audit_trio_cmd() -> None:
    """Runs deterministic validation of prompt/artifact gates and review invariants."""
    scratch_dir = _get_scratch_dir()
    events_file = scratch_dir / "events.jsonl"
    symlink_path = _first_symlink((scratch_dir.parent.parent, scratch_dir.parent, scratch_dir, events_file))
    if symlink_path is not None:
        raise ValueError(f"Validation failed: events path is a symlink: {symlink_path}")

    if not events_file.exists():
        raise FileNotFoundError(f"Validation failed: Events file not found at {events_file}")
    if not events_file.is_file():
        raise ValueError(f"Validation failed: Events file must be a regular file: {events_file}")

    try:
        event_rows: list[dict[str, object]] = []
        events = events_file.read_text(encoding="utf-8").splitlines()
        for i, line in enumerate(events):
            if line.strip():
                parsed = json.loads(line)
                if _has_non_standard_float(parsed):
                    raise ValueError(
                        f"Validation failed: Non-standard JSON constant (NaN or Infinity) on line {i + 1}."
                    )
                if not isinstance(parsed, dict):
                    raise ValueError(f"Validation failed: Event on line {i + 1} must be a JSON object.")
                event = parsed.get("event")
                if not isinstance(event, str):
                    raise ValueError(f"Validation failed: Event on line {i + 1} is missing string field 'event'.")
                if event not in _ALLOWED_TRIO_EVENTS:
                    raise ValueError(f"Validation failed: Event on line {i + 1} has unsupported type {event!r}.")
                if event not in _LIFECYCLE_TRIO_EVENTS:
                    payload_key = _ARTIFACT_EVENT_PAYLOAD_KEYS[event]
                    payload_fields = [key for key in parsed if key != "event"]
                    if set(payload_fields) != {payload_key}:
                        raise ValueError(
                            "Validation failed: Event on line "
                            f"{i + 1} with type {event!r} must include exactly one payload field "
                            f"named {payload_key!r}."
                        )
                    payload = parsed[payload_key]
                    if not isinstance(payload, dict):
                        raise ValueError(
                            "Validation failed: Event on line "
                            f"{i + 1} with type {event!r} must use an object payload for field "
                            f"{payload_key!r}."
                        )
                event_rows.append(parsed)
    except json.JSONDecodeError as e:
        raise ValueError(f"Validation failed: Malformed JSON in events file on line {i + 1}: {e}") from e

    if not event_rows:
        raise ValueError("Validation failed: events.jsonl must contain at least one non-empty event object.")

    events_by_name = [str(row["event"]) for row in event_rows]
    lifecycle_order = list(_LIFECYCLE_TRIO_EVENTS)
    lifecycle_events = [name for name in events_by_name if name in lifecycle_order]
    if len(lifecycle_events) > len(lifecycle_order):
        raise ValueError("Validation failed: lifecycle contains extra events after completion.")
    expected_prefix = lifecycle_order[: len(lifecycle_events)]
    for actual, expected in zip(lifecycle_events, expected_prefix):
        if actual == expected:
            continue
        if actual == "completed" and expected == "finalizing":
            raise ValueError("Validation failed: completed event requires a prior finalizing event.")
        if actual in {"finalizing", "completed"} and expected == "AWAITING_HUMAN_APPROVAL":
            raise ValueError("Validation failed: finalization events require an AWAITING_HUMAN_APPROVAL gate event.")
        raise ValueError(f"Validation failed: event {actual!r} appears out of lifecycle order.")

    print(f"Auditing events from {events_file}...")
    print("Deterministic validation of prompt/artifact gates and review invariants passed.")


# --- Async Wrappers ---


def orchestrate_init_async() -> None:
    """Async wrapper for orchestrate_init_cmd."""
    run_function_in_background(
        "agentic_devtools.cli.workflows.orchestrator_commands",
        "orchestrate_init_cmd",
        command_display_name="agdt-orchestrate-init",
    )


def orchestrate_step_async() -> None:
    """Async wrapper for orchestrate_step_cmd."""
    run_function_in_background(
        "agentic_devtools.cli.workflows.orchestrator_commands",
        "orchestrate_step_cmd",
        command_display_name="agdt-orchestrate-step",
    )


def orchestrate_finalize_async() -> None:
    """Async wrapper for orchestrate_finalize_cmd."""
    run_function_in_background(
        "agentic_devtools.cli.workflows.orchestrator_commands",
        "orchestrate_finalize_cmd",
        command_display_name="agdt-orchestrate-finalize",
    )


def audit_trio_async() -> None:
    """Async wrapper for audit_trio_cmd."""
    run_function_in_background(
        "agentic_devtools.cli.workflows.orchestrator_commands",
        "audit_trio_cmd",
        command_display_name="agdt-audit-trio",
    )


__all__ = [
    "orchestrate_init_cmd",
    "orchestrate_step_cmd",
    "orchestrate_finalize_cmd",
    "audit_trio_cmd",
    "orchestrate_init_async",
    "orchestrate_step_async",
    "orchestrate_finalize_async",
    "audit_trio_async",
]
