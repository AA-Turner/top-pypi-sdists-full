import pytest
from pydantic import ValidationError
from temporalio.testing import WorkflowEnvironment

from mistralai.workflows.core.config.config import AppConfig, PayloadCompressionConfig, WorkerConfig
from mistralai.workflows.core.worker import _create_temporal_workers


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

    def test_app_config_reads_top_level_events_api_version(self, monkeypatch):
        monkeypatch.setenv("EVENTS_API_VERSION", "v2")

        cfg = AppConfig()

        assert cfg.worker.events_api_version == "v2"

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

        workers, _ = _create_temporal_workers(
            temporal_client=temporal_env.client,
            workflows=[],
            config=AppConfig(),
            task_queue="test-task-queue",
        )

        assert {worker.config()["max_concurrent_activities"] for worker in workers} == {1}
