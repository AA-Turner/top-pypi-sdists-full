"""Fast provider connectivity checks for issue discovery."""

from __future__ import annotations

import multiprocessing
import subprocess
import time
from contextlib import suppress
from pathlib import Path
from queue import Empty
from typing import Any
from urllib.parse import urlparse

from agentic_devtools.cli.subprocess_utils import run_safe
from agentic_devtools.config import load_platform_config

_MAX_JIRA_PROBE_BODY_CHARS = 200


def _check_markdown_connectivity(git_root: Path, *, timeout: float) -> tuple[bool, str | None]:
    """Check that the markdown repo path is usable without network access."""
    del timeout
    try:
        if not git_root.exists():
            return False, f"Markdown workspace path does not exist: {git_root}"
        if not git_root.is_dir():
            return False, f"Markdown workspace path is not a directory: {git_root}"
        next(git_root.iterdir(), None)
    except OSError as exc:
        return False, f"Markdown workspace not accessible: {exc}"
    return True, None


def _jira_probe_worker(
    result_queue: Any,
    probe_url: str,
    headers: dict[str, str],
    timeout: float,
    verify: bool | str,
) -> None:
    """Execute the Jira HTTP probe in a child process with a hard parent deadline."""
    import requests

    try:
        response = requests.get(
            probe_url,
            headers=headers,
            timeout=timeout,
            verify=verify,
            allow_redirects=False,
        )
    except requests.Timeout as exc:
        result_queue.put(("timeout", str(exc)))
        return
    except requests.RequestException as exc:
        result_queue.put(("error", str(exc)))
        return
    except Exception as exc:  # noqa: BLE001
        result_queue.put(("error", str(exc)))
        return

    response_text = response.text
    result_queue.put(("response", response.status_code, response_text[:_MAX_JIRA_PROBE_BODY_CHARS]))


def _resolve_jira_probe_config(git_root: Path) -> tuple[str, dict[str, str], bool | str]:
    """Resolve Jira probe URL/auth/TLS settings using the shared adapter resolver."""
    from agentic_devtools.adapters import resolve_jira_config

    config = resolve_jira_config(git_root)
    headers = {**config.headers, "Accept": "application/json"}
    return config.base_url, headers, config.ssl_verify


def _run_jira_probe_with_deadline(
    probe_url: str,
    headers: dict[str, str],
    *,
    timeout: float,
    verify: bool | str,
) -> tuple[int | None, str | None, str | None]:
    """Run the Jira probe behind a hard wall-clock deadline."""
    result_queue: Any = None
    try:
        context = multiprocessing.get_context("spawn")
        result_queue = context.Queue()
        process = context.Process(
            target=_jira_probe_worker,
            args=(result_queue, probe_url, headers, timeout, verify),
        )
        started_at = time.monotonic()
        process.start()
        process.join(timeout)
        if process.is_alive():
            process.terminate()
            elapsed = time.monotonic() - started_at
            process.join(timeout=max(0.0, timeout - elapsed))
            if process.is_alive():
                process.kill()
                process.join(timeout=min(0.1, timeout))
            return None, None, f"Jira connectivity check timed out after {timeout:.1f}s"

        try:
            result = result_queue.get_nowait()
        except Empty:
            if process.exitcode not in (0, None):
                return None, None, f"Jira connectivity check failed: probe exited with code {process.exitcode}"
            return None, None, "Jira connectivity check failed: probe returned no result"
    except OSError as exc:
        return None, None, f"Jira connectivity check failed: {exc}"
    finally:
        with suppress(AttributeError):
            result_queue.close()
            result_queue.join_thread()

    if not isinstance(result, tuple) or not result:
        return None, None, "Jira connectivity check failed: probe returned an invalid result"

    if result[0] == "response" and len(result) == 3:
        return result[1], result[2], None
    if result[0] == "timeout" and len(result) == 2:
        return None, None, f"Jira connectivity check timed out after {timeout:.1f}s: {result[1]}"
    if result[0] == "error" and len(result) == 2:
        return None, None, f"Jira connectivity check failed: {result[1]}"
    return None, None, "Jira connectivity check failed: probe returned an invalid result"


def _check_jira_connectivity(git_root: Path, timeout: float) -> tuple[bool, str | None]:
    """Probe the configured Jira instance with a short timeout."""
    base_url, headers, ssl_verify = _resolve_jira_probe_config(git_root)

    parsed = urlparse(base_url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return False, f"Invalid Jira base URL configuration: {base_url}"

    probe_url = base_url.rstrip("/") + "/rest/api/2/myself"
    status_code, response_text, error = _run_jira_probe_with_deadline(
        probe_url,
        headers,
        timeout=timeout,
        verify=ssl_verify,
    )
    if error is not None:
        return False, error

    if status_code == 200:
        return True, None
    if status_code in {401, 403}:
        return False, "Jira authentication failed (401/403): credentials may be expired or missing"

    detail = (response_text or "").strip().replace("\n", " ")
    summary = detail[:_MAX_JIRA_PROBE_BODY_CHARS] if detail else "no response body"
    return False, f"Jira connectivity check failed with HTTP {status_code}: {summary}"


def _resolve_github_repo_slug(git_root: Path) -> tuple[str | None, str | None]:
    """Resolve the configured GitHub ``owner/repo`` slug for *git_root*."""
    platform_config = load_platform_config(str(git_root))
    github_cfg = platform_config.get("github", {})
    if not isinstance(github_cfg, dict):
        github_cfg = {}

    repo = github_cfg.get("repo")
    if isinstance(repo, str) and repo.strip():
        repo_slug = repo.strip()
    else:
        owner = github_cfg.get("repo_owner")
        name = github_cfg.get("repo_name")
        if not isinstance(owner, str) or not owner.strip() or not isinstance(name, str) or not name.strip():
            return None, "GitHub repository is not configured"
        repo_slug = f"{owner.strip()}/{name.strip()}"

    parts = repo_slug.split("/")
    if len(parts) != 2 or not parts[0].strip() or not parts[1].strip():
        return None, f"Invalid GitHub repository configuration: {repo_slug}"

    return f"{parts[0].strip()}/{parts[1].strip()}", None


def _check_github_connectivity(git_root: Path, timeout: float) -> tuple[bool, str | None]:
    """Check GitHub CLI access to the configured repository."""
    repo_slug, repo_error = _resolve_github_repo_slug(git_root)
    if repo_slug is None:
        return False, repo_error

    try:
        result = run_safe(
            ["gh", "repo", "view", repo_slug, "--json", "nameWithOwner"],
            capture_output=True,
            text=True,
            shell=False,
            timeout=timeout,
        )
    except FileNotFoundError:
        return False, "gh CLI not found in PATH"
    except subprocess.TimeoutExpired:
        return False, f"GitHub connectivity check timed out after {timeout:.1f}s"
    except OSError as exc:
        return False, f"GitHub connectivity check failed: {exc}"

    if result.returncode == 0:
        return True, None

    detail = (result.stderr or result.stdout or "").strip()
    if not detail:
        detail = f"gh repo view {repo_slug} failed with exit code {result.returncode}"
    return False, detail


def check_provider_connectivity(
    provider_slug: str,
    git_root: Path,
    timeout: float = 5.0,
) -> tuple[bool, str | None]:
    """Return whether the configured issue provider is reachable and authenticated.

    Returns a ``(is_connected, message)`` tuple. When the provider is unsupported,
    connectivity is treated as failed and the reason is returned as a string.
    """
    if timeout <= 0:
        return False, "Connectivity timeout must be greater than 0 seconds"

    provider = str(provider_slug).strip().lower()
    try:
        if provider == "jira":
            return _check_jira_connectivity(Path(git_root), timeout)
        if provider == "github":
            return _check_github_connectivity(Path(git_root), timeout)
        if provider == "markdown":
            return _check_markdown_connectivity(Path(git_root), timeout=timeout)
        return False, f"Unsupported issue provider: {provider or provider_slug}"
    except Exception as exc:  # noqa: BLE001
        return False, str(exc)
