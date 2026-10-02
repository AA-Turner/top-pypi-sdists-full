from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ProfileCompleteness")


@_attrs_define
class ProfileCompleteness:
    """
    Attributes:
        is_complete (Union[Unset, bool]): Whether all mandatory profile fields are filled.
        missing_fields (Union[Unset, list[str]]): List of mandatory fields that are missing.
        mandatory_fields (Union[Unset, list[str]]): List of all mandatory fields.
        enforcement_enabled (Union[Unset, bool]): Whether enforcement of mandatory attributes is enabled.
    """

    is_complete: Union[Unset, bool] = UNSET
    missing_fields: Union[Unset, list[str]] = UNSET
    mandatory_fields: Union[Unset, list[str]] = UNSET
    enforcement_enabled: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        is_complete = self.is_complete

        missing_fields: Union[Unset, list[str]] = UNSET
        if not isinstance(self.missing_fields, Unset):
            missing_fields = self.missing_fields

        mandatory_fields: Union[Unset, list[str]] = UNSET
        if not isinstance(self.mandatory_fields, Unset):
            mandatory_fields = self.mandatory_fields

        enforcement_enabled = self.enforcement_enabled

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if is_complete is not UNSET:
            field_dict["is_complete"] = is_complete
        if missing_fields is not UNSET:
            field_dict["missing_fields"] = missing_fields
        if mandatory_fields is not UNSET:
            field_dict["mandatory_fields"] = mandatory_fields
        if enforcement_enabled is not UNSET:
            field_dict["enforcement_enabled"] = enforcement_enabled

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        is_complete = d.pop("is_complete", UNSET)

        missing_fields = cast(list[str], d.pop("missing_fields", UNSET))

        mandatory_fields = cast(list[str], d.pop("mandatory_fields", UNSET))

        enforcement_enabled = d.pop("enforcement_enabled", UNSET)

        profile_completeness = cls(
            is_complete=is_complete,
            missing_fields=missing_fields,
            mandatory_fields=mandatory_fields,
            enforcement_enabled=enforcement_enabled,
        )

        profile_completeness.additional_properties = d
        return profile_completeness

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
