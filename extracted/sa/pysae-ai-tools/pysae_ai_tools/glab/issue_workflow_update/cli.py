"""``pysae-ai-tools glab issue-workflow-update`` — reconcile ticket board statuses.

Audits open issues and proposes (or applies) these corrections:

- Tickets carrying a cancelled label (``ANNULE``) → closed (highest precedence).
- Tickets with an *open* related MR → bumped to at least ``workflow::In
  progress``, or ``workflow::Under review`` if that open MR is already approved.
- Tickets whose related MRs are all merged **and shipped** → closed.
- Tickets whose related MRs are all merged but **not yet shipped** → bumped to
  at least ``workflow::To deploy``.

**Shipped detection** — "shipped" is decided **per line** from a source→deploy
branch mapping (``.pysae-ai-tools.yaml`` ``board.deploy_branches``, else
``{main: deploy/prod, support/*: deploy/support/*}``), not by the changelog.
Wildcards expand to concrete ``(source, deploy)`` pairs whose deploy branch
exists; for each, one ``compare?from=deploy&to=source`` yields the commits on
that source line not yet on its deploy branch. A merged MR (merged into
``source``) whose merge/squash commit is absent from that set has shipped. This
keeps diverging lines correct (``main``→``deploy/prod``,
``support/5.2.x``→``deploy/support/5.2.x``). No clone, no local git; per-issue
lookups are fanned out across a thread pool. ``To deploy`` is skipped
(``has_deploy: false``) — merged tickets **closed directly** — either when a
project has **no deploy branch at all** (nothing happens after the merge: its CI
deploys from the MR pipeline) or when it opts out of the column via
``.pysae-ai-tools.yaml`` ``board.to_deploy: false``. Same rule as the live
merge path, shared through ``glab/deploy_branches.py``.

Dry-run by default; pass ``--apply`` to perform the changes. Status bumps reuse
``glab workflow-transition`` so other labels (``review::release``,
``version::*`` …) are preserved.
"""

import json
import sys
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from enum import StrEnum
from pathlib import Path
from typing import Annotated, Any

import typer

from ...common.glab.fetch_issues import get_current_username, resolve_username
from ...common.glab.models import GitLabIssue
from ...common.glab.runner import glab_api, glab_api_paginated, run_glab
from ...common.references.gitlab_labels import BoardLabel
from ..deploy_branches import deploy_branches_for, resolve_deploy_pairs, uses_to_deploy_column
from ..workflow_transition import transition
from .core import (
    Action,
    Decision,
    MrSummary,
    RelatedMR,
    apply_mine_by_default,
    decide,
    decide_closed,
    issue_passes_filter,
    latest_semver,
    select_fixing_mrs,
)

_ALL_BOARD_LABELS: str = ",".join(str(b) for b in BoardLabel)


class OutputFormat(StrEnum):
    JSON = "json"
    REPORT = "report"  # human-readable, one block per ticket


_SET_TARGET_LABEL: dict[str, str] = {
    "set_to_deploy": "workflow::To deploy",
    "set_under_review": "workflow::Under review",
    "set_in_progress": "workflow::In progress",
}


@dataclass(frozen=True)
class DecisionEntry:
    """One actionable decision, as reported (and optionally applied) for a ticket."""

    iid: int
    title: str
    owner: str
    current_board: str
    action: str
    reason: str
    target: str = ""
    result: str | None = None  # the apply outcome, only set on an --apply run

    def to_dict(self) -> dict[str, object]:
        entry: dict[str, object] = {
            "iid": self.iid,
            "title": self.title,
            "owner": self.owner,
            "current_board": self.current_board,
            "action": self.action,
            "reason": self.reason,
        }
        if self.target:
            entry["target"] = self.target
        if self.result is not None:
            entry["result"] = self.result
        return entry


@dataclass(frozen=True)
class ProjectReport:
    """Audit outcome for one project: its deployment context and its decisions."""

    project: str
    project_id: str
    deployed_version: str
    deploy_branches: list[str]
    has_deploy: bool
    open_issues_scanned: int
    actionable: int
    decisions: list[DecisionEntry]
    closed_issues_scanned: int | None = None  # only set on a --reopen run

    def to_dict(self) -> dict[str, object]:
        block: dict[str, object] = {
            "project": self.project,
            "project_id": self.project_id,
            "deployed_version": self.deployed_version,
            "deploy_branches": self.deploy_branches,
            "has_deploy": self.has_deploy,
            "open_issues_scanned": self.open_issues_scanned,
            "actionable": self.actionable,
            "decisions": [d.to_dict() for d in self.decisions],
        }
        if self.closed_issues_scanned is not None:
            block["closed_issues_scanned"] = self.closed_issues_scanned
        return block


@dataclass(frozen=True)
class AppliedDecision:
    """One decision acted on when replaying a plan file verbatim (``--apply-plan``)."""

    project_id: str
    iid: int
    action: str
    result: str

    def to_dict(self) -> dict[str, object]:
        return {"project_id": self.project_id, "iid": self.iid, "action": self.action, "result": self.result}


def _status_transition(decision: DecisionEntry) -> tuple[str, str]:
    """``(current status, corrected status)`` for a decision, human-readable."""
    current = decision.current_board or "(aucune colonne)"
    if decision.action == "close":
        return current, "Closed"
    if decision.action == "reopen":
        return "Closed", decision.target or "(rouvert)"
    return current, _SET_TARGET_LABEL.get(decision.action, decision.action)


def _render_report(reports: list[ProjectReport]) -> str:
    """Render a detailed per-ticket report from the actionable project reports."""
    if not reports:
        return "Aucune action — board déjà à jour."
    actionable = sum(r.actionable for r in reports)
    lines: list[str] = [f"{actionable} ticket(s) à corriger :", ""]
    for report in reports:
        for d in report.decisions:
            current, corrected = _status_transition(d)
            lines.append(f"■ {report.project} #{d.iid} — {d.title}")
            lines.append(f"    owner  : {d.owner or '—'}")
            lines.append(f"    statut : {current} → {corrected}")
            lines.append(f"    raison : {d.reason}")
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


app = typer.Typer()


def _parse_deploy_override(entries: list[str] | None) -> dict[str, str] | None:
    """Parse ``--deploy-branch source=deploy`` entries into a mapping (None when unset)."""
    if not entries:
        return None
    mapping: dict[str, str] = {}
    for entry in entries:
        source, sep, deploy = entry.partition("=")
        if sep and source and deploy:
            mapping[source] = deploy
    return mapping or None


def _project_matches(label: str, project_id: str, wanted: set[str]) -> bool:
    """Match a project against a user filter by full path, id, or short name."""
    short = label.rsplit("/", 1)[-1]
    return bool({label, project_id, short} & wanted)


def _list_group_projects(group: str) -> list[tuple[str, str, str]]:
    """Return ``(id, path_with_namespace, default_branch)`` for every non-archived project."""
    enc = group.replace("/", "%2F")
    data = glab_api_paginated(f"groups/{enc}/projects?include_subgroups=true&archived=false")
    return [
        (str(proj["id"]), str(proj.get("path_with_namespace", proj["id"])), str(proj.get("default_branch", "") or ""))
        for proj in data
        if proj.get("id")
    ]


def _unshipped_by_source(project_id: str, pairs: list[tuple[str, str]]) -> dict[str, frozenset[str]]:
    """For each ``(source, deploy)`` pair, the commits on ``source`` **not yet** on ``deploy``.

    One ``compare?from=deploy&to=source`` call per pair: a merged MR targeting ``source``
    whose merge commit is **absent** from this set has shipped. Keyed by source branch.
    """
    result: dict[str, frozenset[str]] = {}
    for source, deploy in pairs:
        frm = deploy.replace("/", "%2F")
        to = source.replace("/", "%2F")
        data = glab_api(f"projects/{project_id}/repository/compare?from={frm}&to={to}&straight=false")
        commits = data.get("commits") if isinstance(data, dict) else None
        if isinstance(commits, list):
            result[source] = frozenset(str(c["id"]) for c in commits if isinstance(c, dict) and c.get("id"))
    return result


def _commit_deployed(merge_commit: str, target_branch: str, unshipped: dict[str, frozenset[str]]) -> bool:
    """Whether a merged MR's commit has shipped on its own line.

    ``target_branch`` is the source branch the MR merged into; the commit is shipped when
    that line is tracked and the commit is no longer among its unshipped commits.
    """
    if not merge_commit or target_branch not in unshipped:
        return False
    return merge_commit not in unshipped[target_branch]


def _deployed_version(project_id: str, deploy_branches: list[str]) -> str:
    """Highest semver tag reachable from ``deploy/prod`` (for display only)."""
    branch = "deploy/prod" if "deploy/prod" in deploy_branches else (deploy_branches[0] if deploy_branches else "")
    if not branch:
        return ""
    enc = branch.replace("/", "%2F")
    refs = glab_api(f"projects/{project_id}/repository/commits/{enc}/refs?type=tag&per_page=100")
    if not isinstance(refs, list):
        return ""
    tags = sorted(
        (str(r["name"]) for r in refs if isinstance(r, dict) and r.get("name")),
        key=_semver_key,
        reverse=True,
    )
    return latest_semver(tags) or ""


def _semver_key(tag: str) -> tuple[int, ...]:
    parts = tag.strip().lstrip("v").split(".")
    try:
        return tuple(int(p) for p in parts[:3])
    except ValueError:
        return (-1,)


def _fetch_open_issues(project_id: str, limit: int) -> list[GitLabIssue]:
    data = glab_api_paginated(f"projects/{project_id}/issues?state=opened")
    issues = [GitLabIssue.from_api(d) for d in data]
    return issues[:limit] if limit > 0 else issues


def _fetch_closed_issues(project_id: str, updated_after: str, limit: int) -> list[GitLabIssue]:
    """Closed issues updated on/after ``updated_after`` (ISO 8601) — the reopen candidates."""
    enc = updated_after.replace(":", "%3A").replace("+", "%2B")
    data = glab_api_paginated(f"projects/{project_id}/issues?state=closed&updated_after={enc}")
    issues = [GitLabIssue.from_api(d) for d in data]
    return issues[:limit] if limit > 0 else issues


def _mr_is_approved(mr_project_id: str, mr_iid: int) -> bool:
    approvals = glab_api(f"projects/{mr_project_id}/merge_requests/{mr_iid}/approvals")
    if not isinstance(approvals, dict):
        return False
    approved_by = approvals.get("approved_by")
    if isinstance(approved_by, list) and approved_by:
        return True
    return approvals.get("approved") is True or approvals.get("approvals_left") == 0


def _mrs_from(project_id: str, iid: int, endpoint: str) -> list[RelatedMR]:
    data = glab_api(f"projects/{project_id}/issues/{iid}/{endpoint}")
    if not isinstance(data, list):
        return []
    out: list[RelatedMR] = []
    for mr in data:
        if not isinstance(mr, dict) or not mr.get("iid"):
            continue
        merge_commit = str(mr.get("merge_commit_sha") or mr.get("squash_commit_sha") or mr.get("sha") or "")
        out.append(
            RelatedMR(
                iid=int(mr["iid"]),
                state=str(mr.get("state", "")),
                source_branch=str(mr.get("source_branch", "") or ""),
                project_id=str(mr.get("project_id", project_id)),
                merge_commit=merge_commit,
                target_branch=str(mr.get("target_branch", "") or ""),
            )
        )
    return out


def _dedupe_mrs(mrs: list[RelatedMR]) -> list[RelatedMR]:
    seen: set[tuple[str, int]] = set()
    out: list[RelatedMR] = []
    for mr in mrs:
        key = (mr.project_id, mr.iid)
        if key not in seen:
            seen.add(key)
            out.append(mr)
    return out


def _mr_summary(
    project_id: str, iid: int, unshipped: dict[str, frozenset[str]], *, comprehensive: bool = False
) -> MrSummary:
    # Priority: the native closed_by link (MRs whose `Closes #N` ties them to the
    # issue). Fall back to related_merge_requests only when closed_by is empty.
    # For the reopen pass, union both so an open MR absent from closed_by is not missed.
    if comprehensive:
        candidates = _dedupe_mrs(
            _mrs_from(project_id, iid, "closed_by") + _mrs_from(project_id, iid, "related_merge_requests")
        )
    else:
        candidates = _mrs_from(project_id, iid, "closed_by") or _mrs_from(project_id, iid, "related_merge_requests")
    selected = select_fixing_mrs(candidates, iid)

    mrs: list[tuple[str, bool, bool]] = []
    for mr in selected:
        approved = mr.state == "opened" and _mr_is_approved(mr.project_id, mr.iid)
        in_prod = mr.state == "merged" and _commit_deployed(mr.merge_commit, mr.target_branch, unshipped)
        mrs.append((mr.state, approved, in_prod))
    return MrSummary.from_mrs(mrs)


def _close_issue(project_id: str, iid: int) -> bool:
    # Closing also strips the board/workflow column label — a closed ticket owns no column.
    return run_glab(
        "api",
        "-X",
        "PUT",
        f"projects/{project_id}/issues/{iid}",
        "-f",
        f"remove_labels={_ALL_BOARD_LABELS}",
        "-f",
        "state_event=close",
    ).ok


def _reopen_issue(project_id: str, iid: int) -> bool:
    return run_glab("api", "-X", "PUT", f"projects/{project_id}/issues/{iid}", "-f", "state_event=reopen").ok


def _apply(project_id: str, d: Decision) -> str:
    if d.action == Action.CLOSE:
        return "closed" if _close_issue(project_id, d.iid) else "error:close-failed"
    if d.action == Action.REOPEN:
        if not _reopen_issue(project_id, d.iid):
            return "error:reopen-failed"
        return f"reopened+{transition(str(d.iid), d.target, project_id)}" if d.target else "reopened"
    if d.action == Action.SET_TO_DEPLOY:
        return transition(str(d.iid), "workflow::To deploy", project_id)
    if d.action == Action.SET_UNDER_REVIEW:
        return transition(str(d.iid), "workflow::Under review", project_id)
    if d.action == Action.SET_IN_PROGRESS:
        return transition(str(d.iid), "workflow::In progress", project_id)
    return "noop"


def _decision_from_plan(entry: dict[str, Any]) -> Decision | None:
    """Rebuild a Decision from a plan-file entry, or ``None`` if it is not applicable."""
    iid = entry.get("iid")
    action = str(entry.get("action", ""))
    if not isinstance(iid, int) or action not in {a.value for a in Action} or action == Action.NOOP:
        return None
    return Decision(
        iid=iid,
        title=str(entry.get("title", "")),
        current_board=str(entry.get("current_board", "")),
        action=Action(action),
        reason="",
        target=str(entry.get("target", "")),
    )


def _apply_plan_file(path: str) -> dict[str, object]:
    """Apply a previously generated plan **verbatim** — no re-audit, no recompute.

    Only the decisions recorded in the file are acted on (close, reopen, set_*),
    exactly as they were shown. Reopens carry their ``target`` column from the plan.
    """
    plan = json.loads(Path(path).read_text(encoding="utf-8"))
    applied: list[AppliedDecision] = []
    results = plan.get("results", []) if isinstance(plan, dict) else []
    for block in results:
        if not isinstance(block, dict):
            continue
        project_id = str(block.get("project_id", ""))
        decisions = block.get("decisions", [])
        if not project_id or not isinstance(decisions, list):
            continue
        for entry in decisions:
            if not isinstance(entry, dict):
                continue
            d = _decision_from_plan(entry)
            if d is None:
                continue
            applied.append(AppliedDecision(project_id, d.iid, str(d.action), _apply(project_id, d)))
    return {
        "applied": True,
        "from_plan": path,
        "count": len(applied),
        "results": [a.to_dict() for a in applied],
    }


@dataclass(frozen=True)
class IssueFilter:
    """Resolved assignment filters (GitLab usernames), applied as AND."""

    mine_user: str | None = None
    assignee_user: str | None = None
    author_user: str | None = None

    def active(self) -> bool:
        return any((self.mine_user, self.assignee_user, self.author_user))


def _issue_owner(issue: GitLabIssue) -> str:
    """Owner username: the first assignee if any, else the author."""
    return issue.assignees[0].username if issue.assignees else issue.author.username


def _keep_issue(issue: GitLabIssue, flt: IssueFilter) -> bool:
    return issue_passes_filter(
        issue.author.username,
        [a.username for a in issue.assignees],
        mine_user=flt.mine_user,
        assignee_user=flt.assignee_user,
        author_user=flt.author_user,
    )


def _has_cancelled_label(issue: GitLabIssue, cancelled_labels: frozenset[str]) -> bool:
    return bool(set(issue.labels) & cancelled_labels)


def _process_project(
    project_id: str,
    label: str,
    *,
    deploy_branch_override: dict[str, str] | None,
    limit: int,
    apply: bool,
    workers: int,
    issue_filter: IssueFilter,
    reopen: bool,
    closed_since: str,
    cancelled_labels: frozenset[str],
) -> ProjectReport:
    """Audit one project; return its report (and apply changes when asked)."""
    mapping = deploy_branches_for(label, deploy_branch_override)
    pairs = resolve_deploy_pairs(project_id, mapping)
    has_deploy = uses_to_deploy_column(label) and bool(pairs)
    unshipped = _unshipped_by_source(project_id, pairs)
    deploy_branches = sorted({dep for _, dep in pairs})
    deployed_version = _deployed_version(project_id, deploy_branches)

    open_issues = _fetch_open_issues(project_id, limit)
    if issue_filter.active():
        open_issues = [i for i in open_issues if _keep_issue(i, issue_filter)]

    closed_issues: list[GitLabIssue] = []
    if reopen:
        closed_issues = _fetch_closed_issues(project_id, closed_since, limit)
        if issue_filter.active():
            closed_issues = [i for i in closed_issues if _keep_issue(i, issue_filter)]
        closed_issues = [i for i in closed_issues if not _has_cancelled_label(i, cancelled_labels)]

    open_iids = [i.iid for i in open_issues if i.iid]
    closed_iids = [i.iid for i in closed_issues if i.iid]
    tasks = [(iid, False) for iid in open_iids] + [(iid, True) for iid in closed_iids]
    mr_map: dict[int, MrSummary] = {}
    if tasks:
        with ThreadPoolExecutor(max_workers=max(1, workers)) as pool:
            summaries = pool.map(lambda t: _mr_summary(project_id, t[0], unshipped, comprehensive=t[1]), tasks)
            for (iid, _), summary in zip(tasks, summaries, strict=True):
                mr_map[iid] = summary

    owner_by_iid: dict[int, str] = {}
    decisions: list[Decision] = []
    for issue in open_issues:
        if issue.iid:
            owner_by_iid[issue.iid] = _issue_owner(issue)
            decisions.append(
                decide(
                    issue.iid,
                    issue.title,
                    issue.labels,
                    mr_map.get(issue.iid, MrSummary()),
                    cancelled_labels,
                    has_deploy,
                )
            )
    for issue in closed_issues:
        if issue.iid:
            owner_by_iid[issue.iid] = _issue_owner(issue)
            decisions.append(
                decide_closed(issue.iid, issue.title, issue.labels, mr_map.get(issue.iid, MrSummary()), has_deploy)
            )

    actionable = [d for d in decisions if d.action != Action.NOOP]
    entries = [
        DecisionEntry(
            iid=d.iid,
            title=d.title,
            owner=owner_by_iid.get(d.iid, ""),
            current_board=d.current_board,
            action=str(d.action),
            reason=d.reason,
            target=d.target,
            result=_apply(project_id, d) if apply else None,
        )
        for d in actionable
    ]
    return ProjectReport(
        project=label,
        project_id=project_id,
        deployed_version=deployed_version,
        deploy_branches=deploy_branches,
        has_deploy=has_deploy,
        open_issues_scanned=len(open_issues),
        actionable=len(actionable),
        decisions=entries,
        closed_issues_scanned=len(closed_issues) if reopen else None,
    )


def _resolve_filter(*, anyone: bool, assignee: str | None, author: str | None) -> IssueFilter:
    """Resolve the assignment flags into GitLab usernames (``@me`` → current user).

    "Mine" is applied by default; ``--anyone`` (or a specific ``--assignee`` /
    ``--author``) opts out of it.
    """
    cached_me: list[str] = []

    def me() -> str:
        if not cached_me:
            cached_me.append(get_current_username())
        return cached_me[0]

    def resolve(token: str) -> str:
        return me() if token.lstrip("@").lower() == "me" else resolve_username(token)

    mine = apply_mine_by_default(anyone=anyone, has_assignee=bool(assignee), has_author=bool(author))
    return IssueFilter(
        mine_user=me() if mine else None,
        assignee_user=resolve(assignee) if assignee else None,
        author_user=resolve(author) if author else None,
    )


@app.command()
def main(
    project: Annotated[
        list[str] | None,
        typer.Option(
            "--project",
            help="Filter to these project(s): path, id or short name (repeatable). Default: all in --group.",
        ),
    ] = None,
    group: Annotated[str, typer.Option("--group", help="Group whose projects are swept.")] = "pysae",
    deploy_branch: Annotated[
        list[str] | None,
        typer.Option(
            "--deploy-branch",
            help="Override the source→deploy branch mapping, as 'source=deploy' (repeatable, globs must "
            "correspond, e.g. 'support/*=deploy/support/*'). Default: the repo's board.deploy_branches, "
            "else main=deploy/prod + support/*=deploy/support/*.",
        ),
    ] = None,
    apply: Annotated[bool, typer.Option("--apply", help="Apply the changes (default: dry-run plan only).")] = False,
    output_format: Annotated[
        OutputFormat,
        typer.Option("--format", help="stdout rendering of the plan: json (default) or report (per-ticket blocks)."),
    ] = OutputFormat.JSON,
    plan_out: Annotated[
        str | None,
        typer.Option(
            "--plan-out", help="Write the computed plan (JSON) to this file, to apply later with --apply-plan."
        ),
    ] = None,
    apply_plan: Annotated[
        str | None,
        typer.Option(
            "--apply-plan",
            help="Apply a plan file written by --plan-out, verbatim (no re-audit). Ignores all other filters.",
        ),
    ] = None,
    limit: Annotated[int, typer.Option("--limit", help="Cap open issues scanned per project (0 = no cap).")] = 0,
    workers: Annotated[int, typer.Option("--workers", help="Concurrent MR lookups.")] = 8,
    anyone: Annotated[
        bool,
        typer.Option(
            "--anyone",
            help="Audit everyone's tickets. By default only mine are audited (assigned to me, "
            "or authored by me with no one else assigned; me = current glab user).",
        ),
    ] = False,
    assignee: Annotated[
        str | None,
        typer.Option(
            "--assignee",
            help="Only tickets assigned to this user (username, name, or @me). Overrides the default 'mine' scope.",
        ),
    ] = None,
    author: Annotated[
        str | None,
        typer.Option(
            "--author",
            help="Only tickets authored by this user (username, name, or @me). Overrides the default 'mine' scope.",
        ),
    ] = None,
    reopen: Annotated[
        bool,
        typer.Option(
            "--reopen",
            help="Also reopen recently-closed tickets closed by mistake (open MR, or a merged MR not yet shipped). "
            "Off by default (opt-in): adds a pass over closed tickets.",
        ),
    ] = False,
    closed_since_days: Annotated[
        int,
        typer.Option(
            "--closed-since", help="For the reopen pass: only consider tickets closed within the last N days."
        ),
    ] = 30,
    cancelled_label: Annotated[
        list[str] | None,
        typer.Option(
            "--cancelled-label",
            help="Label marking a cancelled ticket: closed if still open, never reopened (repeatable, default ANNULE).",
        ),
    ] = None,
) -> None:
    """Audit and (with --apply) fix ticket board statuses across the group.

    By default every non-archived project in ``--group`` is swept; ``--project``
    narrows that set to one or more projects (it is a filter, not a mode). Within
    the scanned projects, **only my tickets are audited by default** — pass
    ``--anyone`` to audit everyone's, or ``--assignee`` / ``--author`` to target a
    specific person. ``--reopen`` additionally reopens recently-closed tickets
    that were closed by mistake (off by default).

    Plan/apply via a file: ``--plan-out plan.json`` saves the computed plan;
    ``--apply-plan plan.json`` then applies it **verbatim** (close, reopen, set_*)
    with no re-audit, so what is applied is exactly what was reviewed.
    """
    if apply_plan:
        try:
            outcome = _apply_plan_file(apply_plan)
        except (OSError, json.JSONDecodeError) as exc:
            print(json.dumps({"error": f"cannot read plan file '{apply_plan}': {exc}"}))
            raise typer.Exit(1) from exc
        print(json.dumps(outcome, ensure_ascii=False, indent=2))
        return

    issue_filter = _resolve_filter(anyone=anyone, assignee=assignee, author=author)
    deploy_override = _parse_deploy_override(deploy_branch)
    cancelled_labels = frozenset(cancelled_label) if cancelled_label else frozenset({"ANNULE"})
    closed_since = (datetime.now(UTC) - timedelta(days=max(0, closed_since_days))).strftime("%Y-%m-%dT%H:%M:%SZ")
    projects = _list_group_projects(group)
    if not projects:
        print(json.dumps({"error": f"no projects found in group '{group}'"}))
        raise typer.Exit(1)

    if project:
        wanted = set(project)
        projects = [t for t in projects if _project_matches(t[1], t[0], wanted)]
        if not projects:
            print(json.dumps({"error": f"no project matched filter {sorted(wanted)} in group '{group}'"}))
            raise typer.Exit(1)

    reports = [
        _process_project(
            pid,
            label,
            deploy_branch_override=deploy_override,
            limit=limit,
            apply=apply,
            workers=workers,
            issue_filter=issue_filter,
            reopen=reopen,
            closed_since=closed_since,
            cancelled_labels=cancelled_labels,
        )
        for pid, label, _default_branch in projects
    ]
    actionable_reports = [r for r in reports if r.actionable]
    plan = {
        "group": group,
        "filtered": bool(project),
        "assignment_filter": (
            {
                "mine": issue_filter.mine_user,
                "assignee": issue_filter.assignee_user,
                "author": issue_filter.author_user,
            }
            if issue_filter.active()
            else None
        ),
        "applied": apply,
        "reopen": reopen,
        "projects_scanned": len(reports),
        "actionable": sum(r.actionable for r in reports),
        "results": [r.to_dict() for r in actionable_reports],
    }
    json_text = json.dumps(plan, ensure_ascii=False, indent=2)
    if plan_out:
        Path(plan_out).write_text(json_text, encoding="utf-8")
        print(f"plan written to {plan_out}", file=sys.stderr)
    print(_render_report(actionable_reports) if output_format is OutputFormat.REPORT else json_text)


if __name__ == "__main__":
    app()
