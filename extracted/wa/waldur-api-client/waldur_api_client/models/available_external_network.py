from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.available_external_network_source_enum import AvailableExternalNetworkSourceEnum

if TYPE_CHECKING:
    from ..models.available_external_network_subnets_item import AvailableExternalNetworkSubnetsItem


T = TypeVar("T", bound="AvailableExternalNetwork")


@_attrs_define
class AvailableExternalNetwork:
    """
    Attributes:
        backend_id (str):
        name (str):
        description (str):
        source (AvailableExternalNetworkSourceEnum):
        subnets (list['AvailableExternalNetworkSubnetsItem']):
    """

    backend_id: str
    name: str
    description: str
    source: AvailableExternalNetworkSourceEnum
    subnets: list["AvailableExternalNetworkSubnetsItem"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        backend_id = self.backend_id

        name = self.name

        description = self.description

        source = self.source.value

        subnets = []
        for subnets_item_data in self.subnets:
            subnets_item = subnets_item_data.to_dict()
            subnets.append(subnets_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "backend_id": backend_id,
                "name": name,
                "description": description,
                "source": source,
                "subnets": subnets,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.available_external_network_subnets_item import AvailableExternalNetworkSubnetsItem

        d = dict(src_dict)
        backend_id = d.pop("backend_id")

        name = d.pop("name")

        description = d.pop("description")

        source = AvailableExternalNetworkSourceEnum(d.pop("source"))

        subnets = []
        _subnets = d.pop("subnets")
        for subnets_item_data in _subnets:
            subnets_item = AvailableExternalNetworkSubnetsItem.from_dict(subnets_item_data)

            subnets.append(subnets_item)

        available_external_network = cls(
            backend_id=backend_id,
            name=name,
            description=description,
            source=source,
            subnets=subnets,
        )

        available_external_network.additional_properties = d
        return available_external_network

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
