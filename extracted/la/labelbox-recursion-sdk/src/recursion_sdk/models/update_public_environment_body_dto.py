from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="UpdatePublicEnvironmentBodyDto")



@_attrs_define
class UpdatePublicEnvironmentBodyDto:
    """ Patch body for updating the marketplace listing of a published environment (at least one field required).

        Attributes:
            description (str | Unset): Updated marketing description; omit to keep the current value.
            image_url (str | Unset): Updated cover image URL; omit to keep the current value.
     """

    description: str | Unset = UNSET
    image_url: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        description = self.description

        image_url = self.image_url


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if description is not UNSET:
            field_dict["description"] = description
        if image_url is not UNSET:
            field_dict["imageUrl"] = image_url

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        description = d.pop("description", UNSET)

        image_url = d.pop("imageUrl", UNSET)

        update_public_environment_body_dto = cls(
            description=description,
            image_url=image_url,
        )


        update_public_environment_body_dto.additional_properties = d
        return update_public_environment_body_dto

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
