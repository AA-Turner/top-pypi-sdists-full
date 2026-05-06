import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="ComponentStatsPerOffering")


@_attrs_define
class ComponentStatsPerOffering:
    """
    Attributes:
        type_ (str):
        name (str):
        description (str):
        measured_unit (str):
        billing_type (str):
        usage (float):
        limit_usage (float):
        limit (Union[None, float]):
        offering_name (str):
        offering_uuid (UUID):
        limit_period (Union[None, str]):
        current_period_label (str):
        current_period_start (Union[None, datetime.date]):
        current_period_end (Union[None, datetime.date]):
    """

    type_: str
    name: str
    description: str
    measured_unit: str
    billing_type: str
    usage: float
    limit_usage: float
    limit: Union[None, float]
    offering_name: str
    offering_uuid: UUID
    limit_period: Union[None, str]
    current_period_label: str
    current_period_start: Union[None, datetime.date]
    current_period_end: Union[None, datetime.date]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        name = self.name

        description = self.description

        measured_unit = self.measured_unit

        billing_type = self.billing_type

        usage = self.usage

        limit_usage = self.limit_usage

        limit: Union[None, float]
        limit = self.limit

        offering_name = self.offering_name

        offering_uuid = str(self.offering_uuid)

        limit_period: Union[None, str]
        limit_period = self.limit_period

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

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "name": name,
                "description": description,
                "measured_unit": measured_unit,
                "billing_type": billing_type,
                "usage": usage,
                "limit_usage": limit_usage,
                "limit": limit,
                "offering_name": offering_name,
                "offering_uuid": offering_uuid,
                "limit_period": limit_period,
                "current_period_label": current_period_label,
                "current_period_start": current_period_start,
                "current_period_end": current_period_end,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = d.pop("type")

        name = d.pop("name")

        description = d.pop("description")

        measured_unit = d.pop("measured_unit")

        billing_type = d.pop("billing_type")

        usage = d.pop("usage")

        limit_usage = d.pop("limit_usage")

        def _parse_limit(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        limit = _parse_limit(d.pop("limit"))

        offering_name = d.pop("offering_name")

        offering_uuid = UUID(d.pop("offering_uuid"))

        def _parse_limit_period(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        limit_period = _parse_limit_period(d.pop("limit_period"))

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

        component_stats_per_offering = cls(
            type_=type_,
            name=name,
            description=description,
            measured_unit=measured_unit,
            billing_type=billing_type,
            usage=usage,
            limit_usage=limit_usage,
            limit=limit,
            offering_name=offering_name,
            offering_uuid=offering_uuid,
            limit_period=limit_period,
            current_period_label=current_period_label,
            current_period_start=current_period_start,
            current_period_end=current_period_end,
        )

        component_stats_per_offering.additional_properties = d
        return component_stats_per_offering

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
