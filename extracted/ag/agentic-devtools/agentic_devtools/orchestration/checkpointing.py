"""SqliteSaver checkpoint configuration for LangGraph workflows."""

import os
import sqlite3
import sys
from pathlib import Path
from urllib.parse import quote

from langgraph.checkpoint.sqlite import SqliteSaver

_CHECKPOINT_DB_FILENAME = "orchestration.db"


def _same_resolved_path(left: Path, right: Path) -> bool:
    """Return whether two paths resolve to the same location."""
    try:
        return left.samefile(right)
    except OSError:
        return left.resolve() == right.resolve()


def _canonical_worktree_key_from_state_dir(state_dir: Path, repo_root: Path) -> str | None:
    """Return the canonical worktree key when *state_dir* is exactly in workflow layout."""
    workflows_root = (repo_root / ".agdt" / "workflows").resolve()
    try:
        relative = state_dir.resolve().relative_to(workflows_root)
    except ValueError:
        return None
    return relative.parts[1] if len(relative.parts) == 2 else None


def validate_checkpoint_state_dir(state_dir: Path, *, worktree_key: str | None = None) -> None:
    """Fail closed for unresolved-scope fallback paths and canonical key mismatches."""
    from agentic_devtools.state import get_repo_root

    repo_root = get_repo_root()
    if repo_root is not None:
        unscoped_dir = repo_root / ".agdt" / "workflows" / "_unscoped"
        if _same_resolved_path(state_dir, unscoped_dir):
            raise ValueError(
                f"Workflow state directory resolved to an unscoped fallback path ({state_dir}). "
                "Ensure bootstrap identity and scope are established before running the workflow."
            )
    else:
        fallback_dir = Path.cwd() / ".agdt-temp"
        if _same_resolved_path(state_dir, fallback_dir):
            raise ValueError(
                f"Workflow state directory resolved to an unscoped fallback path ({state_dir}). "
                "Ensure bootstrap identity and scope are established before running the workflow."
            )

    if repo_root is None or worktree_key is None:
        return

    canonical_worktree_key = _canonical_worktree_key_from_state_dir(state_dir, repo_root)
    if canonical_worktree_key is not None and canonical_worktree_key != worktree_key:
        raise ValueError(
            f"Workflow state directory {state_dir} is pinned to worktree scope {canonical_worktree_key!r}, "
            f"but the active worktree key is {worktree_key!r}. "
            "Run the workflow initializer again to re-establish a matching scoped path."
        )


def _probe_legacy_checkpoint_database(legacy_path: Path) -> str | None:
    """Return legacy probe outcome: None absent, '' readable, otherwise failure reason."""
    try:
        legacy_path.stat()
    except FileNotFoundError:
        return None
    except OSError as exc:
        return exc.strerror or str(exc)

    uri = f"file:{quote(str(legacy_path.resolve()), safe='/')}?mode=ro"
    try:
        with sqlite3.connect(uri, uri=True) as conn:
            row = conn.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='checkpoints'").fetchone()
    except OSError as exc:
        return exc.strerror or str(exc)
    except sqlite3.DatabaseError as exc:
        message = str(exc) or exc.__class__.__name__
        if "not a database" in message.lower():
            return "not a valid SQLite database"
        return message

    return "" if row is not None else "checkpoints table missing"


def _emit_legacy_checkpoint_warning(legacy_path: Path, scoped_path: Path) -> None:
    """Emit the FR-007 warning when a legacy repository-root database is present."""
    probe_outcome = _probe_legacy_checkpoint_database(legacy_path)
    if probe_outcome is None:
        return

    if probe_outcome == "":
        print(
            "WARNING: legacy checkpoint database detected at "
            f"'{legacy_path}'. The active worktree will use '{scoped_path}' for new checkpoints. "
            "No automatic migration is performed. Remove or relocate the legacy database manually "
            "to suppress this warning.",
            file=sys.stderr,
        )
        return

    print(
        "WARNING: legacy checkpoint database at "
        f"'{legacy_path}' is inaccessible ({probe_outcome}). "
        f"The file will be ignored; the active worktree will use '{scoped_path}' for new checkpoints.",
        file=sys.stderr,
    )


def _resolve_scoped_redirect_state_dir(
    *,
    repo_root: Path,
    worktree_key: str | None,
) -> Path:
    """Build the canonical scoped state directory for legacy-root redirect handling."""
    from agentic_devtools.state import _get_or_refresh_identity, get_bootstrap_state, is_safe_dir_segment

    resolved_worktree_key = worktree_key
    if resolved_worktree_key is None:
        bootstrap_worktree_key = get_bootstrap_state().get("worktree_key", "")
        resolved_worktree_key = bootstrap_worktree_key if isinstance(bootstrap_worktree_key, str) else ""
    resolved_worktree_key = resolved_worktree_key.strip()

    if not is_safe_dir_segment(resolved_worktree_key):
        raise ValueError(
            "Legacy checkpoint path alias requires a valid worktree key so new checkpoints can be "
            "redirected to a canonical scoped database."
        )

    identity = _get_or_refresh_identity(repo_root)
    if not is_safe_dir_segment(identity):
        raise ValueError(
            "Legacy checkpoint path alias requires a valid scoped identity so new checkpoints can be redirected safely."
        )

    return repo_root / ".agdt" / "workflows" / identity / resolved_worktree_key


def _resolve_scoped_redirect_db_path(
    *,
    repo_root: Path,
    worktree_key: str | None,
    legacy_path: Path,
) -> Path:
    """Resolve and validate the redirected database path for legacy-root aliases."""
    redirected_state_dir = _resolve_scoped_redirect_state_dir(
        repo_root=repo_root,
        worktree_key=worktree_key,
    )
    redirected_path = (redirected_state_dir / _CHECKPOINT_DB_FILENAME).resolve()
    if _same_resolved_path(redirected_path, legacy_path):
        raise ValueError(
            "Legacy checkpoint redirect resolved back to the legacy repository-root database path. "
            "Ensure the scoped workflow directory does not alias the repository .agdt directory."
        )
    return redirected_path


def _resolve_workflow_managed_db_path(
    *,
    state_dir: Path,
    worktree_key: str | None,
) -> Path:
    """Resolve the database path for workflow-managed checkpoint initialization."""
    from agentic_devtools.state import get_repo_root

    validate_checkpoint_state_dir(state_dir, worktree_key=worktree_key)

    resolved = (state_dir / _CHECKPOINT_DB_FILENAME).resolve()
    repo_root = get_repo_root()
    if repo_root is None:
        return resolved

    legacy_path = repo_root / ".agdt" / _CHECKPOINT_DB_FILENAME
    is_canonical_workflow_state_dir = _canonical_worktree_key_from_state_dir(state_dir, repo_root) is not None
    if _same_resolved_path(resolved, legacy_path):
        resolved = _resolve_scoped_redirect_db_path(
            repo_root=repo_root,
            worktree_key=worktree_key,
            legacy_path=legacy_path,
        )
        _emit_legacy_checkpoint_warning(legacy_path, resolved)
    elif is_canonical_workflow_state_dir:
        _emit_legacy_checkpoint_warning(legacy_path, resolved)
    return resolved


def resolve_effective_workflow_state_dir(
    *,
    state_dir: Path,
    worktree_key: str | None,
) -> Path:
    """Return the effective workflow state directory after any legacy-root redirect.

    When *state_dir* would cause the checkpoint database to alias the legacy
    repository-root path, the canonical scoped directory is returned instead so
    that callers such as ``ExecutionLock`` use the same directory as
    ``get_checkpointer()``.  Both callers must use the same directory or a
    concurrent normal invocation can acquire a different lock file while writing
    to the same redirected database.

    Args:
        state_dir: The workflow-resolved state directory from ``get_state_dir()``.
        worktree_key: The validated active worktree key for redirect resolution.

    Returns:
        The canonical scoped state directory when a redirect applies; otherwise
        *state_dir* unchanged.
    """
    from agentic_devtools.state import get_repo_root

    repo_root = get_repo_root()
    if repo_root is None:
        return state_dir

    legacy_path = repo_root / ".agdt" / _CHECKPOINT_DB_FILENAME
    if _same_resolved_path(state_dir / _CHECKPOINT_DB_FILENAME, legacy_path):
        redirected = _resolve_scoped_redirect_db_path(
            repo_root=repo_root,
            worktree_key=worktree_key,
            legacy_path=legacy_path,
        )
        return redirected.parent
    return state_dir


def get_checkpointer(
    db_path: str | None = None,
    *,
    state_dir: Path | None = None,
    worktree_key: str | None = None,
) -> SqliteSaver:
    """Create a SqliteSaver checkpointer for durable workflow state.

    At most one of ``state_dir`` and ``db_path`` may be provided. When neither
    is provided, the path is resolved via ``get_state_dir()``.

    Args:
        db_path: *User-supplied* path to a SQLite database file.  The value
            is expanded (``~``) and resolved to absolute form.  Use this only
            for custom overrides external to the normal workflow scope (e.g.
            tests or ad-hoc tooling). Do not pass workflow-derived paths here;
            use ``state_dir`` instead.
        state_dir: A pre-validated, workflow-resolved state directory (a
            ``Path`` object already returned by ``get_state_dir()``).  The
            database file is placed at ``state_dir / "orchestration.db"``
            unless that would alias the legacy repository-root database, in
            which case workflow-managed initialization is redirected to the
            canonical scoped database.  Non-canonical override paths remain
            authoritative when they do not alias the legacy root path.
        worktree_key: Optional validated active worktree key for
            workflow-managed calls.  Used to verify canonical scoped paths and
            to build the canonical redirect target when a workflow-managed
            path would otherwise alias the legacy repository-root database.
            When omitted, legacy-root redirect falls back to bootstrap state.

    Returns:
        A configured ``SqliteSaver`` instance with the schema initialized.

    Note:
        The caller owns the underlying SQLite connection.  When the
        checkpointer is no longer needed, close it with
        ``saver.conn.close()`` to release the file descriptor.
    """
    if db_path is not None and state_dir is not None:
        raise ValueError("get_checkpointer() accepts only one of db_path or state_dir")

    if db_path is None:
        from agentic_devtools.state import get_state_dir

        resolved_state_dir = state_dir if state_dir is not None else get_state_dir(create=False)
        resolved = _resolve_workflow_managed_db_path(
            state_dir=Path(resolved_state_dir),
            worktree_key=worktree_key,
        )
    else:
        resolved = Path(db_path).expanduser().resolve()

    os.makedirs(resolved.parent, exist_ok=True)

    conn = sqlite3.connect(str(resolved), check_same_thread=False)
    saver = SqliteSaver(conn)
    saver.setup()
    return saver
