import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.flow_conversation_message_message_type import FlowConversationMessageMessageType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.flow_conversation_message_attachments_item import FlowConversationMessageAttachmentsItem


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
        created_seq (int): Monotonic cursor assigned when the message is inserted
        job_id (Union[Unset, None, str]): Associated job ID if this message came from a flow run
        step_name (Union[Unset, str]): The step name that produced that message
        success (Union[Unset, bool]): Whether the message is a success
        tool_arguments (Union[Unset, None, str]): On a tool row, the arguments the model wrote for the call. For a
            script, flow or AI agent tool these exclude the inputs its step wires in, which only the tool's job holds. Null
            for a provider-native web search, whose query the provider does not return.
        tool_result (Union[Unset, None, str]): On a tool row, the text the model got back from the call, or what the
            call failed with — the row's own text names the tool rather than the reason. For a provider-native web search,
            its citations.
        reasoning (Union[Unset, None, str]): On an answer, the thinking that produced it; on a tool row, the thinking
            that led to the call. Each round's thinking is on one row. The agent job's result keeps the turn's thinking as a
            single string.
        attachments (Union[Unset, None, List['FlowConversationMessageAttachmentsItem']]): The files a user message
            carried, as object-storage references: every flow input other than user_message that held one or a list of them,
            at most 20. Never file bytes or a presigned URL.
    """

    id: str
    conversation_id: str
    message_type: FlowConversationMessageMessageType
    content: str
    created_at: datetime.datetime
    created_seq: int
    job_id: Union[Unset, None, str] = UNSET
    step_name: Union[Unset, str] = UNSET
    success: Union[Unset, bool] = UNSET
    tool_arguments: Union[Unset, None, str] = UNSET
    tool_result: Union[Unset, None, str] = UNSET
    reasoning: Union[Unset, None, str] = UNSET
    attachments: Union[Unset, None, List["FlowConversationMessageAttachmentsItem"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        conversation_id = self.conversation_id
        message_type = self.message_type.value

        content = self.content
        created_at = self.created_at.isoformat()

        created_seq = self.created_seq
        job_id = self.job_id
        step_name = self.step_name
        success = self.success
        tool_arguments = self.tool_arguments
        tool_result = self.tool_result
        reasoning = self.reasoning
        attachments: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.attachments, Unset):
            if self.attachments is None:
                attachments = None
            else:
                attachments = []
                for attachments_item_data in self.attachments:
                    attachments_item = attachments_item_data.to_dict()

                    attachments.append(attachments_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "conversation_id": conversation_id,
                "message_type": message_type,
                "content": content,
                "created_at": created_at,
                "created_seq": created_seq,
            }
        )
        if job_id is not UNSET:
            field_dict["job_id"] = job_id
        if step_name is not UNSET:
            field_dict["step_name"] = step_name
        if success is not UNSET:
            field_dict["success"] = success
        if tool_arguments is not UNSET:
            field_dict["tool_arguments"] = tool_arguments
        if tool_result is not UNSET:
            field_dict["tool_result"] = tool_result
        if reasoning is not UNSET:
            field_dict["reasoning"] = reasoning
        if attachments is not UNSET:
            field_dict["attachments"] = attachments

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.flow_conversation_message_attachments_item import FlowConversationMessageAttachmentsItem

        d = src_dict.copy()
        id = d.pop("id")

        conversation_id = d.pop("conversation_id")

        message_type = FlowConversationMessageMessageType(d.pop("message_type"))

        content = d.pop("content")

        created_at = isoparse(d.pop("created_at"))

        created_seq = d.pop("created_seq")

        job_id = d.pop("job_id", UNSET)

        step_name = d.pop("step_name", UNSET)

        success = d.pop("success", UNSET)

        tool_arguments = d.pop("tool_arguments", UNSET)

        tool_result = d.pop("tool_result", UNSET)

        reasoning = d.pop("reasoning", UNSET)

        attachments = []
        _attachments = d.pop("attachments", UNSET)
        for attachments_item_data in _attachments or []:
            attachments_item = FlowConversationMessageAttachmentsItem.from_dict(attachments_item_data)

            attachments.append(attachments_item)

        flow_conversation_message = cls(
            id=id,
            conversation_id=conversation_id,
            message_type=message_type,
            content=content,
            created_at=created_at,
            created_seq=created_seq,
            job_id=job_id,
            step_name=step_name,
            success=success,
            tool_arguments=tool_arguments,
            tool_result=tool_result,
            reasoning=reasoning,
            attachments=attachments,
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
