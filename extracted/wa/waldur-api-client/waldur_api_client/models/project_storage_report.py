from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.project_storage_report_daily_reports import ProjectStorageReportDailyReports
    from ..models.project_storage_report_project_quotas import ProjectStorageReportProjectQuotas
    from ..models.project_storage_report_user_quotas import ProjectStorageReportUserQuotas
    from ..models.project_storage_report_users import ProjectStorageReportUsers


T = TypeVar("T", bound="ProjectStorageReport")


@_attrs_define
class ProjectStorageReport:
    """
    Attributes:
        project (str):
        generated_at (str): RFC3339 timestamp
        project_quotas (ProjectStorageReportProjectQuotas): Volume → Quota
        user_quotas (ProjectStorageReportUserQuotas): UserIdentifier → (Volume → Quota)
        users (ProjectStorageReportUsers): UserIdentifier → local_username
        daily_reports (Union[Unset, ProjectStorageReportDailyReports]): "YYYY-MM-DD" → DailyStorageReportJson. Absent
            from JSON when there are no daily snapshots.
    """

    project: str
    generated_at: str
    project_quotas: "ProjectStorageReportProjectQuotas"
    user_quotas: "ProjectStorageReportUserQuotas"
    users: "ProjectStorageReportUsers"
    daily_reports: Union[Unset, "ProjectStorageReportDailyReports"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project = self.project

        generated_at = self.generated_at

        project_quotas = self.project_quotas.to_dict()

        user_quotas = self.user_quotas.to_dict()

        users = self.users.to_dict()

        daily_reports: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.daily_reports, Unset):
            daily_reports = self.daily_reports.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "project": project,
                "generated_at": generated_at,
                "project_quotas": project_quotas,
                "user_quotas": user_quotas,
                "users": users,
            }
        )
        if daily_reports is not UNSET:
            field_dict["daily_reports"] = daily_reports

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.project_storage_report_daily_reports import ProjectStorageReportDailyReports
        from ..models.project_storage_report_project_quotas import ProjectStorageReportProjectQuotas
        from ..models.project_storage_report_user_quotas import ProjectStorageReportUserQuotas
        from ..models.project_storage_report_users import ProjectStorageReportUsers

        d = dict(src_dict)
        project = d.pop("project")

        generated_at = d.pop("generated_at")

        project_quotas = ProjectStorageReportProjectQuotas.from_dict(d.pop("project_quotas"))

        user_quotas = ProjectStorageReportUserQuotas.from_dict(d.pop("user_quotas"))

        users = ProjectStorageReportUsers.from_dict(d.pop("users"))

        _daily_reports = d.pop("daily_reports", UNSET)
        daily_reports: Union[Unset, ProjectStorageReportDailyReports]
        if isinstance(_daily_reports, Unset):
            daily_reports = UNSET
        else:
            daily_reports = ProjectStorageReportDailyReports.from_dict(_daily_reports)

        project_storage_report = cls(
            project=project,
            generated_at=generated_at,
            project_quotas=project_quotas,
            user_quotas=user_quotas,
            users=users,
            daily_reports=daily_reports,
        )

        project_storage_report.additional_properties = d
        return project_storage_report

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
