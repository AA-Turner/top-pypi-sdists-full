import logging

from mistralai.workflows.core.config.config import AgentConfig, CommonConfig, TemporalConfig

LOGGER_NAME = "mistralai.workflows.core.config.config"
MISMATCH_MSG = "Value mismatch between .env file and environment variable"


def _has_mismatch_warning(caplog):
    return any(MISMATCH_MSG in msg for msg in caplog.messages)


class TestEnvDotenvConflictDetection:
    def test_warns_on_mistral_api_key_mismatch(self, monkeypatch, tmp_path, caplog):
        (tmp_path / ".env.test").write_text("MISTRAL_API_KEY=from-dotenv\n")
        monkeypatch.setenv("MISTRAL_API_KEY", "from-env")
        monkeypatch.chdir(tmp_path)

        with caplog.at_level(logging.WARNING, logger=LOGGER_NAME):
            cfg = CommonConfig()

        assert cfg.mistral_api_key.get_secret_value() == "from-env"
        assert _has_mismatch_warning(caplog)

    def test_no_warning_when_values_match(self, monkeypatch, tmp_path, caplog):
        (tmp_path / ".env.test").write_text("MISTRAL_API_KEY=same-value\n")
        monkeypatch.setenv("MISTRAL_API_KEY", "same-value")
        monkeypatch.chdir(tmp_path)

        with caplog.at_level(logging.WARNING, logger=LOGGER_NAME):
            CommonConfig()

        assert not _has_mismatch_warning(caplog)

    def test_no_warning_when_only_env_set(self, monkeypatch, tmp_path, caplog):
        (tmp_path / ".env.test").write_text("\n")
        monkeypatch.setenv("MISTRAL_API_KEY", "from-env")
        monkeypatch.chdir(tmp_path)

        with caplog.at_level(logging.WARNING, logger=LOGGER_NAME):
            CommonConfig()

        assert not _has_mismatch_warning(caplog)

    def test_no_warning_when_only_dotenv_set(self, monkeypatch, tmp_path, caplog):
        (tmp_path / ".env.test").write_text("MISTRAL_API_KEY=from-dotenv\n")
        monkeypatch.delenv("MISTRAL_API_KEY", raising=False)
        monkeypatch.chdir(tmp_path)

        with caplog.at_level(logging.WARNING, logger=LOGGER_NAME):
            CommonConfig()

        assert not _has_mismatch_warning(caplog)

    def test_warns_on_temporal_api_key_mismatch(self, monkeypatch, tmp_path, caplog):
        (tmp_path / ".env.test").write_text("TEMPORAL_API_KEY=from-dotenv\n")
        monkeypatch.setenv("TEMPORAL_API_KEY", "from-env")
        monkeypatch.chdir(tmp_path)

        with caplog.at_level(logging.WARNING, logger=LOGGER_NAME):
            cfg = TemporalConfig()

        assert cfg.api_key.get_secret_value() == "from-env"
        assert _has_mismatch_warning(caplog)

    def test_warns_on_mistral_client_api_key_mismatch(self, monkeypatch, tmp_path, caplog):
        (tmp_path / ".env.test").write_text("MISTRAL_CLIENT_API_KEY=from-dotenv\n")
        monkeypatch.setenv("MISTRAL_CLIENT_API_KEY", "from-env")
        monkeypatch.chdir(tmp_path)

        with caplog.at_level(logging.WARNING, logger=LOGGER_NAME):
            cfg = AgentConfig()

        assert cfg.mistral_client_api_key.get_secret_value() == "from-env"
        assert _has_mismatch_warning(caplog)
