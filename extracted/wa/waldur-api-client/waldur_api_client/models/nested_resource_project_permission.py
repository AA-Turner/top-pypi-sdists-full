import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="NestedResourceProjectPermission")


@_attrs_define
class NestedResourceProjectPermission:
    """
    Attributes:
        url (Union[Unset, str]):
        uuid (Union[Unset, str]):
        name (Union[Unset, str]):
        role_name (Union[Unset, str]):
        role_uuid (Union[Unset, UUID]):
        expiration_time (Union[None, Unset, datetime.datetime]):
        sync_state (Union[None, Unset, str]):
        sync_message (Union[None, Unset, str]):
        sync_reported_at (Union[None, Unset, datetime.datetime]):
    """

    url: Union[Unset, str] = UNSET
    uuid: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    role_name: Union[Unset, str] = UNSET
    role_uuid: Union[Unset, UUID] = UNSET
    expiration_time: Union[None, Unset, datetime.datetime] = UNSET
    sync_state: Union[None, Unset, str] = UNSET
    sync_message: Union[None, Unset, str] = UNSET
    sync_reported_at: Union[None, Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = self.uuid

        name = self.name

        role_name = self.role_name

        role_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.role_uuid, Unset):
            role_uuid = str(self.role_uuid)

        expiration_time: Union[None, Unset, str]
        if isinstance(self.expiration_time, Unset):
            expiration_time = UNSET
        elif isinstance(self.expiration_time, datetime.datetime):
            expiration_time = self.expiration_time.isoformat()
        else:
            expiration_time = self.expiration_time

        sync_state: Union[None, Unset, str]
        if isinstance(self.sync_state, Unset):
            sync_state = UNSET
        else:
            sync_state = self.sync_state

        sync_message: Union[None, Unset, str]
        if isinstance(self.sync_message, Unset):
            sync_message = UNSET
        else:
            sync_message = self.sync_message

        sync_reported_at: Union[None, Unset, str]
        if isinstance(self.sync_reported_at, Unset):
            sync_reported_at = UNSET
        elif isinstance(self.sync_reported_at, datetime.datetime):
            sync_reported_at = self.sync_reported_at.isoformat()
        else:
            sync_reported_at = self.sync_reported_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if url is not UNSET:
            field_dict["url"] = url
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if name is not UNSET:
            field_dict["name"] = name
        if role_name is not UNSET:
            field_dict["role_name"] = role_name
        if role_uuid is not UNSET:
            field_dict["role_uuid"] = role_uuid
        if expiration_time is not UNSET:
            field_dict["expiration_time"] = expiration_time
        if sync_state is not UNSET:
            field_dict["sync_state"] = sync_state
        if sync_message is not UNSET:
            field_dict["sync_message"] = sync_message
        if sync_reported_at is not UNSET:
            field_dict["sync_reported_at"] = sync_reported_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url", UNSET)

        uuid = d.pop("uuid", UNSET)

        name = d.pop("name", UNSET)

        role_name = d.pop("role_name", UNSET)

        _role_uuid = d.pop("role_uuid", UNSET)
        role_uuid: Union[Unset, UUID]
        if isinstance(_role_uuid, Unset):
            role_uuid = UNSET
        else:
            role_uuid = UUID(_role_uuid)

        def _parse_expiration_time(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                expiration_time_type_0 = isoparse(data)

                return expiration_time_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        expiration_time = _parse_expiration_time(d.pop("expiration_time", UNSET))

        def _parse_sync_state(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        sync_state = _parse_sync_state(d.pop("sync_state", UNSET))

        def _parse_sync_message(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        sync_message = _parse_sync_message(d.pop("sync_message", UNSET))

        def _parse_sync_reported_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                sync_reported_at_type_0 = isoparse(data)

                return sync_reported_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        sync_reported_at = _parse_sync_reported_at(d.pop("sync_reported_at", UNSET))

        nested_resource_project_permission = cls(
            url=url,
            uuid=uuid,
            name=name,
            role_name=role_name,
            role_uuid=role_uuid,
            expiration_time=expiration_time,
            sync_state=sync_state,
            sync_message=sync_message,
            sync_reported_at=sync_reported_at,
        )

        nested_resource_project_permission.additional_properties = d
        return nested_resource_project_permission

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
