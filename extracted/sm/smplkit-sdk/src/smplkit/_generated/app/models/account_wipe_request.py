from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset


T = TypeVar("T", bound="AccountWipeRequest")


@_attrs_define
class AccountWipeRequest:
    """Confirmation envelope for the wipe-account action.

    Example:
        {'confirm': True, 'generate_sample_data': False}

    Attributes:
        confirm (bool): Must be `true` for the wipe to proceed. Any other value returns 400.
        generate_sample_data (bool | Unset): When `true`, re-seed the account with the standard sample dataset after
            wiping. Best-effort: any seeding failure is logged but does not fail the wipe. Default: False.
    """

    confirm: bool
    generate_sample_data: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        confirm = self.confirm

        generate_sample_data = self.generate_sample_data

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "confirm": confirm,
            }
        )
        if generate_sample_data is not UNSET:
            field_dict["generate_sample_data"] = generate_sample_data

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        confirm = d.pop("confirm")

        generate_sample_data = d.pop("generate_sample_data", UNSET)

        account_wipe_request = cls(
            confirm=confirm,
            generate_sample_data=generate_sample_data,
        )

        account_wipe_request.additional_properties = d
        return account_wipe_request

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
