from __future__ import annotations

import time
import uuid
from typing import Generic, Literal, TypeVar, Protocol, cast
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from collections.abc import Callable, Sequence

from ._state import (
    DOWNLOAD_MODE_EVERYTHING,
    DOWNLOAD_MODE_METADATA_ONLY,
    RunType,
    RunMetadata,
    DownloadMode,
    PipelinePending,
    PredictionPending,
    load_metadata,
    save_metadata,
    ensure_directory_ready,
    normalize_download_mode,
)
from ._errors import (
    ExperimentError,
    ExperimentFingerprintMismatchError,
    ExperimentUnsupportedOperationError,
)
from .._client import Boltz
from ._results import write_run_metadata, write_pipeline_result_metadata, append_pipeline_result_metadata
from ._progress import ProgressSink
from ._materialize import (
    pipeline_paths,
    is_materialized,
    prediction_paths,
    materialize_archive,
    prefix_prediction_structure_file,
    prefix_pipeline_result_structure_file,
)

PipelineStatus = Literal["pending", "running", "succeeded", "failed", "stopped"]
PredictionStatus = Literal["pending", "running", "succeeded", "failed"]


class ErrorLike(Protocol):
    @property
    def code(self) -> str: ...


class ProgressLike(Protocol):
    @property
    def latest_result_id(self) -> str | None: ...


class PredictionRunResponseLike(Protocol):
    @property
    def id(self) -> str: ...

    @property
    def status(self) -> str: ...

    @property
    def workspace_id(self) -> str | None: ...

    @property
    def started_at(self) -> datetime | None: ...

    @property
    def completed_at(self) -> datetime | None: ...

    @property
    def error(self) -> ErrorLike | None: ...


class PipelineRunResponseLike(PredictionRunResponseLike, Protocol):
    @property
    def stopped_at(self) -> datetime | None: ...

    @property
    def progress(self) -> ProgressLike | None: ...


class PredictionArchiveLike(Protocol):
    @property
    def url(self) -> str: ...


class PredictionOutputLike(Protocol):
    @property
    def archive(self) -> PredictionArchiveLike | None: ...


class PredictionRetrieveResponseLike(PredictionRunResponseLike, Protocol):
    @property
    def output(self) -> object | None: ...


class PredictionRetrieveArchiveResponseLike(PredictionRunResponseLike, Protocol):
    @property
    def output(self) -> PredictionOutputLike | None: ...


class ResultArchiveLike(Protocol):
    @property
    def url(self) -> str: ...


class ResultArtifactsLike(Protocol):
    @property
    def archive(self) -> ResultArchiveLike: ...


class PipelineResultLike(Protocol):
    @property
    def id(self) -> str: ...

    @property
    def artifacts(self) -> ResultArtifactsLike: ...


class PipelineResultsPageLike(Protocol):
    @property
    def data(self) -> Sequence[PipelineResultLike]: ...

    @property
    def last_id(self) -> str | None: ...


PredictionPayloadT = TypeVar("PredictionPayloadT")
PipelinePayloadT = TypeVar("PipelinePayloadT")


@dataclass(frozen=True)
class PredictionDefinition(Generic[PredictionPayloadT]):
    run_type: RunType
    start_call: Callable[[Boltz, PredictionPayloadT, str, str | None], PredictionRunResponseLike]
    retrieve_call: Callable[[Boltz, str, str | None], PredictionRetrieveResponseLike]
    materialize_archive: bool = True


@dataclass(frozen=True)
class PipelineDefinition(Generic[PipelinePayloadT]):
    run_type: RunType
    start_call: Callable[[Boltz, PipelinePayloadT, str, str | None], PipelineRunResponseLike]
    retrieve_call: Callable[[Boltz, str, str | None], PipelineRunResponseLike]
    list_results_call: Callable[[Boltz, str, str | None, int, str | None], PipelineResultsPageLike]
    stop_call: Callable[[Boltz, str], PipelineRunResponseLike]


class ExperimentEngine:
    def __init__(self, *, client: Boltz, sink: ProgressSink) -> None:
        self._client = client
        self._sink = sink

    def start_prediction(
        self,
        *,
        definition: PredictionDefinition[PredictionPayloadT],
        run_dir: Path,
        request_payload: PredictionPayloadT,
        request_fingerprint: str,
        workspace_id: str | None,
    ) -> Path:
        metadata = self._prepare_start(
            run_dir=run_dir,
            run_type=definition.run_type,
            request_fingerprint=request_fingerprint,
            workspace_id=workspace_id,
        )

        if metadata.remote.run_id is None:
            self._sink.info(f"Submitting prediction from {run_dir}")
            response = definition.start_call(
                self._client,
                request_payload,
                metadata.idempotency_key,
                metadata.remote.workspace_id,
            )
            self._update_prediction_remote(metadata, response)
            write_run_metadata(run_dir=run_dir, response=response)
            save_metadata(run_dir, metadata)
            self._sink.info(f"Prediction run ID: {metadata.remote.run_id}")
        else:
            self._sink.info(f"Reusing existing prediction run {metadata.remote.run_id} in {run_dir}")

        return run_dir

    def start_pipeline(
        self,
        *,
        definition: PipelineDefinition[PipelinePayloadT],
        run_dir: Path,
        request_payload: PipelinePayloadT,
        request_fingerprint: str,
        workspace_id: str | None,
        download_mode: DownloadMode | None,
    ) -> Path:
        metadata = self._prepare_start(
            run_dir=run_dir,
            run_type=definition.run_type,
            request_fingerprint=request_fingerprint,
            workspace_id=workspace_id,
            download_mode=download_mode,
        )

        if metadata.remote.run_id is None:
            self._sink.info(f"Submitting {definition.run_type.replace('_', ' ')} from {run_dir}")
            response = definition.start_call(
                self._client,
                request_payload,
                metadata.idempotency_key,
                metadata.remote.workspace_id,
            )
            self._update_pipeline_remote(metadata, response)
            write_run_metadata(run_dir=run_dir, response=response)
            save_metadata(run_dir, metadata)
            self._sink.info(f"Pipeline run ID: {metadata.remote.run_id}")
        else:
            self._sink.info(f"Reusing existing pipeline run {metadata.remote.run_id} in {run_dir}")

        return run_dir

    def wait_for_prediction(
        self,
        *,
        definition: PredictionDefinition[PredictionPayloadT],
        run_dir: Path,
        poll_interval_seconds: float,
    ) -> Path:
        metadata = load_metadata(run_dir)
        run_id = metadata.remote.run_id
        if run_id is None:
            raise ExperimentError(
                f"Run {run_dir} has no confirmed remote run ID yet. Rerun the original start/run call with the same `name`."
            )

        self._sink.info(f"Waiting for prediction in {run_dir}")

        while True:
            response = definition.retrieve_call(self._client, run_id, metadata.remote.workspace_id)
            previous_status = metadata.remote.status
            self._update_prediction_remote(metadata, response)
            write_run_metadata(run_dir=run_dir, response=response)
            save_metadata(run_dir, metadata)

            if metadata.remote.status != previous_status:
                self._sink.info(f"Prediction status: {metadata.remote.status}")

            status = cast(PredictionStatus, metadata.remote.status)
            if status in {"pending", "running"}:
                self._sink.maybe_running_summary("Prediction still running...")
                time.sleep(poll_interval_seconds)
                continue

            if status == "failed":
                raise ExperimentError(self._failure_message(metadata))

            if definition.materialize_archive:
                archive_url = _prediction_archive_url(cast(PredictionRetrieveArchiveResponseLike, response))
                archive_path, extracted_dir = prediction_paths(run_dir, archive_url)
                if not is_materialized(archive_path, extracted_dir):
                    metadata.pending = PredictionPending.archive()
                    save_metadata(run_dir, metadata)
                    materialize_archive(
                        client=self._client,
                        archive_url=archive_url,
                        archive_path=archive_path,
                        extracted_dir=extracted_dir,
                        sink=self._sink,
                    )
                    metadata.pending = None
                    save_metadata(run_dir, metadata)
                prefix_prediction_structure_file(run_dir=run_dir, prediction_id=run_id)

            self._sink.info(f"Prediction ready in {run_dir}")
            return run_dir

    def wait_for_pipeline(
        self,
        *,
        definition: PipelineDefinition[PipelinePayloadT],
        run_dir: Path,
        poll_interval_seconds: float,
        download_mode: DownloadMode | None = None,
    ) -> Path:
        metadata = load_metadata(run_dir)
        self._reconcile_download_mode(run_dir=run_dir, metadata=metadata, download_mode=download_mode)
        run_id = metadata.remote.run_id
        if run_id is None:
            raise ExperimentError(
                f"Run {run_dir} has no confirmed remote run ID yet. Rerun the original start/run call with the same `name`."
            )

        self._sink.info(f"Waiting for {metadata.run_type.replace('_', ' ')} in {run_dir}")

        while True:
            response = definition.retrieve_call(self._client, run_id, metadata.remote.workspace_id)
            previous_status = metadata.remote.status
            self._update_pipeline_remote(metadata, response)
            write_run_metadata(run_dir=run_dir, response=response)
            save_metadata(run_dir, metadata)

            if metadata.remote.status != previous_status:
                self._sink.info(f"Pipeline status: {metadata.remote.status}")

            made_progress = False
            while True:
                if isinstance(metadata.pending, PipelinePending):
                    self._drain_pending_page(definition=definition, run_dir=run_dir, metadata=metadata)
                    made_progress = True
                    continue

                if self._discover_next_page(definition=definition, metadata=metadata):
                    save_metadata(run_dir, metadata)
                    made_progress = True
                    continue
                break

            status = cast(PipelineStatus, metadata.remote.status)
            if status in {"pending", "running"}:
                if not made_progress:
                    self._sink.maybe_running_summary(_pipeline_running_summary(metadata.remote.latest_result_id))
                    time.sleep(poll_interval_seconds)
                continue

            if status == "failed":
                raise ExperimentError(self._failure_message(metadata))

            self._sink.info(f"Pipeline ready in {run_dir}")
            return run_dir

    def stop_pipeline(
        self,
        *,
        definition: PipelineDefinition[PipelinePayloadT],
        run_dir: Path,
    ) -> Path:
        metadata = load_metadata(run_dir)
        run_id = metadata.remote.run_id
        if run_id is None:
            raise ExperimentError(
                f"Run {run_dir} has no confirmed remote run ID yet. Rerun the original start/run call with the same `name`."
            )

        status = metadata.remote.status
        if status in {"succeeded", "failed", "stopped"}:
            self._sink.info(f"Pipeline already terminal with status {status}")
            return run_dir

        self._sink.info(f"Stopping pipeline {run_id}")
        response = definition.stop_call(self._client, run_id)
        self._update_pipeline_remote(metadata, response)
        write_run_metadata(run_dir=run_dir, response=response)
        save_metadata(run_dir, metadata)
        self._sink.info(f"Pipeline status: {metadata.remote.status}")
        return run_dir

    def _prepare_start(
        self,
        *,
        run_dir: Path,
        run_type: RunType,
        request_fingerprint: str,
        workspace_id: str | None,
        download_mode: DownloadMode | None = None,
    ) -> RunMetadata:
        ensure_directory_ready(run_dir)

        metadata_path = run_dir / ".boltz-run.json"
        if metadata_path.exists():
            metadata = load_metadata(run_dir)
            if metadata.run_type != run_type:
                raise ExperimentFingerprintMismatchError(
                    f"Run directory {run_dir} belongs to {metadata.run_type}, not {run_type}"
                )
            if metadata.request_fingerprint != request_fingerprint:
                raise ExperimentFingerprintMismatchError(
                    f"Run directory {run_dir} belongs to a different request. Choose a new `name`."
                )
            if workspace_id is not None and metadata.remote.workspace_id not in {None, workspace_id}:
                raise ExperimentFingerprintMismatchError(
                    f"Run directory {run_dir} belongs to workspace {metadata.remote.workspace_id}, not {workspace_id}"
                )
            self._reconcile_download_mode(run_dir=run_dir, metadata=metadata, download_mode=download_mode)
            return metadata

        metadata = RunMetadata.create(
            name=run_dir.name,
            run_type=run_type,
            download_mode=download_mode or DOWNLOAD_MODE_EVERYTHING,
            request_fingerprint=request_fingerprint,
            idempotency_key=f"exp_{uuid.uuid4().hex}",
        )
        metadata.remote.workspace_id = workspace_id
        save_metadata(run_dir, metadata)
        return metadata

    def _discover_next_page(
        self,
        *,
        definition: PipelineDefinition[PipelinePayloadT],
        metadata: RunMetadata,
    ) -> bool:
        run_id = metadata.remote.run_id
        if run_id is None:
            raise ExperimentError("Pipeline metadata is missing a remote run ID")

        page = definition.list_results_call(
            self._client,
            run_id,
            metadata.remote.workspace_id,
            20,
            metadata.cursor_after_id,
        )
        results = list(page.data)
        if not results:
            return False

        page_last_id = page.last_id
        if page_last_id is None and results:
            page_last_id = results[-1].id

        metadata.pending = PipelinePending.current_page(
            after_id=metadata.cursor_after_id,
            page_last_id=page_last_id,
            result_ids=[result.id for result in results],
        )
        return True

    def _drain_pending_page(
        self,
        *,
        definition: PipelineDefinition[PipelinePayloadT],
        run_dir: Path,
        metadata: RunMetadata,
    ) -> None:
        pending = metadata.pending
        if not isinstance(pending, PipelinePending):
            raise ExperimentError("Pipeline metadata does not contain a pending page")

        run_id = metadata.remote.run_id
        if run_id is None:
            raise ExperimentError("Pipeline metadata is missing a remote run ID")

        page = definition.list_results_call(
            self._client,
            run_id,
            metadata.remote.workspace_id,
            20,
            pending.after_id,
        )
        results = {result.id: result for result in page.data}

        for result_id in list(pending.result_ids):
            result = results.get(result_id)
            if result is None:
                raise ExperimentError(f"Unable to resume result page; result {result_id} is no longer present")

            if metadata.download_mode == DOWNLOAD_MODE_METADATA_ONLY:
                append_pipeline_result_metadata(run_dir=run_dir, result=result)
            else:
                archive_url = _result_archive_url(result)
                archive_path, extracted_dir = pipeline_paths(run_dir, result_id, archive_url)
                if not is_materialized(archive_path, extracted_dir):
                    materialize_archive(
                        client=self._client,
                        archive_url=archive_url,
                        archive_path=archive_path,
                        extracted_dir=extracted_dir,
                        sink=self._sink,
                    )
                prefix_pipeline_result_structure_file(result_dir=run_dir / "results" / result_id, result_id=result_id)
                write_pipeline_result_metadata(run_dir=run_dir, result=result)

            pending.result_ids.remove(result_id)
            save_metadata(run_dir, metadata)

        metadata.cursor_after_id = pending.page_last_id
        metadata.pending = None
        save_metadata(run_dir, metadata)

    def _update_prediction_remote(self, metadata: RunMetadata, response: PredictionRunResponseLike) -> None:
        metadata.remote.run_id = response.id
        if response.workspace_id is not None:
            metadata.remote.workspace_id = response.workspace_id
        metadata.remote.status = response.status
        metadata.remote.started_at = _isoformat(response.started_at)
        metadata.remote.completed_at = _isoformat(response.completed_at)
        metadata.remote.stopped_at = None
        metadata.remote.latest_result_id = None

        error = response.error
        metadata.remote.error_code = None if error is None else error.code

    def _update_pipeline_remote(self, metadata: RunMetadata, response: PipelineRunResponseLike) -> None:
        metadata.remote.run_id = response.id
        if response.workspace_id is not None:
            metadata.remote.workspace_id = response.workspace_id
        metadata.remote.status = response.status
        metadata.remote.started_at = _isoformat(response.started_at)
        metadata.remote.completed_at = _isoformat(response.completed_at)
        metadata.remote.stopped_at = _isoformat(response.stopped_at)

        progress = response.progress
        metadata.remote.latest_result_id = None if progress is None else progress.latest_result_id

        error = response.error
        metadata.remote.error_code = None if error is None else error.code

    def _failure_message(self, metadata: RunMetadata) -> str:
        run_id = metadata.remote.run_id or metadata.name
        if metadata.remote.error_code:
            return f"Run {run_id} failed with error code {metadata.remote.error_code}"
        return f"Run {run_id} failed"

    def _reconcile_download_mode(
        self,
        *,
        run_dir: Path,
        metadata: RunMetadata,
        download_mode: DownloadMode | None,
    ) -> None:
        metadata.download_mode = normalize_download_mode(metadata.download_mode)
        if metadata.run_type in {"prediction", "adme"} and metadata.download_mode != DOWNLOAD_MODE_EVERYTHING:
            raise ExperimentError(
                f"Run directory {run_dir} belongs to a prediction and cannot use download mode {metadata.download_mode}"
            )
        if download_mode is not None and metadata.download_mode != download_mode:
            raise ExperimentError(
                f"Run directory {run_dir} uses download mode {metadata.download_mode}, not {download_mode}"
            )


def unsupported_stop(run_type: str) -> None:
    raise ExperimentUnsupportedOperationError(f"`stop()` is not supported for {run_type}")


def _prediction_archive_url(response: PredictionRetrieveArchiveResponseLike) -> str:
    output = response.output
    archive = None if output is None else output.archive
    url = None if archive is None else archive.url
    if not isinstance(url, str):
        raise ExperimentError("Prediction succeeded but did not return an archive URL")
    return url


def _result_archive_url(result: PipelineResultLike) -> str:
    return result.artifacts.archive.url


def _isoformat(value: datetime | str | None) -> str | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.isoformat()
    return value


def _pipeline_running_summary(latest_result_id: str | None) -> str:
    if latest_result_id is None:
        return "Pipeline still running..."
    return f"Pipeline still running... latest result: {latest_result_id}"
