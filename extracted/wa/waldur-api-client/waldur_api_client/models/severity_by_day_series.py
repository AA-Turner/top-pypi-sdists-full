from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SeverityByDaySeries")


@_attrs_define
class SeverityByDaySeries:
    """
    Attributes:
        none (list[int]):
        low (list[int]):
        medium (list[int]):
        high (list[int]):
        critical (list[int]):
    """

    none: list[int]
    low: list[int]
    medium: list[int]
    high: list[int]
    critical: list[int]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        none = self.none

        low = self.low

        medium = self.medium

        high = self.high

        critical = self.critical

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "NONE": none,
                "LOW": low,
                "MEDIUM": medium,
                "HIGH": high,
                "CRITICAL": critical,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        none = cast(list[int], d.pop("NONE"))

        low = cast(list[int], d.pop("LOW"))

        medium = cast(list[int], d.pop("MEDIUM"))

        high = cast(list[int], d.pop("HIGH"))

        critical = cast(list[int], d.pop("CRITICAL"))

        severity_by_day_series = cls(
            none=none,
            low=low,
            medium=medium,
            high=high,
            critical=critical,
        )

        severity_by_day_series.additional_properties = d
        return severity_by_day_series

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
