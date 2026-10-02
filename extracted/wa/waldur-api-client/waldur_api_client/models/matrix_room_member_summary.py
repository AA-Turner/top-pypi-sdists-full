from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="MatrixRoomMemberSummary")


@_attrs_define
class MatrixRoomMemberSummary:
    """
    Attributes:
        user_full_name (str):
        matrix_user_id (str):
        membership_state (str):
    """

    user_full_name: str
    matrix_user_id: str
    membership_state: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        user_full_name = self.user_full_name

        matrix_user_id = self.matrix_user_id

        membership_state = self.membership_state

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "user_full_name": user_full_name,
                "matrix_user_id": matrix_user_id,
                "membership_state": membership_state,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        user_full_name = d.pop("user_full_name")

        matrix_user_id = d.pop("matrix_user_id")

        membership_state = d.pop("membership_state")

        matrix_room_member_summary = cls(
            user_full_name=user_full_name,
            matrix_user_id=matrix_user_id,
            membership_state=membership_state,
        )

        matrix_room_member_summary.additional_properties = d
        return matrix_room_member_summary

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
