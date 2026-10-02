from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="IdentityBridgeResult")


@_attrs_define
class IdentityBridgeResult:
    """
    Attributes:
        uuid (UUID):
        created (bool):
        updated_fields (list[str]):
    """

    uuid: UUID
    created: bool
    updated_fields: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        created = self.created

        updated_fields = self.updated_fields

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "created": created,
                "updated_fields": updated_fields,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        created = d.pop("created")

        updated_fields = cast(list[str], d.pop("updated_fields"))

        identity_bridge_result = cls(
            uuid=uuid,
            created=created,
            updated_fields=updated_fields,
        )

        identity_bridge_result.additional_properties = d
        return identity_bridge_result

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
