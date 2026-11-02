from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="GitHubAuthorizationDecisionMetadata")


@_attrs_define
class GitHubAuthorizationDecisionMetadata:
    """
    Attributes:
        decided_by (str):
        decided_at_unix_seconds (int):
    """

    decided_by: str
    decided_at_unix_seconds: int

    def to_dict(self) -> dict[str, Any]:
        decided_by = self.decided_by

        decided_at_unix_seconds = self.decided_at_unix_seconds

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "decided_by": decided_by,
                "decided_at_unix_seconds": decided_at_unix_seconds,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        decided_by = d.pop("decided_by")

        decided_at_unix_seconds = d.pop("decided_at_unix_seconds")

        git_hub_authorization_decision_metadata = cls(
            decided_by=decided_by,
            decided_at_unix_seconds=decided_at_unix_seconds,
        )

        return git_hub_authorization_decision_metadata
