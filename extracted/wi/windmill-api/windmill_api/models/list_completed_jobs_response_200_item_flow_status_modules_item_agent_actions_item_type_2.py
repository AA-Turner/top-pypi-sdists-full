from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.list_completed_jobs_response_200_item_flow_status_modules_item_agent_actions_item_type_2_type import (
    ListCompletedJobsResponse200ItemFlowStatusModulesItemAgentActionsItemType2Type,
)

T = TypeVar("T", bound="ListCompletedJobsResponse200ItemFlowStatusModulesItemAgentActionsItemType2")


@_attrs_define
class ListCompletedJobsResponse200ItemFlowStatusModulesItemAgentActionsItemType2:
    """
    Attributes:
        type (ListCompletedJobsResponse200ItemFlowStatusModulesItemAgentActionsItemType2Type):
    """

    type: ListCompletedJobsResponse200ItemFlowStatusModulesItemAgentActionsItemType2Type
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
        type = ListCompletedJobsResponse200ItemFlowStatusModulesItemAgentActionsItemType2Type(d.pop("type"))

        list_completed_jobs_response_200_item_flow_status_modules_item_agent_actions_item_type_2 = cls(
            type=type,
        )

        list_completed_jobs_response_200_item_flow_status_modules_item_agent_actions_item_type_2.additional_properties = (
            d
        )
        return list_completed_jobs_response_200_item_flow_status_modules_item_agent_actions_item_type_2

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
