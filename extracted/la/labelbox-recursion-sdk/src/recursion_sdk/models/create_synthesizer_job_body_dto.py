from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.create_synthesizer_job_body_dto_target_fields_item import CreateSynthesizerJobBodyDtoTargetFieldsItem
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.create_synthesizer_job_body_dto_context_inputs import CreateSynthesizerJobBodyDtoContextInputs





T = TypeVar("T", bound="CreateSynthesizerJobBodyDto")



@_attrs_define
class CreateSynthesizerJobBodyDto:
    """ Payload for creating a new user-defined synthesizer job inside an environment.

        Example:
            {'name': 'sharpen-task-prompt', 'description': 'Rewrites the task prompt to be more specific and measurable.',
                'systemPrompt': 'You are a prompt engineer. Rewrite the task prompt so it is unambiguous, measurable, and
                concise.', 'runConfigVersionId': '39088cb6-ca62-4544-a074-fc66e10807ad', 'contextInputs': {'files': {'problem':
                True, 'supporting': True, 'graderSupport': False, 'goldStandard': False}, 'rubrics': True, 'currentFieldValues':
                ['prompt', 'tools'], 'forms': False}, 'targetFields': ['prompt']}

        Attributes:
            name (str): Display name for the synthesizer; unique within the environment.
            system_prompt (str): System prompt sent to the agent that drives the synthesis pipeline.
            context_inputs (CreateSynthesizerJobBodyDtoContextInputs): Declares which problem-version artifacts to bundle
                into the input tarball for the agent.
            target_fields (list[CreateSynthesizerJobBodyDtoTargetFieldsItem]): Allowed write targets for this synthesizer;
                outputs touching any other target are filtered out.
            description (None | str | Unset): Optional free-form description of what this synthesizer is for.
            run_config_version_id (None | Unset | UUID): Pinned run-config version that supplies the harness and model for
                this synthesizer. Null falls back to the environment-level synthesizer binding.
     """

    name: str
    system_prompt: str
    context_inputs: CreateSynthesizerJobBodyDtoContextInputs
    target_fields: list[CreateSynthesizerJobBodyDtoTargetFieldsItem]
    description: None | str | Unset = UNSET
    run_config_version_id: None | Unset | UUID = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.create_synthesizer_job_body_dto_context_inputs import CreateSynthesizerJobBodyDtoContextInputs # noqa: PLC0415
        name = self.name

        system_prompt = self.system_prompt

        context_inputs = self.context_inputs.to_dict()

        target_fields = []
        for target_fields_item_data in self.target_fields:
            target_fields_item = target_fields_item_data.value
            target_fields.append(target_fields_item)



        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        run_config_version_id: None | str | Unset
        if isinstance(self.run_config_version_id, Unset):
            run_config_version_id = UNSET
        elif isinstance(self.run_config_version_id, UUID):
            run_config_version_id = str(self.run_config_version_id)
        else:
            run_config_version_id = self.run_config_version_id


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "name": name,
            "systemPrompt": system_prompt,
            "contextInputs": context_inputs,
            "targetFields": target_fields,
        })
        if description is not UNSET:
            field_dict["description"] = description
        if run_config_version_id is not UNSET:
            field_dict["runConfigVersionId"] = run_config_version_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_synthesizer_job_body_dto_context_inputs import CreateSynthesizerJobBodyDtoContextInputs # noqa: PLC0415
        d = dict(src_dict)
        name = d.pop("name")

        system_prompt = d.pop("systemPrompt")

        context_inputs = CreateSynthesizerJobBodyDtoContextInputs.from_dict(d.pop("contextInputs"))




        target_fields = []
        _target_fields = d.pop("targetFields")
        for target_fields_item_data in (_target_fields):
            target_fields_item = CreateSynthesizerJobBodyDtoTargetFieldsItem(target_fields_item_data)



            target_fields.append(target_fields_item)


        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))


        def _parse_run_config_version_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                run_config_version_id_type_0 = UUID(data)



                return run_config_version_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        run_config_version_id = _parse_run_config_version_id(d.pop("runConfigVersionId", UNSET))


        create_synthesizer_job_body_dto = cls(
            name=name,
            system_prompt=system_prompt,
            context_inputs=context_inputs,
            target_fields=target_fields,
            description=description,
            run_config_version_id=run_config_version_id,
        )


        create_synthesizer_job_body_dto.additional_properties = d
        return create_synthesizer_job_body_dto

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
