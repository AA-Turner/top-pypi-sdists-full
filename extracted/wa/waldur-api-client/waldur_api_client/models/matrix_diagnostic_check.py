from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="MatrixDiagnosticCheck")


@_attrs_define
class MatrixDiagnosticCheck:
    """
    Attributes:
        name (str):
        label (str):
        ok (bool):
        detail (str):
    """

    name: str
    label: str
    ok: bool
    detail: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        label = self.label

        ok = self.ok

        detail = self.detail

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "label": label,
                "ok": ok,
                "detail": detail,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        label = d.pop("label")

        ok = d.pop("ok")

        detail = d.pop("detail")

        matrix_diagnostic_check = cls(
            name=name,
            label=label,
            ok=ok,
            detail=detail,
        )

        matrix_diagnostic_check.additional_properties = d
        return matrix_diagnostic_check

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
