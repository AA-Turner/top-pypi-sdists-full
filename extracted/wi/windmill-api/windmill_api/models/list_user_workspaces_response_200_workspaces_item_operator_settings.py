from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ListUserWorkspacesResponse200WorkspacesItemOperatorSettings")


@_attrs_define
class ListUserWorkspacesResponse200WorkspacesItemOperatorSettings:
    """
    Attributes:
        runs (bool): Whether operators can view runs
        schedules (bool): Whether operators can view schedules
        resources (bool): Whether operators can view resources
        variables (bool): Whether operators can view variables
        assets (bool): Whether operators can view assets
        audit_logs (bool): Whether operators can view audit logs
        triggers (bool): Whether operators can view triggers
        groups (bool): Whether operators can view groups page
        folders (bool): Whether operators can view folders page
        workers (bool): Whether operators can view workers page
    """

    runs: bool
    schedules: bool
    resources: bool
    variables: bool
    assets: bool
    audit_logs: bool
    triggers: bool
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
        audit_logs = self.audit_logs
        triggers = self.triggers
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
                "audit_logs": audit_logs,
                "triggers": triggers,
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

        audit_logs = d.pop("audit_logs")

        triggers = d.pop("triggers")

        groups = d.pop("groups")

        folders = d.pop("folders")

        workers = d.pop("workers")

        list_user_workspaces_response_200_workspaces_item_operator_settings = cls(
            runs=runs,
            schedules=schedules,
            resources=resources,
            variables=variables,
            assets=assets,
            audit_logs=audit_logs,
            triggers=triggers,
            groups=groups,
            folders=folders,
            workers=workers,
        )

        list_user_workspaces_response_200_workspaces_item_operator_settings.additional_properties = d
        return list_user_workspaces_response_200_workspaces_item_operator_settings

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
