"""Provider-neutral data models for the merge-request abstraction.

The single :class:`MergeRequest` model is the GitLab MR / GitHub PR seen through
a host-agnostic lens. It carries only the fields the MR commands and skills
consume; each provider maps its host payload onto them so consumers never see a
GitLab- or GitHub-shaped object.

``merge_status`` is the one deliberately host-shaped field: it passes the host's
own mergeability vocabulary through verbatim (GitLab ``detailed_merge_status`` /
GitHub ``mergeable_state``). The GitLab merge dispatch loop needs those exact
tokens, so the model relays them rather than flattening them to a lossy neutral
enum.
"""

from dataclasses import dataclass, field


@dataclass
class MergeRequest:
    """A merge request / pull request, as exposed by any provider."""

    iid: str = ""
    title: str = ""
    description: str = ""
    web_url: str = ""
    state: str = ""
    source_branch: str = ""
    target_branch: str = ""
    labels: list[str] = field(default_factory=list)
    assignees: list[str] = field(default_factory=list)
    reviewers: list[str] = field(default_factory=list)
    author: str = ""
    draft: bool = False
    merge_status: str = ""
    merge_commit_sha: str = ""


@dataclass
class Note:
    """A comment on a merge request."""

    id: str = ""
    body: str = ""
    author: str = ""
