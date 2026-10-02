from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.run_events_snapshot_dto_terminal_type_0_type_0_schema_version import RunEventsSnapshotDtoTerminalType0Type0SchemaVersion
from ..models.run_events_snapshot_dto_terminal_type_0_type_0_status import RunEventsSnapshotDtoTerminalType0Type0Status
from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="RunEventsSnapshotDtoTerminalType0Type0")



@_attrs_define
class RunEventsSnapshotDtoTerminalType0Type0:
    """ The training-run shape of output.json, written exactly once at terminal for a GRPO trainer job (no mode field,
    unlike the eval sub-mode shape).

        Attributes:
            schema_version (RunEventsSnapshotDtoTerminalType0Type0SchemaVersion): Contract schema version of this terminal
                record.
            status (RunEventsSnapshotDtoTerminalType0Type0Status): Terminal outcome of the training run.
            final_checkpoint_ref (None | str): Opaque reference to the final checkpoint produced by the training run; null
                when the run produced no checkpoint.
            output_model_id (None | str): Identifier of the produced output model, when one was published.
            trainer_job_id (None | str): Trainer-side job id for this run.
            final_checkpoint (None | str): Human-readable final checkpoint label (distinct from the opaque ref).
            steps (int | None): Total optimizer steps completed by the run.
            metrics_ref (str): Reference to the run metrics.jsonl artifact.
            job_status_ref (str): Reference to the final job_status.json artifact.
            error_message (None | str | Unset): Generic human-readable terminal failure reason, when the trainer reports one
                (relayed verbatim, never parsed).
     """

    schema_version: RunEventsSnapshotDtoTerminalType0Type0SchemaVersion
    status: RunEventsSnapshotDtoTerminalType0Type0Status
    final_checkpoint_ref: None | str
    output_model_id: None | str
    trainer_job_id: None | str
    final_checkpoint: None | str
    steps: int | None
    metrics_ref: str
    job_status_ref: str
    error_message: None | str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        schema_version = self.schema_version.value

        status = self.status.value

        final_checkpoint_ref: None | str
        final_checkpoint_ref = self.final_checkpoint_ref

        output_model_id: None | str
        output_model_id = self.output_model_id

        trainer_job_id: None | str
        trainer_job_id = self.trainer_job_id

        final_checkpoint: None | str
        final_checkpoint = self.final_checkpoint

        steps: int | None
        steps = self.steps

        metrics_ref = self.metrics_ref

        job_status_ref = self.job_status_ref

        error_message: None | str | Unset
        if isinstance(self.error_message, Unset):
            error_message = UNSET
        else:
            error_message = self.error_message


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "schema_version": schema_version,
            "status": status,
            "final_checkpoint_ref": final_checkpoint_ref,
            "output_model_id": output_model_id,
            "trainer_job_id": trainer_job_id,
            "final_checkpoint": final_checkpoint,
            "steps": steps,
            "metrics_ref": metrics_ref,
            "job_status_ref": job_status_ref,
        })
        if error_message is not UNSET:
            field_dict["error_message"] = error_message

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        schema_version = RunEventsSnapshotDtoTerminalType0Type0SchemaVersion(d.pop("schema_version"))




        status = RunEventsSnapshotDtoTerminalType0Type0Status(d.pop("status"))




        def _parse_final_checkpoint_ref(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        final_checkpoint_ref = _parse_final_checkpoint_ref(d.pop("final_checkpoint_ref"))


        def _parse_output_model_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        output_model_id = _parse_output_model_id(d.pop("output_model_id"))


        def _parse_trainer_job_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        trainer_job_id = _parse_trainer_job_id(d.pop("trainer_job_id"))


        def _parse_final_checkpoint(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        final_checkpoint = _parse_final_checkpoint(d.pop("final_checkpoint"))


        def _parse_steps(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        steps = _parse_steps(d.pop("steps"))


        metrics_ref = d.pop("metrics_ref")

        job_status_ref = d.pop("job_status_ref")

        def _parse_error_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        error_message = _parse_error_message(d.pop("error_message", UNSET))


        run_events_snapshot_dto_terminal_type_0_type_0 = cls(
            schema_version=schema_version,
            status=status,
            final_checkpoint_ref=final_checkpoint_ref,
            output_model_id=output_model_id,
            trainer_job_id=trainer_job_id,
            final_checkpoint=final_checkpoint,
            steps=steps,
            metrics_ref=metrics_ref,
            job_status_ref=job_status_ref,
            error_message=error_message,
        )

        return run_events_snapshot_dto_terminal_type_0_type_0

