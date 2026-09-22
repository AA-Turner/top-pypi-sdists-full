from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.datatable_permissions_available_roles_item import DatatablePermissionsAvailableRolesItem
    from ..models.datatable_permissions_clone_of import DatatablePermissionsCloneOf
    from ..models.datatable_permissions_roles_item import DatatablePermissionsRolesItem
    from ..models.datatable_permissions_ungoverned_reachers_item import DatatablePermissionsUngovernedReachersItem


T = TypeVar("T", bound="DatatablePermissions")


@_attrs_define
class DatatablePermissions:
    """
    Attributes:
        supported (bool): Whether this data table can be put under roles at all. Only one backed by the instance
            database can: a role is a login on that cluster.
        permissioned (bool):
        default_role (str):
        roles (List['DatatablePermissionsRolesItem']):
        editable (bool):
        available_roles (List['DatatablePermissionsAvailableRolesItem']):
        governing_workspace_id (Union[Unset, str]):
        clone_of (Union[Unset, DatatablePermissionsCloneOf]): for a clone, the data table whose roles it takes
        ungoverned_reachers (Union[Unset, List['DatatablePermissionsUngovernedReachersItem']]):
    """

    supported: bool
    permissioned: bool
    default_role: str
    roles: List["DatatablePermissionsRolesItem"]
    editable: bool
    available_roles: List["DatatablePermissionsAvailableRolesItem"]
    governing_workspace_id: Union[Unset, str] = UNSET
    clone_of: Union[Unset, "DatatablePermissionsCloneOf"] = UNSET
    ungoverned_reachers: Union[Unset, List["DatatablePermissionsUngovernedReachersItem"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        supported = self.supported
        permissioned = self.permissioned
        default_role = self.default_role
        roles = []
        for roles_item_data in self.roles:
            roles_item = roles_item_data.to_dict()

            roles.append(roles_item)

        editable = self.editable
        available_roles = []
        for available_roles_item_data in self.available_roles:
            available_roles_item = available_roles_item_data.to_dict()

            available_roles.append(available_roles_item)

        governing_workspace_id = self.governing_workspace_id
        clone_of: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.clone_of, Unset):
            clone_of = self.clone_of.to_dict()

        ungoverned_reachers: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.ungoverned_reachers, Unset):
            ungoverned_reachers = []
            for ungoverned_reachers_item_data in self.ungoverned_reachers:
                ungoverned_reachers_item = ungoverned_reachers_item_data.to_dict()

                ungoverned_reachers.append(ungoverned_reachers_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "supported": supported,
                "permissioned": permissioned,
                "default_role": default_role,
                "roles": roles,
                "editable": editable,
                "available_roles": available_roles,
            }
        )
        if governing_workspace_id is not UNSET:
            field_dict["governing_workspace_id"] = governing_workspace_id
        if clone_of is not UNSET:
            field_dict["clone_of"] = clone_of
        if ungoverned_reachers is not UNSET:
            field_dict["ungoverned_reachers"] = ungoverned_reachers

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.datatable_permissions_available_roles_item import DatatablePermissionsAvailableRolesItem
        from ..models.datatable_permissions_clone_of import DatatablePermissionsCloneOf
        from ..models.datatable_permissions_roles_item import DatatablePermissionsRolesItem
        from ..models.datatable_permissions_ungoverned_reachers_item import DatatablePermissionsUngovernedReachersItem

        d = src_dict.copy()
        supported = d.pop("supported")

        permissioned = d.pop("permissioned")

        default_role = d.pop("default_role")

        roles = []
        _roles = d.pop("roles")
        for roles_item_data in _roles:
            roles_item = DatatablePermissionsRolesItem.from_dict(roles_item_data)

            roles.append(roles_item)

        editable = d.pop("editable")

        available_roles = []
        _available_roles = d.pop("available_roles")
        for available_roles_item_data in _available_roles:
            available_roles_item = DatatablePermissionsAvailableRolesItem.from_dict(available_roles_item_data)

            available_roles.append(available_roles_item)

        governing_workspace_id = d.pop("governing_workspace_id", UNSET)

        _clone_of = d.pop("clone_of", UNSET)
        clone_of: Union[Unset, DatatablePermissionsCloneOf]
        if isinstance(_clone_of, Unset):
            clone_of = UNSET
        else:
            clone_of = DatatablePermissionsCloneOf.from_dict(_clone_of)

        ungoverned_reachers = []
        _ungoverned_reachers = d.pop("ungoverned_reachers", UNSET)
        for ungoverned_reachers_item_data in _ungoverned_reachers or []:
            ungoverned_reachers_item = DatatablePermissionsUngovernedReachersItem.from_dict(
                ungoverned_reachers_item_data
            )

            ungoverned_reachers.append(ungoverned_reachers_item)

        datatable_permissions = cls(
            supported=supported,
            permissioned=permissioned,
            default_role=default_role,
            roles=roles,
            editable=editable,
            available_roles=available_roles,
            governing_workspace_id=governing_workspace_id,
            clone_of=clone_of,
            ungoverned_reachers=ungoverned_reachers,
        )

        datatable_permissions.additional_properties = d
        return datatable_permissions

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
