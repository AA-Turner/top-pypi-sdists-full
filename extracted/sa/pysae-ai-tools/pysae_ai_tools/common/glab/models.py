"""Data models for GitLab API objects."""

from dataclasses import dataclass, field
from typing import Any, Self


@dataclass
class GitLabUser:
    """GitLab user summary (as embedded in issue responses)."""

    name: str = ""
    username: str = ""


@dataclass
class GitLabIssue:
    """A GitLab issue as returned by the REST API.

    Fields map to the GitLab Issues API response.
    Optional fields default to sensible values so the dataclass
    can be constructed from partial API data.
    """

    iid: int = 0
    project_id: int = 0
    title: str = ""
    web_url: str = ""
    labels: list[str] = field(default_factory=list)
    description: str = ""
    weight: int | None = None
    assignees: list[GitLabUser] = field(default_factory=list)
    author: GitLabUser = field(default_factory=GitLabUser)
    created_at: str = ""

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> Self:
        """Construct from a raw GitLab API JSON dict."""
        return cls(
            iid=data.get("iid", 0),
            project_id=data.get("project_id", 0),
            title=data.get("title", ""),
            web_url=data.get("web_url", ""),
            labels=data.get("labels", []),
            description=data.get("description") or "",
            weight=data.get("weight"),
            assignees=[
                GitLabUser(name=a.get("name", ""), username=a.get("username", "")) for a in data.get("assignees", [])
            ],
            author=GitLabUser(
                name=(data.get("author") or {}).get("name", ""), username=(data.get("author") or {}).get("username", "")
            ),
            created_at=data.get("created_at", ""),
        )


@dataclass
class Mr:
    """A GitLab merge request as returned by the REST API.

    Fields map to the GitLab Merge Requests API response. Optional fields
    default to sensible values so the dataclass can be constructed from the
    partial payloads returned by the list endpoints (related_merge_requests,
    closed_by, source-branch lookup) as well as the full single-MR endpoint.
    """

    iid: int = 0
    title: str = ""
    description: str = ""
    web_url: str = ""
    source_branch: str = ""
    target_branch: str = ""
    state: str = ""
    labels: list[str] = field(default_factory=list)
    assignees: list[GitLabUser] = field(default_factory=list)
    author: GitLabUser = field(default_factory=GitLabUser)

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> Self:
        """Construct from a raw GitLab API JSON dict."""
        return cls(
            iid=data.get("iid", 0),
            title=data.get("title", ""),
            description=data.get("description") or "",
            web_url=data.get("web_url", ""),
            source_branch=data.get("source_branch", ""),
            target_branch=data.get("target_branch", ""),
            state=data.get("state", ""),
            labels=data.get("labels", []),
            assignees=[
                GitLabUser(name=a.get("name", ""), username=a.get("username", "")) for a in data.get("assignees", [])
            ],
            author=GitLabUser(
                name=(data.get("author") or {}).get("name", ""), username=(data.get("author") or {}).get("username", "")
            ),
        )
