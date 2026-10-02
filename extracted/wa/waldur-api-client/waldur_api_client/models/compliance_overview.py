from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ComplianceOverview")


@_attrs_define
class ComplianceOverview:
    """
    Attributes:
        total_projects (int):
        projects_with_completions (int):
        fully_completed_projects (int):
        projects_requiring_review (int):
        average_completion_percentage (float):
    """

    total_projects: int
    projects_with_completions: int
    fully_completed_projects: int
    projects_requiring_review: int
    average_completion_percentage: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        total_projects = self.total_projects

        projects_with_completions = self.projects_with_completions

        fully_completed_projects = self.fully_completed_projects

        projects_requiring_review = self.projects_requiring_review

        average_completion_percentage = self.average_completion_percentage

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "total_projects": total_projects,
                "projects_with_completions": projects_with_completions,
                "fully_completed_projects": fully_completed_projects,
                "projects_requiring_review": projects_requiring_review,
                "average_completion_percentage": average_completion_percentage,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        total_projects = d.pop("total_projects")

        projects_with_completions = d.pop("projects_with_completions")

        fully_completed_projects = d.pop("fully_completed_projects")

        projects_requiring_review = d.pop("projects_requiring_review")

        average_completion_percentage = d.pop("average_completion_percentage")

        compliance_overview = cls(
            total_projects=total_projects,
            projects_with_completions=projects_with_completions,
            fully_completed_projects=fully_completed_projects,
            projects_requiring_review=projects_requiring_review,
            average_completion_percentage=average_completion_percentage,
        )

        compliance_overview.additional_properties = d
        return compliance_overview

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
