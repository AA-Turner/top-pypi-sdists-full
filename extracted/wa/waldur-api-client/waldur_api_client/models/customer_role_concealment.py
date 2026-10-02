from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CustomerRoleConcealment")


@_attrs_define
class CustomerRoleConcealment:
    """
    Attributes:
        uuid (UUID):
        role (UUID):
        role_name (str):
        customer_uuid (Union[None, str]):
        customer_name (Union[None, str]):
    """

    uuid: UUID
    role: UUID
    role_name: str
    customer_uuid: Union[None, str]
    customer_name: Union[None, str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        role = str(self.role)

        role_name = self.role_name

        customer_uuid: Union[None, str]
        customer_uuid = self.customer_uuid

        customer_name: Union[None, str]
        customer_name = self.customer_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "role": role,
                "role_name": role_name,
                "customer_uuid": customer_uuid,
                "customer_name": customer_name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        role = UUID(d.pop("role"))

        role_name = d.pop("role_name")

        def _parse_customer_uuid(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        customer_uuid = _parse_customer_uuid(d.pop("customer_uuid"))

        def _parse_customer_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        customer_name = _parse_customer_name(d.pop("customer_name"))

        customer_role_concealment = cls(
            uuid=uuid,
            role=role,
            role_name=role_name,
            customer_uuid=customer_uuid,
            customer_name=customer_name,
        )

        customer_role_concealment.additional_properties = d
        return customer_role_concealment

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
