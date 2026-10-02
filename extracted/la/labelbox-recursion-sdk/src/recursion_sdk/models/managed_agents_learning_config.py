from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="ManagedAgentsLearningConfig")



@_attrs_define
class ManagedAgentsLearningConfig:
    """ Model and guidance for automatic learning from an agent's finished sessions. The default model follows the agent's
    model.

        Example:
            {'instructions': 'example', 'memory_model_ref': 'example', 'reflector_agent_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}

        Attributes:
            instructions (str | Unset): Read-only standing guidance for every consolidation of this agent. Capped at 4096
                characters; the learning PATCH does not accept this field.
            memory_model_ref (str | Unset): Model used for all memory learning stages. Empty inherits the agent's model; an
                explicit model reference or gateway model overrides it.
            reflector_agent_id (str | Unset): Read-only analyzer reference used for memory updates. Empty uses the platform
                default; the learning PATCH does not accept this field.
     """

    instructions: str | Unset = UNSET
    memory_model_ref: str | Unset = UNSET
    reflector_agent_id: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        instructions = self.instructions

        memory_model_ref = self.memory_model_ref

        reflector_agent_id = self.reflector_agent_id


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if instructions is not UNSET:
            field_dict["instructions"] = instructions
        if memory_model_ref is not UNSET:
            field_dict["memory_model_ref"] = memory_model_ref
        if reflector_agent_id is not UNSET:
            field_dict["reflector_agent_id"] = reflector_agent_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        instructions = d.pop("instructions", UNSET)

        memory_model_ref = d.pop("memory_model_ref", UNSET)

        reflector_agent_id = d.pop("reflector_agent_id", UNSET)

        managed_agents_learning_config = cls(
            instructions=instructions,
            memory_model_ref=memory_model_ref,
            reflector_agent_id=reflector_agent_id,
        )


        managed_agents_learning_config.additional_properties = d
        return managed_agents_learning_config

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
