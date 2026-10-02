from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.update_synthesizer_job_body_dto_target_fields_item import UpdateSynthesizerJobBodyDtoTargetFieldsItem
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.update_synthesizer_job_body_dto_context_inputs import UpdateSynthesizerJobBodyDtoContextInputs





T = TypeVar("T", bound="UpdateSynthesizerJobBodyDto")



@_attrs_define
class UpdateSynthesizerJobBodyDto:
    """ Partial update payload for an existing user-defined synthesizer job.

        Example:
            {'systemPrompt': 'You are a prompt engineer. Rewrite the task prompt so it is unambiguous, measurable, and
                verifiable.', 'targetFields': ['prompt']}

        Attributes:
            name (str | Unset): Updated display name for the synthesizer.
            description (None | str | Unset): Updated description; pass null to clear.
            system_prompt (str | Unset): Updated agent system prompt.
            run_config_version_id (None | Unset | UUID): Updated pinned run-config version for harness and model; pass null
                to clear and fall back to the environment-level synthesizer binding.
            context_inputs (UpdateSynthesizerJobBodyDtoContextInputs | Unset): Updated declaration of which inputs to bundle
                into the input tarball.
            target_fields (list[UpdateSynthesizerJobBodyDtoTargetFieldsItem] | Unset): Updated allowed write targets; at
                least one target must remain.
     """

    name: str | Unset = UNSET
    description: None | str | Unset = UNSET
    system_prompt: str | Unset = UNSET
    run_config_version_id: None | Unset | UUID = UNSET
    context_inputs: UpdateSynthesizerJobBodyDtoContextInputs | Unset = UNSET
    target_fields: list[UpdateSynthesizerJobBodyDtoTargetFieldsItem] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.update_synthesizer_job_body_dto_context_inputs import UpdateSynthesizerJobBodyDtoContextInputs # noqa: PLC0415
        name = self.name

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        system_prompt = self.system_prompt

        run_config_version_id: None | str | Unset
        if isinstance(self.run_config_version_id, Unset):
            run_config_version_id = UNSET
        elif isinstance(self.run_config_version_id, UUID):
            run_config_version_id = str(self.run_config_version_id)
        else:
            run_config_version_id = self.run_config_version_id

        context_inputs: dict[str, Any] | Unset = UNSET
        if not isinstance(self.context_inputs, Unset):
            context_inputs = self.context_inputs.to_dict()

        target_fields: list[str] | Unset = UNSET
        if not isinstance(self.target_fields, Unset):
            target_fields = []
            for target_fields_item_data in self.target_fields:
                target_fields_item = target_fields_item_data.value
                target_fields.append(target_fields_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if system_prompt is not UNSET:
            field_dict["systemPrompt"] = system_prompt
        if run_config_version_id is not UNSET:
            field_dict["runConfigVersionId"] = run_config_version_id
        if context_inputs is not UNSET:
            field_dict["contextInputs"] = context_inputs
        if target_fields is not UNSET:
            field_dict["targetFields"] = target_fields

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.update_synthesizer_job_body_dto_context_inputs import UpdateSynthesizerJobBodyDtoContextInputs # noqa: PLC0415
        d = dict(src_dict)
        name = d.pop("name", UNSET)

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))


        system_prompt = d.pop("systemPrompt", UNSET)

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


        _context_inputs = d.pop("contextInputs", UNSET)
        context_inputs: UpdateSynthesizerJobBodyDtoContextInputs | Unset
        if isinstance(_context_inputs,  Unset):
            context_inputs = UNSET
        else:
            context_inputs = UpdateSynthesizerJobBodyDtoContextInputs.from_dict(_context_inputs)




        _target_fields = d.pop("targetFields", UNSET)
        target_fields: list[UpdateSynthesizerJobBodyDtoTargetFieldsItem] | Unset = UNSET
        if _target_fields is not UNSET:
            target_fields = []
            for target_fields_item_data in _target_fields:
                target_fields_item = UpdateSynthesizerJobBodyDtoTargetFieldsItem(target_fields_item_data)



                target_fields.append(target_fields_item)


        update_synthesizer_job_body_dto = cls(
            name=name,
            description=description,
            system_prompt=system_prompt,
            run_config_version_id=run_config_version_id,
            context_inputs=context_inputs,
            target_fields=target_fields,
        )


        update_synthesizer_job_body_dto.additional_properties = d
        return update_synthesizer_job_body_dto

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
