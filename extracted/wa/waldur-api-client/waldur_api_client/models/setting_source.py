import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.setting_source_source_enum import SettingSourceSourceEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="SettingSource")


@_attrs_define
class SettingSource:
    """
    Attributes:
        key (str):
        source (SettingSourceSourceEnum):
        source_detail (str): File, command or other origin within the source.
        locked (bool): Managed by the deployment: cannot be changed through the API or the Django admin.
        managed_by (str): File or command that re-applies the setting on every deploy, so a change made elsewhere does
            not last. Empty when no deploy does, such as for a value the deployment only seeded.
        updated_at (datetime.datetime):
        updated_by_username (Union[None, Unset, str]):
    """

    key: str
    source: SettingSourceSourceEnum
    source_detail: str
    locked: bool
    managed_by: str
    updated_at: datetime.datetime
    updated_by_username: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        key = self.key

        source = self.source.value

        source_detail = self.source_detail

        locked = self.locked

        managed_by = self.managed_by

        updated_at = self.updated_at.isoformat()

        updated_by_username: Union[None, Unset, str]
        if isinstance(self.updated_by_username, Unset):
            updated_by_username = UNSET
        else:
            updated_by_username = self.updated_by_username

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "key": key,
                "source": source,
                "source_detail": source_detail,
                "locked": locked,
                "managed_by": managed_by,
                "updated_at": updated_at,
            }
        )
        if updated_by_username is not UNSET:
            field_dict["updated_by_username"] = updated_by_username

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        key = d.pop("key")

        source = SettingSourceSourceEnum(d.pop("source"))

        source_detail = d.pop("source_detail")

        locked = d.pop("locked")

        managed_by = d.pop("managed_by")

        updated_at = isoparse(d.pop("updated_at"))

        def _parse_updated_by_username(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        updated_by_username = _parse_updated_by_username(d.pop("updated_by_username", UNSET))

        setting_source = cls(
            key=key,
            source=source,
            source_detail=source_detail,
            locked=locked,
            managed_by=managed_by,
            updated_at=updated_at,
            updated_by_username=updated_by_username,
        )

        setting_source.additional_properties = d
        return setting_source

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
