from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="HpcScriptPreview")


@_attrs_define
class HpcScriptPreview:
    """
    Attributes:
        script (str):
        errors (list[str]):
        warnings (list[str]):
    """

    script: str
    errors: list[str]
    warnings: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        script = self.script

        errors = self.errors

        warnings = self.warnings

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "script": script,
                "errors": errors,
                "warnings": warnings,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        script = d.pop("script")

        errors = cast(list[str], d.pop("errors"))

        warnings = cast(list[str], d.pop("warnings"))

        hpc_script_preview = cls(
            script=script,
            errors=errors,
            warnings=warnings,
        )

        hpc_script_preview.additional_properties = d
        return hpc_script_preview

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
