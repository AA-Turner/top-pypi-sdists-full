# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Paused Rollout Reports.

When AutoPilot pauses a progressive rollout on the failure-threshold gate it
hands the investigation to a Devin session and makes the #human-in-the-loop
pause thread the artifact operators read: the session analyzes the failing
connections and posts its summary and recommendation as a reply in that thread
(and as `structured_output` on the session).

The session is found again on later pauses of the same rollout through a
`rollout:<rollout_id>` session tag, so nothing is stored on the rollout row or
in a bucket. A repeated pause unarchives the session if needed and sends it the
new gate snapshot plus the new thread to reply in. Recovery actions stay
HITL-gated and are never executed by the investigation session itself.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import UTC, datetime

import requests

from airbyte_ops_mcp import devin_api
from airbyte_ops_mcp.connector_ops.rollouts._helpers import HealthGateResult
from airbyte_ops_mcp.connector_ops.rollouts.models import ConnectorRolloutRecord
from airbyte_ops_mcp.slack_posting import SlackPostResult

logger = logging.getLogger(__name__)

DEVIN_SESSION_TAGS = ("rollout-autopilot", "paused-rollout-report")
"""Tags common to every investigation session; the rollout tag is added per row."""

ROLLOUT_TAG_PREFIX = "rollout:"

MAX_ACU_LIMIT = 25
"""Spend cap per investigation session (covers a few pauses of one rollout)."""

SESSION_ERRORS = (requests.RequestException, RuntimeError, ValueError)
"""Failures while talking to the Devin API that must not abort AutoPilot."""

STRUCTURED_OUTPUT_SCHEMA: dict[str, object] = {
    "type": "object",
    "properties": {
        "summary": {
            "type": "string",
            "description": "Two or three sentences: what failed and whether the RC is implicated.",
        },
        "groups": {
            "type": "array",
            "description": "Failing connections grouped by cause.",
            "items": {
                "type": "object",
                "properties": {
                    "label": {"type": "string"},
                    "actor_count": {"type": "integer"},
                    "failure_origin": {
                        "type": "string",
                        "enum": [
                            "source",
                            "destination",
                            "platform",
                            "replication",
                            "unknown",
                        ],
                    },
                    "attributable_to_rc": {
                        "type": "string",
                        "enum": ["yes", "no", "unclear"],
                    },
                    "notes": {"type": "string"},
                },
                "required": ["label", "actor_count", "failure_origin"],
            },
        },
        "recommendation": {
            "type": "string",
            "description": "One of: unpause, finalize, unpin-then-unpause, rollback, leave-paused, or none-clear; with one sentence of reasoning.",
        },
        "caveats": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["summary", "groups", "recommendation", "caveats"],
}
"""Schema passed as `structured_output_schema` when creating the session."""


def rollout_tag(rollout_id: str) -> str:
    """Return the session tag that identifies a rollout's investigation."""
    return f"{ROLLOUT_TAG_PREFIX}{rollout_id}"


def _gate_snapshot(gate: HealthGateResult) -> str:
    return (
        f"{gate.failed_actor_count} of {gate.actors_with_sync_signal} actors with "
        f"sync signal have at least one failed RC sync ({gate.failure_percent:.1%}); "
        f"{gate.failure_count} failed syncs"
    )


def _thread_instructions(thread: SlackPostResult | None) -> str:
    if thread is None:
        return (
            "AutoPilot could not post the #human-in-the-loop pause alert for this "
            "pause, so there is no thread to reply in; put the write-up in this "
            "session instead."
        )
    return (
        f"Post it as a reply in the #human-in-the-loop pause thread: channel "
        f"`{thread.channel_id}`, thread_ts `{thread.ts}` ({thread.permalink}). "
        "Use your Slack tool to post a reply with that channel and `thread_ts`. "
        "If you have no Slack tool, the Ops MCP tool "
        "`devin_session_feedback_followup` posts a reply to any thread in the "
        "workspace: pass the permalink above as `thread_url` (it appends a "
        "not-monitored footer, which is acceptable). If neither works, say so in "
        "this session and put the write-up here instead."
    )


def build_investigation_prompt(
    rollout: ConnectorRolloutRecord,
    rc_version: str,
    gate: HealthGateResult,
    thread: SlackPostResult | None,
) -> str:
    """Return the prompt handed to a newly created investigation session."""
    now = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    return f"""\
# Paused Rollout Report: {rollout.connector_name} {rc_version}

AutoPilot paused progressive rollout `{rollout.rollout_id}` because its
failure-threshold health gate tripped. Investigate why and write the result for
an operator deciding what to do with the rollout. The operator reads the Slack
thread, not this session, so the thread reply must stand on its own.

## Rollout
- Connector: {rollout.connector_name} (actor_definition_id `{rollout.actor_definition_id}`)
- Release candidate: {rc_version} (GA before rollout: {rollout.initial_docker_image_tag or "unknown"})
- Tier: {rollout.tier or "unknown"}
- Rollout created: {rollout.created_at or "unknown"}
- Paused at: {now}
- Gate reason: {gate.reason}
- Gate snapshot: {_gate_snapshot(gate)}

## Order of work
1. `query_prod_rollout_monitoring_stats` for rollout `{rollout.rollout_id}`
   returns the pinned actor IDs and per-actor RC sync counts with no customer
   details. The failing set is every actor with `num_failed > 0`.
2. Until a human approves otherwise, use **only tier-filtered tools** and keep
   their `customer_tier_filter` at its default `TIER_2`; the filter is applied
   server-side, so TIER_0/TIER_1 rows never reach this session. Both DB
   tools default to `lookback_days=7` and `limit=100`: set `lookback_days`
   to cover the whole rollout (from the created timestamp above) and raise
   `limit` until the result is no longer capped; if a result stays capped,
   say so in the write-up and mark the affected groups incomplete:
   - `query_prod_failed_sync_attempts_for_connector` (by
     `source_definition_id` `{rollout.actor_definition_id}`, `lookback_days`
     covering the rollout) gives each failed attempt's `failure_summary`
     (`failureOrigin`, `failureType`, message), `actor_id`,
     `organization_id` and `customer_tier`.
   - `query_prod_recent_syncs_for_connector` (same definition ID,
     `status_filter="all"`) gives each connection's recent job outcomes and
     its *current* pin (`pin_origin`, `pinned_version_id`), but not the
     version each job ran on or when the pin was created. For a destination
     rollout pass `destination_definition_id` instead; the failed-attempts
     tool is source-only, so use this tool's `status_filter="failed"` rows
     there.
   - `query_prod_connector_versions` (by `connector_definition_id`
     `{rollout.actor_definition_id}`) lists the version IDs; pick the RC and
     GA `version_id` values and pass each to
     `query_connector_version_health_summary` for an **actor-level**
     healthy/unhealthy comparison of RC vs GA (it does not count jobs).
   Confirm the returned organizations' tiers with `lookup_customer_tiers`.
   Do NOT call `query_prod_actors_by_pinned_connector_version`,
   `query_prod_recent_syncs_for_connector_version` or
   `query_prod_connection_sync_activity` before approval: they have no tier
   filter and return connection, workspace and organization names.
3. Failing actors from step 1 that are absent from the TIER_2 results may be
   TIER_0/TIER_1, `UNKNOWN` tier (organization not in the tier export), or
   simply outside the lookback window or row limit; absence alone tells you
   nothing about sensitivity. Report them only as a count. If they matter to
   the conclusion, call `escalate_to_human`, wait for approval, and only then
   re-run the tier-filtered queries with `customer_tier_filter="ALL"`,
   reporting UNKNOWN-tier actors as their own aggregate.
4. Then analyze **every** actor the gate counts as failing that you have data
   for. For each, record: successes and failures on the RC (from step 1),
   whether its most recent job succeeded or failed and when it last ran (from
   the recent-syncs rows), and the latest failure's `failureOrigin`,
   `failureType` and message. A per-job RC-vs-GA *job-level* failure rate and
   an exact before/after-pin timeline need
   `query_prod_recent_syncs_for_connector_version` (job-stamped version IDs),
   which is unfiltered; use it only after approval in step 3, otherwise report
   the actor-level comparison and say that is what it is.

## What to produce
1. A summary of the failing connections grouped by cause, failure origin
   (source / destination / platform / replication) and organization. Call out
   correlated failures (one customer outage counted many times) and stale
   failures (connections that failed once and never ran again).
2. The RC-vs-GA health comparison (actor-level, or job-level if approved),
   kept distinct from the gate's metric, which counts every pinned actor with
   at least one failed RC sync — including actors that failed once weeks ago
   and never ran again.
3. Per group, whether the failure plausibly traces to the RC. Treat
   destination failures as a judgment call: a source data-type or schema
   change can surface as a destination error, so do not dismiss them blindly.
4. The recovery options (unpause, finalize to GA, unpin failing actors then
   unpause, roll back, leave paused) with trade-offs, and a recommendation
   only when the evidence clearly favors one.

## When done
- {_thread_instructions(thread)}
  Keep it to what an operator needs: the grouped summary, the RC-vs-GA
  comparison versus the gate metric, the recommendation (or "no clear call"), and the
  caveats. Slack mrkdwn, no tables wider than a phone screen.
- Then call `provide_structured_output` with `summary`, `groups`,
  `recommendation` and `caveats` matching the same conclusions.

## Guardrails
- Do NOT unpause, finalize, cancel, unpin or otherwise mutate the rollout or
  any actor pins. Any recovery action must go through the Slack
  human-in-the-loop approval flow (`escalate_to_human`) and be explicitly
  approved by a human before it is executed.
- Customer tiers: follow the order of work above and never widen
  `customer_tier_filter` without approval. Describe TIER_0/TIER_1
  actors only in aggregate (counts and failure origin) with no identifying
  details, whether or not access was approved. The Slack thread is visible to
  everyone in the channel: never paste connection names, hostnames, or
  credentials there.
- If this rollout pauses again, AutoPilot sends a follow-up message here with
  a new gate snapshot and a new thread to reply in; treat it as a fresh pause
  and update your analysis rather than repeating the old one.
"""


def build_repause_message(
    rollout: ConnectorRolloutRecord,
    rc_version: str,
    gate: HealthGateResult,
    thread: SlackPostResult | None,
) -> str:
    """Return the follow-up message sent when a rollout pauses again."""
    now = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    return (
        f"Rollout `{rollout.rollout_id}` ({rollout.connector_name} {rc_version}) "
        f"paused again at {now}.\n"
        f"Gate reason: {gate.reason}\n"
        f"Gate snapshot: {_gate_snapshot(gate)}.\n"
        "Re-run the analysis against the current failing set, say what changed "
        "since the previous pause, and update the recommendation. "
        f"{_thread_instructions(thread)} Then call `provide_structured_output` "
        "again with the updated conclusions. Same guardrails apply: no rollout "
        "or pin mutations without HITL approval."
    )


def find_investigation_session(rollout_id: str) -> devin_api.DevinSessionRef | None:
    """Return the newest session tagged for `rollout_id`, if any.

    The list endpoint matches any of the given tags, so only the
    rollout-specific tag is sent and the result is re-checked client-side.
    """
    tag = rollout_tag(rollout_id)
    sessions = devin_api.list_sessions(tags=[tag], limit=5)
    return next((s for s in sessions if tag in s.tags), None)


@dataclass(frozen=True)
class SessionLookup:
    """Outcome of `lookup_investigation_session`.

    `failed` is set when the Devin API could not be queried, in which case no
    session is started either (a fresh one would risk duplicating an existing
    investigation).
    """

    session: devin_api.DevinSessionRef | None = None
    failed: bool = False


def lookup_investigation_session(rollout_id: str) -> SessionLookup:
    """Non-raising `find_investigation_session` for use in the pause path."""
    if not devin_api.is_configured():
        return SessionLookup()
    try:
        return SessionLookup(session=find_investigation_session(rollout_id))
    except SESSION_ERRORS as exc:
        logger.warning(
            "paused-rollout-report: failed to look up investigation session for %s: %s",
            rollout_id,
            exc,
        )
        return SessionLookup(failed=True)


def start_investigation_session(
    rollout: ConnectorRolloutRecord,
    rc_version: str,
    gate: HealthGateResult,
    thread: SlackPostResult | None,
    lookup: SessionLookup,
) -> devin_api.DevinSessionRef | None:
    """Start (or continue) the Devin investigation for a rollout pause.

    `lookup` comes from `lookup_investigation_session`; an existing session is
    unarchived if needed and sent a follow-up with the new gate snapshot and
    `thread`, otherwise a new session is created with the investigation
    prompt. Returns `None` when the Devin API is not configured
    or a call fails, so the pause and its Slack alert proceed regardless. Two
    AutoPilot runs pausing the same rollout within the same minute could both
    create a session; that is accepted rather than adding a claim step.
    """
    if not devin_api.is_configured():
        logger.info(
            "paused-rollout-report: Devin API token/org ID not configured; "
            "skipping investigation session for %s",
            rollout.rollout_id,
        )
        return None
    if lookup.failed:
        return None

    existing = lookup.session
    if existing is not None:
        try:
            if existing.is_archived:
                existing = devin_api.unarchive_session(existing.session_id)
            devin_api.send_session_message(
                existing.session_id,
                build_repause_message(rollout, rc_version, gate, thread),
            )
        except SESSION_ERRORS as exc:
            logger.warning(
                "paused-rollout-report: failed to message existing session %s "
                "for %s: %s",
                existing.url,
                rollout.rollout_id,
                exc,
            )
            return None
        logger.info(
            "paused-rollout-report: re-used investigation session %s for %s",
            existing.url,
            rollout.rollout_id,
        )
        return existing

    try:
        created = devin_api.create_session(
            build_investigation_prompt(rollout, rc_version, gate, thread),
            title=(
                f"Paused Rollout Report: {rollout.connector_name} {rc_version} "
                f"({rollout.rollout_id[:8]})"
            ),
            tags=[*DEVIN_SESSION_TAGS, rollout_tag(rollout.rollout_id)],
            max_acu_limit=MAX_ACU_LIMIT,
            structured_output_schema=STRUCTURED_OUTPUT_SCHEMA,
        )
    except SESSION_ERRORS as exc:
        logger.warning(
            "paused-rollout-report: failed to start investigation session for %s: %s",
            rollout.rollout_id,
            exc,
        )
        return None
    logger.info(
        "paused-rollout-report: started investigation session %s for %s",
        created.url,
        rollout.rollout_id,
    )
    return created
