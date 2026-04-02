from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.checklist_info import ChecklistInfo
    from ..models.project_detail import ProjectDetail


T = TypeVar("T", bound="ProjectDetailsResponse")


@_attrs_define
class ProjectDetailsResponse:
    """
    Attributes:
        checklist (ChecklistInfo):
        total_projects (int):
        projects_with_completions (int):
        fully_completed_projects (int):
        projects_requiring_review (int):
        project_details (list['ProjectDetail']):
    """

    checklist: "ChecklistInfo"
    total_projects: int
    projects_with_completions: int
    fully_completed_projects: int
    projects_requiring_review: int
    project_details: list["ProjectDetail"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        checklist = self.checklist.to_dict()

        total_projects = self.total_projects

        projects_with_completions = self.projects_with_completions

        fully_completed_projects = self.fully_completed_projects

        projects_requiring_review = self.projects_requiring_review

        project_details = []
        for project_details_item_data in self.project_details:
            project_details_item = project_details_item_data.to_dict()
            project_details.append(project_details_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "checklist": checklist,
                "total_projects": total_projects,
                "projects_with_completions": projects_with_completions,
                "fully_completed_projects": fully_completed_projects,
                "projects_requiring_review": projects_requiring_review,
                "project_details": project_details,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.checklist_info import ChecklistInfo
        from ..models.project_detail import ProjectDetail

        d = dict(src_dict)
        checklist = ChecklistInfo.from_dict(d.pop("checklist"))

        total_projects = d.pop("total_projects")

        projects_with_completions = d.pop("projects_with_completions")

        fully_completed_projects = d.pop("fully_completed_projects")

        projects_requiring_review = d.pop("projects_requiring_review")

        project_details = []
        _project_details = d.pop("project_details")
        for project_details_item_data in _project_details:
            project_details_item = ProjectDetail.from_dict(project_details_item_data)

            project_details.append(project_details_item)

        project_details_response = cls(
            checklist=checklist,
            total_projects=total_projects,
            projects_with_completions=projects_with_completions,
            fully_completed_projects=fully_completed_projects,
            projects_requiring_review=projects_requiring_review,
            project_details=project_details,
        )

        project_details_response.additional_properties = d
        return project_details_response

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
