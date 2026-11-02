import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.list_queue_response_200_item_flow_status_preprocessor_module_agent_actions_item_type_4_type import (
    ListQueueResponse200ItemFlowStatusPreprocessorModuleAgentActionsItemType4Type,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="ListQueueResponse200ItemFlowStatusPreprocessorModuleAgentActionsItemType4")


@_attrs_define
class ListQueueResponse200ItemFlowStatusPreprocessorModuleAgentActionsItemType4:
    """
    Attributes:
        type (ListQueueResponse200ItemFlowStatusPreprocessorModuleAgentActionsItemType4Type):
        call_id (str):
        question (str):
        expires_at (datetime.datetime):
        choices (Union[Unset, List[str]]): answers the model proposes; a free-text answer is always possible
        multi_select (Union[Unset, bool]): whether several choices can be picked together
    """

    type: ListQueueResponse200ItemFlowStatusPreprocessorModuleAgentActionsItemType4Type
    call_id: str
    question: str
    expires_at: datetime.datetime
    choices: Union[Unset, List[str]] = UNSET
    multi_select: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        call_id = self.call_id
        question = self.question
        expires_at = self.expires_at.isoformat()

        choices: Union[Unset, List[str]] = UNSET
        if not isinstance(self.choices, Unset):
            choices = self.choices

        multi_select = self.multi_select

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "call_id": call_id,
                "question": question,
                "expires_at": expires_at,
            }
        )
        if choices is not UNSET:
            field_dict["choices"] = choices
        if multi_select is not UNSET:
            field_dict["multi_select"] = multi_select

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = ListQueueResponse200ItemFlowStatusPreprocessorModuleAgentActionsItemType4Type(d.pop("type"))

        call_id = d.pop("call_id")

        question = d.pop("question")

        expires_at = isoparse(d.pop("expires_at"))

        choices = cast(List[str], d.pop("choices", UNSET))

        multi_select = d.pop("multi_select", UNSET)

        list_queue_response_200_item_flow_status_preprocessor_module_agent_actions_item_type_4 = cls(
            type=type,
            call_id=call_id,
            question=question,
            expires_at=expires_at,
            choices=choices,
            multi_select=multi_select,
        )

        list_queue_response_200_item_flow_status_preprocessor_module_agent_actions_item_type_4.additional_properties = d
        return list_queue_response_200_item_flow_status_preprocessor_module_agent_actions_item_type_4

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
