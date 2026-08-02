"""GitLab implementation of :class:`IssueTrackingProvider`.

Preserves the current behaviour by delegating to the single ``glab`` runner
(``common/glab``) and the same REST endpoints the standalone commands use, so
routing an operation through this provider is byte-for-byte what happens today.
"""

from typing import Any, ClassVar
from urllib.parse import quote

from ..glab.runner import glab_api, glab_api_paginated
from ..group import ensure_group_namespace, resolve_group_id
from .context import RepoContext
from .models import Epic, Issue, Label
from .platform import Platform
from .provider import Capability, IssueTrackingProvider


class GitlabIssueTrackingProvider(IssueTrackingProvider):
    """Issue/epic/label operations backed by the GitLab REST API via ``glab``."""

    platform: ClassVar[Platform] = Platform.GITLAB
    capabilities: ClassVar[frozenset[Capability]] = frozenset({Capability.EPICS, Capability.OWNER_LABELS})

    def __init__(self, ctx: RepoContext) -> None:
        self.ctx = ctx

    @property
    def _project(self) -> str:
        return quote(self.ctx.project, safe="")

    def _group_id(self) -> int:
        return resolve_group_id(self.ctx.owner or None)

    def _label_scope(self) -> str:
        """API scope for owner labels: the group when the owner is one, else the project.

        A personal (user-namespace) repo has no group, so group labels can't exist —
        fall back to project-level labels (like the GitHub provider does per-repo).
        """
        try:
            return f"groups/{self._group_id()}"
        except RuntimeError:
            return f"projects/{self._project}"

    @staticmethod
    def _epic_from_api(data: dict[str, Any]) -> Epic:
        return Epic(
            iid=str(data.get("iid", "") or ""),
            title=data.get("title", "") or "",
            description=data.get("description") or "",
            web_url=data.get("web_url", "") or "",
            labels=list(data.get("labels", []) or []),
        )

    @staticmethod
    def _issue_from_api(data: dict[str, Any]) -> Issue:
        return Issue(
            iid=str(data.get("iid", "") or ""),
            title=data.get("title", "") or "",
            description=data.get("description") or "",
            web_url=data.get("web_url", "") or "",
            state=data.get("state", "") or "",
            labels=list(data.get("labels", []) or []),
            assignees=[a.get("username", "") for a in data.get("assignees", []) or []],
            author=(data.get("author") or {}).get("username", "") or "",
            weight=data.get("weight"),
        )

    def current_user(self) -> str:
        data = glab_api("user")
        return (data or {}).get("username", "") if isinstance(data, dict) else ""

    def get_issue(self, iid: str) -> Issue:
        data = glab_api(f"projects/{self._project}/issues/{iid}")
        if not isinstance(data, dict):
            raise LookupError(f"issue {iid} not found in {self.ctx.project}")
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
        fields = [f"title={title}", f"description={description}"]
        if labels:
            fields.append(f"labels={','.join(labels)}")
        if weight is not None:
            fields.append(f"weight={weight}")
        ids = self._assignee_ids(assignees)
        if ids:
            fields.append(f"assignee_ids={','.join(str(i) for i in ids)}")
        data = glab_api(f"projects/{self._project}/issues", method="POST", fields=fields)
        if not isinstance(data, dict):
            raise RuntimeError(f"failed to create issue in {self.ctx.project}")
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
        fields: list[str] = []
        if title is not None:
            fields.append(f"title={title}")
        if description is not None:
            fields.append(f"description={description}")
        if add_labels:
            fields.append(f"add_labels={','.join(add_labels)}")
        if remove_labels:
            fields.append(f"remove_labels={','.join(remove_labels)}")
        data = glab_api(f"projects/{self._project}/issues/{iid}", method="PUT", fields=fields)
        if not isinstance(data, dict):
            raise RuntimeError(f"failed to update issue {iid} in {self.ctx.project}")
        return self._issue_from_api(data)

    def close_issue(self, iid: str) -> Issue:
        return self._set_state(iid, "close")

    def reopen_issue(self, iid: str) -> Issue:
        return self._set_state(iid, "reopen")

    def _set_state(self, iid: str, state_event: str) -> Issue:
        data = glab_api(f"projects/{self._project}/issues/{iid}", method="PUT", fields=[f"state_event={state_event}"])
        if not isinstance(data, dict):
            raise RuntimeError(f"failed to {state_event} issue {iid} in {self.ctx.project}")
        return self._issue_from_api(data)

    def list_issues(
        self,
        *,
        search: str | None = None,
        assignee: str | None = None,
        labels: list[str] | None = None,
        state: str = "opened",
    ) -> list[Issue]:
        query = [f"state={state}"] if state else []
        if search:
            query.append(f"search={quote(search, safe='')}")
        if assignee:
            query.append(f"assignee_username={quote(assignee, safe='')}")
        if labels:
            query.append(f"labels={quote(','.join(labels), safe='')}")
        suffix = f"?{'&'.join(query)}" if query else ""
        return [self._issue_from_api(d) for d in glab_api_paginated(f"projects/{self._project}/issues{suffix}")]

    def add_note(self, iid: str, body: str) -> None:
        glab_api(f"projects/{self._project}/issues/{iid}/notes", method="POST", fields=[f"body={body}"])

    def ensure_owner_label(self, name: str, *, color: str = "", description: str = "") -> Label:
        self.require(Capability.OWNER_LABELS)
        scope = self._label_scope()
        for label in glab_api_paginated(f"{scope}/labels"):
            if label.get("name") == name:
                return Label(
                    name=name,
                    color=label.get("color", "") or "",
                    description=label.get("description", "") or "",
                )
        fields = [f"name={name}"]
        if color:
            fields.append(f"color={color}")
        if description:
            fields.append(f"description={description}")
        glab_api(f"{scope}/labels", method="POST", fields=fields)
        return Label(name=name, color=color, description=description)

    def list_open_epics(self) -> list[Epic]:
        self.require(Capability.EPICS)
        gid = self._group_id()
        return [self._epic_from_api(e) for e in glab_api_paginated(f"groups/{gid}/epics?state=opened")]

    def get_epic(self, iid: str) -> Epic:
        self.require(Capability.EPICS)
        data = glab_api(f"groups/{self._group_id()}/epics/{iid}")
        if not isinstance(data, dict):
            raise LookupError(f"epic {iid} not found under {self.ctx.owner}")
        return self._epic_from_api(data)

    def create_epic(self, *, title: str, description: str = "", labels: list[str] | None = None) -> Epic:
        self.require(Capability.EPICS)
        gid = self._group_id()
        fields = [f"title={title}"]
        if description:
            fields.append(f"description={description}")
        if labels:
            fields.append(f"labels={','.join(labels)}")
        data = glab_api(f"groups/{gid}/epics", method="POST", fields=fields)
        if not isinstance(data, dict):
            raise RuntimeError("failed to create epic")
        return self._epic_from_api(data)

    def update_epic(
        self,
        iid: str,
        *,
        title: str | None = None,
        description: str | None = None,
        add_labels: list[str] | None = None,
        remove_labels: list[str] | None = None,
    ) -> Epic:
        self.require(Capability.EPICS)
        gid = self._group_id()
        fields: list[str] = []
        if title is not None:
            fields.append(f"title={title}")
        if description is not None:
            fields.append(f"description={description}")
        if add_labels:
            fields.append(f"add_labels={','.join(add_labels)}")
        if remove_labels:
            fields.append(f"remove_labels={','.join(remove_labels)}")
        data = glab_api(f"groups/{gid}/epics/{iid}", method="PUT", fields=fields)
        if not isinstance(data, dict):
            raise RuntimeError(f"failed to update epic {iid}")
        return self._epic_from_api(data)

    def attach_to_epic(self, issue_iid: str, epic_iid: str, *, project: str | None = None) -> None:
        self.require(Capability.EPICS)
        target = self.ctx.project
        if project:
            target = project if "/" in project else ensure_group_namespace(project, self.ctx.owner or None)
        enc_project = quote(target, safe="")
        issue = glab_api(f"projects/{enc_project}/issues/{issue_iid}")
        if not isinstance(issue, dict) or "id" not in issue:
            raise LookupError(f"cannot resolve global id of issue {issue_iid} in {target}")
        global_id = issue["id"]
        gid = self._group_id()
        glab_api(f"groups/{gid}/epics/{epic_iid}/issues/{global_id}", method="POST")

    def _assignee_ids(self, usernames: list[str]) -> list[int]:
        ids: list[int] = []
        for username in usernames:
            if not username:
                continue
            data = glab_api(f"users?username={quote(username, safe='')}")
            if isinstance(data, list) and data and isinstance(data[0], dict) and "id" in data[0]:
                ids.append(int(data[0]["id"]))
        return ids
