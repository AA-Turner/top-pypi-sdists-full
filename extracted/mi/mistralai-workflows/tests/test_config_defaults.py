from mistralai.workflows.core.config.config import AppConfig, WorkerConfig


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
