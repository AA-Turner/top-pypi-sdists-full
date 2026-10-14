import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.resource_api_key_usage_request_usages import ResourceApiKeyUsageRequestUsages


T = TypeVar("T", bound="ResourceApiKeyUsageRequest")


@_attrs_define
class ResourceApiKeyUsageRequest:
    """
    Attributes:
        usages (ResourceApiKeyUsageRequestUsages): The key's usage so far in billing_period, per component type.
        billing_period (Union[Unset, datetime.date]): Any day of the month the usage belongs to; the current month when
            omitted. Limits are monthly, so a later month starts them afresh.
    """

    usages: "ResourceApiKeyUsageRequestUsages"
    billing_period: Union[Unset, datetime.date] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        usages = self.usages.to_dict()

        billing_period: Union[Unset, str] = UNSET
        if not isinstance(self.billing_period, Unset):
            billing_period = self.billing_period.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "usages": usages,
            }
        )
        if billing_period is not UNSET:
            field_dict["billing_period"] = billing_period

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.resource_api_key_usage_request_usages import ResourceApiKeyUsageRequestUsages

        d = dict(src_dict)
        usages = ResourceApiKeyUsageRequestUsages.from_dict(d.pop("usages"))

        _billing_period = d.pop("billing_period", UNSET)
        billing_period: Union[Unset, datetime.date]
        if isinstance(_billing_period, Unset):
            billing_period = UNSET
        else:
            billing_period = isoparse(_billing_period).date()

        resource_api_key_usage_request = cls(
            usages=usages,
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
