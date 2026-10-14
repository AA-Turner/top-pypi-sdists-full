import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.changelog_release import ChangelogRelease


T = TypeVar("T", bound="ChangelogPending")


@_attrs_define
class ChangelogPending:
    """
    Attributes:
        current_version (str):
        latest_version (str):
        versions_behind (int):
        releases (list['ChangelogRelease']):
        impact_analysis_status (Union[Unset, str]):
        impact_analysis_computed_at (Union[Unset, datetime.datetime]):
    """

    current_version: str
    latest_version: str
    versions_behind: int
    releases: list["ChangelogRelease"]
    impact_analysis_status: Union[Unset, str] = UNSET
    impact_analysis_computed_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        current_version = self.current_version

        latest_version = self.latest_version

        versions_behind = self.versions_behind

        releases = []
        for releases_item_data in self.releases:
            releases_item = releases_item_data.to_dict()
            releases.append(releases_item)

        impact_analysis_status = self.impact_analysis_status

        impact_analysis_computed_at: Union[Unset, str] = UNSET
        if not isinstance(self.impact_analysis_computed_at, Unset):
            impact_analysis_computed_at = self.impact_analysis_computed_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "current_version": current_version,
                "latest_version": latest_version,
                "versions_behind": versions_behind,
                "releases": releases,
            }
        )
        if impact_analysis_status is not UNSET:
            field_dict["impact_analysis_status"] = impact_analysis_status
        if impact_analysis_computed_at is not UNSET:
            field_dict["impact_analysis_computed_at"] = impact_analysis_computed_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.changelog_release import ChangelogRelease

        d = dict(src_dict)
        current_version = d.pop("current_version")

        latest_version = d.pop("latest_version")

        versions_behind = d.pop("versions_behind")

        releases = []
        _releases = d.pop("releases")
        for releases_item_data in _releases:
            releases_item = ChangelogRelease.from_dict(releases_item_data)

            releases.append(releases_item)

        impact_analysis_status = d.pop("impact_analysis_status", UNSET)

        _impact_analysis_computed_at = d.pop("impact_analysis_computed_at", UNSET)
        impact_analysis_computed_at: Union[Unset, datetime.datetime]
        if isinstance(_impact_analysis_computed_at, Unset):
            impact_analysis_computed_at = UNSET
        else:
            impact_analysis_computed_at = isoparse(_impact_analysis_computed_at)

        changelog_pending = cls(
            current_version=current_version,
            latest_version=latest_version,
            versions_behind=versions_behind,
            releases=releases,
            impact_analysis_status=impact_analysis_status,
            impact_analysis_computed_at=impact_analysis_computed_at,
        )

        changelog_pending.additional_properties = d
        return changelog_pending

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
