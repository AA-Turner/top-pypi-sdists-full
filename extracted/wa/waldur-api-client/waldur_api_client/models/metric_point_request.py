import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.metric_point_request_attributes import MetricPointRequestAttributes


T = TypeVar("T", bound="MetricPointRequest")


@_attrs_define
class MetricPointRequest:
    """
    Attributes:
        resource (UUID): UUID of the resource
        metric (str): Key of a metric the resource's offering adopts
        timestamp (datetime.datetime):
        value (float):
        start_time (Union[None, Unset, datetime.datetime]): Only for a counter reported as a running total: when the
            total started counting. Omit it to report the increment since the previous point.
        attributes (Union[Unset, MetricPointRequestAttributes]): Values of the attributes the metric declares
    """

    resource: UUID
    metric: str
    timestamp: datetime.datetime
    value: float
    start_time: Union[None, Unset, datetime.datetime] = UNSET
    attributes: Union[Unset, "MetricPointRequestAttributes"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        resource = str(self.resource)

        metric = self.metric

        timestamp = self.timestamp.isoformat()

        value = self.value

        start_time: Union[None, Unset, str]
        if isinstance(self.start_time, Unset):
            start_time = UNSET
        elif isinstance(self.start_time, datetime.datetime):
            start_time = self.start_time.isoformat()
        else:
            start_time = self.start_time

        attributes: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.attributes, Unset):
            attributes = self.attributes.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "resource": resource,
                "metric": metric,
                "timestamp": timestamp,
                "value": value,
            }
        )
        if start_time is not UNSET:
            field_dict["start_time"] = start_time
        if attributes is not UNSET:
            field_dict["attributes"] = attributes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.metric_point_request_attributes import MetricPointRequestAttributes

        d = dict(src_dict)
        resource = UUID(d.pop("resource"))

        metric = d.pop("metric")

        timestamp = isoparse(d.pop("timestamp"))

        value = d.pop("value")

        def _parse_start_time(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                start_time_type_0 = isoparse(data)

                return start_time_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        start_time = _parse_start_time(d.pop("start_time", UNSET))

        _attributes = d.pop("attributes", UNSET)
        attributes: Union[Unset, MetricPointRequestAttributes]
        if isinstance(_attributes, Unset):
            attributes = UNSET
        else:
            attributes = MetricPointRequestAttributes.from_dict(_attributes)

        metric_point_request = cls(
            resource=resource,
            metric=metric,
            timestamp=timestamp,
            value=value,
            start_time=start_time,
            attributes=attributes,
        )

        metric_point_request.additional_properties = d
        return metric_point_request

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
