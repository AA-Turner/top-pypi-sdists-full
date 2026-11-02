from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..models.expired_git_hub_authorization_status import (
    ExpiredGitHubAuthorizationStatus,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.git_hub_authorization_decision_metadata import (
        GitHubAuthorizationDecisionMetadata,
    )


T = TypeVar("T", bound="ExpiredGitHubAuthorization")


@_attrs_define
class ExpiredGitHubAuthorization:
    """
    Attributes:
        status (ExpiredGitHubAuthorizationStatus):
        expires_at_unix_seconds (int):
        decision (GitHubAuthorizationDecisionMetadata | Unset):
    """

    status: ExpiredGitHubAuthorizationStatus
    expires_at_unix_seconds: int
    decision: GitHubAuthorizationDecisionMetadata | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        status = self.status.value

        expires_at_unix_seconds = self.expires_at_unix_seconds

        decision: dict[str, Any] | Unset = UNSET
        if not isinstance(self.decision, Unset):
            decision = self.decision.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "status": status,
                "expires_at_unix_seconds": expires_at_unix_seconds,
            }
        )
        if decision is not UNSET:
            field_dict["decision"] = decision

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.git_hub_authorization_decision_metadata import (
            GitHubAuthorizationDecisionMetadata,
        )

        d = dict(src_dict)
        status = ExpiredGitHubAuthorizationStatus(d.pop("status"))

        expires_at_unix_seconds = d.pop("expires_at_unix_seconds")

        _decision = d.pop("decision", UNSET)
        decision: GitHubAuthorizationDecisionMetadata | Unset
        if isinstance(_decision, Unset):
            decision = UNSET
        else:
            decision = GitHubAuthorizationDecisionMetadata.from_dict(_decision)

        expired_git_hub_authorization = cls(
            status=status,
            expires_at_unix_seconds=expires_at_unix_seconds,
            decision=decision,
        )

        return expired_git_hub_authorization
