from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.run_events_snapshot_dto_terminal_type_0_type_1_mode import RunEventsSnapshotDtoTerminalType0Type1Mode
from ..models.run_events_snapshot_dto_terminal_type_0_type_1_schema_version import RunEventsSnapshotDtoTerminalType0Type1SchemaVersion
from ..models.run_events_snapshot_dto_terminal_type_0_type_1_status import RunEventsSnapshotDtoTerminalType0Type1Status
from typing import cast

if TYPE_CHECKING:
  from ..models.run_events_snapshot_dto_terminal_type_0_type_1_eval_type_0 import RunEventsSnapshotDtoTerminalType0Type1EvalType0





T = TypeVar("T", bound="RunEventsSnapshotDtoTerminalType0Type1")



@_attrs_define
class RunEventsSnapshotDtoTerminalType0Type1:
    """ The eval sub-mode shape of output.json (mode: eval), written by the trainer's own internal evaluation pass rather
    than the platform-launched evaluation_run job type.

        Attributes:
            schema_version (RunEventsSnapshotDtoTerminalType0Type1SchemaVersion): Contract schema version of this terminal
                record.
            mode (RunEventsSnapshotDtoTerminalType0Type1Mode): Discriminant marking the eval sub-mode terminal shape.
            status (RunEventsSnapshotDtoTerminalType0Type1Status): Terminal outcome of the eval pass.
            final_checkpoint_ref (None | str): Opaque reference to the checkpoint evaluated by this pass; null when no
                checkpoint was available.
            output_model_id (None | str): Identifier of the evaluated output model, when one applies.
            eval_step (int): Trainer step this evaluation pass was run at.
            eval_ (None | RunEventsSnapshotDtoTerminalType0Type1EvalType0): Free-form eval result payload, or null when none
                was produced.
            eval_ref (str): Reference to the eval result artifact.
            job_status_ref (str): Reference to the final job_status.json artifact.
     """

    schema_version: RunEventsSnapshotDtoTerminalType0Type1SchemaVersion
    mode: RunEventsSnapshotDtoTerminalType0Type1Mode
    status: RunEventsSnapshotDtoTerminalType0Type1Status
    final_checkpoint_ref: None | str
    output_model_id: None | str
    eval_step: int
    eval_: None | RunEventsSnapshotDtoTerminalType0Type1EvalType0
    eval_ref: str
    job_status_ref: str





    def to_dict(self) -> dict[str, Any]:
        from ..models.run_events_snapshot_dto_terminal_type_0_type_1_eval_type_0 import RunEventsSnapshotDtoTerminalType0Type1EvalType0 # noqa: PLC0415
        schema_version = self.schema_version.value

        mode = self.mode.value

        status = self.status.value

        final_checkpoint_ref: None | str
        final_checkpoint_ref = self.final_checkpoint_ref

        output_model_id: None | str
        output_model_id = self.output_model_id

        eval_step = self.eval_step

        eval_: dict[str, Any] | None
        if isinstance(self.eval_, RunEventsSnapshotDtoTerminalType0Type1EvalType0):
            eval_ = self.eval_.to_dict()
        else:
            eval_ = self.eval_

        eval_ref = self.eval_ref

        job_status_ref = self.job_status_ref


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "schema_version": schema_version,
            "mode": mode,
            "status": status,
            "final_checkpoint_ref": final_checkpoint_ref,
            "output_model_id": output_model_id,
            "eval_step": eval_step,
            "eval": eval_,
            "eval_ref": eval_ref,
            "job_status_ref": job_status_ref,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.run_events_snapshot_dto_terminal_type_0_type_1_eval_type_0 import RunEventsSnapshotDtoTerminalType0Type1EvalType0 # noqa: PLC0415
        d = dict(src_dict)
        schema_version = RunEventsSnapshotDtoTerminalType0Type1SchemaVersion(d.pop("schema_version"))




        mode = RunEventsSnapshotDtoTerminalType0Type1Mode(d.pop("mode"))




        status = RunEventsSnapshotDtoTerminalType0Type1Status(d.pop("status"))




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


        eval_step = d.pop("eval_step")

        def _parse_eval_(data: object) -> None | RunEventsSnapshotDtoTerminalType0Type1EvalType0:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                eval_type_0 = RunEventsSnapshotDtoTerminalType0Type1EvalType0.from_dict(data)



                return eval_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | RunEventsSnapshotDtoTerminalType0Type1EvalType0, data)

        eval_ = _parse_eval_(d.pop("eval"))


        eval_ref = d.pop("eval_ref")

        job_status_ref = d.pop("job_status_ref")

        run_events_snapshot_dto_terminal_type_0_type_1 = cls(
            schema_version=schema_version,
            mode=mode,
            status=status,
            final_checkpoint_ref=final_checkpoint_ref,
            output_model_id=output_model_id,
            eval_step=eval_step,
            eval_=eval_,
            eval_ref=eval_ref,
            job_status_ref=job_status_ref,
        )

        return run_events_snapshot_dto_terminal_type_0_type_1

