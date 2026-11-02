from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.flow_status_modules_item_agent_actions_item_type_0_type import (
    FlowStatusModulesItemAgentActionsItemType0Type,
)

T = TypeVar("T", bound="FlowStatusModulesItemAgentActionsItemType0")


@_attrs_define
class FlowStatusModulesItemAgentActionsItemType0:
    """
    Attributes:
        job_id (str):
        function_name (str):
        type (FlowStatusModulesItemAgentActionsItemType0Type):
        module_id (str):
    """

    job_id: str
    function_name: str
    type: FlowStatusModulesItemAgentActionsItemType0Type
    module_id: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        job_id = self.job_id
        function_name = self.function_name
        type = self.type.value

        module_id = self.module_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "job_id": job_id,
                "function_name": function_name,
                "type": type,
                "module_id": module_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        job_id = d.pop("job_id")

        function_name = d.pop("function_name")

        type = FlowStatusModulesItemAgentActionsItemType0Type(d.pop("type"))

        module_id = d.pop("module_id")

        flow_status_modules_item_agent_actions_item_type_0 = cls(
            job_id=job_id,
            function_name=function_name,
            type=type,
            module_id=module_id,
        )

        flow_status_modules_item_agent_actions_item_type_0.additional_properties = d
        return flow_status_modules_item_agent_actions_item_type_0

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
