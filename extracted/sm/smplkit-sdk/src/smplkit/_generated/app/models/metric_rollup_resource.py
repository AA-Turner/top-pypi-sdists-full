from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


from ..models.metric_rollup_resource_type import check_metric_rollup_resource_type
from ..models.metric_rollup_resource_type import MetricRollupResourceType

if TYPE_CHECKING:
    from ..models.metric_rollup_attributes import MetricRollupAttributes


T = TypeVar("T", bound="MetricRollupResource")


@_attrs_define
class MetricRollupResource:
    """JSON:API resource envelope for a metric rollup.

    Example:
        {'attributes': {'bucket': '2026-04-10T15:00:00Z', 'name': 'flags.evaluations', 'rollup': '1h', 'unit':
            'evaluations', 'value': 87420}, 'type': 'metric_rollup'}

    Attributes:
        type_ (MetricRollupResourceType):
        attributes (MetricRollupAttributes): An aggregated metric value over a fixed-size time bucket.
    """

    type_: MetricRollupResourceType
    attributes: MetricRollupAttributes
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_: str = self.type_

        attributes = self.attributes.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "attributes": attributes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.metric_rollup_attributes import MetricRollupAttributes

        d = dict(src_dict)
        type_ = check_metric_rollup_resource_type(d.pop("type"))

        attributes = MetricRollupAttributes.from_dict(d.pop("attributes"))

        metric_rollup_resource = cls(
            type_=type_,
            attributes=attributes,
        )

        metric_rollup_resource.additional_properties = d
        return metric_rollup_resource

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
