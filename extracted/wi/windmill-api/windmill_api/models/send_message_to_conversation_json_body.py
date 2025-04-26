from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.send_message_to_conversation_json_body_card_block import SendMessageToConversationJsonBodyCardBlock


T = TypeVar("T", bound="SendMessageToConversationJsonBody")


@_attrs_define
class SendMessageToConversationJsonBody:
    """
    Attributes:
        conversation_id (str): The ID of the Teams conversation/activity
        text (str): The message text to be sent in the Teams card
        success (Union[Unset, bool]): Used for styling the card conditionally Default: True.
        card_block (Union[Unset, SendMessageToConversationJsonBodyCardBlock]): The card block to be sent in the Teams
            card
    """

    conversation_id: str
    text: str
    success: Union[Unset, bool] = True
    card_block: Union[Unset, "SendMessageToConversationJsonBodyCardBlock"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        conversation_id = self.conversation_id
        text = self.text
        success = self.success
        card_block: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.card_block, Unset):
            card_block = self.card_block.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "conversation_id": conversation_id,
                "text": text,
            }
        )
        if success is not UNSET:
            field_dict["success"] = success
        if card_block is not UNSET:
            field_dict["card_block"] = card_block

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.send_message_to_conversation_json_body_card_block import (
            SendMessageToConversationJsonBodyCardBlock,
        )

        d = src_dict.copy()
        conversation_id = d.pop("conversation_id")

        text = d.pop("text")

        success = d.pop("success", UNSET)

        _card_block = d.pop("card_block", UNSET)
        card_block: Union[Unset, SendMessageToConversationJsonBodyCardBlock]
        if isinstance(_card_block, Unset):
            card_block = UNSET
        else:
            card_block = SendMessageToConversationJsonBodyCardBlock.from_dict(_card_block)

        send_message_to_conversation_json_body = cls(
            conversation_id=conversation_id,
            text=text,
            success=success,
            card_block=card_block,
        )

        send_message_to_conversation_json_body.additional_properties = d
        return send_message_to_conversation_json_body

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
