from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CustomerDefaultAffiliationsUpdateRequest")


@_attrs_define
class CustomerDefaultAffiliationsUpdateRequest:
    """
    Attributes:
        default_affiliations (Union[Unset, list[UUID]]):
    """

    default_affiliations: Union[Unset, list[UUID]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        default_affiliations: Union[Unset, list[str]] = UNSET
        if not isinstance(self.default_affiliations, Unset):
            default_affiliations = []
            for default_affiliations_item_data in self.default_affiliations:
                default_affiliations_item = str(default_affiliations_item_data)
                default_affiliations.append(default_affiliations_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if default_affiliations is not UNSET:
            field_dict["default_affiliations"] = default_affiliations

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        default_affiliations = []
        _default_affiliations = d.pop("default_affiliations", UNSET)
        for default_affiliations_item_data in _default_affiliations or []:
            default_affiliations_item = UUID(default_affiliations_item_data)

            default_affiliations.append(default_affiliations_item)

        customer_default_affiliations_update_request = cls(
            default_affiliations=default_affiliations,
        )

        customer_default_affiliations_update_request.additional_properties = d
        return customer_default_affiliations_update_request

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
