"""GitHub implementation of :class:`IssueTrackingProvider`.

Issue operations are wired to the GitHub REST API through the shared ``gh``
runner (``common/github``). GitHub has no native epics, so the ``EPICS``
capability is unsupported (raises :class:`UnsupportedCapability`). Owner-scoped
labels are supported in a degraded form: GitHub only has per-repo labels, so
:meth:`ensure_owner_label` creates the label on the current repo.
"""

from typing import Any, ClassVar
from urllib.parse import quote

from ..github.runner import gh_api, gh_api_paginated
from .context import RepoContext
from .models import Epic, Issue, Label
from .platform import Platform
from .provider import Capability, IssueTrackingProvider, UnsupportedCapability

_STATE_TO_GITHUB = {"opened": "open", "closed": "closed", "all": "all"}


class GithubIssueTrackingProvider(IssueTrackingProvider):
    """Issue and repo-label operations backed by the GitHub REST API via ``gh``."""

    platform: ClassVar[Platform] = Platform.GITHUB
    capabilities: ClassVar[frozenset[Capability]] = frozenset({Capability.OWNER_LABELS})

    def __init__(self, ctx: RepoContext) -> None:
        self.ctx = ctx

    @property
    def _repo(self) -> str:
        return self.ctx.project

    @staticmethod
    def _label_names(labels: Any) -> list[str]:
        names: list[str] = []
        for label in labels or []:
            names.append(label["name"] if isinstance(label, dict) else label)
        return names

    @classmethod
    def _issue_from_api(cls, data: dict[str, Any]) -> Issue:
        return Issue(
            iid=str(data.get("number", "") or ""),
            title=data.get("title", "") or "",
            description=data.get("body") or "",
            web_url=data.get("html_url", "") or "",
            state=data.get("state", "") or "",
            labels=cls._label_names(data.get("labels")),
            assignees=[a.get("login", "") for a in data.get("assignees", []) or []],
            author=(data.get("user") or {}).get("login", "") or "",
            weight=None,
        )

    def current_user(self) -> str:
        data = gh_api("user")
        return data.get("login", "") if isinstance(data, dict) else ""

    def get_issue(self, iid: str) -> Issue:
        data = gh_api(f"repos/{self._repo}/issues/{iid}")
        if not isinstance(data, dict):
            raise LookupError(f"issue {iid} not found in {self._repo}")
        return self._issue_from_api(data)

    def create_issue(
        self,
        *,
        title: str,
        description: str,
        labels: list[str],
        assignees: list[str],
        weight: int | None = None,
    ) -> Issue:
        body: dict[str, Any] = {"title": title, "body": description}
        if labels:
            body["labels"] = labels
        if assignees:
            body["assignees"] = assignees
        data = gh_api(f"repos/{self._repo}/issues", method="POST", input_json=body)
        if not isinstance(data, dict):
            raise RuntimeError(f"failed to create issue in {self._repo}")
        return self._issue_from_api(data)

    def update_issue(
        self,
        iid: str,
        *,
        title: str | None = None,
        description: str | None = None,
        add_labels: list[str] | None = None,
        remove_labels: list[str] | None = None,
    ) -> Issue:
        body: dict[str, Any] = {}
        if title is not None:
            body["title"] = title
        if description is not None:
            body["body"] = description
        if add_labels or remove_labels:
            current = self.get_issue(iid).labels
            removed = set(remove_labels or [])
            names = [name for name in current if name not in removed]
            for name in add_labels or []:
                if name not in names:
                    names.append(name)
            body["labels"] = names
        data = gh_api(f"repos/{self._repo}/issues/{iid}", method="PATCH", input_json=body)
        if not isinstance(data, dict):
            raise RuntimeError(f"failed to update issue {iid} in {self._repo}")
        return self._issue_from_api(data)

    def close_issue(self, iid: str) -> Issue:
        return self._set_state(iid, "closed")

    def reopen_issue(self, iid: str) -> Issue:
        return self._set_state(iid, "open")

    def _set_state(self, iid: str, state: str) -> Issue:
        data = gh_api(f"repos/{self._repo}/issues/{iid}", method="PATCH", input_json={"state": state})
        if not isinstance(data, dict):
            raise RuntimeError(f"failed to set issue {iid} state to {state} in {self._repo}")
        return self._issue_from_api(data)

    def list_issues(
        self,
        *,
        search: str | None = None,
        assignee: str | None = None,
        labels: list[str] | None = None,
        state: str = "opened",
    ) -> list[Issue]:
        query = [f"state={_STATE_TO_GITHUB.get(state, state)}"]
        if assignee:
            query.append(f"assignee={quote(assignee, safe='')}")
        if labels:
            query.append(f"labels={','.join(quote(name, safe='') for name in labels)}")
        raw = gh_api_paginated(f"repos/{self._repo}/issues?{'&'.join(query)}")
        issues = [self._issue_from_api(item) for item in raw if "pull_request" not in item]
        if search:
            needle = search.lower()
            issues = [i for i in issues if needle in i.title.lower() or needle in i.description.lower()]
        return issues

    def add_note(self, iid: str, body: str) -> None:
        gh_api(f"repos/{self._repo}/issues/{iid}/comments", method="POST", input_json={"body": body})

    def ensure_owner_label(self, name: str, *, color: str = "", description: str = "") -> Label:
        self.require(Capability.OWNER_LABELS)
        for label in gh_api_paginated(f"repos/{self._repo}/labels"):
            if label.get("name") == name:
                return Label(
                    name=name,
                    color=label.get("color", "") or "",
                    description=label.get("description", "") or "",
                )
        body: dict[str, Any] = {"name": name}
        if color:
            body["color"] = color.lstrip("#")
        if description:
            body["description"] = description
        gh_api(f"repos/{self._repo}/labels", method="POST", input_json=body)
        return Label(name=name, color=color, description=description)

    def list_open_epics(self) -> list[Epic]:
        raise UnsupportedCapability(self.platform, Capability.EPICS)

    def get_epic(self, iid: str) -> Epic:
        raise UnsupportedCapability(self.platform, Capability.EPICS)

    def create_epic(self, *, title: str, description: str = "", labels: list[str] | None = None) -> Epic:
        raise UnsupportedCapability(self.platform, Capability.EPICS)

    def update_epic(
        self,
        iid: str,
        *,
        title: str | None = None,
        description: str | None = None,
        add_labels: list[str] | None = None,
        remove_labels: list[str] | None = None,
    ) -> Epic:
        raise UnsupportedCapability(self.platform, Capability.EPICS)

    def attach_to_epic(self, issue_iid: str, epic_iid: str, *, project: str | None = None) -> None:
        raise UnsupportedCapability(self.platform, Capability.EPICS)
