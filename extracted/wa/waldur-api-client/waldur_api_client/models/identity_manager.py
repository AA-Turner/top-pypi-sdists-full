from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="IdentityManager")


@_attrs_define
class IdentityManager:
    """
    Attributes:
        uuid (UUID):
        full_name (str):
        managed_isds (list[str]):
    """

    uuid: UUID
    full_name: str
    managed_isds: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        full_name = self.full_name

        managed_isds = self.managed_isds

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "full_name": full_name,
                "managed_isds": managed_isds,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        full_name = d.pop("full_name")

        managed_isds = cast(list[str], d.pop("managed_isds"))

        identity_manager = cls(
            uuid=uuid,
            full_name=full_name,
            managed_isds=managed_isds,
        )

        identity_manager.additional_properties = d
        return identity_manager

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
