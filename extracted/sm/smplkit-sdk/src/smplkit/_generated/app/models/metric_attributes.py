from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from dateutil.parser import isoparse
from typing import cast
import datetime

if TYPE_CHECKING:
    from ..models.metric_attributes_dimensions import MetricAttributesDimensions


T = TypeVar("T", bound="MetricAttributes")


@_attrs_define
class MetricAttributes:
    """A pre-aggregated metric data point recorded for the account.

    Attributes:
        name (str): Metric series name, e.g. `flags.evaluations`. Dot-separated.
        value (float | str): Aggregated value for this data point over `period_seconds`.
        period_seconds (int): Length of the aggregation window in seconds (e.g. `60` for a one-minute roll-up).
        recorded_at (datetime.datetime): Start of the aggregation window this data point covers.
        unit (None | str | Unset): Unit the value is expressed in, e.g. `evaluations`, `ms`, `bytes`.
        dimensions (MetricAttributesDimensions | Unset): Optional dimension keys that scope the data point, e.g.
            `environment`, `service`. Used as filter targets on the list endpoint via `filter[dimensions.<key>]=...`.
        created_at (datetime.datetime | None | Unset): When the data point was ingested.
    """

    name: str
    value: float | str
    period_seconds: int
    recorded_at: datetime.datetime
    unit: None | str | Unset = UNSET
    dimensions: MetricAttributesDimensions | Unset = UNSET
    created_at: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        value: float | str
        value = self.value

        period_seconds = self.period_seconds

        recorded_at = self.recorded_at.isoformat()

        unit: None | str | Unset
        if isinstance(self.unit, Unset):
            unit = UNSET
        else:
            unit = self.unit

        dimensions: dict[str, Any] | Unset = UNSET
        if not isinstance(self.dimensions, Unset):
            dimensions = self.dimensions.to_dict()

        created_at: None | str | Unset
        if isinstance(self.created_at, Unset):
            created_at = UNSET
        elif isinstance(self.created_at, datetime.datetime):
            created_at = self.created_at.isoformat()
        else:
            created_at = self.created_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "value": value,
                "period_seconds": period_seconds,
                "recorded_at": recorded_at,
            }
        )
        if unit is not UNSET:
            field_dict["unit"] = unit
        if dimensions is not UNSET:
            field_dict["dimensions"] = dimensions
        if created_at is not UNSET:
            field_dict["created_at"] = created_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.metric_attributes_dimensions import MetricAttributesDimensions

        d = dict(src_dict)
        name = d.pop("name")

        def _parse_value(data: object) -> float | str:
            return cast(float | str, data)

        value = _parse_value(d.pop("value"))

        period_seconds = d.pop("period_seconds")

        recorded_at = isoparse(d.pop("recorded_at"))

        def _parse_unit(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        unit = _parse_unit(d.pop("unit", UNSET))

        _dimensions = d.pop("dimensions", UNSET)
        dimensions: MetricAttributesDimensions | Unset
        if isinstance(_dimensions, Unset):
            dimensions = UNSET
        else:
            dimensions = MetricAttributesDimensions.from_dict(_dimensions)

        def _parse_created_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                created_at_type_0 = isoparse(data)

                return created_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        created_at = _parse_created_at(d.pop("created_at", UNSET))

        metric_attributes = cls(
            name=name,
            value=value,
            period_seconds=period_seconds,
            recorded_at=recorded_at,
            unit=unit,
            dimensions=dimensions,
            created_at=created_at,
        )

        metric_attributes.additional_properties = d
        return metric_attributes

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
