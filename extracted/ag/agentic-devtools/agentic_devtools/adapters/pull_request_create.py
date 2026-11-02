"""Provider-neutral pull-request creation adapters."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol
from urllib.parse import urlparse

from agentic_devtools import state as _state_module
from agentic_devtools.cli.azure_devops.commands import PullRequestCreationPostSubmitError
from agentic_devtools.cli.azure_devops.commands import create_pull_request as azure_create_pull_request
from agentic_devtools.cli.ci.credential_roles import require_default_repo_workflow_token
from agentic_devtools.cli.github.repo_resolution import resolve_github_repo_safe
from agentic_devtools.cli.subprocess_utils import run_safe
from agentic_devtools.cli.workflows.advancement import try_advance_workflow_after_pr_creation
from agentic_devtools.file_locking import locked_file, locked_state_file
from agentic_devtools.state import STATE_FILENAME

_GITHUB_CLI_TIMEOUT_SECONDS = 60
_AZURE_CLI_TIMEOUT_SECONDS = 90.0
# Azure CLI verification runs two bounded probes before the bounded PR-create
# subprocess. Allow all three budgets plus time for state cleanup before a
# concurrent creation gives up waiting for the bridge lock.
_AZURE_BRIDGE_LOCK_TIMEOUT_SECONDS = 3 * _AZURE_CLI_TIMEOUT_SECONDS + 30.0
_AZURE_BRIDGE_LOCK_FILENAME = "azure-pr-create-bridge.lock"
_EXISTING_GH_PR_RE = re.compile(
    r'(?is)\b(?:an?\s+(?:open\s+)?pull\s+request(?:\s+for\s+branch\s+".*?"\s+into\s+branch\s+".*?")?)\s+already exists:\s*(https?://\S+)'
)


@contextmanager
def _read_modify_write_state_at(state_dir: Path, lock_timeout: float = 30.0) -> Iterator[dict[str, Any]]:
    """Like ``read_modify_write_state``, but pinned to an explicit directory.

    ``azure_create_pull_request()`` can call ``set_value("pull_request_id", ...)``,
    which updates the bootstrap ``worktree_key`` mid-flight. If the bridge's
    restore step re-resolved ``get_state_dir()`` afterwards (as plain
    ``read_modify_write_state()`` does), it could then operate on a different
    directory than the one its snapshot came from, silently skipping
    restoration and leaking the bridge's temporary values into whichever
    state file happened to live there. Pinning the directory captured before
    ``azure_create_pull_request()`` runs keeps the snapshot/restore pair
    atomic against exactly the directory they operated on.
    """
    path = state_dir / STATE_FILENAME
    with locked_state_file(path, timeout=lock_timeout) as f:
        content = f.read()
        try:
            loaded = json.loads(content) if content.strip() else {}
        except json.JSONDecodeError:
            loaded = {}
        state: dict[str, Any] = loaded if isinstance(loaded, dict) else {}
        original_content = json.dumps(state, indent=2, ensure_ascii=False)
        yield state
        new_content = json.dumps(state, indent=2, ensure_ascii=False)
        if new_content != original_content:
            f.seek(0)
            f.write(new_content)
            f.truncate()
            f.flush()
            os.fsync(f.fileno())
            try:
                from agentic_devtools.cli.git.agdt_branch import mark_dirty

                mark_dirty()
            except ImportError:  # pragma: no cover
                pass  # agdt_branch not available (e.g., minimal install)


def _merge_stranded_value(new_state: dict[str, Any], key: str, value: Any) -> None:
    """Merge one stranded key into *new_state*, preferring existing values on conflict.

    Dict values (e.g. ``workflow: {...}``) are merged recursively instead of
    via a whole-mapping ``setdefault``. A plain ``setdefault`` would treat an
    existing mapping as a full conflict and silently drop stranded fields at
    deeper levels. Existing destination leaf values win on conflict. If
    *new_state* already holds a non-dict value under *key*, that value wins
    outright and is left untouched.
    """
    if isinstance(value, dict):
        if key not in new_state:
            new_state[key] = {}
        existing = new_state[key]
        if not isinstance(existing, dict):
            # Destination already holds a non-dict value (e.g. a concurrent
            # writer set a scalar under this key); leave it as-is rather than
            # clobbering it with a mapping built from the stranded value.
            return
        for nested_key, nested_value in value.items():
            _merge_stranded_value(existing, nested_key, nested_value)
    else:
        new_state.setdefault(key, value)


def _migrate_state_dir(old_dir: Path, new_dir: Path) -> None:
    """Copy state stranded by a mid-flight worktree-key switch.

    ``_sync_bootstrap_for_context_key()`` can move the active worktree key --
    and therefore what ``get_state_dir()`` resolves to -- after state has
    already been written to *old_dir* (e.g. when creating the first PR for a
    worktree that has no issue key set yet). Without this, the just-persisted
    ``pull_request_id``/``github.*`` keys, and any prior workflow state that
    already lived in *old_dir*, would be stranded and invisible to
    subsequent commands, which now resolve *new_dir* instead. Keys already
    present in *new_dir* win on conflict, since they reflect state a
    concurrent writer already established under the new context.
    """
    with _read_modify_write_state_at(old_dir) as old_state:
        stranded = dict(old_state)
    if not stranded:
        return
    with _read_modify_write_state_at(new_dir) as new_state:
        for key, value in stranded.items():
            _merge_stranded_value(new_state, key, value)


def _bridge_lock_path() -> Path:
    """Resolve the Azure bridge lock path at a location stable across worktree-key switches.

    Must NOT be derived from ``get_state_dir()``: the legacy command can call
    ``set_value("pull_request_id", ...)`` mid-flight, which switches the
    active worktree key -- and therefore what ``get_state_dir()`` resolves to.
    A lock keyed off that directory would let a second invocation started
    after the switch acquire a *different* lock file than the one the first
    invocation still holds, letting both legacy calls interleave their
    bridged state. The repository root is stable across that switch, so the
    lock lives under its (already git-ignored) ``.agdt`` directory instead.
    """
    root = _state_module.get_repo_root() or Path.cwd()
    lock_dir = root / ".agdt"
    lock_dir.mkdir(parents=True, exist_ok=True)
    return lock_dir / _AZURE_BRIDGE_LOCK_FILENAME


@dataclass(frozen=True)
class PullRequestCreateRequest:
    """Validated provider-neutral pull-request creation request.

    ``reviewers`` is supported for both providers: the ``github`` adapter passes
    them to ``gh pr create --reviewer``, and the ``azure_devops`` adapter maps
    them onto ``az repos pr create --reviewers``.
    """

    provider: str
    source_branch: str
    title: str
    body: str = ""
    target_branch: str = "main"
    draft: bool = True
    reviewers: tuple[str, ...] = ()
    dry_run: bool = False
    body_is_explicit: bool = True

    def __post_init__(self) -> None:
        if not isinstance(self.provider, str) or self.provider not in {"azure_devops", "github"}:
            raise ValueError("provider must be 'azure_devops' or 'github'")
        for name, value in (("source_branch", self.source_branch), ("title", self.title)):
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} is required")
        if not isinstance(self.body, str):
            raise ValueError("body must be a string")
        if not isinstance(self.target_branch, str) or not self.target_branch.strip():
            raise ValueError("target_branch is required")
        if not isinstance(self.draft, bool):
            raise ValueError("draft must be a boolean")
        if not isinstance(self.reviewers, tuple) or any(
            not isinstance(reviewer, str) or not reviewer.strip() for reviewer in self.reviewers
        ):
            raise ValueError("reviewers must be a tuple of non-empty strings")
        if not isinstance(self.dry_run, bool):
            raise ValueError("dry_run must be a boolean")
        if not isinstance(self.body_is_explicit, bool):
            raise ValueError("body_is_explicit must be a boolean")
        # Normalize branch/title/reviewer fields so downstream `gh`/`az` calls never
        # receive surrounding whitespace that only the *validation* stripped away.
        object.__setattr__(self, "source_branch", self.source_branch.strip())
        object.__setattr__(self, "title", self.title.strip())
        object.__setattr__(self, "target_branch", self.target_branch.strip())
        object.__setattr__(self, "reviewers", tuple(reviewer.strip() for reviewer in self.reviewers))


@dataclass(frozen=True)
class PullRequestCreateResult:
    """Equivalent result for either pull-request provider."""

    success: bool
    provider: str
    status: str
    url: str = ""
    error: str = ""

    def as_dict(self) -> dict[str, object]:
        """Return a JSON-serializable result."""
        return {
            "success": self.success,
            "provider": self.provider,
            "status": self.status,
            "url": self.url,
            "error": self.error,
        }


class PullRequestCreateAdapter(Protocol):
    """Transport implemented by a pull-request provider."""

    def create(self, request: PullRequestCreateRequest) -> PullRequestCreateResult:
        """Create one pull request."""


class AzureDevOpsPullRequestCreateAdapter:
    """Delegate Azure DevOps creation to the established command."""

    def create(self, request: PullRequestCreateRequest) -> PullRequestCreateResult:
        """Pass the immutable request directly to the legacy Azure command."""
        if request.provider != "azure_devops":
            return PullRequestCreateResult(False, request.provider, "failed", error="provider mismatch")
        lock_path = _bridge_lock_path()
        with locked_file(lock_path, mode="a+", timeout=_AZURE_BRIDGE_LOCK_TIMEOUT_SECONDS):
            # Capture the directory once before the command can shift the
            # bootstrap worktree key while persisting the created PR ID.
            state_dir = _state_module.get_state_dir()
            create_error: PullRequestCreateResult | None = None
            created_pr_id: int | None = None

            def _record_created_pr_id(pull_request_id: int) -> None:
                nonlocal created_pr_id
                created_pr_id = pull_request_id

            result_url: object = None
            try:
                try:
                    result_url = azure_create_pull_request(
                        timeout=_AZURE_CLI_TIMEOUT_SECONDS,
                        source_branch=request.source_branch,
                        title=request.title,
                        title_is_rendered=True,
                        description=request.body,
                        target_branch=request.target_branch,
                        draft=request.draft,
                        reviewers=",".join(request.reviewers),
                        dry_run=request.dry_run,
                        on_pull_request_created=_record_created_pr_id,
                    )
                except PullRequestCreationPostSubmitError as exc:
                    create_error = PullRequestCreateResult(
                        True,
                        request.provider,
                        "indeterminate",
                        error=str(exc)[:1000],
                    )
                except SystemExit as exc:
                    create_error = PullRequestCreateResult(
                        False, request.provider, "failed", error=f"exit status {exc.code}"
                    )
                except subprocess.TimeoutExpired:
                    create_error = PullRequestCreateResult(
                        True,
                        request.provider,
                        "indeterminate",
                        error="Azure DevOps pull-request creation outcome is indeterminate: the subprocess timed out",
                    )
                except Exception as exc:
                    create_error = PullRequestCreateResult(False, request.provider, "failed", error=str(exc)[:1000])
            finally:
                # A state persistence or migration failure must never override
                # remote creation success: callers could otherwise retry and
                # create a duplicate PR.
                try:
                    if created_pr_id is not None:
                        with _state_module.read_modify_write_state(
                            _bootstrap_update=("pull_request_id", created_pr_id),
                            _override_migrated_keys=("pull_request_id",),
                        ) as state:
                            state["pull_request_id"] = created_pr_id
                        # Only perform the stranded-state merge when the captured
                        # PR ID and returned URL identify the destination context.
                        # An unrelated context switch must not receive this state.
                        new_state_dir = _state_module.get_state_dir()
                        with _state_module.read_modify_write_state() as state:
                            created_pr_id = state.get("pull_request_id")
                            issue_key = state.get("issue_key")
                            jira = state.get("jira")
                            jira_issue_key = jira.get("issue_key") if isinstance(jira, dict) else None
                        has_issue_key = type(issue_key) is int or (
                            isinstance(issue_key, str) and bool(issue_key.strip())
                        )
                        has_issue_key = has_issue_key or (
                            isinstance(jira_issue_key, str) and bool(jira_issue_key.strip())
                        )
                        url_pr_id = (
                            urlparse(result_url).path.rstrip("/").rsplit("/", 1)[-1]
                            if isinstance(result_url, str)
                            else ""
                        )
                        if (
                            create_error is None
                            and type(created_pr_id) is int
                            and created_pr_id > 0
                            and url_pr_id == str(created_pr_id)
                            and not has_issue_key
                            and new_state_dir != state_dir
                            and new_state_dir.parent == state_dir.parent
                            and new_state_dir.name == f"PR{created_pr_id}"
                        ):
                            _migrate_state_dir(state_dir, new_state_dir)
                except Exception as exc:
                    print(
                        f"Warning: pull request state persistence/migration failed: {exc}",
                        file=sys.stderr,
                    )
            if create_error is not None:
                return create_error
        return PullRequestCreateResult(
            True,
            request.provider,
            "dry_run" if request.dry_run else "created",
            url=result_url if isinstance(result_url, str) else "",
        )


class GitHubPullRequestCreateAdapter:
    """Create GitHub pull requests through the GitHub CLI."""

    def create(self, request: PullRequestCreateRequest) -> PullRequestCreateResult:
        """Run ``gh pr create`` with the complete request."""
        if request.provider != "github":
            return PullRequestCreateResult(False, request.provider, "failed", error="provider mismatch")
        if request.dry_run:
            print("[DRY RUN] Would create GitHub PR:")
            print(f"  Source Branch: {request.source_branch}")
            print(f"  Target Branch: {request.target_branch}")
            print(f"  Title: {request.title}")
            print(f"  Draft Mode: {request.draft}")
            if request.reviewers:
                print(f"  Reviewers: {', '.join(request.reviewers)}")
            return PullRequestCreateResult(True, request.provider, "dry_run")

        repo = resolve_github_repo_safe()
        if not repo:
            return PullRequestCreateResult(
                False,
                request.provider,
                "failed",
                error="Could not determine GitHub repository for pull-request creation",
            )
        try:
            result = self._run_gh_create(request, repo)
        except subprocess.TimeoutExpired:
            return PullRequestCreateResult(
                True,
                request.provider,
                "indeterminate",
                error="GitHub pull-request creation outcome is indeterminate: the subprocess timed out",
            )
        except RuntimeError as exc:
            return PullRequestCreateResult(False, request.provider, "failed", error=str(exc)[:1000])
        combined_output = f"{result.stdout or ''}\n{result.stderr or ''}"
        pr_url = result.stdout.strip()
        post_create_warning = ""
        if result.returncode != 0:
            existing_match = _EXISTING_GH_PR_RE.search(combined_output)
            existing_url = existing_match.group(1).rstrip(").,") if existing_match else ""
            if existing_url:
                pr_url = existing_url
            else:
                stdout_pr_url = next(
                    (
                        line.strip()
                        for line in (result.stdout or "").splitlines()
                        if re.fullmatch(r"https?://\S+/pull/[1-9][0-9]*/?", line.strip())
                    ),
                    "",
                )
                if not stdout_pr_url:
                    return PullRequestCreateResult(
                        False,
                        request.provider,
                        "failed",
                        error=str(result.stderr or result.stdout or "gh pr create failed")[:1000],
                    )
                pr_url = stdout_pr_url
                post_create_warning = str(result.stderr or f"gh pr create exited with status {result.returncode}")[
                    :1000
                ]
        gh_host = os.environ.get("GH_HOST", "").strip()
        github_server_url = (
            f"https://{gh_host.rstrip('/')}"
            if gh_host
            else os.environ.get("GITHUB_SERVER_URL", "https://github.com").rstrip("/")
        )
        expected = urlparse(github_server_url)
        parsed = urlparse(pr_url)
        expected_path_prefix = [part for part in expected.path.split("/") if part]
        path_parts = [part for part in parsed.path.split("/") if part]
        if expected_path_prefix and path_parts[: len(expected_path_prefix)] != expected_path_prefix:
            relative_parts: list[str] = []
        else:
            relative_parts = path_parts[len(expected_path_prefix) :]
        tail_parts = relative_parts[-4:]
        repo_owner, repo_name = repo.split("/", 1)
        if (
            parsed.scheme.casefold() != expected.scheme.casefold()
            or parsed.netloc.casefold() != expected.netloc.casefold()
            or len(relative_parts) != 4
            or tail_parts[0].casefold() != repo_owner.casefold()
            or tail_parts[1].casefold() != repo_name.casefold()
            or tail_parts[2] != "pull"
            or not re.fullmatch(r"[1-9][0-9]*", tail_parts[3])
        ):
            # A returned URL that doesn't identify the expected repository
            # must never be used to persist a PR ID into this repository's state.
            if result.returncode != 0:
                return PullRequestCreateResult(
                    False,
                    request.provider,
                    "failed",
                    error=str(result.stderr or result.stdout or "gh pr create failed")[:1000],
                )
            print(
                f"Warning: pull request created but its URL did not match the expected repository: {pr_url}",
                file=sys.stderr,
            )
            return PullRequestCreateResult(True, request.provider, "created_untracked", error=pr_url[:1000])
        else:
            pull_request_id = int(tail_parts[3])
        if post_create_warning:
            print(
                f"Warning: pull request created, but gh pr create exited with status {result.returncode}: "
                f"{post_create_warning}",
                file=sys.stderr,
            )
        try:
            # Defer publishing the new worktree key until the PR identifiers
            # have been committed and migrated under the repository-stable
            # transaction lock.
            with _state_module.read_modify_write_state(
                _bootstrap_update=("pull_request_id", pull_request_id),
                _override_migrated_keys=("pull_request_id", "github.pull_request_number"),
            ) as state:
                state["pull_request_id"] = pull_request_id
                github_section = state.get("github")
                if not isinstance(github_section, dict):
                    github_section = {}
                    state["github"] = github_section
                github_section["pull_request_number"] = pull_request_id
        except Exception as exc:
            # The remote PR already exists at this point. Reporting this as a
            # failed creation (like the pre-persistence error paths above)
            # would let a caller retry the task and create a duplicate PR, so
            # this is surfaced as a non-fatal warning instead -- the same
            # treatment given to workflow-advancement failures below.
            print(f"Warning: pull request created but state persistence failed: {exc}", file=sys.stderr)
        try:
            try_advance_workflow_after_pr_creation(pull_request_id, pr_url)
        except Exception as exc:
            print(f"Warning: pull request created but workflow advancement failed: {exc}", file=sys.stderr)
        return PullRequestCreateResult(True, request.provider, "created", url=pr_url, error=post_create_warning)

    def _run_gh_create(self, request: PullRequestCreateRequest, repo: str):
        """Execute ``gh pr create`` and return the raw subprocess result."""
        body_file = ""
        try:
            with tempfile.NamedTemporaryFile("w", suffix=".md", encoding="utf-8", delete=False) as handle:
                body_file = handle.name
                handle.write(request.body)
            os.chmod(body_file, 0o600)
            command = [
                "gh",
                "pr",
                "create",
                "--title",
                request.title,
                "--body-file",
                body_file,
                "--base",
                request.target_branch,
                "--head",
                request.source_branch,
            ]
            command.extend(["--repo", repo])
            if request.draft:
                command.append("--draft")
            for reviewer in request.reviewers:
                command.extend(["--reviewer", reviewer])
            result = run_safe(
                command,
                capture_output=True,
                text=True,
                shell=False,
                timeout=_GITHUB_CLI_TIMEOUT_SECONDS,
                env={**os.environ, "GH_TOKEN": require_default_repo_workflow_token("create a GitHub pull request")},
            )
        except subprocess.TimeoutExpired:
            raise
        except Exception as exc:
            raise RuntimeError(str(exc)[:1000]) from exc
        finally:
            if body_file:
                try:
                    Path(body_file).unlink(missing_ok=True)
                except OSError:
                    # Cleanup is best-effort only; a temp-file deletion failure
                    # must not change the already-determined PR creation result.
                    pass
        return result
