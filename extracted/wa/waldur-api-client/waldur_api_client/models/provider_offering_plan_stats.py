from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ProviderOfferingPlanStats")


@_attrs_define
class ProviderOfferingPlanStats:
    """
    Attributes:
        plan_uuid (UUID):
        plan_name (str):
        usage (int):
        limit (Union[None, int]):
        utilization (Union[None, float]):
    """

    plan_uuid: UUID
    plan_name: str
    usage: int
    limit: Union[None, int]
    utilization: Union[None, float]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        plan_uuid = str(self.plan_uuid)

        plan_name = self.plan_name

        usage = self.usage

        limit: Union[None, int]
        limit = self.limit

        utilization: Union[None, float]
        utilization = self.utilization

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "plan_uuid": plan_uuid,
                "plan_name": plan_name,
                "usage": usage,
                "limit": limit,
                "utilization": utilization,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        plan_uuid = UUID(d.pop("plan_uuid"))

        plan_name = d.pop("plan_name")

        usage = d.pop("usage")

        def _parse_limit(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        limit = _parse_limit(d.pop("limit"))

        def _parse_utilization(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        utilization = _parse_utilization(d.pop("utilization"))

        provider_offering_plan_stats = cls(
            plan_uuid=plan_uuid,
            plan_name=plan_name,
            usage=usage,
            limit=limit,
            utilization=utilization,
        )

        provider_offering_plan_stats.additional_properties = d
        return provider_offering_plan_stats

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
