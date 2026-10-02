from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.member_sync_status_entry_scope_type_enum import MemberSyncStatusEntryScopeTypeEnum
from ..models.member_sync_status_entry_state_enum import MemberSyncStatusEntryStateEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="MemberSyncStatusEntryRequest")


@_attrs_define
class MemberSyncStatusEntryRequest:
    """
    Attributes:
        scope_type (MemberSyncStatusEntryScopeTypeEnum):
        role_name (str):
        state (MemberSyncStatusEntryStateEnum):
        username (Union[Unset, str]):
        user_uuid (Union[Unset, UUID]):
        resource_project_uuid (Union[Unset, UUID]):
        message (Union[Unset, str]):  Default: ''.
    """

    scope_type: MemberSyncStatusEntryScopeTypeEnum
    role_name: str
    state: MemberSyncStatusEntryStateEnum
    username: Union[Unset, str] = UNSET
    user_uuid: Union[Unset, UUID] = UNSET
    resource_project_uuid: Union[Unset, UUID] = UNSET
    message: Union[Unset, str] = ""
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        scope_type = self.scope_type.value

        role_name = self.role_name

        state = self.state.value

        username = self.username

        user_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.user_uuid, Unset):
            user_uuid = str(self.user_uuid)

        resource_project_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.resource_project_uuid, Unset):
            resource_project_uuid = str(self.resource_project_uuid)

        message = self.message

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "scope_type": scope_type,
                "role_name": role_name,
                "state": state,
            }
        )
        if username is not UNSET:
            field_dict["username"] = username
        if user_uuid is not UNSET:
            field_dict["user_uuid"] = user_uuid
        if resource_project_uuid is not UNSET:
            field_dict["resource_project_uuid"] = resource_project_uuid
        if message is not UNSET:
            field_dict["message"] = message

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        scope_type = MemberSyncStatusEntryScopeTypeEnum(d.pop("scope_type"))

        role_name = d.pop("role_name")

        state = MemberSyncStatusEntryStateEnum(d.pop("state"))

        username = d.pop("username", UNSET)

        _user_uuid = d.pop("user_uuid", UNSET)
        user_uuid: Union[Unset, UUID]
        if isinstance(_user_uuid, Unset):
            user_uuid = UNSET
        else:
            user_uuid = UUID(_user_uuid)

        _resource_project_uuid = d.pop("resource_project_uuid", UNSET)
        resource_project_uuid: Union[Unset, UUID]
        if isinstance(_resource_project_uuid, Unset):
            resource_project_uuid = UNSET
        else:
            resource_project_uuid = UUID(_resource_project_uuid)

        message = d.pop("message", UNSET)

        member_sync_status_entry_request = cls(
            scope_type=scope_type,
            role_name=role_name,
            state=state,
            username=username,
            user_uuid=user_uuid,
            resource_project_uuid=resource_project_uuid,
            message=message,
        )

        member_sync_status_entry_request.additional_properties = d
        return member_sync_status_entry_request

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
