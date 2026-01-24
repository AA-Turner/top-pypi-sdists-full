import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.flow_conversation_message_message_type import FlowConversationMessageMessageType
from ..types import UNSET, Unset

T = TypeVar("T", bound="FlowConversationMessage")


@_attrs_define
class FlowConversationMessage:
    """
    Attributes:
        id (str): Unique identifier for the message
        conversation_id (str): The conversation this message belongs to
        message_type (FlowConversationMessageMessageType): Type of the message
        content (str): The message content
        created_at (datetime.datetime): When the message was created
        job_id (Union[Unset, None, str]): Associated job ID if this message came from a flow run
        step_name (Union[Unset, str]): The step name that produced that message
        success (Union[Unset, bool]): Whether the message is a success
    """

    id: str
    conversation_id: str
    message_type: FlowConversationMessageMessageType
    content: str
    created_at: datetime.datetime
    job_id: Union[Unset, None, str] = UNSET
    step_name: Union[Unset, str] = UNSET
    success: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        conversation_id = self.conversation_id
        message_type = self.message_type.value

        content = self.content
        created_at = self.created_at.isoformat()

        job_id = self.job_id
        step_name = self.step_name
        success = self.success

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "conversation_id": conversation_id,
                "message_type": message_type,
                "content": content,
                "created_at": created_at,
            }
        )
        if job_id is not UNSET:
            field_dict["job_id"] = job_id
        if step_name is not UNSET:
            field_dict["step_name"] = step_name
        if success is not UNSET:
            field_dict["success"] = success

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        conversation_id = d.pop("conversation_id")

        message_type = FlowConversationMessageMessageType(d.pop("message_type"))

        content = d.pop("content")

        created_at = isoparse(d.pop("created_at"))

        job_id = d.pop("job_id", UNSET)

        step_name = d.pop("step_name", UNSET)

        success = d.pop("success", UNSET)

        flow_conversation_message = cls(
            id=id,
            conversation_id=conversation_id,
            message_type=message_type,
            content=content,
            created_at=created_at,
            job_id=job_id,
            step_name=step_name,
            success=success,
        )

        flow_conversation_message.additional_properties = d
        return flow_conversation_message

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
