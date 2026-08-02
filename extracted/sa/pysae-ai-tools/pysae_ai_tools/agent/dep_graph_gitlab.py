"""GitLab-backed fetchers for the dependency graph (issue links + merged check).

The pure graph logic lives in :mod:`pysae_ai_tools.agent.dep_graph`; these are the live
``glab``-backed callables it takes, shared by ``agent dep-graph`` and the headless pipeline.
"""

from typing import Any
from urllib.parse import quote

from ..common.glab.runner import glab_api
from .dep_graph import LinkedIssue


def _glab_json(path: str) -> Any:
    return glab_api(path)


def fetch_links(candidate_ref: str) -> list[LinkedIssue]:
    """The issue links of one candidate (``project_path#iid``); empty on any glab failure."""
    project_path, _, iid = candidate_ref.rpartition("#")
    data = _glab_json(f"projects/{quote(project_path, safe='')}/issues/{iid}/links")
    if not isinstance(data, list):
        return []
    links: list[LinkedIssue] = []
    for item in data:
        if not isinstance(item, dict):
            continue
        full = (item.get("references") or {}).get("full")
        link_type = item.get("link_type")
        if not full or not link_type:
            continue
        links.append(LinkedIssue(ref=str(full), link_type=str(link_type), state=str(item.get("state", ""))))
    return links


def _has_merged_mr(project_path: str, iid: str) -> bool:
    data = _glab_json(f"projects/{quote(project_path, safe='')}/issues/{iid}/related_merge_requests")
    return isinstance(data, list) and any(isinstance(mr, dict) and mr.get("state") == "merged" for mr in data)


def is_satisfied(blocker_ref: str, state: str) -> bool:
    """An external blocker is satisfied when it is closed or has a merged MR (merged to main)."""
    if state == "closed":
        return True
    project_path, _, iid = blocker_ref.rpartition("#")
    return _has_merged_mr(project_path, iid)
