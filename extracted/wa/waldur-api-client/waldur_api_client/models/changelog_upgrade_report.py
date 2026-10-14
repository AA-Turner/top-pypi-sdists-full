from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.announcement_type_enum import AnnouncementTypeEnum

if TYPE_CHECKING:
    from ..models.upgrade_commands import UpgradeCommands


T = TypeVar("T", bound="ChangelogUpgradeReport")


@_attrs_define
class ChangelogUpgradeReport:
    """
    Attributes:
        current_version (str):
        latest_version (str):
        entry_count (int):
        commands (UpgradeCommands):
        report (str): Markdown upgrade report
        announcement (str): Markdown text for a maintenance announcement
        announcement_type (AnnouncementTypeEnum):
    """

    current_version: str
    latest_version: str
    entry_count: int
    commands: "UpgradeCommands"
    report: str
    announcement: str
    announcement_type: AnnouncementTypeEnum
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        current_version = self.current_version

        latest_version = self.latest_version

        entry_count = self.entry_count

        commands = self.commands.to_dict()

        report = self.report

        announcement = self.announcement

        announcement_type = self.announcement_type.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "current_version": current_version,
                "latest_version": latest_version,
                "entry_count": entry_count,
                "commands": commands,
                "report": report,
                "announcement": announcement,
                "announcement_type": announcement_type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.upgrade_commands import UpgradeCommands

        d = dict(src_dict)
        current_version = d.pop("current_version")

        latest_version = d.pop("latest_version")

        entry_count = d.pop("entry_count")

        commands = UpgradeCommands.from_dict(d.pop("commands"))

        report = d.pop("report")

        announcement = d.pop("announcement")

        announcement_type = AnnouncementTypeEnum(d.pop("announcement_type"))

        changelog_upgrade_report = cls(
            current_version=current_version,
            latest_version=latest_version,
            entry_count=entry_count,
            commands=commands,
            report=report,
            announcement=announcement,
            announcement_type=announcement_type,
        )

        changelog_upgrade_report.additional_properties = d
        return changelog_upgrade_report

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
