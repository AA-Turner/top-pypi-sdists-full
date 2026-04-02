from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreatePoolMemberRequest")


@_attrs_define
class CreatePoolMemberRequest:
    """
    Attributes:
        pool (str): Pool this member belongs to
        address (str): An IPv4 or IPv6 address.
        protocol_port (int): Port on the backend server
        subnet_id (str):
        name (Union[Unset, str]):
        weight (Union[Unset, int]):  Default: 1.
    """

    pool: str
    address: str
    protocol_port: int
    subnet_id: str
    name: Union[Unset, str] = UNSET
    weight: Union[Unset, int] = 1
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        pool = self.pool

        address: str
        address = self.address

        protocol_port = self.protocol_port

        subnet_id = self.subnet_id

        name = self.name

        weight = self.weight

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "pool": pool,
                "address": address,
                "protocol_port": protocol_port,
                "subnet_id": subnet_id,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if weight is not UNSET:
            field_dict["weight"] = weight

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        pool = d.pop("pool")

        def _parse_address(data: object) -> str:
            return cast(str, data)

        address = _parse_address(d.pop("address"))

        protocol_port = d.pop("protocol_port")

        subnet_id = d.pop("subnet_id")

        name = d.pop("name", UNSET)

        weight = d.pop("weight", UNSET)

        create_pool_member_request = cls(
            pool=pool,
            address=address,
            protocol_port=protocol_port,
            subnet_id=subnet_id,
            name=name,
            weight=weight,
        )

        create_pool_member_request.additional_properties = d
        return create_pool_member_request

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
