from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.ai_session_backup_push_chats_item_record import AISessionBackupPushChatsItemRecord


T = TypeVar("T", bound="AISessionBackupPushChatsItem")


@_attrs_define
class AISessionBackupPushChatsItem:
    """
    Attributes:
        id (str):
        record (AISessionBackupPushChatsItemRecord):
    """

    id: str
    record: "AISessionBackupPushChatsItemRecord"
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
        from ..models.ai_session_backup_push_chats_item_record import AISessionBackupPushChatsItemRecord

        d = src_dict.copy()
        id = d.pop("id")

        record = AISessionBackupPushChatsItemRecord.from_dict(d.pop("record"))

        ai_session_backup_push_chats_item = cls(
            id=id,
            record=record,
        )

        ai_session_backup_push_chats_item.additional_properties = d
        return ai_session_backup_push_chats_item

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
