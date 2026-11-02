from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.list_ai_session_backups_response_200_sessions_item import ListAiSessionBackupsResponse200SessionsItem


T = TypeVar("T", bound="ListAiSessionBackupsResponse200")


@_attrs_define
class ListAiSessionBackupsResponse200:
    """
    Attributes:
        enabled (bool):
        sessions (List['ListAiSessionBackupsResponse200SessionsItem']): the newest 500 at most
        storage_id (Union[Unset, str]): names the storage answered from; sync state recorded against another one is void
        backup_generation (Union[Unset, int]): bumped by every workspace key rotation; sync state recorded under another
            one is void
        fallback (Union[Unset, bool]): the storage answered from is the instance object store, standing in for a
            workspace without storage of its own; a removal owed to it is retired by any answer from the workspace's own
            storage
        truncated (Union[Unset, bool]): the user has more sessions than the answer names
    """

    enabled: bool
    sessions: List["ListAiSessionBackupsResponse200SessionsItem"]
    storage_id: Union[Unset, str] = UNSET
    backup_generation: Union[Unset, int] = UNSET
    fallback: Union[Unset, bool] = UNSET
    truncated: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        enabled = self.enabled
        sessions = []
        for sessions_item_data in self.sessions:
            sessions_item = sessions_item_data.to_dict()

            sessions.append(sessions_item)

        storage_id = self.storage_id
        backup_generation = self.backup_generation
        fallback = self.fallback
        truncated = self.truncated

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "enabled": enabled,
                "sessions": sessions,
            }
        )
        if storage_id is not UNSET:
            field_dict["storage_id"] = storage_id
        if backup_generation is not UNSET:
            field_dict["backup_generation"] = backup_generation
        if fallback is not UNSET:
            field_dict["fallback"] = fallback
        if truncated is not UNSET:
            field_dict["truncated"] = truncated

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_ai_session_backups_response_200_sessions_item import (
            ListAiSessionBackupsResponse200SessionsItem,
        )

        d = src_dict.copy()
        enabled = d.pop("enabled")

        sessions = []
        _sessions = d.pop("sessions")
        for sessions_item_data in _sessions:
            sessions_item = ListAiSessionBackupsResponse200SessionsItem.from_dict(sessions_item_data)

            sessions.append(sessions_item)

        storage_id = d.pop("storage_id", UNSET)

        backup_generation = d.pop("backup_generation", UNSET)

        fallback = d.pop("fallback", UNSET)

        truncated = d.pop("truncated", UNSET)

        list_ai_session_backups_response_200 = cls(
            enabled=enabled,
            sessions=sessions,
            storage_id=storage_id,
            backup_generation=backup_generation,
            fallback=fallback,
            truncated=truncated,
        )

        list_ai_session_backups_response_200.additional_properties = d
        return list_ai_session_backups_response_200

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
