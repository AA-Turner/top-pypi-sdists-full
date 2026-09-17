from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.pull_ai_session_backups_response_200_sessions_item_chats_item_record import (
        PullAiSessionBackupsResponse200SessionsItemChatsItemRecord,
    )


T = TypeVar("T", bound="PullAiSessionBackupsResponse200SessionsItemChatsItem")


@_attrs_define
class PullAiSessionBackupsResponse200SessionsItemChatsItem:
    """
    Attributes:
        id (str):
        record (PullAiSessionBackupsResponse200SessionsItemChatsItemRecord):
    """

    id: str
    record: "PullAiSessionBackupsResponse200SessionsItemChatsItemRecord"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        record = self.record.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "record": record,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.pull_ai_session_backups_response_200_sessions_item_chats_item_record import (
            PullAiSessionBackupsResponse200SessionsItemChatsItemRecord,
        )

        d = src_dict.copy()
        id = d.pop("id")

        record = PullAiSessionBackupsResponse200SessionsItemChatsItemRecord.from_dict(d.pop("record"))

        pull_ai_session_backups_response_200_sessions_item_chats_item = cls(
            id=id,
            record=record,
        )

        pull_ai_session_backups_response_200_sessions_item_chats_item.additional_properties = d
        return pull_ai_session_backups_response_200_sessions_item_chats_item

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
