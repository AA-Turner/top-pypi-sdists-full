from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedSystemPromptRequest")


@_attrs_define
class PatchedSystemPromptRequest:
    """
    Attributes:
        name (Union[Unset, str]):
        description (Union[Unset, str]):
        custom_instructions (Union[Unset, str]): Additional instructions injected into the system prompt. Use this for
            organisation-specific context, terminology, FAQ content, or behavioural guidelines. Supports {assistant_name}
            and {organization} placeholders.
    """

    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    custom_instructions: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        description = self.description

        custom_instructions = self.custom_instructions

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if custom_instructions is not UNSET:
            field_dict["custom_instructions"] = custom_instructions

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        custom_instructions = d.pop("custom_instructions", UNSET)

        patched_system_prompt_request = cls(
            name=name,
            description=description,
            custom_instructions=custom_instructions,
        )

        patched_system_prompt_request.additional_properties = d
        return patched_system_prompt_request

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
