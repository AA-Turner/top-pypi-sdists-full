"""Source context enrichment for PR file reviews (FR-008).

Provides ``fetch_source_context()`` to retrieve full file content from
the source branch via Azure DevOps Items API, and
``extract_surrounding_context()`` to extract lines above/below diff hunks.

For LangChain-driven PR reviews, source context is enabled by default.
It is disabled by the ``--no-source-context`` CLI flag and the resolved
setting is persisted in the graph state as ``source_context_enabled`` and
workflow state as ``review.source_context_enabled``.
"""

from __future__ import annotations

import sys
from typing import Any
from urllib.parse import quote

import requests

from agentic_devtools.cli.azure_devops.auth import get_auth_headers, get_pat

# Minimum number of context lines above and below each diff hunk.
_MIN_CONTEXT_LINES: int = 20

# Maximum characters of full-file content injected as fallback source context
# when no diff line anchors are available.  Bounds the LLM context budget (and
# token limits) so large files don't blow up latency/cost or fail the review.
_MAX_FALLBACK_CONTEXT_CHARS: int = 8000

# Explicit marker inserted where fallback content was clipped, so the model
# knows the source context is not complete.
_TRUNCATION_MARKER: str = "\n... [source context truncated] ...\n"


def fetch_source_context(
    *,
    file_path: str,
    state: dict[str, Any],
) -> str | None:
    """Retrieve source context for a file from the source branch.

    Attempts to fetch the full file content via the Azure DevOps Items API.
    Falls back gracefully when retrieval fails (newly added files, API errors).

    Args:
        file_path: Repository-relative path of the file.
        state: Current graph state (contains ``commit_hash``, ``repo_id``,
            ``organization``, ``project``).

    Returns:
        File content as a string, or ``None`` if retrieval fails.
    """
    commit_hash = state.get("commit_hash", "")
    repo_id = state.get("repo_id", "")
    organization = state.get("organization", "")
    project = state.get("project", "")

    if not commit_hash or not repo_id or not organization or not project:
        return None

    try:
        pat = get_pat()
        headers = get_auth_headers(pat)
    except Exception:
        return None

    try:
        project_encoded = quote(project, safe="")
        # Use version descriptor to get file at specific commit
        scope_path = file_path if file_path.startswith("/") else f"/{file_path}"
        scope_path_encoded = quote(scope_path, safe="/")
        url = (
            f"{organization}/{project_encoded}/_apis/git/repositories/"
            f"{repo_id}/items?path={scope_path_encoded}"
            f"&versionDescriptor.version={commit_hash}"
            f"&versionDescriptor.versionType=commit"
            f"&includeContent=true&api-version=7.1-preview.1"
        )

        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code == 200:
            # The Items API returns content directly for text files
            content_type = response.headers.get("Content-Type", "")
            if "application/json" in content_type:
                data = response.json()
                content = data.get("content", "")
                if not isinstance(content, str):
                    return None
                return content
            # Only return text content — skip binary payloads (e.g. application/octet-stream)
            # that would inject garbage into the LLM prompt.
            if not content_type.startswith("text/"):
                return None
            return response.text
        return None
    except Exception as exc:
        print(f"Warning: could not fetch source context for {file_path}: {exc}", file=sys.stderr)
        return None


def extract_surrounding_context(
    file_content: str,
    diff_lines: list[tuple[int, int]],
    context_lines: int = _MIN_CONTEXT_LINES,
) -> str:
    """Extract surrounding context from file content around diff hunks.

    For each diff hunk (defined by a start and end line), extracts at
    least ``context_lines`` lines above and below, plus any import
    statements and class/function signatures that appear before the
    first hunk.

    Args:
        file_content: Full content of the file.
        diff_lines: List of ``(start_line, end_line)`` tuples (1-based).
        context_lines: Minimum lines of context above/below each hunk.

    Returns:
        Extracted context as a string with line numbers.
    """
    if context_lines < 0:
        raise ValueError("context_lines must be >= 0")

    if not file_content or not diff_lines:
        return ""

    lines = file_content.splitlines()
    total_lines = len(lines)

    if total_lines == 0:
        return ""

    # Collect line ranges to include
    included_ranges: list[tuple[int, int]] = []

    # Always include imports and signatures from the top of the file
    for i, line in enumerate(lines):
        stripped = line.strip()
        if (
            stripped.startswith("import ")
            or stripped.startswith("from ")
            or stripped.startswith("class ")
            or stripped.startswith("def ")
            or stripped.startswith("async def ")
        ):
            included_ranges.append((i, i))
        elif i > 50:
            break

    # Add context around each diff hunk
    for start, end in diff_lines:
        # Convert to 0-based
        ctx_start = max(0, start - 1 - context_lines)
        ctx_end = min(total_lines - 1, end - 1 + context_lines)
        # Skip ranges where the hunk is entirely beyond the file content.
        # This can happen when diff anchors reference base-file line numbers
        # for removed lines that do not exist in the source-branch version.
        if ctx_start > ctx_end:
            continue
        included_ranges.append((ctx_start, ctx_end))

    # Merge overlapping ranges
    merged = _merge_ranges(included_ranges)

    # Build output with line numbers
    output_parts: list[str] = []
    for idx, (start, end) in enumerate(merged):
        for i in range(start, min(end + 1, total_lines)):
            output_parts.append(f"{i + 1:>4} | {lines[i]}")
        if idx < len(merged) - 1:
            output_parts.append("...")

    return "\n".join(output_parts)


def bound_fallback_context(
    file_content: str,
    max_chars: int = _MAX_FALLBACK_CONTEXT_CHARS,
) -> str:
    """Bound full-file fallback context to a maximum character budget.

    When no diff line anchors are available, the reviewer falls back to the
    full file content.  For large files this can exceed the LLM context
    budget (increasing latency/cost or hitting token limits), so this caps
    the content to ``max_chars`` characters by keeping the head and tail of
    the file and inserting an explicit truncation marker in the middle so the
    model knows the context was clipped.

    Args:
        file_content: Full content of the file.
        max_chars: Maximum number of characters to return (must be > 0).

    Returns:
        The original content when it fits within ``max_chars``; otherwise a
        head + marker + tail excerpt bounded to ``max_chars``.  When
        ``max_chars`` is smaller than the truncation marker itself, a plain
        head slice of ``max_chars`` characters (without the marker) is
        returned.
    """
    if max_chars <= 0:
        raise ValueError("max_chars must be > 0")

    if len(file_content) <= max_chars:
        return file_content

    budget = max_chars - len(_TRUNCATION_MARKER)
    if budget <= 0:
        return file_content[:max_chars]

    # Favor the head when the budget splits unevenly: the beginning of a file
    # typically holds imports and critical setup that aid review context.
    tail_len = budget // 2
    head_len = budget - tail_len
    head = file_content[:head_len]
    # Guard against tail_len == 0: file_content[-0:] returns the entire string
    # in Python, which would silently exceed max_chars.
    tail = file_content[-tail_len:] if tail_len > 0 else ""
    return f"{head}{_TRUNCATION_MARKER}{tail}"


def _merge_ranges(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    if not ranges:
        return []

    sorted_ranges = sorted(ranges, key=lambda r: r[0])
    merged: list[tuple[int, int]] = [sorted_ranges[0]]

    for start, end in sorted_ranges[1:]:
        prev_start, prev_end = merged[-1]
        if start <= prev_end + 1:
            merged[-1] = (prev_start, max(prev_end, end))
        else:
            merged.append((start, end))

    return merged
