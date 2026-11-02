from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.workspace_roles_my_capabilities import WorkspaceRolesMyCapabilities
    from ..models.workspace_roles_overrides import WorkspaceRolesOverrides
    from ..models.workspace_roles_roles_item import WorkspaceRolesRolesItem


T = TypeVar("T", bound="WorkspaceRoles")


@_attrs_define
class WorkspaceRoles:
    """
    Attributes:
        roles (List['WorkspaceRolesRolesItem']):
        overrides (WorkspaceRolesOverrides): A workspace's overrides keyed by role name; a name the instance does not
            define adds a workspace-only role (EE).
        custom_roles_enabled (bool): Whether this workspace may add roles of its own.
        my_capabilities (WorkspaceRolesMyCapabilities):
        my_role (Union[Unset, None, str]):
    """

    roles: List["WorkspaceRolesRolesItem"]
    overrides: "WorkspaceRolesOverrides"
    custom_roles_enabled: bool
    my_capabilities: "WorkspaceRolesMyCapabilities"
    my_role: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        roles = []
        for roles_item_data in self.roles:
            roles_item = roles_item_data.to_dict()

            roles.append(roles_item)

        overrides = self.overrides.to_dict()

        custom_roles_enabled = self.custom_roles_enabled
        my_capabilities = self.my_capabilities.to_dict()

        my_role = self.my_role

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "roles": roles,
                "overrides": overrides,
                "custom_roles_enabled": custom_roles_enabled,
                "my_capabilities": my_capabilities,
            }
        )
        if my_role is not UNSET:
            field_dict["my_role"] = my_role

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.workspace_roles_my_capabilities import WorkspaceRolesMyCapabilities
        from ..models.workspace_roles_overrides import WorkspaceRolesOverrides
        from ..models.workspace_roles_roles_item import WorkspaceRolesRolesItem

        d = src_dict.copy()
        roles = []
        _roles = d.pop("roles")
        for roles_item_data in _roles:
            roles_item = WorkspaceRolesRolesItem.from_dict(roles_item_data)

            roles.append(roles_item)

        overrides = WorkspaceRolesOverrides.from_dict(d.pop("overrides"))

        custom_roles_enabled = d.pop("custom_roles_enabled")

        my_capabilities = WorkspaceRolesMyCapabilities.from_dict(d.pop("my_capabilities"))

        my_role = d.pop("my_role", UNSET)

        workspace_roles = cls(
            roles=roles,
            overrides=overrides,
            custom_roles_enabled=custom_roles_enabled,
            my_capabilities=my_capabilities,
            my_role=my_role,
        )

        workspace_roles.additional_properties = d
        return workspace_roles

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
