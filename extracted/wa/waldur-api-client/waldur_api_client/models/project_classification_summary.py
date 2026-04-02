from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ProjectClassificationSummary")


@_attrs_define
class ProjectClassificationSummary:
    """
    Attributes:
        total_projects (int): Total number of projects
        academic_projects (int): Number of academic projects (industry_flag=False)
        industry_projects (int): Number of industry projects (industry_flag=True)
    """

    total_projects: int
    academic_projects: int
    industry_projects: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        total_projects = self.total_projects

        academic_projects = self.academic_projects

        industry_projects = self.industry_projects

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "total_projects": total_projects,
                "academic_projects": academic_projects,
                "industry_projects": industry_projects,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        total_projects = d.pop("total_projects")

        academic_projects = d.pop("academic_projects")

        industry_projects = d.pop("industry_projects")

        project_classification_summary = cls(
            total_projects=total_projects,
            academic_projects=academic_projects,
            industry_projects=industry_projects,
        )

        project_classification_summary.additional_properties = d
        return project_classification_summary

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
