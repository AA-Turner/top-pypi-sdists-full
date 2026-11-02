from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.list_extended_jobs_response_200_jobs_item_type_1_flow_status_failure_module_agent_actions_item_type_1_type import (
    ListExtendedJobsResponse200JobsItemType1FlowStatusFailureModuleAgentActionsItemType1Type,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.list_extended_jobs_response_200_jobs_item_type_1_flow_status_failure_module_agent_actions_item_type_1_arguments import (
        ListExtendedJobsResponse200JobsItemType1FlowStatusFailureModuleAgentActionsItemType1Arguments,
    )


T = TypeVar("T", bound="ListExtendedJobsResponse200JobsItemType1FlowStatusFailureModuleAgentActionsItemType1")


@_attrs_define
class ListExtendedJobsResponse200JobsItemType1FlowStatusFailureModuleAgentActionsItemType1:
    """
    Attributes:
        call_id (str):
        function_name (str):
        resource_path (str):
        type (ListExtendedJobsResponse200JobsItemType1FlowStatusFailureModuleAgentActionsItemType1Type):
        arguments (Union[Unset,
            ListExtendedJobsResponse200JobsItemType1FlowStatusFailureModuleAgentActionsItemType1Arguments]):
    """

    call_id: str
    function_name: str
    resource_path: str
    type: ListExtendedJobsResponse200JobsItemType1FlowStatusFailureModuleAgentActionsItemType1Type
    arguments: Union[
        Unset, "ListExtendedJobsResponse200JobsItemType1FlowStatusFailureModuleAgentActionsItemType1Arguments"
    ] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        call_id = self.call_id
        function_name = self.function_name
        resource_path = self.resource_path
        type = self.type.value

        arguments: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.arguments, Unset):
            arguments = self.arguments.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "call_id": call_id,
                "function_name": function_name,
                "resource_path": resource_path,
                "type": type,
            }
        )
        if arguments is not UNSET:
            field_dict["arguments"] = arguments

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_extended_jobs_response_200_jobs_item_type_1_flow_status_failure_module_agent_actions_item_type_1_arguments import (
            ListExtendedJobsResponse200JobsItemType1FlowStatusFailureModuleAgentActionsItemType1Arguments,
        )

        d = src_dict.copy()
        call_id = d.pop("call_id")

        function_name = d.pop("function_name")

        resource_path = d.pop("resource_path")

        type = ListExtendedJobsResponse200JobsItemType1FlowStatusFailureModuleAgentActionsItemType1Type(d.pop("type"))

        _arguments = d.pop("arguments", UNSET)
        arguments: Union[
            Unset, ListExtendedJobsResponse200JobsItemType1FlowStatusFailureModuleAgentActionsItemType1Arguments
        ]
        if isinstance(_arguments, Unset):
            arguments = UNSET
        else:
            arguments = (
                ListExtendedJobsResponse200JobsItemType1FlowStatusFailureModuleAgentActionsItemType1Arguments.from_dict(
                    _arguments
                )
            )

        list_extended_jobs_response_200_jobs_item_type_1_flow_status_failure_module_agent_actions_item_type_1 = cls(
            call_id=call_id,
            function_name=function_name,
            resource_path=resource_path,
            type=type,
            arguments=arguments,
        )

        list_extended_jobs_response_200_jobs_item_type_1_flow_status_failure_module_agent_actions_item_type_1.additional_properties = (
            d
        )
        return list_extended_jobs_response_200_jobs_item_type_1_flow_status_failure_module_agent_actions_item_type_1

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
