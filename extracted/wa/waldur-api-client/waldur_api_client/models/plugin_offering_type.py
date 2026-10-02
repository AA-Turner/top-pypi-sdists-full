from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.plugin_component import PluginComponent


T = TypeVar("T", bound="PluginOfferingType")


@_attrs_define
class PluginOfferingType:
    """
    Attributes:
        offering_type (str):
        components (list['PluginComponent']):
        available_limits (list[str]):
    """

    offering_type: str
    components: list["PluginComponent"]
    available_limits: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        offering_type = self.offering_type

        components = []
        for components_item_data in self.components:
            components_item = components_item_data.to_dict()
            components.append(components_item)

        available_limits = self.available_limits

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "offering_type": offering_type,
                "components": components,
                "available_limits": available_limits,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.plugin_component import PluginComponent

        d = dict(src_dict)
        offering_type = d.pop("offering_type")

        components = []
        _components = d.pop("components")
        for components_item_data in _components:
            components_item = PluginComponent.from_dict(components_item_data)

            components.append(components_item)

        available_limits = cast(list[str], d.pop("available_limits"))

        plugin_offering_type = cls(
            offering_type=offering_type,
            components=components,
            available_limits=available_limits,
        )

        plugin_offering_type.additional_properties = d
        return plugin_offering_type

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
