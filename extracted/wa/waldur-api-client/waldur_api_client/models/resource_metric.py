import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.offering_metric import OfferingMetric


T = TypeVar("T", bound="ResourceMetric")


@_attrs_define
class ResourceMetric:
    """
    Attributes:
        offering_metric (OfferingMetric):
        period (str):
        period_start (datetime.datetime):
        current (Union[None, float]):
        previous (Union[None, float]):
    """

    offering_metric: "OfferingMetric"
    period: str
    period_start: datetime.datetime
    current: Union[None, float]
    previous: Union[None, float]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        offering_metric = self.offering_metric.to_dict()

        period = self.period

        period_start = self.period_start.isoformat()

        current: Union[None, float]
        current = self.current

        previous: Union[None, float]
        previous = self.previous

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "offering_metric": offering_metric,
                "period": period,
                "period_start": period_start,
                "current": current,
                "previous": previous,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.offering_metric import OfferingMetric

        d = dict(src_dict)
        offering_metric = OfferingMetric.from_dict(d.pop("offering_metric"))

        period = d.pop("period")

        period_start = isoparse(d.pop("period_start"))

        def _parse_current(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        current = _parse_current(d.pop("current"))

        def _parse_previous(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        previous = _parse_previous(d.pop("previous"))

        resource_metric = cls(
            offering_metric=offering_metric,
            period=period,
            period_start=period_start,
            current=current,
            previous=previous,
        )

        resource_metric.additional_properties = d
        return resource_metric

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
