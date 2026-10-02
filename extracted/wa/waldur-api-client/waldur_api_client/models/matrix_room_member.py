import datetime
from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.membership_state_enum import MembershipStateEnum

T = TypeVar("T", bound="MatrixRoomMember")


@_attrs_define
class MatrixRoomMember:
    """
    Attributes:
        uuid (UUID):
        user_uuid (UUID):
        user_full_name (str):
        user_image (str):
        matrix_user_id (str):
        power_level (int):
        membership_state (MembershipStateEnum):
        created (datetime.datetime):
        modified (datetime.datetime):
    """

    uuid: UUID
    user_uuid: UUID
    user_full_name: str
    user_image: str
    matrix_user_id: str
    power_level: int
    membership_state: MembershipStateEnum
    created: datetime.datetime
    modified: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        user_uuid = str(self.user_uuid)

        user_full_name = self.user_full_name

        user_image = self.user_image

        matrix_user_id = self.matrix_user_id

        power_level = self.power_level

        membership_state = self.membership_state.value

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "user_uuid": user_uuid,
                "user_full_name": user_full_name,
                "user_image": user_image,
                "matrix_user_id": matrix_user_id,
                "power_level": power_level,
                "membership_state": membership_state,
                "created": created,
                "modified": modified,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        user_uuid = UUID(d.pop("user_uuid"))

        user_full_name = d.pop("user_full_name")

        user_image = d.pop("user_image")

        matrix_user_id = d.pop("matrix_user_id")

        power_level = d.pop("power_level")

        membership_state = MembershipStateEnum(d.pop("membership_state"))

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        matrix_room_member = cls(
            uuid=uuid,
            user_uuid=user_uuid,
            user_full_name=user_full_name,
            user_image=user_image,
            matrix_user_id=matrix_user_id,
            power_level=power_level,
            membership_state=membership_state,
            created=created,
            modified=modified,
        )

        matrix_room_member.additional_properties = d
        return matrix_room_member

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
