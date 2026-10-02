from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedProviderCannedResponseRequest")


@_attrs_define
class PatchedProviderCannedResponseRequest:
    """
    Attributes:
        name (Union[Unset, str]):
        provider_helpdesk (Union[Unset, UUID]):
        text (Union[Unset, str]): Template text. Supports Django template syntax.
        category (Union[Unset, str]):
    """

    name: Union[Unset, str] = UNSET
    provider_helpdesk: Union[Unset, UUID] = UNSET
    text: Union[Unset, str] = UNSET
    category: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        provider_helpdesk: Union[Unset, str] = UNSET
        if not isinstance(self.provider_helpdesk, Unset):
            provider_helpdesk = str(self.provider_helpdesk)

        text = self.text

        category = self.category

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if provider_helpdesk is not UNSET:
            field_dict["provider_helpdesk"] = provider_helpdesk
        if text is not UNSET:
            field_dict["text"] = text
        if category is not UNSET:
            field_dict["category"] = category

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name", UNSET)

        _provider_helpdesk = d.pop("provider_helpdesk", UNSET)
        provider_helpdesk: Union[Unset, UUID]
        if isinstance(_provider_helpdesk, Unset):
            provider_helpdesk = UNSET
        else:
            provider_helpdesk = UUID(_provider_helpdesk)

        text = d.pop("text", UNSET)

        category = d.pop("category", UNSET)

        patched_provider_canned_response_request = cls(
            name=name,
            provider_helpdesk=provider_helpdesk,
            text=text,
            category=category,
        )

        patched_provider_canned_response_request.additional_properties = d
        return patched_provider_canned_response_request

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
