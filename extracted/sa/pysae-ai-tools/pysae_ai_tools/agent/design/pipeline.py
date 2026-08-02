"""Design-lane batch loop: pull → auto-eligibility gate → headless /design-generate.

Mirrors the code autopilot loop but for design: no MR/deploy-watch, the artifact
is a GitLab Pages proto URL. Reuses the generic engine pieces (orphan reclaim,
budget guard, business score, report publish, the explicit-ticket resolver).
"""

import json
import logging
import os
import subprocess
import time
from datetime import datetime, timezone
from typing import Any

from ...common.references.gitlab_labels import BoardLabel
from ..common import fetch_with_label, resolve_explicit_tickets, run_batch
from ..guards import budget_exhausted
from ..labels import CommentPostError, LabelTransitionError
from ..models import Outcome, OutcomeStatus, RunConfig, RunResult, ScoredTicket, Ticket
from ..orphan import find_orphans
from ..score import business_score
from ..tracking import log_usage
from .eligibility import OVERRIDE_OUT, assess_eligibility
from .labels import (
    DESIGN_BLOCKED,
    DESIGN_REVIEW,
    DESIGN_WIP,
    mark_design_blocked,
    mark_design_review,
    mark_design_wip,
)
from .outcome import resolve_design_outcome

logger = logging.getLogger(__name__)

READY_LABEL = str(BoardLabel.READY)
_ALREADY_PROCESSED = {DESIGN_WIP, DESIGN_REVIEW, DESIGN_BLOCKED, OVERRIDE_OUT}


def _new_run_id() -> str:
    return datetime.now(tz=timezone.utc).strftime("design-%Y-%m-%d-%H%M%S")


def _escalated(ticket: Ticket, reason: str) -> Outcome:
    return Outcome(
        ticket_iid=ticket.iid,
        project_path=ticket.project_path,
        ticket_title=ticket.title,
        ticket_url=ticket.web_url,
        author_username=ticket.author_username,
        status=OutcomeStatus.ESCALATED,
        mr_url=None,
        mr_iid=None,
        escalation_reason=reason,
    )


def exec_design_generate(ticket: Ticket, per_ticket_timeout: int) -> Outcome:
    """Invoke `claude -p --output-format=json /design-generate <url> --auto`.

    `--auto` puts the skill in non-interactive mode (no AskUserQuestion) and makes
    it emit the `<<<DESIGN_RESULT ...>>>` footer parsed by ``resolve_design_outcome``.
    """
    cmd = [
        "claude",
        "-p",
        "--output-format",
        "json",
        "--dangerously-skip-permissions",
        f"/design-generate {ticket.web_url} --auto",
    ]
    sub_env = dict(os.environ)
    autopilot_key = os.environ.get("ANTHROPIC_CI_AUTOPILOT_API_KEY")
    if autopilot_key:
        sub_env["ANTHROPIC_API_KEY"] = autopilot_key
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=per_ticket_timeout,
            check=False,
            env=sub_env,
        )
    except subprocess.TimeoutExpired:
        return _escalated(ticket, f"subprocess timeout after {per_ticket_timeout}s")

    stdout = proc.stdout or ""
    wrapper: dict[str, Any] = {}
    result_text = stdout
    try:
        parsed = json.loads(stdout)
        if isinstance(parsed, dict) and "result" in parsed:
            wrapper = parsed
            result_text = str(wrapper.get("result", ""))
    except json.JSONDecodeError:
        pass

    if proc.returncode != 0 and "DESIGN_RESULT" not in result_text:
        tail = "\n".join(result_text.splitlines()[-50:]) or "\n".join(stdout.splitlines()[-50:])
        return _escalated(ticket, f"subprocess exit {proc.returncode}: {tail[:300]}")

    outcome = resolve_design_outcome(result_text, fallback_iid=ticket.iid, fallback_project=ticket.project_path)
    outcome.ticket_title = ticket.title
    outcome.ticket_url = ticket.web_url
    outcome.author_username = ticket.author_username
    usage = wrapper.get("usage", {}) if wrapper else {}
    if usage:
        outcome.tokens_used = (
            int(usage.get("input_tokens", 0))
            + int(usage.get("output_tokens", 0))
            + int(usage.get("cache_creation_input_tokens", 0))
            + int(usage.get("cache_read_input_tokens", 0))
        )
    duration_ms = wrapper.get("duration_ms")
    if isinstance(duration_ms, (int, float)) and duration_ms > 0:
        outcome.duration_seconds = int(duration_ms // 1000)
    cost = wrapper.get("total_cost_usd")
    if isinstance(cost, (int, float)):
        outcome.cost_usd = float(cost)
    usage_dict = wrapper.get("usage") or {}
    model_used = next(iter((wrapper.get("modelUsage") or {}).keys()), "claude")
    log_usage(
        caller="design-generate",
        model=str(model_used),
        input_tokens=int(usage_dict.get("input_tokens", 0)),
        output_tokens=int(usage_dict.get("output_tokens", 0)),
        cache_creation_tokens=int(usage_dict.get("cache_creation_input_tokens", 0)),
        cache_read_tokens=int(usage_dict.get("cache_read_input_tokens", 0)),
        cost_usd=outcome.cost_usd,
        ticket_iid=ticket.iid,
        project=ticket.project_path,
        duration_seconds=outcome.duration_seconds,
    )
    return outcome


def _already_processed(ticket: Ticket) -> bool:
    return any(lbl in _ALREADY_PROCESSED for lbl in ticket.labels)


def _safe(fn: Any, ticket: Ticket, *args: Any) -> bool:
    """Run a label transition best-effort; return False if it failed."""
    try:
        fn(ticket, *args)
        return True
    except (LabelTransitionError, CommentPostError) as exc:
        logger.error("label transition failed on %s#%s: %s", ticket.project_path, ticket.iid, exc)
        return False


def run_design_pipeline(cfg: RunConfig) -> RunResult:
    """Run the design batch; always publishes the report, even on crash."""
    return run_batch(cfg, _new_run_id(), _run_design_body)


def _run_design_body(cfg: RunConfig, result: RunResult) -> None:
    # 1. Reclaim design::wip orphans (same pickup-marker convention as the code lane).
    wip = fetch_with_label(cfg.projects, DESIGN_WIP)
    for orphan in find_orphans(wip, timeout_seconds=cfg.orphan_timeout_seconds):
        if not cfg.dry_run:
            _safe(
                mark_design_blocked,
                orphan,
                f"WIP orphelin (>{cfg.orphan_timeout_seconds}s), agent crashé probable",
                result.run_id,
            )

    # 2. Pull candidates: workflow::Ready minus already-processed (design::*) tickets.
    if cfg.explicit_tickets:
        ready, failures = resolve_explicit_tickets(cfg.explicit_tickets)
        result.outcomes.extend(failures)
    else:
        ready = [t for t in fetch_with_label(cfg.projects, READY_LABEL) if not _already_processed(t)]

    # 3. Auto-eligibility gate (deterministic prefilter + Haiku + threshold).
    eligible: list[Ticket] = []
    for t in ready:
        verdict = assess_eligibility(t, threshold=cfg.design_eligibility_threshold, skip_llm=cfg.skip_llm_rank)
        if verdict.eligible:
            eligible.append(t)
        else:
            logger.info("[eligibility] skip %s#%d: %s — %s", t.project_path, t.iid, verdict.source, verdict.reason)

    # 4. Rank by deterministic business score, cap to max_tickets.
    ranked = sorted(eligible, key=business_score, reverse=True)[: cfg.max_tickets]

    # 5. Sequential loop.
    start = time.monotonic()
    for ticket in ranked:
        elapsed = int(time.monotonic() - start)
        if budget_exhausted(result, cfg, elapsed_seconds=elapsed):
            break
        if cfg.dry_run:
            logger.info("[dry-run] would design %s#%s", ticket.project_path, ticket.iid)
            biz = float(business_score(ticket))
            result.dry_run_picks.append(
                ScoredTicket(
                    ticket=ticket,
                    business_score=biz,
                    success_probability=100,
                    sensitive_domain_match=False,
                    final_score=biz,
                    rationale="design-eligible",
                )
            )
            continue
        if not _safe(mark_design_wip, ticket):
            continue
        per_ticket_remaining = max(60, cfg.timeout_seconds - elapsed)
        per_ticket_timeout = min(cfg.per_ticket_timeout_seconds, per_ticket_remaining)
        ticket_start = time.monotonic()
        outcome = exec_design_generate(ticket, per_ticket_timeout=per_ticket_timeout)
        if outcome.is_success:
            _safe(mark_design_review, ticket, outcome.preview_url, result.run_id)
        else:
            _safe(mark_design_blocked, ticket, outcome.escalation_reason or "unknown", result.run_id)
        outcome.duration_seconds = int(time.monotonic() - ticket_start)
        result.outcomes.append(outcome)
