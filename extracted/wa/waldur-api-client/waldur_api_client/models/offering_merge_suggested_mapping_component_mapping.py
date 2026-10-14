from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.offering_merge_suggested_mapping_component_mapping_additional_property import (
        OfferingMergeSuggestedMappingComponentMappingAdditionalProperty,
    )


T = TypeVar("T", bound="OfferingMergeSuggestedMappingComponentMapping")


@_attrs_define
class OfferingMergeSuggestedMappingComponentMapping:
    """Per source offering UUID: source component type to the target component of the same type, else the same name."""

    additional_properties: dict[str, "OfferingMergeSuggestedMappingComponentMappingAdditionalProperty"] = _attrs_field(
        init=False, factory=dict
    )

    def to_dict(self) -> dict[str, Any]:
        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.offering_merge_suggested_mapping_component_mapping_additional_property import (
            OfferingMergeSuggestedMappingComponentMappingAdditionalProperty,
        )

        d = dict(src_dict)
        offering_merge_suggested_mapping_component_mapping = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = OfferingMergeSuggestedMappingComponentMappingAdditionalProperty.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        offering_merge_suggested_mapping_component_mapping.additional_properties = additional_properties
        return offering_merge_suggested_mapping_component_mapping

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> "OfferingMergeSuggestedMappingComponentMappingAdditionalProperty":
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: "OfferingMergeSuggestedMappingComponentMappingAdditionalProperty") -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
