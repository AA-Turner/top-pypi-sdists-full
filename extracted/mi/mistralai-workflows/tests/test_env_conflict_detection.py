import logging

import pytest
from pydantic import SecretStr
from structlog.testing import capture_logs

from mistralai.workflows.core.config.config import AgentConfig, CommonConfig, TemporalConfig

LOGGER_NAME = "mistralai.workflows.core.config.config"
MISMATCH_MSG = "Value mismatch between .env file and environment variable"


def _has_mismatch_warning(caplog):
    return any(MISMATCH_MSG in msg for msg in caplog.messages)


class TestEnvDotenvConflictDetection:
    @pytest.mark.parametrize(
        ("config_cls", "variable", "field_name"),
        [
            (CommonConfig, "MISTRAL_API_KEY", "mistral_api_key"),
            (CommonConfig, "MISTRAL_SA_TOKEN_PATH", "mistral_sa_token_path"),
            (TemporalConfig, "TEMPORAL_API_KEY", "api_key"),
            (AgentConfig, "MISTRAL_CLIENT_API_KEY", "mistral_client_api_key"),
        ],
    )
    @pytest.mark.parametrize(
        ("env_value", "dotenv_value"),
        [("from-env-ENVA", "from-dotenv-DOTA"), ("E123", "D456")],
        ids=["long-values", "short-values"],
    )
    def test_warns_without_values_on_mismatch(
        self, monkeypatch, tmp_path, config_cls, variable, field_name, env_value, dotenv_value
    ):
        (tmp_path / ".env.test").write_text(f"{variable}={dotenv_value}\n")
        monkeypatch.setenv(variable, env_value)
        monkeypatch.chdir(tmp_path)

        with capture_logs() as logs:
            cfg = config_cls()

        resolved_value = getattr(cfg, field_name)
        if isinstance(resolved_value, SecretStr):
            resolved_value = resolved_value.get_secret_value()
        assert resolved_value == env_value

        warnings = [log for log in logs if MISMATCH_MSG in log.get("event", "")]
        assert len(warnings) == 1
        warning = warnings[0]
        assert warning["log_level"] == "warning"
        assert warning["env_variable"] == field_name
        assert warning["dotenv_variable"] == field_name
        assert "the environment variable value will take precedence" in warning["event"]
        assert "env_variable_value" not in warning
        assert "dotenv_variable_value" not in warning
        for value in (env_value, dotenv_value):
            assert value not in str(warning)
            assert value[-4:] not in str(warning)

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
