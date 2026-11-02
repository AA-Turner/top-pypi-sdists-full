from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="PushAiSessionBackupsJsonBodySessionsItemDeleteImagesItem")


@_attrs_define
class PushAiSessionBackupsJsonBodySessionsItemDeleteImagesItem:
    """
    Attributes:
        chat_id (str):
        id (str):
    """

    chat_id: str
    id: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        chat_id = self.chat_id
        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "chat_id": chat_id,
                "id": id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        chat_id = d.pop("chat_id")

        id = d.pop("id")

        push_ai_session_backups_json_body_sessions_item_delete_images_item = cls(
            chat_id=chat_id,
            id=id,
        )

        push_ai_session_backups_json_body_sessions_item_delete_images_item.additional_properties = d
        return push_ai_session_backups_json_body_sessions_item_delete_images_item

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
