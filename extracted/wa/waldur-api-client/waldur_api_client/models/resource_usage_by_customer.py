from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.resource_usage_by_customer_limits import ResourceUsageByCustomerLimits
    from ..models.resource_usage_by_customer_usages import ResourceUsageByCustomerUsages


T = TypeVar("T", bound="ResourceUsageByCustomer")


@_attrs_define
class ResourceUsageByCustomer:
    """
    Attributes:
        customer_uuid (UUID): UUID of the customer
        customer_name (str): Name of the customer
        customer_abbreviation (Union[None, str]): Abbreviation of the customer
        resources_ok (int): Number of OK resources
        resources_erred (int): Number of erred resources
        resources_total (int): Total number of active resources
        total_cost (str): Total cost of resources
        usages (ResourceUsageByCustomerUsages): Component usages keyed by component type
        limits (ResourceUsageByCustomerLimits): Resource limits keyed by limit name
    """

    customer_uuid: UUID
    customer_name: str
    customer_abbreviation: Union[None, str]
    resources_ok: int
    resources_erred: int
    resources_total: int
    total_cost: str
    usages: "ResourceUsageByCustomerUsages"
    limits: "ResourceUsageByCustomerLimits"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        customer_uuid = str(self.customer_uuid)

        customer_name = self.customer_name

        customer_abbreviation: Union[None, str]
        customer_abbreviation = self.customer_abbreviation

        resources_ok = self.resources_ok

        resources_erred = self.resources_erred

        resources_total = self.resources_total

        total_cost = self.total_cost

        usages = self.usages.to_dict()

        limits = self.limits.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "customer_uuid": customer_uuid,
                "customer_name": customer_name,
                "customer_abbreviation": customer_abbreviation,
                "resources_ok": resources_ok,
                "resources_erred": resources_erred,
                "resources_total": resources_total,
                "total_cost": total_cost,
                "usages": usages,
                "limits": limits,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.resource_usage_by_customer_limits import ResourceUsageByCustomerLimits
        from ..models.resource_usage_by_customer_usages import ResourceUsageByCustomerUsages

        d = dict(src_dict)
        customer_uuid = UUID(d.pop("customer_uuid"))

        customer_name = d.pop("customer_name")

        def _parse_customer_abbreviation(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        customer_abbreviation = _parse_customer_abbreviation(d.pop("customer_abbreviation"))

        resources_ok = d.pop("resources_ok")

        resources_erred = d.pop("resources_erred")

        resources_total = d.pop("resources_total")

        total_cost = d.pop("total_cost")

        usages = ResourceUsageByCustomerUsages.from_dict(d.pop("usages"))

        limits = ResourceUsageByCustomerLimits.from_dict(d.pop("limits"))

        resource_usage_by_customer = cls(
            customer_uuid=customer_uuid,
            customer_name=customer_name,
            customer_abbreviation=customer_abbreviation,
            resources_ok=resources_ok,
            resources_erred=resources_erred,
            resources_total=resources_total,
            total_cost=total_cost,
            usages=usages,
            limits=limits,
        )

        resource_usage_by_customer.additional_properties = d
        return resource_usage_by_customer

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
