import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.remote_resource_sync_status_remote_state_enum import RemoteResourceSyncStatusRemoteStateEnum
from ..models.resource_state import ResourceState
from ..models.sync_status_enum import SyncStatusEnum

T = TypeVar("T", bound="RemoteResourceSyncStatus")


@_attrs_define
class RemoteResourceSyncStatus:
    """
    Attributes:
        local_state (ResourceState):
        remote_state (Union[None, RemoteResourceSyncStatusRemoteStateEnum]): Remote resource state
        sync_status (SyncStatusEnum):
        last_sync (Union[None, datetime.datetime]): Last sync timestamp
    """

    local_state: ResourceState
    remote_state: Union[None, RemoteResourceSyncStatusRemoteStateEnum]
    sync_status: SyncStatusEnum
    last_sync: Union[None, datetime.datetime]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        local_state = self.local_state.value

        remote_state: Union[None, int]
        if isinstance(self.remote_state, RemoteResourceSyncStatusRemoteStateEnum):
            remote_state = self.remote_state.value
        else:
            remote_state = self.remote_state

        sync_status = self.sync_status.value

        last_sync: Union[None, str]
        if isinstance(self.last_sync, datetime.datetime):
            last_sync = self.last_sync.isoformat()
        else:
            last_sync = self.last_sync

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "local_state": local_state,
                "remote_state": remote_state,
                "sync_status": sync_status,
                "last_sync": last_sync,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        local_state = ResourceState(d.pop("local_state"))

        def _parse_remote_state(data: object) -> Union[None, RemoteResourceSyncStatusRemoteStateEnum]:
            if data is None:
                return data
            try:
                if not isinstance(data, int):
                    raise TypeError()
                remote_state_type_0 = RemoteResourceSyncStatusRemoteStateEnum(data)

                return remote_state_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, RemoteResourceSyncStatusRemoteStateEnum], data)

        remote_state = _parse_remote_state(d.pop("remote_state"))

        sync_status = SyncStatusEnum(d.pop("sync_status"))

        def _parse_last_sync(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_sync_type_0 = isoparse(data)

                return last_sync_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        last_sync = _parse_last_sync(d.pop("last_sync"))

        remote_resource_sync_status = cls(
            local_state=local_state,
            remote_state=remote_state,
            sync_status=sync_status,
            last_sync=last_sync,
        )

        remote_resource_sync_status.additional_properties = d
        return remote_resource_sync_status

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
