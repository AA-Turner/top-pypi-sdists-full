from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="DemoPresetLoadRequestRequest")


@_attrs_define
class DemoPresetLoadRequestRequest:
    """
    Attributes:
        dry_run (Union[Unset, bool]): Preview changes without applying them Default: False.
        cleanup_first (Union[Unset, bool]): Clean up existing data before loading the preset Default: True.
        skip_users (Union[Unset, bool]): Skip user import/cleanup Default: False.
        skip_roles (Union[Unset, bool]): Skip role import/cleanup Default: False.
    """

    dry_run: Union[Unset, bool] = False
    cleanup_first: Union[Unset, bool] = True
    skip_users: Union[Unset, bool] = False
    skip_roles: Union[Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        dry_run = self.dry_run

        cleanup_first = self.cleanup_first

        skip_users = self.skip_users

        skip_roles = self.skip_roles

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if dry_run is not UNSET:
            field_dict["dry_run"] = dry_run
        if cleanup_first is not UNSET:
            field_dict["cleanup_first"] = cleanup_first
        if skip_users is not UNSET:
            field_dict["skip_users"] = skip_users
        if skip_roles is not UNSET:
            field_dict["skip_roles"] = skip_roles

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        dry_run = d.pop("dry_run", UNSET)

        cleanup_first = d.pop("cleanup_first", UNSET)

        skip_users = d.pop("skip_users", UNSET)

        skip_roles = d.pop("skip_roles", UNSET)

        demo_preset_load_request_request = cls(
            dry_run=dry_run,
            cleanup_first=cleanup_first,
            skip_users=skip_users,
            skip_roles=skip_roles,
        )

        demo_preset_load_request_request.additional_properties = d
        return demo_preset_load_request_request

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
