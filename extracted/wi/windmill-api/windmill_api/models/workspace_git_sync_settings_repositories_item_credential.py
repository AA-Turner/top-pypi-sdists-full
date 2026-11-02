import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.workspace_git_sync_settings_repositories_item_credential_provider import (
    WorkspaceGitSyncSettingsRepositoriesItemCredentialProvider,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkspaceGitSyncSettingsRepositoriesItemCredential")


@_attrs_define
class WorkspaceGitSyncSettingsRepositoriesItemCredential:
    """server-owned, what the repo's own credential reports about itself

    Attributes:
        provider (WorkspaceGitSyncSettingsRepositoriesItemCredentialProvider):
        rotatable (bool): whether this workspace renews the credential itself
        checked_at (int):
        token_id (Union[Unset, int]):
        expires_at (Union[Unset, datetime.date]): absent for a non-expiring token
        scopes (Union[Unset, List[str]]):
        error (Union[Unset, str]):
    """

    provider: WorkspaceGitSyncSettingsRepositoriesItemCredentialProvider
    rotatable: bool
    checked_at: int
    token_id: Union[Unset, int] = UNSET
    expires_at: Union[Unset, datetime.date] = UNSET
    scopes: Union[Unset, List[str]] = UNSET
    error: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        provider = self.provider.value

        rotatable = self.rotatable
        checked_at = self.checked_at
        token_id = self.token_id
        expires_at: Union[Unset, str] = UNSET
        if not isinstance(self.expires_at, Unset):
            expires_at = self.expires_at.isoformat()

        scopes: Union[Unset, List[str]] = UNSET
        if not isinstance(self.scopes, Unset):
            scopes = self.scopes

        error = self.error

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "provider": provider,
                "rotatable": rotatable,
                "checked_at": checked_at,
            }
        )
        if token_id is not UNSET:
            field_dict["token_id"] = token_id
        if expires_at is not UNSET:
            field_dict["expires_at"] = expires_at
        if scopes is not UNSET:
            field_dict["scopes"] = scopes
        if error is not UNSET:
            field_dict["error"] = error

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        provider = WorkspaceGitSyncSettingsRepositoriesItemCredentialProvider(d.pop("provider"))

        rotatable = d.pop("rotatable")

        checked_at = d.pop("checked_at")

        token_id = d.pop("token_id", UNSET)

        _expires_at = d.pop("expires_at", UNSET)
        expires_at: Union[Unset, datetime.date]
        if isinstance(_expires_at, Unset):
            expires_at = UNSET
        else:
            expires_at = isoparse(_expires_at).date()

        scopes = cast(List[str], d.pop("scopes", UNSET))

        error = d.pop("error", UNSET)

        workspace_git_sync_settings_repositories_item_credential = cls(
            provider=provider,
            rotatable=rotatable,
            checked_at=checked_at,
            token_id=token_id,
            expires_at=expires_at,
            scopes=scopes,
            error=error,
        )

        workspace_git_sync_settings_repositories_item_credential.additional_properties = d
        return workspace_git_sync_settings_repositories_item_credential

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
