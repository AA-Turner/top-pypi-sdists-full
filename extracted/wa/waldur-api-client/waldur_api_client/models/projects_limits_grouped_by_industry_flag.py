from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.projects_limits_grouped_by_industry_flag_limits import ProjectsLimitsGroupedByIndustryFlagLimits


T = TypeVar("T", bound="ProjectsLimitsGroupedByIndustryFlag")


@_attrs_define
class ProjectsLimitsGroupedByIndustryFlag:
    """
    Attributes:
        limits (ProjectsLimitsGroupedByIndustryFlagLimits): Nested dictionary of resource limits by category and
            component type
    """

    limits: "ProjectsLimitsGroupedByIndustryFlagLimits"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        limits = self.limits.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "limits": limits,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.projects_limits_grouped_by_industry_flag_limits import ProjectsLimitsGroupedByIndustryFlagLimits

        d = dict(src_dict)
        limits = ProjectsLimitsGroupedByIndustryFlagLimits.from_dict(d.pop("limits"))

        projects_limits_grouped_by_industry_flag = cls(
            limits=limits,
        )

        projects_limits_grouped_by_industry_flag.additional_properties = d
        return projects_limits_grouped_by_industry_flag

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
