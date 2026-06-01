from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.metric_resource_type import check_metric_resource_type
from ..models.metric_resource_type import MetricResourceType
from typing import cast

if TYPE_CHECKING:
    from ..models.metric_attributes import MetricAttributes


T = TypeVar("T", bound="MetricResource")


@_attrs_define
class MetricResource:
    """JSON:API resource envelope for a metric data point.

    `id` must not be specified for create requests (the server assigns it).

        Example:
            {'attributes': {'created_at': '2026-04-10T18:00:01Z', 'dimensions': {'environment': 'production', 'service':
                'user-service'}, 'name': 'flags.evaluations', 'period_seconds': 60, 'recorded_at': '2026-04-10T18:00:00Z',
                'unit': 'evaluations', 'value': 1482}, 'id': 'a1b2c3d4-5678-90ab-cdef-1234567890ab', 'type': 'metric'}

        Attributes:
            type_ (MetricResourceType):
            attributes (MetricAttributes): A pre-aggregated metric data point recorded for the account.
            id (None | str | Unset):
    """

    type_: MetricResourceType
    attributes: MetricAttributes
    id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_: str = self.type_

        attributes = self.attributes.to_dict()

        id: None | str | Unset
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "attributes": attributes,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.metric_attributes import MetricAttributes

        d = dict(src_dict)
        type_ = check_metric_resource_type(d.pop("type"))

        attributes = MetricAttributes.from_dict(d.pop("attributes"))

        def _parse_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        id = _parse_id(d.pop("id", UNSET))

        metric_resource = cls(
            type_=type_,
            attributes=attributes,
            id=id,
        )

        metric_resource.additional_properties = d
        return metric_resource

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
