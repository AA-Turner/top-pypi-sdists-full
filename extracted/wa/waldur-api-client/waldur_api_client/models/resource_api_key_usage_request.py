import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.component_daily_usage_item_request import ComponentDailyUsageItemRequest
    from ..models.resource_api_key_usage_request_usages import ResourceApiKeyUsageRequestUsages


T = TypeVar("T", bound="ResourceApiKeyUsageRequest")


@_attrs_define
class ResourceApiKeyUsageRequest:
    """
    Attributes:
        usages (Union[Unset, ResourceApiKeyUsageRequestUsages]): The key's usage so far in billing_period, per component
            type. A figure never drops: one lower than the key holds for the month leaves the higher one. Rejected for a
            component that has daily amounts in that month.
        daily_usages (Union[Unset, list['ComponentDailyUsageItemRequest']]): The key's usage per UTC date and component
            type; a date reported again replaces its amount. The month's usage of a component with daily amounts is their
            sum. Needed for limits other than month and total. Days of a month before the one the key holds raise that
            month's figure for a total. At most 1000 items, dated from the start of the current year, or of the previous
            month when that is earlier.
        billing_period (Union[Unset, datetime.date]): Any day of the month usages belongs to; the current month when
            omitted. A later month than the key holds starts afresh. An earlier one, from the start of the current year or
            of the previous month when that is earlier, raises that month's figure for a total limit; older ones are
            refused.
    """

    usages: Union[Unset, "ResourceApiKeyUsageRequestUsages"] = UNSET
    daily_usages: Union[Unset, list["ComponentDailyUsageItemRequest"]] = UNSET
    billing_period: Union[Unset, datetime.date] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        usages: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.usages, Unset):
            usages = self.usages.to_dict()

        daily_usages: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.daily_usages, Unset):
            daily_usages = []
            for daily_usages_item_data in self.daily_usages:
                daily_usages_item = daily_usages_item_data.to_dict()
                daily_usages.append(daily_usages_item)

        billing_period: Union[Unset, str] = UNSET
        if not isinstance(self.billing_period, Unset):
            billing_period = self.billing_period.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if usages is not UNSET:
            field_dict["usages"] = usages
        if daily_usages is not UNSET:
            field_dict["daily_usages"] = daily_usages
        if billing_period is not UNSET:
            field_dict["billing_period"] = billing_period

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.component_daily_usage_item_request import ComponentDailyUsageItemRequest
        from ..models.resource_api_key_usage_request_usages import ResourceApiKeyUsageRequestUsages

        d = dict(src_dict)
        _usages = d.pop("usages", UNSET)
        usages: Union[Unset, ResourceApiKeyUsageRequestUsages]
        if isinstance(_usages, Unset):
            usages = UNSET
        else:
            usages = ResourceApiKeyUsageRequestUsages.from_dict(_usages)

        daily_usages = []
        _daily_usages = d.pop("daily_usages", UNSET)
        for daily_usages_item_data in _daily_usages or []:
            daily_usages_item = ComponentDailyUsageItemRequest.from_dict(daily_usages_item_data)

            daily_usages.append(daily_usages_item)

        _billing_period = d.pop("billing_period", UNSET)
        billing_period: Union[Unset, datetime.date]
        if isinstance(_billing_period, Unset):
            billing_period = UNSET
        else:
            billing_period = isoparse(_billing_period).date()

        resource_api_key_usage_request = cls(
            usages=usages,
            daily_usages=daily_usages,
            billing_period=billing_period,
        )

        resource_api_key_usage_request.additional_properties = d
        return resource_api_key_usage_request

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
