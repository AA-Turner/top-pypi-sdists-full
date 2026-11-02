"""Complete GitHub pull-request file inventory evidence."""

from __future__ import annotations

import json
from collections.abc import Callable, Mapping

from agentic_devtools.cli.ci.retry import retry_with_backoff


def parse_changed_file_count(data: Mapping[str, object]) -> int | None:
    """Return a valid nonnegative changed-file count from PR metadata."""
    count = data.get("changed_files")
    return count if isinstance(count, int) and not isinstance(count, bool) and count >= 0 else None


def decode_paginated_file_entries(response: str) -> list[object] | None:
    """Decode concatenated JSON array pages, rejecting missing or malformed pages."""
    if not response.strip():
        return None
    decoder = json.JSONDecoder()
    index = 0
    entries: list[object] = []
    try:
        while index < len(response):
            while index < len(response) and response[index].isspace():
                index += 1
            if index == len(response):
                break
            page, end = decoder.raw_decode(response, index)
            if not isinstance(page, list):
                return None
            entries.extend(page)
            index = end
    except json.JSONDecodeError:
        return None
    return entries


def parse_complete_pr_file_response(response: str, expected_count: int) -> list[str] | None:
    """Return paths only for a complete, uncapped inventory matching metadata."""
    if isinstance(expected_count, bool) or not isinstance(expected_count, int) or not 0 <= expected_count < 3000:
        return None
    entries = decode_paginated_file_entries(response)
    if entries is None:
        return None
    paths: list[str] = []
    for entry in entries:
        if not isinstance(entry, dict):
            return None
        filename = entry.get("filename")
        if not isinstance(filename, str) or not filename.strip():
            return None
        paths.append(filename)
    return paths if len(paths) == expected_count else None


class GitHubPRFilesMixin:
    """Expose a strict inventory operation alongside the generic file-list API."""

    _gh_api: Callable[..., str]
    _repo_api: Callable[[str], str]

    @retry_with_backoff()
    def list_pr_files_complete(self, pr_number: int, expected_count: int) -> list[str] | None:
        """List PR files only when the raw paginated response proves completeness."""
        if isinstance(expected_count, bool) or not isinstance(expected_count, int) or not 0 <= expected_count < 3000:
            return None
        response = self._gh_api(self._repo_api(f"/pulls/{pr_number}/files"), paginate=True)
        return parse_complete_pr_file_response(response, expected_count)
