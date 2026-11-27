from contextlib import ExitStack
from datetime import timedelta
from types import SimpleNamespace
from typing import Callable, List
from unittest.mock import patch

import pytest
from pydantic import SecretStr, ValidationError
from temporalio.testing import WorkflowEnvironment

from mistralai.workflows import activity
from mistralai.workflows.core.config.config import AppConfig, PayloadCompressionConfig, WorkerConfig
from mistralai.workflows.core.definition.workflow_definition import get_workflow_definition
from mistralai.workflows.core.execution.concurrency._concurrency_workflow import (
    OnBehalfOfParallelExecutionWorkflow,
    ParallelExecutionWorkflow,
)
from mistralai.workflows.core.rate_limiting.rate_limit import RateLimit
from mistralai.workflows.core.worker import _create_temporal_workers, _get_parallel_execution_workflows


class TestAgentServerUrlDefault:
    def test_defaults_to_server_url(self):
        cfg = WorkerConfig(server_url="https://custom.example.com")
        assert cfg.agent.mistral_client_server_url == "https://custom.example.com"

    def test_defaults_to_default_server_url(self):
        cfg = WorkerConfig()
        assert cfg.agent.mistral_client_server_url == "https://api.mistral.ai"

    def test_explicit_value_is_preserved(self):
        cfg = WorkerConfig(
            server_url="https://custom.example.com",
            agent={"mistral_client_server_url": "https://explicit.example.com"},
        )
        assert cfg.agent.mistral_client_server_url == "https://explicit.example.com"

    def test_mistral_api_key_does_not_overwrite_temporal_api_key_source(self, monkeypatch):
        monkeypatch.setenv("MISTRAL_API_KEY", "mistral-key")
        monkeypatch.delenv("TEMPORAL_API_KEY", raising=False)

        cfg = AppConfig()

        assert cfg.common.mistral_api_key == SecretStr("mistral-key")
        assert cfg.temporal.api_key is None

    def test_app_config_reads_temporal_payload_compression(self, monkeypatch):
        monkeypatch.setenv("TEMPORAL_PAYLOAD_COMPRESSION__MIN_SIZE_BYTES", "4096")
        monkeypatch.setenv("TEMPORAL_PAYLOAD_COMPRESSION__ALGORITHM_CONFIG__ALGORITHM", "zstd")
        monkeypatch.setenv("TEMPORAL_PAYLOAD_COMPRESSION__ALGORITHM_CONFIG__LEVEL", "5")

        cfg = AppConfig()

        assert cfg.worker.temporal_payload_compression == PayloadCompressionConfig(
            min_size_bytes=4096,
            algorithm_config={"algorithm": "zstd", "level": 5},
        )

    def test_max_concurrent_activities_defaults_to_the_temporal_default(self):
        assert WorkerConfig().max_concurrent_activities == 100

    def test_max_concurrent_activities_rejects_zero(self):
        # Temporal's create_fixed treats a falsy slot count as "unset" and silently restores 100.
        with pytest.raises(ValidationError):
            WorkerConfig(max_concurrent_activities=0)

    @pytest.mark.asyncio
    async def test_max_concurrent_activities_reaches_every_temporal_worker(
        self, temporal_env: WorkflowEnvironment, monkeypatch
    ):
        monkeypatch.setenv("MAX_CONCURRENT_ACTIVITIES", "1")

        with (
            patch("mistralai.workflows.core.worker.get_all_temporal_activities", return_value=[]),
            ExitStack() as registrations,
        ):
            workers, _ = _create_temporal_workers(
                temporal_client=temporal_env.client,
                workflows=[],
                config=AppConfig(worker={"local_retry_backoff_coefficient": 0}),
                task_queue="test-task-queue",
                workflow_config_registrations=registrations,
            )

            assert {worker.config()["max_concurrent_activities"] for worker in workers} == {1}

    def test_connection_stream_limit_defaults_to_100(self):
        assert WorkerConfig().connection_stream_limit == 100

    def test_connection_stream_limit_can_be_disabled_with_null(self, monkeypatch):
        monkeypatch.setenv("CONNECTION_STREAM_LIMIT", "null")

        assert AppConfig().worker.connection_stream_limit is None

    def test_connection_stream_limit_rejects_zero(self):
        with pytest.raises(ValidationError):
            WorkerConfig(connection_stream_limit=0)

    def test_max_cached_workflows_defaults_to_the_temporal_default(self):
        assert WorkerConfig().max_cached_workflows == 1000

    def test_max_cached_workflows_rejects_zero(self):
        with pytest.raises(ValidationError):
            WorkerConfig(max_cached_workflows=0)

    @pytest.mark.asyncio
    async def test_max_cached_workflows_reaches_every_temporal_worker(
        self, temporal_env: WorkflowEnvironment, monkeypatch
    ):
        monkeypatch.setenv("MAX_CACHED_WORKFLOWS", "64")

        with (
            patch("mistralai.workflows.core.worker.get_all_temporal_activities", return_value=[]),
            ExitStack() as registrations,
        ):
            workers, _ = _create_temporal_workers(
                temporal_client=temporal_env.client,
                workflows=[],
                config=AppConfig(worker={"local_retry_backoff_coefficient": 0}),
                task_queue="test-task-queue",
                workflow_config_registrations=registrations,
            )

            assert {worker.config()["max_cached_workflows"] for worker in workers} == {64}

    def test_graceful_shutdown_timeout_defaults_below_the_kubernetes_grace_period(self):
        assert WorkerConfig().graceful_shutdown_timeout_seconds == 25

    def test_graceful_shutdown_timeout_rejects_a_negative_value(self):
        with pytest.raises(ValidationError):
            WorkerConfig(graceful_shutdown_timeout_seconds=-1)

    @pytest.mark.asyncio
    async def test_graceful_shutdown_timeout_reaches_every_temporal_worker(
        self, temporal_env: WorkflowEnvironment, monkeypatch
    ):
        monkeypatch.setenv("GRACEFUL_SHUTDOWN_TIMEOUT_SECONDS", "7")

        with (
            patch("mistralai.workflows.core.worker.get_all_temporal_activities", return_value=[]),
            ExitStack() as registrations,
        ):
            workers, _ = _create_temporal_workers(
                temporal_client=temporal_env.client,
                workflows=[],
                config=AppConfig(worker={"local_retry_backoff_coefficient": 0}),
                task_queue="test-task-queue",
                workflow_config_registrations=registrations,
            )

            assert {worker.config()["graceful_shutdown_timeout"] for worker in workers} == {timedelta(seconds=7)}


def test_obo_parallel_workflow_is_only_registered_for_obo_workers() -> None:
    non_obo_workflow = type(
        "NonOboWorkflow",
        (),
        {"__workflows_workflow_def": SimpleNamespace(on_behalf_of=False)},
    )
    obo_workflow = type(
        "OboWorkflow",
        (),
        {"__workflows_workflow_def": SimpleNamespace(on_behalf_of=True)},
    )

    assert _get_parallel_execution_workflows([non_obo_workflow]) == [ParallelExecutionWorkflow]
    assert _get_parallel_execution_workflows([obo_workflow]) == [
        ParallelExecutionWorkflow,
        OnBehalfOfParallelExecutionWorkflow,
    ]
    assert get_workflow_definition(ParallelExecutionWorkflow).is_technical is True
    assert get_workflow_definition(ParallelExecutionWorkflow).on_behalf_of is False
    assert get_workflow_definition(OnBehalfOfParallelExecutionWorkflow).is_technical is True
    assert get_workflow_definition(OnBehalfOfParallelExecutionWorkflow).on_behalf_of is True


def _build_rate_limited_activities(n_keys: int) -> List[Callable]:
    activities = []
    for i in range(n_keys):

        @activity(
            name=f"rate_limited_activity_{i}",
            rate_limit=RateLimit(time_window_in_sec=1, max_execution=1, key=f"key-{i}"),
            _skip_registering=True,
        )
        async def rate_limited_activity() -> None:
            pass

        activities.append(rate_limited_activity)
    return activities


class TestWorkerPollWarningAtStartup:
    """WFL-3264 acceptance criteria, exercised against `_create_temporal_workers` itself
    (the call site that logs the warning). The underlying math is unit-tested in
    `test_worker_polls.py`; this covers the wiring between the two."""

    @pytest.mark.asyncio
    async def test_warns_with_19_rate_limit_keys_and_default_pollers(
        self, temporal_env: WorkflowEnvironment, caplog: pytest.LogCaptureFixture
    ):
        activities = _build_rate_limited_activities(19)

        with (
            patch("mistralai.workflows.core.worker.get_all_temporal_activities", return_value=activities),
            ExitStack() as registrations,
        ):
            _create_temporal_workers(
                temporal_client=temporal_env.client,
                workflows=[],
                config=AppConfig(worker={"local_retry_backoff_coefficient": 0}),
                task_queue="poll-warning-default-pollers",
                workflow_config_registrations=registrations,
            )

        assert "Worker poll count approaches the Temporal connection's stream limit" in caplog.text
        assert "key-0" in caplog.text
        assert "MAX_ACTIVITY_TASK_POLLERS" in caplog.text

    @pytest.mark.asyncio
    async def test_does_not_warn_with_19_rate_limit_keys_and_lower_activity_pollers(
        self, temporal_env: WorkflowEnvironment, caplog: pytest.LogCaptureFixture
    ):
        activities = _build_rate_limited_activities(19)

        with (
            patch("mistralai.workflows.core.worker.get_all_temporal_activities", return_value=activities),
            ExitStack() as registrations,
        ):
            _create_temporal_workers(
                temporal_client=temporal_env.client,
                workflows=[],
                config=AppConfig(worker={"local_retry_backoff_coefficient": 0, "max_activity_task_pollers": 2}),
                task_queue="poll-warning-lower-pollers",
                workflow_config_registrations=registrations,
            )

        assert "Worker poll count approaches" not in caplog.text

    @pytest.mark.asyncio
    async def test_does_not_warn_when_the_connection_stream_limit_is_disabled(
        self, temporal_env: WorkflowEnvironment, caplog: pytest.LogCaptureFixture
    ):
        activities = _build_rate_limited_activities(19)

        with (
            patch("mistralai.workflows.core.worker.get_all_temporal_activities", return_value=activities),
            ExitStack() as registrations,
        ):
            _create_temporal_workers(
                temporal_client=temporal_env.client,
                workflows=[],
                config=AppConfig(worker={"local_retry_backoff_coefficient": 0, "connection_stream_limit": None}),
                task_queue="poll-warning-no-limit",
                workflow_config_registrations=registrations,
            )

        assert "Worker poll count approaches" not in caplog.text
