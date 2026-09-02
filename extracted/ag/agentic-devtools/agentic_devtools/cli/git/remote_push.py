"""Shared commit-and-push helper for audit workflows.

Centralises the git subprocess execution, author config, error handling, and
token redaction so ``apply.py`` and ``dispatch.py`` do not duplicate this
plumbing.
"""

from __future__ import annotations

import logging
import subprocess
from pathlib import Path
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


def commit_and_push_branch(
    *,
    repo_path: str,
    branch: str,
    add_paths: list[str],
    commit_message: str,
    author_name: str = "AMARSNIK_swica",
    author_email: str = "amarsnik_swica@users.noreply.github.com",
    start_point: str | None = None,
    force: bool = True,
    allow_empty: bool = False,
    remote: str = "origin",
    token_remote_url: str | None = None,
    skip_checkout: bool = False,
) -> None:
    """Create a branch, commit files, and push to a remote.

    This helper is shared by the audit ``apply`` and ``dispatch`` code paths to
    avoid duplicating git subprocess plumbing.

    The push identity depends on which remote is used:

    * When ``token_remote_url`` is ``None`` (the default), the push goes to the
      bare ``remote`` (default ``"origin"``).  The credentials come from whatever
      ``actions/checkout`` persisted — normally the ambient ``GITHUB_TOKEN``.
      Use this for workflows that grant ``contents: write`` to ``GITHUB_TOKEN``
      (e.g. ``audit-review-feedback-apply.yml``).

    * When ``token_remote_url`` is provided, the push uses that URL verbatim
      (typically an ``https://x-access-token:<PAT>@github.com/...`` URL).  The
      token is redacted from all error messages.  Use this for workflows where
      ``actions/checkout`` does *not* persist ``GITHUB_TOKEN`` credentials (e.g.
      ``audit-review-feedback.yml`` with ``persist-credentials: false``).

    Args:
        repo_path: Absolute path to the git repository root.
        branch: Branch name to create/reset and push.
        add_paths: Repo-relative paths to stage (passed to ``git add --``).
        commit_message: Full commit message string.
        author_name: Git ``user.name`` to configure for the commit.
        author_email: Git ``user.email`` to configure for the commit.
        start_point: If given, the commit/branch to branch off of
            (``git checkout -B <branch> <start_point>``).  Ignored when
            ``skip_checkout`` is ``True``.
        force: When ``True``, push with ``--force`` (default).
        allow_empty: When ``True``, pass ``--allow-empty`` to ``git commit``.
        remote: Bare remote name to push to when ``token_remote_url`` is
            ``None`` (default: ``"origin"``).
        token_remote_url: Optional full remote URL (with embedded PAT) to use
            as the push destination instead of ``remote``.
        skip_checkout: When ``True``, skip the ``git checkout -B`` step.
            Use this when the caller has already created/switched to the target
            branch (e.g. ``apply.py`` must copy files between checkout and
            staging, so it manages the checkout itself).

    Raises:
        subprocess.CalledProcessError: When any git command returns a non-zero
            exit code.  The error message has the token redacted when
            ``token_remote_url`` is provided.
    """
    repo_root = Path(repo_path).resolve()

    # Extract the embedded credential from the token URL (if any) so it can be
    # redacted from error messages even when only a prefix/suffix of the URL
    # appears in git's stderr output.
    embedded_secret: str = ""
    if token_remote_url:
        _parsed = urlparse(token_remote_url)
        if _parsed.password:
            embedded_secret = _parsed.password

    def _redact(text: str) -> str:
        if embedded_secret and embedded_secret in text:
            text = text.replace(embedded_secret, "***")
        if token_remote_url and token_remote_url in text:
            text = text.replace(token_remote_url, "<redacted-url>")
        return text

    def _run_git(step: str, *args: str) -> None:
        cmd = ["git", "-C", str(repo_root), *args]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            shell=False,
        )
        if result.returncode != 0:
            raw_err = result.stderr.strip() or result.stdout.strip()
            safe_msg = _redact(raw_err)
            safe_cmd = [_redact(arg) for arg in cmd]
            logger.error(
                "git %s failed (step: %s): %s",
                args[0] if args else "",
                step,
                safe_msg,
            )
            raise subprocess.CalledProcessError(
                result.returncode,
                safe_cmd,
                output=None,
                stderr=safe_msg,
            )

    if not skip_checkout:
        if start_point:
            _run_git("create branch", "checkout", "-B", branch, start_point)
        else:
            _run_git("create branch", "checkout", "-B", branch)

    if add_paths:
        _run_git("stage files", "add", "--", *add_paths)

    _run_git("config user.name", "config", "user.name", author_name)
    _run_git("config user.email", "config", "user.email", author_email)

    commit_args: list[str] = ["commit"]
    if allow_empty:
        commit_args.append("--allow-empty")
    commit_args += ["-m", commit_message]
    _run_git("commit", *commit_args)

    push_dest = token_remote_url if token_remote_url else remote
    push_args: list[str] = ["push"]
    if force:
        push_args.append("--force")
    push_args += [push_dest, f"HEAD:refs/heads/{branch}"]
    _run_git("push", *push_args)
