from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.built_in_synthesizer_dto_key import BuiltInSynthesizerDtoKey
from ..models.built_in_synthesizer_dto_kind import BuiltInSynthesizerDtoKind
from ..models.built_in_synthesizer_dto_target_fields_item import BuiltInSynthesizerDtoTargetFieldsItem
from typing import cast

if TYPE_CHECKING:
  from ..models.built_in_synthesizer_dto_context_inputs import BuiltInSynthesizerDtoContextInputs





T = TypeVar("T", bound="BuiltInSynthesizerDto")



@_attrs_define
class BuiltInSynthesizerDto:
    """ Built-in synthesizer hardcoded into the platform binary and applied uniformly to every environment.

        Example:
            {'kind': 'built-in', 'key': 'improve-prompt', 'name': 'Improve Prompt', 'description': 'Rewrites the task prompt
                for clarity and specificity using the problem context.', 'systemPrompt': 'You are a prompt engineer. Improve the
                given task prompt while preserving its intent.', 'contextInputs': {'files': {'problem': True, 'supporting':
                True, 'graderSupport': False, 'goldStandard': False}, 'rubrics': True, 'currentFieldValues': ['prompt',
                'tools'], 'forms': False}, 'targetFields': ['prompt'], 'enabled': True}

        Attributes:
            kind (BuiltInSynthesizerDtoKind): Discriminator marking this synthesizer as a built-in shipped with the
                platform.
            key (BuiltInSynthesizerDtoKey): Stable string key identifying a hardcoded built-in synthesizer.
            name (str): Display name of the built-in synthesizer.
            description (str): Description of what this built-in synthesizer does.
            system_prompt (str): Hardcoded system prompt the built-in sends to the agent.
            context_inputs (BuiltInSynthesizerDtoContextInputs): Inputs the built-in bundles into the synthesizer input
                tarball.
            target_fields (list[BuiltInSynthesizerDtoTargetFieldsItem]): Targets the built-in is allowed to write to.
            enabled (bool): Reflects the environment-level disable toggle; disabled built-ins are still listed for re-
                enabling but cannot be triggered.
     """

    kind: BuiltInSynthesizerDtoKind
    key: BuiltInSynthesizerDtoKey
    name: str
    description: str
    system_prompt: str
    context_inputs: BuiltInSynthesizerDtoContextInputs
    target_fields: list[BuiltInSynthesizerDtoTargetFieldsItem]
    enabled: bool





    def to_dict(self) -> dict[str, Any]:
        from ..models.built_in_synthesizer_dto_context_inputs import BuiltInSynthesizerDtoContextInputs # noqa: PLC0415
        kind = self.kind.value

        key = self.key.value

        name = self.name

        description = self.description

        system_prompt = self.system_prompt

        context_inputs = self.context_inputs.to_dict()

        target_fields = []
        for target_fields_item_data in self.target_fields:
            target_fields_item = target_fields_item_data.value
            target_fields.append(target_fields_item)



        enabled = self.enabled


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "kind": kind,
            "key": key,
            "name": name,
            "description": description,
            "systemPrompt": system_prompt,
            "contextInputs": context_inputs,
            "targetFields": target_fields,
            "enabled": enabled,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.built_in_synthesizer_dto_context_inputs import BuiltInSynthesizerDtoContextInputs # noqa: PLC0415
        d = dict(src_dict)
        kind = BuiltInSynthesizerDtoKind(d.pop("kind"))




        key = BuiltInSynthesizerDtoKey(d.pop("key"))




        name = d.pop("name")

        description = d.pop("description")

        system_prompt = d.pop("systemPrompt")

        context_inputs = BuiltInSynthesizerDtoContextInputs.from_dict(d.pop("contextInputs"))




        target_fields = []
        _target_fields = d.pop("targetFields")
        for target_fields_item_data in (_target_fields):
            target_fields_item = BuiltInSynthesizerDtoTargetFieldsItem(target_fields_item_data)



            target_fields.append(target_fields_item)


        enabled = d.pop("enabled")

        built_in_synthesizer_dto = cls(
            kind=kind,
            key=key,
            name=name,
            description=description,
            system_prompt=system_prompt,
            context_inputs=context_inputs,
            target_fields=target_fields,
            enabled=enabled,
        )

        return built_in_synthesizer_dto

