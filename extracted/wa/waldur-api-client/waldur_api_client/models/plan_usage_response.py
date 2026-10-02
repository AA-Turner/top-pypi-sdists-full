from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="PlanUsageResponse")


@_attrs_define
class PlanUsageResponse:
    """
    Attributes:
        plan_uuid (UUID): UUID of the plan
        plan_name (str): Name of the plan
        limit (int): Usage limit
        usage (int): Current usage count
        remaining (int): Remaining usage
        offering_uuid (UUID):
        offering_name (str):
        customer_provider_uuid (UUID):
        customer_provider_name (str):
    """

    plan_uuid: UUID
    plan_name: str
    limit: int
    usage: int
    remaining: int
    offering_uuid: UUID
    offering_name: str
    customer_provider_uuid: UUID
    customer_provider_name: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        plan_uuid = str(self.plan_uuid)

        plan_name = self.plan_name

        limit = self.limit

        usage = self.usage

        remaining = self.remaining

        offering_uuid = str(self.offering_uuid)

        offering_name = self.offering_name

        customer_provider_uuid = str(self.customer_provider_uuid)

        customer_provider_name = self.customer_provider_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "plan_uuid": plan_uuid,
                "plan_name": plan_name,
                "limit": limit,
                "usage": usage,
                "remaining": remaining,
                "offering_uuid": offering_uuid,
                "offering_name": offering_name,
                "customer_provider_uuid": customer_provider_uuid,
                "customer_provider_name": customer_provider_name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        plan_uuid = UUID(d.pop("plan_uuid"))

        plan_name = d.pop("plan_name")

        limit = d.pop("limit")

        usage = d.pop("usage")

        remaining = d.pop("remaining")

        offering_uuid = UUID(d.pop("offering_uuid"))

        offering_name = d.pop("offering_name")

        customer_provider_uuid = UUID(d.pop("customer_provider_uuid"))

        customer_provider_name = d.pop("customer_provider_name")

        plan_usage_response = cls(
            plan_uuid=plan_uuid,
            plan_name=plan_name,
            limit=limit,
            usage=usage,
            remaining=remaining,
            offering_uuid=offering_uuid,
            offering_name=offering_name,
            customer_provider_uuid=customer_provider_uuid,
            customer_provider_name=customer_provider_name,
        )

        plan_usage_response.additional_properties = d
        return plan_usage_response

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
