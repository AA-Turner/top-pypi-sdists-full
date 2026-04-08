import datetime
from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.bucket_size import BucketSize

if TYPE_CHECKING:
    from ..models.run_stats_bucket import RunStatsBucket


T = TypeVar("T", bound="RunStatsResponse")


@_attrs_define
class RunStatsResponse:
    """
    Attributes:
        bucket_size (BucketSize): Bucket size for time series aggregation. 'all' returns a single entry covering the
            full period.
        buckets (list['RunStatsBucket']): Time series buckets. Single entry covering the full period when no bucket
            param is set.
        period_end (datetime.datetime): End of the reporting period (UTC)
        period_start (datetime.datetime): Start of the reporting period (UTC)
        tz (str): IANA timezone used for bucket alignment
    """

    bucket_size: BucketSize
    buckets: list["RunStatsBucket"]
    period_end: datetime.datetime
    period_start: datetime.datetime
    tz: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        bucket_size = self.bucket_size.value

        buckets = []
        for buckets_item_data in self.buckets:
            buckets_item = buckets_item_data.to_dict()
            buckets.append(buckets_item)

        period_end = self.period_end.isoformat()

        period_start = self.period_start.isoformat()

        tz = self.tz

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "bucket_size": bucket_size,
                "buckets": buckets,
                "period_end": period_end,
                "period_start": period_start,
                "tz": tz,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.run_stats_bucket import RunStatsBucket

        d = dict(src_dict)
        bucket_size = BucketSize(d.pop("bucket_size"))

        buckets = []
        _buckets = d.pop("buckets")
        for buckets_item_data in _buckets:
            buckets_item = RunStatsBucket.from_dict(buckets_item_data)

            buckets.append(buckets_item)

        period_end = isoparse(d.pop("period_end"))

        period_start = isoparse(d.pop("period_start"))

        tz = d.pop("tz")

        run_stats_response = cls(
            bucket_size=bucket_size,
            buckets=buckets,
            period_end=period_end,
            period_start=period_start,
            tz=tz,
        )

        run_stats_response.additional_properties = d
        return run_stats_response

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
