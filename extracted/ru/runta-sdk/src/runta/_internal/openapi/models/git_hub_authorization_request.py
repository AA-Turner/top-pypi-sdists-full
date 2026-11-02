from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.approved_git_hub_authorization import ApprovedGitHubAuthorization
    from ..models.denied_git_hub_authorization import DeniedGitHubAuthorization
    from ..models.expired_git_hub_authorization import ExpiredGitHubAuthorization
    from ..models.installed_git_hub_authorization import InstalledGitHubAuthorization
    from ..models.pending_git_hub_authorization import PendingGitHubAuthorization


T = TypeVar("T", bound="GitHubAuthorizationRequest")


@_attrs_define
class GitHubAuthorizationRequest:
    """
    Attributes:
        request_id (str):
        requested_by (str):
        created_at_unix_seconds (int):
        lifecycle (ApprovedGitHubAuthorization | DeniedGitHubAuthorization | ExpiredGitHubAuthorization |
            InstalledGitHubAuthorization | PendingGitHubAuthorization):
        reason (str | Unset): What the agent said it needed access for.
    """

    request_id: str
    requested_by: str
    created_at_unix_seconds: int
    lifecycle: (
        ApprovedGitHubAuthorization
        | DeniedGitHubAuthorization
        | ExpiredGitHubAuthorization
        | InstalledGitHubAuthorization
        | PendingGitHubAuthorization
    )
    reason: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.approved_git_hub_authorization import ApprovedGitHubAuthorization
        from ..models.denied_git_hub_authorization import DeniedGitHubAuthorization
        from ..models.installed_git_hub_authorization import (
            InstalledGitHubAuthorization,
        )
        from ..models.pending_git_hub_authorization import PendingGitHubAuthorization

        request_id = self.request_id

        requested_by = self.requested_by

        created_at_unix_seconds = self.created_at_unix_seconds

        lifecycle: dict[str, Any]
        if isinstance(self.lifecycle, PendingGitHubAuthorization):
            lifecycle = self.lifecycle.to_dict()
        elif isinstance(self.lifecycle, ApprovedGitHubAuthorization):
            lifecycle = self.lifecycle.to_dict()
        elif isinstance(self.lifecycle, InstalledGitHubAuthorization):
            lifecycle = self.lifecycle.to_dict()
        elif isinstance(self.lifecycle, DeniedGitHubAuthorization):
            lifecycle = self.lifecycle.to_dict()
        else:
            lifecycle = self.lifecycle.to_dict()

        reason = self.reason

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "request_id": request_id,
                "requested_by": requested_by,
                "created_at_unix_seconds": created_at_unix_seconds,
                "lifecycle": lifecycle,
            }
        )
        if reason is not UNSET:
            field_dict["reason"] = reason

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.approved_git_hub_authorization import ApprovedGitHubAuthorization
        from ..models.denied_git_hub_authorization import DeniedGitHubAuthorization
        from ..models.expired_git_hub_authorization import ExpiredGitHubAuthorization
        from ..models.installed_git_hub_authorization import (
            InstalledGitHubAuthorization,
        )
        from ..models.pending_git_hub_authorization import PendingGitHubAuthorization

        d = dict(src_dict)
        request_id = d.pop("request_id")

        requested_by = d.pop("requested_by")

        created_at_unix_seconds = d.pop("created_at_unix_seconds")

        def _parse_lifecycle(
            data: object,
        ) -> (
            ApprovedGitHubAuthorization
            | DeniedGitHubAuthorization
            | ExpiredGitHubAuthorization
            | InstalledGitHubAuthorization
            | PendingGitHubAuthorization
        ):
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_git_hub_authorization_lifecycle_type_0 = (
                    PendingGitHubAuthorization.from_dict(data)
                )

                return componentsschemas_git_hub_authorization_lifecycle_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_git_hub_authorization_lifecycle_type_1 = (
                    ApprovedGitHubAuthorization.from_dict(data)
                )

                return componentsschemas_git_hub_authorization_lifecycle_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_git_hub_authorization_lifecycle_type_2 = (
                    InstalledGitHubAuthorization.from_dict(data)
                )

                return componentsschemas_git_hub_authorization_lifecycle_type_2
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_git_hub_authorization_lifecycle_type_3 = (
                    DeniedGitHubAuthorization.from_dict(data)
                )

                return componentsschemas_git_hub_authorization_lifecycle_type_3
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_git_hub_authorization_lifecycle_type_4 = (
                ExpiredGitHubAuthorization.from_dict(data)
            )

            return componentsschemas_git_hub_authorization_lifecycle_type_4

        lifecycle = _parse_lifecycle(d.pop("lifecycle"))

        reason = d.pop("reason", UNSET)

        git_hub_authorization_request = cls(
            request_id=request_id,
            requested_by=requested_by,
            created_at_unix_seconds=created_at_unix_seconds,
            lifecycle=lifecycle,
            reason=reason,
        )

        git_hub_authorization_request.additional_properties = d
        return git_hub_authorization_request

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
