from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="FlowConversationRunningTurn")


@_attrs_define
class FlowConversationRunningTurn:
    """The turn the conversation is still answering, set by the list endpoint: its newest user message, while the flow run
    it started is queued or running. A run into this conversation is refused with 409 until the turn ends.

        Attributes:
            job_id (str): The flow run of the turn
            user_seq (int): created_seq of the user message that started the turn
    """

    job_id: str
    user_seq: int
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        job_id = self.job_id
        user_seq = self.user_seq

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "job_id": job_id,
                "user_seq": user_seq,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        job_id = d.pop("job_id")

        user_seq = d.pop("user_seq")

        flow_conversation_running_turn = cls(
            job_id=job_id,
            user_seq=user_seq,
        )

        flow_conversation_running_turn.additional_properties = d
        return flow_conversation_running_turn

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
