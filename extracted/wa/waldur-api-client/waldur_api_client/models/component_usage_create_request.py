import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.component_usage_item_request import ComponentUsageItemRequest


T = TypeVar("T", bound="ComponentUsageCreateRequest")


@_attrs_define
class ComponentUsageCreateRequest:
    """
    Attributes:
        usages (list['ComponentUsageItemRequest']): List of component usage items to report
        plan_period (Union[Unset, UUID]): UUID of the specific resource plan period for usage reporting
        resource (Union[Unset, UUID]): UUID of the resource for usage reporting (required if plan_period not provided)
        date (Union[Unset, datetime.datetime]): Date for usage reporting (staff and service providers for limit-based
            components). If not provided, current date is used.
    """

    usages: list["ComponentUsageItemRequest"]
    plan_period: Union[Unset, UUID] = UNSET
    resource: Union[Unset, UUID] = UNSET
    date: Union[Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        usages = []
        for usages_item_data in self.usages:
            usages_item = usages_item_data.to_dict()
            usages.append(usages_item)

        plan_period: Union[Unset, str] = UNSET
        if not isinstance(self.plan_period, Unset):
            plan_period = str(self.plan_period)

        resource: Union[Unset, str] = UNSET
        if not isinstance(self.resource, Unset):
            resource = str(self.resource)

        date: Union[Unset, str] = UNSET
        if not isinstance(self.date, Unset):
            date = self.date.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "usages": usages,
            }
        )
        if plan_period is not UNSET:
            field_dict["plan_period"] = plan_period
        if resource is not UNSET:
            field_dict["resource"] = resource
        if date is not UNSET:
            field_dict["date"] = date

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.component_usage_item_request import ComponentUsageItemRequest

        d = dict(src_dict)
        usages = []
        _usages = d.pop("usages")
        for usages_item_data in _usages:
            usages_item = ComponentUsageItemRequest.from_dict(usages_item_data)

            usages.append(usages_item)

        _plan_period = d.pop("plan_period", UNSET)
        plan_period: Union[Unset, UUID]
        if isinstance(_plan_period, Unset):
            plan_period = UNSET
        else:
            plan_period = UUID(_plan_period)

        _resource = d.pop("resource", UNSET)
        resource: Union[Unset, UUID]
        if isinstance(_resource, Unset):
            resource = UNSET
        else:
            resource = UUID(_resource)

        _date = d.pop("date", UNSET)
        date: Union[Unset, datetime.datetime]
        if isinstance(_date, Unset):
            date = UNSET
        else:
            date = isoparse(_date)

        component_usage_create_request = cls(
            usages=usages,
            plan_period=plan_period,
            resource=resource,
            date=date,
        )

        component_usage_create_request.additional_properties = d
        return component_usage_create_request

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
