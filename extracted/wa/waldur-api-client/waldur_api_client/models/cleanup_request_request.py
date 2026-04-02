from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CleanupRequestRequest")


@_attrs_define
class CleanupRequestRequest:
    """
    Attributes:
        dry_run (Union[Unset, bool]): If true, only return what would be deleted without actually deleting Default:
            True.
        older_than_hours (Union[Unset, int]): Delete entries older than this many hours Default: 24.
    """

    dry_run: Union[Unset, bool] = True
    older_than_hours: Union[Unset, int] = 24
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        dry_run = self.dry_run

        older_than_hours = self.older_than_hours

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if dry_run is not UNSET:
            field_dict["dry_run"] = dry_run
        if older_than_hours is not UNSET:
            field_dict["older_than_hours"] = older_than_hours

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        dry_run = d.pop("dry_run", UNSET)

        older_than_hours = d.pop("older_than_hours", UNSET)

        cleanup_request_request = cls(
            dry_run=dry_run,
            older_than_hours=older_than_hours,
        )

        cleanup_request_request.additional_properties = d
        return cleanup_request_request

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
