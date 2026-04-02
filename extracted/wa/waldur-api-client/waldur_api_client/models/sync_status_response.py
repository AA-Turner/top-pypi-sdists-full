from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.synced_group import SyncedGroup


T = TypeVar("T", bound="SyncStatusResponse")


@_attrs_define
class SyncStatusResponse:
    """
    Attributes:
        local_only (list[str]):
        remote_only (list[str]):
        synced (list['SyncedGroup']):
    """

    local_only: list[str]
    remote_only: list[str]
    synced: list["SyncedGroup"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        local_only = self.local_only

        remote_only = self.remote_only

        synced = []
        for synced_item_data in self.synced:
            synced_item = synced_item_data.to_dict()
            synced.append(synced_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "local_only": local_only,
                "remote_only": remote_only,
                "synced": synced,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.synced_group import SyncedGroup

        d = dict(src_dict)
        local_only = cast(list[str], d.pop("local_only"))

        remote_only = cast(list[str], d.pop("remote_only"))

        synced = []
        _synced = d.pop("synced")
        for synced_item_data in _synced:
            synced_item = SyncedGroup.from_dict(synced_item_data)

            synced.append(synced_item)

        sync_status_response = cls(
            local_only=local_only,
            remote_only=remote_only,
            synced=synced,
        )

        sync_status_response.additional_properties = d
        return sync_status_response

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
