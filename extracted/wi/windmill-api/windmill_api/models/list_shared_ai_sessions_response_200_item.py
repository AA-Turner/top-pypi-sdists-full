import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ListSharedAiSessionsResponse200Item")


@_attrs_define
class ListSharedAiSessionsResponse200Item:
    """
    Attributes:
        id (str):
        name (str):
        is_public (bool):
        message_count (int):
        created_by (str):
        shared_at (datetime.datetime):
        mine (bool):
        session_id (Union[Unset, str]):
        opened_at (Union[Unset, datetime.datetime]): when the caller last opened this share by link
    """

    id: str
    name: str
    is_public: bool
    message_count: int
    created_by: str
    shared_at: datetime.datetime
    mine: bool
    session_id: Union[Unset, str] = UNSET
    opened_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        is_public = self.is_public
        message_count = self.message_count
        created_by = self.created_by
        shared_at = self.shared_at.isoformat()

        mine = self.mine
        session_id = self.session_id
        opened_at: Union[Unset, str] = UNSET
        if not isinstance(self.opened_at, Unset):
            opened_at = self.opened_at.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "is_public": is_public,
                "message_count": message_count,
                "created_by": created_by,
                "shared_at": shared_at,
                "mine": mine,
            }
        )
        if session_id is not UNSET:
            field_dict["session_id"] = session_id
        if opened_at is not UNSET:
            field_dict["opened_at"] = opened_at

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        is_public = d.pop("is_public")

        message_count = d.pop("message_count")

        created_by = d.pop("created_by")

        shared_at = isoparse(d.pop("shared_at"))

        mine = d.pop("mine")

        session_id = d.pop("session_id", UNSET)

        _opened_at = d.pop("opened_at", UNSET)
        opened_at: Union[Unset, datetime.datetime]
        if isinstance(_opened_at, Unset):
            opened_at = UNSET
        else:
            opened_at = isoparse(_opened_at)

        list_shared_ai_sessions_response_200_item = cls(
            id=id,
            name=name,
            is_public=is_public,
            message_count=message_count,
            created_by=created_by,
            shared_at=shared_at,
            mine=mine,
            session_id=session_id,
            opened_at=opened_at,
        )

        list_shared_ai_sessions_response_200_item.additional_properties = d
        return list_shared_ai_sessions_response_200_item

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
