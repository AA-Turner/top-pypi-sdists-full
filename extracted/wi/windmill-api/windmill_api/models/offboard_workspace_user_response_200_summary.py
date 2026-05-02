from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="OffboardWorkspaceUserResponse200Summary")


@_attrs_define
class OffboardWorkspaceUserResponse200Summary:
    """
    Attributes:
        scripts_reassigned (int):
        flows_reassigned (int):
        apps_reassigned (int):
        resources_reassigned (int):
        variables_reassigned (int):
        schedules_reassigned (int):
        triggers_reassigned (int):
        drafts_deleted (int):
    """

    scripts_reassigned: int
    flows_reassigned: int
    apps_reassigned: int
    resources_reassigned: int
    variables_reassigned: int
    schedules_reassigned: int
    triggers_reassigned: int
    drafts_deleted: int
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        scripts_reassigned = self.scripts_reassigned
        flows_reassigned = self.flows_reassigned
        apps_reassigned = self.apps_reassigned
        resources_reassigned = self.resources_reassigned
        variables_reassigned = self.variables_reassigned
        schedules_reassigned = self.schedules_reassigned
        triggers_reassigned = self.triggers_reassigned
        drafts_deleted = self.drafts_deleted

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "scripts_reassigned": scripts_reassigned,
                "flows_reassigned": flows_reassigned,
                "apps_reassigned": apps_reassigned,
                "resources_reassigned": resources_reassigned,
                "variables_reassigned": variables_reassigned,
                "schedules_reassigned": schedules_reassigned,
                "triggers_reassigned": triggers_reassigned,
                "drafts_deleted": drafts_deleted,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        scripts_reassigned = d.pop("scripts_reassigned")

        flows_reassigned = d.pop("flows_reassigned")

        apps_reassigned = d.pop("apps_reassigned")

        resources_reassigned = d.pop("resources_reassigned")

        variables_reassigned = d.pop("variables_reassigned")

        schedules_reassigned = d.pop("schedules_reassigned")

        triggers_reassigned = d.pop("triggers_reassigned")

        drafts_deleted = d.pop("drafts_deleted")

        offboard_workspace_user_response_200_summary = cls(
            scripts_reassigned=scripts_reassigned,
            flows_reassigned=flows_reassigned,
            apps_reassigned=apps_reassigned,
            resources_reassigned=resources_reassigned,
            variables_reassigned=variables_reassigned,
            schedules_reassigned=schedules_reassigned,
            triggers_reassigned=triggers_reassigned,
            drafts_deleted=drafts_deleted,
        )

        offboard_workspace_user_response_200_summary.additional_properties = d
        return offboard_workspace_user_response_200_summary

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
