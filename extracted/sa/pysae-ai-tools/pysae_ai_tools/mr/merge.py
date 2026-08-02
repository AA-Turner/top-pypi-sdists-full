"""``pysae-ai-tools mr merge`` — merge a merge request, handling every state.

The MR primitives (fetch, draft flip, merge) go through the
:class:`MergeRequestProvider`, so no code here shells out to ``glab``/``gh``
directly. The GitLab ``detailed_merge_status``
dispatch loop is preserved verbatim (draft flip, transient polling, CI-gating,
delegation to ``/mr-rebase`` and ``/ci-run``) — it is GitLab vocabulary, so
it only runs for the GitLab provider; GitHub takes a straightforward path.

On a default-branch GitLab merge, the linked issue's board column is settled via
``glab.workflow_transition.settle_issue_after_merge`` (a GitLab-only board
concern, hence the reviewed ``mr → glab`` layering edge).

Exit code is ``0`` on ``merged``, ``2`` on ``needs_skill`` (caller must invoke
the named skill and re-run), ``1`` otherwise.
"""

import json
import sys
import time
from dataclasses import dataclass, field
from typing import Annotated, Any, Literal

import typer

from ..common.issue_tracking.platform import Platform
from ..common.merge_requests.models import MergeRequest
from ..common.merge_requests.provider import MergeRequestProvider
from ..glab.workflow_transition import settle_issue_after_merge
from ..internal.detect_context.detect import DetectArgs, detect
from .resolve import resolve_provider

_PROJECT_HELP = "Target another repo relative to the current owner ('op', 'infra/infra-cluster') or a full URL"

AUTO_FIX_CAP = 10
SHORT_POLL_ATTEMPTS = 6
SHORT_POLL_INTERVAL_S = 5
LONG_POLL_ATTEMPTS = 60
LONG_POLL_INTERVAL_S = 30

REBASE_STATUSES = {"conflict", "requires_rebase", "need_rebase"}
CI_STATUSES = {"ci_must_pass", "ci_still_running"}
LONG_TRANSIENT = {"checking", "unchecked"}
SHORT_TRANSIENT = {"preparing", "approvals_syncing", "cannot_be_merged_rechecking"}
HARD_BLOCKERS = {
    "not_open",
    "not_approved",
    "discussions_not_resolved",
    "external_status_checks",
    "jira_association_missing",
    "requested_changes",
    "policies_denied",
    "commits_status",
    "blocked_status",
    "merge_request_blocked",
    "cannot_be_merged",
    "cannot_be_merged_recheck",
}

OutcomeStatus = Literal["merged", "blocked", "needs_skill", "error"]


@dataclass
class MergeOutcome:
    """Final result of a merge attempt."""

    status: OutcomeStatus
    mr_iid: str
    mr_url: str = ""
    merge_status: str = ""
    sha: str = ""
    issue_transitioned: str = ""
    skill: str = ""
    skill_args: list[str] = field(default_factory=list)
    blocker: str = ""
    message: str = ""

    def to_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {
            "status": self.status,
            "mr_iid": self.mr_iid,
            "mr_url": self.mr_url,
            "detailed_merge_status": self.merge_status,
        }
        if self.status == "merged":
            out["sha"] = self.sha
            out["issue_transitioned"] = self.issue_transitioned
        elif self.status == "needs_skill":
            out["skill"] = self.skill
            out["skill_args"] = self.skill_args
        elif self.status in ("blocked", "error"):
            out["blocker"] = self.blocker
            out["message"] = self.message
        return out

    def to_text(self) -> str:
        url = self.mr_url or f"!{self.mr_iid}"
        if self.status == "merged":
            line = f"✓ MR mergée : {url} ({self.sha[:8]})"
            if self.issue_transitioned:
                line += f" — {self.issue_transitioned}"
            return line
        if self.status == "needs_skill":
            args = " ".join(self.skill_args) if self.skill_args else ""
            return f"⤴ MR {url} : statut {self.merge_status} — déléguer à /{self.skill} {args}".rstrip()
        if self.status == "blocked":
            extra = f" — {self.message}" if self.message else ""
            return f"✗ MR {url} : bloquée ({self.blocker}){extra}"
        return f"✗ MR {url} : erreur — {self.message}"


def _linked_issue_iid(description: str) -> str:
    for token in description.split():
        stripped = token.strip(".,;:()")
        if stripped.startswith("#") and stripped[1:].isdigit():
            return stripped[1:]
    return ""


def _merge_now(provider: MergeRequestProvider, iid: str) -> tuple[MergeRequest | None, str]:
    """Attempt the merge; return ``(merged_mr, "")`` or ``(None, error_message)``."""
    try:
        return provider.merge(iid), ""
    except (RuntimeError, LookupError) as exc:
        return None, str(exc)


def _settle_issue(mr: MergeRequest, project_path: str, default_branch: str) -> str:
    """Settle the linked issue's board column after a default-branch GitLab merge."""
    issue_iid = _linked_issue_iid(mr.description)
    if not issue_iid:
        return ""
    if mr.target_branch and default_branch and mr.target_branch != default_branch:
        return ""
    return settle_issue_after_merge(issue_iid, project_path=project_path)


def _classify(status: str) -> str:
    if status == "mergeable":
        return "mergeable"
    if status == "draft_status":
        return "draft"
    if status in REBASE_STATUSES:
        return "needs_rebase"
    if status in CI_STATUSES:
        return "needs_ci"
    if status in LONG_TRANSIENT:
        return "transient_long"
    if status in SHORT_TRANSIENT:
        return "transient_short"
    if status in HARD_BLOCKERS:
        return "blocker"
    return "unknown"


def _poll(provider: MergeRequestProvider, iid: str, transient: set[str], attempts: int, interval: int) -> str:
    last = ""
    for _ in range(attempts):
        time.sleep(interval)
        try:
            last = provider.get_mr(iid).merge_status
        except LookupError:
            return ""
        if last not in transient:
            return last
    return last


def _merge_gitlab(provider: MergeRequestProvider, iid: str, project_path: str, default_branch: str) -> MergeOutcome:
    for _ in range(AUTO_FIX_CAP):
        try:
            mr = provider.get_mr(iid)
        except LookupError:
            return MergeOutcome("error", iid, blocker="fetch_failed", message=f"impossible de récupérer la MR !{iid}")
        category = _classify(mr.merge_status)

        if category == "mergeable":
            merged, err = _merge_now(provider, iid)
            if merged is not None:
                return MergeOutcome(
                    "merged",
                    iid,
                    mr_url=mr.web_url,
                    merge_status=mr.merge_status,
                    sha=merged.merge_commit_sha,
                    issue_transitioned=_settle_issue(merged, project_path, default_branch),
                )
            return MergeOutcome(
                "error", iid, mr_url=mr.web_url, merge_status=mr.merge_status, blocker="merge_failed", message=err
            )

        if category == "draft":
            provider.update_mr(iid, draft=False)
            continue

        if category == "needs_rebase":
            return MergeOutcome(
                "needs_skill",
                iid,
                mr_url=mr.web_url,
                merge_status=mr.merge_status,
                skill="mr-rebase",
                skill_args=[f"!{iid}"],
            )

        if category == "needs_ci":
            merged, _err = _merge_now(provider, iid)
            if merged is not None:
                return MergeOutcome(
                    "merged",
                    iid,
                    mr_url=mr.web_url,
                    merge_status=mr.merge_status,
                    sha=merged.merge_commit_sha,
                    issue_transitioned=_settle_issue(merged, project_path, default_branch),
                )
            return MergeOutcome(
                "needs_skill",
                iid,
                mr_url=mr.web_url,
                merge_status=mr.merge_status,
                skill="ci-run",
                skill_args=["start"],
            )

        if category == "transient_long":
            new_status = _poll(provider, iid, LONG_TRANSIENT, LONG_POLL_ATTEMPTS, LONG_POLL_INTERVAL_S)
            if new_status in LONG_TRANSIENT or not new_status:
                minutes = LONG_POLL_ATTEMPTS * LONG_POLL_INTERVAL_S // 60
                return MergeOutcome(
                    "blocked",
                    iid,
                    mr_url=mr.web_url,
                    merge_status=new_status or mr.merge_status,
                    blocker="transient_timeout",
                    message=f"statut encore {mr.merge_status} après {minutes} min",
                )
            continue

        if category == "transient_short":
            new_status = _poll(provider, iid, SHORT_TRANSIENT, SHORT_POLL_ATTEMPTS, SHORT_POLL_INTERVAL_S)
            if new_status in SHORT_TRANSIENT or not new_status:
                return MergeOutcome(
                    "blocked",
                    iid,
                    mr_url=mr.web_url,
                    merge_status=new_status or mr.merge_status,
                    blocker=mr.merge_status,
                    message=f"statut encore {mr.merge_status} après {SHORT_POLL_ATTEMPTS * SHORT_POLL_INTERVAL_S} s",
                )
            continue

        if category == "blocker":
            return MergeOutcome(
                "blocked", iid, mr_url=mr.web_url, merge_status=mr.merge_status, blocker=mr.merge_status
            )

        return MergeOutcome(
            "blocked",
            iid,
            mr_url=mr.web_url,
            merge_status=mr.merge_status,
            blocker="unknown_status",
            message=f"detailed_merge_status='{mr.merge_status}' inconnu — vérifier manuellement la MR",
        )

    return MergeOutcome(
        "error",
        iid,
        blocker="auto_fix_loop_exceeded",
        message=f"plus de {AUTO_FIX_CAP} itérations d'auto-fix sans atteindre mergeable",
    )


def _merge_github(provider: MergeRequestProvider, iid: str) -> MergeOutcome:
    try:
        mr = provider.get_mr(iid)
    except LookupError:
        return MergeOutcome("error", iid, blocker="fetch_failed", message=f"impossible de récupérer la PR #{iid}")
    if mr.draft:
        provider.update_mr(iid, draft=False)
    merged, err = _merge_now(provider, iid)
    if merged is not None:
        return MergeOutcome("merged", iid, mr_url=mr.web_url, merge_status=mr.merge_status, sha=merged.merge_commit_sha)
    return MergeOutcome(
        "blocked", iid, mr_url=mr.web_url, merge_status=mr.merge_status, blocker="merge_failed", message=err
    )


def merge_mr(iid: str, project: str | None = None) -> MergeOutcome:
    """Run the full dispatch and return the outcome."""
    provider = resolve_provider(project=project)
    if provider.platform is Platform.GITHUB:
        return _merge_github(provider, iid)
    ctx = detect(DetectArgs(refs=[], local=True))
    return _merge_gitlab(provider, iid, ctx.project_path or ctx.project_id, ctx.default_branch or "main")


def main(
    iid: Annotated[str, typer.Argument(help="Merge request number to merge")],
    as_json: Annotated[bool, typer.Option("--json", help="Emit the outcome as a JSON object on stdout.")] = False,
    project: Annotated[str, typer.Option("--project", help=_PROJECT_HELP)] = "",
) -> None:
    """Merge a merge request, handling every merge state."""
    outcome = merge_mr(iid, project=project or None)
    if as_json:
        json.dump(outcome.to_dict(), sys.stdout, ensure_ascii=False)
        sys.stdout.write("\n")
    else:
        typer.echo(outcome.to_text())
    if outcome.status == "merged":
        return
    if outcome.status == "needs_skill":
        raise typer.Exit(code=2)
    raise typer.Exit(code=1)
