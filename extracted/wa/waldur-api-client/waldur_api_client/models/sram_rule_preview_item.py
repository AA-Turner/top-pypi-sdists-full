from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.sram_group import SramGroup
    from ..models.sram_rule_preview_project import SramRulePreviewProject
    from ..models.sram_rule_preview_user import SramRulePreviewUser


T = TypeVar("T", bound="SramRulePreviewItem")


@_attrs_define
class SramRulePreviewItem:
    """
    Attributes:
        group (SramGroup):
        projects (list['SramRulePreviewProject']):
        users (list['SramRulePreviewUser']):
    """

    group: "SramGroup"
    projects: list["SramRulePreviewProject"]
    users: list["SramRulePreviewUser"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        group = self.group.to_dict()

        projects = []
        for projects_item_data in self.projects:
            projects_item = projects_item_data.to_dict()
            projects.append(projects_item)

        users = []
        for users_item_data in self.users:
            users_item = users_item_data.to_dict()
            users.append(users_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "group": group,
                "projects": projects,
                "users": users,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.sram_group import SramGroup
        from ..models.sram_rule_preview_project import SramRulePreviewProject
        from ..models.sram_rule_preview_user import SramRulePreviewUser

        d = dict(src_dict)
        group = SramGroup.from_dict(d.pop("group"))

        projects = []
        _projects = d.pop("projects")
        for projects_item_data in _projects:
            projects_item = SramRulePreviewProject.from_dict(projects_item_data)

            projects.append(projects_item)

        users = []
        _users = d.pop("users")
        for users_item_data in _users:
            users_item = SramRulePreviewUser.from_dict(users_item_data)

            users.append(users_item)

        sram_rule_preview_item = cls(
            group=group,
            projects=projects,
            users=users,
        )

        sram_rule_preview_item.additional_properties = d
        return sram_rule_preview_item

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
