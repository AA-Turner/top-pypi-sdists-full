from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.version_changelog_summary import VersionChangelogSummary


T = TypeVar("T", bound="Version")


@_attrs_define
class Version:
    """
    Attributes:
        version (str): Current installed version of the application
        latest_version (Union[Unset, str]): Latest available version from GitHub. Only included for staff or support
            users when update checks are enabled.
        changelog_summary (Union[Unset, VersionChangelogSummary]): Compact changelog summary with version count, risk
            info, and security alerts.
    """

    version: str
    latest_version: Union[Unset, str] = UNSET
    changelog_summary: Union[Unset, "VersionChangelogSummary"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        version = self.version

        latest_version = self.latest_version

        changelog_summary: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.changelog_summary, Unset):
            changelog_summary = self.changelog_summary.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "version": version,
            }
        )
        if latest_version is not UNSET:
            field_dict["latest_version"] = latest_version
        if changelog_summary is not UNSET:
            field_dict["changelog_summary"] = changelog_summary

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.version_changelog_summary import VersionChangelogSummary

        d = dict(src_dict)
        version = d.pop("version")

        latest_version = d.pop("latest_version", UNSET)

        _changelog_summary = d.pop("changelog_summary", UNSET)
        changelog_summary: Union[Unset, VersionChangelogSummary]
        if isinstance(_changelog_summary, Unset):
            changelog_summary = UNSET
        else:
            changelog_summary = VersionChangelogSummary.from_dict(_changelog_summary)

        version = cls(
            version=version,
            latest_version=latest_version,
            changelog_summary=changelog_summary,
        )

        version.additional_properties = d
        return version

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
