from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SyncResourcesResponse")


@_attrs_define
class SyncResourcesResponse:
    """
    Attributes:
        synced (int):
        created (int):
        updated (int):
    """

    synced: int
    created: int
    updated: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        synced = self.synced

        created = self.created

        updated = self.updated

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "synced": synced,
                "created": created,
                "updated": updated,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        synced = d.pop("synced")

        created = d.pop("created")

        updated = d.pop("updated")

        sync_resources_response = cls(
            synced=synced,
            created=created,
            updated=updated,
        )

        sync_resources_response.additional_properties = d
        return sync_resources_response

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
