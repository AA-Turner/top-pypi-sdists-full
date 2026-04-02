from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.category_serializer_for_for_nested_fields_request import CategorySerializerForForNestedFieldsRequest


T = TypeVar("T", bound="PatchedCategoryComponentsRequest")


@_attrs_define
class PatchedCategoryComponentsRequest:
    """
    Attributes:
        type_ (Union[Unset, str]): Unique internal name of the measured unit, for example floating_ip.
        name (Union[Unset, str]): Display name for the measured unit, for example, Floating IP.
        description (Union[Unset, str]):
        measured_unit (Union[Unset, str]): Unit of measurement, for example, GB.
        category (Union[Unset, CategorySerializerForForNestedFieldsRequest]):
    """

    type_: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    measured_unit: Union[Unset, str] = UNSET
    category: Union[Unset, "CategorySerializerForForNestedFieldsRequest"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        name = self.name

        description = self.description

        measured_unit = self.measured_unit

        category: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.category, Unset):
            category = self.category.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if type_ is not UNSET:
            field_dict["type"] = type_
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if measured_unit is not UNSET:
            field_dict["measured_unit"] = measured_unit
        if category is not UNSET:
            field_dict["category"] = category

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.category_serializer_for_for_nested_fields_request import (
            CategorySerializerForForNestedFieldsRequest,
        )

        d = dict(src_dict)
        type_ = d.pop("type", UNSET)

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        measured_unit = d.pop("measured_unit", UNSET)

        _category = d.pop("category", UNSET)
        category: Union[Unset, CategorySerializerForForNestedFieldsRequest]
        if isinstance(_category, Unset):
            category = UNSET
        else:
            category = CategorySerializerForForNestedFieldsRequest.from_dict(_category)

        patched_category_components_request = cls(
            type_=type_,
            name=name,
            description=description,
            measured_unit=measured_unit,
            category=category,
        )

        patched_category_components_request.additional_properties = d
        return patched_category_components_request

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
