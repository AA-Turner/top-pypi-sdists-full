import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.queued_job_flow_status_preprocessor_module_agent_actions_item_type_3_type import (
    QueuedJobFlowStatusPreprocessorModuleAgentActionsItemType3Type,
)

if TYPE_CHECKING:
    from ..models.queued_job_flow_status_preprocessor_module_agent_actions_item_type_3_calls_item import (
        QueuedJobFlowStatusPreprocessorModuleAgentActionsItemType3CallsItem,
    )


T = TypeVar("T", bound="QueuedJobFlowStatusPreprocessorModuleAgentActionsItemType3")


@_attrs_define
class QueuedJobFlowStatusPreprocessorModuleAgentActionsItemType3:
    """
    Attributes:
        type (QueuedJobFlowStatusPreprocessorModuleAgentActionsItemType3Type):
        call_id (str):
        calls (List['QueuedJobFlowStatusPreprocessorModuleAgentActionsItemType3CallsItem']):
        expires_at (datetime.datetime):
    """

    type: QueuedJobFlowStatusPreprocessorModuleAgentActionsItemType3Type
    call_id: str
    calls: List["QueuedJobFlowStatusPreprocessorModuleAgentActionsItemType3CallsItem"]
    expires_at: datetime.datetime
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        call_id = self.call_id
        calls = []
        for calls_item_data in self.calls:
            calls_item = calls_item_data.to_dict()

            calls.append(calls_item)

        expires_at = self.expires_at.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "call_id": call_id,
                "calls": calls,
                "expires_at": expires_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.queued_job_flow_status_preprocessor_module_agent_actions_item_type_3_calls_item import (
            QueuedJobFlowStatusPreprocessorModuleAgentActionsItemType3CallsItem,
        )

        d = src_dict.copy()
        type = QueuedJobFlowStatusPreprocessorModuleAgentActionsItemType3Type(d.pop("type"))

        call_id = d.pop("call_id")

        calls = []
        _calls = d.pop("calls")
        for calls_item_data in _calls:
            calls_item = QueuedJobFlowStatusPreprocessorModuleAgentActionsItemType3CallsItem.from_dict(calls_item_data)

            calls.append(calls_item)

        expires_at = isoparse(d.pop("expires_at"))

        queued_job_flow_status_preprocessor_module_agent_actions_item_type_3 = cls(
            type=type,
            call_id=call_id,
            calls=calls,
            expires_at=expires_at,
        )

        queued_job_flow_status_preprocessor_module_agent_actions_item_type_3.additional_properties = d
        return queued_job_flow_status_preprocessor_module_agent_actions_item_type_3

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
