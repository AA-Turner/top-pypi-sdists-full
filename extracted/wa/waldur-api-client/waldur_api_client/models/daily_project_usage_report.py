from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.daily_project_usage_report_components import DailyProjectUsageReportComponents
    from ..models.daily_project_usage_report_reports import DailyProjectUsageReportReports
    from ..models.daily_project_usage_report_user_job_counts import DailyProjectUsageReportUserJobCounts
    from ..models.daily_project_usage_report_user_wait_seconds import DailyProjectUsageReportUserWaitSeconds


T = TypeVar("T", bound="DailyProjectUsageReport")


@_attrs_define
class DailyProjectUsageReport:
    """
    Attributes:
        reports (DailyProjectUsageReportReports): local_username → Usage
        is_complete (bool):
        components (Union[Unset, DailyProjectUsageReportComponents]): component_name → local_username → Usage. e.g. {
            "cpu": { "chris.aiproject": { "seconds": 41055 } } }
        user_job_counts (Union[Unset, DailyProjectUsageReportUserJobCounts]): local_username → job count
        user_wait_seconds (Union[Unset, DailyProjectUsageReportUserWaitSeconds]): local_username → wait seconds
        num_jobs (Union[Unset, int]):
        total_wait_seconds (Union[Unset, int]):
    """

    reports: "DailyProjectUsageReportReports"
    is_complete: bool
    components: Union[Unset, "DailyProjectUsageReportComponents"] = UNSET
    user_job_counts: Union[Unset, "DailyProjectUsageReportUserJobCounts"] = UNSET
    user_wait_seconds: Union[Unset, "DailyProjectUsageReportUserWaitSeconds"] = UNSET
    num_jobs: Union[Unset, int] = UNSET
    total_wait_seconds: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        reports = self.reports.to_dict()

        is_complete = self.is_complete

        components: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.components, Unset):
            components = self.components.to_dict()

        user_job_counts: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.user_job_counts, Unset):
            user_job_counts = self.user_job_counts.to_dict()

        user_wait_seconds: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.user_wait_seconds, Unset):
            user_wait_seconds = self.user_wait_seconds.to_dict()

        num_jobs = self.num_jobs

        total_wait_seconds = self.total_wait_seconds

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "reports": reports,
                "is_complete": is_complete,
            }
        )
        if components is not UNSET:
            field_dict["components"] = components
        if user_job_counts is not UNSET:
            field_dict["user_job_counts"] = user_job_counts
        if user_wait_seconds is not UNSET:
            field_dict["user_wait_seconds"] = user_wait_seconds
        if num_jobs is not UNSET:
            field_dict["num_jobs"] = num_jobs
        if total_wait_seconds is not UNSET:
            field_dict["total_wait_seconds"] = total_wait_seconds

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.daily_project_usage_report_components import DailyProjectUsageReportComponents
        from ..models.daily_project_usage_report_reports import DailyProjectUsageReportReports
        from ..models.daily_project_usage_report_user_job_counts import DailyProjectUsageReportUserJobCounts
        from ..models.daily_project_usage_report_user_wait_seconds import DailyProjectUsageReportUserWaitSeconds

        d = dict(src_dict)
        reports = DailyProjectUsageReportReports.from_dict(d.pop("reports"))

        is_complete = d.pop("is_complete")

        _components = d.pop("components", UNSET)
        components: Union[Unset, DailyProjectUsageReportComponents]
        if isinstance(_components, Unset):
            components = UNSET
        else:
            components = DailyProjectUsageReportComponents.from_dict(_components)

        _user_job_counts = d.pop("user_job_counts", UNSET)
        user_job_counts: Union[Unset, DailyProjectUsageReportUserJobCounts]
        if isinstance(_user_job_counts, Unset):
            user_job_counts = UNSET
        else:
            user_job_counts = DailyProjectUsageReportUserJobCounts.from_dict(_user_job_counts)

        _user_wait_seconds = d.pop("user_wait_seconds", UNSET)
        user_wait_seconds: Union[Unset, DailyProjectUsageReportUserWaitSeconds]
        if isinstance(_user_wait_seconds, Unset):
            user_wait_seconds = UNSET
        else:
            user_wait_seconds = DailyProjectUsageReportUserWaitSeconds.from_dict(_user_wait_seconds)

        num_jobs = d.pop("num_jobs", UNSET)

        total_wait_seconds = d.pop("total_wait_seconds", UNSET)

        daily_project_usage_report = cls(
            reports=reports,
            is_complete=is_complete,
            components=components,
            user_job_counts=user_job_counts,
            user_wait_seconds=user_wait_seconds,
            num_jobs=num_jobs,
            total_wait_seconds=total_wait_seconds,
        )

        daily_project_usage_report.additional_properties = d
        return daily_project_usage_report

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
