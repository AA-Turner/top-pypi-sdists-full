from mistralai.workflows.core.config.config import AppConfig, PayloadCompressionConfig, WorkerConfig


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
