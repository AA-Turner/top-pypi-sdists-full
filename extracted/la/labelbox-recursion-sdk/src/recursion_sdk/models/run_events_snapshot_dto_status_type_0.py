from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.run_events_snapshot_dto_status_type_0_job_type import RunEventsSnapshotDtoStatusType0JobType
from ..models.run_events_snapshot_dto_status_type_0_schema_version import RunEventsSnapshotDtoStatusType0SchemaVersion
from ..models.run_events_snapshot_dto_status_type_0_state import RunEventsSnapshotDtoStatusType0State
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.run_events_snapshot_dto_status_type_0_headline import RunEventsSnapshotDtoStatusType0Headline
  from ..models.run_events_snapshot_dto_status_type_0_live_type_0 import RunEventsSnapshotDtoStatusType0LiveType0
  from ..models.run_events_snapshot_dto_status_type_0_metrics import RunEventsSnapshotDtoStatusType0Metrics
  from ..models.run_events_snapshot_dto_status_type_0_progress import RunEventsSnapshotDtoStatusType0Progress
  from ..models.run_events_snapshot_dto_status_type_0_throughput import RunEventsSnapshotDtoStatusType0Throughput





T = TypeVar("T", bound="RunEventsSnapshotDtoStatusType0")



@_attrs_define
class RunEventsSnapshotDtoStatusType0:
    """ job_status.json -- the kind-agnostic live status envelope, mirrored on the fast (~4s) cadence. The state field is
    the single authoritative run-state source.

        Attributes:
            schema_version (RunEventsSnapshotDtoStatusType0SchemaVersion): Contract schema version of this status envelope.
            job_type (RunEventsSnapshotDtoStatusType0JobType): Kind of job emitting this status (eval/train/harvest).
            name (str): Trainer-authored run name for this job.
            state (RunEventsSnapshotDtoStatusType0State): Authoritative run state (the single source of truth for status).
            updated_at (float): Epoch seconds when this status envelope was emitted.
            model (None | str | Unset): Model identifier the job is training or evaluating.
            started_at (float | None | Unset): Epoch seconds when the job started, if known.
            elapsed_s (float | None | Unset): Seconds elapsed since the job started.
            eta_s (float | None | Unset): Estimated seconds remaining, when the job reports one.
            progress (RunEventsSnapshotDtoStatusType0Progress | Unset): Count-based (done/expected) OR step-based
                (step/total_steps); a job fills whichever axis it has.
            throughput (RunEventsSnapshotDtoStatusType0Throughput | Unset): Rollout throughput snapshot at status-report
                time.
            artifacts (list[str] | Unset): Opaque artifact references the job has produced so far.
            log_tail_ref (None | str | Unset): Reference to a tail of the job log stream.
            metrics (RunEventsSnapshotDtoStatusType0Metrics | Unset): Free-form, plugin-owned metrics block (deliberately
                untyped beyond object). Rendered as raw text only -- never charted. For anything that must appear on a dashboard
                panel, emit a blocks document (BlocksDocumentSchema) instead.
            headline (RunEventsSnapshotDtoStatusType0Headline | Unset): Free-form, plugin-owned headline block (deliberately
                untyped beyond object). Rendered as raw text only -- never charted. For anything that must appear on a dashboard
                panel, emit a blocks document (BlocksDocumentSchema) instead.
            live (None | RunEventsSnapshotDtoStatusType0LiveType0 | Unset): Bounded live rollout telemetry; absent or null
                when the trainer does not report live rollout progress.
     """

    schema_version: RunEventsSnapshotDtoStatusType0SchemaVersion
    job_type: RunEventsSnapshotDtoStatusType0JobType
    name: str
    state: RunEventsSnapshotDtoStatusType0State
    updated_at: float
    model: None | str | Unset = UNSET
    started_at: float | None | Unset = UNSET
    elapsed_s: float | None | Unset = UNSET
    eta_s: float | None | Unset = UNSET
    progress: RunEventsSnapshotDtoStatusType0Progress | Unset = UNSET
    throughput: RunEventsSnapshotDtoStatusType0Throughput | Unset = UNSET
    artifacts: list[str] | Unset = UNSET
    log_tail_ref: None | str | Unset = UNSET
    metrics: RunEventsSnapshotDtoStatusType0Metrics | Unset = UNSET
    headline: RunEventsSnapshotDtoStatusType0Headline | Unset = UNSET
    live: None | RunEventsSnapshotDtoStatusType0LiveType0 | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.run_events_snapshot_dto_status_type_0_headline import RunEventsSnapshotDtoStatusType0Headline # noqa: PLC0415
        from ..models.run_events_snapshot_dto_status_type_0_live_type_0 import RunEventsSnapshotDtoStatusType0LiveType0 # noqa: PLC0415
        from ..models.run_events_snapshot_dto_status_type_0_metrics import RunEventsSnapshotDtoStatusType0Metrics # noqa: PLC0415
        from ..models.run_events_snapshot_dto_status_type_0_progress import RunEventsSnapshotDtoStatusType0Progress # noqa: PLC0415
        from ..models.run_events_snapshot_dto_status_type_0_throughput import RunEventsSnapshotDtoStatusType0Throughput # noqa: PLC0415
        schema_version = self.schema_version.value

        job_type = self.job_type.value

        name = self.name

        state = self.state.value

        updated_at = self.updated_at

        model: None | str | Unset
        if isinstance(self.model, Unset):
            model = UNSET
        else:
            model = self.model

        started_at: float | None | Unset
        if isinstance(self.started_at, Unset):
            started_at = UNSET
        else:
            started_at = self.started_at

        elapsed_s: float | None | Unset
        if isinstance(self.elapsed_s, Unset):
            elapsed_s = UNSET
        else:
            elapsed_s = self.elapsed_s

        eta_s: float | None | Unset
        if isinstance(self.eta_s, Unset):
            eta_s = UNSET
        else:
            eta_s = self.eta_s

        progress: dict[str, Any] | Unset = UNSET
        if not isinstance(self.progress, Unset):
            progress = self.progress.to_dict()

        throughput: dict[str, Any] | Unset = UNSET
        if not isinstance(self.throughput, Unset):
            throughput = self.throughput.to_dict()

        artifacts: list[str] | Unset = UNSET
        if not isinstance(self.artifacts, Unset):
            artifacts = self.artifacts



        log_tail_ref: None | str | Unset
        if isinstance(self.log_tail_ref, Unset):
            log_tail_ref = UNSET
        else:
            log_tail_ref = self.log_tail_ref

        metrics: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metrics, Unset):
            metrics = self.metrics.to_dict()

        headline: dict[str, Any] | Unset = UNSET
        if not isinstance(self.headline, Unset):
            headline = self.headline.to_dict()

        live: dict[str, Any] | None | Unset
        if isinstance(self.live, Unset):
            live = UNSET
        elif isinstance(self.live, RunEventsSnapshotDtoStatusType0LiveType0):
            live = self.live.to_dict()
        else:
            live = self.live


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "schema_version": schema_version,
            "job_type": job_type,
            "name": name,
            "state": state,
            "updated_at": updated_at,
        })
        if model is not UNSET:
            field_dict["model"] = model
        if started_at is not UNSET:
            field_dict["started_at"] = started_at
        if elapsed_s is not UNSET:
            field_dict["elapsed_s"] = elapsed_s
        if eta_s is not UNSET:
            field_dict["eta_s"] = eta_s
        if progress is not UNSET:
            field_dict["progress"] = progress
        if throughput is not UNSET:
            field_dict["throughput"] = throughput
        if artifacts is not UNSET:
            field_dict["artifacts"] = artifacts
        if log_tail_ref is not UNSET:
            field_dict["log_tail_ref"] = log_tail_ref
        if metrics is not UNSET:
            field_dict["metrics"] = metrics
        if headline is not UNSET:
            field_dict["headline"] = headline
        if live is not UNSET:
            field_dict["live"] = live

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.run_events_snapshot_dto_status_type_0_headline import RunEventsSnapshotDtoStatusType0Headline # noqa: PLC0415
        from ..models.run_events_snapshot_dto_status_type_0_live_type_0 import RunEventsSnapshotDtoStatusType0LiveType0 # noqa: PLC0415
        from ..models.run_events_snapshot_dto_status_type_0_metrics import RunEventsSnapshotDtoStatusType0Metrics # noqa: PLC0415
        from ..models.run_events_snapshot_dto_status_type_0_progress import RunEventsSnapshotDtoStatusType0Progress # noqa: PLC0415
        from ..models.run_events_snapshot_dto_status_type_0_throughput import RunEventsSnapshotDtoStatusType0Throughput # noqa: PLC0415
        d = dict(src_dict)
        schema_version = RunEventsSnapshotDtoStatusType0SchemaVersion(d.pop("schema_version"))




        job_type = RunEventsSnapshotDtoStatusType0JobType(d.pop("job_type"))




        name = d.pop("name")

        state = RunEventsSnapshotDtoStatusType0State(d.pop("state"))




        updated_at = d.pop("updated_at")

        def _parse_model(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        model = _parse_model(d.pop("model", UNSET))


        def _parse_started_at(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        started_at = _parse_started_at(d.pop("started_at", UNSET))


        def _parse_elapsed_s(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        elapsed_s = _parse_elapsed_s(d.pop("elapsed_s", UNSET))


        def _parse_eta_s(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        eta_s = _parse_eta_s(d.pop("eta_s", UNSET))


        _progress = d.pop("progress", UNSET)
        progress: RunEventsSnapshotDtoStatusType0Progress | Unset
        if isinstance(_progress,  Unset):
            progress = UNSET
        else:
            progress = RunEventsSnapshotDtoStatusType0Progress.from_dict(_progress)




        _throughput = d.pop("throughput", UNSET)
        throughput: RunEventsSnapshotDtoStatusType0Throughput | Unset
        if isinstance(_throughput,  Unset):
            throughput = UNSET
        else:
            throughput = RunEventsSnapshotDtoStatusType0Throughput.from_dict(_throughput)




        artifacts = cast(list[str], d.pop("artifacts", UNSET))


        def _parse_log_tail_ref(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        log_tail_ref = _parse_log_tail_ref(d.pop("log_tail_ref", UNSET))


        _metrics = d.pop("metrics", UNSET)
        metrics: RunEventsSnapshotDtoStatusType0Metrics | Unset
        if isinstance(_metrics,  Unset):
            metrics = UNSET
        else:
            metrics = RunEventsSnapshotDtoStatusType0Metrics.from_dict(_metrics)




        _headline = d.pop("headline", UNSET)
        headline: RunEventsSnapshotDtoStatusType0Headline | Unset
        if isinstance(_headline,  Unset):
            headline = UNSET
        else:
            headline = RunEventsSnapshotDtoStatusType0Headline.from_dict(_headline)




        def _parse_live(data: object) -> None | RunEventsSnapshotDtoStatusType0LiveType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                live_type_0 = RunEventsSnapshotDtoStatusType0LiveType0.from_dict(data)



                return live_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | RunEventsSnapshotDtoStatusType0LiveType0 | Unset, data)

        live = _parse_live(d.pop("live", UNSET))


        run_events_snapshot_dto_status_type_0 = cls(
            schema_version=schema_version,
            job_type=job_type,
            name=name,
            state=state,
            updated_at=updated_at,
            model=model,
            started_at=started_at,
            elapsed_s=elapsed_s,
            eta_s=eta_s,
            progress=progress,
            throughput=throughput,
            artifacts=artifacts,
            log_tail_ref=log_tail_ref,
            metrics=metrics,
            headline=headline,
            live=live,
        )

        return run_events_snapshot_dto_status_type_0

