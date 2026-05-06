from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.daily_storage_report_project_quotas import DailyStorageReportProjectQuotas
    from ..models.daily_storage_report_user_quotas import DailyStorageReportUserQuotas


T = TypeVar("T", bound="DailyStorageReport")


@_attrs_define
class DailyStorageReport:
    """
    Attributes:
        project (str):
        generated_at (str): RFC3339 timestamp
        project_quotas (DailyStorageReportProjectQuotas): Volume → Quota
        user_quotas (DailyStorageReportUserQuotas): UserIdentifier → (Volume → Quota)
    """

    project: str
    generated_at: str
    project_quotas: "DailyStorageReportProjectQuotas"
    user_quotas: "DailyStorageReportUserQuotas"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project = self.project

        generated_at = self.generated_at

        project_quotas = self.project_quotas.to_dict()

        user_quotas = self.user_quotas.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "project": project,
                "generated_at": generated_at,
                "project_quotas": project_quotas,
                "user_quotas": user_quotas,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.daily_storage_report_project_quotas import DailyStorageReportProjectQuotas
        from ..models.daily_storage_report_user_quotas import DailyStorageReportUserQuotas

        d = dict(src_dict)
        project = d.pop("project")

        generated_at = d.pop("generated_at")

        project_quotas = DailyStorageReportProjectQuotas.from_dict(d.pop("project_quotas"))

        user_quotas = DailyStorageReportUserQuotas.from_dict(d.pop("user_quotas"))

        daily_storage_report = cls(
            project=project,
            generated_at=generated_at,
            project_quotas=project_quotas,
            user_quotas=user_quotas,
        )

        daily_storage_report.additional_properties = d
        return daily_storage_report

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
