from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.run_config_probe_run_dto_status import RunConfigProbeRunDtoStatus
from typing import cast
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.run_config_probe_run_dto_result_type_0 import RunConfigProbeRunDtoResultType0





T = TypeVar("T", bound="RunConfigProbeRunDto")



@_attrs_define
class RunConfigProbeRunDto:
    """ One attempt at running the probe against a draft run-config version. Async lifecycle: submit returns 202 with the
    probe-run id, then the parallel poller writes the terminal result back.

        Example:
            {'id': '1be7d569-e271-4926-af2c-569798de74d7', 'runConfigVersionId': '39088cb6-ca62-4544-a074-fc66e10807ad',
                'externalRunId': 'run_a1b2c3d4e5f6', 'status': 'succeeded', 'submittedByUserId':
                '49dea803-7390-49c4-abb1-5629718fc9cd', 'submittedAt': '2026-01-16T14:05:00.000Z', 'completedAt':
                '2026-01-16T14:10:00.000Z', 'result': {'passed': True, 'exitCode': 0, 'transcript': '[{"type":"text","text":"A
                scratch defect is visible in the lower-left quadrant."}]', 'failureReason': None, 'runAt':
                '2026-01-16T14:10:00.000Z'}, 'createdAt': '2026-01-16T14:05:00.000Z', 'updatedAt': '2026-01-16T14:10:00.000Z'}

        Attributes:
            id (UUID): Stable probe-run identifier (UUID). Probe runs validate a run-config version before locking.
            run_config_version_id (UUID): Draft version this probe run is validating.
            external_run_id (None | str): Agent-service run id. Null while still pending and on terminal rows for failures
                that never reached agent-service (build failure, submit-call rejection).
            status (RunConfigProbeRunDtoStatus): Lifecycle status of this probe-run.
            submitted_by_user_id (UUID): User who submitted this probe run.
            submitted_at (datetime.datetime): Timestamp when the probe run was submitted (ISO-8601, UTC).
            completed_at (datetime.datetime | None): Timestamp when the probe run reached a terminal status (ISO-8601, UTC).
                Null while non-terminal.
            result (None | RunConfigProbeRunDtoResultType0): Probe outcome plus completion timestamp. Populated only on
                terminal rows (succeeded / failed / cancelled).
            created_at (datetime.datetime): Timestamp when the probe-run row was created (ISO-8601, UTC).
            updated_at (datetime.datetime): Timestamp when the probe-run row was last updated (ISO-8601, UTC).
     """

    id: UUID
    run_config_version_id: UUID
    external_run_id: None | str
    status: RunConfigProbeRunDtoStatus
    submitted_by_user_id: UUID
    submitted_at: datetime.datetime
    completed_at: datetime.datetime | None
    result: None | RunConfigProbeRunDtoResultType0
    created_at: datetime.datetime
    updated_at: datetime.datetime





    def to_dict(self) -> dict[str, Any]:
        from ..models.run_config_probe_run_dto_result_type_0 import RunConfigProbeRunDtoResultType0 # noqa: PLC0415
        id = str(self.id)

        run_config_version_id = str(self.run_config_version_id)

        external_run_id: None | str
        external_run_id = self.external_run_id

        status = self.status.value

        submitted_by_user_id = str(self.submitted_by_user_id)

        submitted_at = self.submitted_at.isoformat()

        completed_at: None | str
        if isinstance(self.completed_at, datetime.datetime):
            completed_at = self.completed_at.isoformat()
        else:
            completed_at = self.completed_at

        result: dict[str, Any] | None
        if isinstance(self.result, RunConfigProbeRunDtoResultType0):
            result = self.result.to_dict()
        else:
            result = self.result

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "runConfigVersionId": run_config_version_id,
            "externalRunId": external_run_id,
            "status": status,
            "submittedByUserId": submitted_by_user_id,
            "submittedAt": submitted_at,
            "completedAt": completed_at,
            "result": result,
            "createdAt": created_at,
            "updatedAt": updated_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.run_config_probe_run_dto_result_type_0 import RunConfigProbeRunDtoResultType0 # noqa: PLC0415
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        run_config_version_id = UUID(d.pop("runConfigVersionId"))




        def _parse_external_run_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        external_run_id = _parse_external_run_id(d.pop("externalRunId"))


        status = RunConfigProbeRunDtoStatus(d.pop("status"))




        submitted_by_user_id = UUID(d.pop("submittedByUserId"))




        submitted_at = datetime.datetime.fromisoformat(d.pop("submittedAt"))




        def _parse_completed_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                completed_at_type_0 = datetime.datetime.fromisoformat(data)



                return completed_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        completed_at = _parse_completed_at(d.pop("completedAt"))


        def _parse_result(data: object) -> None | RunConfigProbeRunDtoResultType0:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                result_type_0 = RunConfigProbeRunDtoResultType0.from_dict(data)



                return result_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | RunConfigProbeRunDtoResultType0, data)

        result = _parse_result(d.pop("result"))


        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updatedAt"))




        run_config_probe_run_dto = cls(
            id=id,
            run_config_version_id=run_config_version_id,
            external_run_id=external_run_id,
            status=status,
            submitted_by_user_id=submitted_by_user_id,
            submitted_at=submitted_at,
            completed_at=completed_at,
            result=result,
            created_at=created_at,
            updated_at=updated_at,
        )

        return run_config_probe_run_dto

