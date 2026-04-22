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

if TYPE_CHECKING:
    from ..models.run_bucket_data import RunBucketData


T = TypeVar("T", bound="RunStatsBucket")


@_attrs_define
class RunStatsBucket:
    """
    Attributes:
        bucket_start (datetime.datetime): datetime with the constraint that the value must have timezone info
        data (RunBucketData): Bucket payload data
    """

    bucket_start: datetime.datetime
    data: "RunBucketData"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        bucket_start = self.bucket_start.isoformat()

        data = self.data.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "bucket_start": bucket_start,
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.run_bucket_data import RunBucketData

        d = dict(src_dict)
        bucket_start = isoparse(d.pop("bucket_start"))

        data = RunBucketData.from_dict(d.pop("data"))

        run_stats_bucket = cls(
            bucket_start=bucket_start,
            data=data,
        )

        run_stats_bucket.additional_properties = d
        return run_stats_bucket

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
