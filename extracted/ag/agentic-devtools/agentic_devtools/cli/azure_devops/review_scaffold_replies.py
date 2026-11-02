"""Azure DevOps thread reply request helpers."""

from typing import Any

from .helpers import build_cross_identity_reply_content


def _append_path_to_url(base_url: str, *segments: str | int) -> str:
    """Append path segments to a URL, preserving any query string.

    If ``base_url`` contains a query string (e.g. ``?api-version=7.0``),
    the new segments are inserted before it.  Trailing/leading slashes are
    normalised to avoid double-slash artifacts.

    Args:
        base_url: The base URL (may include a query string).
        *segments: Path segments to append (converted to str).

    Returns:
        URL with segments appended before the query string, or the
        original *base_url* unchanged when no segments are provided.
    """
    if not segments:
        return base_url

    if "?" in base_url:
        path_part, query_part = base_url.split("?", 1)
    else:
        path_part, query_part = base_url, None

    normalized_base = path_part.rstrip("/")
    suffix = "/".join(str(s).strip("/") for s in segments)

    new_path = f"{normalized_base}/{suffix}" if suffix else normalized_base

    if query_part is not None:
        return f"{new_path}?{query_part}"
    return new_path


def _post_reply(
    requests_module: Any,
    headers: dict[str, str],
    threads_url: str,
    thread_id: int,
    content: str,
) -> int:
    """Post a reply to an existing thread.

    Args:
        requests_module: requests module for HTTP calls.
        headers: Auth headers.
        threads_url: Base threads URL (without thread ID suffix).
        thread_id: Thread to reply to.
        content: Reply content (markdown).

    Returns:
        The new comment ID.
    """
    url = _append_path_to_url(threads_url, thread_id, "comments")
    body = {"content": content, "commentType": "text"}
    response = requests_module.post(url, headers=headers, json=body, timeout=30)
    response.raise_for_status()
    return response.json()["id"]


def _post_cross_identity_reply(
    requests_module: Any,
    headers: dict[str, str],
    threads_url: str,
    thread_id: int,
    content: str,
) -> int:
    """Post a cross-identity update reply to an existing thread.

    Used when the original thread comment is owned by a different identity
    and cannot be PATCHed. Posts the full content as a reply prefixed with
    a cross-identity-update marker.

    Args:
        requests_module: requests module for HTTP calls.
        headers: Auth headers.
        threads_url: Base threads URL.
        thread_id: Thread to reply to.
        content: Full scaffold content to post.

    Returns:
        The new reply comment ID.
    """
    return _post_reply(requests_module, headers, threads_url, thread_id, build_cross_identity_reply_content(content))
