from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ISDUserCount")


@_attrs_define
class ISDUserCount:
    """
    Attributes:
        isd (str):
        user_count (int):
        stale_user_count (int):
        oldest_sync (Union[None, str]):
    """

    isd: str
    user_count: int
    stale_user_count: int
    oldest_sync: Union[None, str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        isd = self.isd

        user_count = self.user_count

        stale_user_count = self.stale_user_count

        oldest_sync: Union[None, str]
        oldest_sync = self.oldest_sync

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "isd": isd,
                "user_count": user_count,
                "stale_user_count": stale_user_count,
                "oldest_sync": oldest_sync,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        isd = d.pop("isd")

        user_count = d.pop("user_count")

        stale_user_count = d.pop("stale_user_count")

        def _parse_oldest_sync(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        oldest_sync = _parse_oldest_sync(d.pop("oldest_sync"))

        isd_user_count = cls(
            isd=isd,
            user_count=user_count,
            stale_user_count=stale_user_count,
            oldest_sync=oldest_sync,
        )

        isd_user_count.additional_properties = d
        return isd_user_count

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
