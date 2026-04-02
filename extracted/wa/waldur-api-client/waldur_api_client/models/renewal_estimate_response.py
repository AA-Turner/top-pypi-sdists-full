import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.renewal_estimate_component import RenewalEstimateComponent


T = TypeVar("T", bound="RenewalEstimateResponse")


@_attrs_define
class RenewalEstimateResponse:
    """
    Attributes:
        components (list['RenewalEstimateComponent']):
        subscription_total (str):
        limit_change_total (str):
        total (str):
        remaining_days (int):
        new_end_date (datetime.date):
    """

    components: list["RenewalEstimateComponent"]
    subscription_total: str
    limit_change_total: str
    total: str
    remaining_days: int
    new_end_date: datetime.date
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        components = []
        for components_item_data in self.components:
            components_item = components_item_data.to_dict()
            components.append(components_item)

        subscription_total = self.subscription_total

        limit_change_total = self.limit_change_total

        total = self.total

        remaining_days = self.remaining_days

        new_end_date = self.new_end_date.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "components": components,
                "subscription_total": subscription_total,
                "limit_change_total": limit_change_total,
                "total": total,
                "remaining_days": remaining_days,
                "new_end_date": new_end_date,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.renewal_estimate_component import RenewalEstimateComponent

        d = dict(src_dict)
        components = []
        _components = d.pop("components")
        for components_item_data in _components:
            components_item = RenewalEstimateComponent.from_dict(components_item_data)

            components.append(components_item)

        subscription_total = d.pop("subscription_total")

        limit_change_total = d.pop("limit_change_total")

        total = d.pop("total")

        remaining_days = d.pop("remaining_days")

        new_end_date = isoparse(d.pop("new_end_date")).date()

        renewal_estimate_response = cls(
            components=components,
            subscription_total=subscription_total,
            limit_change_total=limit_change_total,
            total=total,
            remaining_days=remaining_days,
            new_end_date=new_end_date,
        )

        renewal_estimate_response.additional_properties = d
        return renewal_estimate_response

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
