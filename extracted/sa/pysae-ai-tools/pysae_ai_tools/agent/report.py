"""Reporting: stdout summary table + Slack notifications."""

import json
import logging
import urllib.error
from typing import Any

from ..common.project_config import ProjectConfig, ProjectConfigError, load_project_config_for
from ..slack.common import get_slack_token
from ..slack.post_message import post_message
from .models import Outcome, OutcomeStatus, RunConfig, RunResult

logger = logging.getLogger(__name__)


def _project_config(project_path: str, cache: dict[str, ProjectConfig]) -> ProjectConfig:
    """Resolve (and memoise) a project's config; degrade to schema defaults on any failure.

    Reporting must never break because a repo's config couldn't be fetched (glab down, parse
    error, not found) — the schema defaults leave Slack on, so a transient failure never
    silences a repo by accident.
    """
    if project_path not in cache:
        try:
            cache[project_path] = load_project_config_for(project_path) or ProjectConfig()
        except (ProjectConfigError, RuntimeError, OSError) as exc:
            logger.warning("project config resolution failed for %s: %s", project_path, exc)
            cache[project_path] = ProjectConfig()
    return cache[project_path]


def _slack_on(project_path: str, cache: dict[str, ProjectConfig]) -> bool:
    """Whether the batch report may post about ``project_path``: the repo's ``slack.enabled``
    master switch AND its dedicated ``autopilot.slack`` toggle must both be on."""
    cfg = _project_config(project_path, cache)
    return cfg.slack.enabled and cfg.autopilot.slack


def format_summary_table(result: RunResult, max_tokens: int, max_tickets: int) -> str:
    dry_run = bool(result.dry_run_picks) and not result.outcomes
    header_count = len(result.dry_run_picks) if dry_run else len(result.outcomes)
    header_label = "Tickets that would be processed (dry-run)" if dry_run else "Tickets processed"
    not_ready_outcomes = [o for o in result.outcomes if o.status == OutcomeStatus.NOT_READY]
    deferred_outcomes = [o for o in result.outcomes if o.status == OutcomeStatus.DEFERRED]
    skipped_statuses = {OutcomeStatus.NOT_READY, OutcomeStatus.DEFERRED}
    processed_outcomes = [o for o in result.outcomes if o.status not in skipped_statuses]
    lines = [
        "=== code-autopilot-batch run summary ===",
        f"Run ID: {result.run_id}",
        f"{header_label}: {header_count} / {max_tickets}",
        f"Tokens used: {result.total_tokens:,} / {max_tokens:,}",
        f"Successes: {result.successes} | Escalations: {result.escalations} "
        f"| Not ready: {result.not_readys} | Deferred: {result.deferreds}",
        "",
    ]
    if dry_run:
        lines += [
            "| IID  | Project              | Score  | Title",
            "|------|----------------------|--------|------",
        ]
        for s in result.dry_run_picks:
            t = s.ticket
            lines.append(f"| {t.iid:<4} | {t.project_path:<20} | {s.final_score:>6.1f} | {t.title[:80]}")
    else:
        lines += [
            "| IID  | Project        | Status     | MR    | Time   | Tokens  | Reason",
            "|------|----------------|------------|-------|--------|---------|-------",
        ]
        for o in processed_outcomes:
            mr = f"!{o.mr_iid}" if o.mr_iid else "-"
            time_str = f"{o.duration_seconds // 60}m {o.duration_seconds % 60:02d}s"
            reason = o.escalation_reason or ""
            lines.append(
                f"| {o.ticket_iid:<4} | {o.project_path:<14} | {o.status.value:<10} "
                f"| {mr:<5} | {time_str:<6} | {o.tokens_used:>7,} | {reason[:60]}"
            )
    if not_ready_outcomes:
        lines += [
            "",
            "Not-ready tickets (skipped before scoring):",
        ]
        for o in not_ready_outcomes:
            violations_str = ", ".join(o.not_ready_violations) if o.not_ready_violations else "unknown"
            lines.append(f"  - {o.project_path}#{o.ticket_iid} : {violations_str}")
    if deferred_outcomes:
        lines += [
            "",
            "Deferred tickets (unmet dependency — retried next run):",
        ]
        for o in deferred_outcomes:
            reason_str = ", ".join(o.not_ready_violations) if o.not_ready_violations else "unknown"
            lines.append(f"  - {o.project_path}#{o.ticket_iid} : {reason_str}")
    return "\n".join(lines)


def _post_to_slack(channel: str, text: str) -> None:
    try:
        token = get_slack_token()
        if not token:
            logger.warning("slack post skipped (channel=%s): no token (SLACK_BOT_TOKEN/USER_TOKEN unset)", channel)
            return
        resp = post_message(token, {"channel": channel, "text": text})
    except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError) as exc:
        logger.warning("slack post failed (channel=%s): %s", channel, exc)
        return
    # Slack returns 200 + {ok: false, error: "..."} on application errors
    # (not_in_channel, channel_not_found, invalid_auth, etc.) — surface them.
    if isinstance(resp, dict) and not resp.get("ok"):
        logger.warning("slack post rejected (channel=%s): %s", channel, resp.get("error", "unknown"))


def _resolve_channel(project_path: str, cfg: RunConfig, cache: dict[str, ProjectConfig] | None = None) -> str:
    """Pick the Slack channel for a project: explicit map override, then (when per-project
    routing is on) the repo's own ``slack.tech_channel``, else the default channel."""
    if project_path in cfg.slack_channel_map:
        return cfg.slack_channel_map[project_path]
    if cfg.slack_per_project:
        tech = _project_config(project_path, cache if cache is not None else {}).slack.tech_channel
        if tech:
            return tech
    return cfg.slack_channel


def _fmt_duration(seconds: int) -> str:
    if seconds <= 0:
        return "0s"
    m, s = divmod(seconds, 60)
    return f"{m}m {s:02d}s" if m else f"{s}s"


def _fmt_tokens(n: int) -> str:
    if n <= 0:
        return "0"
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n / 1_000:.0f}k"
    return str(n)


def _fmt_cost(usd: float) -> str:
    if usd <= 0:
        return "$0"
    return f"${usd:.2f}" if usd >= 0.01 else f"${usd:.4f}"


def _ticket_header(o: Any) -> str:
    """One-line header: emoji + bold ticket ref/title."""
    label = f"#{o.ticket_iid}"
    if o.ticket_title:
        label = f"{label} — {o.ticket_title}"
    return label


def _not_ready_bullet(o: Outcome) -> str:
    """Slack bullet for a NOT_READY outcome: clickable ref + @-mention + raison."""
    title = o.ticket_title or o.project_path
    if o.ticket_url:
        ref = f"<{o.ticket_url}|#{o.ticket_iid} — {title}>"
    else:
        ref = f"{o.project_path}#{o.ticket_iid}"
    mention = f" (cc @{o.author_username})" if o.author_username else ""
    reason = "; ".join(o.not_ready_violations) or "unknown"
    return f"• {ref}{mention} — {reason}"


def publish(result: RunResult, cfg: RunConfig) -> None:
    table = format_summary_table(result, cfg.max_tokens, cfg.max_tickets)
    print(table)

    if not cfg.slack_enabled:
        return

    # Per-project gate: a repo with slack.enabled=false, or autopilot.slack=false, gets no
    # batch post at all (per-ticket, grouped, or counted in the aggregate). Resolved once per
    # project and memoised for the whole publish.
    cfg_cache: dict[str, ProjectConfig] = {}

    not_ready_outcomes: list[Outcome] = [
        o for o in result.outcomes if o.status == OutcomeStatus.NOT_READY and _slack_on(o.project_path, cfg_cache)
    ]
    if not_ready_outcomes:
        bullets = "\n".join(_not_ready_bullet(o) for o in not_ready_outcomes)
        _post_to_slack(
            cfg.slack_channel,
            f":no_entry_sign: *{len(not_ready_outcomes)} ticket(s) non prêts* (skipped avant scoring)\n{bullets}",
        )

    for o in result.outcomes:
        if o.status == OutcomeStatus.NOT_READY or not _slack_on(o.project_path, cfg_cache):
            continue
        header = _ticket_header(o)
        if o.status == OutcomeStatus.SUCCESS:
            mr_link = f"<{o.mr_url}|MR !{o.mr_iid}>" if o.mr_url and o.mr_iid else f"MR !{o.mr_iid}"
            metrics = (
                f":hourglass: {_fmt_duration(o.duration_seconds)} · "
                f":coin: {_fmt_tokens(o.tokens_used)} tokens · "
                f":moneybag: {_fmt_cost(o.cost_usd)}"
            )
            deploy_note = ""
            if o.deploy_status:
                if o.deploy_retries == 1:
                    retries_txt = " (1 retry)"
                elif o.deploy_retries > 1:
                    retries_txt = f" ({o.deploy_retries} retries)"
                else:
                    retries_txt = ""
                deploy_note = f" · :rocket: deploy_dev {o.deploy_status}{retries_txt}"
            text = (
                f":white_check_mark: *{header}*\n"
                f"{mr_link} mergée sur `{o.project_path}`\n"
                f"{metrics}{deploy_note}"
            )
        elif o.status == OutcomeStatus.ESCALATED:
            prefix = f"@{o.author_username} — " if o.author_username else ""
            text = f":octagonal_sign: {prefix}*{header}* — `{o.project_path}`\nRaison : {o.escalation_reason}"
            if o.mr_url and o.mr_iid:
                text += f"\nMR : <{o.mr_url}|MR !{o.mr_iid}>"
            if o.deploy_job_url:
                text += f"\n<{o.deploy_job_url}|Voir le job deploy>"
        else:
            text = f":warning: Échec technique : *{header}* — `{o.project_path}`"
        _post_to_slack(_resolve_channel(o.project_path, cfg, cfg_cache), text)

    # Skip the aggregate summary when one or fewer Slack-enabled processed outcomes remain: a
    # single one would just repeat the per-ticket numbers, and zero means every repo opted out.
    # NOT_READY outcomes already got their own grouped notif above, so exclude them here.
    processed = [
        o for o in result.outcomes if o.status != OutcomeStatus.NOT_READY and _slack_on(o.project_path, cfg_cache)
    ]
    if len(processed) <= 1:
        return

    total_duration = sum(o.duration_seconds for o in processed)
    total_cost = sum(o.cost_usd for o in processed)
    succ_word = "succès"  # invariable
    esc_word = "escalade" if result.escalations <= 1 else "escalades"
    summary = (
        f":robot_face: *Run {result.run_id} terminé*\n"
        f":white_check_mark: {result.successes} {succ_word} · "
        f":octagonal_sign: {result.escalations} {esc_word}\n"
        f":hourglass: {_fmt_duration(total_duration)} total · "
        f":coin: {_fmt_tokens(result.total_tokens)} tokens · "
        f":moneybag: {_fmt_cost(total_cost)}"
    )
    # Aggregate summary lands on the default channel only — per-project channels
    # already got their per-ticket notifs.
    _post_to_slack(cfg.slack_channel, summary)
