from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.push_ai_session_backups_json_body_sessions_item import PushAiSessionBackupsJsonBodySessionsItem


T = TypeVar("T", bound="PushAiSessionBackupsJsonBody")


@_attrs_define
class PushAiSessionBackupsJsonBody:
    """
    Attributes:
        owner (str): the email the push was prepared for; refused with a 409 when it is not the caller's
        sessions (Union[Unset, List['PushAiSessionBackupsJsonBodySessionsItem']]):
        removed (Union[Unset, List[str]]):
    """

    owner: str
    sessions: Union[Unset, List["PushAiSessionBackupsJsonBodySessionsItem"]] = UNSET
    removed: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        owner = self.owner
        sessions: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.sessions, Unset):
            sessions = []
            for sessions_item_data in self.sessions:
                sessions_item = sessions_item_data.to_dict()

                sessions.append(sessions_item)

        removed: Union[Unset, List[str]] = UNSET
        if not isinstance(self.removed, Unset):
            removed = self.removed

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "owner": owner,
            }
        )
        if sessions is not UNSET:
            field_dict["sessions"] = sessions
        if removed is not UNSET:
            field_dict["removed"] = removed

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.push_ai_session_backups_json_body_sessions_item import PushAiSessionBackupsJsonBodySessionsItem

        d = src_dict.copy()
        owner = d.pop("owner")

        sessions = []
        _sessions = d.pop("sessions", UNSET)
        for sessions_item_data in _sessions or []:
            sessions_item = PushAiSessionBackupsJsonBodySessionsItem.from_dict(sessions_item_data)

            sessions.append(sessions_item)

        removed = cast(List[str], d.pop("removed", UNSET))

        push_ai_session_backups_json_body = cls(
            owner=owner,
            sessions=sessions,
            removed=removed,
        )

        push_ai_session_backups_json_body.additional_properties = d
        return push_ai_session_backups_json_body

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
