"""Cross-task verified delivery receipt lifecycle."""

import hashlib
import json
from dataclasses import replace
from threading import Barrier, Lock
from unittest.mock import patch

from agentic_devtools.cli.ci.initial_delivery_claims import InitialDeliveryClaims
from agentic_devtools.cli.ci.models import PRMetadata
from agentic_devtools.cli.ci.pipeline.actions.retry_failed_session import RetryFailedSessionAction
from agentic_devtools.cli.ci.pipeline.delivery import InitialDeliveryEvidence, InitialDeliveryOutcome
from agentic_devtools.cli.ci.pipeline.models import ActionDecision
from agentic_devtools.cli.ci.pipeline.session_detector import SessionOutcome, SessionState
from agentic_devtools.cli.ci.pipeline.snapshot_models import DerivedState, PRStateSnapshot
from tests.workflows.test_initial_delivery_recovery import (
    HEAD,
    RECOVERY,
    RETRY,
    _assert_ordinary_retry,
    _assert_same_head_delivery_reuse,
    _assert_single_initial_recovery,
    _provider,
)


def test_concurrent_runs_restart_and_recovered_handoff():
    documents = {}
    lock = Lock()
    barrier = Barrier(4)
    evidence = InitialDeliveryEvidence(InitialDeliveryOutcome.NO_DELIVERY, "initial-task", HEAD, HEAD)
    snapshot = PRStateSnapshot(
        pr_number=12,
        head_sha=HEAD,
        head_branch="copilot/feature",
        base_branch="main",
        head_repo_full_name="org/repo",
        base_repo_full_name="org/repo",
        initial_delivery=evidence,
    )
    metadata = PRMetadata(
        12,
        "Task",
        snapshot.head_branch,
        HEAD,
        "main",
        head_repo_full_name="org/repo",
        base_repo_full_name="org/repo",
        changed_files=0,
    )
    provider = _provider(metadata)
    state = [SessionState(SessionOutcome.FINISHED, task_id="initial-task")]

    def api(endpoint, *, method="GET", body=None):
        path = endpoint.split("?")[0]
        with lock:
            if method == "PUT":
                current = documents.get(path)
                current_sha = hashlib.sha256(current.encode()).hexdigest() if current is not None else None
                if body.get("sha") != current_sha:
                    raise RuntimeError("HTTP 409 blob SHA conflict")
                documents[path] = body["content"]
                return "{}"
            if path not in documents:
                raise RuntimeError("HTTP 404")
            return json.dumps(
                {
                    "content": documents[path],
                    "sha": hashlib.sha256(documents[path].encode()).hexdigest(),
                }
            )

    def run(concurrent=False):
        action = RetryFailedSessionAction(provider)
        derived = DerivedState(snapshot)
        result = action.evaluate(snapshot, derived)
        if concurrent:
            barrier.wait(timeout=10)
        if result.decision is ActionDecision.EXECUTE:
            result = action.execute(provider, snapshot, derived)
        return result

    with (
        patch.object(InitialDeliveryClaims, "_api", side_effect=api),
        patch(f"{RETRY}.get_latest_session_state", side_effect=lambda *a, **kw: state[0]),
        patch(f"{RECOVERY}.get_latest_session_state", side_effect=lambda *a, **kw: state[0]),
        patch(f"{RECOVERY}.is_copilot_session_active_via_agent_task", return_value=False),
    ):
        _assert_single_initial_recovery(run, provider, documents)

        # A complete live recovered head can return to normal gates, never direct CCR.
        new_head = "b" * 40
        state[0] = SessionState(SessionOutcome.FINISHED, task_id="recovery-task")
        delivery = replace(evidence, outcome=InitialDeliveryOutcome.DELIVERED, head_sha=new_head)
        snapshot = replace(snapshot, head_sha=new_head, initial_delivery=delivery)
        provider.get_pr_metadata.return_value = replace(metadata, head_sha=new_head, changed_files=1)
        provider.list_pr_files_complete.return_value = ["implementation.py"]
        assert run().decision is ActionDecision.SKIP
        provider.request_copilot_review.assert_not_called()

        _assert_same_head_delivery_reuse(run, provider, state)

        next_head = "c" * 40
        state[0] = SessionState(SessionOutcome.FINISHED, task_id="repair-task")
        delivery = replace(delivery, head_sha=next_head)
        snapshot = replace(snapshot, head_sha=next_head, initial_delivery=delivery)
        provider.get_pr_metadata.return_value = replace(metadata, head_sha=next_head, changed_files=1)
        assert run().decision is ActionDecision.SKIP
        state[0] = SessionState(SessionOutcome.FAILED, task_id="unrelated-task", failure_event_id=123)
        _assert_ordinary_retry(provider, snapshot, documents)
