from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.access_subnet_impact_address import AccessSubnetImpactAddress


T = TypeVar("T", bound="AccessSubnetImpactResource")


@_attrs_define
class AccessSubnetImpactResource:
    """
    Attributes:
        resource_uuid (str):
        resource_name (str):
        project_name (str):
        offering_uuid (str):
        offering_name (str):
        concealment_enabled (bool):
        unrestricted (bool):
        addresses (list['AccessSubnetImpactAddress']):
        packed (list[str]):
    """

    resource_uuid: str
    resource_name: str
    project_name: str
    offering_uuid: str
    offering_name: str
    concealment_enabled: bool
    unrestricted: bool
    addresses: list["AccessSubnetImpactAddress"]
    packed: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        resource_uuid = self.resource_uuid

        resource_name = self.resource_name

        project_name = self.project_name

        offering_uuid = self.offering_uuid

        offering_name = self.offering_name

        concealment_enabled = self.concealment_enabled

        unrestricted = self.unrestricted

        addresses = []
        for addresses_item_data in self.addresses:
            addresses_item = addresses_item_data.to_dict()
            addresses.append(addresses_item)

        packed = self.packed

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "resource_uuid": resource_uuid,
                "resource_name": resource_name,
                "project_name": project_name,
                "offering_uuid": offering_uuid,
                "offering_name": offering_name,
                "concealment_enabled": concealment_enabled,
                "unrestricted": unrestricted,
                "addresses": addresses,
                "packed": packed,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.access_subnet_impact_address import AccessSubnetImpactAddress

        d = dict(src_dict)
        resource_uuid = d.pop("resource_uuid")

        resource_name = d.pop("resource_name")

        project_name = d.pop("project_name")

        offering_uuid = d.pop("offering_uuid")

        offering_name = d.pop("offering_name")

        concealment_enabled = d.pop("concealment_enabled")

        unrestricted = d.pop("unrestricted")

        addresses = []
        _addresses = d.pop("addresses")
        for addresses_item_data in _addresses:
            addresses_item = AccessSubnetImpactAddress.from_dict(addresses_item_data)

            addresses.append(addresses_item)

        packed = cast(list[str], d.pop("packed"))

        access_subnet_impact_resource = cls(
            resource_uuid=resource_uuid,
            resource_name=resource_name,
            project_name=project_name,
            offering_uuid=offering_uuid,
            offering_name=offering_name,
            concealment_enabled=concealment_enabled,
            unrestricted=unrestricted,
            addresses=addresses,
            packed=packed,
        )

        access_subnet_impact_resource.additional_properties = d
        return access_subnet_impact_resource

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
