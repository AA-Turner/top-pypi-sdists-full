from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..models.pending_git_hub_authorization_status import (
    PendingGitHubAuthorizationStatus,
)

T = TypeVar("T", bound="PendingGitHubAuthorization")


@_attrs_define
class PendingGitHubAuthorization:
    """
    Attributes:
        status (PendingGitHubAuthorizationStatus):
        authorization_url (str):
        expires_at_unix_seconds (int):
    """

    status: PendingGitHubAuthorizationStatus
    authorization_url: str
    expires_at_unix_seconds: int

    def to_dict(self) -> dict[str, Any]:
        status = self.status.value

        authorization_url = self.authorization_url

        expires_at_unix_seconds = self.expires_at_unix_seconds

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "status": status,
                "authorization_url": authorization_url,
                "expires_at_unix_seconds": expires_at_unix_seconds,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        status = PendingGitHubAuthorizationStatus(d.pop("status"))

        authorization_url = d.pop("authorization_url")

        expires_at_unix_seconds = d.pop("expires_at_unix_seconds")

        pending_git_hub_authorization = cls(
            status=status,
            authorization_url=authorization_url,
            expires_at_unix_seconds=expires_at_unix_seconds,
        )

        return pending_git_hub_authorization
