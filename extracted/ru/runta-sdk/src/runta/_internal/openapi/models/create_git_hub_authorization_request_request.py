from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateGitHubAuthorizationRequestRequest")


@_attrs_define
class CreateGitHubAuthorizationRequestRequest:
    """
    Attributes:
        reason (str | Unset): What access is needed for, shown to the approver verbatim.
    """

    reason: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        reason = self.reason

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if reason is not UNSET:
            field_dict["reason"] = reason

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        reason = d.pop("reason", UNSET)

        create_git_hub_authorization_request_request = cls(
            reason=reason,
        )

        return create_git_hub_authorization_request_request
