from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.synthesizer_job_dto_kind import SynthesizerJobDtoKind
from ..models.synthesizer_job_dto_target_fields_item import SynthesizerJobDtoTargetFieldsItem
from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.synthesizer_job_dto_context_inputs import SynthesizerJobDtoContextInputs
  from ..models.synthesizer_job_dto_files_item import SynthesizerJobDtoFilesItem





T = TypeVar("T", bound="SynthesizerJobDto")



@_attrs_define
class SynthesizerJobDto:
    """ User-defined synthesizer job persisted at the environment level.

        Example:
            {'kind': 'user', 'id': 'b45c081d-3069-4e32-98d4-aa5ec3d442c6', 'environmentId':
                '784e2386-e297-4f9d-a886-838422383b65', 'name': 'sharpen-task-prompt', 'description': 'Rewrites the task prompt
                to be more specific and measurable.', 'systemPrompt': 'You are a prompt engineer. Rewrite the task prompt so it
                is unambiguous, measurable, and concise.', 'runConfigVersionId': '39088cb6-ca62-4544-a074-fc66e10807ad',
                'runConfigName': 'claude-sonnet-baseline', 'runConfigVersionNumber': 1, 'contextInputs': {'files': {'problem':
                True, 'supporting': True, 'graderSupport': False, 'goldStandard': False}, 'rubrics': True, 'currentFieldValues':
                ['prompt', 'tools'], 'forms': False}, 'targetFields': ['prompt'], 'files': [{'id':
                'a7c9f2e1-4b3d-4a6e-9f1c-2d8e5b7a0c34', 'fileId': 'e2a910d9-32c4-4ed6-8071-c7190a8c1951', 'filename': 'style-
                guide.md', 'mountPath': '/workspace/files/style-guide.md', 'sizeBytes': 4096, 'createdAt':
                '2026-01-15T09:35:00.000Z'}], 'enabled': True, 'createdAt': '2026-01-15T09:30:00.000Z', 'updatedAt':
                '2026-01-16T14:20:00.000Z'}

        Attributes:
            kind (SynthesizerJobDtoKind): Discriminator marking this synthesizer as a user-defined job (vs. a built-in).
            id (UUID): Stable synthesizer-job identifier (UUID).
            environment_id (UUID): Stable environment identifier (UUID).
            name (str): Display name of the synthesizer.
            description (None | str): Free-form description of the synthesizer.
            system_prompt (str): System prompt sent to the agent that drives the synthesis pipeline.
            run_config_version_id (None | UUID): Run-config version pinned for this synthesizer, supplying harness and
                model. Null when no binding is set.
            run_config_name (None | str): Display name of the synthesizer run-config bound to this job, denormalized via
                JOIN.
            run_config_version_number (int | None): Version number of the synthesizer run-config-version, denormalized via
                JOIN.
            context_inputs (SynthesizerJobDtoContextInputs): Declares which problem-version artifacts are bundled into the
                input tarball for the agent.
            target_fields (list[SynthesizerJobDtoTargetFieldsItem]): Allowed write targets for this synthesizer.
            files (list[SynthesizerJobDtoFilesItem]): Files attached to this synthesizer and mounted into the agent
                container.
            enabled (bool): Always true for user-defined synthesizers; mirrored from built-ins so consumers can filter the
                unified list without branching.
            created_at (str): Timestamp when the synthesizer was created (ISO-8601, UTC).
            updated_at (str): Timestamp when the synthesizer was last updated (ISO-8601, UTC).
     """

    kind: SynthesizerJobDtoKind
    id: UUID
    environment_id: UUID
    name: str
    description: None | str
    system_prompt: str
    run_config_version_id: None | UUID
    run_config_name: None | str
    run_config_version_number: int | None
    context_inputs: SynthesizerJobDtoContextInputs
    target_fields: list[SynthesizerJobDtoTargetFieldsItem]
    files: list[SynthesizerJobDtoFilesItem]
    enabled: bool
    created_at: str
    updated_at: str





    def to_dict(self) -> dict[str, Any]:
        from ..models.synthesizer_job_dto_context_inputs import SynthesizerJobDtoContextInputs # noqa: PLC0415
        from ..models.synthesizer_job_dto_files_item import SynthesizerJobDtoFilesItem # noqa: PLC0415
        kind = self.kind.value

        id = str(self.id)

        environment_id = str(self.environment_id)

        name = self.name

        description: None | str
        description = self.description

        system_prompt = self.system_prompt

        run_config_version_id: None | str
        if isinstance(self.run_config_version_id, UUID):
            run_config_version_id = str(self.run_config_version_id)
        else:
            run_config_version_id = self.run_config_version_id

        run_config_name: None | str
        run_config_name = self.run_config_name

        run_config_version_number: int | None
        run_config_version_number = self.run_config_version_number

        context_inputs = self.context_inputs.to_dict()

        target_fields = []
        for target_fields_item_data in self.target_fields:
            target_fields_item = target_fields_item_data.value
            target_fields.append(target_fields_item)



        files = []
        for files_item_data in self.files:
            files_item = files_item_data.to_dict()
            files.append(files_item)



        enabled = self.enabled

        created_at = self.created_at

        updated_at = self.updated_at


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "kind": kind,
            "id": id,
            "environmentId": environment_id,
            "name": name,
            "description": description,
            "systemPrompt": system_prompt,
            "runConfigVersionId": run_config_version_id,
            "runConfigName": run_config_name,
            "runConfigVersionNumber": run_config_version_number,
            "contextInputs": context_inputs,
            "targetFields": target_fields,
            "files": files,
            "enabled": enabled,
            "createdAt": created_at,
            "updatedAt": updated_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.synthesizer_job_dto_context_inputs import SynthesizerJobDtoContextInputs # noqa: PLC0415
        from ..models.synthesizer_job_dto_files_item import SynthesizerJobDtoFilesItem # noqa: PLC0415
        d = dict(src_dict)
        kind = SynthesizerJobDtoKind(d.pop("kind"))




        id = UUID(d.pop("id"))




        environment_id = UUID(d.pop("environmentId"))




        name = d.pop("name")

        def _parse_description(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        description = _parse_description(d.pop("description"))


        system_prompt = d.pop("systemPrompt")

        def _parse_run_config_version_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                run_config_version_id_type_0 = UUID(data)



                return run_config_version_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        run_config_version_id = _parse_run_config_version_id(d.pop("runConfigVersionId"))


        def _parse_run_config_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        run_config_name = _parse_run_config_name(d.pop("runConfigName"))


        def _parse_run_config_version_number(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        run_config_version_number = _parse_run_config_version_number(d.pop("runConfigVersionNumber"))


        context_inputs = SynthesizerJobDtoContextInputs.from_dict(d.pop("contextInputs"))




        target_fields = []
        _target_fields = d.pop("targetFields")
        for target_fields_item_data in (_target_fields):
            target_fields_item = SynthesizerJobDtoTargetFieldsItem(target_fields_item_data)



            target_fields.append(target_fields_item)


        files = []
        _files = d.pop("files")
        for files_item_data in (_files):
            files_item = SynthesizerJobDtoFilesItem.from_dict(files_item_data)



            files.append(files_item)


        enabled = d.pop("enabled")

        created_at = d.pop("createdAt")

        updated_at = d.pop("updatedAt")

        synthesizer_job_dto = cls(
            kind=kind,
            id=id,
            environment_id=environment_id,
            name=name,
            description=description,
            system_prompt=system_prompt,
            run_config_version_id=run_config_version_id,
            run_config_name=run_config_name,
            run_config_version_number=run_config_version_number,
            context_inputs=context_inputs,
            target_fields=target_fields,
            files=files,
            enabled=enabled,
            created_at=created_at,
            updated_at=updated_at,
        )

        return synthesizer_job_dto

