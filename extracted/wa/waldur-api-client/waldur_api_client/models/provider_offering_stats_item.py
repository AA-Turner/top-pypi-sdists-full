from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.provider_offering_plan_stats import ProviderOfferingPlanStats


T = TypeVar("T", bound="ProviderOfferingStatsItem")


@_attrs_define
class ProviderOfferingStatsItem:
    """
    Attributes:
        offering_uuid (UUID):
        offering_name (str):
        category_name (str):
        state (str):
        active_resources (int):
        total_resources (int):
        revenue (Union[None, str]):
        plans (list['ProviderOfferingPlanStats']):
    """

    offering_uuid: UUID
    offering_name: str
    category_name: str
    state: str
    active_resources: int
    total_resources: int
    revenue: Union[None, str]
    plans: list["ProviderOfferingPlanStats"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        offering_uuid = str(self.offering_uuid)

        offering_name = self.offering_name

        category_name = self.category_name

        state = self.state

        active_resources = self.active_resources

        total_resources = self.total_resources

        revenue: Union[None, str]
        revenue = self.revenue

        plans = []
        for plans_item_data in self.plans:
            plans_item = plans_item_data.to_dict()
            plans.append(plans_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "offering_uuid": offering_uuid,
                "offering_name": offering_name,
                "category_name": category_name,
                "state": state,
                "active_resources": active_resources,
                "total_resources": total_resources,
                "revenue": revenue,
                "plans": plans,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.provider_offering_plan_stats import ProviderOfferingPlanStats

        d = dict(src_dict)
        offering_uuid = UUID(d.pop("offering_uuid"))

        offering_name = d.pop("offering_name")

        category_name = d.pop("category_name")

        state = d.pop("state")

        active_resources = d.pop("active_resources")

        total_resources = d.pop("total_resources")

        def _parse_revenue(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        revenue = _parse_revenue(d.pop("revenue"))

        plans = []
        _plans = d.pop("plans")
        for plans_item_data in _plans:
            plans_item = ProviderOfferingPlanStats.from_dict(plans_item_data)

            plans.append(plans_item)

        provider_offering_stats_item = cls(
            offering_uuid=offering_uuid,
            offering_name=offering_name,
            category_name=category_name,
            state=state,
            active_resources=active_resources,
            total_resources=total_resources,
            revenue=revenue,
            plans=plans,
        )

        provider_offering_stats_item.additional_properties = d
        return provider_offering_stats_item

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
