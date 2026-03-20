"""Spec-to-Git linkage — branch/PR association for spec artifacts (#1018).

Links are stored in spec artifact metadata:
    metadata["git_links"] = [
        {"id": "uuid", "type": "branch", "ref": "issue-42-add-api", "url": null,
         "linked_at": "ISO", "linked_by": null, "auto": true},
        ...
    ]
"""

from __future__ import annotations

import subprocess
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..db import ThreadSafeConnection

from . import artifact_storage
from .artifacts import ArtifactType


@dataclass(frozen=True)
class GitLink:
    id: str
    type: str  # "branch" or "pr"
    ref: str  # branch name or PR number string
    url: str | None
    linked_at: str
    linked_by: str | None
    auto: bool


def parse_git_links(metadata: dict[str, Any]) -> list[GitLink]:
    """Extract GitLink list from artifact metadata."""
    raw = metadata.get("git_links", [])
    if not isinstance(raw, list):
        return []
    links: list[GitLink] = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        try:
            links.append(
                GitLink(
                    id=item.get("id", ""),
                    type=item.get("type", ""),
                    ref=str(item.get("ref", "")),
                    url=item.get("url"),
                    linked_at=item.get("linked_at", ""),
                    linked_by=item.get("linked_by"),
                    auto=bool(item.get("auto", False)),
                )
            )
        except (TypeError, ValueError):
            continue
    return links


def add_git_link(metadata: dict[str, Any], link: GitLink) -> dict[str, Any]:
    """Return new metadata with link appended. Deduplicates by type+ref."""
    new_meta = dict(metadata)
    existing = list(new_meta.get("git_links", []))
    for item in existing:
        if isinstance(item, dict) and item.get("type") == link.type and str(item.get("ref")) == link.ref:
            return new_meta  # Already linked
    existing.append(
        {
            "id": link.id,
            "type": link.type,
            "ref": link.ref,
            "url": link.url,
            "linked_at": link.linked_at,
            "linked_by": link.linked_by,
            "auto": link.auto,
        }
    )
    new_meta["git_links"] = existing
    return new_meta


def remove_git_link(metadata: dict[str, Any], link_id: str) -> dict[str, Any]:
    """Return new metadata without the specified link."""
    new_meta = dict(metadata)
    existing = list(new_meta.get("git_links", []))
    new_meta["git_links"] = [item for item in existing if not (isinstance(item, dict) and item.get("id") == link_id)]
    return new_meta


def detect_current_branch() -> str | None:
    """Detect current git branch via rev-parse. Returns None if not in a git repo."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            branch = result.stdout.strip()
            if branch and branch != "HEAD":  # HEAD = detached
                return branch
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return None


def link_branch_to_spec(
    db: ThreadSafeConnection,
    fqn: str,
    branch: str,
    *,
    user_id: str | None = None,
    auto: bool = False,
) -> dict[str, Any] | None:
    """Add a branch link to spec metadata. Returns updated artifact dict."""
    art = artifact_storage.get_artifact_by_fqn(db, fqn)
    if art is None or art["type"] != ArtifactType.SPEC.value:
        return None
    link = GitLink(
        id=str(uuid.uuid4()),
        type="branch",
        ref=branch,
        url=None,
        linked_at=datetime.now(timezone.utc).isoformat(),
        linked_by=user_id,
        auto=auto,
    )
    new_meta = add_git_link(art["metadata"], link)
    if new_meta is art["metadata"]:  # No change (deduplicated)
        return art
    return artifact_storage.update_artifact(db, art["id"], metadata=new_meta)


def link_pr_to_spec(
    db: ThreadSafeConnection,
    fqn: str,
    pr_number: str,
    pr_url: str | None = None,
    *,
    user_id: str | None = None,
) -> dict[str, Any] | None:
    """Add a PR link to spec metadata. Returns updated artifact dict."""
    art = artifact_storage.get_artifact_by_fqn(db, fqn)
    if art is None or art["type"] != ArtifactType.SPEC.value:
        return None
    link = GitLink(
        id=str(uuid.uuid4()),
        type="pr",
        ref=str(pr_number),
        url=pr_url,
        linked_at=datetime.now(timezone.utc).isoformat(),
        linked_by=user_id,
        auto=False,
    )
    new_meta = add_git_link(art["metadata"], link)
    if new_meta is art["metadata"]:
        return art
    return artifact_storage.update_artifact(db, art["id"], metadata=new_meta)


def unlink_from_spec(
    db: ThreadSafeConnection,
    fqn: str,
    link_id: str,
) -> dict[str, Any] | None:
    """Remove a link by ID. Returns updated artifact dict."""
    art = artifact_storage.get_artifact_by_fqn(db, fqn)
    if art is None or art["type"] != ArtifactType.SPEC.value:
        return None
    new_meta = remove_git_link(art["metadata"], link_id)
    return artifact_storage.update_artifact(db, art["id"], metadata=new_meta)


def get_spec_links(db: ThreadSafeConnection, fqn: str) -> list[GitLink]:
    """Return all links for a spec."""
    art = artifact_storage.get_artifact_by_fqn(db, fqn)
    if art is None:
        return []
    return parse_git_links(art.get("metadata", {}))
