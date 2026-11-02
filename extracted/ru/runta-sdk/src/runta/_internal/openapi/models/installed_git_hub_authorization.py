from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..models.installed_git_hub_authorization_status import (
    InstalledGitHubAuthorizationStatus,
)

if TYPE_CHECKING:
    from ..models.git_hub_authorization_decision_metadata import (
        GitHubAuthorizationDecisionMetadata,
    )


T = TypeVar("T", bound="InstalledGitHubAuthorization")


@_attrs_define
class InstalledGitHubAuthorization:
    """
    Attributes:
        status (InstalledGitHubAuthorizationStatus):
        decision (GitHubAuthorizationDecisionMetadata):
        installation_id (int):
    """

    status: InstalledGitHubAuthorizationStatus
    decision: GitHubAuthorizationDecisionMetadata
    installation_id: int

    def to_dict(self) -> dict[str, Any]:
        status = self.status.value

        decision = self.decision.to_dict()

        installation_id = self.installation_id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "status": status,
                "decision": decision,
                "installation_id": installation_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.git_hub_authorization_decision_metadata import (
            GitHubAuthorizationDecisionMetadata,
        )

        d = dict(src_dict)
        status = InstalledGitHubAuthorizationStatus(d.pop("status"))

        decision = GitHubAuthorizationDecisionMetadata.from_dict(d.pop("decision"))

        installation_id = d.pop("installation_id")

        installed_git_hub_authorization = cls(
            status=status,
            decision=decision,
            installation_id=installation_id,
        )

        return installed_git_hub_authorization
