from __future__ import annotations

import json
from typing import Union, Literal, TypeVar, Optional, cast
from pathlib import Path

import pydantic

from ._errors import ExperimentError
from .._compat import parse_obj
from .._models import BaseModel
from ._addressing import metadata_path

SCHEMA_VERSION: Literal[1] = 1

RunType = Literal[
    "adme",
    "prediction",
    "protein_design",
    "small_molecule_design",
    "protein_library_screen",
    "small_molecule_library_screen",
]
DownloadMode = Literal["everything", "metadata_only"]

DOWNLOAD_MODE_EVERYTHING: DownloadMode = "everything"
DOWNLOAD_MODE_METADATA_ONLY: DownloadMode = "metadata_only"

_ModelT = TypeVar("_ModelT", bound=BaseModel)


class MetadataHeader(BaseModel):
    schema_version: int


class RemoteState(BaseModel):
    run_id: Optional[str]
    workspace_id: Optional[str]
    status: Optional[str]
    started_at: Optional[str]
    completed_at: Optional[str]
    stopped_at: Optional[str]
    latest_result_id: Optional[str]
    error_code: Optional[str]

    @classmethod
    def empty(cls) -> "RemoteState":
        return cls(
            run_id=None,
            workspace_id=None,
            status=None,
            started_at=None,
            completed_at=None,
            stopped_at=None,
            latest_result_id=None,
            error_code=None,
        )


class PredictionPending(BaseModel):
    kind: Literal["prediction_archive"]

    @classmethod
    def archive(cls) -> "PredictionPending":
        return cls(kind="prediction_archive")


class PipelinePending(BaseModel):
    kind: Literal["result_page"]
    after_id: Optional[str]
    page_last_id: Optional[str]
    result_ids: list[str]

    @classmethod
    def current_page(
        cls,
        *,
        after_id: Optional[str],
        page_last_id: Optional[str],
        result_ids: list[str],
    ) -> "PipelinePending":
        return cls(
            kind="result_page",
            after_id=after_id,
            page_last_id=page_last_id,
            result_ids=result_ids,
        )


PendingState = Optional[Union[PredictionPending, PipelinePending]]


class RunMetadata(BaseModel):
    schema_version: Literal[1] = SCHEMA_VERSION
    name: str
    run_type: RunType
    download_mode: DownloadMode = DOWNLOAD_MODE_EVERYTHING
    request_fingerprint: str
    idempotency_key: str
    remote: RemoteState
    pending: PendingState
    cursor_after_id: Optional[str]

    @classmethod
    def create(
        cls,
        *,
        name: str,
        run_type: RunType,
        download_mode: DownloadMode = DOWNLOAD_MODE_EVERYTHING,
        request_fingerprint: str,
        idempotency_key: str,
    ) -> "RunMetadata":
        return cls(
            name=name,
            run_type=run_type,
            download_mode=download_mode,
            request_fingerprint=request_fingerprint,
            idempotency_key=idempotency_key,
            remote=RemoteState.empty(),
            pending=None,
            cursor_after_id=None,
        )


def normalize_download_mode(value: object) -> DownloadMode:
    if value is None or value == "":
        return DOWNLOAD_MODE_EVERYTHING
    if not isinstance(value, str):
        raise ExperimentError("Invalid `download_mode` in run metadata")

    normalized = value.strip().lower().replace("-", "_")
    if normalized in {"all", DOWNLOAD_MODE_EVERYTHING}:
        return DOWNLOAD_MODE_EVERYTHING
    if normalized == DOWNLOAD_MODE_METADATA_ONLY:
        return DOWNLOAD_MODE_METADATA_ONLY
    raise ExperimentError(f"Unsupported download mode: {value!r}")


def load_metadata(run_dir: Path) -> RunMetadata:
    path = metadata_path(run_dir)
    if not path.exists():
        raise ExperimentError(f"Run metadata does not exist: {path}")

    raw_data: object = json.loads(path.read_text(encoding="utf-8"))
    schema_version = _parse_model(MetadataHeader, raw_data, context="run metadata").schema_version
    if schema_version != SCHEMA_VERSION:
        raise ExperimentError(f"Unsupported experiments metadata schema version: {schema_version!r}")

    return _parse_model(RunMetadata, raw_data, context="run metadata")


def save_metadata(run_dir: Path, metadata: RunMetadata) -> None:
    path = metadata_path(run_dir)
    tmp_path = path.with_suffix(f"{path.suffix}.tmp")
    payload = metadata.to_dict(exclude_unset=False, exclude_defaults=False, exclude_none=False)
    tmp_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    tmp_path.replace(path)


def ensure_directory_ready(run_dir: Path) -> None:
    if run_dir.exists():
        if not run_dir.is_dir():
            raise ExperimentError(f"Run path is not a directory: {run_dir}")
        metadata = metadata_path(run_dir)
        if metadata.exists():
            return
        if any(run_dir.iterdir()):
            raise ExperimentError(
                f"Run directory already exists without experiments metadata: {run_dir}. Choose a different `name`."
            )
        return

    run_dir.mkdir(parents=True, exist_ok=False)


def _parse_model(model: type[_ModelT], data: object, *, context: str) -> _ModelT:
    try:
        return parse_obj(model, data)
    except pydantic.ValidationError as err:
        raise ExperimentError(_format_validation_error(err, context=context)) from err


def _format_validation_error(err: pydantic.ValidationError, *, context: str) -> str:
    error_list = cast(list[dict[str, object]], err.errors())
    if not error_list:
        return f"Invalid {context}"

    first_error = error_list[0]
    message_obj: object = first_error.get("msg")
    message = message_obj if isinstance(message_obj, str) else "invalid value"

    location_obj: object = first_error.get("loc")
    if not isinstance(location_obj, tuple):
        return f"Invalid {context}: {message}"

    path_parts = [str(part) for part in cast(tuple[object, ...], location_obj) if part != "__root__"]
    if not path_parts:
        return f"Invalid {context}: {message}"

    location = ".".join(path_parts)
    return f"Invalid {context}.{location}: {message}"
