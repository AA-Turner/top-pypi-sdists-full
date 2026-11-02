from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..models.approved_git_hub_authorization_status import (
    ApprovedGitHubAuthorizationStatus,
)

if TYPE_CHECKING:
    from ..models.git_hub_authorization_decision_metadata import (
        GitHubAuthorizationDecisionMetadata,
    )


T = TypeVar("T", bound="ApprovedGitHubAuthorization")


@_attrs_define
class ApprovedGitHubAuthorization:
    """
    Attributes:
        status (ApprovedGitHubAuthorizationStatus):
        decision (GitHubAuthorizationDecisionMetadata):
        expires_at_unix_seconds (int):
    """

    status: ApprovedGitHubAuthorizationStatus
    decision: GitHubAuthorizationDecisionMetadata
    expires_at_unix_seconds: int

    def to_dict(self) -> dict[str, Any]:
        status = self.status.value

        decision = self.decision.to_dict()

        expires_at_unix_seconds = self.expires_at_unix_seconds

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "status": status,
                "decision": decision,
                "expires_at_unix_seconds": expires_at_unix_seconds,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.git_hub_authorization_decision_metadata import (
            GitHubAuthorizationDecisionMetadata,
        )

        d = dict(src_dict)
        status = ApprovedGitHubAuthorizationStatus(d.pop("status"))

        decision = GitHubAuthorizationDecisionMetadata.from_dict(d.pop("decision"))

        expires_at_unix_seconds = d.pop("expires_at_unix_seconds")

        approved_git_hub_authorization = cls(
            status=status,
            decision=decision,
            expires_at_unix_seconds=expires_at_unix_seconds,
        )

        return approved_git_hub_authorization
