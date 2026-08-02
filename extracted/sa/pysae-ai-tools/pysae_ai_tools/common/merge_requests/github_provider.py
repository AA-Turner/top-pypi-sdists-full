"""GitHub implementation of :class:`MergeRequestProvider`.

Pull-request operations wired to the GitHub REST API through the shared ``gh``
runner (``common/github``), with GraphQL for the one thing REST cannot express
(toggling a PR's draft state). GitHub has no server-side rebase endpoint, so the
``REBASE`` capability is unsupported. ``APPROVALS`` is declared, but note GitHub
forbids approving one's own PR (``422``) — a product rule with no override,
unlike GitLab; :meth:`approve` still issues the request and lets the caller see
the host's refusal.
"""

from typing import Any, ClassVar

from ..github.runner import gh_api, gh_api_paginated, gh_graphql
from ..issue_tracking.context import RepoContext
from ..issue_tracking.platform import Platform
from .models import MergeRequest, Note
from .provider import Capability, MergeRequestProvider, UnsupportedCapability

_STATE_TO_GITHUB = {"opened": "open", "closed": "closed", "all": "all"}

_READY_MUTATION = (
    "mutation($id: ID!) { markPullRequestReadyForReview(input: {pullRequestId: $id}) { clientMutationId } }"
)
_DRAFT_MUTATION = "mutation($id: ID!) { convertPullRequestToDraft(input: {pullRequestId: $id}) { clientMutationId } }"


class GithubMergeRequestProvider(MergeRequestProvider):
    """Pull-request operations backed by the GitHub REST/GraphQL APIs via ``gh``."""

    platform: ClassVar[Platform] = Platform.GITHUB
    capabilities: ClassVar[frozenset[Capability]] = frozenset({Capability.APPROVALS})

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
    def _mr_from_api(cls, data: dict[str, Any]) -> MergeRequest:
        return MergeRequest(
            iid=str(data.get("number", "") or ""),
            title=data.get("title", "") or "",
            description=data.get("body") or "",
            web_url=data.get("html_url", "") or "",
            state=data.get("state", "") or "",
            source_branch=(data.get("head") or {}).get("ref", "") or "",
            target_branch=(data.get("base") or {}).get("ref", "") or "",
            labels=cls._label_names(data.get("labels")),
            assignees=[a.get("login", "") for a in data.get("assignees", []) or []],
            reviewers=[r.get("login", "") for r in data.get("requested_reviewers", []) or []],
            author=(data.get("user") or {}).get("login", "") or "",
            draft=bool(data.get("draft", False)),
            merge_status=str(data.get("mergeable_state") or ""),
            merge_commit_sha=str(data.get("merge_commit_sha") or ""),
        )

    def current_user(self) -> str:
        data = gh_api("user")
        return data.get("login", "") if isinstance(data, dict) else ""

    def get_mr(self, iid: str) -> MergeRequest:
        data = gh_api(f"repos/{self._repo}/pulls/{iid}")
        if not isinstance(data, dict):
            raise LookupError(f"pull request {iid} not found in {self._repo}")
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
        # remove_source_branch is a GitLab create-time field; GitHub deletes merged
        # branches via a repo-level setting, so the flag is accepted and ignored here.
        body: dict[str, Any] = {
            "title": title,
            "body": description,
            "head": source_branch,
            "base": target_branch,
            "draft": draft,
        }
        data = gh_api(f"repos/{self._repo}/pulls", method="POST", input_json=body, check=True)
        if not isinstance(data, dict):
            raise RuntimeError(f"unexpected response creating pull request in {self._repo}")
        number = str(data.get("number", "") or "")
        # Labels and assignees live on the shared issues endpoint, not the PR one.
        if labels:
            gh_api(f"repos/{self._repo}/issues/{number}/labels", method="POST", input_json={"labels": labels})
        if assignees:
            gh_api(f"repos/{self._repo}/issues/{number}/assignees", method="POST", input_json={"assignees": assignees})
        return self.get_mr(number) if (labels or assignees) else self._mr_from_api(data)

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
        body: dict[str, Any] = {}
        if title is not None:
            body["title"] = title
        if description is not None:
            body["body"] = description
        if body:
            gh_api(f"repos/{self._repo}/pulls/{iid}", method="PATCH", input_json=body)
        if add_labels or remove_labels:
            self._recompose_labels(iid, add_labels or [], remove_labels or [])
        if draft is not None:
            self._set_draft(iid, draft)
        return self.get_mr(iid)

    def list_mrs(
        self,
        *,
        search: str | None = None,
        author: str | None = None,
        assignee: str | None = None,
        labels: list[str] | None = None,
        state: str = "opened",
    ) -> list[MergeRequest]:
        # GitHub's pulls endpoint only knows open/closed/all; a merged PR is a
        # closed one with a merged_at timestamp, so "merged" queries closed + filters.
        gh_state = "closed" if state == "merged" else _STATE_TO_GITHUB.get(state, state)
        raw = gh_api_paginated(f"repos/{self._repo}/pulls?state={gh_state}")
        if state == "merged":
            raw = [item for item in raw if item.get("merged_at")]
        mrs = [self._mr_from_api(item) for item in raw]
        if author:
            mrs = [m for m in mrs if m.author == author]
        if assignee:
            mrs = [m for m in mrs if assignee in m.assignees]
        if labels:
            wanted = set(labels)
            mrs = [m for m in mrs if wanted.issubset(set(m.labels))]
        if search:
            needle = search.lower()
            mrs = [m for m in mrs if needle in m.title.lower() or needle in m.description.lower()]
        return mrs

    def add_note(self, iid: str, body: str) -> None:
        gh_api(f"repos/{self._repo}/issues/{iid}/comments", method="POST", input_json={"body": body})

    def list_notes(self, iid: str) -> list[Note]:
        # A PR's conversation comments live on the shared issues endpoint.
        comments = gh_api_paginated(f"repos/{self._repo}/issues/{iid}/comments")
        return [
            Note(
                id=str(c.get("id", "") or ""),
                body=c.get("body", "") or "",
                author=(c.get("user") or {}).get("login", "") or "",
            )
            for c in comments
        ]

    def update_note(self, iid: str, note_id: str, body: str) -> None:
        gh_api(f"repos/{self._repo}/issues/comments/{note_id}", method="PATCH", input_json={"body": body})

    def set_reviewers(self, iid: str, usernames: list[str]) -> None:
        if usernames:
            gh_api(
                f"repos/{self._repo}/pulls/{iid}/requested_reviewers",
                method="POST",
                input_json={"reviewers": usernames},
            )

    def merge(self, iid: str) -> MergeRequest:
        data = gh_api(f"repos/{self._repo}/pulls/{iid}/merge", method="PUT", input_json={})
        if not isinstance(data, dict) or not data.get("merged"):
            raise RuntimeError(f"failed to merge pull request {iid} in {self._repo}")
        merged = self.get_mr(iid)
        merged.merge_commit_sha = str(data.get("sha") or merged.merge_commit_sha)
        return merged

    def approve(self, iid: str) -> None:
        self.require(Capability.APPROVALS)
        gh_api(f"repos/{self._repo}/pulls/{iid}/reviews", method="POST", input_json={"event": "APPROVE"})

    def approvals_count(self, iid: str) -> int:
        self.require(Capability.APPROVALS)
        reviews = gh_api_paginated(f"repos/{self._repo}/pulls/{iid}/reviews")
        return len({r.get("user", {}).get("login") for r in reviews if r.get("state") == "APPROVED"})

    def rebase(self, iid: str) -> None:
        raise UnsupportedCapability(self.platform, Capability.REBASE)

    def _recompose_labels(self, iid: str, add: list[str], remove: list[str]) -> None:
        current = self.get_mr(iid).labels
        removed = set(remove)
        names = [name for name in current if name not in removed]
        for name in add:
            if name not in names:
                names.append(name)
        gh_api(f"repos/{self._repo}/issues/{iid}/labels", method="PUT", input_json={"labels": names})

    def _set_draft(self, iid: str, draft: bool) -> None:
        # REST cannot toggle draft; the PR's GraphQL node ID drives the mutation.
        data = gh_api(f"repos/{self._repo}/pulls/{iid}")
        node_id = data.get("node_id") if isinstance(data, dict) else None
        if not node_id:
            raise RuntimeError(f"cannot resolve node id of pull request {iid} in {self._repo}")
        gh_graphql(_DRAFT_MUTATION if draft else _READY_MUTATION, variables={"id": str(node_id)})
