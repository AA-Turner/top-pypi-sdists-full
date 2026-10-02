import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ComponentUsageMonthly")


@_attrs_define
class ComponentUsageMonthly:
    """
    Attributes:
        offering_uuid (Union[Unset, UUID]):
        offering_name (Union[Unset, str]):
        offering_type (Union[Unset, str]):
        service_provider_uuid (Union[Unset, UUID]):
        service_provider_name (Union[Unset, str]):
        category_uuid (Union[Unset, UUID]):
        category_title (Union[Unset, str]):
        component_type (Union[Unset, str]):
        component_name (Union[Unset, str]):
        measured_unit (Union[Unset, str]):
        billing_type (Union[Unset, str]):
        limit_amount (Union[Unset, int]):
        limit_period (Union[Unset, str]):
        billing_period (Union[Unset, datetime.date]):
        total_consumed (Union[Unset, str]):
        total_allocated (Union[Unset, str]):
        usage_percent (Union[None, Unset, str]):
    """

    offering_uuid: Union[Unset, UUID] = UNSET
    offering_name: Union[Unset, str] = UNSET
    offering_type: Union[Unset, str] = UNSET
    service_provider_uuid: Union[Unset, UUID] = UNSET
    service_provider_name: Union[Unset, str] = UNSET
    category_uuid: Union[Unset, UUID] = UNSET
    category_title: Union[Unset, str] = UNSET
    component_type: Union[Unset, str] = UNSET
    component_name: Union[Unset, str] = UNSET
    measured_unit: Union[Unset, str] = UNSET
    billing_type: Union[Unset, str] = UNSET
    limit_amount: Union[Unset, int] = UNSET
    limit_period: Union[Unset, str] = UNSET
    billing_period: Union[Unset, datetime.date] = UNSET
    total_consumed: Union[Unset, str] = UNSET
    total_allocated: Union[Unset, str] = UNSET
    usage_percent: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        offering_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.offering_uuid, Unset):
            offering_uuid = str(self.offering_uuid)

        offering_name = self.offering_name

        offering_type = self.offering_type

        service_provider_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.service_provider_uuid, Unset):
            service_provider_uuid = str(self.service_provider_uuid)

        service_provider_name = self.service_provider_name

        category_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.category_uuid, Unset):
            category_uuid = str(self.category_uuid)

        category_title = self.category_title

        component_type = self.component_type

        component_name = self.component_name

        measured_unit = self.measured_unit

        billing_type = self.billing_type

        limit_amount = self.limit_amount

        limit_period = self.limit_period

        billing_period: Union[Unset, str] = UNSET
        if not isinstance(self.billing_period, Unset):
            billing_period = self.billing_period.isoformat()

        total_consumed = self.total_consumed

        total_allocated = self.total_allocated

        usage_percent: Union[None, Unset, str]
        if isinstance(self.usage_percent, Unset):
            usage_percent = UNSET
        else:
            usage_percent = self.usage_percent

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if offering_uuid is not UNSET:
            field_dict["offering_uuid"] = offering_uuid
        if offering_name is not UNSET:
            field_dict["offering_name"] = offering_name
        if offering_type is not UNSET:
            field_dict["offering_type"] = offering_type
        if service_provider_uuid is not UNSET:
            field_dict["service_provider_uuid"] = service_provider_uuid
        if service_provider_name is not UNSET:
            field_dict["service_provider_name"] = service_provider_name
        if category_uuid is not UNSET:
            field_dict["category_uuid"] = category_uuid
        if category_title is not UNSET:
            field_dict["category_title"] = category_title
        if component_type is not UNSET:
            field_dict["component_type"] = component_type
        if component_name is not UNSET:
            field_dict["component_name"] = component_name
        if measured_unit is not UNSET:
            field_dict["measured_unit"] = measured_unit
        if billing_type is not UNSET:
            field_dict["billing_type"] = billing_type
        if limit_amount is not UNSET:
            field_dict["limit_amount"] = limit_amount
        if limit_period is not UNSET:
            field_dict["limit_period"] = limit_period
        if billing_period is not UNSET:
            field_dict["billing_period"] = billing_period
        if total_consumed is not UNSET:
            field_dict["total_consumed"] = total_consumed
        if total_allocated is not UNSET:
            field_dict["total_allocated"] = total_allocated
        if usage_percent is not UNSET:
            field_dict["usage_percent"] = usage_percent

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _offering_uuid = d.pop("offering_uuid", UNSET)
        offering_uuid: Union[Unset, UUID]
        if isinstance(_offering_uuid, Unset):
            offering_uuid = UNSET
        else:
            offering_uuid = UUID(_offering_uuid)

        offering_name = d.pop("offering_name", UNSET)

        offering_type = d.pop("offering_type", UNSET)

        _service_provider_uuid = d.pop("service_provider_uuid", UNSET)
        service_provider_uuid: Union[Unset, UUID]
        if isinstance(_service_provider_uuid, Unset):
            service_provider_uuid = UNSET
        else:
            service_provider_uuid = UUID(_service_provider_uuid)

        service_provider_name = d.pop("service_provider_name", UNSET)

        _category_uuid = d.pop("category_uuid", UNSET)
        category_uuid: Union[Unset, UUID]
        if isinstance(_category_uuid, Unset):
            category_uuid = UNSET
        else:
            category_uuid = UUID(_category_uuid)

        category_title = d.pop("category_title", UNSET)

        component_type = d.pop("component_type", UNSET)

        component_name = d.pop("component_name", UNSET)

        measured_unit = d.pop("measured_unit", UNSET)

        billing_type = d.pop("billing_type", UNSET)

        limit_amount = d.pop("limit_amount", UNSET)

        limit_period = d.pop("limit_period", UNSET)

        _billing_period = d.pop("billing_period", UNSET)
        billing_period: Union[Unset, datetime.date]
        if isinstance(_billing_period, Unset):
            billing_period = UNSET
        else:
            billing_period = isoparse(_billing_period).date()

        total_consumed = d.pop("total_consumed", UNSET)

        total_allocated = d.pop("total_allocated", UNSET)

        def _parse_usage_percent(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        usage_percent = _parse_usage_percent(d.pop("usage_percent", UNSET))

        component_usage_monthly = cls(
            offering_uuid=offering_uuid,
            offering_name=offering_name,
            offering_type=offering_type,
            service_provider_uuid=service_provider_uuid,
            service_provider_name=service_provider_name,
            category_uuid=category_uuid,
            category_title=category_title,
            component_type=component_type,
            component_name=component_name,
            measured_unit=measured_unit,
            billing_type=billing_type,
            limit_amount=limit_amount,
            limit_period=limit_period,
            billing_period=billing_period,
            total_consumed=total_consumed,
            total_allocated=total_allocated,
            usage_percent=usage_percent,
        )

        component_usage_monthly.additional_properties = d
        return component_usage_monthly

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
