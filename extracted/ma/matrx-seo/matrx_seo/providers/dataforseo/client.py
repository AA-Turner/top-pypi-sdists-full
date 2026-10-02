from __future__ import annotations

import asyncio
import logging
import time
from collections import Counter
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from typing import Any

from ...adapters import ProviderExecutionContext
from ...contracts import ProviderCallRecord, ProviderResponse, ProviderTaskCheckpoint
from ...identity import stable_hash
from .contracts import (
    DataForSeoEnvelope,
    DataForSeoLanguage,
    DataForSeoLocation,
    DataForSeoOperationName,
    DataForSeoOperationRequest,
    DataForSeoTask,
    DataForSeoWorkflow,
)
from .operations import (
    GET_LIST_ENDPOINTS,
    LIVE_OFFSET_CEILING,
    LIVE_PAGE_MAX_LIMIT,
    PAGINATED_LIVE_ENDPOINTS,
    DataForSeoOperation,
    get_operation,
)
from .transport import DataForSeoTransport

logger = logging.getLogger(__name__)

#: Task status codes that mean the work SUCCEEDED with nothing to report —
#: never a batch failure. 40102 "No Search Results." is the provider's answer
#: for a query that genuinely matches nothing (measured live 2026-08-16: a
#: niche keyword restricted to the last 24 hours, tbs=qdr:d) — the search ran,
#: the answer is "nobody ranks", and failing the whole 16-task prospecting run
#: over it turned a correct empty answer into a paid error. The task row still
#: records the provider's code verbatim; only the batch-failure decision and
#: the run's terminal status treat it as success.
_OK_TASK_STATUS_CODES = frozenset({20000, 40102})


class DataForSeoApiError(RuntimeError):
    def __init__(self, status_code: int, message: str) -> None:
        self.status_code = status_code
        super().__init__(f"DataForSEO {status_code}: {message}")


class DataForSeoTaskTimeout(DataForSeoApiError):
    pass


@dataclass(frozen=True)
class PollingPolicy:
    first_poll_seconds: float
    interval_seconds: float
    timeout_seconds: float


@dataclass
class _TaskState:
    checkpoint: ProviderTaskCheckpoint
    final_task: DataForSeoTask | None = None
    retrieval_raw: list[dict[str, Any]] = field(default_factory=list)
    requests: list[dict[str, Any]] = field(default_factory=list)


class DataForSeoClient:
    def __init__(
        self,
        transport: DataForSeoTransport,
        *,
        sleeper: Callable[[float], Awaitable[None]] = asyncio.sleep,
        monotonic: Callable[[], float] = time.monotonic,
        polling_policy: PollingPolicy | None = None,
        catalog_ttl: timedelta = timedelta(hours=24),
    ) -> None:
        self.transport = transport
        self._sleeper = sleeper
        self._monotonic = monotonic
        self._polling_policy = polling_policy
        self._catalog_ttl = catalog_ttl
        self._catalog: dict[str, tuple[datetime, list[dict[str, Any]], dict[str, Any]]] = {}

    async def execute(
        self,
        request: DataForSeoOperationRequest,
        execution: ProviderExecutionContext | None = None,
    ) -> ProviderResponse:
        operation = get_operation(request.operation)
        if request.workflow not in operation.workflows:
            raise ValueError(f"{operation.name.value} does not support {request.workflow.value}")
        endpoint = operation.endpoint_for(request.workflow, request.endpoint)
        if request.workflow is DataForSeoWorkflow.LIVE:
            if len(request.tasks) != 1:
                raise ValueError("DataForSEO live endpoints accept exactly one task")
            if request.max_items is not None and request.max_items > LIVE_PAGE_MAX_LIMIT:
                if endpoint not in PAGINATED_LIVE_ENDPOINTS:
                    raise ValueError(
                        f"{endpoint} does not paginate; max_items must stay at or below "
                        f"{LIVE_PAGE_MAX_LIMIT}. Paginated endpoints: "
                        f"{', '.join(sorted(PAGINATED_LIVE_ENDPOINTS))}"
                    )
                return await self._execute_live_paged(endpoint, request.tasks[0], request.max_items)
            return await self._execute_live(operation, endpoint, request.tasks)
        if request.max_items is not None:
            raise ValueError(
                "max_items is a live-workflow paging budget; standard tasks cannot use it"
            )
        if execution is None:
            raise ValueError("standard DataForSEO tasks require a ProviderExecutionContext")
        return await self._execute_standard(operation, endpoint, request.tasks, execution)

    async def _execute_live(
        self,
        operation: DataForSeoOperation,
        endpoint: str,
        tasks: list[dict[str, Any]],
    ) -> ProviderResponse:
        # A provider list endpoint (GET_LIST_ENDPOINTS) is a bodiless GET; its
        # single task is the empty placeholder that keeps the one-live-task
        # contract, never a body the provider would see.
        method = "GET" if endpoint in GET_LIST_ENDPOINTS else "POST"
        try:
            if method == "GET":
                response = await self.transport.request("GET", endpoint)
            else:
                response = await self.transport.request("POST", endpoint, json_body=tasks)
        except Exception as exc:
            return self._transport_failure_response(method, endpoint, tasks, exc)
        envelope = self._parse_envelope(response.payload)
        fetched_at = datetime.now(UTC)
        records = [
            self._call_record(
                task,
                fetched_at=fetched_at,
                request_count=1,
                requests=[response.request] if response.request is not None else [],
                response_status=response.status_code,
                response_headers=response.headers,
            )
            for task in envelope.tasks
        ]
        return ProviderResponse(
            raw=response.payload,
            fetched_at=fetched_at,
            provider_schema_version=envelope.version,
            external_task_id=envelope.tasks[0].id if len(envelope.tasks) == 1 else None,
            reported_cost=envelope.cost if not records else None,
            call_records=records,
            currency="USD",
            error=self._envelope_error(envelope),
        )

    async def _execute_live_paged(
        self,
        endpoint: str,
        task_body: dict[str, Any],
        max_items: int,
    ) -> ProviderResponse:
        """Collect one live endpoint past the provider's 1000-item page ceiling.

        The provider returns at most 1000 items per request whatever ``limit``
        says, so every dataset larger than that was silently truncated. This
        loops on the result's ``search_after_token`` (falling back to ``offset``
        while it is still under the provider's 20 000 ceiling) and merges every
        page into ONE result.

        Merging — rather than emitting a response per page — is required, not
        cosmetic. The observation dedup key is
        (run, site, dataset, target, observed_at), so per-page observations
        collapse into one row and only the first page's links would persist; and
        ``upsert_current_backlinks`` REPLACES a referring domain's
        ``current_backlinks`` count, so a domain split across pages would end up
        counted at whatever the last page happened to hold.

        Every page is separately billed, so the loop never discards pages it has
        already paid for: a failure after page one stops the loop and is reported
        inside ``_matrx_pagination``, never as ``ProviderResponse.error`` — which
        fails the run and drops every collected row.
        """
        requested_limit = task_body.get("limit")
        page_size = LIVE_PAGE_MAX_LIMIT if requested_limit is None else int(requested_limit)
        if page_size < 1 or page_size > LIVE_PAGE_MAX_LIMIT:
            raise ValueError(
                f"DataForSEO live limit must be 1..{LIVE_PAGE_MAX_LIMIT}, "
                f"received {requested_limit!r}"
            )

        items: list[Any] = []
        pages: list[dict[str, Any]] = []
        records: list[ProviderCallRecord] = []
        base_payload: dict[str, Any] | None = None
        base_task: dict[str, Any] | None = None
        base_result: dict[str, Any] | None = None
        base_version: str | None = None
        base_cost: Decimal | None = None
        total_count: int | None = None
        token: str | None = None
        stop_reason = "budget_reached"
        stop_error: dict[str, Any] | None = None
        fetched_at = datetime.now(UTC)

        while len(items) < max_items:
            page_index = len(pages)
            page_limit = min(page_size, max_items - len(items))
            body: dict[str, Any] = {**task_body, "limit": page_limit}
            cursor: dict[str, Any] = {}
            if page_index:
                if token is not None:
                    body["search_after_token"] = token
                    cursor = {"search_after_token": token}
                elif len(items) < LIVE_OFFSET_CEILING:
                    body["offset"] = len(items)
                    cursor = {"offset": len(items)}
                else:
                    stop_reason = "no_cursor"
                    break
            try:
                response = await self.transport.request("POST", endpoint, json_body=[body])
            except Exception as exc:
                if not pages:
                    return self._transport_failure_response("POST", endpoint, [body], exc)
                stop_reason = "transport_failure"
                stop_error = self._transport_error(exc)
                logger.error(
                    "DataForSEO paged live collection stopped after %s items on page %s "
                    "(%s): transport failure %s — keeping the pages already paid for",
                    len(items),
                    page_index,
                    endpoint,
                    exc,
                )
                break

            envelope = self._parse_envelope(response.payload)
            page_error = self._envelope_error(envelope)
            page_task = envelope.tasks[0] if envelope.tasks else None
            if page_task is not None:
                records.append(
                    self._call_record(
                        page_task,
                        fetched_at=fetched_at,
                        request_count=1,
                        requests=[response.request] if response.request is not None else [],
                        response_status=response.status_code,
                        response_headers=response.headers,
                    )
                )
            if base_payload is None:
                base_payload = response.payload
                base_version = envelope.version
                base_cost = envelope.cost
                base_task = page_task.model_dump(mode="json") if page_task is not None else None

            results = page_task.result if page_task is not None else None
            results = results if isinstance(results, list) else []
            if len(results) > 1:
                stop_reason = "multi_result"
                logger.error(
                    "DataForSEO %s returned %s results for one live task — refusing to "
                    "merge pages; stopping at %s items",
                    endpoint,
                    len(results),
                    len(items),
                )
                break
            result = results[0] if results and isinstance(results[0], dict) else None
            page_items = result.get("items") if result is not None else None
            page_items = page_items if isinstance(page_items, list) else []
            if base_result is None and result is not None:
                base_result = result
            if result is not None and total_count is None:
                total_count = _optional_int_value(result.get("total_count"))
            token = _optional_string_value(
                result.get("search_after_token") if result is not None else None
            )
            items.extend(page_items)
            pages.append(
                {
                    "page": page_index,
                    "limit": page_limit,
                    **cursor,
                    "items": len(page_items),
                    "total_count": _optional_int_value(
                        result.get("total_count") if result is not None else None
                    ),
                    "status_code": page_task.status_code if page_task is not None else None,
                    "cost": (
                        float(page_task.cost)
                        if page_task is not None and page_task.cost is not None
                        else None
                    ),
                }
            )

            if page_error is not None:
                stop_reason = "provider_error"
                stop_error = page_error
                if pages[:-1]:
                    logger.error(
                        "DataForSEO paged live collection stopped after %s items on page %s "
                        "(%s): %s — keeping the pages already paid for",
                        len(items),
                        page_index,
                        endpoint,
                        page_error.get("message"),
                    )
                break
            if not page_items:
                stop_reason = "exhausted"
                break
            if len(page_items) < page_limit:
                stop_reason = "complete"
                break
            if total_count is not None and len(items) >= total_count:
                stop_reason = "complete"
                break

        pagination: dict[str, Any] = {
            "endpoint": endpoint,
            "budget": max_items,
            "page_size": page_size,
            "collected": len(items),
            "total_count": total_count,
            "pages": pages,
            "stop_reason": stop_reason,
            "truncated": bool(
                total_count is not None and len(items) < total_count and stop_reason != "complete"
            ),
        }
        if stop_error is not None:
            pagination["stop_error"] = stop_error
        if pagination["truncated"]:
            logger.warning(
                "DataForSEO %s collected %s of %s items (stop_reason=%s) — the stored "
                "dataset is incomplete for this run",
                endpoint,
                len(items),
                total_count,
                stop_reason,
            )

        if base_payload is None:
            raise DataForSeoApiError(20000, f"{endpoint} returned no pages")
        raw: dict[str, Any] = {key: value for key, value in base_payload.items() if key != "tasks"}
        if base_task is not None:
            merged_task = dict(base_task)
            if base_result is not None:
                merged_result = {**base_result, "items": items, "items_count": len(items)}
                merged_task["result"] = [merged_result]
                merged_task["result_count"] = 1
            raw["tasks"] = [merged_task]
        else:
            raw["tasks"] = base_payload.get("tasks", [])
        raw["_matrx_pagination"] = pagination

        return ProviderResponse(
            raw=raw,
            fetched_at=fetched_at,
            provider_schema_version=base_version,
            external_task_id=records[0].external_task_id if records else None,
            reported_cost=base_cost if not records else None,
            call_records=_unique_call_records(records),
            currency="USD",
            # Demoted to `_matrx_pagination.stop_error` whenever at least one
            # page landed: failing the run would discard rows we already bought.
            error=None if items else stop_error,
        )

    async def _execute_standard(
        self,
        operation: DataForSeoOperation,
        post_endpoint: str,
        tasks: list[dict[str, Any]],
        execution: ProviderExecutionContext,
    ) -> ProviderResponse:
        states, submission_marker = await self._resume_states(execution, post_endpoint)
        cardinality_error: dict[str, Any] | None = None
        submission_raw = next(
            (
                state.checkpoint.request_payload.get("_matrx_submission_envelope")
                for state in states
                if isinstance(
                    state.checkpoint.request_payload.get("_matrx_submission_envelope"),
                    dict,
                )
            ),
            None,
        )
        if submission_marker is not None and not states:
            return self._uncertain_submission_response(post_endpoint, tasks, submission_marker)
        if states and not self._states_match_tasks(states, tasks):
            return self._resume_mismatch_response(post_endpoint, tasks, states)
        if not states:
            now = datetime.now(UTC)
            submission_marker = ProviderTaskCheckpoint(
                external_task_id=f"_matrx_submission:{execution.run.id}",
                endpoint=post_endpoint,
                status="submitted",
                request_payload={"_matrx_submission_pending": tasks},
                request_count=0,
                submitted_at=now,
            )
            await execution.checkpoint(submission_marker)
            try:
                submission = await self.transport.request("POST", post_endpoint, json_body=tasks)
            except Exception as exc:
                failed_marker = submission_marker.model_copy(
                    update={
                        "status": "failed",
                        "request_count": self._attempt_count(exc),
                        "completed_at": datetime.now(UTC),
                        "error": self._transport_error(exc),
                    }
                )
                await execution.checkpoint(failed_marker)
                return self._transport_failure_response(
                    "POST",
                    post_endpoint,
                    tasks,
                    exc,
                    provider_call_key=submission_marker.external_task_id,
                )
            submission_raw = submission.payload
            envelope = self._parse_envelope(submission.payload)
            states = []
            checkpoints: list[ProviderTaskCheckpoint] = []
            shape_error = len(envelope.tasks) != len(tasks)
            returned_tasks = list(envelope.tasks)
            if shape_error:
                cardinality_error = {
                    "expected": len(tasks),
                    "received": len(returned_tasks),
                }
            for index in range(max(len(returned_tasks), len(tasks))):
                task = (
                    returned_tasks[index]
                    if index < len(returned_tasks)
                    else DataForSeoTask(
                        id=f"_matrx_missing:{execution.run.id}:{index}",
                        status_code=50001,
                        status_message="DataForSEO task POST omitted this requested task",
                        data=tasks[index],
                    )
                )
                accepted = task.status_code == 20100
                checkpoint = ProviderTaskCheckpoint(
                    external_task_id=task.id,
                    endpoint=post_endpoint,
                    status="submitted" if accepted else "failed",
                    request_payload={
                        **(tasks[index] if index < len(tasks) else task.data),
                        **(
                            {"_matrx_requests": [submission.request]}
                            if submission.request is not None
                            else {}
                        ),
                        **(
                            {"_matrx_submission_envelope": submission.payload} if index == 0 else {}
                        ),
                    },
                    response_payload=task.model_dump(mode="json"),
                    request_count=1,
                    provider_cost=task.cost,
                    submitted_at=now,
                    completed_at=None if accepted else now,
                    error=(
                        None
                        if accepted
                        else {
                            "status_code": task.status_code,
                            "status_message": task.status_message,
                        }
                    ),
                )
                checkpoints.append(checkpoint)
                states.append(
                    _TaskState(
                        checkpoint=checkpoint,
                        final_task=None if accepted else task,
                        requests=[submission.request] if submission.request is not None else [],
                    )
                )
            completed_marker = submission_marker.model_copy(
                update={
                    "status": "completed",
                    "response_payload": submission.payload,
                    "request_count": 0,
                    "completed_at": now,
                    "error": (
                        {
                            "type": "DataForSeoTaskCardinalityError",
                            "expected": len(tasks),
                            "received": len(returned_tasks),
                        }
                        if shape_error
                        else None
                    ),
                }
            )
            await execution.checkpoint_many([*checkpoints, completed_marker])
            if envelope.status_code != 20000 and not states:
                return self._failed_provider_response(submission.payload, envelope)
        if not states:
            raise DataForSeoApiError(20000, "task POST returned no tasks")

        policy = self._policy_for(operation, tasks)
        pending = [state for state in states if state.final_task is None]
        if pending:
            logger.warning(
                "DataForSEO standard workflow waiting before first poll: "
                "operation=%s pending_tasks=%s first_poll_seconds=%s "
                "interval_seconds=%s timeout_seconds=%s — this request stays "
                "open until polling finishes; use workflow=live for a single "
                "synchronous call",
                operation.name.value,
                len(pending),
                policy.first_poll_seconds,
                policy.interval_seconds,
                policy.timeout_seconds,
            )
            if policy.first_poll_seconds > 0:
                await self._sleeper(policy.first_poll_seconds)
            deadline = self._monotonic() + policy.timeout_seconds
            await asyncio.gather(
                *(
                    self._poll_task(operation, state, execution, policy, deadline)
                    for state in pending
                )
            )

        final_tasks = [state.final_task for state in states if state.final_task is not None]
        if len(final_tasks) != len(states):
            raise RuntimeError("DataForSEO task workflow ended without all task results")
        fetched_at = datetime.now(UTC)
        retrievals = [state.retrieval_raw for state in states]
        final_raw = {
            "version": "3",
            "status_code": 20000,
            "status_message": "Ok.",
            "tasks_count": len(final_tasks),
            "tasks_error": 0,
            "tasks": [task.model_dump(mode="json") for task in final_tasks],
            "_matrx_provider_responses": {
                "task_post": submission_raw,
                "task_get": retrievals,
            },
        }
        records = [
            self._call_record(
                task,
                fetched_at=fetched_at,
                request_count=state.checkpoint.request_count - 1 + (1 if index == 0 else 0),
                cost=state.checkpoint.provider_cost,
                requests=state.requests,
            )
            for index, (state, task) in enumerate(zip(states, final_tasks, strict=True))
        ]
        return ProviderResponse(
            raw=final_raw,
            fetched_at=fetched_at,
            provider_schema_version="3",
            external_task_id=final_tasks[0].id if len(final_tasks) == 1 else None,
            call_records=records,
            currency="USD",
            error=(
                {
                    "type": "DataForSeoTaskBatchError",
                    "message": (
                        "DataForSEO task POST cardinality mismatch"
                        if cardinality_error is not None
                        else "one or more DataForSEO tasks failed"
                    ),
                    "cardinality": cardinality_error,
                    "tasks": [
                        {
                            "id": task.id,
                            "status_code": task.status_code,
                            "status_message": task.status_message,
                        }
                        for task in final_tasks
                        if task.status_code not in _OK_TASK_STATUS_CODES
                    ],
                }
                if cardinality_error is not None
                or any(task.status_code not in _OK_TASK_STATUS_CODES for task in final_tasks)
                else None
            ),
        )

    async def _resume_states(
        self,
        execution: ProviderExecutionContext,
        post_endpoint: str,
    ) -> tuple[list[_TaskState], ProviderTaskCheckpoint | None]:
        checkpoints = await execution.resumable_tasks()
        states: list[_TaskState] = []
        marker = None
        for checkpoint in checkpoints:
            if checkpoint.endpoint != post_endpoint or checkpoint.status == "cancelled":
                continue
            if checkpoint.external_task_id.startswith("_matrx_submission:"):
                marker = checkpoint
                continue
            stored_requests = checkpoint.request_payload.get("_matrx_requests")
            state = _TaskState(
                checkpoint=checkpoint,
                requests=(
                    [item for item in stored_requests if isinstance(item, dict)]
                    if isinstance(stored_requests, list)
                    else []
                ),
            )
            if checkpoint.status in {"completed", "failed"} and isinstance(
                checkpoint.response_payload, dict
            ):
                state.final_task = DataForSeoTask.model_validate(checkpoint.response_payload)
                state.retrieval_raw.append(
                    {
                        "status_code": 20000,
                        "status_message": "Replayed from provider_task checkpoint.",
                        "tasks": [checkpoint.response_payload],
                    }
                )
            states.append(state)
        return states, marker

    @classmethod
    def _states_match_tasks(cls, states: list[_TaskState], tasks: list[dict[str, Any]]) -> bool:
        if len(states) != len(tasks):
            return False
        resumed = Counter(
            stable_hash(cls._provider_task_payload(state.checkpoint.request_payload))
            for state in states
        )
        requested = Counter(stable_hash(task) for task in tasks)
        return resumed == requested

    async def _poll_task(
        self,
        operation: DataForSeoOperation,
        state: _TaskState,
        execution: ProviderExecutionContext,
        policy: PollingPolicy,
        deadline: float,
    ) -> None:
        endpoint = operation.task_get_endpoint(state.checkpoint.external_task_id)
        while self._monotonic() <= deadline:
            try:
                response = await self.transport.request("GET", endpoint)
            except Exception as exc:
                await self._settle_poll_failure(
                    state,
                    execution,
                    status_code=50000,
                    message=str(exc),
                    response_payload={
                        "type": type(exc).__name__,
                        "message": str(exc),
                    },
                    request_attempted=True,
                )
                return
            state.retrieval_raw.append(response.payload)
            if response.request is not None:
                state.requests.append(response.request)
            envelope = self._parse_envelope(response.payload)
            task = next(
                (item for item in envelope.tasks if item.id == state.checkpoint.external_task_id),
                None,
            )
            if task is None:
                task = DataForSeoTask(
                    id=state.checkpoint.external_task_id,
                    status_code=envelope.status_code,
                    status_message=envelope.status_message,
                    cost=state.checkpoint.provider_cost,
                    data=self._provider_task_payload(state.checkpoint.request_payload),
                )
            now = datetime.now(UTC)
            request_count = state.checkpoint.request_count + 1
            if (
                task.status_code == 20000
                and task.result is not None
                and self._task_is_complete(operation, task)
            ):
                retrieval_raw: dict[str, Any] = response.payload
                extra_requests = 0
                if operation.name is DataForSeoOperationName.ON_PAGE_CRAWL:
                    (
                        task,
                        retrieval_raw,
                        extra_requests,
                        result_requests,
                    ) = await self._collect_on_page_results(
                        operation,
                        task,
                        response.payload,
                        state.checkpoint.request_payload,
                    )
                    state.requests.extend(result_requests)
                completed = task.status_code == 20000
                checkpoint = state.checkpoint.model_copy(
                    update={
                        "status": "completed" if completed else "failed",
                        "request_payload": {
                            **state.checkpoint.request_payload,
                            "_matrx_requests": state.requests,
                        },
                        "response_payload": task.model_dump(mode="json"),
                        "request_count": request_count + extra_requests,
                        "last_polled_at": now,
                        "completed_at": now,
                        "error": (
                            None
                            if completed
                            else {
                                "status_code": task.status_code,
                                "status_message": task.status_message,
                            }
                        ),
                    }
                )
                await execution.checkpoint(checkpoint)
                state.checkpoint = checkpoint
                state.final_task = task
                if operation.name is DataForSeoOperationName.ON_PAGE_CRAWL:
                    state.retrieval_raw.append(retrieval_raw)
                return
            if task.status_code not in {20000, 40601, 40602}:
                checkpoint = state.checkpoint.model_copy(
                    update={
                        "status": "failed",
                        "request_payload": {
                            **state.checkpoint.request_payload,
                            "_matrx_requests": state.requests,
                        },
                        "response_payload": task.model_dump(mode="json"),
                        "request_count": request_count,
                        "last_polled_at": now,
                        "error": {
                            "status_code": task.status_code,
                            "status_message": task.status_message,
                        },
                    }
                )
                await execution.checkpoint(checkpoint)
                state.checkpoint = checkpoint
                state.final_task = task
                return
            checkpoint = state.checkpoint.model_copy(
                update={
                    "status": "polling",
                    "request_payload": {
                        **state.checkpoint.request_payload,
                        "_matrx_requests": state.requests,
                    },
                    "response_payload": task.model_dump(mode="json"),
                    "request_count": request_count,
                    "last_polled_at": now,
                }
            )
            await execution.checkpoint(checkpoint)
            state.checkpoint = checkpoint
            if policy.interval_seconds > 0:
                await self._sleeper(policy.interval_seconds)
        await self._settle_poll_failure(
            state,
            execution,
            status_code=40800,
            message=f"task {state.checkpoint.external_task_id} timed out",
            response_payload={"type": "DataForSeoTaskTimeout"},
            request_attempted=False,
        )

    @staticmethod
    def _task_is_complete(
        operation: DataForSeoOperation,
        task: DataForSeoTask,
    ) -> bool:
        if operation.name is not DataForSeoOperationName.ON_PAGE_CRAWL:
            return True
        values: list[str] = []

        def visit(value: Any) -> None:
            if isinstance(value, dict):
                for key, nested in value.items():
                    if key in {"crawl_status", "crawl_progress"} and isinstance(nested, str):
                        values.append(nested.casefold())
                    visit(nested)
            elif isinstance(value, list):
                for nested in value:
                    visit(nested)

        visit(task.result)
        if any(value in {"in_progress", "processing", "crawling"} for value in values):
            return False
        return not values or any(value in {"finished", "completed", "done"} for value in values)

    async def _collect_on_page_results(
        self,
        operation: DataForSeoOperation,
        task: DataForSeoTask,
        summary_raw: dict[str, Any],
        request_payload: dict[str, Any],
    ) -> tuple[DataForSeoTask, dict[str, Any], int, list[dict[str, Any]]]:
        max_results = min(
            max(int(request_payload.get("max_crawl_pages") or 100), 1),
            100_000,
        )
        raw_results: dict[str, Any] = {"summary": summary_raw}
        combined: dict[str, Any] = {"summary": task.result}
        failures: list[dict[str, Any]] = []
        request_count = 0
        requests: list[dict[str, Any]] = []
        result_endpoints = [
            endpoint
            for endpoint in operation.endpoints
            if endpoint
            not in {
                "/v3/on_page/task_post",
                "/v3/on_page/summary/{task_id}",
            }
        ]
        for endpoint in result_endpoints:
            offset = 0
            raw_pages: list[dict[str, Any]] = []
            combined_pages: list[Any] = []
            keyword_density_url = (
                self._first_crawled_url(combined.get("/v3/on_page/pages", []))
                if endpoint == "/v3/on_page/keyword_density"
                else None
            )
            if endpoint == "/v3/on_page/keyword_density" and keyword_density_url is None:
                raw_results[endpoint] = []
                combined[endpoint] = []
                continue
            while offset < max_results:
                limit = min(1_000, max_results - offset)
                body: dict[str, Any] = {"id": task.id, "limit": limit, "offset": offset}
                if endpoint == "/v3/on_page/duplicate_tags":
                    body["type"] = "duplicate_description"
                elif endpoint == "/v3/on_page/keyword_density":
                    body = {
                        "id": task.id,
                        "url": keyword_density_url,
                        "keyword_length": 1,
                    }
                try:
                    response = await self.transport.request(
                        "POST",
                        endpoint,
                        json_body=[body],
                    )
                    request_count += 1
                    if response.request is not None:
                        requests.append(response.request)
                except Exception as exc:
                    request_count += self._attempt_count(exc)
                    failure = {
                        "type": type(exc).__name__,
                        "message": str(exc),
                        "endpoint": endpoint,
                        "offset": offset,
                    }
                    failures.append(failure)
                    raw_pages.append({"_matrx_transport_failure": failure})
                    break
                raw_pages.append(response.payload)
                envelope = self._parse_envelope(response.payload)
                page_results = [item.result for item in envelope.tasks if item.result is not None]
                combined_pages.extend(page_results)
                error = self._envelope_error(envelope)
                if error is not None:
                    failures.append(error)
                    break
                if endpoint == "/v3/on_page/keyword_density":
                    break
                received, total = self._page_progress(page_results)
                if received == 0 or received < limit or (total > 0 and offset + received >= total):
                    break
                offset += received
            raw_results[endpoint] = raw_pages
            combined[endpoint] = combined_pages
        if failures:
            task = task.model_copy(
                update={
                    "status_code": 50000,
                    "status_message": "On-Page result retrieval failed",
                    "result": combined,
                }
            )
        else:
            task = task.model_copy(update={"result": combined})
        return task, raw_results, request_count, requests

    @staticmethod
    def _first_crawled_url(value: Any) -> str | None:
        if isinstance(value, dict):
            url = value.get("url")
            if isinstance(url, str) and url.strip():
                return url
            for nested in value.values():
                found = DataForSeoClient._first_crawled_url(nested)
                if found is not None:
                    return found
        elif isinstance(value, list):
            for nested in value:
                found = DataForSeoClient._first_crawled_url(nested)
                if found is not None:
                    return found
        return None

    @staticmethod
    def _page_progress(results: list[Any]) -> tuple[int, int]:
        received = 0
        total = 0
        for result in results:
            values = result if isinstance(result, list) else [result]
            for value in values:
                if not isinstance(value, dict):
                    continue
                items = value.get("items")
                item_count = len(items) if isinstance(items, list) else 0
                received += int(value.get("items_count") or item_count)
                total = max(total, int(value.get("total_count") or 0))
        return received, total

    async def _settle_poll_failure(
        self,
        state: _TaskState,
        execution: ProviderExecutionContext,
        *,
        status_code: int,
        message: str,
        response_payload: dict[str, Any],
        request_attempted: bool,
    ) -> None:
        now = datetime.now(UTC)
        task = DataForSeoTask(
            id=state.checkpoint.external_task_id,
            status_code=status_code,
            status_message=message,
            cost=state.checkpoint.provider_cost,
            data=self._provider_task_payload(state.checkpoint.request_payload),
        )
        checkpoint = state.checkpoint.model_copy(
            update={
                "status": "failed",
                "response_payload": task.model_dump(mode="json"),
                "request_count": state.checkpoint.request_count + (1 if request_attempted else 0),
                "last_polled_at": now,
                "completed_at": now,
                "error": {
                    "status_code": status_code,
                    "status_message": message,
                },
            }
        )
        await execution.checkpoint(checkpoint)
        state.checkpoint = checkpoint
        state.final_task = task
        state.retrieval_raw.append(response_payload)

    @staticmethod
    def _provider_task_payload(payload: dict[str, Any]) -> dict[str, Any]:
        return {key: value for key, value in payload.items() if not key.startswith("_matrx_")}

    @staticmethod
    def _attempt_count(exc: Exception) -> int:
        attempts = getattr(exc, "attempts", 1)
        return max(int(attempts), 1)

    @staticmethod
    def _transport_error(exc: Exception) -> dict[str, Any]:
        return {
            "type": type(exc).__name__,
            "message": str(exc),
            "status_code": getattr(exc, "status_code", None),
            "headers": getattr(exc, "headers", {}),
            "response_body": getattr(exc, "response_body", None),
        }

    @classmethod
    def _transport_failure_response(
        cls,
        method: str,
        endpoint: str,
        request_payload: list[dict[str, Any]],
        exc: Exception,
        *,
        provider_call_key: str | None = None,
    ) -> ProviderResponse:
        fetched_at = datetime.now(UTC)
        error = cls._transport_error(exc)
        return ProviderResponse(
            raw={
                "_matrx_transport_failure": {
                    "method": method,
                    "endpoint": endpoint,
                    "request_payload": request_payload,
                    **error,
                }
            },
            fetched_at=fetched_at,
            call_records=[
                ProviderCallRecord(
                    provider_call_key=provider_call_key
                    or f"transport:{method}:{endpoint}:{fetched_at.isoformat()}",
                    request_count=cls._attempt_count(exc),
                    fetched_at=fetched_at,
                    metadata={
                        **error,
                        "requests": [
                            {
                                "method": method,
                                "url": endpoint,
                                "headers": {},
                                "json": request_payload,
                            }
                        ],
                    },
                )
            ],
            error=error,
        )

    @classmethod
    def _uncertain_submission_response(
        cls,
        endpoint: str,
        tasks: list[dict[str, Any]],
        marker: ProviderTaskCheckpoint,
    ) -> ProviderResponse:
        fetched_at = datetime.now(UTC)
        error = {
            "type": "DataForSeoSubmissionUncertain",
            "message": "A prior task POST may have completed before its response was checkpointed",
        }
        return ProviderResponse(
            raw={
                "_matrx_submission_uncertain": {
                    "endpoint": endpoint,
                    "request_payload": tasks,
                    "checkpoint": marker.model_dump(mode="json"),
                }
            },
            fetched_at=fetched_at,
            call_records=[
                ProviderCallRecord(
                    provider_call_key=marker.external_task_id,
                    external_task_id=marker.external_task_id,
                    request_count=max(marker.request_count, 1),
                    fetched_at=fetched_at,
                    metadata=error,
                )
            ],
            error=error,
        )

    @classmethod
    def _resume_mismatch_response(
        cls,
        endpoint: str,
        tasks: list[dict[str, Any]],
        states: list[_TaskState],
    ) -> ProviderResponse:
        fetched_at = datetime.now(UTC)
        error = {
            "type": "DataForSeoResumeStateMismatch",
            "message": "Durable provider tasks do not match the requested task batch",
            "expected_tasks": len(tasks),
            "checkpointed_tasks": len(states),
        }
        return ProviderResponse(
            raw={
                "_matrx_resume_mismatch": {
                    "endpoint": endpoint,
                    "request_payload": tasks,
                    "checkpoints": [state.checkpoint.model_dump(mode="json") for state in states],
                }
            },
            fetched_at=fetched_at,
            call_records=[
                cls._call_record(
                    state.final_task
                    or DataForSeoTask(
                        id=state.checkpoint.external_task_id,
                        status_code=50002,
                        status_message="Resume state mismatch",
                        data=cls._provider_task_payload(state.checkpoint.request_payload),
                    ),
                    fetched_at=fetched_at,
                    request_count=state.checkpoint.request_count,
                    cost=state.checkpoint.provider_cost,
                )
                for state in states
            ],
            error=error,
        )

    def _policy_for(
        self,
        operation: DataForSeoOperation,
        tasks: list[dict[str, Any]],
    ) -> PollingPolicy:
        if self._polling_policy is not None:
            return self._polling_policy
        if operation.family == "keywords_data":
            return PollingPolicy(30, 30, 14_400)
        if operation.family == "serp" and any(task.get("priority") == 2 for task in tasks):
            return PollingPolicy(5, 5, 2_700)
        return PollingPolicy(10, 10, 2_700)

    async def locations(self, engine: str = "google") -> list[DataForSeoLocation]:
        values, _, _, _ = await self._catalog_values(f"/v3/serp/{engine}/locations")
        return [DataForSeoLocation.model_validate(item) for item in values]

    async def location_catalog(
        self, engine: str = "google"
    ) -> tuple[list[DataForSeoLocation], dict[str, Any], ProviderCallRecord | None]:
        values, raw, requested, request = await self._catalog_values(f"/v3/serp/{engine}/locations")
        record = None
        if requested:
            envelope = self._parse_envelope(raw)
            record = self._call_record(
                envelope.tasks[0],
                fetched_at=datetime.now(UTC),
                request_count=1,
                requests=[request] if request is not None else [],
            )
        return [DataForSeoLocation.model_validate(item) for item in values], raw, record

    async def languages(self, engine: str = "google") -> list[DataForSeoLanguage]:
        values, _, _, _ = await self._catalog_values(f"/v3/serp/{engine}/languages")
        return [DataForSeoLanguage.model_validate(item) for item in values]

    async def account_snapshot(self) -> dict[str, Any]:
        response = await self.transport.request("GET", "/v3/appendix/user_data")
        envelope = self._parse_envelope(response.payload)
        if envelope.status_code != 20000:
            raise DataForSeoApiError(envelope.status_code, envelope.status_message)
        return response.payload

    async def _catalog_values(
        self, path: str
    ) -> tuple[list[dict[str, Any]], dict[str, Any], bool, dict[str, Any] | None]:
        now = datetime.now(UTC)
        cached = self._catalog.get(path)
        if cached is not None and cached[0] > now:
            return [dict(item) for item in cached[1]], dict(cached[2]), False, None
        response = await self.transport.request("GET", path)
        envelope = self._parse_envelope(response.payload)
        self._require_completed_tasks(envelope)
        values: list[dict[str, Any]] = []
        for task in envelope.tasks:
            if isinstance(task.result, list):
                values.extend(item for item in task.result if isinstance(item, dict))
        self._catalog[path] = (now + self._catalog_ttl, values, response.payload)
        return [dict(item) for item in values], dict(response.payload), True, response.request

    @staticmethod
    def _parse_envelope(payload: dict[str, Any]) -> DataForSeoEnvelope:
        return DataForSeoEnvelope.model_validate(payload)

    @staticmethod
    def _require_completed_tasks(envelope: DataForSeoEnvelope) -> None:
        if not envelope.tasks:
            raise DataForSeoApiError(envelope.status_code, "response contained no tasks")
        for task in envelope.tasks:
            if task.status_code != 20000:
                raise DataForSeoApiError(task.status_code, task.status_message)

    @staticmethod
    def _matching_task(envelope: DataForSeoEnvelope, task_id: str) -> DataForSeoTask:
        for task in envelope.tasks:
            if task.id == task_id:
                return task
        raise DataForSeoApiError(envelope.status_code, f"response omitted task {task_id}")

    @staticmethod
    def _envelope_error(envelope: DataForSeoEnvelope) -> dict[str, Any] | None:
        failed = [
            task for task in envelope.tasks if task.status_code not in _OK_TASK_STATUS_CODES
        ]
        if envelope.status_code == 20000 and not failed:
            return None
        # DEF-5 (2026-07-23): the top-level envelope status_message is "Ok."
        # whenever the ENVELOPE itself succeeded (status_code 20000) even
        # when one or more TASKS inside it failed — DataForSEO's own success
        # marker for the transport call, not for the task. Blindly using
        # envelope.status_message stamped every task-level failure with the
        # success text "Ok." on a status='failed' run. Prefer the failing
        # task's own message; fall back to the envelope message only when
        # the envelope itself is what failed (no per-task detail to report).
        if failed:
            message = "; ".join(f"{task.id}: {task.status_message}" for task in failed)
        else:
            message = envelope.status_message
        return {
            "type": "DataForSeoApiError",
            "message": message,
            "status_code": envelope.status_code,
            "tasks": [
                {
                    "id": task.id,
                    "status_code": task.status_code,
                    "status_message": task.status_message,
                }
                for task in failed
            ],
        }

    @classmethod
    def _failed_provider_response(
        cls,
        raw: dict[str, Any],
        envelope: DataForSeoEnvelope,
    ) -> ProviderResponse:
        fetched_at = datetime.now(UTC)
        return ProviderResponse(
            raw=raw,
            fetched_at=fetched_at,
            provider_schema_version=envelope.version,
            reported_cost=envelope.cost,
            call_records=[
                cls._call_record(task, fetched_at=fetched_at, request_count=1)
                for task in envelope.tasks
            ],
            error=cls._envelope_error(envelope),
        )

    @staticmethod
    def _call_record(
        task: DataForSeoTask,
        *,
        fetched_at: datetime,
        request_count: int,
        cost: Decimal | None = None,
        requests: list[dict[str, Any]] | None = None,
        response_status: int | None = None,
        response_headers: dict[str, str] | None = None,
    ) -> ProviderCallRecord:
        return ProviderCallRecord(
            provider_call_key=task.id,
            external_task_id=task.id,
            request_count=request_count,
            reported_cost=task.cost if cost is None else cost,
            currency="USD",
            fetched_at=fetched_at,
            metadata={
                "path": task.path,
                "data": task.data,
                "tag": task.data.get("tag"),
                "status_code": task.status_code,
                "status_message": task.status_message,
                "result_count": task.result_count,
                "requests": requests or [],
                "response_status": response_status,
                "response_headers": response_headers or {},
            },
        )


def _optional_int_value(value: Any) -> int | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _optional_string_value(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    normalized = value.strip()
    return normalized or None


def _unique_call_records(records: list[ProviderCallRecord]) -> list[ProviderCallRecord]:
    """Keep every paid page's record even when the provider repeats a task id.

    ``ProviderResponse`` requires unique call keys. A duplicate id across pages
    would raise AFTER the requests were billed, so the page index disambiguates
    instead of throwing the whole collection away.
    """

    seen: set[str] = set()
    unique: list[ProviderCallRecord] = []
    for index, record in enumerate(records):
        key = record.provider_call_key
        if key in seen:
            key = f"{key}#p{index}"
        seen.add(key)
        unique.append(
            record
            if key == record.provider_call_key
            else record.model_copy(update={"provider_call_key": key})
        )
    return unique
