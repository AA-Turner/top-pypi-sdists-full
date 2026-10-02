from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="RmqStatsUser")


@_attrs_define
class RmqStatsUser:
    """
    Attributes:
        uuid (str): Waldur user UUID
        username (str): Waldur username
        full_name (str): User's full name
    """

    uuid: str
    username: str
    full_name: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = self.uuid

        username = self.username

        full_name = self.full_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "username": username,
                "full_name": full_name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = d.pop("uuid")

        username = d.pop("username")

        full_name = d.pop("full_name")

        rmq_stats_user = cls(
            uuid=uuid,
            username=username,
            full_name=full_name,
        )

        rmq_stats_user.additional_properties = d
        return rmq_stats_user

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
