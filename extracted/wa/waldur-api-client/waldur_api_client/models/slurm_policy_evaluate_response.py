from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.slurm_policy_evaluate_resource import SlurmPolicyEvaluateResource


T = TypeVar("T", bound="SlurmPolicyEvaluateResponse")


@_attrs_define
class SlurmPolicyEvaluateResponse:
    """
    Attributes:
        policy_uuid (UUID):
        billing_period (str):
        resources (list['SlurmPolicyEvaluateResource']):
    """

    policy_uuid: UUID
    billing_period: str
    resources: list["SlurmPolicyEvaluateResource"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        policy_uuid = str(self.policy_uuid)

        billing_period = self.billing_period

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
                "resources": resources,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.slurm_policy_evaluate_resource import SlurmPolicyEvaluateResource

        d = dict(src_dict)
        policy_uuid = UUID(d.pop("policy_uuid"))

        billing_period = d.pop("billing_period")

        resources = []
        _resources = d.pop("resources")
        for resources_item_data in _resources:
            resources_item = SlurmPolicyEvaluateResource.from_dict(resources_item_data)

            resources.append(resources_item)

        slurm_policy_evaluate_response = cls(
            policy_uuid=policy_uuid,
            billing_period=billing_period,
            resources=resources,
        )

        slurm_policy_evaluate_response.additional_properties = d
        return slurm_policy_evaluate_response

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
