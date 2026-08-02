"""Provider-neutral data models for the issue-tracking abstraction.

These intentionally carry only the fields the ticket-management commands and
skills actually consume. Each provider maps its host-specific payload onto them,
so consumers never see a GitLab- or GitHub-shaped object.
"""

from dataclasses import dataclass, field


@dataclass
class Issue:
    """An issue, as exposed by any :class:`IssueTrackingProvider`."""

    iid: str = ""
    title: str = ""
    description: str = ""
    web_url: str = ""
    state: str = ""
    labels: list[str] = field(default_factory=list)
    assignees: list[str] = field(default_factory=list)
    author: str = ""
    weight: int | None = None


@dataclass
class Epic:
    """An epic (or the closest provider equivalent) with its child linkage."""

    iid: str = ""
    title: str = ""
    description: str = ""
    web_url: str = ""
    labels: list[str] = field(default_factory=list)


@dataclass
class Label:
    """A label, resolved or created on a project or on the owner namespace."""

    name: str
    color: str = ""
    description: str = ""
