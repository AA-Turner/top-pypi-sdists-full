from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.diagnose_check_status_enum import DiagnoseCheckStatusEnum

T = TypeVar("T", bound="DiagnoseCheck")


@_attrs_define
class DiagnoseCheck:
    """
    Attributes:
        check (str):
        status (DiagnoseCheckStatusEnum):
        detail (str):
        fix_hint (str):
    """

    check: str
    status: DiagnoseCheckStatusEnum
    detail: str
    fix_hint: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        check = self.check

        status = self.status.value

        detail = self.detail

        fix_hint = self.fix_hint

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "check": check,
                "status": status,
                "detail": detail,
                "fix_hint": fix_hint,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        check = d.pop("check")

        status = DiagnoseCheckStatusEnum(d.pop("status"))

        detail = d.pop("detail")

        fix_hint = d.pop("fix_hint")

        diagnose_check = cls(
            check=check,
            status=status,
            detail=detail,
            fix_hint=fix_hint,
        )

        diagnose_check.additional_properties = d
        return diagnose_check

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
