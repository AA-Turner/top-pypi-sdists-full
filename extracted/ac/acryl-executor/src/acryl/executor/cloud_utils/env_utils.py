import os
from typing import Optional, Union

DATAHUB_CLOUD_LOG_PATH_ENV_VAR = "DATAHUB_CLOUD_LOG_PATH"
DATAHUB_CLOUD_LOG_BUCKET_ENV_VAR = "DATAHUB_CLOUD_LOG_BUCKET"
DATAHUB_CLOUD_LOG_CLEANUP_ENV_VAR = "DATAHUB_CLOUD_LOG_CLEANUP"
DEFAULT_GMS_PAYLOAD_MAX_LENGTH = 15368520


def string_to_bool(string: str) -> bool:
    return string.lower() == "true"


def get_executor_pool_id() -> Optional[str]:
    return os.environ.get("DATAHUB_EXECUTOR_POOL_ID")


def get_payload_max_length() -> int:
    val = os.environ.get("ACRYL_EXECUTOR_GMS_PAYLOAD_MAX_LENGTH")
    return int(val) if val and val.isdigit() else DEFAULT_GMS_PAYLOAD_MAX_LENGTH


def get_bundled_venv_path() -> str:
    return os.environ.get("DATAHUB_BUNDLED_VENV_PATH", "/opt/datahub/venvs")


def get_dependency_resolution_enabled() -> bool:
    return string_to_bool(
        os.environ.get("INGESTION_DEPENDENCY_RESOLUTION_ENABLED", "true")
    )


def get_cloud_log_bucket() -> Union[str, None]:
    return os.environ.get("DATAHUB_CLOUD_LOG_BUCKET")


def get_cloud_log_path() -> str:
    return os.environ.get("DATAHUB_CLOUD_LOG_PATH", "")


def get_cloud_log_cleanup() -> bool:
    return string_to_bool(os.environ.get(DATAHUB_CLOUD_LOG_CLEANUP_ENV_VAR, "false"))


def is_datahub_hosted() -> bool:
    return string_to_bool(os.environ.get("DATAHUB_EXECUTOR_INTERNAL_WORKER", "false"))


def get_print_subprocess_logs() -> bool:
    return string_to_bool(
        os.environ.get("DATAHUB_EXECUTOR_PRINT_SUBPROCESS_LOGS", "true")
    )
