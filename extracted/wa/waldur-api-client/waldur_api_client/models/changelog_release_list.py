from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.changelog_release_summary import ChangelogReleaseSummary


T = TypeVar("T", bound="ChangelogReleaseList")


@_attrs_define
class ChangelogReleaseList:
    """
    Attributes:
        current_version (str):
        releases (list['ChangelogReleaseSummary']):
    """

    current_version: str
    releases: list["ChangelogReleaseSummary"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        current_version = self.current_version

        releases = []
        for releases_item_data in self.releases:
            releases_item = releases_item_data.to_dict()
            releases.append(releases_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "current_version": current_version,
                "releases": releases,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.changelog_release_summary import ChangelogReleaseSummary

        d = dict(src_dict)
        current_version = d.pop("current_version")

        releases = []
        _releases = d.pop("releases")
        for releases_item_data in _releases:
            releases_item = ChangelogReleaseSummary.from_dict(releases_item_data)

            releases.append(releases_item)

        changelog_release_list = cls(
            current_version=current_version,
            releases=releases,
        )

        changelog_release_list.additional_properties = d
        return changelog_release_list

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
