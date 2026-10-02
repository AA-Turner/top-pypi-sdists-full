import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.matrix_room_state_enum import MatrixRoomStateEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.matrix_room_member_summary import MatrixRoomMemberSummary


T = TypeVar("T", bound="MatrixRoom")


@_attrs_define
class MatrixRoom:
    """
    Attributes:
        uuid (UUID):
        url (str):
        room_id (Union[None, str]): Matrix room ID, e.g. !abc:domain
        room_alias (str): Matrix room alias, e.g. #project-name:domain
        state (MatrixRoomStateEnum):
        error_message (str):
        scope (str):
        scope_uuid (Union[None, str]):
        scope_name (Union[None, str]):
        customer_uuid (Union[None, str]):
        customer_name (Union[None, str]):
        members_count (int):
        members (list['MatrixRoomMemberSummary']):
        current_user_membership_state (Union[None, str]):
        created (datetime.datetime):
        modified (datetime.datetime):
        room_name (Union[Unset, str]):
    """

    uuid: UUID
    url: str
    room_id: Union[None, str]
    room_alias: str
    state: MatrixRoomStateEnum
    error_message: str
    scope: str
    scope_uuid: Union[None, str]
    scope_name: Union[None, str]
    customer_uuid: Union[None, str]
    customer_name: Union[None, str]
    members_count: int
    members: list["MatrixRoomMemberSummary"]
    current_user_membership_state: Union[None, str]
    created: datetime.datetime
    modified: datetime.datetime
    room_name: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        url = self.url

        room_id: Union[None, str]
        room_id = self.room_id

        room_alias = self.room_alias

        state = self.state.value

        error_message = self.error_message

        scope = self.scope

        scope_uuid: Union[None, str]
        scope_uuid = self.scope_uuid

        scope_name: Union[None, str]
        scope_name = self.scope_name

        customer_uuid: Union[None, str]
        customer_uuid = self.customer_uuid

        customer_name: Union[None, str]
        customer_name = self.customer_name

        members_count = self.members_count

        members = []
        for members_item_data in self.members:
            members_item = members_item_data.to_dict()
            members.append(members_item)

        current_user_membership_state: Union[None, str]
        current_user_membership_state = self.current_user_membership_state

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        room_name = self.room_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "url": url,
                "room_id": room_id,
                "room_alias": room_alias,
                "state": state,
                "error_message": error_message,
                "scope": scope,
                "scope_uuid": scope_uuid,
                "scope_name": scope_name,
                "customer_uuid": customer_uuid,
                "customer_name": customer_name,
                "members_count": members_count,
                "members": members,
                "current_user_membership_state": current_user_membership_state,
                "created": created,
                "modified": modified,
            }
        )
        if room_name is not UNSET:
            field_dict["room_name"] = room_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.matrix_room_member_summary import MatrixRoomMemberSummary

        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        url = d.pop("url")

        def _parse_room_id(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        room_id = _parse_room_id(d.pop("room_id"))

        room_alias = d.pop("room_alias")

        state = MatrixRoomStateEnum(d.pop("state"))

        error_message = d.pop("error_message")

        scope = d.pop("scope")

        def _parse_scope_uuid(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        scope_uuid = _parse_scope_uuid(d.pop("scope_uuid"))

        def _parse_scope_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        scope_name = _parse_scope_name(d.pop("scope_name"))

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

        members_count = d.pop("members_count")

        members = []
        _members = d.pop("members")
        for members_item_data in _members:
            members_item = MatrixRoomMemberSummary.from_dict(members_item_data)

            members.append(members_item)

        def _parse_current_user_membership_state(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        current_user_membership_state = _parse_current_user_membership_state(d.pop("current_user_membership_state"))

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        room_name = d.pop("room_name", UNSET)

        matrix_room = cls(
            uuid=uuid,
            url=url,
            room_id=room_id,
            room_alias=room_alias,
            state=state,
            error_message=error_message,
            scope=scope,
            scope_uuid=scope_uuid,
            scope_name=scope_name,
            customer_uuid=customer_uuid,
            customer_name=customer_name,
            members_count=members_count,
            members=members,
            current_user_membership_state=current_user_membership_state,
            created=created,
            modified=modified,
            room_name=room_name,
        )

        matrix_room.additional_properties = d
        return matrix_room

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
