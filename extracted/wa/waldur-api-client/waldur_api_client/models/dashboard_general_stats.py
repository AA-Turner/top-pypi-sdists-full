from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="DashboardGeneralStats")


@_attrs_define
class DashboardGeneralStats:
    """
    Attributes:
        pending_permission_requests (int):
        active_invitations (int):
        pending_onboarding_applications (int):
    """

    pending_permission_requests: int
    active_invitations: int
    pending_onboarding_applications: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        pending_permission_requests = self.pending_permission_requests

        active_invitations = self.active_invitations

        pending_onboarding_applications = self.pending_onboarding_applications

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "pending_permission_requests": pending_permission_requests,
                "active_invitations": active_invitations,
                "pending_onboarding_applications": pending_onboarding_applications,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        pending_permission_requests = d.pop("pending_permission_requests")

        active_invitations = d.pop("active_invitations")

        pending_onboarding_applications = d.pop("pending_onboarding_applications")

        dashboard_general_stats = cls(
            pending_permission_requests=pending_permission_requests,
            active_invitations=active_invitations,
            pending_onboarding_applications=pending_onboarding_applications,
        )

        dashboard_general_stats.additional_properties = d
        return dashboard_general_stats

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
