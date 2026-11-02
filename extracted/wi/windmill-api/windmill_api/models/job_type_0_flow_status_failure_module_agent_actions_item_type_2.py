from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.job_type_0_flow_status_failure_module_agent_actions_item_type_2_type import (
    JobType0FlowStatusFailureModuleAgentActionsItemType2Type,
)

T = TypeVar("T", bound="JobType0FlowStatusFailureModuleAgentActionsItemType2")


@_attrs_define
class JobType0FlowStatusFailureModuleAgentActionsItemType2:
    """
    Attributes:
        type (JobType0FlowStatusFailureModuleAgentActionsItemType2Type):
    """

    type: JobType0FlowStatusFailureModuleAgentActionsItemType2Type
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = JobType0FlowStatusFailureModuleAgentActionsItemType2Type(d.pop("type"))

        job_type_0_flow_status_failure_module_agent_actions_item_type_2 = cls(
            type=type,
        )

        job_type_0_flow_status_failure_module_agent_actions_item_type_2.additional_properties = d
        return job_type_0_flow_status_failure_module_agent_actions_item_type_2

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
