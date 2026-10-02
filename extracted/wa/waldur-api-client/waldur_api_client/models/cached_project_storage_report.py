from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.project_storage_report import ProjectStorageReport


T = TypeVar("T", bound="CachedProjectStorageReport")


@_attrs_define
class CachedProjectStorageReport:
    """
    Attributes:
        id (int):
        year (int):
        month (int):
        project_identifier (str):
        resource (str):
        report (ProjectStorageReport):
    """

    id: int
    year: int
    month: int
    project_identifier: str
    resource: str
    report: "ProjectStorageReport"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        year = self.year

        month = self.month

        project_identifier = self.project_identifier

        resource = self.resource

        report = self.report.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "year": year,
                "month": month,
                "project_identifier": project_identifier,
                "resource": resource,
                "report": report,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.project_storage_report import ProjectStorageReport

        d = dict(src_dict)
        id = d.pop("id")

        year = d.pop("year")

        month = d.pop("month")

        project_identifier = d.pop("project_identifier")

        resource = d.pop("resource")

        report = ProjectStorageReport.from_dict(d.pop("report"))

        cached_project_storage_report = cls(
            id=id,
            year=year,
            month=month,
            project_identifier=project_identifier,
            resource=resource,
            report=report,
        )

        cached_project_storage_report.additional_properties = d
        return cached_project_storage_report

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
