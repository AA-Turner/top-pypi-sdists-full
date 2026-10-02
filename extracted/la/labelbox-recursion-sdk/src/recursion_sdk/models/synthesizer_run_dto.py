from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.synthesizer_run_dto_applied_targets_item import SynthesizerRunDtoAppliedTargetsItem
from ..models.synthesizer_run_dto_built_in_key_type_0 import SynthesizerRunDtoBuiltInKeyType0
from ..models.synthesizer_run_dto_status import SynthesizerRunDtoStatus
from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.synthesizer_run_dto_diff_payload_item_type_0 import SynthesizerRunDtoDiffPayloadItemType0
  from ..models.synthesizer_run_dto_diff_payload_item_type_1 import SynthesizerRunDtoDiffPayloadItemType1
  from ..models.synthesizer_run_dto_diff_payload_item_type_2 import SynthesizerRunDtoDiffPayloadItemType2





T = TypeVar("T", bound="SynthesizerRunDto")



@_attrs_define
class SynthesizerRunDto:
    """ Single execution of a synthesizer against a problem version, capturing the produced diff and audit metadata.

        Example:
            {'id': 'e6016881-c0b4-4412-92af-c84c3093e770', 'synthesizerJobId': 'b45c081d-3069-4e32-98d4-aa5ec3d442c6',
                'builtInKey': None, 'problemVersionId': '0c3ac467-57e1-4074-b57d-b6a7be392f71', 'triggeredByUserId':
                '49dea803-7390-49c4-abb1-5629718fc9cd', 'status': 'completed', 'diffPayload': [{'target': 'prompt', 'kind':
                'row', 'current': 'Find the defect in the image.', 'proposed': 'Inspect the product image and report each
                surface defect with its type and location.', 'canWrite': True}], 'appliedTargets': ['prompt'], 'appliedAt':
                '2026-01-16T15:05:00.000Z', 'appliedByUserId': '49dea803-7390-49c4-abb1-5629718fc9cd', 'errorMessage': None,
                'startedAt': '2026-01-16T14:50:00.000Z', 'completedAt': '2026-01-16T14:52:30.000Z', 'createdAt':
                '2026-01-16T14:49:45.000Z', 'updatedAt': '2026-01-16T15:05:00.000Z', 'synthesizerRunConfigVersionId':
                '39088cb6-ca62-4544-a074-fc66e10807ad', 'synthesizerRunConfigName': 'claude-sonnet-baseline',
                'synthesizerRunConfigVersionNumber': 1}

        Attributes:
            id (UUID): Stable synthesizer-run identifier (UUID). One execution of a synthesizer job.
            synthesizer_job_id (None | UUID): User-defined synthesizer job that triggered this run; mutually exclusive with
                the built-in key.
            built_in_key (None | SynthesizerRunDtoBuiltInKeyType0): Built-in synthesizer key that triggered this run;
                mutually exclusive with the synthesizer job id.
            problem_version_id (UUID): Stable problem-version identifier (UUID). Each problem can have many versions; this
                points at one specific version.
            triggered_by_user_id (None | UUID): User who triggered the run. Null for system-initiated runs.
            status (SynthesizerRunDtoStatus): Lifecycle status of a synthesizer run.
            diff_payload (list[SynthesizerRunDtoDiffPayloadItemType0 | SynthesizerRunDtoDiffPayloadItemType1 |
                SynthesizerRunDtoDiffPayloadItemType2]): Diff payload produced by the synthesizer agent. Empty before successful
                completion or when the completed run proposed no changes; inspect status for lifecycle state.
            applied_targets (list[SynthesizerRunDtoAppliedTargetsItem]): Targets from the most recent successful apply.
                Empty when no targets have been applied; appliedAt and appliedByUserId identify the latest successful apply.
            applied_at (None | str): Timestamp of the most recent successful apply (ISO-8601, UTC). Null if never applied.
            applied_by_user_id (None | UUID): User who performed the most recent successful apply. Null if never applied.
            error_message (None | str): Error message captured when the run failed. Null otherwise.
            started_at (None | str): Timestamp when the run started executing (ISO-8601, UTC). Null before start.
            completed_at (None | str): Timestamp when the run reached a terminal status (ISO-8601, UTC). Null while in-
                flight.
            created_at (str): Timestamp when the run was created (ISO-8601, UTC).
            updated_at (str): Timestamp when the run was last updated (ISO-8601, UTC).
            synthesizer_run_config_version_id (None | UUID): Run-config-version that drove this synthesizer run, captured at
                run-insert time for audit fidelity.
            synthesizer_run_config_name (None | str): Display name of the synthesizer run-config bound to this run,
                denormalized via JOIN.
            synthesizer_run_config_version_number (int | None): Version number of the synthesizer run-config-version,
                denormalized via JOIN.
     """

    id: UUID
    synthesizer_job_id: None | UUID
    built_in_key: None | SynthesizerRunDtoBuiltInKeyType0
    problem_version_id: UUID
    triggered_by_user_id: None | UUID
    status: SynthesizerRunDtoStatus
    diff_payload: list[SynthesizerRunDtoDiffPayloadItemType0 | SynthesizerRunDtoDiffPayloadItemType1 | SynthesizerRunDtoDiffPayloadItemType2]
    applied_targets: list[SynthesizerRunDtoAppliedTargetsItem]
    applied_at: None | str
    applied_by_user_id: None | UUID
    error_message: None | str
    started_at: None | str
    completed_at: None | str
    created_at: str
    updated_at: str
    synthesizer_run_config_version_id: None | UUID
    synthesizer_run_config_name: None | str
    synthesizer_run_config_version_number: int | None





    def to_dict(self) -> dict[str, Any]:
        from ..models.synthesizer_run_dto_diff_payload_item_type_0 import SynthesizerRunDtoDiffPayloadItemType0 # noqa: PLC0415
        from ..models.synthesizer_run_dto_diff_payload_item_type_1 import SynthesizerRunDtoDiffPayloadItemType1 # noqa: PLC0415
        from ..models.synthesizer_run_dto_diff_payload_item_type_2 import SynthesizerRunDtoDiffPayloadItemType2 # noqa: PLC0415
        id = str(self.id)

        synthesizer_job_id: None | str
        if isinstance(self.synthesizer_job_id, UUID):
            synthesizer_job_id = str(self.synthesizer_job_id)
        else:
            synthesizer_job_id = self.synthesizer_job_id

        built_in_key: None | str
        if isinstance(self.built_in_key, SynthesizerRunDtoBuiltInKeyType0):
            built_in_key = self.built_in_key.value
        else:
            built_in_key = self.built_in_key

        problem_version_id = str(self.problem_version_id)

        triggered_by_user_id: None | str
        if isinstance(self.triggered_by_user_id, UUID):
            triggered_by_user_id = str(self.triggered_by_user_id)
        else:
            triggered_by_user_id = self.triggered_by_user_id

        status = self.status.value

        diff_payload = []
        for diff_payload_item_data in self.diff_payload:
            diff_payload_item: dict[str, Any]
            if isinstance(diff_payload_item_data, SynthesizerRunDtoDiffPayloadItemType0):
                diff_payload_item = diff_payload_item_data.to_dict()
            elif isinstance(diff_payload_item_data, SynthesizerRunDtoDiffPayloadItemType1):
                diff_payload_item = diff_payload_item_data.to_dict()
            else:
                diff_payload_item = diff_payload_item_data.to_dict()

            diff_payload.append(diff_payload_item)



        applied_targets = []
        for applied_targets_item_data in self.applied_targets:
            applied_targets_item = applied_targets_item_data.value
            applied_targets.append(applied_targets_item)



        applied_at: None | str
        applied_at = self.applied_at

        applied_by_user_id: None | str
        if isinstance(self.applied_by_user_id, UUID):
            applied_by_user_id = str(self.applied_by_user_id)
        else:
            applied_by_user_id = self.applied_by_user_id

        error_message: None | str
        error_message = self.error_message

        started_at: None | str
        started_at = self.started_at

        completed_at: None | str
        completed_at = self.completed_at

        created_at = self.created_at

        updated_at = self.updated_at

        synthesizer_run_config_version_id: None | str
        if isinstance(self.synthesizer_run_config_version_id, UUID):
            synthesizer_run_config_version_id = str(self.synthesizer_run_config_version_id)
        else:
            synthesizer_run_config_version_id = self.synthesizer_run_config_version_id

        synthesizer_run_config_name: None | str
        synthesizer_run_config_name = self.synthesizer_run_config_name

        synthesizer_run_config_version_number: int | None
        synthesizer_run_config_version_number = self.synthesizer_run_config_version_number


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "synthesizerJobId": synthesizer_job_id,
            "builtInKey": built_in_key,
            "problemVersionId": problem_version_id,
            "triggeredByUserId": triggered_by_user_id,
            "status": status,
            "diffPayload": diff_payload,
            "appliedTargets": applied_targets,
            "appliedAt": applied_at,
            "appliedByUserId": applied_by_user_id,
            "errorMessage": error_message,
            "startedAt": started_at,
            "completedAt": completed_at,
            "createdAt": created_at,
            "updatedAt": updated_at,
            "synthesizerRunConfigVersionId": synthesizer_run_config_version_id,
            "synthesizerRunConfigName": synthesizer_run_config_name,
            "synthesizerRunConfigVersionNumber": synthesizer_run_config_version_number,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.synthesizer_run_dto_diff_payload_item_type_0 import SynthesizerRunDtoDiffPayloadItemType0 # noqa: PLC0415
        from ..models.synthesizer_run_dto_diff_payload_item_type_1 import SynthesizerRunDtoDiffPayloadItemType1 # noqa: PLC0415
        from ..models.synthesizer_run_dto_diff_payload_item_type_2 import SynthesizerRunDtoDiffPayloadItemType2 # noqa: PLC0415
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        def _parse_synthesizer_job_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                synthesizer_job_id_type_0 = UUID(data)



                return synthesizer_job_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        synthesizer_job_id = _parse_synthesizer_job_id(d.pop("synthesizerJobId"))


        def _parse_built_in_key(data: object) -> None | SynthesizerRunDtoBuiltInKeyType0:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                built_in_key_type_0 = SynthesizerRunDtoBuiltInKeyType0(data)



                return built_in_key_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | SynthesizerRunDtoBuiltInKeyType0, data)

        built_in_key = _parse_built_in_key(d.pop("builtInKey"))


        problem_version_id = UUID(d.pop("problemVersionId"))




        def _parse_triggered_by_user_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                triggered_by_user_id_type_0 = UUID(data)



                return triggered_by_user_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        triggered_by_user_id = _parse_triggered_by_user_id(d.pop("triggeredByUserId"))


        status = SynthesizerRunDtoStatus(d.pop("status"))




        diff_payload = []
        _diff_payload = d.pop("diffPayload")
        for diff_payload_item_data in (_diff_payload):
            def _parse_diff_payload_item(data: object) -> SynthesizerRunDtoDiffPayloadItemType0 | SynthesizerRunDtoDiffPayloadItemType1 | SynthesizerRunDtoDiffPayloadItemType2:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    diff_payload_item_type_0 = SynthesizerRunDtoDiffPayloadItemType0.from_dict(data)



                    return diff_payload_item_type_0
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    diff_payload_item_type_1 = SynthesizerRunDtoDiffPayloadItemType1.from_dict(data)



                    return diff_payload_item_type_1
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                diff_payload_item_type_2 = SynthesizerRunDtoDiffPayloadItemType2.from_dict(data)



                return diff_payload_item_type_2

            diff_payload_item = _parse_diff_payload_item(diff_payload_item_data)

            diff_payload.append(diff_payload_item)


        applied_targets = []
        _applied_targets = d.pop("appliedTargets")
        for applied_targets_item_data in (_applied_targets):
            applied_targets_item = SynthesizerRunDtoAppliedTargetsItem(applied_targets_item_data)



            applied_targets.append(applied_targets_item)


        def _parse_applied_at(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        applied_at = _parse_applied_at(d.pop("appliedAt"))


        def _parse_applied_by_user_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                applied_by_user_id_type_0 = UUID(data)



                return applied_by_user_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        applied_by_user_id = _parse_applied_by_user_id(d.pop("appliedByUserId"))


        def _parse_error_message(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        error_message = _parse_error_message(d.pop("errorMessage"))


        def _parse_started_at(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        started_at = _parse_started_at(d.pop("startedAt"))


        def _parse_completed_at(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        completed_at = _parse_completed_at(d.pop("completedAt"))


        created_at = d.pop("createdAt")

        updated_at = d.pop("updatedAt")

        def _parse_synthesizer_run_config_version_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                synthesizer_run_config_version_id_type_0 = UUID(data)



                return synthesizer_run_config_version_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        synthesizer_run_config_version_id = _parse_synthesizer_run_config_version_id(d.pop("synthesizerRunConfigVersionId"))


        def _parse_synthesizer_run_config_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        synthesizer_run_config_name = _parse_synthesizer_run_config_name(d.pop("synthesizerRunConfigName"))


        def _parse_synthesizer_run_config_version_number(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        synthesizer_run_config_version_number = _parse_synthesizer_run_config_version_number(d.pop("synthesizerRunConfigVersionNumber"))


        synthesizer_run_dto = cls(
            id=id,
            synthesizer_job_id=synthesizer_job_id,
            built_in_key=built_in_key,
            problem_version_id=problem_version_id,
            triggered_by_user_id=triggered_by_user_id,
            status=status,
            diff_payload=diff_payload,
            applied_targets=applied_targets,
            applied_at=applied_at,
            applied_by_user_id=applied_by_user_id,
            error_message=error_message,
            started_at=started_at,
            completed_at=completed_at,
            created_at=created_at,
            updated_at=updated_at,
            synthesizer_run_config_version_id=synthesizer_run_config_version_id,
            synthesizer_run_config_name=synthesizer_run_config_name,
            synthesizer_run_config_version_number=synthesizer_run_config_version_number,
        )

        return synthesizer_run_dto

