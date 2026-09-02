"""``scaffold_comments`` node — idempotent review comment scaffolding.

Delegates to ``scaffold_review_threads()`` from ``review_scaffold.py``
(FR-001) to create or locate the per-commit consolidated review comment
thread with full lifecycle support: session management, commit-hash
idempotency, file-change detection, multi-model reviews, and
force-rereview semantics.
"""

from __future__ import annotations

import datetime
import sys
from typing import Any


def _extract_file_paths(files: Any) -> list[str]:
    """Extract non-blank file paths from a potentially malformed files payload."""
    if not isinstance(files, list):
        return []

    file_paths: list[str] = []
    for entry in files:
        if not isinstance(entry, dict):
            continue
        raw_path = entry.get("path")
        if not isinstance(raw_path, str):
            continue
        path = raw_path.strip()
        if path:
            file_paths.append(path)
    return file_paths


def _resolve_model_id(state: dict[str, Any], get_value_fn: Any) -> str:
    """Resolve model_id per FR-007 precedence.

    The effective model returned in file results is preferred so persisted
    session metadata reflects the model that actually served the review.
    An explicit ``requested_model`` override comes next so scaffolding and
    session attribution stay aligned before file review results exist.
    Configured-provider values are later fallbacks.
    """
    file_results = state.get("file_results")
    if isinstance(file_results, list):
        result_models: list[str] = []
        for result in file_results:
            candidate = result.get("model_id") if isinstance(result, dict) else getattr(result, "model_id", None)
            if isinstance(candidate, str) and candidate.strip():
                result_models.append(candidate.strip())
        if len(result_models) == len(file_results) and len(set(result_models)) == 1:
            return result_models[0]
    requested_model = state.get("requested_model")
    if isinstance(requested_model, str) and requested_model.strip():
        return requested_model.strip()
    model_config_raw = state.get("model_config_raw")
    if isinstance(model_config_raw, dict):
        candidate = model_config_raw.get("default-model")
        if isinstance(candidate, str) and candidate.strip():
            return candidate.strip()
    if get_value_fn("review.engine") == "langchain":
        try:
            from agentic_devtools.orchestration.llm.config import load_config, resolve_node_config

            llm_config_path = state.get("llm_config_path")
            snapshot = load_config(llm_config_path)
            node_config = resolve_node_config(snapshot, "pr_review", "review_files")
            effective = node_config.effective_model
            if isinstance(effective, str) and effective.strip():
                return effective.strip()
        except Exception:
            pass
    fallback = get_value_fn("copilot.model_id")
    if isinstance(fallback, str) and fallback.strip():
        return fallback.strip()
    return "unknown"


def _resolve_bool_flag(state: dict[str, Any], state_key: str, get_value_fn: Any) -> bool:
    """Resolve a boolean runtime flag from ``get_value()`` state keys only.

    ``state["config"]`` is target-repo metadata and MUST NOT control
    runtime execution flags (FR-006, NFR-003).
    """
    raw = get_value_fn(state_key)
    if isinstance(raw, bool):
        return raw
    if isinstance(raw, str):
        return raw.strip().lower() in ("true", "1", "yes")
    return False


def _build_dry_run_placeholder(
    state: dict[str, Any],
    repo_name: str,
    model_id: str,
    files: list[Any],
) -> Any:
    """Build a placeholder ``ReviewState`` for dry-run mode (NFR-003).

    Uses metadata from graph state with zero thread/comment IDs.
    """
    from agentic_devtools.cli.azure_devops.review_state import (
        FileEntry,
        OverallSummary,
        ReviewSession,
        ReviewState,
        normalize_file_path,
    )

    pr_id = int(state.get("pr_id", 0))
    repo_id = state.get("repo_id", "")
    project = state.get("project", "")
    organization = state.get("organization", "")
    commit_hash = state.get("commit_hash", "")
    latest_iteration_id = state.get("latest_iteration_id", 0)
    now = datetime.datetime.now(datetime.UTC)

    file_entries: dict[str, FileEntry] = {}
    for path in _extract_file_paths(files):
        normalized = normalize_file_path(path)
        stripped = normalized.lstrip("/")
        folder = stripped.split("/")[0] if "/" in stripped else "root"
        file_entries[normalized] = FileEntry(
            threadId=0,
            commentId=0,
            folder=folder,
            fileName=normalized.split("/")[-1],
            status="unreviewed",
        )

    session = ReviewSession(
        sessionId="dry-run-placeholder",
        modelId=model_id,
        startedUtc=now.isoformat(),
        status="in_progress",
        commitHash=commit_hash,
        engine="langchain",
    )

    return ReviewState(
        prId=pr_id,
        repoId=repo_id,
        repoName=repo_name,
        project=project,
        organization=organization,
        latestIterationId=latest_iteration_id if isinstance(latest_iteration_id, int) else 0,
        scaffoldedUtc=now.isoformat(),
        overallSummary=OverallSummary(threadId=0, commentId=0, status="unreviewed"),
        files=file_entries,
        commitHash=commit_hash,
        modelId=model_id,
        sessions=[session],
    )


def scaffold_comments_node(state: dict[str, Any]) -> dict[str, Any]:
    """Scaffold review comment threads in Azure DevOps.

    Delegates to ``scaffold_review_threads()`` from ``review_scaffold.py``
    (FR-001) for the complete scaffolding lifecycle.  The node extracts
    parameters from ``ReviewGraphState``, resolves runtime flags from
    ``get_value()`` state keys, handles the return value, injects
    ``engine="langchain"`` on newly created sessions (FR-002), and
    propagates errors through the ``errors`` channel (FR-005).

    Args:
        state: Current ``ReviewGraphState``.

    Returns:
        State update dict with ``review_state_path`` on success,
        or ``errors`` on failure.
    """
    from agentic_devtools.cli.azure_devops.review_state import (
        ReviewState,
        save_review_state,
    )
    from agentic_devtools.state import get_state_dir, get_value

    # --- 1. Validate pr_id: coerce to int and enforce > 0 (fatal if invalid) ---
    raw_pr_id = state.get("pr_id")
    try:
        pr_id: int = int(raw_pr_id)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return {"errors": [f"scaffold_comments: pr_id is required and must be a positive integer, got {raw_pr_id!r}"]}
    if pr_id <= 0:
        return {"errors": [f"scaffold_comments: pr_id must be a positive integer, got {pr_id}"]}

    # --- 2. Extract state fields ---
    repo_id = state.get("repo_id", "")
    commit_hash = state.get("commit_hash", "")
    latest_iteration_id = state.get("latest_iteration_id", 0)
    files = state.get("files", [])

    # Build file list as list[str] for scaffold_review_threads()
    file_paths = _extract_file_paths(files)

    # --- 3. Resolve runtime flags from get_value() only ---
    model_id = _resolve_model_id(state, get_value)
    dry_run = _resolve_bool_flag(state, "dry_run", get_value)
    force_rereview = _resolve_bool_flag(state, "review.force_rereview", get_value)

    # --- 4. Resolve ADO config (best-effort for repo_name) ---
    repo_name = ""
    ado_config = None
    try:
        from agentic_devtools.cli.azure_devops.config import AzureDevOpsConfig

        ado_config = AzureDevOpsConfig.from_state()
        repo_name = ado_config.repository or ""
    except Exception:
        pass

    # Compute review_state_path
    state_dir = get_state_dir()
    reviews_dir = state_dir / "reviews"
    reviews_dir.mkdir(parents=True, exist_ok=True)
    review_state_path = str(reviews_dir / "review-state.json")

    # --- 5. Snapshot existing session IDs for engine injection ---
    existing_session_ids: set[str] = set()
    try:
        from agentic_devtools.cli.azure_devops.review_state import load_review_state

        existing_rs = load_review_state(pr_id)
        existing_session_ids = {s.sessionId for s in existing_rs.sessions}
    except Exception:
        pass

    # --- 6. Delegate to scaffold_review_threads() (FR-001) ---
    try:
        import requests as requests_module

        from agentic_devtools.cli.azure_devops.auth import get_auth_headers, get_pat
        from agentic_devtools.cli.azure_devops.config import AzureDevOpsConfig as _ADOConfig
        from agentic_devtools.cli.azure_devops.review_scaffold import scaffold_review_threads

        if ado_config is None:
            ado_config = _ADOConfig.from_state()
            repo_name = ado_config.repository or ""

        headers = {} if dry_run else get_auth_headers(get_pat())

        result: ReviewState | None = scaffold_review_threads(
            pull_request_id=pr_id,
            files=file_paths,
            config=ado_config,
            repo_id=repo_id,
            repo_name=repo_name,
            latest_iteration_id=latest_iteration_id if isinstance(latest_iteration_id, int) else 0,
            requests_module=requests_module,
            headers=headers,
            dry_run=dry_run,
            commit_hash=commit_hash or None,
            model_id=model_id,
            force_rereview=force_rereview,
        )
    except Exception as exc:
        error_msg = f"scaffold_comments: scaffolding failed (pr_id={pr_id}): {type(exc).__name__}: {exc}"
        print(error_msg, file=sys.stderr)
        return {"errors": [error_msg]}

    # --- 7. Handle return value ---
    if result is not None:
        # Inject engine="langchain" on newly created sessions (FR-002)
        for session in result.sessions:
            if session.sessionId not in existing_session_ids:
                session.engine = "langchain"

        # Save and return
        try:
            save_review_state(result)
        except Exception as exc:
            error_msg = f"scaffold_comments: failed to save review state (pr_id={pr_id}): {type(exc).__name__}: {exc}"
            print(error_msg, file=sys.stderr)
            return {"errors": [error_msg]}

        return {
            "review_state_path": review_state_path,
            "errors": [],
        }

    # result is None
    if dry_run:
        # Build placeholder ReviewState (NFR-003)
        placeholder = _build_dry_run_placeholder(state, repo_name, model_id, files)
        try:
            save_review_state(placeholder)
        except Exception as exc:
            error_msg = (
                f"scaffold_comments: failed to save dry-run review state (pr_id={pr_id}): {type(exc).__name__}: {exc}"
            )
            print(error_msg, file=sys.stderr)
            return {"errors": [error_msg]}

        return {
            "review_state_path": review_state_path,
            "errors": [],
        }

    # None + not dry_run = concurrent session abort (FR-003, FR-005)
    error_msg = f"scaffold_comments: concurrent session detected, aborting (pr_id={pr_id})"
    print(error_msg, file=sys.stderr)
    return {"errors": [error_msg]}
