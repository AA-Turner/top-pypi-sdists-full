from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.bucket_size import BucketSize
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.pipeline_run_bucket import PipelineRunBucket


T = TypeVar("T", bound="PipelineRunStatsResponse")


@_attrs_define
class PipelineRunStatsResponse:
    """
    Attributes:
        bucket_size (BucketSize): Bucket size for time series aggregation. 'all' returns a single entry covering the
            full period.
        period_end (datetime.datetime): datetime with the constraint that the value must have timezone info
        period_start (datetime.datetime): datetime with the constraint that the value must have timezone info
        tz (str): IANA timezone used for bucket alignment
        buckets (list[PipelineRunBucket] | Unset): Time series buckets with per-bucket pipeline run aggregates.
    """

    bucket_size: BucketSize
    period_end: datetime.datetime
    period_start: datetime.datetime
    tz: str
    buckets: list[PipelineRunBucket] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        bucket_size = self.bucket_size.value

        period_end = self.period_end.isoformat()

        period_start = self.period_start.isoformat()

        tz = self.tz

        buckets: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.buckets, Unset):
            buckets = []
            for buckets_item_data in self.buckets:
                buckets_item = buckets_item_data.to_dict()
                buckets.append(buckets_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "bucket_size": bucket_size,
                "period_end": period_end,
                "period_start": period_start,
                "tz": tz,
            }
        )
        if buckets is not UNSET:
            field_dict["buckets"] = buckets

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.pipeline_run_bucket import PipelineRunBucket

        d = dict(src_dict)
        bucket_size = BucketSize(d.pop("bucket_size"))

        period_end = isoparse(d.pop("period_end"))

        period_start = isoparse(d.pop("period_start"))

        tz = d.pop("tz")

        _buckets = d.pop("buckets", UNSET)
        buckets: list[PipelineRunBucket] | Unset = UNSET
        if _buckets is not UNSET:
            buckets = []
            for buckets_item_data in _buckets:
                buckets_item = PipelineRunBucket.from_dict(buckets_item_data)

                buckets.append(buckets_item)

        pipeline_run_stats_response = cls(
            bucket_size=bucket_size,
            period_end=period_end,
            period_start=period_start,
            tz=tz,
            buckets=buckets,
        )

        pipeline_run_stats_response.additional_properties = d
        return pipeline_run_stats_response

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
