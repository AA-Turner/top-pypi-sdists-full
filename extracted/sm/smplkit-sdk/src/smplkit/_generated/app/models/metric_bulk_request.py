from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


if TYPE_CHECKING:
    from ..models.metric_resource import MetricResource


T = TypeVar("T", bound="MetricBulkRequest")


@_attrs_define
class MetricBulkRequest:
    """Bulk-ingest request envelope for metric data points.

    Example:
        {'data': [{'attributes': {'dimensions': {'environment': 'production'}, 'name': 'flags.evaluations',
            'period_seconds': 60, 'recorded_at': '2026-04-10T18:00:00Z', 'unit': 'evaluations', 'value': 1482}, 'type':
            'metric'}]}

    Attributes:
        data (list[MetricResource]): Metric data points to ingest in a single request.
    """

    data: list[MetricResource]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = []
        for data_item_data in self.data:
            data_item = data_item_data.to_dict()
            data.append(data_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.metric_resource import MetricResource

        d = dict(src_dict)
        data = []
        _data = d.pop("data")
        for data_item_data in _data:
            data_item = MetricResource.from_dict(data_item_data)

            data.append(data_item)

        metric_bulk_request = cls(
            data=data,
        )

        metric_bulk_request.additional_properties = d
        return metric_bulk_request

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
