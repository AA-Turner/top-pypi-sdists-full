from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.slurm_policy_dry_run_resource import SlurmPolicyDryRunResource


T = TypeVar("T", bound="SlurmPolicyDryRunResponse")


@_attrs_define
class SlurmPolicyDryRunResponse:
    """
    Attributes:
        policy_uuid (UUID):
        billing_period (str):
        grace_limit_percentage (float):
        resources (list['SlurmPolicyDryRunResource']):
    """

    policy_uuid: UUID
    billing_period: str
    grace_limit_percentage: float
    resources: list["SlurmPolicyDryRunResource"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        policy_uuid = str(self.policy_uuid)

        billing_period = self.billing_period

        grace_limit_percentage = self.grace_limit_percentage

        resources = []
        for resources_item_data in self.resources:
            resources_item = resources_item_data.to_dict()
            resources.append(resources_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "policy_uuid": policy_uuid,
                "billing_period": billing_period,
                "grace_limit_percentage": grace_limit_percentage,
                "resources": resources,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.slurm_policy_dry_run_resource import SlurmPolicyDryRunResource

        d = dict(src_dict)
        policy_uuid = UUID(d.pop("policy_uuid"))

        billing_period = d.pop("billing_period")

        grace_limit_percentage = d.pop("grace_limit_percentage")

        resources = []
        _resources = d.pop("resources")
        for resources_item_data in _resources:
            resources_item = SlurmPolicyDryRunResource.from_dict(resources_item_data)

            resources.append(resources_item)

        slurm_policy_dry_run_response = cls(
            policy_uuid=policy_uuid,
            billing_period=billing_period,
            grace_limit_percentage=grace_limit_percentage,
            resources=resources,
        )

        slurm_policy_dry_run_response.additional_properties = d
        return slurm_policy_dry_run_response

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
