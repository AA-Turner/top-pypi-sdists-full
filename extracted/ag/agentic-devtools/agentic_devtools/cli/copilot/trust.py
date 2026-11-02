"""Pre-seed GitHub Copilot CLI *trusted folders* so that agdt-created worktrees
do not block on the interactive "Confirm folder trust" prompt.

The trust prompt is a separate security gate from ``--allow-all``: it is governed
solely by the ``trustedFolders`` array in ``~/.copilot/config.json`` (location
overridable via the ``COPILOT_HOME`` environment variable). No CLI flag or
environment variable suppresses it, so the only non-interactive way to avoid the
prompt is to pre-populate that array *before* a ``copilot`` session is launched.

This module does exactly that, idempotently and best-effort:

* ``config.json`` is JSONC (it has leading ``//`` comment lines); the header is
  preserved across the read-modify-write.
* The write is performed in place under :func:`agentic_devtools.file_locking.locked_file`
  (no ``os.replace`` — that would raise a sharing violation on Windows while a
  live session holds the file open).
* All failures degrade silently to today's behavior (the prompt is shown); this
  module never raises into the calling workflow.
"""

from __future__ import annotations

import json
import logging
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import IO, cast

from agentic_devtools.file_locking import FileLockError, locked_file

logger = logging.getLogger(__name__)

# Project-config flag (``.agdt/config/project.json``) and env kill-switch that
# gate automatic worktree trust-seeding.
_PROJECT_FLAG = "auto_trust_copilot_worktrees"
_ENV_KILL_SWITCH = "AGDT_AUTO_TRUST_COPILOT"
_DISABLED_VALUES = frozenset({"0", "false", "no", "off"})

# Matches a run of leading blank lines and/or ``//`` line comments that precede
# the JSON object in Copilot CLI's ``config.json`` (supports LF and CRLF).
_LEADING_COMMENT_RE = re.compile(r"^(?:[ \t]*//[^\r\n]*(?:\r?\n)|[ \t]*(?:\r?\n))+")


@dataclass(frozen=True)
class TrustMutationResult:
    """Outcome of a locked trusted-folder mutation."""

    succeeded: bool
    added: bool = False


def _in_test_environment() -> bool:
    """Return ``True`` when running inside a pytest session.

    Mirrors ``worktree_setup._in_test_environment`` (kept local to avoid a
    circular import) so that wiring call sites can invoke
    :func:`seed_worktree_trust` unconditionally without mutating the developer's
    real ``~/.copilot/config.json`` during test runs.
    """
    return bool(os.environ.get("PYTEST_CURRENT_TEST"))


def get_copilot_config_path() -> Path:
    """Return the path to Copilot CLI's ``config.json`` (honors ``COPILOT_HOME``)."""
    home = os.environ.get("COPILOT_HOME")
    base = Path(home) if home else (Path.home() / ".copilot")
    return base / "config.json"


def _normalize_path(path: str) -> str:
    """Return an absolute, normalized, OS-native path string."""
    return os.path.normpath(os.path.abspath(path))


def _path_key(path: str) -> str:
    """Return a comparison key for *path* (case-insensitive on Windows)."""
    normalized = _normalize_path(path)
    return normalized.lower() if os.name == "nt" else normalized


def _is_ancestor_or_equal(ancestor: str, target: str) -> bool:
    """Return ``True`` when *target* is *ancestor* itself or nested below it."""
    a = _path_key(ancestor)
    t = _path_key(target)
    if a == t:
        return True
    try:
        return os.path.commonpath([a, t]) == a
    except ValueError:
        # Different drives / mixed absolute-relative — not comparable.
        return False


def _is_already_trusted(folders: list[str], target: str, *, subtree_trust: bool) -> bool:
    """Return ``True`` when *target* is already covered by *folders*.

    With ``subtree_trust=True`` a trusted ancestor covers *target*; otherwise an
    exact entry is required (ancestors do not count). ``subtree_trust`` defaults
    to ``False`` everywhere because Copilot CLI's subtree-trust semantics are not
    yet empirically confirmed.
    """
    for folder in folders:
        if not isinstance(folder, str):
            continue
        if subtree_trust:
            if _is_ancestor_or_equal(folder, target):
                return True
        elif _path_key(folder) == _path_key(target):
            return True
    return False


def _split_jsonc_header(raw: str) -> tuple[str, str]:
    """Split *raw* into (leading-comment-header, json-body).

    Copilot CLI's ``config.json`` begins with ``//`` comment lines; ``json.loads``
    cannot parse those, so they are peeled off and preserved verbatim.
    """
    match = _LEADING_COMMENT_RE.match(raw)
    if match:
        return raw[: match.end()], raw[match.end() :]
    return "", raw


def ensure_trusted_folder(path: str, *, subtree_trust: bool = False) -> bool:
    """Idempotently add *path* to Copilot CLI's ``trustedFolders``.

    Must be called *before* a ``copilot`` session is spawned so the CLI loads —
    and therefore preserves — the entry. Best-effort: returns ``True`` when the
    folder is trusted after the call, ``False`` on any handled error. Never
    raises into the caller.
    """
    return _ensure_trusted_folder(path, subtree_trust=subtree_trust).succeeded


def _ensure_trusted_folder(path: str, *, subtree_trust: bool = False) -> TrustMutationResult:
    """Add *path* under the config lock and report whether this call added it."""
    config_path = get_copilot_config_path()
    target = _normalize_path(path)
    try:
        with locked_file(config_path, mode="r+", encoding="utf-8") as handle:
            file_handle = cast(IO[str], handle)
            raw = file_handle.read()
            header, body = _split_jsonc_header(raw)
            data = json.loads(body) if body.strip() else {}
            if not isinstance(data, dict):
                return TrustMutationResult(False)
            folders = data.get("trustedFolders")
            if not isinstance(folders, list):
                folders = []
            if _is_already_trusted(folders, target, subtree_trust=subtree_trust):
                return TrustMutationResult(True)
            folders.append(target)
            data["trustedFolders"] = folders
            file_handle.seek(0)
            file_handle.write(header + json.dumps(data, indent=2) + "\n")
            file_handle.truncate()
    except (OSError, FileLockError, ValueError) as exc:
        logger.debug("Copilot trust seed skipped for %s: %s", target, exc)
        return TrustMutationResult(False)
    return TrustMutationResult(
        _verify_trusted(config_path, target, subtree_trust=subtree_trust),
        added=True,
    )


def _verify_trusted(config_path: Path, target: str, *, subtree_trust: bool) -> bool:
    """Re-read *config_path* and confirm *target* survived the write."""
    try:
        raw = config_path.read_text(encoding="utf-8")
    except OSError:
        return False
    _, body = _split_jsonc_header(raw)
    try:
        data = json.loads(body) if body.strip() else {}
    except ValueError:
        return False
    if not isinstance(data, dict):
        return False
    folders = data.get("trustedFolders")
    if not isinstance(folders, list):
        return False
    return _is_already_trusted(folders, target, subtree_trust=subtree_trust)


def is_trusted_folder(path: str, *, subtree_trust: bool = False) -> bool:
    """Return whether *path* is already covered by Copilot trust settings."""
    return _verify_trusted(
        get_copilot_config_path(),
        _normalize_path(path),
        subtree_trust=subtree_trust,
    )


def remove_trusted_folder(path: str) -> bool:
    """Best-effort removal of an exact Copilot trusted-folder entry."""
    config_path = get_copilot_config_path()
    target = _normalize_path(path)
    try:
        with locked_file(config_path, mode="r+", encoding="utf-8") as handle:
            file_handle = cast(IO[str], handle)
            raw = file_handle.read()
            header, body = _split_jsonc_header(raw)
            data = json.loads(body)
            if not isinstance(data, dict):
                return False
            folders = data.get("trustedFolders")
            if not isinstance(folders, list):
                return False

            removed = False
            remaining: list[object] = []
            for folder in folders:
                if isinstance(folder, str) and _path_key(folder) == _path_key(target):
                    removed = True
                else:
                    remaining.append(folder)
            if not removed:
                return False

            data["trustedFolders"] = remaining
            file_handle.seek(0)
            file_handle.write(header + json.dumps(data, indent=2) + "\n")
            file_handle.truncate()
    except (OSError, FileLockError, ValueError) as exc:
        logger.debug("Copilot trust removal skipped for %s: %s", target, exc)
        return False
    return not _verify_trusted(config_path, target, subtree_trust=False)


def is_auto_trust_enabled() -> bool:
    """Return whether automatic worktree trust-seeding is enabled.

    Disabled when the ``AGDT_AUTO_TRUST_COPILOT`` env var is a falsy value
    (``0``/``false``/``no``/``off``), or when the project-config flag
    ``auto_trust_copilot_worktrees`` is set to such a value. Enabled (default)
    otherwise.
    """
    kill = os.environ.get(_ENV_KILL_SWITCH, "").strip().lower()
    if kill in _DISABLED_VALUES:
        return False
    try:
        from agentic_devtools.cli.config.project_config import get_effective_project_config_value

        configured = get_effective_project_config_value(_PROJECT_FLAG)
    except Exception:
        return True
    if configured is None:
        return True
    return configured.strip().lower() not in _DISABLED_VALUES


def seed_worktree_trust_result(
    worktree_path: str,
    *,
    repos_parent: str | None = None,
    subtree_trust: bool = False,
) -> TrustMutationResult:
    """Best-effort: add *worktree_path* to Copilot's trusted folders.

    Returns a :class:`TrustMutationResult` so callers that need *both* the
    success signal (``succeeded``) *and* the ownership flag (``added``) can
    consume them independently.  ``succeeded`` is ``False`` and ``added`` is
    ``False`` for the same early-exit conditions as :func:`seed_worktree_trust`.
    On a successful seed a one-line notice is printed for transparency.
    """
    _sentinel = TrustMutationResult(False)
    if _in_test_environment():
        return _sentinel
    if not is_auto_trust_enabled():
        return _sentinel
    target = _normalize_path(worktree_path)
    if repos_parent is not None and not _is_ancestor_or_equal(repos_parent, target):
        logger.debug("Refusing to trust %s outside repos parent %s", target, repos_parent)
        return _sentinel
    mutation = _ensure_trusted_folder(target, subtree_trust=subtree_trust)
    if mutation.succeeded and mutation.added:
        print(f"Added {target} to Copilot trusted folders ({get_copilot_config_path()}).")
    return mutation


def seed_worktree_trust(
    worktree_path: str,
    *,
    repos_parent: str | None = None,
    subtree_trust: bool = False,
) -> bool:
    """Best-effort: add *worktree_path* to Copilot's trusted folders.

    Returns ``True`` when the folder is trusted after the call (either already
    present or successfully written and verified), ``False`` otherwise.
    No-ops (returning ``False``) inside pytest, when auto-trust is disabled, or
    when *worktree_path* escapes *repos_parent* (a path-traversal guard applied
    only when *repos_parent* is provided).

    Callers that also need the *ownership* flag (i.e., whether *this* call added
    the entry, for later cleanup) should use :func:`seed_worktree_trust_result`
    instead.
    """
    return seed_worktree_trust_result(worktree_path, repos_parent=repos_parent, subtree_trust=subtree_trust).succeeded
