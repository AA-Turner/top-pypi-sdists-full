"""Run, telemetry and checkpoint client."""

from __future__ import annotations

import asyncio
import json
from functools import partial
from collections.abc import Generator, Sequence
from urllib.parse import urlencode
from typing import ParamSpec, TypeVar

from labqoat._generated.checkpoint import Checkpoint
from labqoat._generated.run import Run
from labqoat._generated.run_placement import RunPlacement
from labqoat._generated.run_stream_event import RunStreamEvent
from labqoat._generated.transport import Transport
from labqoat.base_client import BaseClient
from labqoat.errors.api_error import ApiError
from labqoat.json_document import JsonDocument
from labqoat.sse_client import SseClient
from labqoat.compute.function import Function
from labqoat.compute.function_signature import FunctionSignature
from labqoat.compute.submission import Submission
from labqoat.compute.run_options import RunOptions
from labqoat.compute.upload_memo import UploadMemo
from labqoat.compute.prepared_submission import PreparedSubmission
from labqoat.authoring.resources import Resources
from labqoat.runs.run_handle import RunHandle
from labqoat.compute.checkpoint_identity import CheckpointIdentity
from labqoat.references.checkpoint_ref import CheckpointRef
from labqoat.runs.recovery_client import RecoveryClient
from labqoat.runs.workflow_recovery_client import WorkflowRecoveryClient
from labqoat.runs.fork_client import ForkClient
from labqoat.runs.budget_history_client import BudgetHistoryClient
from labqoat._generated.fork_lineage import ForkLineage
from labqoat._generated.fork_request import ForkRequest
from labqoat.runs.recovery_handle import RecoveryHandle
from labqoat._generated.recovery_discovery import RecoveryDiscovery
from labqoat._generated.recovery_request import RecoveryRequest
from labqoat._generated.attempt_page import AttemptPage
from labqoat._generated.distributed_group_page import DistributedGroupPage

P = ParamSpec("P")
R = TypeVar("R")


class RunsClient(BaseClient):
    """Submit ordinary typed executions and read their retained outputs."""

    def __init__(
        self, transport: Transport, options: RunOptions | None = None, uploads: UploadMemo | None = None
    ) -> None:
        """Bind one explicit transport and optional retry-safe root operation identity."""
        super().__init__(transport)
        self._options = options or RunOptions()
        self._uploads = uploads

    @property
    def options(self) -> RunOptions:
        """Expose immutable dispatch policy for explicitly bound bulk operations."""
        return self._options

    @property
    def recoveries(self) -> RecoveryClient:
        """Access bounded discovery, operation history, cancellation and explicit recovery handles."""
        return RecoveryClient(self._transport)

    @property
    def workflow_recovery(self) -> WorkflowRecoveryClient:
        """Read paginated failed-descendant previews and durable frozen workflow plans."""
        return WorkflowRecoveryClient(self._transport)

    def recover(
        self,
        run_id: str,
        *,
        expected_state_version: int,
        reason: str = "",
        include_cancelled: bool = False,
        operation_key: str | None = None,
    ) -> RecoveryHandle:
        """Recover failed descendants and replay retained orchestration under the existing run IDs."""
        return self.workflow_recovery.recover(
            run_id,
            expected_state_version=expected_state_version,
            reason=reason,
            include_cancelled=include_cancelled,
            operation_key=operation_key,
        )

    @property
    def fit_budget(self) -> BudgetHistoryClient:
        """Read scientific usage and establish unknown historical consumption from retained evidence."""
        return BudgetHistoryClient(self._transport)

    @property
    def forks(self) -> ForkClient:
        """Read changed-work history and immutable checkpoint and usage ancestry."""
        return ForkClient(self._transport)

    def fork(self, run_id: str, request: ForkRequest, *, operation_key: str | None = None) -> ForkLineage:
        """Accept explicitly changed work under a new run ID with source-version protection."""
        return self.forks.create(run_id, request, operation_key=operation_key)

    def recovery(self, run_id: str, *, limit: int = 50, cursor: str | None = None) -> RecoveryDiscovery:
        """Discover advisory recovery eligibility and retained checkpoint candidates."""
        return self.recoveries.discovery(run_id, limit=limit, cursor=cursor)

    def restart(
        self,
        run_id: str,
        *,
        expected_state_version: int,
        reason: str = "",
        include_cancelled: bool = False,
        operation_key: str | None = None,
    ) -> RecoveryHandle:
        """Restart immutable intended work under its existing Run ID and cumulative allowance."""
        request = RecoveryRequest(
            expected_state_version, "restart", include_cancelled=include_cancelled, reason=reason, scope="run"
        )
        return self.recoveries.create(run_id, request, operation_key=operation_key)

    def attempts(
        self,
        run_id: str,
        *,
        limit: int = 50,
        cursor: str | None = None,
        attempt: str | None = None,
        cycle: int | None = None,
    ) -> AttemptPage:
        """Read one bounded page of fenced attempt history."""
        query = {"limit": str(limit)}
        if cursor is not None:
            query["cursor"] = cursor
        if attempt is not None:
            query["attempt"] = attempt
        if cycle is not None:
            query["cycle"] = str(cycle)
        path = f"/api/v1/runs/{BaseClient.encode_ref(run_id)}/attempts?" + urlencode(query)
        return self.decode(self.send("GET", path), path, AttemptPage.from_dict)

    def restart_shards(
        self,
        run_id: str,
        *,
        expected_state_version: int,
        reason: str = "",
        include_cancelled: bool = False,
        operation_key: str | None = None,
    ) -> RecoveryHandle:
        """Restart only unsuccessful independent shards, preserving the original successful output receipts."""
        request = RecoveryRequest(
            expected_state_version,
            "restart",
            include_cancelled=include_cancelled,
            reason=reason,
            scope="failed_shards",
        )
        return self.recoveries.create(run_id, request, operation_key=operation_key)

    def group(
        self, run_id: str, attempt_id: str, *, limit: int = 50, cursor: str | None = None
    ) -> DistributedGroupPage:
        """Read bounded rank restoration evidence for one immutable attempt generation."""
        query = {"limit": str(limit)}
        if cursor is not None:
            query["cursor"] = cursor
        run = BaseClient.encode_ref(run_id)
        attempt = BaseClient.encode_ref(attempt_id)
        path = f"/api/v1/runs/{run}/attempts/{attempt}/group?" + urlencode(query)
        return self.decode(self.send("GET", path), path, DistributedGroupPage.from_dict)

    def resume(
        self,
        run_id: str,
        *,
        expected_state_version: int,
        checkpoint: str = "latest-durable",
        reason: str = "",
        include_cancelled: bool = False,
        operation_key: str | None = None,
    ) -> RecoveryHandle:
        """Freeze a compatible durable checkpoint without permitting fallback to fresh training."""
        selection = {"selection": "latest_durable"} if checkpoint == "latest-durable" else {"id": checkpoint}
        request = RecoveryRequest(
            expected_state_version,
            "resume",
            checkpoint=selection,
            include_cancelled=include_cancelled,
            reason=reason,
            scope="run",
        )
        return self.recoveries.create(run_id, request, operation_key=operation_key)

    def prepare(self, function: Function[P, R]) -> PreparedSubmission[R]:
        """Create a lazy publication shared by explicitly bound bulk submissions."""
        return PreparedSubmission(self._transport, function)

    def finalize(
        self,
        run_id: str,
        *,
        expected_state_version: int,
        checkpoint: str = "latest-durable",
        reason: str = "",
        include_cancelled: bool = False,
        operation_key: str | None = None,
    ) -> RecoveryHandle:
        """Restore durable completed-training state and publish results without another fit interval."""
        selection = {"selection": "latest_durable"} if checkpoint == "latest-durable" else {"id": checkpoint}
        request = RecoveryRequest(
            expected_state_version,
            "finalize",
            checkpoint=selection,
            include_cancelled=include_cancelled,
            reason=reason,
            scope="run",
        )
        return self.recoveries.create(run_id, request, operation_key=operation_key)

    def with_options(
        self,
        *,
        key: str | None = None,
        seed: int = 0,
        resources: Resources | None = None,
        location: str | None = None,
    ) -> RunsClient:
        """Select explicit execution configuration independently of authored callable arguments."""
        return RunsClient(
            self._transport,
            RunOptions(key=key, seed=seed, resources=resources, location=location),
            self._uploads,
        )

    def submit(self, function: Function[P, R], *args: P.args, **kwargs: P.kwargs) -> RunHandle[R]:
        """Automatically publish a declared function and accept a typed, service-owned root Run."""
        record = Submission(self._transport, self._uploads).submit(function, args, kwargs, self._options)
        return RunHandle(record.id, self, FunctionSignature(function.local).annotations["return"])

    async def submit_async(self, function: Function[P, R], *args: P.args, **kwargs: P.kwargs) -> RunHandle[R]:
        """Run host publication and acceptance off the event loop with explicit client authority."""
        operation = partial(self.submit, function, *args, **kwargs)
        return await asyncio.to_thread(operation)

    def handle(self, run_id: str, *, result_type: type[R]) -> RunHandle[R]:
        """Attach this client's explicit transport to an existing immutable Run identity."""
        return RunHandle(run_id, self, result_type)

    def get(self, ref: str, *, expected_kind: str | None = None) -> Run:
        """Read one run."""
        path = f"/api/v1/runs/{BaseClient.encode_ref(ref)}"
        if expected_kind is not None:
            path += "?expected_kind=" + BaseClient.encode_ref(expected_kind)
        return self.decode(self.send("GET", path), path, Run.from_dict)

    def events(
        self,
        run_id: str,
        *,
        cursor: str | None = None,
        expected_kind: str | None = None,
        recovery_operation_id: str | None = None,
    ) -> Generator[RunStreamEvent]:
        """Replay retained Run events and keep following committed progress with a closable HTTP response."""
        query = {"cursor": cursor, "expected_kind": expected_kind, "recovery_operation_id": recovery_operation_id}
        path = f"/api/v1/runs/{BaseClient.encode_ref(run_id)}/events?" + urlencode(
            {key: value for key, value in query.items() if value is not None}
        )
        with self.stream_response("GET", path, event_stream=True) as response:
            for event in SseClient.parse_events(response.iter_bytes()):
                try:
                    yield RunStreamEvent.from_dict(event)
                except (KeyError, TypeError, ValueError) as error:
                    raise ApiError("Malformed Run event.") from error

    def wait(self, run_id: str, *, expected_kind: str | None = None, max_reconnects: int = 8) -> Run:
        """Follow events and fetch authoritative terminal state, raising a typed error for unsuccessful Runs."""
        from labqoat.runs.run_waiter import RunWaiter

        return RunWaiter(self, run_id, expected_kind, max_reconnects).run()

    def logs(
        self,
        run_id: str,
        *,
        attempt: str | None = None,
        cycle: int | None = None,
        depth: int | None = None,
        run: str | Sequence[str] | None = None,
        include_metrics: bool = False,
        build_output: str | None = None,
    ) -> Generator[JsonDocument]:
        """Follow retained build, lifecycle and execution logs until the Run becomes terminal."""
        path = f"/api/v1/runs/{BaseClient.encode_ref(run_id)}/logs?follow=true"
        selection: dict[str, str] = {}
        if build_output is not None:
            selection["build_output"] = build_output
        if include_metrics:
            selection["include_metrics"] = "true"
        if depth is not None:
            selection["depth"] = str(depth)
        if run:
            selection["run"] = run if isinstance(run, str) else json.dumps(list(run), separators=(",", ":"))
        if attempt is not None:
            selection["attempt"] = attempt
        if cycle is not None:
            selection["cycle"] = str(cycle)
        if selection:
            path += "&" + urlencode(selection)
        from labqoat.runs.run_log_stream import RunLogStream

        yield from RunLogStream(self, path).entries()

    def result(self, run_id: str, *, expected_kind: str | None = None) -> JsonDocument:
        """Retrieve the exact validated authored result without transport or shard metadata."""
        path = f"/api/v1/runs/{BaseClient.encode_ref(run_id)}/result"
        if expected_kind is not None:
            path += "?expected_kind=" + BaseClient.encode_ref(expected_kind)
        return self.decode(self.send("GET", path), path, JsonDocument.expect_dict)

    def cancel(self, ref: str) -> Run:
        """Cancel active work."""
        path = f"/api/v1/runs/{BaseClient.encode_ref(ref)}/cancel"
        response = self.send_json("POST", path, {})
        return self.decode(response, path, Run.from_dict)

    def add_tag(self, ref: str, tag: str) -> Run:
        """Tag a run, finished or not, so listings and dashboard queries can select or exclude it."""
        return self.change_tag("PUT", ref, tag)

    def remove_tag(self, ref: str, tag: str) -> Run:
        """Take a tag off a run."""
        return self.change_tag("DELETE", ref, tag)

    def change_tag(self, method: str, ref: str, tag: str) -> Run:
        """Send one tag change and return the run as it now stands."""
        path = f"/api/v1/runs/{BaseClient.encode_ref(ref)}/tags/{BaseClient.encode_ref(tag)}"
        return self.decode(self.send(method, path), path, Run.from_dict)

    def evaluation(self, run_id: str) -> JsonDocument:
        """Read an authored evaluation result through the validated ordinary result endpoint."""
        return self.result(run_id)

    def placement(self, run_id: str) -> RunPlacement:
        """Read physical worker attribution and placement without paginated collection parameters."""
        path = f"/api/v1/runs/{BaseClient.encode_ref(run_id)}/placement"
        return self.decode(self.send("GET", path), path, RunPlacement.from_dict)

    def child_collection(self, name: str, ref: str, limit: int = 20) -> JsonDocument:
        """Read a paged child collection."""
        path = f"/api/v1/runs/{BaseClient.encode_ref(ref)}/{name}?limit={limit}"
        return JsonDocument.expect_dict(self.send("GET", path).json())

    def list_checkpoints(self, limit: int = 20) -> JsonDocument:
        """List checkpoints."""
        return JsonDocument.expect_dict(self.send("GET", f"/api/v1/checkpoints?limit={limit}").json())

    def get_checkpoint(self, ref: str) -> Checkpoint:
        """Read one checkpoint."""
        path = f"/api/v1/checkpoints/item?ref={BaseClient.encode_ref(ref)}"
        return self.decode(self.send("GET", path), path, Checkpoint.from_dict)

    def resolve_checkpoint(self, ref: str) -> CheckpointRef[object]:
        """Resolve and verify an immutable checkpoint for use as an ordinary function argument."""
        checkpoint = self.get_checkpoint(ref)
        reference = CheckpointIdentity.reference(checkpoint.to_dict())
        if str(reference.id) != ref:
            raise ValueError("Resolved checkpoint identity mismatch")
        return reference
