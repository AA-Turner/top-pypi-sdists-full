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
from agentic_devtools.cli.ci.reconciliation.cas_recovery import CASExhaustionReporter, _PreDispatchCASRetry
from agentic_devtools.cli.ci.reconciliation.command_errors import handle_reconciliation_error
from agentic_devtools.cli.ci.reconciliation.contention import (
    QueueTransitionRetryExhaustedError,
    rebase_rehydration,
    retry_queue_transition,
    wait_for_contention,
)
from agentic_devtools.cli.ci.reconciliation.dispatch import (
    DispatchResult,
    DispatchRetryExhaustedError,
    dispatch_due_work,
    select_due_work,
)
from agentic_devtools.cli.ci.reconciliation.inventory_diagnostics import _build_live_eligibility_checker, summarize_scan
from agentic_devtools.cli.ci.reconciliation.metrics import MetricEventType, create_metric_event
from agentic_devtools.cli.ci.reconciliation.models import (
    Lease,
    MetricEvent,
    OperationStatus,
    QueueState,
    ReconciliationAction,
    ReconciliationRecord,
    WorkItem,
    WorkItemStatus,
)
from agentic_devtools.cli.ci.reconciliation.queue_store import (
    ConcurrentModificationError,
    QueueStore,
    QueueStoreError,
    StateTooLargeError,
)
from agentic_devtools.cli.ci.reconciliation.queue_transitions import complete_work_item
from agentic_devtools.cli.ci.reconciliation.recovery import (
    RecoveryExhaustedError,
    reclaim_leases,
    rehydrate_state,
)
from agentic_devtools.cli.github.repo_resolution import resolve_github_repo
from agentic_devtools.orchestration.safety.operation_log import OperationLog, OperationLogRecord

logger = logging.getLogger(__name__)
_MAX_METRIC_EVENTS = 4096
_ALLOWED_WORKFLOW_IDS = ("ai-pr-loop.yml",)


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
    """Retry pre-dispatch CAS conflicts iteratively, without growing the Python stack."""
    return CASExhaustionReporter.run_with_outer_retries(
        lambda triggering_retry: _reconcile_command_once(argv, triggering_retry),
        config.MAX_RETRY_ATTEMPTS,
        wait_for_contention,
    )


def _reconcile_command_once(
    argv: list[str] | None = None,
    triggering_retry: _PreDispatchCASRetry | None = None,
) -> int:
    """CLI entry point for ``agdt-ci-reconcile``.

    Args:
        argv: Command-line arguments (defaults to sys.argv[1:]).

    Returns:
        Exit code: 0 for success/no-op or classified rate-limit deferral, 1 for errors.
    """
    parser = argparse.ArgumentParser(
        prog="agdt-ci-reconcile",
        description="Dispatch one durable reconciliation work item.",
    )
    parser.add_argument(
        "--mode",
        choices=["dispatch", "inspect-inventory", "inspect-ledger", "inspect-runs", "restart-recovery-epoch"],
        default="dispatch",
        help="Command mode: dispatch due work (default), inspect durable state, or restart recovery epoch.",
    )
    parser.add_argument(
        "--workflow-id",
        required=True,
        choices=_ALLOWED_WORKFLOW_IDS,
        help="Workflow file to reconcile.",
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
        "--record-id",
        default="",
        help="Optional record identifier filter for inspection modes.",
    )
    parser.add_argument(
        "--actor",
        default="",
        help="Required for --mode restart-recovery-epoch: operator identity.",
    )
    parser.add_argument(
        "--reason",
        default="",
        help="Required for --mode restart-recovery-epoch: audit reason.",
    )
    parser.add_argument(
        "--prior-epoch",
        type=int,
        default=None,
        help="Required for --mode restart-recovery-epoch: expected current recovery epoch.",
    )
    parser.add_argument(
        "--no-late-write-confirmed",
        action="store_true",
        help="Required for --mode restart-recovery-epoch: confirms no late writes can commit.",
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

    repo_input = args.repo or os.environ.get("GITHUB_REPOSITORY", "")
    repo = resolve_github_repo(repo_input) if repo_input else ""

    if args.mode != "dispatch":
        try:
            queue_store = QueueStore(repo=repo)
            CASExhaustionReporter.update_retry_store(triggering_retry, queue_store)
            queue_store.ensure_state_ref()
            trusted_queue_state = queue_store.load()
        except QueueStoreError as exc:
            logger.error("Reconciliation failed: %s", exc)
            return 1
        return _handle_trusted_state_mode(args, queue_store, trusted_queue_state)

    recovery_token: str | None = None
    unresolved_dispatch_pr: int | None = None
    queue_state: QueueState | None = None
    last_persisted_state: QueueState | None = None
    try:
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
        CASExhaustionReporter.update_retry_store(triggering_retry, queue_store)
        queue_store.ensure_state_ref()

        def persist_unreadable_recovery_state(state: QueueState, expected_token: str | None) -> None:
            """Persist a terminal alert for a state whose original read never succeeded.

            Only the initial load-failure path should reach this: there is no prior
            revision-CAS ownership to retain, so a recovery token is the only
            available compare-and-swap anchor for the blind replacement write.
            """
            try:
                if expected_token is None:
                    logger.error("Unable to persist reconciliation recovery: no recovery token is available")
                    return
                queue_store.save_recovery(state, expected_token)
            except (QueueStoreError, RuntimeError) as recovery_error:
                logger.error("Unable to persist reconciliation recovery: %s", recovery_error)

        def persist_readable_recovery_alert(current_state: QueueState, alerted_state: QueueState) -> None:
            """Persist a terminal alert for a state that was read successfully.

            Readability -- not migration_status -- must choose revision-CAS behavior.
            Routing a readable state through save_recovery() would acquire a fresh
            replacement token only after rehydration already ran; if another
            reconciler wrote a newer state during those attempts, that fresh token
            would let this stale terminal snapshot silently replace the winner's
            state. Retaining ownership via the original read's revision avoids that.

            save_alert() (not save()) persists it: the state passed here only ever
            differs from the persisted document by an appended quarantine/record, so
            it must remain persistable even once migration_status reaches "active" --
            where save()'s legacy-digest freeze would otherwise reject it outright and
            silently drop the terminal alert (MigrationRequiredError is a QueueStoreError).
            """
            next_state = alerted_state
            if config.MAX_RETRY_ATTEMPTS <= 0:
                logger.error("Unable to persist reconciliation recovery: no alert retry attempts are configured")
                return
            attempt = 0
            while True:
                try:
                    queue_store.save_alert(next_state, expected_revision=next_state.revision)
                    return
                except ConcurrentModificationError as recovery_error:
                    attempt += 1
                    if attempt >= config.MAX_RETRY_ATTEMPTS:
                        logger.error("Unable to persist reconciliation recovery: %s", recovery_error)
                        return
                    try:
                        winning_state = queue_store.load()
                        next_state = _merge_readable_recovery_alert_state(
                            current_state,
                            alerted_state,
                            winning_state,
                        )
                    except (QueueStoreError, RuntimeError) as merge_error:
                        logger.error("Unable to persist reconciliation recovery: %s", merge_error)
                        return
                except (QueueStoreError, RuntimeError) as recovery_error:
                    if isinstance(recovery_error, StateTooLargeError):
                        # Build the compact replacement and its CAS anchor from next_state, not
                        # the original alerted_state: after a prior CAS conflict, next_state
                        # already carries the merged winning revision. Submitting alerted_state's
                        # stale revision here would make save_compact_recovery() deterministically
                        # conflict instead of persisting the terminal alert.
                        compact_items = {
                            pr_number: item
                            for pr_number, item in next_state.items.items()
                            if item.status
                            in {
                                WorkItemStatus.UNKNOWN,
                                WorkItemStatus.CLAIMED,
                                WorkItemStatus.LEASED,
                                WorkItemStatus.QUARANTINED,
                            }
                        }
                        if unresolved_dispatch_pr is not None and unresolved_dispatch_pr in next_state.items:
                            compact_items[unresolved_dispatch_pr] = next_state.items[unresolved_dispatch_pr]
                        compact_state = replace(
                            next_state,
                            items=compact_items,
                            records=next_state.records[-1:],
                            quarantines=next_state.quarantines[-1:],
                            metric_events=[],
                            pagination_cursor=None,
                            full_scan_complete=False,
                            next_inventory_at=None,
                            inventory_invalidated=True,
                            inventory_scan_started_at=None,
                        )
                        try:
                            queue_store.save_compact_recovery(compact_state, next_state.revision)
                            return
                        except (QueueStoreError, RuntimeError) as compact_error:
                            recovery_error = compact_error
                    logger.error("Unable to persist reconciliation recovery: %s", recovery_error)
                    return

        try:
            queue_state = queue_store.load()
        except QueueStoreError as exc:
            logger.warning("Queue state requires recovery: %s", exc)
            recovery_token = queue_store.recovery_token()
            recovery_seed = QueueState(repo=repo, revision=0, items={}, records=[], quarantines=[])
            try:
                queue_state = rehydrate_state(
                    recovery_seed,
                    lambda: _authoritative_rehydrate_loader(provider, queue_store, recovery_seed, repo),
                )
            except RecoveryExhaustedError as recovery_error:
                persist_unreadable_recovery_state(recovery_error.state, recovery_token)
                return 1
        else:
            if (
                queue_state.last_updated_at is not None
                and (datetime.now(UTC) - queue_state.last_updated_at).total_seconds() > config.MAX_STATE_AGE_SECONDS
            ):
                logger.warning("Queue state is stale; rehydrating before reconciliation")
                current_state = queue_state
                try:
                    queue_state = rehydrate_state(
                        current_state,
                        lambda: _authoritative_rehydrate_loader(provider, queue_store, current_state, repo),
                    )
                except RecoveryExhaustedError as recovery_error:
                    persist_readable_recovery_alert(current_state, recovery_error.state)
                    return 1
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
        last_persisted_state = queue_state
        reclaimed_state = reclaim_leases(queue_state)
        if reclaimed_state != queue_state:  # pragma: no cover - provider-backed persistence path
            queue_state = queue_store.save(reclaimed_state, expected_revision=queue_state.revision)
            last_persisted_state = queue_state
        dispatch_now = datetime.now(UTC)
        due_work = select_due_work(queue_state, dispatch_now)
        eligibility_checker = _build_live_eligibility_checker(provider) if due_work else None
        dispatch_result = dispatch_due_work(
            queue_state,
            eligibility_checker=eligibility_checker,
            preflight_checker=_build_live_preflight_checker(provider) if due_work else None,
            now=dispatch_now,
            store=queue_store,
            operation_log=operation_log,
            operation_identity=os.environ.get("AGDT_OPERATION_ID") or None,
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
        queue_state = metric_state
        if dispatch_result.lease is None:
            saved_metric_state = queue_store.save(metric_state, expected_revision=metric_state.revision)
            last_persisted_state = saved_metric_state if isinstance(saved_metric_state, QueueState) else metric_state
        else:
            dispatch_result = replace(dispatch_result, state=metric_state)
        completion_persisted = False
        if dispatch_result.lease is not None:  # pragma: no cover - provider-backed dispatch path
            try:
                head_sha = provider.get_pr_metadata(dispatch_result.lease.pr_number).head_sha
                if not isinstance(head_sha, str) or not head_sha.strip():
                    raise RuntimeError(f"PR #{dispatch_result.lease.pr_number} has no head SHA")
                # Fence the outcome before invoking the provider: the workflow request may be
                # accepted even when the provider reports an ambiguous response error.
                unresolved_dispatch_pr = dispatch_result.lease.pr_number
                provider.dispatch_workflow(
                    args.workflow_id,
                    {
                        "pr_number": str(dispatch_result.lease.pr_number),
                        "head_sha": head_sha,
                        "operation_id": dispatch_result.operation_id,
                    },
                )
                dispatch_state = dispatch_result.state or queue_state
                # Promote the durably persisted, leased state to the recovery baseline now so
                # that any later persistence failure recovers from a snapshot that already
                # reflects this dispatch instead of discarding it as if it never happened.
                queue_state = dispatch_state
                last_persisted_state = dispatch_state
                if dispatch_result.lease.pr_number in dispatch_state.items:
                    completed = complete_work_item(
                        dispatch_state,
                        dispatch_result.lease,
                        dispatch_result.operation_id,
                        dispatch_state.recovery_epoch,
                    )
                    saved_completed_state = queue_store.save(completed, expected_revision=dispatch_state.revision)
                    last_persisted_state = (
                        saved_completed_state if isinstance(saved_completed_state, QueueState) else completed
                    )
                    # The completion state is now durably persisted, so this PR's outcome is no
                    # longer unresolved. Clear the flag before the operation-log append below: an
                    # I/O failure in that append must not leave a durably completed item fenced
                    # as if its dispatch outcome were still unknown. `completion_persisted` records
                    # the same fact for the except-block below, which must not release a lease
                    # whose completion is already durable.
                    unresolved_dispatch_pr = None
                    completion_persisted = True
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
                if completion_persisted:
                    failure_status = "completed"
                elif unresolved_dispatch_pr is not None:
                    failure_status = "pending"
                else:
                    failure_status = "pre_dispatch_failed"
                operation_log.append(
                    OperationLogRecord(
                        operation_id=dispatch_result.operation_id,
                        run_id=operation_log.run_id,
                        tool_name="reconciliation.dispatch",
                        node_name="reconcile_command",
                        status=failure_status,
                    )
                )
                if unresolved_dispatch_pr is None and not completion_persisted:
                    failed = _release_dispatch_lease(dispatch_result.state or queue_state, dispatch_result.lease)
                    queue_store.save(failed, expected_revision=(dispatch_result.state or queue_state).revision)
                raise
    except QueueTransitionRetryExhaustedError as exc:
        return CASExhaustionReporter.transition_retry_result(queue_store, args, exc, triggering_retry=triggering_retry)
    except DispatchRetryExhaustedError as exc:
        return CASExhaustionReporter.dispatch_retry_result(queue_store, args, exc, triggering_retry=triggering_retry)
    except ConcurrentModificationError as exc:
        if unresolved_dispatch_pr is not None:
            logger.error("Reconciliation queue state changed after dispatch; outcome remains unresolved: %s", exc)
            # The provider dispatch already happened; a CAS conflict on the completion save
            # must not be treated as "nothing happened" or the durable lease can be discarded
            # and the same work dispatched again. Reload the winning state and durably fence
            # this PR through a fresh revision-CAS update rather than overwriting the conflict.
            _fence_unknown_dispatch_outcome(
                queue_store,
                repo,
                unresolved_dispatch_pr,
                (
                    "queue-store revision changed concurrently after provider dispatch for"
                    f" pr_number={unresolved_dispatch_pr}: {exc}"
                ),
                lease=dispatch_result.lease,
            )
        else:
            raise CASExhaustionReporter.retry_after_conflict(
                exc, queue_store, args, last_persisted_state or queue_state
            ) from exc
        return 1
    except QueueStoreError as exc:
        logger.error("Reconciliation queue persistence failed: %s", exc)
        if queue_state is not None:
            current_state = last_persisted_state or queue_state
            try:
                recovered_state = rehydrate_state(
                    current_state,
                    lambda: _authoritative_rehydrate_loader(
                        provider,
                        queue_store,
                        current_state,
                        repo,
                        unresolved_dispatch_pr=unresolved_dispatch_pr,
                    ),
                )
            except RecoveryExhaustedError as recovery_error:
                terminal_state = recovery_error.state
                if unresolved_dispatch_pr is not None:
                    lease = dispatch_result.lease
                    terminal_state = _append_unknown_outcome_alert(
                        terminal_state,
                        repo=repo,
                        unresolved_dispatch_pr=unresolved_dispatch_pr,
                        message=(
                            f"recovery exhausted after provider dispatch for pr_number={unresolved_dispatch_pr}: {exc}"
                        ),
                        claim_id=lease.claim_id if lease is not None else "",
                        lease_id=lease.lease_id if lease is not None else "",
                        operation_id=lease.operation_id if lease is not None else "",
                    )
                persist_readable_recovery_alert(current_state, terminal_state)
            except QueueStoreError as recovery_error:
                logger.error("Reconciliation recovery failed: %s", recovery_error)
            else:
                message = f"queue-store persistence failed: {exc}"
                if unresolved_dispatch_pr is not None:
                    message = (
                        f"queue-store persistence failed after provider dispatch for"
                        f" pr_number={unresolved_dispatch_pr}: {exc}"
                    )
                alerted_state = _append_unknown_outcome_alert(
                    recovered_state,
                    repo=repo,
                    unresolved_dispatch_pr=unresolved_dispatch_pr,
                    message=message,
                )
                # Successful rehydration already persisted the rebuilt state through
                # store.save_rehydration() inside _authoritative_rehydrate_loader, which advanced the
                # backing-store revision. The document is therefore readable (not corrupt)
                # regardless of its migration_status, so the alert is persisted through the
                # same revision-CAS path as any other readable-state terminal alert.
                persist_readable_recovery_alert(recovered_state, alerted_state)
        return 1
    except (NotImplementedError, RuntimeError) as exc:
        logger.error("Reconciliation failed: %s", exc)
        if unresolved_dispatch_pr is not None:
            # A non-storage failure after the provider dispatch already happened must not
            # silently drop the lease: the item would otherwise sit leased until reclaimed
            # and dispatched again, duplicating work whose outcome is genuinely unknown.
            _fence_unknown_dispatch_outcome(
                queue_store,
                repo,
                unresolved_dispatch_pr,
                f"reconciliation failed after provider dispatch for pr_number={unresolved_dispatch_pr}: {exc}",
                lease=dispatch_result.lease,
            )
        return 1
    except Exception as exc:  # noqa: BLE001
        return handle_reconciliation_error(
            exc,
            json_output=args.json_output,
            repo=repo,
            dispatch_context=(queue_store, unresolved_dispatch_pr, dispatch_result.lease)
            if unresolved_dispatch_pr is not None
            else None,
            fence_unknown_dispatch_outcome=_fence_unknown_dispatch_outcome,
        )

    action, message = summarize_scan(_summarize_dispatch_result(dispatch_result), eligibility_checker)
    if args.json_output:
        output = {
            "action": action.value,
            "message": message,
            "lease_id": dispatch_result.lease.lease_id if dispatch_result.lease else None,
            "operation_id": dispatch_result.operation_id or None,
            "pr_number": dispatch_result.lease.pr_number if dispatch_result.lease else None,
            **(eligibility_checker.diagnostics() if eligibility_checker else {}),
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
    fenced_pr_number: int | None = None,
    authoritative: bool = False,
) -> QueueState:
    """Observe the bounded provider inventory and merge changed PRs into the queue.

    ``authoritative`` selects the persistence channel for the rebuilt baseline: an
    authoritative rehydration (``fenced_pr_number`` set from
    ``_authoritative_rehydrate_loader``) rebuilds the entire legacy inventory, which the
    ordinary ``store.save()`` legacy-digest freeze always rejects once ``migration_status``
    reaches ``"active"``. ``store.save_rehydration()`` is the narrowly validated channel for
    that specific rebuild; the ordinary per-cycle refresh keeps using ``store.save()``.
    """
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
        attributions = {}
        for pr_number in observed:
            existing = state.items.get(pr_number)
            watermark = existing.observation_watermark if existing else ""
            attributions[pr_number] = provider.get_pr_copilot_attribution(pr_number, observation_watermark=watermark)

        def merge_inventory(current: QueueState) -> QueueState:
            merged = (
                rebase_rehydration(current, state, unresolved_dispatch_pr=fenced_pr_number)
                if authoritative
                else current
            )
            for pr_number, metadata in observed.items():
                existing = current.items.get(pr_number)
                attribution = attributions[pr_number]
                merged = _merge_observed_pull_request(
                    merged,
                    metadata=metadata,
                    eligible=pr_number != fenced_pr_number,
                    should_queue=existing is None or bool(attribution.get("review")) or bool(attribution.get("push")),
                    observation_watermark=(
                        str(attribution["observation_watermark"])
                        if "observation_watermark" in attribution
                        else (existing.observation_watermark if existing else metadata.head_sha)
                    ),
                    now=now,
                )
            # A concurrent scan owns its cursor/cache progress. Merge only observations
            # into that winner rather than overwriting it with our older scan position.
            if any(
                getattr(current, key) != getattr(state, key)
                for key in (
                    "pagination_cursor",
                    "full_scan_complete",
                    "next_inventory_at",
                    "inventory_invalidated",
                    "inventory_scan_started_at",
                )
            ):
                return merged
            items = merged.items
            if cursor is None and scan_started_at is not None and current.revision == state.revision:
                items = _retire_absent_work_items_after_scan(
                    dict(items), observed_numbers=eligible_numbers, scan_started_at=scan_started_at, now=now
                )
            next_scan_started_at = scan_started_at
            if cursor is None:
                next_scan_started_at = None
            elif next_scan_started_at is None and (cursor != initial_cursor or bool(observed)):
                next_scan_started_at = now
            return replace(
                merged,
                items=items,
                pagination_cursor=cursor,
                full_scan_complete=cursor is None,
                metric_events=(
                    [
                        *current.metric_events,
                        create_metric_event(
                            MetricEventType.DISCOVERY,
                            repo,
                            {"observed_count": len(observed), "pages": config.MAX_PAGINATION_PAGES_PER_RUN},
                        ),
                    ][-_MAX_METRIC_EVENTS:]
                    if observed
                    else current.metric_events
                ),
                next_inventory_at=(
                    now + timedelta(minutes=config.RECONCILIATION_SCHEDULE_INTERVAL_MINUTES) if cursor is None else None
                ),
                inventory_invalidated=cursor is not None,
                inventory_scan_started_at=next_scan_started_at,
            )

    except (NotImplementedError, AttributeError, KeyError, TypeError, ValueError, RuntimeError) as exc:
        logger.warning("Inventory observation unavailable: %s", exc)
        return state
    return retry_queue_transition(
        store,
        state,
        merge_inventory,
        authoritative=authoritative,
        triggering_pr=(trusted_pr_number, trusted_head_sha),
    )


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
    *,
    unresolved_dispatch_pr: int | None = None,
) -> QueueState:
    """Rebuild queue state from a forced full provider inventory scan."""
    # Preserve every in-flight item -- UNKNOWN (fenced), CLAIMED, and LEASED -- in the
    # baseline. Dropping a claimed/leased item here would make _refresh_inventory()'s merge
    # treat the still-open PR as unseen and recreate it as QUEUED, erasing its durable lease
    # before reclaim_leases() can assess expiry and letting the same work dispatch again
    # while the original operation may still be running.
    baseline_items: dict[int, WorkItem] = {
        pr_number: item
        for pr_number, item in state.items.items()
        if item.status
        in {
            WorkItemStatus.UNKNOWN,
            WorkItemStatus.CLAIMED,
            WorkItemStatus.LEASED,
            WorkItemStatus.QUARANTINED,
        }
    }
    if unresolved_dispatch_pr is not None:
        fenced_state = _fence_unknown_outcome_item(state, unresolved_dispatch_pr)
        unresolved_item = fenced_state.items.get(unresolved_dispatch_pr)
        if unresolved_item is not None:
            baseline_items[unresolved_dispatch_pr] = unresolved_item
    # Advance the recovery epoch and mark quarantines rehydrated *before* the inventory
    # refresh below persists its baseline. rehydrate_state() applies the same transition
    # to the value this loader returns, but _refresh_inventory() saves its own baseline
    # first (see below); the baseline must therefore match the state returned by
    # rehydrate_state() for both quarantined and stale non-quarantined loads.
    recovery_epoch = state.recovery_epoch + 1
    quarantines = [replace(record, rehydration_attempted=True) for record in state.quarantines]
    baseline = replace(
        state,
        items=baseline_items,
        pagination_cursor=None,
        full_scan_complete=False,
        next_inventory_at=None,
        inventory_invalidated=True,
        recovery_epoch=recovery_epoch,
        quarantines=quarantines,
    )
    refreshed = _refresh_inventory(
        provider,
        store,
        baseline,
        repo,
        invalidate_inventory=True,
        fenced_pr_number=unresolved_dispatch_pr,
        authoritative=True,
    )
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
    except (NotImplementedError, AttributeError, KeyError, TypeError, ValueError, RuntimeError) as exc:
        logger.warning("Trusted-event observation unavailable for PR #%s: %s", pr_number, exc)
        invalidated_state = replace(state, inventory_invalidated=True)
        return store.save(invalidated_state, expected_revision=state.revision) if invalidated_state != state else state

    def merge_observation(current: QueueState) -> QueueState:
        existing = current.items.get(pr_number)
        observed = _merge_observed_pull_request(
            current,
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
        return replace(observed, inventory_invalidated=True) if observed != current else current

    return retry_queue_transition(store, state, merge_observation, triggering_pr=(pr_number, trusted_head_sha))


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
    if existing is not None and existing.last_observed_at is not None and existing.last_observed_at >= now:
        return state
    # An item held at WorkItemStatus.UNKNOWN carries a persisted, unresolved-dispatch outcome
    # (see _fence_unknown_outcome_item): a trusted-event observation must not silently clear
    # that fence back to eligible just because the PR is still readable.
    held = existing is not None and existing.status == WorkItemStatus.UNKNOWN
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
        eligibility="ineligible" if held else ("eligible" if eligible else "ineligible"),
        due_at=None if held or not eligible else (now if should_queue else (existing.due_at if existing else None)),
        status=WorkItemStatus.QUEUED if reset_completed or existing is None else existing.status,
        claimed_at=None if reset_completed else (existing.claimed_at if existing else None),
        claim_expires_at=None if reset_completed else (existing.claim_expires_at if existing else None),
        claim_id="" if reset_completed else (existing.claim_id if existing else ""),
        lease_id="" if reset_completed else (existing.lease_id if existing else ""),
        lease_expires_at=None if reset_completed else (existing.lease_expires_at if existing else None),
        operation_id=existing.operation_id if existing else "",
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


def _build_live_preflight_checker(provider: CIPlatformProvider):
    """Build a checker that confirms the PR is still readable and open-relevant."""

    def _check(item: WorkItem) -> bool:
        metadata = provider.get_pr_metadata(item.pr_number)
        return metadata.number == item.pr_number and metadata.head_sha == item.change_id

    return _check


def _fence_unknown_outcome_item(
    state: QueueState,
    pr_number: int | None,
    *,
    claim_id: str = "",
    lease_id: str = "",
    operation_id: str = "",
) -> QueueState:
    """Mark an unresolved-dispatch work item ineligible so it cannot be dispatched again.

    Recording an unknown outcome as a ``ReconciliationRecord`` alone does not stop
    ``select_due_work``/``dispatch_due_work`` from picking the same item back up on a
    later cycle. Fencing the item here, in addition to the alert record, closes that
    duplicate-dispatch window.

    Marking ``eligibility`` alone is not durable: the very next ordinary
    ``_refresh_inventory``/``_merge_observed_pull_request`` cycle resets every observed
    item back to ``eligibility="eligible"`` unless it is told otherwise, and
    ``reclaim_expired`` would then be free to move the item back to
    ``WorkItemStatus.QUEUED`` once its lease expires. Holding ``status`` at
    ``WorkItemStatus.UNKNOWN`` closes that window: ``select_due_work`` never dispatches a
    non-``QUEUED`` item, ``reclaim_expired`` never reclaims one, and later observation
    cycles recognize the held status and refuse to clear the fence on their own. Only an
    operator (or another explicit resolution step) that changes the status away from
    ``UNKNOWN`` can put the item back in play.
    """
    if pr_number is None:
        return state
    item = state.items.get(pr_number)
    if item is None or item.status == WorkItemStatus.UNKNOWN:
        return state
    if claim_id or lease_id or operation_id:
        if (
            item.status not in {WorkItemStatus.CLAIMED, WorkItemStatus.LEASED}
            or item.claim_id != claim_id
            or item.lease_id != lease_id
            or item.operation_id != operation_id
            or item.operation_status is not OperationStatus.ACTIVE
        ):
            return state
    if item.status == WorkItemStatus.COMPLETED:
        return state
    return replace(
        state,
        items={
            **state.items,
            pr_number: replace(item, eligibility="ineligible", due_at=None, status=WorkItemStatus.UNKNOWN),
        },
    )


def _append_unknown_outcome_alert(
    state: QueueState,
    *,
    repo: str,
    unresolved_dispatch_pr: int | None,
    message: str,
    claim_id: str = "",
    lease_id: str = "",
    operation_id: str = "",
) -> QueueState:
    """Fence an unresolved dispatch PR and append a terminal alert recording its outcome."""
    fenced = _fence_unknown_outcome_item(
        state,
        unresolved_dispatch_pr,
        claim_id=claim_id,
        lease_id=lease_id,
        operation_id=operation_id,
    )
    return replace(
        fenced,
        records=[
            *fenced.records,
            ReconciliationRecord(
                record_id=str(uuid4()),
                repo=repo,
                run_id="recovery",
                started_at=datetime.now(UTC),
                completed_at=datetime.now(UTC),
                provider_status="alertable",
                message=message,
                unknown_outcomes=((unresolved_dispatch_pr,) if unresolved_dispatch_pr is not None else ()),
            ),
        ],
    )


def _merge_readable_recovery_alert_state(
    current_state: QueueState,
    alerted_state: QueueState,
    winning_state: QueueState,
) -> QueueState:
    """Reapply a readable-state alert delta onto the latest winning queue state."""
    if alerted_state.records[: len(current_state.records)] != current_state.records:
        raise RuntimeError("readable recovery alert rewrote existing records")
    if set(alerted_state.items) != set(current_state.items):
        raise RuntimeError("readable recovery alert changed the item set")
    appended_quarantines = alerted_state.quarantines[len(current_state.quarantines) :]
    recovery_epoch_advanced = alerted_state.recovery_epoch == current_state.recovery_epoch + 1
    if recovery_epoch_advanced:
        if len(alerted_state.quarantines) != len(current_state.quarantines):
            raise RuntimeError("epoch-advancing readable recovery alert must not append quarantines")
        if not all(
            replacement.rehydration_attempted
            and replace(replacement, rehydration_attempted=original.rehydration_attempted) == original
            for original, replacement in zip(current_state.quarantines, alerted_state.quarantines, strict=True)
        ):
            raise RuntimeError("epoch-advancing readable recovery alert must mark quarantines rehydrated")
    elif alerted_state.quarantines[: len(current_state.quarantines)] != current_state.quarantines:
        raise RuntimeError("readable recovery alert rewrote existing quarantines")

    merged_items = dict(winning_state.items)
    for pr_number, current_item in current_state.items.items():
        if alerted_state.items[pr_number] == current_item:
            continue
        winning_item = merged_items.get(pr_number)
        if (
            winning_item is not None
            and current_item.status in {WorkItemStatus.CLAIMED, WorkItemStatus.LEASED}
            and winning_item.status in {WorkItemStatus.CLAIMED, WorkItemStatus.LEASED}
            and winning_item.claim_id == current_item.claim_id
            and winning_item.lease_id == current_item.lease_id
            and winning_item.operation_id == current_item.operation_id
            and winning_item.operation_status is OperationStatus.ACTIVE
        ):
            merged_items[pr_number] = replace(
                winning_item, eligibility="ineligible", due_at=None, status=WorkItemStatus.UNKNOWN
            )

    if recovery_epoch_advanced:
        if len(winning_state.quarantines) != len(current_state.quarantines):
            raise RuntimeError("queue quarantines changed during readable recovery alert retry")
        if not all(
            replace(winning, rehydration_attempted=current.rehydration_attempted) == current
            for current, winning in zip(current_state.quarantines, winning_state.quarantines, strict=True)
        ):
            raise RuntimeError("queue quarantines changed during readable recovery alert retry")
        merged_quarantines = [replace(record, rehydration_attempted=True) for record in winning_state.quarantines]
        if winning_state.recovery_epoch == current_state.recovery_epoch:
            merged_recovery_epoch = winning_state.recovery_epoch + 1
        elif winning_state.recovery_epoch == alerted_state.recovery_epoch:
            merged_recovery_epoch = winning_state.recovery_epoch
        else:
            raise RuntimeError("queue recovery epoch changed during readable recovery alert retry")
    else:
        merged_quarantines = [*winning_state.quarantines, *appended_quarantines]
        merged_recovery_epoch = winning_state.recovery_epoch

    return replace(
        winning_state,
        items=merged_items,
        records=[*winning_state.records, *alerted_state.records[len(current_state.records) :]],
        quarantines=merged_quarantines,
        recovery_epoch=merged_recovery_epoch,
    )


def _fence_unknown_dispatch_outcome(
    queue_store: QueueStore,
    repo: str,
    unresolved_dispatch_pr: int,
    message: str,
    *,
    lease: Lease | None = None,
) -> bool:
    """Durably alert an unresolved post-dispatch outcome and verify that it is fenced.

    Reloads the winning state, uses a revision-CAS save, and retries concurrent
    conflicts within a bounded budget. ``save_alert`` supports active queues; a
    completed item or newer owner is preserved when a lease is supplied.

    Returns True only after read-back confirms the item is held in ``UNKNOWN``.
    """
    for attempt in range(config.MAX_RETRY_ATTEMPTS):  # pragma: no branch - every branch inside always returns
        try:
            winning_state = queue_store.load()
        except (QueueStoreError, RuntimeError) as load_error:
            logger.error("Unable to record unknown dispatch outcome: %s", load_error)
            return False
        alerted_state = _append_unknown_outcome_alert(
            winning_state,
            repo=repo,
            unresolved_dispatch_pr=unresolved_dispatch_pr,
            message=message,
            claim_id=lease.claim_id if lease is not None else "",
            lease_id=lease.lease_id if lease is not None else "",
            operation_id=lease.operation_id if lease is not None else "",
        )
        try:
            queue_store.save_alert(alerted_state, expected_revision=winning_state.revision)
        except ConcurrentModificationError:
            if attempt + 1 >= config.MAX_RETRY_ATTEMPTS:
                logger.error(
                    "Unable to persist unknown dispatch outcome for pr_number=%s after %s attempts:"
                    " queue state kept changing concurrently",
                    unresolved_dispatch_pr,
                    config.MAX_RETRY_ATTEMPTS,
                )
                return False
            continue
        except (QueueStoreError, RuntimeError) as save_error:
            logger.error("Unable to persist unknown dispatch outcome: %s", save_error)
            return False
        try:
            persisted_state = queue_store.load()
        except (QueueStoreError, RuntimeError) as verification_error:
            logger.error("Unable to verify unknown dispatch outcome fence: %s", verification_error)
            return False
        persisted_item = persisted_state.items.get(unresolved_dispatch_pr)
        if persisted_item is None or persisted_item.status is not WorkItemStatus.UNKNOWN:
            logger.error(
                "Persisted alert does not fence unknown dispatch for pr_number=%s (item status=%s)",
                unresolved_dispatch_pr,
                persisted_item.status.value if persisted_item is not None else "missing",
            )
            return False
        return True
    logger.error("Unable to persist unknown dispatch outcome: no fencing retry attempts are configured")
    return False


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


def _handle_trusted_state_mode(args: argparse.Namespace, queue_store: QueueStore, queue_state: QueueState) -> int:
    if args.mode == "inspect-inventory":
        payload = _build_inventory_inspection(queue_state, record_id=args.record_id)
        _emit_mode_payload(args, payload)
        return 0
    if args.mode == "inspect-ledger":
        payload = _build_ledger_inspection(queue_state, record_id=args.record_id)
        _emit_mode_payload(args, payload)
        return 0
    if args.mode == "inspect-runs":
        payload = _build_run_inspection(queue_state, record_id=args.record_id)
        _emit_mode_payload(args, payload)
        return 0
    if args.mode == "restart-recovery-epoch":
        return _restart_recovery_epoch_mode(args, queue_store, queue_state)
    logger.error("Unknown reconciliation mode: %s", args.mode)
    return 1


def _emit_mode_payload(args: argparse.Namespace, payload: dict[str, object]) -> None:
    if args.json_output:
        print(json.dumps(payload, indent=2))
        return
    print(json.dumps(payload, indent=2))


def _build_inventory_inspection(state: QueueState, *, record_id: str = "") -> dict[str, object]:
    records: list[dict[str, object]] = []
    now = datetime.now(UTC)
    for pr_number in sorted(state.items):
        item = state.items[pr_number]
        item_record_id = f"{item.repo}#{item.pr_number}"
        if record_id and item_record_id != record_id:
            continue
        freshness = "unknown"
        if item.last_observed_at is not None:
            age_seconds = (now - item.last_observed_at).total_seconds()
            freshness = "stale" if age_seconds > config.TRUSTED_OBSERVATION_FRESHNESS_MINUTES * 60 else "fresh"
        records.append(
            {
                "record_id": item_record_id,
                "pr_number": item.pr_number,
                "repo": item.repo,
                "status": item.status.value,
                "scope_classification": "active" if item.eligibility == "eligible" else "non_actionable_ineligible",
                "eligibility": item.eligibility,
                "observation_freshness_state": freshness,
                "retry_reason": "none" if item.retry_count == 0 else "retry_attempted",
                "recovery_state": "active" if state.recovery_epoch == 0 else "epoch_restartable",
                "recovery_epoch": state.recovery_epoch,
                "recovery_attempt_count": item.retry_count,
                "exhaustion_metadata": (
                    "exhausted" if item.retry_count >= config.MAX_RETRY_ATTEMPTS else "not_exhausted"
                ),
                "finality_metadata": "terminal" if item.status == WorkItemStatus.COMPLETED else "non_terminal",
                "next_due_at_utc_z": _format_datetime(item.due_at),
                "last_observed_at_utc_z": _format_datetime(item.last_observed_at),
                "observation_watermark": item.observation_watermark,
            }
        )
    return {"mode": "inspect-inventory", "recovery_epoch": state.recovery_epoch, "records": records}


def _build_ledger_inspection(state: QueueState, *, record_id: str = "") -> dict[str, object]:
    ledgers: list[dict[str, object]] = []
    for pr_number in sorted(state.items):
        item = state.items[pr_number]
        item_record_id = f"{item.repo}#{item.pr_number}"
        if record_id and item_record_id != record_id:
            continue
        ledgers.append(
            {
                "record_id": item_record_id,
                "current_work_state": item.status.value,
                "unfinished_decision_context": item.pending_change_id,
                "action_eligibility": item.eligibility,
                "history": {
                    "retry_count": item.retry_count,
                    "has_claim": bool(item.claim_id),
                    "has_lease": bool(item.lease_id),
                    "operation_status": item.operation_status.value,
                },
                "supersession": {
                    "pending_change_id": item.pending_change_id,
                    "claimed_at_utc_z": _format_datetime(item.claimed_at),
                    "lease_expires_at_utc_z": _format_datetime(item.lease_expires_at),
                },
                "invalidations": [
                    record.message
                    for record in state.records
                    if str(item.pr_number) in record.message and "invalidat" in record.message.lower()
                ],
            }
        )
    return {"mode": "inspect-ledger", "recovery_epoch": state.recovery_epoch, "ledgers": ledgers}


def _build_run_inspection(state: QueueState, *, record_id: str = "") -> dict[str, object]:
    runs = [
        {
            "record_id": record.record_id,
            "run_id": record.run_id,
            "provider_status": record.provider_status,
            "message": record.message,
            "started_at_utc_z": _format_datetime(record.started_at),
            "completed_at_utc_z": _format_datetime(record.completed_at),
            "cursor_progress": record.cursor_progress,
            "unknown_outcomes": list(record.unknown_outcomes),
            "run_duration_seconds": record.run_duration_seconds,
        }
        for record in state.records
        if not record_id or record.record_id == record_id
    ]
    return {"mode": "inspect-runs", "recovery_epoch": state.recovery_epoch, "runs": runs}


def _restart_recovery_epoch_mode(args: argparse.Namespace, queue_store: QueueStore, state: QueueState) -> int:
    if not args.actor.strip():
        logger.error("restart-recovery-epoch requires --actor")
        return 1
    authenticated_actor = os.environ.get("GITHUB_ACTOR", "").strip()
    if not authenticated_actor:
        logger.error("restart-recovery-epoch requires an authenticated GITHUB_ACTOR")
        return 1
    if args.actor.strip() != authenticated_actor:
        logger.error("restart-recovery-epoch actor does not match authenticated GITHUB_ACTOR")
        return 1
    if not args.reason.strip():
        logger.error("restart-recovery-epoch requires --reason")
        return 1
    if args.prior_epoch is None:
        logger.error("restart-recovery-epoch requires --prior-epoch")
        return 1
    if not args.no_late_write_confirmed:
        logger.error("restart-recovery-epoch requires --no-late-write-confirmed")
        return 1
    if args.prior_epoch != state.recovery_epoch:
        logger.error("prior epoch mismatch: expected %s, got %s", state.recovery_epoch, args.prior_epoch)
        return 1
    active_items = [
        item.pr_number
        for item in state.items.values()
        if item.status in {WorkItemStatus.CLAIMED, WorkItemStatus.LEASED}
    ]
    if active_items:
        logger.error("cannot restart recovery epoch while active work exists: %s", active_items)
        return 1
    now = datetime.now(UTC)
    updated = replace(
        state,
        recovery_epoch=state.recovery_epoch + 1,
        records=[
            *state.records,
            ReconciliationRecord(
                record_id=str(uuid4()),
                repo=state.repo,
                run_id="manual-recovery-epoch-restart",
                started_at=now,
                completed_at=now,
                provider_status="manual_recovery_epoch_restart",
                message=(
                    f"recovery epoch restarted by {args.actor}; reason={args.reason}; "
                    f"prior_epoch={args.prior_epoch}; no_late_write=true"
                ),
                unknown_outcomes=(),
            ),
        ],
    )
    try:
        saved = queue_store.save(updated, expected_revision=state.revision)
    except QueueStoreError as exc:
        logger.error("Reconciliation failed: %s", exc)
        return 1
    payload = {
        "mode": "restart-recovery-epoch",
        "previous_recovery_epoch": state.recovery_epoch,
        "recovery_epoch": saved.recovery_epoch,
        "actor": args.actor,
        "reason": args.reason,
    }
    _emit_mode_payload(args, payload)
    return 0


def _format_datetime(value: datetime | None) -> str:
    if value is None:
        return ""
    return value.astimezone(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
