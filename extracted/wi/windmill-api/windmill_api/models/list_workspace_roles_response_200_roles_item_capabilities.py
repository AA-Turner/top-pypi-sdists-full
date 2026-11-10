from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.list_workspace_roles_response_200_roles_item_capabilities_apps import (
    ListWorkspaceRolesResponse200RolesItemCapabilitiesApps,
)
from ..models.list_workspace_roles_response_200_roles_item_capabilities_flows import (
    ListWorkspaceRolesResponse200RolesItemCapabilitiesFlows,
)

if TYPE_CHECKING:
    from ..models.list_workspace_roles_response_200_roles_item_capabilities_visibility import (
        ListWorkspaceRolesResponse200RolesItemCapabilitiesVisibility,
    )


T = TypeVar("T", bound="ListWorkspaceRolesResponse200RolesItemCapabilities")


@_attrs_define
class ListWorkspaceRolesResponse200RolesItemCapabilities:
    """
    Attributes:
        code (bool): Author scripts and run code of one's own (previews, dependency jobs, dynamic selects, resolving
            jobs, data table migrations). Required by `full` flows or apps. Previews also need `run`.
        flows (ListWorkspaceRolesResponse200RolesItemCapabilitiesFlows): How much of a kind of runnable a role may
            author. `compose` assembles already-deployed runnables with no code of one's own.
        apps (ListWorkspaceRolesResponse200RolesItemCapabilitiesApps): How much of a kind of runnable a role may author.
            `compose` assembles already-deployed runnables with no code of one's own.
        manage_schedules (bool):
        manage_triggers (bool):
        run (bool): Start runs of scripts, flows and AI agents (by path, hash or version, restarts, previews, MCP run
            tools). Without it a role is view-only. Schedules and triggers keep their own rights; resuming a suspended step
            is not a run.
        fork (bool): Fork the workspace.
        visibility (ListWorkspaceRolesResponse200RolesItemCapabilitiesVisibility): Pages a role sees. Not enforced.
    """

    code: bool
    flows: ListWorkspaceRolesResponse200RolesItemCapabilitiesFlows
    apps: ListWorkspaceRolesResponse200RolesItemCapabilitiesApps
    manage_schedules: bool
    manage_triggers: bool
    run: bool
    fork: bool
    visibility: "ListWorkspaceRolesResponse200RolesItemCapabilitiesVisibility"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        code = self.code
        flows = self.flows.value

        apps = self.apps.value

        manage_schedules = self.manage_schedules
        manage_triggers = self.manage_triggers
        run = self.run
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
                "run": run,
                "fork": fork,
                "visibility": visibility,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_workspace_roles_response_200_roles_item_capabilities_visibility import (
            ListWorkspaceRolesResponse200RolesItemCapabilitiesVisibility,
        )

        d = src_dict.copy()
        code = d.pop("code")

        flows = ListWorkspaceRolesResponse200RolesItemCapabilitiesFlows(d.pop("flows"))

        apps = ListWorkspaceRolesResponse200RolesItemCapabilitiesApps(d.pop("apps"))

        manage_schedules = d.pop("manage_schedules")

        manage_triggers = d.pop("manage_triggers")

        run = d.pop("run")

        fork = d.pop("fork")

        visibility = ListWorkspaceRolesResponse200RolesItemCapabilitiesVisibility.from_dict(d.pop("visibility"))

        list_workspace_roles_response_200_roles_item_capabilities = cls(
            code=code,
            flows=flows,
            apps=apps,
            manage_schedules=manage_schedules,
            manage_triggers=manage_triggers,
            run=run,
            fork=fork,
            visibility=visibility,
        )

        list_workspace_roles_response_200_roles_item_capabilities.additional_properties = d
        return list_workspace_roles_response_200_roles_item_capabilities

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
