from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..models.denied_git_hub_authorization_status import DeniedGitHubAuthorizationStatus

if TYPE_CHECKING:
    from ..models.git_hub_authorization_decision_metadata import (
        GitHubAuthorizationDecisionMetadata,
    )


T = TypeVar("T", bound="DeniedGitHubAuthorization")


@_attrs_define
class DeniedGitHubAuthorization:
    """
    Attributes:
        status (DeniedGitHubAuthorizationStatus):
        decision (GitHubAuthorizationDecisionMetadata):
    """

    status: DeniedGitHubAuthorizationStatus
    decision: GitHubAuthorizationDecisionMetadata

    def to_dict(self) -> dict[str, Any]:
        status = self.status.value

        decision = self.decision.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "status": status,
                "decision": decision,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.git_hub_authorization_decision_metadata import (
            GitHubAuthorizationDecisionMetadata,
        )

        d = dict(src_dict)
        status = DeniedGitHubAuthorizationStatus(d.pop("status"))

        decision = GitHubAuthorizationDecisionMetadata.from_dict(d.pop("decision"))

        denied_git_hub_authorization = cls(
            status=status,
            decision=decision,
        )

        return denied_git_hub_authorization
