"""GitLab implementation of :class:`MergeRequestProvider`.

Delegates to the single ``glab`` runner (``common/glab``) and the same REST
endpoints the standalone MR commands use, so routing an operation through this
provider is byte-for-byte what happens today. GitLab supports both gated
capabilities: server-side approvals and rebase.
"""

from typing import Any, ClassVar
from urllib.parse import quote

from ..glab.runner import glab_api, glab_api_paginated
from ..issue_tracking.context import RepoContext
from ..issue_tracking.platform import Platform
from .models import MergeRequest, Note
from .provider import Capability, MergeRequestProvider

_DRAFT_PREFIX = "Draft: "


class GitlabMergeRequestProvider(MergeRequestProvider):
    """Merge-request operations backed by the GitLab REST API via ``glab``."""

    platform: ClassVar[Platform] = Platform.GITLAB
    capabilities: ClassVar[frozenset[Capability]] = frozenset({Capability.APPROVALS, Capability.REBASE})

    def __init__(self, ctx: RepoContext) -> None:
        self.ctx = ctx

    @property
    def _project(self) -> str:
        return quote(self.ctx.project, safe="")

    @staticmethod
    def _mr_from_api(data: dict[str, Any]) -> MergeRequest:
        return MergeRequest(
            iid=str(data.get("iid", "") or ""),
            title=data.get("title", "") or "",
            description=data.get("description") or "",
            web_url=data.get("web_url", "") or "",
            state=data.get("state", "") or "",
            source_branch=data.get("source_branch", "") or "",
            target_branch=data.get("target_branch", "") or "",
            labels=list(data.get("labels", []) or []),
            assignees=[a.get("username", "") for a in data.get("assignees", []) or []],
            reviewers=[r.get("username", "") for r in data.get("reviewers", []) or []],
            author=(data.get("author") or {}).get("username", "") or "",
            draft=bool(data.get("draft", data.get("work_in_progress", False))),
            merge_status=str(data.get("detailed_merge_status") or data.get("merge_status") or ""),
            merge_commit_sha=str(data.get("merge_commit_sha") or data.get("squash_commit_sha") or ""),
        )

    def current_user(self) -> str:
        data = glab_api("user")
        return (data or {}).get("username", "") if isinstance(data, dict) else ""

    def get_mr(self, iid: str) -> MergeRequest:
        data = glab_api(f"projects/{self._project}/merge_requests/{iid}")
        if not isinstance(data, dict):
            raise LookupError(f"merge request {iid} not found in {self.ctx.project}")
        return self._mr_from_api(data)

    def create_mr(
        self,
        *,
        title: str,
        description: str,
        source_branch: str,
        target_branch: str,
        labels: list[str],
        assignees: list[str],
        draft: bool = False,
        remove_source_branch: bool = False,
    ) -> MergeRequest:
        # GitLab derives draft state from the title prefix at creation time
        # (the create API has no draft boolean; the update API does — see update_mr).
        mr_title = f"{_DRAFT_PREFIX}{title}" if draft and not title.startswith(_DRAFT_PREFIX) else title
        fields = [
            f"source_branch={source_branch}",
            f"target_branch={target_branch}",
            f"title={mr_title}",
            f"description={description}",
        ]
        if labels:
            fields.append(f"labels={','.join(labels)}")
        if remove_source_branch:
            fields.append("remove_source_branch=true")
        ids = self._assignee_ids(assignees)
        if ids:
            fields.append(f"assignee_ids={','.join(str(i) for i in ids)}")
        data = glab_api(f"projects/{self._project}/merge_requests", method="POST", fields=fields)
        if not isinstance(data, dict):
            raise RuntimeError(f"failed to create merge request in {self.ctx.project}")
        return self._mr_from_api(data)

    def update_mr(
        self,
        iid: str,
        *,
        title: str | None = None,
        description: str | None = None,
        add_labels: list[str] | None = None,
        remove_labels: list[str] | None = None,
        draft: bool | None = None,
    ) -> MergeRequest:
        fields: list[str] = []
        if title is not None:
            fields.append(f"title={title}")
        if description is not None:
            fields.append(f"description={description}")
        if add_labels:
            fields.append(f"add_labels={','.join(add_labels)}")
        if remove_labels:
            fields.append(f"remove_labels={','.join(remove_labels)}")
        if draft is not None:
            fields.append(f"draft={'true' if draft else 'false'}")
        data = glab_api(f"projects/{self._project}/merge_requests/{iid}", method="PUT", fields=fields)
        if not isinstance(data, dict):
            raise RuntimeError(f"failed to update merge request {iid} in {self.ctx.project}")
        return self._mr_from_api(data)

    def list_mrs(
        self,
        *,
        search: str | None = None,
        author: str | None = None,
        assignee: str | None = None,
        labels: list[str] | None = None,
        state: str = "opened",
    ) -> list[MergeRequest]:
        query = [f"state={state}"] if state else []
        if search:
            query.append(f"search={quote(search, safe='')}")
        if author:
            query.append(f"author_username={quote(author, safe='')}")
        if assignee:
            query.append(f"assignee_username={quote(assignee, safe='')}")
        if labels:
            query.append(f"labels={quote(','.join(labels), safe='')}")
        suffix = f"?{'&'.join(query)}" if query else ""
        return [self._mr_from_api(d) for d in glab_api_paginated(f"projects/{self._project}/merge_requests{suffix}")]

    def add_note(self, iid: str, body: str) -> None:
        glab_api(f"projects/{self._project}/merge_requests/{iid}/notes", method="POST", fields=[f"body={body}"])

    def list_notes(self, iid: str) -> list[Note]:
        notes = glab_api_paginated(f"projects/{self._project}/merge_requests/{iid}/notes")
        return [
            Note(
                id=str(n.get("id", "") or ""),
                body=n.get("body", "") or "",
                author=(n.get("author") or {}).get("username", "") or "",
            )
            for n in notes
        ]

    def update_note(self, iid: str, note_id: str, body: str) -> None:
        glab_api(
            f"projects/{self._project}/merge_requests/{iid}/notes/{note_id}",
            method="PUT",
            fields=[f"body={body}"],
        )

    def set_reviewers(self, iid: str, usernames: list[str]) -> None:
        ids = self._assignee_ids(usernames)
        fields = [f"reviewer_ids={','.join(str(i) for i in ids)}"] if ids else ["reviewer_ids="]
        glab_api(f"projects/{self._project}/merge_requests/{iid}", method="PUT", fields=fields)

    def merge(self, iid: str) -> MergeRequest:
        # No body — let GitLab apply its project-level defaults (squash_option,
        # remove_source_branch_after_merge, …). The high-level `glab mr merge` is
        # avoided on purpose: it injects body fields the server rejects with 405.
        data = glab_api(f"projects/{self._project}/merge_requests/{iid}/merge", method="PUT")
        if not isinstance(data, dict):
            raise RuntimeError(f"failed to merge merge request {iid} in {self.ctx.project}")
        return self._mr_from_api(data)

    def approve(self, iid: str) -> None:
        self.require(Capability.APPROVALS)
        glab_api(f"projects/{self._project}/merge_requests/{iid}/approve", method="POST")

    def approvals_count(self, iid: str) -> int:
        self.require(Capability.APPROVALS)
        data = glab_api(f"projects/{self._project}/merge_requests/{iid}/approvals")
        approved_by = data.get("approved_by", []) if isinstance(data, dict) else []
        return len(approved_by or [])

    def rebase(self, iid: str) -> None:
        self.require(Capability.REBASE)
        glab_api(f"projects/{self._project}/merge_requests/{iid}/rebase", method="PUT")

    def _assignee_ids(self, usernames: list[str]) -> list[int]:
        ids: list[int] = []
        for username in usernames:
            if not username:
                continue
            data = glab_api(f"users?username={quote(username, safe='')}")
            if isinstance(data, list) and data and isinstance(data[0], dict) and "id" in data[0]:
                ids.append(int(data[0]["id"]))
        return ids
