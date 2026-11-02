from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.workspace_roles_roles_item_capabilities_apps import WorkspaceRolesRolesItemCapabilitiesApps
from ..models.workspace_roles_roles_item_capabilities_flows import WorkspaceRolesRolesItemCapabilitiesFlows

if TYPE_CHECKING:
    from ..models.workspace_roles_roles_item_capabilities_visibility import (
        WorkspaceRolesRolesItemCapabilitiesVisibility,
    )


T = TypeVar("T", bound="WorkspaceRolesRolesItemCapabilities")


@_attrs_define
class WorkspaceRolesRolesItemCapabilities:
    """
    Attributes:
        code (bool): Author scripts and run code of one's own (previews, dependency jobs, dynamic selects, resolving
            jobs, data table migrations). Required by `full` flows or apps.
        flows (WorkspaceRolesRolesItemCapabilitiesFlows): How much of a kind of runnable a role may author. `compose`
            assembles already-deployed runnables with no code of one's own.
        apps (WorkspaceRolesRolesItemCapabilitiesApps): How much of a kind of runnable a role may author. `compose`
            assembles already-deployed runnables with no code of one's own.
        manage_schedules (bool):
        manage_triggers (bool):
        fork (bool): Fork the workspace.
        visibility (WorkspaceRolesRolesItemCapabilitiesVisibility): Pages a role sees. Not enforced.
    """

    code: bool
    flows: WorkspaceRolesRolesItemCapabilitiesFlows
    apps: WorkspaceRolesRolesItemCapabilitiesApps
    manage_schedules: bool
    manage_triggers: bool
    fork: bool
    visibility: "WorkspaceRolesRolesItemCapabilitiesVisibility"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        code = self.code
        flows = self.flows.value

        apps = self.apps.value

        manage_schedules = self.manage_schedules
        manage_triggers = self.manage_triggers
        fork = self.fork
        visibility = self.visibility.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "code": code,
                "flows": flows,
                "apps": apps,
                "manage_schedules": manage_schedules,
                "manage_triggers": manage_triggers,
                "fork": fork,
                "visibility": visibility,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.workspace_roles_roles_item_capabilities_visibility import (
            WorkspaceRolesRolesItemCapabilitiesVisibility,
        )

        d = src_dict.copy()
        code = d.pop("code")

        flows = WorkspaceRolesRolesItemCapabilitiesFlows(d.pop("flows"))

        apps = WorkspaceRolesRolesItemCapabilitiesApps(d.pop("apps"))

        manage_schedules = d.pop("manage_schedules")

        manage_triggers = d.pop("manage_triggers")

        fork = d.pop("fork")

        visibility = WorkspaceRolesRolesItemCapabilitiesVisibility.from_dict(d.pop("visibility"))

        workspace_roles_roles_item_capabilities = cls(
            code=code,
            flows=flows,
            apps=apps,
            manage_schedules=manage_schedules,
            manage_triggers=manage_triggers,
            fork=fork,
            visibility=visibility,
        )

        workspace_roles_roles_item_capabilities.additional_properties = d
        return workspace_roles_roles_item_capabilities

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
