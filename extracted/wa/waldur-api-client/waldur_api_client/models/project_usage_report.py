from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.project_usage_report_reports import ProjectUsageReportReports
    from ..models.project_usage_report_users import ProjectUsageReportUsers


T = TypeVar("T", bound="ProjectUsageReport")


@_attrs_define
class ProjectUsageReport:
    """
    Attributes:
        project (str): ProjectIdentifier string e.g. "aiproject.brics"
        reports (ProjectUsageReportReports): "YYYY-MM-DD" → DailyProjectUsageReportJson
        users (ProjectUsageReportUsers): UserIdentifier → local_username. e.g. { "chris.aiproject.brics":
            "chris.aiproject" }
    """

    project: str
    reports: "ProjectUsageReportReports"
    users: "ProjectUsageReportUsers"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project = self.project

        reports = self.reports.to_dict()

        users = self.users.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "project": project,
                "reports": reports,
                "users": users,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.project_usage_report_reports import ProjectUsageReportReports
        from ..models.project_usage_report_users import ProjectUsageReportUsers

        d = dict(src_dict)
        project = d.pop("project")

        reports = ProjectUsageReportReports.from_dict(d.pop("reports"))

        users = ProjectUsageReportUsers.from_dict(d.pop("users"))

        project_usage_report = cls(
            project=project,
            reports=reports,
            users=users,
        )

        project_usage_report.additional_properties = d
        return project_usage_report

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
