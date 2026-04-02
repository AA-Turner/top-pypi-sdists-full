from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SlurmPolicyPreviewRequestRequest")


@_attrs_define
class SlurmPolicyPreviewRequestRequest:
    """
    Attributes:
        allocation (Union[Unset, float]): Base allocation for the period (in node-hours or billing units) Default:
            1000.0.
        grace_ratio (Union[Unset, float]): Grace ratio for overconsumption allowance (0.2 = 20%) Default: 0.2.
        previous_usage (Union[Unset, float]): Usage from the previous period Default: 0.0.
        carryover_factor (Union[Unset, int]): Maximum percentage of base allocation that can carry over (0-100) Default:
            50.
        carryover_enabled (Union[Unset, bool]): Whether unused allocation carries over to next period Default: True.
        resource_uuid (Union[None, UUID, Unset]): Optional resource UUID to use for current usage data
        current_usage (Union[Unset, float]): Current usage in this period (manual input or from resource) Default: 0.0.
        daily_usage_rate (Union[Unset, float]): Average daily usage rate for projections Default: 0.0.
    """

    allocation: Union[Unset, float] = 1000.0
    grace_ratio: Union[Unset, float] = 0.2
    previous_usage: Union[Unset, float] = 0.0
    carryover_factor: Union[Unset, int] = 50
    carryover_enabled: Union[Unset, bool] = True
    resource_uuid: Union[None, UUID, Unset] = UNSET
    current_usage: Union[Unset, float] = 0.0
    daily_usage_rate: Union[Unset, float] = 0.0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        allocation = self.allocation

        grace_ratio = self.grace_ratio

        previous_usage = self.previous_usage

        carryover_factor = self.carryover_factor

        carryover_enabled = self.carryover_enabled

        resource_uuid: Union[None, Unset, str]
        if isinstance(self.resource_uuid, Unset):
            resource_uuid = UNSET
        elif isinstance(self.resource_uuid, UUID):
            resource_uuid = str(self.resource_uuid)
        else:
            resource_uuid = self.resource_uuid

        current_usage = self.current_usage

        daily_usage_rate = self.daily_usage_rate

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if allocation is not UNSET:
            field_dict["allocation"] = allocation
        if grace_ratio is not UNSET:
            field_dict["grace_ratio"] = grace_ratio
        if previous_usage is not UNSET:
            field_dict["previous_usage"] = previous_usage
        if carryover_factor is not UNSET:
            field_dict["carryover_factor"] = carryover_factor
        if carryover_enabled is not UNSET:
            field_dict["carryover_enabled"] = carryover_enabled
        if resource_uuid is not UNSET:
            field_dict["resource_uuid"] = resource_uuid
        if current_usage is not UNSET:
            field_dict["current_usage"] = current_usage
        if daily_usage_rate is not UNSET:
            field_dict["daily_usage_rate"] = daily_usage_rate

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        allocation = d.pop("allocation", UNSET)

        grace_ratio = d.pop("grace_ratio", UNSET)

        previous_usage = d.pop("previous_usage", UNSET)

        carryover_factor = d.pop("carryover_factor", UNSET)

        carryover_enabled = d.pop("carryover_enabled", UNSET)

        def _parse_resource_uuid(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                resource_uuid_type_0 = UUID(data)

                return resource_uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        resource_uuid = _parse_resource_uuid(d.pop("resource_uuid", UNSET))

        current_usage = d.pop("current_usage", UNSET)

        daily_usage_rate = d.pop("daily_usage_rate", UNSET)

        slurm_policy_preview_request_request = cls(
            allocation=allocation,
            grace_ratio=grace_ratio,
            previous_usage=previous_usage,
            carryover_factor=carryover_factor,
            carryover_enabled=carryover_enabled,
            resource_uuid=resource_uuid,
            current_usage=current_usage,
            daily_usage_rate=daily_usage_rate,
        )

        slurm_policy_preview_request_request.additional_properties = d
        return slurm_policy_preview_request_request

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
