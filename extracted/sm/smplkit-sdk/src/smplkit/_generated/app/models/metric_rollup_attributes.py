from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from dateutil.parser import isoparse
from typing import cast
import datetime


T = TypeVar("T", bound="MetricRollupAttributes")


@_attrs_define
class MetricRollupAttributes:
    """An aggregated metric value over a fixed-size time bucket.

    Attributes:
        name (str): Metric series name the rollup is computed from.
        value (str): Sum of the underlying metric values over the bucket.
        bucket (datetime.datetime): Start of the time bucket this rollup covers.
        rollup (str): Rollup interval. One of `1m`, `5m`, `15m`, `1h`, `6h`, `1d`.
        unit (None | str | Unset): Unit the value is expressed in.
    """

    name: str
    value: str
    bucket: datetime.datetime
    rollup: str
    unit: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        value = self.value

        bucket = self.bucket.isoformat()

        rollup = self.rollup

        unit: None | str | Unset
        if isinstance(self.unit, Unset):
            unit = UNSET
        else:
            unit = self.unit

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "value": value,
                "bucket": bucket,
                "rollup": rollup,
            }
        )
        if unit is not UNSET:
            field_dict["unit"] = unit

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        value = d.pop("value")

        bucket = isoparse(d.pop("bucket"))

        rollup = d.pop("rollup")

        def _parse_unit(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        unit = _parse_unit(d.pop("unit", UNSET))

        metric_rollup_attributes = cls(
            name=name,
            value=value,
            bucket=bucket,
            rollup=rollup,
            unit=unit,
        )

        metric_rollup_attributes.additional_properties = d
        return metric_rollup_attributes

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
