from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast






T = TypeVar("T", bound="UpdateEnvironmentSettingsDtoRunFieldConfigAttemptCount")



@_attrs_define
class UpdateEnvironmentSettingsDtoRunFieldConfigAttemptCount:
    """ Per-field config for the attempt-count input on the Run problem modal.

        Attributes:
            default (int | None): Default number of attempts pre-filled in the Run problem modal. Null leaves the field
                empty.
     """

    default: int | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        default: int | None
        default = self.default


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "default": default,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        def _parse_default(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        default = _parse_default(d.pop("default"))


        update_environment_settings_dto_run_field_config_attempt_count = cls(
            default=default,
        )


        update_environment_settings_dto_run_field_config_attempt_count.additional_properties = d
        return update_environment_settings_dto_run_field_config_attempt_count

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
