from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SyncedGroup")


@_attrs_define
class SyncedGroup:
    """
    Attributes:
        local_name (str):
        remote_name (str):
        backend_id (str):
    """

    local_name: str
    remote_name: str
    backend_id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        local_name = self.local_name

        remote_name = self.remote_name

        backend_id = self.backend_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "local_name": local_name,
                "remote_name": remote_name,
                "backend_id": backend_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        local_name = d.pop("local_name")

        remote_name = d.pop("remote_name")

        backend_id = d.pop("backend_id")

        synced_group = cls(
            local_name=local_name,
            remote_name=remote_name,
            backend_id=backend_id,
        )

        synced_group.additional_properties = d
        return synced_group

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
