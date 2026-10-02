from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.synthesizer_list_dto_items_built_in_key import SynthesizerListDtoItemsBuiltInKey
from ..models.synthesizer_list_dto_items_built_in_kind import SynthesizerListDtoItemsBuiltInKind
from ..models.synthesizer_list_dto_items_built_in_target_fields_item import SynthesizerListDtoItemsBuiltInTargetFieldsItem
from typing import cast

if TYPE_CHECKING:
  from ..models.synthesizer_list_dto_items_built_in_context_inputs import SynthesizerListDtoItemsBuiltInContextInputs





T = TypeVar("T", bound="SynthesizerListDtoItemsBuiltIn")



@_attrs_define
class SynthesizerListDtoItemsBuiltIn:
    """ Built-in synthesizer hardcoded into the platform binary and applied uniformly to every environment.

        Attributes:
            kind (SynthesizerListDtoItemsBuiltInKind): Discriminator marking this synthesizer as a built-in shipped with the
                platform.
            key (SynthesizerListDtoItemsBuiltInKey): Stable string key identifying a hardcoded built-in synthesizer.
            name (str): Display name of the built-in synthesizer.
            description (str): Description of what this built-in synthesizer does.
            system_prompt (str): Hardcoded system prompt the built-in sends to the agent.
            context_inputs (SynthesizerListDtoItemsBuiltInContextInputs): Inputs the built-in bundles into the synthesizer
                input tarball.
            target_fields (list[SynthesizerListDtoItemsBuiltInTargetFieldsItem]): Targets the built-in is allowed to write
                to.
            enabled (bool): Reflects the environment-level disable toggle; disabled built-ins are still listed for re-
                enabling but cannot be triggered.
     """

    kind: SynthesizerListDtoItemsBuiltInKind
    key: SynthesizerListDtoItemsBuiltInKey
    name: str
    description: str
    system_prompt: str
    context_inputs: SynthesizerListDtoItemsBuiltInContextInputs
    target_fields: list[SynthesizerListDtoItemsBuiltInTargetFieldsItem]
    enabled: bool





    def to_dict(self) -> dict[str, Any]:
        from ..models.synthesizer_list_dto_items_built_in_context_inputs import SynthesizerListDtoItemsBuiltInContextInputs # noqa: PLC0415
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
        from ..models.synthesizer_list_dto_items_built_in_context_inputs import SynthesizerListDtoItemsBuiltInContextInputs # noqa: PLC0415
        d = dict(src_dict)
        kind = SynthesizerListDtoItemsBuiltInKind(d.pop("kind"))




        key = SynthesizerListDtoItemsBuiltInKey(d.pop("key"))




        name = d.pop("name")

        description = d.pop("description")

        system_prompt = d.pop("systemPrompt")

        context_inputs = SynthesizerListDtoItemsBuiltInContextInputs.from_dict(d.pop("contextInputs"))




        target_fields = []
        _target_fields = d.pop("targetFields")
        for target_fields_item_data in (_target_fields):
            target_fields_item = SynthesizerListDtoItemsBuiltInTargetFieldsItem(target_fields_item_data)



            target_fields.append(target_fields_item)


        enabled = d.pop("enabled")

        synthesizer_list_dto_items_built_in = cls(
            kind=kind,
            key=key,
            name=name,
            description=description,
            system_prompt=system_prompt,
            context_inputs=context_inputs,
            target_fields=target_fields,
            enabled=enabled,
        )

        return synthesizer_list_dto_items_built_in

