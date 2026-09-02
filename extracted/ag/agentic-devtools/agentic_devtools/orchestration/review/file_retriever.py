"""File content retrieval for source context enrichment.

Provides ``retrieve_file_content`` for fetching file content via git-show
(primary) with Azure DevOps Items API fallback, plus helpers for path
normalization, binary detection, and size threshold enforcement.
"""

from __future__ import annotations

import json
import logging
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger(__name__)

# Maximum file size (bytes) before skipping retrieval.
DEFAULT_MAX_FILE_SIZE_BYTES: int = 500_000  # 500KB

# Binary file extensions that should be skipped.
DEFAULT_BINARY_EXTENSIONS: frozenset[str] = frozenset({
    ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".ico", ".svg",
    ".woff", ".woff2", ".ttf", ".eot", ".otf",
    ".pdf", ".zip", ".gz", ".tar", ".rar", ".7z",
    ".exe", ".dll", ".so", ".dylib", ".bin",
    ".pyc", ".pyo", ".class", ".o", ".obj",
    ".db", ".sqlite", ".sqlite3",
    ".mp3", ".mp4", ".wav", ".avi", ".mov",
})  # fmt: skip

# Default max concurrency for parallel file retrieval.
DEFAULT_MAX_CONCURRENCY: int = 10


def _normalize_max_concurrency(max_concurrency: int) -> int:
    """Normalize max_concurrency to a safe positive integer."""
    try:
        parsed = int(max_concurrency)
    except (TypeError, ValueError):
        return 1
    return max(1, parsed)


@dataclass
class RetrievalResult:
    """Result of a file content retrieval attempt."""

    content: str | None = None
    context_status: str = "success"
    context_status_reason: str = ""
    estimated_tokens: int = 0
    file_size: int = 0


def normalize_path_for_git(path: str) -> str:
    """Strip leading '/' for git-show commands.

    Args:
        path: File path (possibly with leading slash from ADO).

    Returns:
        Path without leading slash.
    """
    return path.lstrip("/")


def normalize_path_for_ado(path: str) -> str:
    """Ensure leading '/' for ADO Items API.

    Args:
        path: File path.

    Returns:
        Path with leading slash.
    """
    if not path.startswith("/"):
        return f"/{path}"
    return path


def is_binary_file(file_entry: dict[str, Any], binary_extensions: frozenset[str] = DEFAULT_BINARY_EXTENSIONS) -> bool:
    """Detect whether a file is binary.

    Checks the ``isBinary`` field first (from diff enrichment), then falls
    back to extension-based heuristic.

    Args:
        file_entry: File entry dict from graph state.
        binary_extensions: Set of extensions to treat as binary.

    Returns:
        True if file is detected as binary.
    """
    # Prefer explicit field from diff enrichment
    is_binary = file_entry.get("isBinary")
    if is_binary is True:
        return True
    if is_binary is False:
        return False

    path = file_entry.get("path", "")
    dot_idx = path.rfind(".")
    if dot_idx >= 0:
        ext = path[dot_idx:].lower()
        if ext in binary_extensions:
            return True

    return False


def _retrieve_via_git_show(
    commit_ref: str,
    file_path: str,
    max_size_bytes: int = DEFAULT_MAX_FILE_SIZE_BYTES,
) -> RetrievalResult:
    """Retrieve file content using ``git show <commit>:<path>``.

    Args:
        commit_ref: Git commit reference (SHA, branch, tag).
        file_path: Repository-relative file path (no leading slash).
        max_size_bytes: Maximum file size before skipping.

    Returns:
        RetrievalResult with content or status information.
    """
    git_path = normalize_path_for_git(file_path)

    # Check blob size before buffering the full content.
    try:
        size_result = subprocess.run(
            ["git", "cat-file", "-s", f"{commit_ref}:{git_path}"],
            capture_output=True,
            encoding="utf-8",
            timeout=10,
            shell=False,
        )
    except subprocess.TimeoutExpired:
        return RetrievalResult(
            context_status="unavailable",
            context_status_reason="git_cat_file_timeout",
        )
    except OSError as exc:
        return RetrievalResult(
            context_status="unavailable",
            context_status_reason=f"git_cat_file_error: {exc}",
        )

    if size_result.returncode == 0:
        try:
            blob_size = int(size_result.stdout.strip())
        except ValueError:
            blob_size = 0
        if blob_size > max_size_bytes:
            return RetrievalResult(
                context_status="skipped_too_large",
                context_status_reason=f"exceeds {max_size_bytes} bytes",
                file_size=blob_size,
            )

    try:
        result = subprocess.run(
            ["git", "show", f"{commit_ref}:{git_path}"],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=30,
            shell=False,
        )
    except subprocess.TimeoutExpired:
        return RetrievalResult(
            context_status="unavailable",
            context_status_reason="git_show_timeout",
        )
    except OSError as exc:
        return RetrievalResult(
            context_status="unavailable",
            context_status_reason=f"git_show_error: {exc}",
        )

    if result.returncode != 0:
        return RetrievalResult(
            context_status="unavailable",
            context_status_reason="git_show_failed",
        )

    content = result.stdout
    file_size = len(content.encode("utf-8", errors="replace"))
    if file_size > max_size_bytes:
        return RetrievalResult(
            context_status="skipped_too_large",
            context_status_reason=f"exceeds {max_size_bytes} bytes",
            file_size=file_size,
        )

    return RetrievalResult(
        content=content,
        context_status="success",
        file_size=file_size,
    )


def _retrieve_via_ado_api(
    file_path: str,
    commit_ref: str,
    state: dict[str, Any],
    max_size_bytes: int = DEFAULT_MAX_FILE_SIZE_BYTES,
) -> RetrievalResult:
    """Retrieve file content via Azure DevOps Items API (fallback).

    Args:
        file_path: File path (will be normalized with leading slash).
        commit_ref: Commit hash for version descriptor.
        state: Graph state with organization, project, repo_id.
        max_size_bytes: Maximum content size before returning oversized status.

    Returns:
        RetrievalResult with content or status information.
    """
    from urllib.parse import quote

    try:
        from agentic_devtools.cli.azure_devops.auth import get_auth_headers, get_pat

        pat = get_pat()
        headers = get_auth_headers(pat)
    except Exception:
        return RetrievalResult(
            context_status="unavailable",
            context_status_reason="auth_failed",
        )

    organization = state.get("organization", "")
    project = state.get("project", "")
    repo_id = state.get("repo_id", "")

    if not organization or not project or not repo_id:
        return RetrievalResult(
            context_status="unavailable",
            context_status_reason="missing_ado_config",
        )

    try:
        import requests

        scope_path = normalize_path_for_ado(file_path)
        project_encoded = quote(project, safe="")
        scope_path_encoded = quote(scope_path, safe="/")

        url = (
            f"{organization}/{project_encoded}/_apis/git/repositories/"
            f"{repo_id}/items?path={scope_path_encoded}"
            f"&versionDescriptor.version={commit_ref}"
            f"&versionDescriptor.versionType=commit"
            f"&includeContent=true&api-version=7.1-preview.1"
        )

        response = requests.get(url, headers=headers, timeout=30, stream=True)
        if response.status_code != 200:
            response.close()
            return RetrievalResult(
                context_status="unavailable",
                context_status_reason=f"ado_api_status_{response.status_code}",
            )

        # Reject oversized responses early using Content-Length when available.
        content_length = response.headers.get("Content-Length")
        if content_length is not None:
            try:
                if int(content_length) > max_size_bytes:
                    response.close()
                    return RetrievalResult(
                        context_status="skipped_too_large",
                        context_status_reason=f"ado_api_content_length_exceeds_{max_size_bytes}",
                        file_size=int(content_length),
                    )
            except ValueError:
                pass

        # Stream body with a hard byte cap to bound memory usage.
        chunks: list[bytes] = []
        total = 0
        for chunk in response.iter_content(chunk_size=65536):
            if not chunk:
                continue
            chunks.append(chunk)
            total += len(chunk)
            if total > max_size_bytes:
                response.close()
                return RetrievalResult(
                    context_status="skipped_too_large",
                    context_status_reason=f"ado_api_streamed_size_exceeds_{max_size_bytes}",
                    file_size=total,
                )

        raw = b"".join(chunks)
        content_type = response.headers.get("Content-Type", "")

        if "application/json" in content_type:
            try:
                data = json.loads(raw)
            except ValueError:
                return RetrievalResult(
                    context_status="unavailable",
                    context_status_reason="ado_api_json_decode_error",
                )
            content = data.get("content", "")
            if not isinstance(content, str):
                return RetrievalResult(
                    context_status="unavailable",
                    context_status_reason="ado_api_non_string_content",
                )
            return RetrievalResult(content=content, context_status="success", file_size=len(raw))
        if content_type.startswith("text/"):
            text = raw.decode("utf-8", errors="replace")
            return RetrievalResult(content=text, context_status="success", file_size=len(raw))

        return RetrievalResult(
            context_status="skipped_binary",
            context_status_reason="binary_content_type",
        )
    except Exception as exc:
        return RetrievalResult(
            context_status="unavailable",
            context_status_reason=f"ado_api_error: {exc}",
        )


def retrieve_file_content(
    file_path: str,
    commit_ref: str,
    state: dict[str, Any],
    *,
    max_size_bytes: int = DEFAULT_MAX_FILE_SIZE_BYTES,
) -> RetrievalResult:
    """Retrieve file content with git-show primary and ADO API fallback.

    Args:
        file_path: Repository-relative file path.
        commit_ref: Git commit reference for the version to retrieve.
        state: Graph state (for ADO API fallback configuration).
        max_size_bytes: Maximum file size threshold.

    Returns:
        RetrievalResult with content or structured status.
    """
    # Primary: git show
    result = _retrieve_via_git_show(commit_ref, file_path, max_size_bytes)
    if result.context_status == "success":
        return result
    # Don't fallback for deliberate skip statuses
    if result.context_status in ("skipped_too_large", "skipped_binary"):
        return result

    # Fallback: ADO Items API
    logger.info("git-show failed for %s@%s, trying ADO API fallback", file_path, commit_ref[:8])
    ado_result = _retrieve_via_ado_api(file_path, commit_ref, state, max_size_bytes)
    return ado_result


def retrieve_files_concurrent(
    file_requests: list[tuple[str, str, str]],
    state: dict[str, Any],
    *,
    max_concurrency: int = DEFAULT_MAX_CONCURRENCY,
    max_size_bytes: int = DEFAULT_MAX_FILE_SIZE_BYTES,
) -> dict[tuple[str, str], RetrievalResult]:
    """Retrieve multiple files concurrently.

    Deduplicates requests by (file_path, branch_side) to avoid redundant fetches.

    Args:
        file_requests: List of (file_path, commit_ref, branch_side) tuples.
        state: Graph state for ADO fallback.
        max_concurrency: Maximum parallel retrievals.
        max_size_bytes: Per-file size threshold.

    Returns:
        Dict mapping (file_path, branch_side) to RetrievalResult.
    """
    # Deduplicate
    unique_requests: dict[tuple[str, str], tuple[str, str]] = {}
    for file_path, commit_ref, branch_side in file_requests:
        key = (file_path, branch_side)
        if key not in unique_requests:
            unique_requests[key] = (file_path, commit_ref)

    results: dict[tuple[str, str], RetrievalResult] = {}

    if not unique_requests:
        return results

    def _fetch(key: tuple[str, str], file_path: str, commit_ref: str) -> tuple[tuple[str, str], RetrievalResult]:
        return key, retrieve_file_content(file_path, commit_ref, state, max_size_bytes=max_size_bytes)

    safe_concurrency = _normalize_max_concurrency(max_concurrency)
    with ThreadPoolExecutor(max_workers=min(safe_concurrency, len(unique_requests))) as executor:
        futures = {executor.submit(_fetch, key, fp, cr): key for key, (fp, cr) in unique_requests.items()}
        for future in as_completed(futures):
            try:
                key, result = future.result()
                results[key] = result
            except Exception as exc:
                key = futures[future]
                results[key] = RetrievalResult(
                    context_status="unavailable",
                    context_status_reason=f"concurrent_error: {exc}",
                )

    return results
