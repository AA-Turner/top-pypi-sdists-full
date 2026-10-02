from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SlurmPolicyDryRunResource")


@_attrs_define
class SlurmPolicyDryRunResource:
    """
    Attributes:
        resource_uuid (UUID):
        resource_name (str):
        usage_percentage (float):
        paused (bool):
        downscaled (bool):
        would_trigger (list[str]):
    """

    resource_uuid: UUID
    resource_name: str
    usage_percentage: float
    paused: bool
    downscaled: bool
    would_trigger: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        resource_uuid = str(self.resource_uuid)

        resource_name = self.resource_name

        usage_percentage = self.usage_percentage

        paused = self.paused

        downscaled = self.downscaled

        would_trigger = self.would_trigger

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "resource_uuid": resource_uuid,
                "resource_name": resource_name,
                "usage_percentage": usage_percentage,
                "paused": paused,
                "downscaled": downscaled,
                "would_trigger": would_trigger,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        resource_uuid = UUID(d.pop("resource_uuid"))

        resource_name = d.pop("resource_name")

        usage_percentage = d.pop("usage_percentage")

        paused = d.pop("paused")

        downscaled = d.pop("downscaled")

        would_trigger = cast(list[str], d.pop("would_trigger"))

        slurm_policy_dry_run_resource = cls(
            resource_uuid=resource_uuid,
            resource_name=resource_name,
            usage_percentage=usage_percentage,
            paused=paused,
            downscaled=downscaled,
            would_trigger=would_trigger,
        )

        slurm_policy_dry_run_resource.additional_properties = d
        return slurm_policy_dry_run_resource

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
