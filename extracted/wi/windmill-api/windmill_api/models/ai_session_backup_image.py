from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AISessionBackupImage")


@_attrs_define
class AISessionBackupImage:
    """
    Attributes:
        chat_id (str):
        id (str):
        data_url (str):
    """

    chat_id: str
    id: str
    data_url: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        chat_id = self.chat_id
        id = self.id
        data_url = self.data_url

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "chat_id": chat_id,
                "id": id,
                "data_url": data_url,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        chat_id = d.pop("chat_id")

        id = d.pop("id")

        data_url = d.pop("data_url")

        ai_session_backup_image = cls(
            chat_id=chat_id,
            id=id,
            data_url=data_url,
        )

        ai_session_backup_image.additional_properties = d
        return ai_session_backup_image

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
