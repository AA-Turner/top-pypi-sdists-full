from __future__ import annotations

import json
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path
from uuid import uuid4

import pytest
from pydantic import ValidationError

from matrx_seo.adapters import ProviderExecutionContext
from matrx_seo.contracts import (
    CollectionRequest,
    NormalizationContext,
    ProviderCallRecord,
    ProviderResponse,
    ProviderResponseError,
    RawPayloadEnvelope,
    ResolvedCredential,
    ResolvedSeoIdentity,
    SeoCapability,
)
from matrx_seo.providers.dataforseo.ai_answers import build_ai_answer_task
from matrx_seo.providers.dataforseo.client import (
    DataForSeoApiError,
    DataForSeoClient,
    PollingPolicy,
)
from matrx_seo.providers.dataforseo.contracts import (
    DataForSeoEnvelope,
    DataForSeoOperationName,
    DataForSeoOperationRequest,
    DataForSeoWorkflow,
)
from matrx_seo.providers.dataforseo.operations import (
    GET_LIST_ENDPOINTS,
    APPROVED_OPERATIONS,
    DATAFORSEO_ENDPOINT_EXAMPLE_TASKS,
    get_operation,
)
from matrx_seo.providers.dataforseo.transport import AdaptiveRateLimiter, ReplayTransport
from matrx_seo.repository import InMemorySeoRepository
from matrx_seo.service import SeoCollectionService


def test_google_ads_search_volume_rejects_provider_invalid_keywords() -> None:
    with pytest.raises(ValueError, match="exceeds 10 words"):
        DataForSeoOperationRequest(
            operation=DataForSeoOperationName.KEYWORDS_GOOGLE_ADS_SEARCH_VOLUME,
            tasks=[
                {
                    "keywords": [
                        "audit checklist for preventing retired IT assets "
                        "from becoming shadow inventory"
                    ]
                }
            ],
        )


def test_google_ads_search_volume_rejects_more_than_provider_limit() -> None:
    with pytest.raises(ValueError, match="at most 1000 keywords"):
        DataForSeoOperationRequest(
            operation=DataForSeoOperationName.KEYWORDS_GOOGLE_ADS_SEARCH_VOLUME,
            tasks=[{"keywords": [f"keyword {index}" for index in range(1001)]}],
        )


def test_gemini_live_task_uses_supported_model_without_location_fields() -> None:
    task = build_ai_answer_task(
        prompt="Which provider should I choose?",
        engine="gemini",
        country_iso="US",
        city="Los Angeles",
    )

    assert task["model_name"] == "gemini-2.5-flash"
    assert task["web_search"] is True
    assert "web_search_country_iso_code" not in task
    assert "web_search_city" not in task


async def _async_none() -> None:
    return None


def _collection_request(operation: str = "serp.google.organic.advanced") -> CollectionRequest:
    return CollectionRequest(
        organization_id=str(uuid4()),
        created_by=str(uuid4()),
        capability=SeoCapability.SERP_RANK,
        operation=operation,
        target_ref="keyword",
        observation_period="2026-07-21",
        execution_id=uuid4(),
    )


def _envelope(tasks: list[dict[str, object]], *, cost: str = "0") -> dict[str, object]:
    return {
        "version": "3.0.20260721",
        "status_code": 20000,
        "status_message": "Ok.",
        "cost": cost,
        "tasks_count": len(tasks),
        "tasks_error": 0,
        "tasks": tasks,
        "unknown_envelope_field": "retained",
    }


def _task(
    task_id: str,
    *,
    status_code: int,
    cost: str = "0.0006",
    result: list[dict[str, object]] | None = None,
) -> dict[str, object]:
    return {
        "id": task_id,
        "status_code": status_code,
        "status_message": "Ok." if status_code == 20000 else "Task Created.",
        "cost": cost,
        "result_count": len(result or []),
        "path": ["v3", "serp"],
        "data": {"tag": f"tag-{task_id}", "keyword": "synthetic"},
        "result": result,
        "unknown_task_field": "retained",
    }


def _provider_task_rows(repository: InMemorySeoRepository) -> list[dict[str, object]]:
    return [
        row for key, row in repository.provider_tasks.items() if ":_matrx_submission:" not in key
    ]


def test_approved_operations_match_reviewed_matrix() -> None:
    matrix_path = Path(__file__).parents[3] / "docs/seo/dataforseo_capability_matrix.json"
    if matrix_path.exists():
        matrix = json.loads(matrix_path.read_text())
        approved = {
            item["id"]: item for item in matrix["operations"] if item["decision"] == "approved"
        }
        assert {operation.name.value for operation in APPROVED_OPERATIONS} == set(approved)
        for operation in APPROVED_OPERATIONS:
            assert set(operation.endpoints) == set(approved[operation.name.value]["endpoints"])
    assert len(APPROVED_OPERATIONS) == 49
    with pytest.raises(ValueError, match="not approved"):
        get_operation("ai_optimization.llm_responses")


def test_every_approved_operation_can_be_collected_as_raw_provider_evidence() -> None:
    assert all(
        SeoCapability.RAW_PROVIDER in operation.capabilities for operation in APPROVED_OPERATIONS
    )


def test_every_workflow_resolves_or_requires_exact_approved_endpoint() -> None:
    for operation in APPROVED_OPERATIONS:
        for workflow in operation.workflows:
            candidates = [
                endpoint
                for endpoint in operation.endpoints
                if "{task_id}" not in endpoint
                and (
                    (workflow is DataForSeoWorkflow.STANDARD and "task_post" in endpoint)
                    or (workflow is DataForSeoWorkflow.LIVE and "task_post" not in endpoint)
                )
            ]
            if len(candidates) == 1:
                assert operation.endpoint_for(workflow, None) == candidates[0]
            else:
                with pytest.raises(ValueError, match="requires one exact"):
                    operation.endpoint_for(workflow, None)
                for endpoint in candidates:
                    assert operation.endpoint_for(workflow, endpoint) == endpoint


def test_every_selectable_endpoint_has_one_canonical_example() -> None:
    examples = [
        example for operation in APPROVED_OPERATIONS for example in operation.endpoint_examples
    ]
    assert len(examples) == 69
    assert len({example.endpoint for example in examples}) == 69
    assert {example.endpoint for example in examples} == set(DATAFORSEO_ENDPOINT_EXAMPLE_TASKS)
    # A bodiless GET list endpoint's one task is the empty placeholder; every
    # other endpoint's example is a real request body.
    assert all(example.task or example.endpoint in GET_LIST_ENDPOINTS for example in examples)
    assert all(
        ("task_post" in example.endpoint) == (example.workflow is DataForSeoWorkflow.STANDARD)
        for example in examples
    )
    assert "/v3/backlinks/new_lost_timeseries/live" not in DATAFORSEO_ENDPOINT_EXAMPLE_TASKS
    new_lost = DATAFORSEO_ENDPOINT_EXAMPLE_TASKS["/v3/backlinks/timeseries_new_lost_summary/live"]
    assert new_lost == {"target": "dataforseo.com"}
    assert (
        "date_from"
        not in DATAFORSEO_ENDPOINT_EXAMPLE_TASKS["/v3/backlinks/bulk_new_lost_backlinks/live"]
    )


def test_canonical_examples_preserve_endpoint_specific_task_shapes() -> None:
    examples = DATAFORSEO_ENDPOINT_EXAMPLE_TASKS
    suggestions = examples["/v3/dataforseo_labs/google/keyword_suggestions/live"]
    assert set(suggestions) >= {"keyword", "location_code", "language_code"}
    assert "keywords" not in suggestions
    assert set(examples["/v3/dataforseo_labs/google/domain_intersection/live"]) >= {
        "target1",
        "target2",
    }
    assert "pages" in examples["/v3/dataforseo_labs/google/page_intersection/live"]
    assert "targets" in examples["/v3/dataforseo_labs/google/bulk_traffic_estimation/live"]
    assert "targets" in examples["/v3/backlinks/domain_intersection/live"]
    assert examples["/v3/on_page/instant_pages"] == {"url": "https://dataforseo.com/"}
    assert "limit" not in examples["/v3/keywords_data/clickstream_data/bulk_search_volume/live"]
    assert "limit" not in examples["/v3/backlinks/summary/live"]


def test_envelope_retains_unknown_fields_and_rejects_task_failure() -> None:
    raw = _envelope([_task("task-1", status_code=20000, result=[{"rank": 1}])])
    envelope = DataForSeoEnvelope.model_validate(raw)
    assert envelope.model_extra == {"unknown_envelope_field": "retained"}
    assert envelope.tasks[0].model_extra == {"unknown_task_field": "retained"}

    client = DataForSeoClient(ReplayTransport([]))
    failed = DataForSeoEnvelope.model_validate(_envelope([_task("task-1", status_code=40101)]))
    with pytest.raises(DataForSeoApiError, match="40101"):
        client._require_completed_tasks(failed)


@pytest.mark.asyncio
async def test_live_flow_task_failure_reports_task_message_not_envelope_ok() -> None:
    """Regression for DEF-5 (2026-07-23): a live-workflow response whose
    ENVELOPE succeeded (status_code 20000, "Ok.") but whose TASK failed
    (e.g. backlinks.bulk_metrics with an invalid target) was persisted with
    ``error.message == "Ok."`` — the adapter copied the envelope's own
    success text instead of the failing task's status_message, so a run
    surfaced as status='failed' with a success-shaped error. The error must
    now quote the failing task's own message."""
    raw = _envelope(
        [
            {
                "id": "task-bulk-metrics",
                "status_code": 40501,
                "status_message": "Invalid Field: 'targets'.",
                "cost": "0.0",
                "result_count": 0,
                "path": ["v3", "backlinks", "bulk_ranks", "live"],
                "data": {"targets": []},
                "result": None,
            }
        ]
    )
    assert raw["status_message"] == "Ok."  # the envelope itself succeeded
    client = DataForSeoClient(ReplayTransport([raw]))
    response = await client.execute(
        DataForSeoOperationRequest(
            operation=DataForSeoOperationName.BACKLINKS_BULK_METRICS,
            tasks=[{"targets": []}],
            endpoint="/v3/backlinks/bulk_ranks/live",
        )
    )
    assert response.error is not None
    assert response.error["message"] != "Ok."
    assert "Invalid Field" in response.error["message"]
    assert response.error["tasks"][0]["status_code"] == 40501


@pytest.mark.asyncio
async def test_live_flow_no_search_results_is_successful_empty_evidence() -> None:
    """40102 is a completed search with an empty answer, including Business
    Data listing lookups. The live path must agree with the standard-task path
    instead of failing the collection and firing a false ingestion alarm."""
    raw = _envelope(
        [
            {
                "id": "task-no-match",
                "status_code": 40102,
                "status_message": "No Search Results.",
                "cost": "0.0054",
                "result_count": 0,
                "path": ["v3", "business_data", "google", "my_business_info", "live"],
                "data": {"keyword": "A business that is not listed"},
                "result": None,
            }
        ],
        cost="0.0054",
    )
    response = await DataForSeoClient(ReplayTransport([raw])).execute(
        DataForSeoOperationRequest(
            operation=DataForSeoOperationName.BUSINESS_GOOGLE_MY_BUSINESS_INFO,
            tasks=[{"keyword": "A business that is not listed"}],
        )
    )

    assert response.error is None
    assert response.raw["tasks"][0]["status_code"] == 40102
    assert response.call_records[0].metadata["status_code"] == 40102


@pytest.mark.asyncio
async def test_live_flow_uses_decimal_cost_and_preserves_task_tag() -> None:
    raw = _envelope(
        [_task("task-live", status_code=20000, cost="0.01212", result=[{"keyword": "x"}])],
        cost="0.01212",
    )
    client = DataForSeoClient(ReplayTransport([raw]))
    response = await client.execute(
        DataForSeoOperationRequest(
            operation=DataForSeoOperationName.LABS_GOOGLE_KEYWORD_IDEAS,
            tasks=[{"keywords": ["x"]}],
        )
    )
    assert response.reported_cost == Decimal("0.01212")
    assert response.call_records[0].external_task_id == "task-live"
    assert response.call_records[0].metadata["tag"] == "tag-task-live"
    assert response.call_records[0].metadata["requests"] == [
        {
            "method": "POST",
            "url": "/v3/dataforseo_labs/google/keyword_ideas/live",
            "headers": {},
            "json": [{"keywords": ["x"]}],
        }
    ]


@pytest.mark.asyncio
async def test_standard_100_tasks_checkpoint_poll_fairly_and_dedupe_cost() -> None:
    task_ids = [f"task-{index:03d}" for index in range(100)]
    post = _envelope([_task(task_id, status_code=20100) for task_id in task_ids], cost="0.06")
    gets = [
        _envelope([_task(task_id, status_code=20000, cost="0", result=[{"ok": True}])])
        for task_id in task_ids
    ]
    transport = ReplayTransport([post, *gets])
    sleeps: list[float] = []

    async def sleeper(delay: float) -> None:
        sleeps.append(delay)

    client = DataForSeoClient(
        transport,
        sleeper=sleeper,
        polling_policy=PollingPolicy(0, 0, 60),
    )
    repository = InMemorySeoRepository()
    request = _collection_request()
    run = await repository.start_run("dataforseo", request)
    response = await client.execute(
        DataForSeoOperationRequest(
            operation=DataForSeoOperationName.SERP_GOOGLE_ORGANIC_ADVANCED,
            workflow=DataForSeoWorkflow.STANDARD,
            tasks=[{"keyword": task_id} for task_id in task_ids],
        ),
        ProviderExecutionContext(repository, run),
    )
    assert len(_provider_task_rows(repository)) == 100
    assert len(response.call_records) == 100
    assert response.reported_cost == Decimal("0.0600")
    assert sleeps == []
    assert len(transport.requests) == 101

    envelope = RawPayloadEnvelope(payload=response.raw, checksum="checksum", size_bytes=1)
    await repository.persist_raw(run, response, envelope)
    await repository.persist_raw(run, response, envelope)
    row = repository.runs[run.idempotency_key]
    assert len(repository.provider_calls) == 100
    assert row["provider_cost"] == Decimal("0.0600")
    assert row["request_count"] == 101


@pytest.mark.asyncio
async def test_completed_checkpoints_resume_without_post_or_poll() -> None:
    repository = InMemorySeoRepository()
    run = await repository.start_run("dataforseo", _collection_request())
    execution = ProviderExecutionContext(repository, run)
    for index in range(3):
        task_id = f"resume-{index}"
        task = _task(task_id, status_code=20000, result=[{"ok": True}])
        from matrx_seo.contracts import ProviderTaskCheckpoint

        await execution.checkpoint(
            ProviderTaskCheckpoint(
                external_task_id=task_id,
                endpoint="/v3/serp/google/organic/task_post",
                status="completed",
                response_payload=task,
                request_count=2,
                provider_cost=Decimal("0.0006"),
                completed_at=datetime.now(UTC),
            )
        )
    transport = ReplayTransport([])
    client = DataForSeoClient(
        transport,
        polling_policy=PollingPolicy(0, 0, 60),
    )
    response = await client.execute(
        DataForSeoOperationRequest(
            operation=DataForSeoOperationName.SERP_GOOGLE_ORGANIC_ADVANCED,
            workflow=DataForSeoWorkflow.STANDARD,
            tasks=[{"keyword": "ignored-on-resume"}],
        ),
        execution,
    )
    assert len(response.call_records) == 3
    assert transport.requests == []


def test_call_record_validation_and_unknown_aggregate_semantics() -> None:
    with pytest.raises(ValidationError):
        ProviderCallRecord(provider_call_key=" ", request_count=0, reported_cost=-1)
    response = ProviderResponse(
        raw={},
        call_records=[
            ProviderCallRecord(provider_call_key="a", reported_cost=Decimal("1")),
            ProviderCallRecord(provider_call_key="b", reported_cost=None),
        ],
    )
    assert response.reported_cost is None
    assert response.estimated_cost is None


@pytest.mark.asyncio
async def test_partial_standard_post_drains_accepted_tasks_and_preserves_failure() -> None:
    post = _envelope(
        [
            _task("accepted-a", status_code=20100),
            _task("rejected", status_code=40501, cost="0"),
            _task("accepted-b", status_code=20100),
        ]
    )
    gets = [
        _envelope([_task("accepted-a", status_code=20000, cost="0", result=[{}])]),
        _envelope([_task("accepted-b", status_code=20000, cost="0", result=[{}])]),
    ]
    transport = ReplayTransport([post, *gets])
    repository = InMemorySeoRepository()
    run = await repository.start_run("dataforseo", _collection_request())
    client = DataForSeoClient(
        transport,
        polling_policy=PollingPolicy(0, 0, 60),
    )
    response = await client.execute(
        DataForSeoOperationRequest(
            operation=DataForSeoOperationName.SERP_GOOGLE_ORGANIC_ADVANCED,
            workflow=DataForSeoWorkflow.STANDARD,
            tasks=[{"keyword": "a"}, {"keyword": "bad"}, {"keyword": "b"}],
        ),
        ProviderExecutionContext(repository, run),
    )
    assert len(_provider_task_rows(repository)) == 3
    assert {record.external_task_id for record in response.call_records} == {
        "accepted-a",
        "rejected",
        "accepted-b",
    }
    assert response.request_count == 3
    assert response.error is not None
    assert len(transport.requests) == 3


@pytest.mark.asyncio
async def test_all_100_rejected_tasks_account_one_shared_post_request() -> None:
    post = _envelope(
        [_task(f"rejected-{index}", status_code=40501, cost="0") for index in range(100)]
    )
    repository = InMemorySeoRepository()
    run = await repository.start_run("dataforseo", _collection_request())
    response = await DataForSeoClient(
        ReplayTransport([post]),
        polling_policy=PollingPolicy(0, 0, 60),
    ).execute(
        DataForSeoOperationRequest(
            operation=DataForSeoOperationName.SERP_GOOGLE_ORGANIC_ADVANCED,
            workflow=DataForSeoWorkflow.STANDARD,
            tasks=[{"keyword": str(index)} for index in range(100)],
        ),
        ProviderExecutionContext(repository, run),
    )
    assert len(response.call_records) == 100
    assert response.request_count == 1
    assert sum(record.request_count for record in response.call_records) == 1


@pytest.mark.asyncio
async def test_extra_accepted_post_task_is_drained_but_batch_fails_closed() -> None:
    post = _envelope(
        [_task("requested", status_code=20100), _task("unexpected", status_code=20100)]
    )
    gets = [
        _envelope([_task("requested", status_code=20000, cost="0", result=[{}])]),
        _envelope([_task("unexpected", status_code=20000, cost="0", result=[{}])]),
    ]
    repository = InMemorySeoRepository()
    run = await repository.start_run("dataforseo", _collection_request())
    response = await DataForSeoClient(
        ReplayTransport([post, *gets]),
        polling_policy=PollingPolicy(0, 0, 60),
    ).execute(
        DataForSeoOperationRequest(
            operation=DataForSeoOperationName.SERP_GOOGLE_ORGANIC_ADVANCED,
            workflow=DataForSeoWorkflow.STANDARD,
            tasks=[{"keyword": "requested"}],
        ),
        ProviderExecutionContext(repository, run),
    )
    assert len(_provider_task_rows(repository)) == 2
    assert response.error["type"] == "DataForSeoTaskBatchError"
    assert response.error["cardinality"] == {"expected": 1, "received": 2}
    assert response.request_count == 3


@pytest.mark.asyncio
async def test_missing_post_task_is_represented_and_batch_fails_closed() -> None:
    post = _envelope([_task("returned", status_code=20100)])
    completed = _envelope([_task("returned", status_code=20000, cost="0", result=[{}])])
    repository = InMemorySeoRepository()
    run = await repository.start_run("dataforseo", _collection_request())
    response = await DataForSeoClient(
        ReplayTransport([post, completed]),
        polling_policy=PollingPolicy(0, 0, 60),
    ).execute(
        DataForSeoOperationRequest(
            operation=DataForSeoOperationName.SERP_GOOGLE_ORGANIC_ADVANCED,
            workflow=DataForSeoWorkflow.STANDARD,
            tasks=[{"keyword": "returned"}, {"keyword": "omitted"}],
        ),
        ProviderExecutionContext(repository, run),
    )
    assert len(_provider_task_rows(repository)) == 2
    assert response.error["cardinality"] == {"expected": 2, "received": 1}
    assert any(task["status_code"] == 50001 for task in response.error["tasks"])


@pytest.mark.asyncio
async def test_middle_poll_transport_failure_does_not_cancel_siblings() -> None:
    class ScriptedTransport:
        def __init__(self, outcomes):
            self.outcomes = list(outcomes)

        async def request(self, _method, _path, *, json_body=None):
            from matrx_seo.providers.dataforseo.transport import JsonResponse

            outcome = self.outcomes.pop(0)
            if isinstance(outcome, Exception):
                raise outcome
            return JsonResponse(outcome, {})

    post = _envelope([_task(f"task-{index}", status_code=20100) for index in range(3)])
    get_a = _envelope([_task("task-0", status_code=20000, cost="0", result=[{}])])
    get_c = _envelope([_task("task-2", status_code=20000, cost="0", result=[{}])])
    repository = InMemorySeoRepository()
    run = await repository.start_run("dataforseo", _collection_request())
    response = await DataForSeoClient(
        ScriptedTransport([post, get_a, RuntimeError("poll failed"), get_c]),
        polling_policy=PollingPolicy(0, 0, 60),
    ).execute(
        DataForSeoOperationRequest(
            operation=DataForSeoOperationName.SERP_GOOGLE_ORGANIC_ADVANCED,
            workflow=DataForSeoWorkflow.STANDARD,
            tasks=[{"keyword": str(index)} for index in range(3)],
        ),
        ProviderExecutionContext(repository, run),
    )
    assert response.error is not None
    task_rows = _provider_task_rows(repository)
    assert len(task_rows) == 3
    assert sum(value["task"].status == "completed" for value in task_rows) == 2
    await repository.persist_raw(
        run,
        response,
        RawPayloadEnvelope(payload=response.raw, checksum="partial", size_bytes=1),
    )
    assert len(repository.provider_calls) == 3


@pytest.mark.asyncio
async def test_timeout_settles_failed_without_extra_request() -> None:
    monotonic_values = iter([0.0, 2.0])
    repository = InMemorySeoRepository()
    run = await repository.start_run("dataforseo", _collection_request())
    transport = ReplayTransport([_envelope([_task("timeout", status_code=20100)])])
    response = await DataForSeoClient(
        transport,
        monotonic=lambda: next(monotonic_values),
        polling_policy=PollingPolicy(0, 0, 1),
    ).execute(
        DataForSeoOperationRequest(
            operation=DataForSeoOperationName.SERP_GOOGLE_ORGANIC_ADVANCED,
            workflow=DataForSeoWorkflow.STANDARD,
            tasks=[{"keyword": "timeout"}],
        ),
        ProviderExecutionContext(repository, run),
    )
    checkpoint = _provider_task_rows(repository)[0]["task"]
    assert checkpoint.status == "failed"
    assert checkpoint.error["status_code"] == 40800
    assert response.request_count == 1
    assert len(transport.requests) == 1


@pytest.mark.asyncio
async def test_pre_envelope_transport_failure_is_persistable_and_not_reposted() -> None:
    from matrx_seo.providers.dataforseo.transport import DataForSeoTransportError

    repository = InMemorySeoRepository()
    run = await repository.start_run("dataforseo", _collection_request())
    execution = ProviderExecutionContext(repository, run)
    transport = ReplayTransport([])

    async def fail_request(*_args, **_kwargs):
        raise DataForSeoTransportError(
            "network exhausted",
            attempts=4,
            status_code=503,
            headers={"Retry-After": "1"},
            response_body="temporarily unavailable",
        )

    transport.request = fail_request
    operation_request = DataForSeoOperationRequest(
        operation=DataForSeoOperationName.SERP_GOOGLE_ORGANIC_ADVANCED,
        workflow=DataForSeoWorkflow.STANDARD,
        tasks=[{"keyword": "failure"}],
    )
    client = DataForSeoClient(transport, polling_policy=PollingPolicy(0, 0, 60))
    response = await client.execute(operation_request, execution)
    assert response.error["status_code"] == 503
    assert response.request_count == 4
    assert response.raw["_matrx_transport_failure"]["response_body"] == ("temporarily unavailable")
    await repository.persist_raw(
        run,
        response,
        RawPayloadEnvelope(payload=response.raw, checksum="transport", size_bytes=1),
    )
    second = await client.execute(operation_request, execution)
    assert second.error["type"] == "DataForSeoSubmissionUncertain"
    assert second.call_records[0].provider_call_key == response.call_records[0].provider_call_key
    await repository.persist_raw(
        run,
        second,
        RawPayloadEnvelope(payload=second.raw, checksum="uncertain", size_bytes=1),
    )
    assert len(repository.provider_calls) == 1


@pytest.mark.asyncio
async def test_partial_resume_state_fails_closed_without_reposting() -> None:
    from matrx_seo.contracts import ProviderTaskCheckpoint

    repository = InMemorySeoRepository()
    run = await repository.start_run("dataforseo", _collection_request())
    execution = ProviderExecutionContext(repository, run)
    await execution.checkpoint(
        ProviderTaskCheckpoint(
            external_task_id="only-one",
            endpoint="/v3/serp/google/organic/task_post",
            status="completed",
            request_payload={"keyword": "one"},
            response_payload=_task("only-one", status_code=20000, result=[{}]),
            request_count=2,
        )
    )
    transport = ReplayTransport([])
    response = await DataForSeoClient(transport).execute(
        DataForSeoOperationRequest(
            operation=DataForSeoOperationName.SERP_GOOGLE_ORGANIC_ADVANCED,
            workflow=DataForSeoWorkflow.STANDARD,
            tasks=[{"keyword": "one"}, {"keyword": "two"}],
        ),
        execution,
    )
    assert response.error["type"] == "DataForSeoResumeStateMismatch"
    assert transport.requests == []


@pytest.mark.asyncio
async def test_checkpoint_many_cross_run_conflict_does_not_mutate_owner() -> None:
    from matrx_seo.contracts import ProviderTaskCheckpoint

    repository = InMemorySeoRepository()
    first_run = await repository.start_run("dataforseo", _collection_request())
    second_request = _collection_request().model_copy(update={"observation_period": "2026-07-22"})
    second_run = await repository.start_run("dataforseo", second_request)
    first_task = ProviderTaskCheckpoint(
        external_task_id="shared-task",
        status="submitted",
    )
    await repository.checkpoint_provider_tasks(first_run, [first_task])
    with pytest.raises(ValueError, match="another collection run"):
        await repository.checkpoint_provider_tasks(
            second_run,
            [first_task.model_copy(update={"status": "failed"})],
        )
    stored = repository.provider_tasks["dataforseo:shared-task"]
    assert stored["run_id"] == first_run.id
    assert stored["task"].status == "submitted"


@pytest.mark.asyncio
async def test_owned_transport_close_failure_keeps_successful_response(monkeypatch) -> None:
    from matrx_seo.contracts import ResolvedCredential
    from matrx_seo.providers.dataforseo import DataForSeoAdapter
    from matrx_seo.providers.dataforseo import adapter as adapter_module

    class ClosingTransport(ReplayTransport):
        async def aclose(self):
            raise RuntimeError("close failed")

    transport = ClosingTransport(
        [
            _envelope(
                [
                    _task(
                        "live",
                        status_code=20000,
                        result=[{"keyword": "x"}],
                    )
                ]
            )
        ]
    )
    monkeypatch.setattr(adapter_module, "AsyncHttpTransport", lambda **_kwargs: transport)
    adapter = DataForSeoAdapter()
    await adapter.authenticate(
        ResolvedCredential(
            values={
                "DATA_FOR_SEO_EMAIL": "fixture@example.invalid",
                "DATA_FOR_SEO_PASSWORD": "fixture",
            }
        )
    )
    repository = InMemorySeoRepository()
    request = _collection_request("keywords.google_ads.search_volume").model_copy(
        update={
            "capability": SeoCapability.KEYWORD_METRICS,
            "settings": {"workflow": "live", "tasks": [{"keywords": ["x"]}]},
        }
    )
    run = await repository.start_run("dataforseo", request)
    response = await adapter.collect_response(
        request,
        ProviderExecutionContext(repository, run),
    )
    assert response.error is None
    assert response.external_task_id == "live"


@pytest.mark.asyncio
async def test_provider_error_is_persisted_before_collection_fails() -> None:
    raw = _envelope([_task("paid-error", status_code=40501, cost="0.06")], cost="0.06")
    from matrx_seo.contracts import ResolvedCredential
    from matrx_seo.providers.dataforseo import DataForSeoAdapter

    adapter = DataForSeoAdapter(transport=ReplayTransport([raw]))
    repository = InMemorySeoRepository()

    async def credential_resolver(*_: object) -> ResolvedCredential:
        return ResolvedCredential(
            values={
                "DATA_FOR_SEO_EMAIL": "fixture@example.invalid",
                "DATA_FOR_SEO_PASSWORD": "fixture",
            }
        )

    async def authorize(request: CollectionRequest) -> CollectionRequest:
        return request

    request = _collection_request("labs.google.relevant_pages").model_copy(
        update={
            "capability": SeoCapability.RAW_PROVIDER,
            "settings": {"workflow": "live", "tasks": [{"target": "invalid"}]},
        }
    )
    service = SeoCollectionService(
        repository,
        credential_resolver=credential_resolver,
        collection_authorizer=authorize,
    )
    with pytest.raises(ProviderResponseError):
        await service.collect(adapter, request)
    assert len(repository.raw_payloads) == 1
    assert len(repository.provider_calls) == 1
    run_row = next(iter(repository.runs.values()))
    assert run_row["provider_cost"] == Decimal("0.06")
    assert run_row["status"] == "failed"


@pytest.mark.asyncio
async def test_on_page_waits_for_completion_and_fetches_bounded_results() -> None:
    post = _envelope([_task("crawl", status_code=20100)])
    in_progress = _envelope(
        [
            _task(
                "crawl",
                status_code=20000,
                result=[{"crawl_progress": "in_progress"}],
            )
        ]
    )
    completed = _envelope(
        [
            _task(
                "crawl",
                status_code=20000,
                result=[{"crawl_status": "finished"}],
            )
        ]
    )
    pages_response = _envelope(
        [
            _task(
                "crawl",
                status_code=20000,
                result=[
                    {
                        "items": [{"url": "https://example.invalid/"}],
                        "items_count": 1,
                        "total_count": 1,
                    }
                ],
            )
        ]
    )
    empty_result = _envelope([_task("crawl", status_code=20000, result=[{"items": []}])])
    transport = ReplayTransport(
        [post, in_progress, completed, pages_response, empty_result, empty_result, empty_result]
    )
    repository = InMemorySeoRepository()
    request = _collection_request("on_page.crawl").model_copy(
        update={"capability": SeoCapability.RAW_PROVIDER}
    )
    run = await repository.start_run("dataforseo", request)
    client = DataForSeoClient(
        transport,
        polling_policy=PollingPolicy(0, 0, 60),
    )
    response = await client.execute(
        DataForSeoOperationRequest(
            operation=DataForSeoOperationName.ON_PAGE_CRAWL,
            workflow=DataForSeoWorkflow.STANDARD,
            tasks=[{"target": "example.invalid", "max_crawl_pages": 5}],
        ),
        ProviderExecutionContext(repository, run),
    )
    assert response.error is None
    assert len(transport.requests) == 7
    assert len(response.call_records[0].metadata["requests"]) == 7
    assert response.call_records[0].metadata["requests"][-1]["url"].startswith("/v3/on_page/")
    assert transport.requests[-4:] == [
        ("POST", "/v3/on_page/pages", [{"id": "crawl", "limit": 5, "offset": 0}]),
        ("POST", "/v3/on_page/resources", [{"id": "crawl", "limit": 5, "offset": 0}]),
        (
            "POST",
            "/v3/on_page/duplicate_tags",
            [{"id": "crawl", "limit": 5, "offset": 0, "type": "duplicate_description"}],
        ),
        (
            "POST",
            "/v3/on_page/keyword_density",
            [
                {
                    "id": "crawl",
                    "url": "https://example.invalid/",
                    "keyword_length": 1,
                }
            ],
        ),
    ]


@pytest.mark.asyncio
async def test_on_page_paginates_and_result_failure_does_not_cancel_sibling() -> None:
    from matrx_seo.providers.dataforseo.transport import JsonResponse

    class RoutedTransport:
        def __init__(self) -> None:
            self.requests = []

        async def request(self, method, path, *, json_body=None):
            self.requests.append((method, path, json_body))
            if path.endswith("task_post"):
                return JsonResponse(
                    _envelope(
                        [_task("crawl-a", status_code=20100), _task("crawl-b", status_code=20100)]
                    ),
                    {},
                )
            if method == "GET":
                task_id = path.rsplit("/", 1)[-1]
                return JsonResponse(
                    _envelope(
                        [
                            _task(
                                task_id,
                                status_code=20000,
                                result=[{"crawl_status": "finished"}],
                            )
                        ]
                    ),
                    {},
                )
            task_id = json_body[0]["id"]
            offset = json_body[0]["offset"]
            if task_id == "crawl-a" and path.endswith("/pages"):
                raise RuntimeError("pages unavailable")
            count = 1_000 if task_id == "crawl-b" and offset == 0 else 500
            if not path.endswith("/pages"):
                count = 0
            return JsonResponse(
                _envelope(
                    [
                        _task(
                            task_id,
                            status_code=20000,
                            result=[{"items_count": count, "total_count": 1_500, "items": []}],
                        )
                    ]
                ),
                {},
            )

    repository = InMemorySeoRepository()
    request = _collection_request("on_page.crawl").model_copy(
        update={"capability": SeoCapability.RAW_PROVIDER}
    )
    run = await repository.start_run("dataforseo", request)
    transport = RoutedTransport()
    response = await DataForSeoClient(
        transport,
        polling_policy=PollingPolicy(0, 0, 60),
    ).execute(
        DataForSeoOperationRequest(
            operation=DataForSeoOperationName.ON_PAGE_CRAWL,
            workflow=DataForSeoWorkflow.STANDARD,
            tasks=[
                {"target": "a.invalid", "max_crawl_pages": 1_500},
                {"target": "b.invalid", "max_crawl_pages": 1_500},
            ],
        ),
        ProviderExecutionContext(repository, run),
    )
    rows = _provider_task_rows(repository)
    assert {row["task"].status for row in rows} == {"completed", "failed"}
    assert response.error is not None
    pages_b = [
        body[0]["offset"]
        for method, path, body in transport.requests
        if method == "POST" and path.endswith("/pages") and body[0]["id"] == "crawl-b"
    ]
    assert pages_b == [0, 1_000]


@pytest.mark.asyncio
async def test_unknown_cost_stays_unknown_across_separate_persists() -> None:
    repository = InMemorySeoRepository()
    run = await repository.start_run("provider", _collection_request())
    first = ProviderResponse(
        raw={"first": True},
        call_records=[ProviderCallRecord(provider_call_key="unknown")],
    )
    second = ProviderResponse(
        raw={"second": True},
        call_records=[ProviderCallRecord(provider_call_key="known", reported_cost=Decimal("2"))],
    )
    await repository.persist_raw(
        run,
        first,
        RawPayloadEnvelope(payload=first.raw, checksum="first", size_bytes=1),
    )
    await repository.persist_raw(
        run,
        second,
        RawPayloadEnvelope(payload=second.raw, checksum="second", size_bytes=1),
    )
    assert repository.runs[run.idempotency_key]["provider_cost"] is None


@pytest.mark.asyncio
async def test_catalog_cache_and_limits() -> None:
    raw = _envelope(
        [
            _task(
                "catalog",
                status_code=20000,
                result=[
                    {
                        "location_code": 2840,
                        "location_name": "United States",
                        "country_iso_code": "US",
                    }
                ],
            )
        ]
    )
    transport = ReplayTransport([raw])
    client = DataForSeoClient(transport)
    assert (await client.locations())[0].location_code == 2840
    assert (await client.locations())[0].country_iso_code == "US"
    assert len(transport.requests) == 1
    with pytest.raises(ValidationError):
        DataForSeoOperationRequest(
            operation=DataForSeoOperationName.SERP_GOOGLE_ORGANIC_ADVANCED,
            tasks=[{}] * 101,
        )
    with pytest.raises(ValueError):
        AdaptiveRateLimiter(calls_per_minute=0)


@pytest.mark.asyncio
async def test_google_ads_search_volume_normalizes_to_keyword_market() -> None:
    from matrx_seo.providers.dataforseo import DataForSeoAdapter

    live = _envelope(
        [
            _task(
                "volume-task",
                status_code=20000,
                result=[
                    {
                        "keyword": "seo platform",
                        "location_code": 2840,
                        "language_code": "en",
                        "search_volume": 100,
                        "competition": "HIGH",
                        "competition_index": 87,
                        "cpc": 4.25,
                        "low_top_of_page_bid": 1.1,
                        "high_top_of_page_bid": 6.2,
                        "search_intent": "commercial",
                        "monthly_searches": [
                            {"year": 2026, "month": 6, "search_volume": 120},
                            {"year": 2026, "month": 5, "search_volume": 90},
                        ],
                    }
                ],
            )
        ]
    )
    adapter = DataForSeoAdapter(transport=ReplayTransport([live]))
    await adapter.authenticate(
        ResolvedCredential(
            values={
                "DATA_FOR_SEO_EMAIL": "fixture@example.invalid",
                "DATA_FOR_SEO_PASSWORD": "fixture",
            }
        )
    )
    request = _collection_request("keywords.google_ads.search_volume").model_copy(
        update={
            "capability": SeoCapability.KEYWORD_METRICS,
            "settings": {
                "workflow": "live",
                "tasks": [
                    {
                        "keywords": ["seo platform"],
                        "location_code": 2840,
                        "language_code": "en",
                    }
                ],
            },
        }
    )
    repository = InMemorySeoRepository()
    run = await repository.start_run("dataforseo", request)
    response = await adapter.collect_response(request, ProviderExecutionContext(repository, run))
    captured = []

    class IdentityResolver:
        async def resolve_many(self, _request, identities):
            captured.extend(identities)
            return [ResolvedSeoIdentity(keyword_id="keyword-id") for _ in identities]

    observations = await adapter.normalize(
        response,
        NormalizationContext(
            request=request,
            run=run,
            raw_payload_id="raw-id",
            identity_resolver=IdentityResolver(),
            host_binding_resolver=object(),
        ),
    )
    # No location-catalog call — location_code is stored directly.
    assert [path for _, path, _ in adapter._transport.requests] == [
        "/v3/keywords_data/google_ads/search_volume/live"
    ]
    assert captured[0].keyword == "seo platform"
    assert captured[0].language == "en"
    observation = observations[0]
    assert observation.kind == "keyword_market"
    assert observation.keyword_id == "keyword-id"
    assert observation.location_code == 2840
    assert observation.search_volume == 100
    assert observation.competition == "HIGH"
    assert observation.competition_index == 87
    assert str(observation.cpc) == "4.25"
    assert str(observation.low_top_of_page_bid) == "1.1"
    assert str(observation.high_top_of_page_bid) == "6.2"
    assert [item.model_dump() for item in observation.monthly_searches] == [
        {"year": 2026, "month": 6, "search_volume": 120},
        {"year": 2026, "month": 5, "search_volume": 90},
    ]
    assert observation.metrics_task_id == "volume-task"
    # raw is the single result element only — provider intent rides along in
    # raw but is never lifted to a column (the classifier owns intent).
    assert observation.raw["keyword"] == "seo platform"
    assert observation.raw["search_intent"] == "commercial"
    assert not hasattr(observation, "intent")


@pytest.mark.asyncio
async def test_raw_google_ads_collection_skips_large_location_catalog() -> None:
    from matrx_seo.providers.dataforseo import DataForSeoAdapter

    live = _envelope(
        [
            _task(
                "volume-task",
                status_code=20000,
                result=[{"keyword": "seo platform", "search_volume": 100}],
            )
        ]
    )
    transport = ReplayTransport([live])
    adapter = DataForSeoAdapter(transport=transport)
    await adapter.authenticate(
        ResolvedCredential(
            values={
                "DATA_FOR_SEO_EMAIL": "fixture@example.invalid",
                "DATA_FOR_SEO_PASSWORD": "fixture",
            }
        )
    )
    request = _collection_request("keywords.google_ads.search_volume").model_copy(
        update={
            "capability": SeoCapability.RAW_PROVIDER,
            "settings": {
                "workflow": "live",
                "tasks": [
                    {
                        "keywords": ["seo platform"],
                        "location_code": 2840,
                        "language_code": "en",
                    }
                ],
            },
        }
    )
    repository = InMemorySeoRepository()
    run = await repository.start_run("dataforseo", request)

    response = await adapter.collect_response(request, ProviderExecutionContext(repository, run))

    assert [path for _, path, _ in transport.requests] == [
        "/v3/keywords_data/google_ads/search_volume/live"
    ]
    assert "_matrx_location_mappings" not in response.raw


def test_default_standard_polling_starts_promptly() -> None:
    client = DataForSeoClient(ReplayTransport([]))
    keyword_policy = client._policy_for(
        get_operation(DataForSeoOperationName.KEYWORDS_GOOGLE_ADS_SEARCH_VOLUME),
        [{"keywords": ["seo platform"]}],
    )
    serp_policy = client._policy_for(
        get_operation(DataForSeoOperationName.SERP_GOOGLE_ORGANIC_ADVANCED),
        [{"keyword": "seo platform"}],
    )

    assert keyword_policy == PollingPolicy(30, 30, 14_400)
    assert serp_policy == PollingPolicy(10, 10, 2_700)


# ── Google Ads keyword symbol rules (live outage, 2026-08-11) ──────────────


def test_google_ads_rejects_a_question_mark_keyword() -> None:
    """The live phrase that failed the scheduled keyword volume sweep on every
    run for four days, because nothing checked the character set before paying
    for the request and the provider's rejection is opaque."""
    from matrx_seo.providers.dataforseo.contracts import (
        google_ads_search_volume_keyword_rejection_reason,
    )

    reason = google_ads_search_volume_keyword_rejection_reason(
        "what is the best medical spa in sherman oaks?"
    )
    assert reason is not None
    assert "'?'" in reason


@pytest.mark.parametrize("char", list(",=!`<>[]{}()%|?"))
def test_every_disallowed_google_ads_symbol_is_caught(char: str) -> None:
    from matrx_seo.providers.dataforseo.contracts import (
        google_ads_search_volume_keyword_rejection_reason,
    )

    assert google_ads_search_volume_keyword_rejection_reason(f"medical spa{char}") is not None


@pytest.mark.parametrize(
    "keyword",
    [
        "medical spa sherman oaks",
        "best medical spa near me",
        "seo tools 2026",
        "b2b saas pricing",
        "men's haircut",  # apostrophes are fine — do not over-reject
        "e-commerce platform",  # nor hyphens
        "dr. smith dentist",  # nor periods
        "coffee & tea",  # nor ampersands
    ],
)
def test_ordinary_keywords_are_not_rejected(keyword: str) -> None:
    """Over-tightening is a defect: a validator that refuses legitimate
    keywords silently drops real work."""
    from matrx_seo.providers.dataforseo.contracts import (
        google_ads_search_volume_keyword_rejection_reason,
    )

    assert google_ads_search_volume_keyword_rejection_reason(keyword) is None


@pytest.mark.asyncio
async def test_unnormalizable_competitors_request_is_refused_before_any_run() -> None:
    """``seo_collection_failed:dataforseo:competitors`` (2026-08-11 → 2026-09-26):
    the ONLY ``competitors``-capability run ever requested asked for normalized
    observations from ``labs.google.competitors_domain``, which has no canonical
    normalizer. The adapter refused it only AFTER a run was persisted, so the
    request became a failed run and a permanent high-severity platform alarm.
    The refusal now happens at the service boundary: no run, no raw payload,
    no provider call — and the error names the path that works."""
    from matrx_seo.contracts import ResolvedCredential
    from matrx_seo.providers.dataforseo import DataForSeoAdapter

    transport = ReplayTransport([])
    adapter = DataForSeoAdapter(transport=transport)
    repository = InMemorySeoRepository()

    async def credential_resolver(*_: object) -> ResolvedCredential:
        return ResolvedCredential(
            values={
                "DATA_FOR_SEO_EMAIL": "fixture@example.invalid",
                "DATA_FOR_SEO_PASSWORD": "fixture",
            }
        )

    async def authorize(request: CollectionRequest) -> CollectionRequest:
        return request

    request = _collection_request("labs.google.competitors_domain").model_copy(
        update={
            "capability": SeoCapability.COMPETITORS,
            "settings": {"workflow": "live", "tasks": [{"target": "example.com"}]},
        }
    )
    service = SeoCollectionService(
        repository,
        credential_resolver=credential_resolver,
        collection_authorizer=authorize,
    )
    with pytest.raises(ValueError, match="collect it as raw_provider"):
        await service.collect(adapter, request)
    assert repository.runs == {}
    assert repository.raw_payloads == [] or len(repository.raw_payloads) == 0
    assert len(repository.provider_calls) == 0

    # The working path — the same endpoint as raw_provider evidence — is untouched.
    raw_request = request.model_copy(update={"capability": SeoCapability.RAW_PROVIDER})
    assert adapter.unsupported_request_reason(raw_request) is None
