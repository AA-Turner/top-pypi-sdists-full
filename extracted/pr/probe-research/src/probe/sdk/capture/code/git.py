"""run git read-only and record provenance: HEAD, branch, dirty, and why git could not say."""

from __future__ import annotations
import os
import subprocess
from typing import Any


def _NONINTERACTIVE_ENV() -> dict:
    """Git env that fails fast instead of prompting for credentials."""
    return {
        **os.environ,
        "GIT_TERMINAL_PROMPT": "0",
        "GIT_SSH_COMMAND": os.environ.get(
            "GIT_SSH_COMMAND", "ssh -o BatchMode=yes -o StrictHostKeyChecking=accept-new"
        ),
    }


def _read_only(env: dict | None = None) -> dict:
    """Git env for a capture: ``GIT_OPTIONAL_LOCKS=0`` so ``status`` never
    refreshes and rewrites the user's index behind their back. Every git call
    a capture makes goes through here; a capture never writes to ``.git``."""
    return {**(os.environ if env is None else env), "GIT_OPTIONAL_LOCKS": "0"}


def _git(
    cwd: str,
    *args: str,
    env: dict | None = None,
    check: bool = True,
    timeout: float | None = None,
) -> str:
    try:
        proc = subprocess.run(
            ["git", *args],
            cwd=cwd,
            env=_read_only(env),
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        if check:
            raise SnapshotError(f"git {' '.join(args)}: timed out after {timeout}s") from None
        return ""
    if check and proc.returncode != 0:
        raise SnapshotError(f"git {' '.join(args)}: {proc.stderr.strip()}")
    return proc.stdout.strip()


def _repo_check(cwd: str) -> tuple[bool, str | None]:
    """``(inside a work tree, why git could not say)``. The reason is set only
    when git could not answer -- no git executable, or git refusing the repo
    (``detected dubious ownership`` in a container) -- never for a plain
    directory, which is not an error."""
    try:
        proc = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            cwd=cwd,
            env=_read_only(),
            capture_output=True,
            text=True,
        )
    except OSError as exc:  # no git binary (a slim image), or not executable
        return False, f"git is not runnable here ({type(exc).__name__})"
    if proc.returncode == 0 and proc.stdout.strip() == "true":
        return True, None
    stderr = proc.stderr.strip()
    if proc.returncode != 0 and "not a git repository" not in stderr:
        return False, (stderr.splitlines()[0] if stderr else f"git exited {proc.returncode}")
    return False, None


def is_git_repo(cwd: str) -> bool:
    """True inside a git work tree git can read. Any failure to ask -- no git
    executable, a repo git refuses -- is False, and the capture falls back to the
    directory manifest rather than to nothing."""
    return _repo_check(cwd)[0]


def _dot_git_above(cwd: str) -> bool:
    here = os.path.abspath(cwd)
    while True:
        if os.path.exists(os.path.join(here, ".git")):
            return True
        parent = os.path.dirname(here)
        if parent == here:
            return False
        here = parent


def capture_git_snapshot(run_id: str | None = None, cwd: str | None = None) -> dict[str, Any]:
    """Git PROVENANCE for the tree a run starts in: HEAD, branch, dirty.

    READ-ONLY. Three reads under ``GIT_OPTIONAL_LOCKS=0`` (``rev-parse --verify -q
    HEAD``, ``symbolic-ref --short -q HEAD``, ``status --porcelain``), so no object,
    ref or index write happens and none of what used to break capture can: no
    author identity (a bare pod), an unborn HEAD, a read-only ``.git``.

    ``commit`` and ``ref`` are always None: the shadow commit is retired (see the
    module docstring). They stay in the shape because callers read them.
    ``run_id`` is accepted and unused, for the same reason.

    Raises :class:`SnapshotError` if ``cwd`` is not a git repo.
    """
    cwd = cwd or os.getcwd()
    if not is_git_repo(cwd):
        raise SnapshotError(f"{cwd} is not a git repository")
    return _git_state(cwd)[0]


def _git_state(cwd: str) -> tuple[dict[str, Any], str | None]:
    """HEAD, branch and dirty, plus why dirty is unknown (or None).

    ``status`` reads the index and HEAD does not, so a corrupt index fails only
    the dirty check: HEAD and the branch are still recorded, dirty is None
    (unknown, never guessed) and git's reason is returned for ``git_error``.
    """
    head = _git(cwd, "rev-parse", "--verify", "-q", "HEAD", check=False) or None
    # An unborn branch still has a name; a detached HEAD has none (None).
    branch = _git(cwd, "symbolic-ref", "--short", "-q", "HEAD", check=False) or None
    dirty: bool | None
    try:
        dirty, error = bool(_git(cwd, "status", "--porcelain", check=True)), None
    except SnapshotError as exc:
        dirty, error = None, str(exc)
    return {"commit": None, "ref": None, "branch": branch, "head": head, "dirty": dirty}, error


def git_provenance(cwd: str) -> tuple[dict[str, Any] | None, str | None]:
    """``(capture_git_snapshot(...) or None, git_error or None)``, never raising.

    Git is provenance, not the record, so it may never cost the capture: a repo
    git cannot read is captured as a plain directory, and WHY is returned for
    ``meta.git_error``. A plain directory is not an error.
    """
    in_repo, reason = _repo_check(cwd)
    if not in_repo:
        # Only a directory that IS a repo (a `.git` above it) is missing
        # something; a plain folder has no provenance to lose.
        return None, (reason if reason and _dot_git_above(cwd) else None)
    try:
        info, error = _git_state(cwd)
    except (SnapshotError, OSError) as exc:
        return None, str(exc) or type(exc).__name__
    notice_old_snapshot_refs(cwd)
    return info, error


def _common_dir(cwd: str) -> str | None:
    common = _git(cwd, "rev-parse", "--git-common-dir", check=False)
    if not common:
        return None
    return os.path.abspath(common if os.path.isabs(common) else os.path.join(cwd, common))
from probe.sdk.capture.code.code import SnapshotError  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.capture.code.snapshot_refs import notice_old_snapshot_refs  # noqa: E402 -- pieces need each other; the front door loads this one first
