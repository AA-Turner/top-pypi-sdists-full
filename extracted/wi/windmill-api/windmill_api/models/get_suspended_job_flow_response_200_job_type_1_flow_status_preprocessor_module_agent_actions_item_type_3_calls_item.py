from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar(
    "T", bound="GetSuspendedJobFlowResponse200JobType1FlowStatusPreprocessorModuleAgentActionsItemType3CallsItem"
)


@_attrs_define
class GetSuspendedJobFlowResponse200JobType1FlowStatusPreprocessorModuleAgentActionsItemType3CallsItem:
    """
    Attributes:
        function_name (str):
        arguments (Any):
    """

    function_name: str
    arguments: Any
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        function_name = self.function_name
        arguments = self.arguments

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "function_name": function_name,
                "arguments": arguments,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        function_name = d.pop("function_name")

        arguments = d.pop("arguments")

        get_suspended_job_flow_response_200_job_type_1_flow_status_preprocessor_module_agent_actions_item_type_3_calls_item = cls(
            function_name=function_name,
            arguments=arguments,
        )

        get_suspended_job_flow_response_200_job_type_1_flow_status_preprocessor_module_agent_actions_item_type_3_calls_item.additional_properties = (
            d
        )
        return get_suspended_job_flow_response_200_job_type_1_flow_status_preprocessor_module_agent_actions_item_type_3_calls_item

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
