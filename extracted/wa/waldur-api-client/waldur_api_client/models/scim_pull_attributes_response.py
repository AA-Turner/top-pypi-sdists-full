from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ScimPullAttributesResponse")


@_attrs_define
class ScimPullAttributesResponse:
    """
    Attributes:
        detail (str):
        changed_fields (Union[Unset, list[str]]):
    """

    detail: str
    changed_fields: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        detail = self.detail

        changed_fields: Union[Unset, list[str]] = UNSET
        if not isinstance(self.changed_fields, Unset):
            changed_fields = self.changed_fields

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "detail": detail,
            }
        )
        if changed_fields is not UNSET:
            field_dict["changed_fields"] = changed_fields

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        detail = d.pop("detail")

        changed_fields = cast(list[str], d.pop("changed_fields", UNSET))

        scim_pull_attributes_response = cls(
            detail=detail,
            changed_fields=changed_fields,
        )

        scim_pull_attributes_response.additional_properties = d
        return scim_pull_attributes_response

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
