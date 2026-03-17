from __future__ import annotations

import os
import secrets

from exponent.core.config import get_chat_artifacts_dir

BASH_RESULTS_DIR = "bash_results"
QUERY_RESULTS_DIR = "query_results"
USER_UPLOADS_DIR = "user_uploads"
ARTIFACTS_DIR = "artifacts"
ARTIFACTS_HISTORY_DIR = "artifacts/history"
CONVERSATION_HISTORY_FILENAME = "conversation_history.jsonl"


def generate_bash_id() -> str:
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return "".join(secrets.choice(alphabet) for _ in range(8))


def _paths(chat_uuid: str, relative: str) -> tuple[str, str]:
    return os.path.join(get_chat_artifacts_dir(str(chat_uuid)), relative), relative


def bash_result_path(chat_uuid: str, bash_id: str, epoch_ms: int) -> tuple[str, str]:
    return _paths(chat_uuid, f"{BASH_RESULTS_DIR}/{bash_id}_{epoch_ms}.txt")


def query_result_path(chat_uuid: str, query_id: str, epoch_ms: int, ext: str = "parquet") -> tuple[str, str]:
    return _paths(chat_uuid, f"{QUERY_RESULTS_DIR}/{query_id}_{epoch_ms}.{ext}")


def user_upload_path(chat_uuid: str, sanitized_filename: str) -> tuple[str, str]:
    return _paths(chat_uuid, f"{USER_UPLOADS_DIR}/{sanitized_filename}")


def artifact_path(chat_uuid: str, filename: str) -> tuple[str, str]:
    return _paths(chat_uuid, f"{ARTIFACTS_DIR}/{filename}")


def conversation_history_path(chat_uuid: str) -> tuple[str, str]:
    return _paths(chat_uuid, CONVERSATION_HISTORY_FILENAME)


def s3_artifact_key(filename: str) -> str:
    return f"{ARTIFACTS_DIR}/{filename}"


def s3_artifact_history_key(filename: str, version: int) -> str:
    return f"{ARTIFACTS_HISTORY_DIR}/{filename}/{version}"


def s3_query_result_csv_key(query_id: str, epoch_ms: int) -> str:
    return f"{QUERY_RESULTS_DIR}/{query_id}_{epoch_ms}.csv"


def s3_key_to_local_path(s3_key: str, chat_uuid: str) -> str:
    return os.path.join(get_chat_artifacts_dir(chat_uuid), s3_key)


def local_path_to_s3_key(local_path: str, chat_uuid: str) -> str:
    chat_dir = get_chat_artifacts_dir(chat_uuid)
    return os.path.relpath(local_path, chat_dir)


_SUBDIRS = [
    BASH_RESULTS_DIR,
    QUERY_RESULTS_DIR,
    USER_UPLOADS_DIR,
    ARTIFACTS_HISTORY_DIR,
]


def ensure_chat_directories(chat_uuid: str) -> None:
    chat_dir = get_chat_artifacts_dir(chat_uuid)
    for subdir in _SUBDIRS:
        os.makedirs(os.path.join(chat_dir, subdir), exist_ok=True)
