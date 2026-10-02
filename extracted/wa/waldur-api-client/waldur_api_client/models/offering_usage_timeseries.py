import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.usage_timeseries_bucket import UsageTimeseriesBucket


T = TypeVar("T", bound="OfferingUsageTimeseries")


@_attrs_define
class OfferingUsageTimeseries:
    """
    Attributes:
        offering_uuid (UUID):
        offering_name (str):
        type_ (str):
        name (str):
        measured_unit (str):
        billing_type (str):
        limit_period (Union[None, str]):
        limit (Union[None, float]):
        current_period_label (str):
        current_period_start (Union[None, datetime.date]):
        current_period_end (Union[None, datetime.date]):
        today (datetime.date):
        buckets (list['UsageTimeseriesBucket']):
    """

    offering_uuid: UUID
    offering_name: str
    type_: str
    name: str
    measured_unit: str
    billing_type: str
    limit_period: Union[None, str]
    limit: Union[None, float]
    current_period_label: str
    current_period_start: Union[None, datetime.date]
    current_period_end: Union[None, datetime.date]
    today: datetime.date
    buckets: list["UsageTimeseriesBucket"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        offering_uuid = str(self.offering_uuid)

        offering_name = self.offering_name

        type_ = self.type_

        name = self.name

        measured_unit = self.measured_unit

        billing_type = self.billing_type

        limit_period: Union[None, str]
        limit_period = self.limit_period

        limit: Union[None, float]
        limit = self.limit

        current_period_label = self.current_period_label

        current_period_start: Union[None, str]
        if isinstance(self.current_period_start, datetime.date):
            current_period_start = self.current_period_start.isoformat()
        else:
            current_period_start = self.current_period_start

        current_period_end: Union[None, str]
        if isinstance(self.current_period_end, datetime.date):
            current_period_end = self.current_period_end.isoformat()
        else:
            current_period_end = self.current_period_end

        today = self.today.isoformat()

        buckets = []
        for buckets_item_data in self.buckets:
            buckets_item = buckets_item_data.to_dict()
            buckets.append(buckets_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "offering_uuid": offering_uuid,
                "offering_name": offering_name,
                "type": type_,
                "name": name,
                "measured_unit": measured_unit,
                "billing_type": billing_type,
                "limit_period": limit_period,
                "limit": limit,
                "current_period_label": current_period_label,
                "current_period_start": current_period_start,
                "current_period_end": current_period_end,
                "today": today,
                "buckets": buckets,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.usage_timeseries_bucket import UsageTimeseriesBucket

        d = dict(src_dict)
        offering_uuid = UUID(d.pop("offering_uuid"))

        offering_name = d.pop("offering_name")

        type_ = d.pop("type")

        name = d.pop("name")

        measured_unit = d.pop("measured_unit")

        billing_type = d.pop("billing_type")

        def _parse_limit_period(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        limit_period = _parse_limit_period(d.pop("limit_period"))

        def _parse_limit(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        limit = _parse_limit(d.pop("limit"))

        current_period_label = d.pop("current_period_label")

        def _parse_current_period_start(data: object) -> Union[None, datetime.date]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                current_period_start_type_0 = isoparse(data).date()

                return current_period_start_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.date], data)

        current_period_start = _parse_current_period_start(d.pop("current_period_start"))

        def _parse_current_period_end(data: object) -> Union[None, datetime.date]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                current_period_end_type_0 = isoparse(data).date()

                return current_period_end_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.date], data)

        current_period_end = _parse_current_period_end(d.pop("current_period_end"))

        today = isoparse(d.pop("today")).date()

        buckets = []
        _buckets = d.pop("buckets")
        for buckets_item_data in _buckets:
            buckets_item = UsageTimeseriesBucket.from_dict(buckets_item_data)

            buckets.append(buckets_item)

        offering_usage_timeseries = cls(
            offering_uuid=offering_uuid,
            offering_name=offering_name,
            type_=type_,
            name=name,
            measured_unit=measured_unit,
            billing_type=billing_type,
            limit_period=limit_period,
            limit=limit,
            current_period_label=current_period_label,
            current_period_start=current_period_start,
            current_period_end=current_period_end,
            today=today,
            buckets=buckets,
        )

        offering_usage_timeseries.additional_properties = d
        return offering_usage_timeseries

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
