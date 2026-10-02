from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.content_type_input_enum import ContentTypeInputEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedOfferingRoleRequest")


@_attrs_define
class PatchedOfferingRoleRequest:
    """
    Attributes:
        name (Union[Unset, str]):
        description (Union[Unset, str]):
        content_type_input (Union[Unset, ContentTypeInputEnum]):
        offering (Union[Unset, UUID]): Offering UUID — pin role to this single offering.
    """

    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    content_type_input: Union[Unset, ContentTypeInputEnum] = UNSET
    offering: Union[Unset, UUID] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        description = self.description

        content_type_input: Union[Unset, str] = UNSET
        if not isinstance(self.content_type_input, Unset):
            content_type_input = self.content_type_input.value

        offering: Union[Unset, str] = UNSET
        if not isinstance(self.offering, Unset):
            offering = str(self.offering)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if content_type_input is not UNSET:
            field_dict["content_type_input"] = content_type_input
        if offering is not UNSET:
            field_dict["offering"] = offering

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        _content_type_input = d.pop("content_type_input", UNSET)
        content_type_input: Union[Unset, ContentTypeInputEnum]
        if isinstance(_content_type_input, Unset):
            content_type_input = UNSET
        else:
            content_type_input = ContentTypeInputEnum(_content_type_input)

        _offering = d.pop("offering", UNSET)
        offering: Union[Unset, UUID]
        if isinstance(_offering, Unset):
            offering = UNSET
        else:
            offering = UUID(_offering)

        patched_offering_role_request = cls(
            name=name,
            description=description,
            content_type_input=content_type_input,
            offering=offering,
        )

        patched_offering_role_request.additional_properties = d
        return patched_offering_role_request

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
