from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CompareWorkspacesResponse200Summary")


@_attrs_define
class CompareWorkspacesResponse200Summary:
    """Summary statistics of the comparison

    Attributes:
        total_diffs (int): Total number of items with differences
        total_ahead (int): Total number of ahead changes
        total_behind (int): Total number of behind changes
        scripts_changed (int): Number of scripts with differences
        flows_changed (int): Number of flows with differences
        apps_changed (int): Number of apps with differences
        resources_changed (int): Number of resources with differences
        variables_changed (int): Number of variables with differences
        conflicts (int): Number of items that are both ahead and behind (conflicts)
    """

    total_diffs: int
    total_ahead: int
    total_behind: int
    scripts_changed: int
    flows_changed: int
    apps_changed: int
    resources_changed: int
    variables_changed: int
    conflicts: int
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        total_diffs = self.total_diffs
        total_ahead = self.total_ahead
        total_behind = self.total_behind
        scripts_changed = self.scripts_changed
        flows_changed = self.flows_changed
        apps_changed = self.apps_changed
        resources_changed = self.resources_changed
        variables_changed = self.variables_changed
        conflicts = self.conflicts

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "total_diffs": total_diffs,
                "total_ahead": total_ahead,
                "total_behind": total_behind,
                "scripts_changed": scripts_changed,
                "flows_changed": flows_changed,
                "apps_changed": apps_changed,
                "resources_changed": resources_changed,
                "variables_changed": variables_changed,
                "conflicts": conflicts,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        total_diffs = d.pop("total_diffs")

        total_ahead = d.pop("total_ahead")

        total_behind = d.pop("total_behind")

        scripts_changed = d.pop("scripts_changed")

        flows_changed = d.pop("flows_changed")

        apps_changed = d.pop("apps_changed")

        resources_changed = d.pop("resources_changed")

        variables_changed = d.pop("variables_changed")

        conflicts = d.pop("conflicts")

        compare_workspaces_response_200_summary = cls(
            total_diffs=total_diffs,
            total_ahead=total_ahead,
            total_behind=total_behind,
            scripts_changed=scripts_changed,
            flows_changed=flows_changed,
            apps_changed=apps_changed,
            resources_changed=resources_changed,
            variables_changed=variables_changed,
            conflicts=conflicts,
        )

        compare_workspaces_response_200_summary.additional_properties = d
        return compare_workspaces_response_200_summary

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
