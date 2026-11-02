from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.role_definition_capabilities_apps import RoleDefinitionCapabilitiesApps
from ..models.role_definition_capabilities_flows import RoleDefinitionCapabilitiesFlows
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.role_definition_capabilities_visibility import RoleDefinitionCapabilitiesVisibility


T = TypeVar("T", bound="RoleDefinitionCapabilities")


@_attrs_define
class RoleDefinitionCapabilities:
    """A partial RoleCapabilities; an unset key falls through to the layer below.

    Attributes:
        code (Union[Unset, bool]):
        flows (Union[Unset, RoleDefinitionCapabilitiesFlows]): How much of a kind of runnable a role may author.
            `compose` assembles already-deployed runnables with no code of one's own.
        apps (Union[Unset, RoleDefinitionCapabilitiesApps]): How much of a kind of runnable a role may author. `compose`
            assembles already-deployed runnables with no code of one's own.
        manage_schedules (Union[Unset, bool]):
        manage_triggers (Union[Unset, bool]):
        fork (Union[Unset, bool]):
        visibility (Union[Unset, RoleDefinitionCapabilitiesVisibility]):
    """

    code: Union[Unset, bool] = UNSET
    flows: Union[Unset, RoleDefinitionCapabilitiesFlows] = UNSET
    apps: Union[Unset, RoleDefinitionCapabilitiesApps] = UNSET
    manage_schedules: Union[Unset, bool] = UNSET
    manage_triggers: Union[Unset, bool] = UNSET
    fork: Union[Unset, bool] = UNSET
    visibility: Union[Unset, "RoleDefinitionCapabilitiesVisibility"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        code = self.code
        flows: Union[Unset, str] = UNSET
        if not isinstance(self.flows, Unset):
            flows = self.flows.value

        apps: Union[Unset, str] = UNSET
        if not isinstance(self.apps, Unset):
            apps = self.apps.value

        manage_schedules = self.manage_schedules
        manage_triggers = self.manage_triggers
        fork = self.fork
        visibility: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.visibility, Unset):
            visibility = self.visibility.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if code is not UNSET:
            field_dict["code"] = code
        if flows is not UNSET:
            field_dict["flows"] = flows
        if apps is not UNSET:
            field_dict["apps"] = apps
        if manage_schedules is not UNSET:
            field_dict["manage_schedules"] = manage_schedules
        if manage_triggers is not UNSET:
            field_dict["manage_triggers"] = manage_triggers
        if fork is not UNSET:
            field_dict["fork"] = fork
        if visibility is not UNSET:
            field_dict["visibility"] = visibility

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.role_definition_capabilities_visibility import RoleDefinitionCapabilitiesVisibility

        d = src_dict.copy()
        code = d.pop("code", UNSET)

        _flows = d.pop("flows", UNSET)
        flows: Union[Unset, RoleDefinitionCapabilitiesFlows]
        if isinstance(_flows, Unset):
            flows = UNSET
        else:
            flows = RoleDefinitionCapabilitiesFlows(_flows)

        _apps = d.pop("apps", UNSET)
        apps: Union[Unset, RoleDefinitionCapabilitiesApps]
        if isinstance(_apps, Unset):
            apps = UNSET
        else:
            apps = RoleDefinitionCapabilitiesApps(_apps)

        manage_schedules = d.pop("manage_schedules", UNSET)

        manage_triggers = d.pop("manage_triggers", UNSET)

        fork = d.pop("fork", UNSET)

        _visibility = d.pop("visibility", UNSET)
        visibility: Union[Unset, RoleDefinitionCapabilitiesVisibility]
        if isinstance(_visibility, Unset):
            visibility = UNSET
        else:
            visibility = RoleDefinitionCapabilitiesVisibility.from_dict(_visibility)

        role_definition_capabilities = cls(
            code=code,
            flows=flows,
            apps=apps,
            manage_schedules=manage_schedules,
            manage_triggers=manage_triggers,
            fork=fork,
            visibility=visibility,
        )

        role_definition_capabilities.additional_properties = d
        return role_definition_capabilities

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
