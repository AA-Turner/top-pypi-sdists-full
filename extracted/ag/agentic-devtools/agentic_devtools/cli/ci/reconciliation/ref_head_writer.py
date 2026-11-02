"""Private Git Data writer for snapshot-bound queue-state updates."""

from __future__ import annotations

import base64
import json
import re
from collections.abc import Callable
from typing import Any


def _is_ref_conflict(
    exc: RuntimeError,
    ref_endpoint: str,
    captured_head: str,
    *,
    api: Callable[..., str],
    sha_from: Callable[..., str],
) -> bool:
    text = str(exc)
    status = getattr(exc, "http_status", None)
    if status is None:
        if re.search(r"(?<!\d)409(?!\d)", text):
            status = 409
        elif re.search(r"(?<!\d)422(?!\d)", text):
            status = 422
    if status == 409:
        return True
    if status != 422:
        return False
    if re.search(r"\b(?:non[-_ ]fast[-_ ]forward|not (?:a )?fast[- ]forward)\b", text, re.I):
        return True
    try:
        current_head = sha_from(api(ref_endpoint), "object", "sha")
    except Exception:
        return False
    return current_head != captured_head


def _write_ref_head(
    repo: str,
    state_ref: str,
    *,
    api: Callable[..., str],
    bootstrap: Callable[[str, str], None],
    prepare_content: Callable[[str], bytes],
    conflict_error: type[Exception],
    expected_head: str | None = None,
) -> None:
    """Write a child of one observed head, failing closed without a stale retry.

    ``api`` is the caller's credential boundary. ``prepare_content`` validates
    and serializes that exact snapshot. A supplied ``expected_head`` is used
    without reading the ref; otherwise an absent ref is bootstrapped and reread.
    A base tree preserves all paths except the queue document.
    """

    def sha_from(response: str, *keys: str) -> str:
        try:
            value: Any = json.loads(response)
        except ValueError as exc:
            raise RuntimeError("Invalid GitHub Git Data response") from exc
        for key in keys:
            value = value.get(key) if isinstance(value, dict) else None
        if not isinstance(value, str) or not value:
            raise RuntimeError("Invalid GitHub Git Data SHA")
        return value

    root = f"/repos/{repo}/git"
    ref_endpoint = f"{root}/ref/heads/{state_ref}"
    head = expected_head
    if head is None:
        try:
            response = api(ref_endpoint)
        except RuntimeError as exc:
            if not (re.search(r"(?<!\d)404(?!\d)", str(exc)) or "not found" in str(exc).lower()):
                raise
            bootstrap(repo, state_ref)
            response = api(ref_endpoint)
        head = sha_from(response, "object", "sha")
    content = prepare_content(head)
    tree = sha_from(api(f"{root}/commits/{head}"), "tree", "sha")
    blob = sha_from(
        api(
            f"{root}/blobs",
            method="POST",
            body={"content": base64.b64encode(content).decode("ascii"), "encoding": "base64"},
        ),
        "sha",
    )
    replacement_tree = sha_from(
        api(
            f"{root}/trees",
            method="POST",
            body={
                "base_tree": tree,
                "tree": [{"path": ".agdt/ai-pr-loop-state.json", "mode": "100644", "type": "blob", "sha": blob}],
            },
        ),
        "sha",
    )
    commit = sha_from(
        api(
            f"{root}/commits",
            method="POST",
            body={
                "message": "chore: update ai-pr-loop reconciliation state",
                "tree": replacement_tree,
                "parents": [head],
            },
        ),
        "sha",
    )
    try:
        api(f"{root}/refs/heads/{state_ref}", method="PATCH", body={"sha": commit, "force": False})
    except RuntimeError as exc:
        if _is_ref_conflict(exc, ref_endpoint, head, api=api, sha_from=sha_from):
            raise conflict_error("Queue state changed during save") from exc
        raise
