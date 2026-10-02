from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.external_network_subnet_response import ExternalNetworkSubnetResponse


T = TypeVar("T", bound="ExternalNetworkResponse")


@_attrs_define
class ExternalNetworkResponse:
    """
    Attributes:
        id (str):
        name (str):
        is_shared (bool):
        subnets (list['ExternalNetworkSubnetResponse']):
    """

    id: str
    name: str
    is_shared: bool
    subnets: list["ExternalNetworkSubnetResponse"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        is_shared = self.is_shared

        subnets = []
        for subnets_item_data in self.subnets:
            subnets_item = subnets_item_data.to_dict()
            subnets.append(subnets_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "is_shared": is_shared,
                "subnets": subnets,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.external_network_subnet_response import ExternalNetworkSubnetResponse

        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        is_shared = d.pop("is_shared")

        subnets = []
        _subnets = d.pop("subnets")
        for subnets_item_data in _subnets:
            subnets_item = ExternalNetworkSubnetResponse.from_dict(subnets_item_data)

            subnets.append(subnets_item)

        external_network_response = cls(
            id=id,
            name=name,
            is_shared=is_shared,
            subnets=subnets,
        )

        external_network_response.additional_properties = d
        return external_network_response

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
