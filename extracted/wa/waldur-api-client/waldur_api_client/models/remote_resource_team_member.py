from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.sync_status_enum import SyncStatusEnum

T = TypeVar("T", bound="RemoteResourceTeamMember")


@_attrs_define
class RemoteResourceTeamMember:
    """
    Attributes:
        full_name (str): Full name
        local_role (str): Local role
        remote_role (str): Remote role
        sync_status (SyncStatusEnum):
    """

    full_name: str
    local_role: str
    remote_role: str
    sync_status: SyncStatusEnum
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        full_name = self.full_name

        local_role = self.local_role

        remote_role = self.remote_role

        sync_status = self.sync_status.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "full_name": full_name,
                "local_role": local_role,
                "remote_role": remote_role,
                "sync_status": sync_status,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        full_name = d.pop("full_name")

        local_role = d.pop("local_role")

        remote_role = d.pop("remote_role")

        sync_status = SyncStatusEnum(d.pop("sync_status"))

        remote_resource_team_member = cls(
            full_name=full_name,
            local_role=local_role,
            remote_role=remote_role,
            sync_status=sync_status,
        )

        remote_resource_team_member.additional_properties = d
        return remote_resource_team_member

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
