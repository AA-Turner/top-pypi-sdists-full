from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ServiceProviderStatistics")


@_attrs_define
class ServiceProviderStatistics:
    """
    Attributes:
        active_campaigns (int): Number of active campaigns
        current_customers (int): Number of current customers
        customers_number_change (int): Change in number of customers
        active_resources (int): Number of active resources
        resources_number_change (int): Change in number of resources
        active_and_paused_offerings (int): Number of active and paused offerings
        unresolved_tickets (int): Number of unresolved support tickets
        pending_orders (int): Number of pending orders
        erred_resources (int): Number of resources in error state
    """

    active_campaigns: int
    current_customers: int
    customers_number_change: int
    active_resources: int
    resources_number_change: int
    active_and_paused_offerings: int
    unresolved_tickets: int
    pending_orders: int
    erred_resources: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        active_campaigns = self.active_campaigns

        current_customers = self.current_customers

        customers_number_change = self.customers_number_change

        active_resources = self.active_resources

        resources_number_change = self.resources_number_change

        active_and_paused_offerings = self.active_and_paused_offerings

        unresolved_tickets = self.unresolved_tickets

        pending_orders = self.pending_orders

        erred_resources = self.erred_resources

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "active_campaigns": active_campaigns,
                "current_customers": current_customers,
                "customers_number_change": customers_number_change,
                "active_resources": active_resources,
                "resources_number_change": resources_number_change,
                "active_and_paused_offerings": active_and_paused_offerings,
                "unresolved_tickets": unresolved_tickets,
                "pending_orders": pending_orders,
                "erred_resources": erred_resources,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        active_campaigns = d.pop("active_campaigns")

        current_customers = d.pop("current_customers")

        customers_number_change = d.pop("customers_number_change")

        active_resources = d.pop("active_resources")

        resources_number_change = d.pop("resources_number_change")

        active_and_paused_offerings = d.pop("active_and_paused_offerings")

        unresolved_tickets = d.pop("unresolved_tickets")

        pending_orders = d.pop("pending_orders")

        erred_resources = d.pop("erred_resources")

        service_provider_statistics = cls(
            active_campaigns=active_campaigns,
            current_customers=current_customers,
            customers_number_change=customers_number_change,
            active_resources=active_resources,
            resources_number_change=resources_number_change,
            active_and_paused_offerings=active_and_paused_offerings,
            unresolved_tickets=unresolved_tickets,
            pending_orders=pending_orders,
            erred_resources=erred_resources,
        )

        service_provider_statistics.additional_properties = d
        return service_provider_statistics

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
