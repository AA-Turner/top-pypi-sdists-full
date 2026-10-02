from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CreateLoadBalancer")


@_attrs_define
class CreateLoadBalancer:
    """
    Attributes:
        url (str):
        uuid (UUID):
        name (str):
        tenant (str): OpenStack tenant this load balancer belongs to
        vip_subnet (str):
    """

    url: str
    uuid: UUID
    name: str
    tenant: str
    vip_subnet: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        name = self.name

        tenant = self.tenant

        vip_subnet = self.vip_subnet

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "name": name,
                "tenant": tenant,
                "vip_subnet": vip_subnet,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        name = d.pop("name")

        tenant = d.pop("tenant")

        vip_subnet = d.pop("vip_subnet")

        create_load_balancer = cls(
            url=url,
            uuid=uuid,
            name=name,
            tenant=tenant,
            vip_subnet=vip_subnet,
        )

        create_load_balancer.additional_properties = d
        return create_load_balancer

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
