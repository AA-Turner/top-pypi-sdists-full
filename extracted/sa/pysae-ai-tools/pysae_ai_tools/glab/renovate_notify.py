"""Notify each repo's tech Slack channel about *blocking* Renovate MRs.

Renovate runs centrally (one ``pysae/infra/renovate-runner`` pipeline for the whole
group) and has no native per-repo Slack routing. This command closes that gap: after a
Renovate run it scans the group's open Renovate MRs, keeps only the ones that **cannot
auto-merge** and therefore need a human — major bumps (``major-update``) and security
updates (``security``) — and posts each to its repo's tech channel, resolved from the
repo's ``.pysae-ai-tools.yaml`` (``slack.tech_channel_id``). Patch/minor MRs that
auto-merge on green CI are never announced.

Routing carries no hardcoded Pysae data: the channel comes from each repo's config, and
the flow honours that config's ``slack.enabled`` master switch and
``slack.notifications.renovate`` opt-out. Idempotence is a label: every notified MR gets
``slack-notified`` and is skipped on subsequent runs, so re-running the pipeline never
double-pings.

Usage:
    pysae-ai-tools glab renovate-notify [--group pysae] [--dry-run]

Auth: ``glab`` (``GITLAB_TOKEN`` in CI) for the API, ``SLACK_BOT_TOKEN`` for posting.
"""

import re
from dataclasses import dataclass
from typing import Annotated, Any

import typer

from ..common.glab.fetch_issues import glab_api_paginated, run_glab
from ..common.project_config import ProjectConfig, load_project_config_from_gitlab
from ..slack.client import SlackApiError, slack_post
from ..slack.common import get_slack_token

app = typer.Typer()

# Label carried by every Renovate MR (set by the shared preset's ``labels``); scopes the
# group MR scan to Renovate's own MRs server-side.
BASE_LABEL = "dependencies"

# Labels that mark a Renovate MR as *blocking* (never auto-merged → needs a human), mapped
# to their human wording. These are Renovate-preset conventions, not Pysae routing data.
TRIGGER_LABELS: dict[str, str] = {"major-update": "major", "security": "sécurité"}

# Idempotence marker: added to an MR once notified, and used to skip it next run.
NOTIFIED_LABEL = "slack-notified"

_MR_URL_RE = re.compile(r"^https?://[^/]+/(.+?)/-/merge_requests/\d+")


def project_path_from_url(web_url: str) -> str:
    """Extract the ``group/subgroup/repo`` path from an MR ``web_url`` (``""`` if it doesn't match)."""
    match = _MR_URL_RE.match(web_url)
    return match.group(1) if match else ""


def matched_triggers(labels: list[str]) -> list[str]:
    """Human wording of every trigger label present on the MR, in ``TRIGGER_LABELS`` order."""
    present = set(labels)
    return [human for label, human in TRIGGER_LABELS.items() if label in present]


def should_notify(labels: list[str]) -> bool:
    """True when the MR is blocking (a trigger label) and not already notified.

    Draft MRs are intentionally included: a major/security bump is worth surfacing to the
    team even while Renovate is still finishing it, so the review can start early.
    """
    if NOTIFIED_LABEL in labels:
        return False
    return bool(matched_triggers(labels))


def build_message(*, project_path: str, title: str, url: str, source: str, target: str, triggers: list[str]) -> str:
    """Render the Slack mrkdwn body for one blocking Renovate MR."""
    kind = " + ".join(triggers)
    return (
        f":package: *Renovate — mise à jour bloquante* dans `{project_path}` _{kind}_\n"
        f"<{url}|{title}>\n"
        f"`{source}` → `{target}`\n"
        "Cette MR ne s'auto-merge pas et attend une review."
    )


@dataclass
class NotifyResult:
    """Outcome for one candidate MR (drives output + exit reporting)."""

    project_path: str
    url: str
    status: str  # "notified" | "dry-run" | "skipped-slack-disabled" | "skipped-no-channel" | "error"
    detail: str = ""


def _channel_id_for(cfg: ProjectConfig | None) -> str:
    """Resolved tech-channel Slack ID for a repo, or ``""`` when unset/disabled."""
    if cfg is None:
        return ""
    if not cfg.slack.enabled or not cfg.slack.notifications.renovate:
        return ""
    return cfg.slack.tech_channel_id or ""


def list_blocking_mrs(group: str) -> list[dict[str, Any]]:
    """Open Renovate MRs in ``group`` that are blocking and not yet notified."""
    enc = group.replace("/", "%2F")
    mrs = glab_api_paginated(f"groups/{enc}/merge_requests?state=opened&labels={BASE_LABEL}&scope=all")
    return [mr for mr in mrs if should_notify(list(mr.get("labels", [])))]


def mark_notified(project_id: int, mr_iid: int) -> None:
    """Add the ``slack-notified`` label to an MR (additive; keeps existing labels)."""
    endpoint = f"projects/{project_id}/merge_requests/{mr_iid}?add_labels={NOTIFIED_LABEL}"
    run_glab("api", "-X", "PUT", endpoint, allow_fail=True)


def _notify_one(mr: dict[str, Any], token: str, *, dry_run: bool) -> NotifyResult:
    web_url = str(mr.get("web_url", ""))
    project_path = project_path_from_url(web_url)
    triggers = matched_triggers(list(mr.get("labels", [])))
    try:
        cfg = load_project_config_from_gitlab(project_path)
    except (RuntimeError, ValueError):
        cfg = None
    channel_id = _channel_id_for(cfg)
    if cfg is not None and (not cfg.slack.enabled or not cfg.slack.notifications.renovate):
        return NotifyResult(project_path, web_url, "skipped-slack-disabled")
    if not channel_id:
        return NotifyResult(project_path, web_url, "skipped-no-channel", "no slack.tech_channel_id in config")
    text = build_message(
        project_path=project_path,
        title=str(mr.get("title", "")),
        url=web_url,
        source=str(mr.get("source_branch", "")),
        target=str(mr.get("target_branch", "")),
        triggers=triggers,
    )
    if dry_run:
        return NotifyResult(project_path, web_url, "dry-run", f"→ {channel_id}")
    try:
        slack_post(token, "chat.postMessage", {"channel": channel_id, "text": text})
    except SlackApiError as e:
        return NotifyResult(project_path, web_url, "error", e.code or str(e))
    mark_notified(int(mr["project_id"]), int(mr["iid"]))
    return NotifyResult(project_path, web_url, "notified", f"→ {channel_id}")


@app.command()
def main(
    group: Annotated[str, typer.Option("--group", help="GitLab group to scan for Renovate MRs.")] = "pysae",
    dry_run: Annotated[
        bool, typer.Option("--dry-run", help="Report what would be posted without posting or labelling.")
    ] = False,
) -> None:
    """Post blocking Renovate MRs (major/security) to each repo's tech Slack channel."""
    mrs = list_blocking_mrs(group)
    if not mrs:
        typer.echo("No blocking Renovate MR to notify.")
        return
    token = "" if dry_run else get_slack_token()
    if not dry_run and not token:
        typer.secho("✗ no Slack token (set SLACK_BOT_TOKEN)", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)
    errors = 0
    for mr in mrs:
        result = _notify_one(mr, token, dry_run=dry_run)
        if result.status == "error":
            errors += 1
        line = f"[{result.status}] {result.project_path} {result.url}"
        typer.echo(f"{line}  {result.detail}".rstrip(), err=result.status == "error")
    if errors:
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
