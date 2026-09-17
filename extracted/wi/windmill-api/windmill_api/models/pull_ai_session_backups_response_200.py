from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.pull_ai_session_backups_response_200_sessions_item import PullAiSessionBackupsResponse200SessionsItem


T = TypeVar("T", bound="PullAiSessionBackupsResponse200")


@_attrs_define
class PullAiSessionBackupsResponse200:
    """
    Attributes:
        enabled (bool):
        sessions (List['PullAiSessionBackupsResponse200SessionsItem']):
        deferred (List[str]):
        storage_id (Union[Unset, str]):
        backup_generation (Union[Unset, int]):
        fallback (Union[Unset, bool]):
    """

    enabled: bool
    sessions: List["PullAiSessionBackupsResponse200SessionsItem"]
    deferred: List[str]
    storage_id: Union[Unset, str] = UNSET
    backup_generation: Union[Unset, int] = UNSET
    fallback: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        enabled = self.enabled
        sessions = []
        for sessions_item_data in self.sessions:
            sessions_item = sessions_item_data.to_dict()

            sessions.append(sessions_item)

        deferred = self.deferred

        storage_id = self.storage_id
        backup_generation = self.backup_generation
        fallback = self.fallback

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "enabled": enabled,
                "sessions": sessions,
                "deferred": deferred,
            }
        )
        if storage_id is not UNSET:
            field_dict["storage_id"] = storage_id
        if backup_generation is not UNSET:
            field_dict["backup_generation"] = backup_generation
        if fallback is not UNSET:
            field_dict["fallback"] = fallback

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.pull_ai_session_backups_response_200_sessions_item import (
            PullAiSessionBackupsResponse200SessionsItem,
        )

        d = src_dict.copy()
        enabled = d.pop("enabled")

        sessions = []
        _sessions = d.pop("sessions")
        for sessions_item_data in _sessions:
            sessions_item = PullAiSessionBackupsResponse200SessionsItem.from_dict(sessions_item_data)

            sessions.append(sessions_item)

        deferred = cast(List[str], d.pop("deferred"))

        storage_id = d.pop("storage_id", UNSET)

        backup_generation = d.pop("backup_generation", UNSET)

        fallback = d.pop("fallback", UNSET)

        pull_ai_session_backups_response_200 = cls(
            enabled=enabled,
            sessions=sessions,
            deferred=deferred,
            storage_id=storage_id,
            backup_generation=backup_generation,
            fallback=fallback,
        )

        pull_ai_session_backups_response_200.additional_properties = d
        return pull_ai_session_backups_response_200

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
