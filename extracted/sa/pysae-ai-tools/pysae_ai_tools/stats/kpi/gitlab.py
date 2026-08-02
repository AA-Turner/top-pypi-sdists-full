"""GitLab collectors: velocity (issues, weight, lead time) and team metrics
(cycle time, change failure rate, deploy frequency, test coverage).

Definitions follow the sheet literally (see ``kpi-definitions.md``):
lead time = issue ``created_at → closed_at``, cycle time = MR
``created_at → merged_at``. Windows are ``[since, until)`` ISO timestamps.
"""

import datetime as dt
import json
import sys
import time
from typing import Any

from ...common.glab.fetch_issues import glab_api_paginated, run_glab

BOT_AUTHOR_MARKERS = ("bot", "renovate", "dependabot")


def _parse_dt(value: str) -> dt.datetime:
    return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))


def _days_between(start: str, end: str) -> float:
    return (_parse_dt(end) - _parse_dt(start)).total_seconds() / 86400


def _is_bot(username: str) -> bool:
    name = username.lower()
    return any(marker in name for marker in BOT_AUTHOR_MARKERS)


def is_revert(mr_title: str) -> bool:
    return mr_title.lower().startswith("revert")


def _paginated(endpoint: str) -> list[dict[str, Any]]:
    """``glab_api_paginated`` with ``SystemExit`` converted for best-effort callers.

    ``run_glab`` exits the process on glab failure — a single transient API
    error must cost one metric, not the whole snapshot.
    """
    try:
        return glab_api_paginated(endpoint)
    except SystemExit as exc:
        raise RuntimeError(f"glab api failed on {endpoint.split('?')[0]}") from exc


def closed_issues(group_id: int, since: str, until: str) -> list[dict[str, Any]]:
    raw = _paginated(f"groups/{group_id}/issues?state=closed&updated_after={since}&order_by=updated_at&sort=desc")
    return [i for i in raw if i.get("closed_at") and since <= i["closed_at"] < until]


def merged_mrs(group_id: int, since: str, until: str) -> list[dict[str, Any]]:
    raw = _paginated(
        f"groups/{group_id}/merge_requests?state=merged&updated_after={since}&order_by=merged_at&sort=desc"
    )
    return [m for m in raw if m.get("merged_at") and since <= m["merged_at"] < until]


def velocity(issues: list[dict[str, Any]]) -> dict[str, Any]:
    """Weight delivered, issues closed, average lead time (days) over closed issues."""
    weights = [i.get("weight") or 0 for i in issues]
    lead_times = [_days_between(i["created_at"], i["closed_at"]) for i in issues if i.get("created_at")]
    return {
        "issues_closed": len(issues),
        "weight_delivered": sum(weights),
        "unweighted_issues": sum(1 for w in weights if not w),
        "lead_time_days": round(sum(lead_times) / len(lead_times), 1) if lead_times else None,
    }


def mr_metrics(mrs: list[dict[str, Any]]) -> dict[str, Any]:
    """Cycle time (days) and change failure rate (% reverts) over merged MRs, bots excluded."""
    human_mrs = [m for m in mrs if not _is_bot((m.get("author") or {}).get("username") or "")]
    cycle_times = [_days_between(m["created_at"], m["merged_at"]) for m in human_mrs if m.get("created_at")]
    reverts = sum(1 for m in human_mrs if is_revert(m.get("title") or ""))
    return {
        "mrs_merged": len(human_mrs),
        "cycle_time_days": round(sum(cycle_times) / len(cycle_times), 1) if cycle_times else None,
        "revert_mrs": reverts,
        "change_failure_rate_pct": round(reverts / len(human_mrs) * 100, 1) if human_mrs else None,
    }


def _group_projects(group_id: int) -> list[dict[str, Any]]:
    raw = run_glab("api", f"groups/{group_id}/projects?per_page=100&simple=true&archived=false", allow_fail=True)
    projects: list[dict[str, Any]] = json.loads(raw) if raw else []
    return projects


def prod_deploy_count(group_id: int, since: str, until: str) -> int:
    """Successful deployments on ``*-prod`` environments, deduped by (sha, environment)."""
    deploys: set[tuple[str, str]] = set()
    for project in _group_projects(group_id):
        pid = project.get("id")
        if pid is None:
            continue
        envs_raw = run_glab("api", f"projects/{pid}/environments?per_page=50", allow_fail=True)
        envs = json.loads(envs_raw) if envs_raw else []
        for env in (e["name"] for e in envs if e.get("name", "").endswith("-prod")):
            endpoint = (
                f"projects/{pid}/deployments?environment={env}&status=success"
                f"&updated_after={since}&per_page=100&order_by=updated_at&sort=desc"
            )
            raw = run_glab("api", endpoint, allow_fail=True)
            try:
                deploy_list = json.loads(raw) if raw else []
            except json.JSONDecodeError:
                deploy_list = []
            for deploy in deploy_list:
                created_at = deploy.get("created_at") or deploy.get("updated_at") or ""
                if since <= created_at < until:
                    deploys.add((deploy.get("sha", ""), env))
        time.sleep(0.2)
    return len(deploys)


def test_coverage_pct(group_id: int) -> dict[str, Any]:
    """Latest default-branch pipeline coverage per project; average over projects exposing one."""
    coverages: dict[str, float] = {}
    for project in _group_projects(group_id):
        pid, name = project.get("id"), project.get("path", "")
        default_branch = project.get("default_branch") or "main"
        if pid is None:
            continue
        raw = run_glab(
            "api",
            f"projects/{pid}/pipelines?ref={default_branch}&status=success&per_page=20",
            allow_fail=True,
        )
        try:
            pipelines = json.loads(raw) if raw else []
        except json.JSONDecodeError:
            pipelines = []
        for pipeline in pipelines:
            pipeline_id = pipeline.get("id")
            detail_raw = run_glab("api", f"projects/{pid}/pipelines/{pipeline_id}", allow_fail=True)
            detail = json.loads(detail_raw) if detail_raw else {}
            coverage = detail.get("coverage")
            if coverage is not None:
                coverages[name] = float(coverage)
                break
        time.sleep(0.2)
    if not coverages:
        raise RuntimeError("no project exposes pipeline coverage (coverage regex not configured?)")
    print(f"  coverage per repo: {coverages}", file=sys.stderr)
    return {
        "average_pct": round(sum(coverages.values()) / len(coverages), 1),
        "per_repo": coverages,
    }
