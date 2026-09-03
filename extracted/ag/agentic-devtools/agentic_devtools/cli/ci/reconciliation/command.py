"""CLI entry point for durable reconciliation dispatch.

Provides the ``agdt-ci-reconcile`` command that instantiates the configured
provider, loads persisted queue state, and dispatches at most one due item.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from pathlib import Path
from uuid import uuid4

from agentic_devtools.cli.ci.cooldown import active_cooldown, ai_pr_loop_credential_identities
from agentic_devtools.cli.ci.models import PRMetadata
from agentic_devtools.cli.ci.provider import CIPlatformProvider
from agentic_devtools.cli.ci.reconciliation import config
from agentic_devtools.cli.ci.reconciliation.dispatch import DispatchResult, dispatch_due_work, select_due_work
from agentic_devtools.cli.ci.reconciliation.metrics import MetricEventType, create_metric_event
from agentic_devtools.cli.ci.reconciliation.models import (
    MetricEvent,
    OperationStatus,
    QueueState,
    ReconciliationAction,
    ReconciliationRecord,
    WorkItem,
    WorkItemStatus,
)
from agentic_devtools.cli.ci.reconciliation.queue_store import (
    QueueStore,
    QueueStoreError,
)
from agentic_devtools.cli.ci.reconciliation.queue_transitions import complete_work_item
from agentic_devtools.cli.ci.reconciliation.recovery import reclaim_leases, rehydrate_state
from agentic_devtools.cli.github.repo_resolution import resolve_github_repo
from agentic_devtools.orchestration.safety.operation_log import OperationLog, OperationLogRecord

logger = logging.getLogger(__name__)
_MAX_METRIC_EVENTS = 4096


def _positive_int(value: str) -> int:
    """Argparse type helper that rejects non-positive integers."""
    try:
        v = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"{value!r} is not a valid integer") from None
    if v < 1:
        raise argparse.ArgumentTypeError(f"{value} must be >= 1")
    return v


def reconcile_command(argv: list[str] | None = None) -> int:
    """CLI entry point for ``agdt-ci-reconcile``.

    Args:
        argv: Command-line arguments (defaults to sys.argv[1:]).

    Returns:
        Exit code: 0 for success/no-op, 1 for errors.
    """
    parser = argparse.ArgumentParser(
        prog="agdt-ci-reconcile",
        description="Dispatch one durable reconciliation work item.",
    )
    parser.add_argument(
        "--workflow-id",
        required=True,
        help="Workflow file name or ID to reconcile (retained for CLI compatibility).",
    )
    parser.add_argument(
        "--provider",
        choices=["github", "ado"],
        default="github",
        help="CI provider to use (default: github).",
    )
    parser.add_argument(
        "--repo",
        default="",
        help="Repository in 'owner/repo' format (GitHub provider). Defaults to current context.",
    )
    parser.add_argument(
        "--max-attempts",
        type=_positive_int,
        default=None,
        help="Accepted for CLI compatibility; must be >= 1 when provided.",
    )
    parser.add_argument(
        "--window-hours",
        type=_positive_int,
        default=None,
        help="Accepted for CLI compatibility; must be >= 1 when provided.",
    )
    parser.add_argument(
        "--json-output",
        action="store_true",
        help="Output result as JSON.",
    )
    parser.add_argument(
        "--invalidate-inventory",
        action="store_true",
        help="Force the next persisted inventory scan even when a cache window is active.",
    )
    parser.add_argument(
        "--trusted-pr-number",
        type=_positive_int,
        default=None,
        help="Trusted pull request number to observe immediately before the next full inventory scan.",
    )
    parser.add_argument(
        "--trusted-head-sha",
        default="",
        help="Trusted pull request head SHA paired with --trusted-pr-number.",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging.",
    )

    args = parser.parse_args(argv)

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")
    else:
        logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    if not config.ENABLE_RECONCILIATION:
        message = "Reconciliation disabled by AGDT_ENABLE_RECONCILIATION"
        if args.json_output:
            print(
                json.dumps(
                    {
                        "action": ReconciliationAction.NO_ACTION.value,
                        "message": message,
                        "lease_id": None,
                        "operation_id": None,
                        "pr_number": None,
                    },
                    indent=2,
                )
            )
        else:
            print(message)
        return 0

    if args.provider == "ado":
        logger.error("The 'ado' provider does not support durable queue persistence; only 'github' is supported.")
        return 1

    try:
        repo = args.repo
        if args.repo:
            repo = resolve_github_repo(args.repo)
        provider = _create_provider(args.provider, repo)
        if active_cooldown(
            provider,
            credential_identity=ai_pr_loop_credential_identities(),
            use_writer_token=bool(os.environ.get("REPO_VARIABLE_WRITER_PAT", "").strip()),
        ):
            message = "Reconciliation blocked by provider cooldown."
            if args.json_output:
                print(
                    json.dumps(
                        {
                            "action": ReconciliationAction.NO_ACTION.value,
                            "message": message,
                            "lease_id": None,
                            "operation_id": None,
                            "pr_number": None,
                        },
                        indent=2,
                    )
                )
            else:
                print(message)
            return 0
        queue_store = QueueStore(repo=repo)
        queue_store.ensure_state_ref()
        recovery_token: str | None = None
        try:
            queue_state = queue_store.load()
        except QueueStoreError as exc:
            logger.warning("Queue state requires recovery: %s", exc)
            recovery_token = queue_store.recovery_token()
            recovery_seed = QueueState(repo=repo, revision=0, items={}, records=[], quarantines=[])
            queue_state = rehydrate_state(
                recovery_seed,
                lambda: _authoritative_rehydrate_loader(provider, queue_store, recovery_seed, repo),
            )
            if recovery_token is not None:
                queue_state = queue_store.save_recovery(queue_state, recovery_token)
        else:
            if (
                queue_state.last_updated_at is not None
                and (datetime.now(UTC) - queue_state.last_updated_at).total_seconds() > config.MAX_STATE_AGE_SECONDS
            ):
                logger.warning("Queue state is stale; rehydrating before reconciliation")
                queue_state = rehydrate_state(
                    queue_state,
                    lambda: _authoritative_rehydrate_loader(provider, queue_store, queue_state, repo),
                )
        operation_log = OperationLog(
            Path(os.environ.get("AGDT_STATE_DIR", ".agdt")),
            os.environ.get("AGDT_RUN_ID", "reconciliation"),
        )
        operation_log.log_path.parent.mkdir(parents=True, exist_ok=True)
        operation_log.log_path.touch(exist_ok=True)
        queue_state = _refresh_inventory(
            provider,
            queue_store,
            queue_state,
            repo,
            invalidate_inventory=args.invalidate_inventory,
            trusted_pr_number=args.trusted_pr_number,
            trusted_head_sha=args.trusted_head_sha,
        )
        reclaimed_state = reclaim_leases(queue_state)
        if reclaimed_state != queue_state:  # pragma: no cover - provider-backed persistence path
            queue_state = queue_store.save(reclaimed_state, expected_revision=queue_state.revision)
        dispatch_now = datetime.now(UTC)
        due_work = select_due_work(queue_state, dispatch_now)
        dispatch_result = dispatch_due_work(
            queue_state,
            eligibility_checker=_build_live_eligibility_checker(provider) if due_work else None,
            preflight_checker=_build_live_preflight_checker(provider) if due_work else None,
            now=dispatch_now,
            store=queue_store,
            operation_log=operation_log,
            operation_id=os.environ.get("AGDT_OPERATION_ID") or None,
        )
        unknown_dispatch = dispatch_result.eligibility.eligibility_reason in {
            "live_eligibility_unknown",
            "preflight_unknown",
        }
        metric_state = dispatch_result.state or queue_state
        dispatch_item = (
            metric_state.items.get(dispatch_result.lease.pr_number) if dispatch_result.lease is not None else None
        )
        unchanged_dispatch = dispatch_item is not None and _was_unchanged_dispatch(
            metric_state,
            dispatch_item.pr_number,
            dispatch_item.change_id,
        )
        if unknown_dispatch:
            metric_state = replace(
                metric_state,
                records=[
                    *metric_state.records,
                    ReconciliationRecord(
                        record_id=str(uuid4()),
                        repo=repo,
                        run_id=operation_log.run_id,
                        started_at=dispatch_now,
                        completed_at=dispatch_now,
                        provider_status="unknown",
                        message=(
                            f"{dispatch_result.eligibility.eligibility_reason}"
                            f" for pr_number={dispatch_result.eligibility.pr_number}"
                        ),
                        unknown_outcomes=(dispatch_result.eligibility.pr_number,),
                    ),
                ],
            )
        metric_state = _append_metric_event(
            metric_state,
            create_metric_event(
                MetricEventType.DISPATCH_OPPORTUNITY
                if dispatch_result.lease is not None
                else MetricEventType.PROVIDER_FAILURE
                if unknown_dispatch
                else MetricEventType.IDLE_CYCLE,
                repo,
                {
                    "pr_number": dispatch_result.lease.pr_number if dispatch_result.lease is not None else None,
                    "change_id": dispatch_item.change_id if dispatch_item is not None else None,
                    "eligibility_reason": dispatch_result.eligibility.eligibility_reason,
                },
            ),
        )
        if unchanged_dispatch and dispatch_item is not None:
            metric_state = _append_metric_event(
                metric_state,
                create_metric_event(
                    MetricEventType.UNCHANGED_DISPATCH,
                    repo,
                    {"pr_number": dispatch_item.pr_number, "change_id": dispatch_item.change_id},
                ),
            )
        if dispatch_result.lease is None:
            queue_store.save(metric_state, expected_revision=metric_state.revision)
        else:
            dispatch_result = replace(dispatch_result, state=metric_state)
        if dispatch_result.lease is not None:  # pragma: no cover - provider-backed dispatch path
            try:
                provider.dispatch_workflow(
                    args.workflow_id,
                    {
                        "pr_number": str(dispatch_result.lease.pr_number),
                        "operation_id": dispatch_result.operation_id,
                    },
                )
                dispatch_state = dispatch_result.state or queue_state
                if dispatch_result.lease.pr_number in dispatch_state.items:
                    completed = complete_work_item(
                        dispatch_state,
                        dispatch_result.lease,
                        dispatch_result.operation_id,
                        dispatch_state.recovery_epoch,
                    )
                    queue_store.save(completed, expected_revision=dispatch_state.revision)
                    operation_log.append(
                        OperationLogRecord(
                            operation_id=dispatch_result.operation_id,
                            run_id=operation_log.run_id,
                            tool_name="reconciliation.dispatch",
                            node_name="reconcile_command",
                            status="completed",
                        )
                    )
            except Exception:
                operation_log.append(
                    OperationLogRecord(
                        operation_id=dispatch_result.operation_id,
                        run_id=operation_log.run_id,
                        tool_name="reconciliation.dispatch",
                        node_name="reconcile_command",
                        status="failed",
                    )
                )
                failed = _release_dispatch_lease(dispatch_result.state or queue_state, dispatch_result.lease)
                queue_store.save(failed, expected_revision=(dispatch_result.state or queue_state).revision)
                raise
    except (NotImplementedError, RuntimeError) as exc:
        logger.error("Reconciliation failed: %s", exc)
        return 1
    except Exception as exc:  # noqa: BLE001
        logger.error("Unexpected reconciliation error: %s", exc)
        return 1

    action, message = _summarize_dispatch_result(dispatch_result)
    if args.json_output:
        output = {
            "action": action.value,
            "message": message,
            "lease_id": dispatch_result.lease.lease_id if dispatch_result.lease else None,
            "operation_id": dispatch_result.operation_id or None,
            "pr_number": dispatch_result.lease.pr_number if dispatch_result.lease else None,
        }
        print(json.dumps(output, indent=2))
    else:
        print(message)

    return 0


def _summarize_dispatch_result(result: DispatchResult) -> tuple[ReconciliationAction, str]:
    if result.lease is None:
        return ReconciliationAction.NO_ACTION, "No due reconciliation work found."
    return ReconciliationAction.RETRIED, f"Dispatched reconciliation for PR #{result.lease.pr_number}."


def _create_provider(provider_name: str, repo: str):
    """Create the appropriate CI provider instance."""
    if provider_name == "github":
        from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider

        return GitHubActionsProvider(repo=repo)
    if provider_name == "ado":
        from agentic_devtools.cli.ci.ado_provider import AzureDevOpsProvider

        return AzureDevOpsProvider()
    raise ValueError(f"Unknown provider: {provider_name!r}")


def _refresh_inventory(
    provider: CIPlatformProvider,
    store: QueueStore,
    state: QueueState,
    repo: str,
    *,
    invalidate_inventory: bool = False,
    trusted_pr_number: int | None = None,
    trusted_head_sha: str = "",
) -> QueueState:
    """Observe the bounded provider inventory and merge changed PRs into the queue."""
    if not repo:
        return state
    now = datetime.now(UTC)
    trusted_event_state = state
    if invalidate_inventory:
        trusted_event_state = replace(trusted_event_state, inventory_invalidated=True)
    if trusted_pr_number is not None:
        trusted_event_state = _observe_trusted_pull_request(
            provider,
            store,
            trusted_event_state,
            repo,
            trusted_pr_number,
            trusted_head_sha,
            now,
        )
        if trusted_event_state.next_inventory_at is not None and trusted_event_state.next_inventory_at > now:
            return trusted_event_state
    state = trusted_event_state
    if (
        state.full_scan_complete
        and not state.inventory_invalidated
        and state.next_inventory_at is not None
        and state.next_inventory_at > now
    ):
        return state
    try:
        initial_cursor = state.pagination_cursor
        scan_started_at = state.inventory_scan_started_at if initial_cursor is not None else now
        cursor: str | None = initial_cursor
        observed: dict[int, PRMetadata] = {}
        for _ in range(config.MAX_PAGINATION_PAGES_PER_RUN):
            page, cursor = provider.list_relevant_pull_requests(cursor=cursor)
            for metadata in page:
                if metadata.number in observed:
                    continue
                observed[metadata.number] = metadata
            if cursor is None:
                break
        eligible_numbers = set(observed)
        items = dict(state.items)
        for pr_number, metadata in observed.items():
            existing = items.get(pr_number)
            watermark = existing.observation_watermark if existing else ""
            changed = existing is None or existing.change_id != metadata.head_sha
            attribution = provider.get_pr_copilot_attribution(pr_number, observation_watermark=watermark)
            should_queue = existing is None or bool(attribution.get("review")) or bool(attribution.get("push"))
            observation_watermark = (
                str(attribution["observation_watermark"])
                if "observation_watermark" in attribution
                else (existing.observation_watermark if existing else metadata.head_sha)
            )
            if (
                existing and changed and existing.status in {WorkItemStatus.CLAIMED, WorkItemStatus.LEASED}
            ):  # pragma: no cover - concurrent production transition
                items[pr_number] = replace(
                    existing,
                    pending_change_id=metadata.head_sha,
                    eligibility="eligible" if pr_number in eligible_numbers else "ineligible",
                    observation_watermark=observation_watermark,
                    last_observed_at=now,
                )
                continue
            reset_completed = existing is not None and existing.status == WorkItemStatus.COMPLETED and should_queue
            items[pr_number] = WorkItem(
                pr_number=pr_number,
                repo=repo,
                change_id=metadata.head_sha,
                eligibility="eligible" if pr_number in eligible_numbers else "ineligible",
                due_at=now if should_queue else (existing.due_at if existing else None),
                status=WorkItemStatus.QUEUED if reset_completed or existing is None else existing.status,
                claimed_at=None if reset_completed else (existing.claimed_at if existing else None),
                claim_expires_at=None if reset_completed else (existing.claim_expires_at if existing else None),
                claim_id="" if reset_completed else (existing.claim_id if existing else ""),
                lease_id="" if reset_completed else (existing.lease_id if existing else ""),
                lease_expires_at=None if reset_completed else (existing.lease_expires_at if existing else None),
                operation_id="" if reset_completed else (existing.operation_id if existing else ""),
                operation_status=OperationStatus.ACTIVE
                if reset_completed or existing is None
                else existing.operation_status,
                completed_at=None if reset_completed else (existing.completed_at if existing else None),
                retry_count=existing.retry_count if existing else 0,
                last_observed_at=now,
                observation_watermark=observation_watermark,
                pending_change_id="",
            )
        next_scan_started_at = scan_started_at
        if cursor is None:
            next_scan_started_at = None
        elif next_scan_started_at is None and (cursor != initial_cursor or bool(observed)):
            next_scan_started_at = now
        if cursor is None and scan_started_at is not None:
            items = _retire_absent_work_items_after_scan(
                items,
                observed_numbers=eligible_numbers,
                scan_started_at=scan_started_at,
                now=now,
            )
        refreshed = replace(
            state,
            items=items,
            pagination_cursor=cursor,
            full_scan_complete=cursor is None,
            metric_events=(
                [
                    *state.metric_events,
                    create_metric_event(
                        MetricEventType.DISCOVERY,
                        repo,
                        {"observed_count": len(observed), "pages": config.MAX_PAGINATION_PAGES_PER_RUN},
                    ),
                ][-_MAX_METRIC_EVENTS:]
                if observed
                else state.metric_events
            ),
            next_inventory_at=(
                now + timedelta(minutes=config.RECONCILIATION_SCHEDULE_INTERVAL_MINUTES) if cursor is None else None
            ),
            inventory_invalidated=cursor is not None,
            inventory_scan_started_at=next_scan_started_at,
        )
        if refreshed != state:
            return store.save(refreshed, expected_revision=state.revision)
        return state

    except (NotImplementedError, AttributeError, KeyError, TypeError, ValueError, RuntimeError) as exc:
        logger.warning("Inventory observation unavailable: %s", exc)
        return state


def _retire_absent_work_items_after_scan(
    items: dict[int, WorkItem],
    *,
    observed_numbers: set[int],
    scan_started_at: datetime,
    now: datetime,
) -> dict[int, WorkItem]:
    """Mark unobserved non-inflight items ineligible when a full scan completes."""
    for pr_number, existing in list(items.items()):
        if pr_number in observed_numbers:
            continue
        if existing.status in {WorkItemStatus.CLAIMED, WorkItemStatus.LEASED}:
            continue
        if existing.last_observed_at is not None and existing.last_observed_at >= scan_started_at:
            continue
        if existing.eligibility == "ineligible" and existing.due_at is None:
            continue
        items[pr_number] = replace(existing, eligibility="ineligible", due_at=None, last_observed_at=now)
    return items


def _authoritative_rehydrate_loader(
    provider: CIPlatformProvider,
    store: QueueStore,
    state: QueueState,
    repo: str,
) -> QueueState:
    """Rebuild queue state from a forced full provider inventory scan."""
    baseline = replace(
        state,
        items={},
        pagination_cursor=None,
        full_scan_complete=False,
        next_inventory_at=None,
        inventory_invalidated=True,
    )
    refreshed = _refresh_inventory(provider, store, baseline, repo, invalidate_inventory=True)
    if refreshed == baseline:
        raise RuntimeError("Authoritative queue inventory was unavailable")
    return refreshed


def _observe_trusted_pull_request(
    provider: CIPlatformProvider,
    store: QueueStore,
    state: QueueState,
    repo: str,
    pr_number: int,
    trusted_head_sha: str,
    now: datetime,
) -> QueueState:
    """Persist an immediate observation for one trusted PR and invalidate the next full scan."""
    try:
        metadata = provider.get_pr_metadata(pr_number)
        invalidated_state = replace(state, inventory_invalidated=True)
        if trusted_head_sha and metadata.head_sha != trusted_head_sha:
            return (
                store.save(invalidated_state, expected_revision=state.revision) if invalidated_state != state else state
            )
        existing = invalidated_state.items.get(pr_number)
        watermark = existing.observation_watermark if existing else ""
        attribution = provider.get_pr_copilot_attribution(pr_number, observation_watermark=watermark)
        observed = _merge_observed_pull_request(
            invalidated_state,
            metadata=metadata,
            eligible=True,
            should_queue=existing is None or bool(attribution.get("review")) or bool(attribution.get("push")),
            observation_watermark=(
                str(attribution["observation_watermark"])
                if "observation_watermark" in attribution
                else (existing.observation_watermark if existing else metadata.head_sha)
            ),
            now=now,
        )
        return store.save(observed, expected_revision=state.revision) if observed != state else state
    except (NotImplementedError, AttributeError, KeyError, TypeError, ValueError, RuntimeError) as exc:
        logger.warning("Trusted-event observation unavailable for PR #%s: %s", pr_number, exc)
        invalidated_state = replace(state, inventory_invalidated=True)
        return store.save(invalidated_state, expected_revision=state.revision) if invalidated_state != state else state


def _merge_observed_pull_request(
    state: QueueState,
    *,
    metadata: PRMetadata,
    eligible: bool,
    should_queue: bool,
    observation_watermark: str,
    now: datetime,
) -> QueueState:
    items = dict(state.items)
    existing = items.get(metadata.number)
    if (
        existing
        and existing.change_id != metadata.head_sha
        and existing.status in {WorkItemStatus.CLAIMED, WorkItemStatus.LEASED}
    ):
        items[metadata.number] = replace(
            existing,
            pending_change_id=metadata.head_sha,
            eligibility="eligible" if eligible else "ineligible",
            observation_watermark=observation_watermark,
            last_observed_at=now,
        )
        return replace(state, items=items)
    reset_completed = existing is not None and existing.status == WorkItemStatus.COMPLETED and should_queue
    items[metadata.number] = WorkItem(
        pr_number=metadata.number,
        repo=state.repo,
        change_id=metadata.head_sha,
        eligibility="eligible" if eligible else "ineligible",
        due_at=now if should_queue else (existing.due_at if existing else None),
        status=WorkItemStatus.QUEUED if reset_completed or existing is None else existing.status,
        claimed_at=None if reset_completed else (existing.claimed_at if existing else None),
        claim_expires_at=None if reset_completed else (existing.claim_expires_at if existing else None),
        claim_id="" if reset_completed else (existing.claim_id if existing else ""),
        lease_id="" if reset_completed else (existing.lease_id if existing else ""),
        lease_expires_at=None if reset_completed else (existing.lease_expires_at if existing else None),
        operation_id="" if reset_completed else (existing.operation_id if existing else ""),
        operation_status=OperationStatus.ACTIVE if reset_completed or existing is None else existing.operation_status,
        completed_at=None if reset_completed else (existing.completed_at if existing else None),
        retry_count=existing.retry_count if existing else 0,
        last_observed_at=now,
        observation_watermark=observation_watermark,
        pending_change_id="",
    )
    return replace(state, items=items)


def _append_metric_event(state: QueueState, event: MetricEvent) -> QueueState:
    """Persist a bounded history of reconciliation measurements in queue state."""
    return replace(state, metric_events=[*state.metric_events, event][-_MAX_METRIC_EVENTS:])


def _was_unchanged_dispatch(state: QueueState, pr_number: int, change_id: str) -> bool:
    """Return whether the last dispatch opportunity used the same PR revision."""
    for event in reversed(state.metric_events):
        if event.event_type != MetricEventType.DISPATCH_OPPORTUNITY.value:
            continue
        if event.attributes.get("pr_number") != pr_number:
            continue
        return event.attributes.get("change_id") == change_id
    return False


def _build_live_eligibility_checker(provider: CIPlatformProvider):
    """Build a checker backed by the provider's current scheduler eligibility."""
    eligible_numbers = {candidate.number for candidate in provider.list_eligible_prs()}
    return lambda item: item.pr_number in eligible_numbers


def _build_live_preflight_checker(provider: CIPlatformProvider):
    """Build a checker that confirms the PR is still readable and open-relevant."""

    def _check(item: WorkItem) -> bool:
        metadata = provider.get_pr_metadata(item.pr_number)
        return metadata.number == item.pr_number and metadata.head_sha == item.change_id

    return _check


def _release_dispatch_lease(state: QueueState, lease) -> QueueState:  # pragma: no cover - provider failure path
    item = state.items[lease.pr_number]
    return replace(
        state,
        items={
            **state.items,
            lease.pr_number: replace(
                item,
                status=WorkItemStatus.QUEUED,
                claim_id="",
                lease_id="",
                claim_expires_at=None,
                lease_expires_at=None,
                claimed_at=None,
                operation_status=OperationStatus.EXPIRED,
            ),
        },
    )
