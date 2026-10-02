from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.project_template_role_mapping_data_additional_property import (
        ProjectTemplateRoleMappingDataAdditionalProperty,
    )


T = TypeVar("T", bound="ProjectTemplateRoleMappingData")


@_attrs_define
class ProjectTemplateRoleMappingData:
    """Serialize the role mapping dictionary returned by get_role_mapping()"""

    additional_properties: dict[str, "ProjectTemplateRoleMappingDataAdditionalProperty"] = _attrs_field(
        init=False, factory=dict
    )

    def to_dict(self) -> dict[str, Any]:
        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.project_template_role_mapping_data_additional_property import (
            ProjectTemplateRoleMappingDataAdditionalProperty,
        )

        d = dict(src_dict)
        project_template_role_mapping_data = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = ProjectTemplateRoleMappingDataAdditionalProperty.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        project_template_role_mapping_data.additional_properties = additional_properties
        return project_template_role_mapping_data

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> "ProjectTemplateRoleMappingDataAdditionalProperty":
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: "ProjectTemplateRoleMappingDataAdditionalProperty") -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
