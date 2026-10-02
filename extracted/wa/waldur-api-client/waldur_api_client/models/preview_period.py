from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PreviewPeriod")


@_attrs_define
class PreviewPeriod:
    """
    Attributes:
        period (str):
        status (Union[Unset, str]):
        row_count (Union[Unset, int]):
    """

    period: str
    status: Union[Unset, str] = UNSET
    row_count: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        period = self.period

        status = self.status

        row_count = self.row_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "period": period,
            }
        )
        if status is not UNSET:
            field_dict["status"] = status
        if row_count is not UNSET:
            field_dict["row_count"] = row_count

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        period = d.pop("period")

        status = d.pop("status", UNSET)

        row_count = d.pop("row_count", UNSET)

        preview_period = cls(
            period=period,
            status=status,
            row_count=row_count,
        )

        preview_period.additional_properties = d
        return preview_period

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
