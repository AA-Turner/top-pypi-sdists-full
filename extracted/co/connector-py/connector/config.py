import os
from enum import Enum
from pathlib import Path


class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


LOG_LEVEL_ENV_VAR = "LUMOS_LOG_LEVEL"
LOG_DIRECTORY_ENV_VAR = "LUMOS_LOG_DIRECTORY"
LOG_TO_STDOUT_ENV_VAR = "LUMOS_LOG_TO_STDOUT"
ADDITIONAL_REDACTED_LOG_KEYS_ENV_VAR = "LUMOS_ADDITIONAL_REDACTED_LOG_KEYS"
LUMOS_ON_PREMISE_AGENT_SEND_CRITICAL_LOGS_TO_LUMOS_ENV_VAR = (
    "LUMOS_ON_PREMISE_AGENT_SEND_CRITICAL_LOGS_TO_LUMOS"
)
LUMOS_ON_PREMISE_AGENT_API_KEY_ENV_VAR = "LUMOS_ON_PREMISE_AGENT_API_KEY"
LUMOS_AGENT_IDENTIFIER_ENV_VAR = "LUMOS_AGENT_IDENTIFIER"
LUMOS_ON_PREMISE_AGENT_BASE_URL_ENV_VAR = "LUMOS_ON_PREMISE_AGENT_BASE_URL"


class Config:
    def __init__(self) -> None:
        self.log_level: LogLevel = LogLevel.ERROR
        self.log_directory: Path | None = None
        self.log_to_stdout: bool = False
        self.additional_redacted_log_keys: list[str] = []
        self.send_logs_to_on_prem_proxy: bool = False
        self.on_prem_agent_api_key: str | None = None
        self.agent_identifier: str | None = None
        self.base_url: str | None = None
        self.set_log_level()
        self.set_log_directory()
        self.set_log_to_stdout()
        self.set_send_logs_to_on_prem_proxy()
        self.set_additional_redacted_log_keys()
        self.set_on_prem_agent_api_key()
        self.set_agent_identifier()
        self.set_base_url()

    def set_log_level(self) -> None:
        log_level_string = os.environ.get(LOG_LEVEL_ENV_VAR, "ERROR")
        try:
            self.log_level = LogLevel(log_level_string)
        except ValueError as e:
            raise ValueError(
                f"Invalid log level set by environment variable {LOG_LEVEL_ENV_VAR}: {log_level_string}"
            ) from e

    def set_log_directory(self) -> None:
        log_directory_string = os.environ.get(LOG_DIRECTORY_ENV_VAR, None)
        if log_directory_string is not None:
            self.log_directory = Path(log_directory_string)

    def set_log_to_stdout(self) -> None:
        log_to_stdout_string = os.environ.get(LOG_TO_STDOUT_ENV_VAR, "False")
        self.log_to_stdout = log_to_stdout_string.lower() == "true"

    def set_additional_redacted_log_keys(self) -> None:
        additional_redacted_log_keys_string = os.environ.get(
            ADDITIONAL_REDACTED_LOG_KEYS_ENV_VAR, ""
        )
        self.additional_redacted_log_keys = [
            key.strip().lower() for key in additional_redacted_log_keys_string.split(",")
        ]

    def set_send_logs_to_on_prem_proxy(self) -> None:
        send_logs_to_on_prem_proxy_string = os.environ.get(
            LUMOS_ON_PREMISE_AGENT_SEND_CRITICAL_LOGS_TO_LUMOS_ENV_VAR, "False"
        )
        self.send_logs_to_on_prem_proxy = send_logs_to_on_prem_proxy_string.lower() == "true"

    def set_on_prem_agent_api_key(self) -> None:
        on_prem_agent_api_key_string = os.environ.get(LUMOS_ON_PREMISE_AGENT_API_KEY_ENV_VAR, None)
        if on_prem_agent_api_key_string is not None:
            self.on_prem_agent_api_key = on_prem_agent_api_key_string

    def set_agent_identifier(self) -> None:
        agent_identifier_string = os.environ.get(LUMOS_AGENT_IDENTIFIER_ENV_VAR, None)
        if agent_identifier_string is not None:
            self.agent_identifier = agent_identifier_string

    def set_base_url(self) -> None:
        base_url_string = os.environ.get(LUMOS_ON_PREMISE_AGENT_BASE_URL_ENV_VAR, None)
        if base_url_string is not None:
            self.base_url = base_url_string


config = Config()
