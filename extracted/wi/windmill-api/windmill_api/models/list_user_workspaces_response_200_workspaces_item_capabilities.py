from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.list_user_workspaces_response_200_workspaces_item_capabilities_apps import (
    ListUserWorkspacesResponse200WorkspacesItemCapabilitiesApps,
)
from ..models.list_user_workspaces_response_200_workspaces_item_capabilities_flows import (
    ListUserWorkspacesResponse200WorkspacesItemCapabilitiesFlows,
)

if TYPE_CHECKING:
    from ..models.list_user_workspaces_response_200_workspaces_item_capabilities_visibility import (
        ListUserWorkspacesResponse200WorkspacesItemCapabilitiesVisibility,
    )


T = TypeVar("T", bound="ListUserWorkspacesResponse200WorkspacesItemCapabilities")


@_attrs_define
class ListUserWorkspacesResponse200WorkspacesItemCapabilities:
    """
    Attributes:
        code (bool): Author scripts and run code of one's own (previews, dependency jobs, dynamic selects, resolving
            jobs, data table migrations). Required by `full` flows or apps.
        flows (ListUserWorkspacesResponse200WorkspacesItemCapabilitiesFlows): How much of a kind of runnable a role may
            author. `compose` assembles already-deployed runnables with no code of one's own.
        apps (ListUserWorkspacesResponse200WorkspacesItemCapabilitiesApps): How much of a kind of runnable a role may
            author. `compose` assembles already-deployed runnables with no code of one's own.
        manage_schedules (bool):
        manage_triggers (bool):
        fork (bool): Fork the workspace.
        visibility (ListUserWorkspacesResponse200WorkspacesItemCapabilitiesVisibility): Pages a role sees. Not enforced.
    """

    code: bool
    flows: ListUserWorkspacesResponse200WorkspacesItemCapabilitiesFlows
    apps: ListUserWorkspacesResponse200WorkspacesItemCapabilitiesApps
    manage_schedules: bool
    manage_triggers: bool
    fork: bool
    visibility: "ListUserWorkspacesResponse200WorkspacesItemCapabilitiesVisibility"
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
        from ..models.list_user_workspaces_response_200_workspaces_item_capabilities_visibility import (
            ListUserWorkspacesResponse200WorkspacesItemCapabilitiesVisibility,
        )

        d = src_dict.copy()
        code = d.pop("code")

        flows = ListUserWorkspacesResponse200WorkspacesItemCapabilitiesFlows(d.pop("flows"))

        apps = ListUserWorkspacesResponse200WorkspacesItemCapabilitiesApps(d.pop("apps"))

        manage_schedules = d.pop("manage_schedules")

        manage_triggers = d.pop("manage_triggers")

        fork = d.pop("fork")

        visibility = ListUserWorkspacesResponse200WorkspacesItemCapabilitiesVisibility.from_dict(d.pop("visibility"))

        list_user_workspaces_response_200_workspaces_item_capabilities = cls(
            code=code,
            flows=flows,
            apps=apps,
            manage_schedules=manage_schedules,
            manage_triggers=manage_triggers,
            fork=fork,
            visibility=visibility,
        )

        list_user_workspaces_response_200_workspaces_item_capabilities.additional_properties = d
        return list_user_workspaces_response_200_workspaces_item_capabilities

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
