from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AttributeSourceDetail")


@_attrs_define
class AttributeSourceDetail:
    """
    Attributes:
        source (str):
        timestamp (str):
        age_days (float):
        is_stale (bool):
    """

    source: str
    timestamp: str
    age_days: float
    is_stale: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        source = self.source

        timestamp = self.timestamp

        age_days = self.age_days

        is_stale = self.is_stale

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "source": source,
                "timestamp": timestamp,
                "age_days": age_days,
                "is_stale": is_stale,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        source = d.pop("source")

        timestamp = d.pop("timestamp")

        age_days = d.pop("age_days")

        is_stale = d.pop("is_stale")

        attribute_source_detail = cls(
            source=source,
            timestamp=timestamp,
            age_days=age_days,
            is_stale=is_stale,
        )

        attribute_source_detail.additional_properties = d
        return attribute_source_detail

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
