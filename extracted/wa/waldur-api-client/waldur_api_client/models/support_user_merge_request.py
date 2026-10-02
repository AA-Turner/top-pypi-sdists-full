from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SupportUserMergeRequest")


@_attrs_define
class SupportUserMergeRequest:
    """
    Attributes:
        source_users (list[UUID]): Support users to merge into this one. They will be deleted and their issues, comments
            and attachments re-pointed to this user.
    """

    source_users: list[UUID]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        source_users = []
        for source_users_item_data in self.source_users:
            source_users_item = str(source_users_item_data)
            source_users.append(source_users_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "source_users": source_users,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        source_users = []
        _source_users = d.pop("source_users")
        for source_users_item_data in _source_users:
            source_users_item = UUID(source_users_item_data)

            source_users.append(source_users_item)

        support_user_merge_request = cls(
            source_users=source_users,
        )

        support_user_merge_request.additional_properties = d
        return support_user_merge_request

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
