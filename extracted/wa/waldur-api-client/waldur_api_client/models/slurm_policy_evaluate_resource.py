from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.slurm_policy_evaluate_resource_new_state import SlurmPolicyEvaluateResourceNewState
    from ..models.slurm_policy_evaluate_resource_previous_state import SlurmPolicyEvaluateResourcePreviousState


T = TypeVar("T", bound="SlurmPolicyEvaluateResource")


@_attrs_define
class SlurmPolicyEvaluateResource:
    """
    Attributes:
        resource_uuid (UUID):
        resource_name (str):
        usage_percentage (float):
        actions_taken (list[str]):
        previous_state (SlurmPolicyEvaluateResourcePreviousState):
        new_state (SlurmPolicyEvaluateResourceNewState):
    """

    resource_uuid: UUID
    resource_name: str
    usage_percentage: float
    actions_taken: list[str]
    previous_state: "SlurmPolicyEvaluateResourcePreviousState"
    new_state: "SlurmPolicyEvaluateResourceNewState"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        resource_uuid = str(self.resource_uuid)

        resource_name = self.resource_name

        usage_percentage = self.usage_percentage

        actions_taken = self.actions_taken

        previous_state = self.previous_state.to_dict()

        new_state = self.new_state.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "resource_uuid": resource_uuid,
                "resource_name": resource_name,
                "usage_percentage": usage_percentage,
                "actions_taken": actions_taken,
                "previous_state": previous_state,
                "new_state": new_state,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.slurm_policy_evaluate_resource_new_state import SlurmPolicyEvaluateResourceNewState
        from ..models.slurm_policy_evaluate_resource_previous_state import SlurmPolicyEvaluateResourcePreviousState

        d = dict(src_dict)
        resource_uuid = UUID(d.pop("resource_uuid"))

        resource_name = d.pop("resource_name")

        usage_percentage = d.pop("usage_percentage")

        actions_taken = cast(list[str], d.pop("actions_taken"))

        previous_state = SlurmPolicyEvaluateResourcePreviousState.from_dict(d.pop("previous_state"))

        new_state = SlurmPolicyEvaluateResourceNewState.from_dict(d.pop("new_state"))

        slurm_policy_evaluate_resource = cls(
            resource_uuid=resource_uuid,
            resource_name=resource_name,
            usage_percentage=usage_percentage,
            actions_taken=actions_taken,
            previous_state=previous_state,
            new_state=new_state,
        )

        slurm_policy_evaluate_resource.additional_properties = d
        return slurm_policy_evaluate_resource

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
