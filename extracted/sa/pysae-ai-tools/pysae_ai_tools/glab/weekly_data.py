"""Collect weekly engineering data from GitLab for the Pysae group.

Used by the ``stats-weekly-summary`` skill — replaces the previous shell
script. Output: a JSON object with ``merged_mrs``, ``closed_issues``,
``deploys``, and ``epics`` keys.
"""

import datetime as dt
import json
import sys
import time
from typing import Annotated, Any

import typer

from ..common.glab.fetch_issues import glab_api_paginated, run_glab
from ..common.group import resolve_group_id


def _default_since() -> str:
    """ISO-8601 timestamp for 7 days ago at midnight UTC."""
    seven_days_ago = dt.datetime.now(dt.UTC) - dt.timedelta(days=7)
    return seven_days_ago.strftime("%Y-%m-%dT00:00:00Z")


def _normalize_since(value: str) -> str:
    """Accept either a YYYY-MM-DD date or a full ISO-8601 string."""
    if "T" in value:
        return value
    return f"{value}T00:00:00Z"


def _collect_merged_mrs(group_id: int, since: str) -> list[dict[str, Any]]:
    print("  Fetching merged MRs...", file=sys.stderr)
    raw = glab_api_paginated(
        f"groups/{group_id}/merge_requests?state=merged&updated_after={since}&order_by=merged_at&sort=desc",
    )
    out: list[dict[str, Any]] = []
    for mr in raw:
        merged_at = mr.get("merged_at")
        if not merged_at or merged_at < since:
            continue
        full_ref = (mr.get("references") or {}).get("full") or ""
        project = full_ref.split("!", 1)[0] if "!" in full_ref else full_ref
        author = (mr.get("author") or {}).get("username") or ""
        out.append(
            {
                "title": mr.get("title", ""),
                "web_url": mr.get("web_url", ""),
                "author": author,
                "project": project,
                "labels": mr.get("labels", []),
                "merged_at": merged_at,
                "source_branch": mr.get("source_branch", ""),
            }
        )
    print(f"  → {len(out)} MRs", file=sys.stderr)
    return out


def _collect_closed_issues(group_id: int, since: str) -> list[dict[str, Any]]:
    print("  Fetching closed issues...", file=sys.stderr)
    raw = glab_api_paginated(
        f"groups/{group_id}/issues?state=closed&updated_after={since}&order_by=updated_at&sort=desc",
    )
    out: list[dict[str, Any]] = []
    for issue in raw:
        closed_at = issue.get("closed_at")
        if not closed_at or closed_at < since:
            continue
        full_ref = (issue.get("references") or {}).get("full") or ""
        project = full_ref.split("#", 1)[0] if "#" in full_ref else full_ref
        milestone = (issue.get("milestone") or {}).get("title") if issue.get("milestone") else None
        out.append(
            {
                "title": issue.get("title", ""),
                "web_url": issue.get("web_url", ""),
                "iid": issue.get("iid"),
                "project": project,
                "labels": issue.get("labels", []),
                "closed_at": closed_at,
                "weight": issue.get("weight"),
                "milestone": milestone,
            }
        )
    print(f"  → {len(out)} issues", file=sys.stderr)
    return out


def _collect_prod_deploys(group_id: int, since: str, repo_filter: str) -> list[dict[str, Any]]:
    print("  Fetching prod deploys...", file=sys.stderr)
    projects_raw = run_glab("api", f"groups/{group_id}/projects?per_page=100&simple=true", allow_fail=True)
    projects = json.loads(projects_raw) if projects_raw else []

    deploys: list[dict[str, Any]] = []
    for project in projects:
        name = project.get("path", "")
        if repo_filter and name != repo_filter:
            continue
        pid = project.get("id")
        if pid is None:
            continue

        envs_raw = run_glab("api", f"projects/{pid}/environments?per_page=50", allow_fail=True)
        envs = json.loads(envs_raw) if envs_raw else []
        prod_envs = [e["name"] for e in envs if e.get("name", "").endswith("-prod")]
        for env in prod_envs:
            endpoint = (
                f"projects/{pid}/deployments?environment={env}"
                f"&updated_after={since}&status=success&per_page=10"
                "&order_by=updated_at&sort=desc"
            )
            d_raw = run_glab("api", endpoint, allow_fail=True)
            try:
                deploy_list = json.loads(d_raw) if d_raw else []
            except json.JSONDecodeError:
                deploy_list = []
            for deploy in deploy_list:
                updated_at = deploy.get("updated_at")
                if not updated_at or updated_at < since:
                    continue
                sha = deploy.get("sha", "")
                deployer = (deploy.get("user") or {}).get("username") or ""
                deploys.append(
                    {
                        "project": name,
                        "ref": deploy.get("ref", ""),
                        "sha": sha[:8],
                        "deployed_at": updated_at,
                        "deployer": deployer,
                    }
                )
        time.sleep(0.2)

    # Dedupe by (sha, deployer) — same as the original shell script.
    seen: set[tuple[str, str]] = set()
    deduped: list[dict[str, Any]] = []
    for d in deploys:
        key = (d["sha"], d["deployer"])
        if key in seen:
            continue
        seen.add(key)
        deduped.append(d)

    print(f"  → {len(deduped)} deploys", file=sys.stderr)
    return deduped


def _collect_epics_with_activity(group_id: int, since: str) -> list[dict[str, Any]]:
    print("  Fetching epics...", file=sys.stderr)
    epics_raw = run_glab("api", f"groups/{group_id}/epics?state=opened&per_page=100", allow_fail=True)
    epics = json.loads(epics_raw) if epics_raw else []

    out: list[dict[str, Any]] = []
    for epic in epics:
        iid = epic.get("iid")
        if iid is None:
            continue
        issues_raw = run_glab("api", f"groups/{group_id}/epics/{iid}/issues?per_page=100", allow_fail=True)
        try:
            all_issues = json.loads(issues_raw) if issues_raw else []
        except json.JSONDecodeError:
            all_issues = []

        closed_this_week = [i for i in all_issues if i.get("state") == "closed" and (i.get("closed_at") or "") >= since]
        if not closed_this_week:
            continue

        total = len(all_issues)
        closed_total = sum(1 for i in all_issues if i.get("state") == "closed")
        out.append(
            {
                "iid": iid,
                "title": epic.get("title", ""),
                "web_url": epic.get("web_url", ""),
                "description": epic.get("description", ""),
                "total": total,
                "closed_total": closed_total,
                "closed_this_week": len(closed_this_week),
                "closed_issues": closed_this_week,
            }
        )
        time.sleep(0.2)

    print(f"  → {len(out)} epics with activity", file=sys.stderr)
    return out


def main(
    since: Annotated[
        str | None,
        typer.Option("--since", help="Cutoff date (YYYY-MM-DD or ISO-8601). Defaults to 7 days ago."),
    ] = None,
    group_id: Annotated[
        int | None,
        typer.Option("--group-id", help="GitLab group ID (default: resolved live from the group path)."),
    ] = None,
    repo: Annotated[
        str,
        typer.Option("--repo", help="Restrict deploys to a single repo (path)."),
    ] = "",
) -> None:
    """Collect weekly engineering data and emit JSON on stdout."""
    if group_id is None:
        try:
            group_id = resolve_group_id()
        except RuntimeError as exc:
            print(f"✗ {exc}", file=sys.stderr)
            raise typer.Exit(code=1) from None
    since_iso = _normalize_since(since) if since else _default_since()
    print(f"Collecting data since {since_iso} for group {group_id}...", file=sys.stderr)

    payload = {
        "metadata": {
            "since": since_iso,
            "group_id": str(group_id),
            "collected_at": dt.datetime.now(dt.UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        },
        "merged_mrs": _collect_merged_mrs(group_id, since_iso),
        "closed_issues": _collect_closed_issues(group_id, since_iso),
        "deploys": _collect_prod_deploys(group_id, since_iso, repo),
        "epics": _collect_epics_with_activity(group_id, since_iso),
    }

    json.dump(payload, sys.stdout, ensure_ascii=False)
    sys.stdout.write("\n")


if __name__ == "__main__":
    typer.run(main)
