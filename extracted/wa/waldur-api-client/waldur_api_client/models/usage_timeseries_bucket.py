import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="UsageTimeseriesBucket")


@_attrs_define
class UsageTimeseriesBucket:
    """
    Attributes:
        billing_period (datetime.date):
        usage (float):
    """

    billing_period: datetime.date
    usage: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        billing_period = self.billing_period.isoformat()

        usage = self.usage

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "billing_period": billing_period,
                "usage": usage,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        billing_period = isoparse(d.pop("billing_period")).date()

        usage = d.pop("usage")

        usage_timeseries_bucket = cls(
            billing_period=billing_period,
            usage=usage,
        )

        usage_timeseries_bucket.additional_properties = d
        return usage_timeseries_bucket

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
