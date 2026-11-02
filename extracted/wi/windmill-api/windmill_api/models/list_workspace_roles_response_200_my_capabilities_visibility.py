from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ListWorkspaceRolesResponse200MyCapabilitiesVisibility")


@_attrs_define
class ListWorkspaceRolesResponse200MyCapabilitiesVisibility:
    """Pages a role sees. Not enforced.

    Attributes:
        runs (bool):
        schedules (bool):
        resources (bool):
        variables (bool):
        assets (bool):
        triggers (bool):
        audit_logs (bool):
        groups (bool):
        folders (bool):
        workers (bool):
    """

    runs: bool
    schedules: bool
    resources: bool
    variables: bool
    assets: bool
    triggers: bool
    audit_logs: bool
    groups: bool
    folders: bool
    workers: bool
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        runs = self.runs
        schedules = self.schedules
        resources = self.resources
        variables = self.variables
        assets = self.assets
        triggers = self.triggers
        audit_logs = self.audit_logs
        groups = self.groups
        folders = self.folders
        workers = self.workers

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "runs": runs,
                "schedules": schedules,
                "resources": resources,
                "variables": variables,
                "assets": assets,
                "triggers": triggers,
                "audit_logs": audit_logs,
                "groups": groups,
                "folders": folders,
                "workers": workers,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        runs = d.pop("runs")

        schedules = d.pop("schedules")

        resources = d.pop("resources")

        variables = d.pop("variables")

        assets = d.pop("assets")

        triggers = d.pop("triggers")

        audit_logs = d.pop("audit_logs")

        groups = d.pop("groups")

        folders = d.pop("folders")

        workers = d.pop("workers")

        list_workspace_roles_response_200_my_capabilities_visibility = cls(
            runs=runs,
            schedules=schedules,
            resources=resources,
            variables=variables,
            assets=assets,
            triggers=triggers,
            audit_logs=audit_logs,
            groups=groups,
            folders=folders,
            workers=workers,
        )

        list_workspace_roles_response_200_my_capabilities_visibility.additional_properties = d
        return list_workspace_roles_response_200_my_capabilities_visibility

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
