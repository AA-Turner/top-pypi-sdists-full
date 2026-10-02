from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.usage_timeseries_bucket import UsageTimeseriesBucket


T = TypeVar("T", bound="ProjectUsageEntry")


@_attrs_define
class ProjectUsageEntry:
    """
    Attributes:
        project_uuid (UUID):
        project_name (str):
        usage (float):
        buckets (list['UsageTimeseriesBucket']):
    """

    project_uuid: UUID
    project_name: str
    usage: float
    buckets: list["UsageTimeseriesBucket"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project_uuid = str(self.project_uuid)

        project_name = self.project_name

        usage = self.usage

        buckets = []
        for buckets_item_data in self.buckets:
            buckets_item = buckets_item_data.to_dict()
            buckets.append(buckets_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "project_uuid": project_uuid,
                "project_name": project_name,
                "usage": usage,
                "buckets": buckets,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.usage_timeseries_bucket import UsageTimeseriesBucket

        d = dict(src_dict)
        project_uuid = UUID(d.pop("project_uuid"))

        project_name = d.pop("project_name")

        usage = d.pop("usage")

        buckets = []
        _buckets = d.pop("buckets")
        for buckets_item_data in _buckets:
            buckets_item = UsageTimeseriesBucket.from_dict(buckets_item_data)

            buckets.append(buckets_item)

        project_usage_entry = cls(
            project_uuid=project_uuid,
            project_name=project_name,
            usage=usage,
            buckets=buckets,
        )

        project_usage_entry.additional_properties = d
        return project_usage_entry

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
