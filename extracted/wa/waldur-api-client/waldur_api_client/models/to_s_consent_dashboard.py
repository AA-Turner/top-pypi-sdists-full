from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.time_series_to_s_data import TimeSeriesToSData
    from ..models.version_adoption import VersionAdoption


T = TypeVar("T", bound="ToSConsentDashboard")


@_attrs_define
class ToSConsentDashboard:
    """
    Attributes:
        active_users_count (int): Number of active users
        total_users_count (int): Total number of users
        active_users_percentage (float): Percentage of active users
        accepted_consents_count (int): Number of accepted consents
        revoked_consents_count (int): Number of revoked consents
        total_consents_count (int): Total number of consents
        revoked_consents_over_time (list['TimeSeriesToSData']):
        tos_version_adoption (list['VersionAdoption']):
        active_users_over_time (list['TimeSeriesToSData']):
        accepted_consents_over_time (list['TimeSeriesToSData']):
    """

    active_users_count: int
    total_users_count: int
    active_users_percentage: float
    accepted_consents_count: int
    revoked_consents_count: int
    total_consents_count: int
    revoked_consents_over_time: list["TimeSeriesToSData"]
    tos_version_adoption: list["VersionAdoption"]
    active_users_over_time: list["TimeSeriesToSData"]
    accepted_consents_over_time: list["TimeSeriesToSData"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        active_users_count = self.active_users_count

        total_users_count = self.total_users_count

        active_users_percentage = self.active_users_percentage

        accepted_consents_count = self.accepted_consents_count

        revoked_consents_count = self.revoked_consents_count

        total_consents_count = self.total_consents_count

        revoked_consents_over_time = []
        for revoked_consents_over_time_item_data in self.revoked_consents_over_time:
            revoked_consents_over_time_item = revoked_consents_over_time_item_data.to_dict()
            revoked_consents_over_time.append(revoked_consents_over_time_item)

        tos_version_adoption = []
        for tos_version_adoption_item_data in self.tos_version_adoption:
            tos_version_adoption_item = tos_version_adoption_item_data.to_dict()
            tos_version_adoption.append(tos_version_adoption_item)

        active_users_over_time = []
        for active_users_over_time_item_data in self.active_users_over_time:
            active_users_over_time_item = active_users_over_time_item_data.to_dict()
            active_users_over_time.append(active_users_over_time_item)

        accepted_consents_over_time = []
        for accepted_consents_over_time_item_data in self.accepted_consents_over_time:
            accepted_consents_over_time_item = accepted_consents_over_time_item_data.to_dict()
            accepted_consents_over_time.append(accepted_consents_over_time_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "active_users_count": active_users_count,
                "total_users_count": total_users_count,
                "active_users_percentage": active_users_percentage,
                "accepted_consents_count": accepted_consents_count,
                "revoked_consents_count": revoked_consents_count,
                "total_consents_count": total_consents_count,
                "revoked_consents_over_time": revoked_consents_over_time,
                "tos_version_adoption": tos_version_adoption,
                "active_users_over_time": active_users_over_time,
                "accepted_consents_over_time": accepted_consents_over_time,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.time_series_to_s_data import TimeSeriesToSData
        from ..models.version_adoption import VersionAdoption

        d = dict(src_dict)
        active_users_count = d.pop("active_users_count")

        total_users_count = d.pop("total_users_count")

        active_users_percentage = d.pop("active_users_percentage")

        accepted_consents_count = d.pop("accepted_consents_count")

        revoked_consents_count = d.pop("revoked_consents_count")

        total_consents_count = d.pop("total_consents_count")

        revoked_consents_over_time = []
        _revoked_consents_over_time = d.pop("revoked_consents_over_time")
        for revoked_consents_over_time_item_data in _revoked_consents_over_time:
            revoked_consents_over_time_item = TimeSeriesToSData.from_dict(revoked_consents_over_time_item_data)

            revoked_consents_over_time.append(revoked_consents_over_time_item)

        tos_version_adoption = []
        _tos_version_adoption = d.pop("tos_version_adoption")
        for tos_version_adoption_item_data in _tos_version_adoption:
            tos_version_adoption_item = VersionAdoption.from_dict(tos_version_adoption_item_data)

            tos_version_adoption.append(tos_version_adoption_item)

        active_users_over_time = []
        _active_users_over_time = d.pop("active_users_over_time")
        for active_users_over_time_item_data in _active_users_over_time:
            active_users_over_time_item = TimeSeriesToSData.from_dict(active_users_over_time_item_data)

            active_users_over_time.append(active_users_over_time_item)

        accepted_consents_over_time = []
        _accepted_consents_over_time = d.pop("accepted_consents_over_time")
        for accepted_consents_over_time_item_data in _accepted_consents_over_time:
            accepted_consents_over_time_item = TimeSeriesToSData.from_dict(accepted_consents_over_time_item_data)

            accepted_consents_over_time.append(accepted_consents_over_time_item)

        to_s_consent_dashboard = cls(
            active_users_count=active_users_count,
            total_users_count=total_users_count,
            active_users_percentage=active_users_percentage,
            accepted_consents_count=accepted_consents_count,
            revoked_consents_count=revoked_consents_count,
            total_consents_count=total_consents_count,
            revoked_consents_over_time=revoked_consents_over_time,
            tos_version_adoption=tos_version_adoption,
            active_users_over_time=active_users_over_time,
            accepted_consents_over_time=accepted_consents_over_time,
        )

        to_s_consent_dashboard.additional_properties = d
        return to_s_consent_dashboard

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
