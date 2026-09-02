from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.create_workspace_fork_json_body_dev_workspace_label import CreateWorkspaceForkJsonBodyDevWorkspaceLabel
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_workspace_fork_json_body_forked_datatables_item import (
        CreateWorkspaceForkJsonBodyForkedDatatablesItem,
    )


T = TypeVar("T", bound="CreateWorkspaceForkJsonBody")


@_attrs_define
class CreateWorkspaceForkJsonBody:
    """
    Attributes:
        id (str):
        name (str):
        color (Union[Unset, str]):
        forked_datatables (Union[Unset, List['CreateWorkspaceForkJsonBodyForkedDatatablesItem']]):
        shared_ducklakes (Union[Unset, List[str]]): Lake names the fork SHARES with the parent (reads and writes the
            parent's lake directly). Every lake not listed gets the default isolated fork namespace with read-defer to the
            parent.
        is_dev_workspace (Union[Unset, bool]): Create the fork as a persistent dev workspace (id not required to carry
            the wm-fork- prefix; at most one per parent)
        lock_prod_deploy (Union[Unset, bool]): When creating a dev workspace, lock the parent (prod) against direct
            deployment
        lock_prod_forking (Union[Unset, bool]): When creating a dev workspace, prevent forking the parent (prod)
        copy_members (Union[Unset, bool]): Copy the parent's members (users + group memberships) into the fork so the
            team can work in it
        dev_workspace_label (Union[Unset, CreateWorkspaceForkJsonBodyDevWorkspaceLabel]): Environment label for the dev
            workspace: its badge text and the branch it deploys to. Ignored for non-dev forks. Omitted defaults to 'dev'
    """

    id: str
    name: str
    color: Union[Unset, str] = UNSET
    forked_datatables: Union[Unset, List["CreateWorkspaceForkJsonBodyForkedDatatablesItem"]] = UNSET
    shared_ducklakes: Union[Unset, List[str]] = UNSET
    is_dev_workspace: Union[Unset, bool] = UNSET
    lock_prod_deploy: Union[Unset, bool] = UNSET
    lock_prod_forking: Union[Unset, bool] = UNSET
    copy_members: Union[Unset, bool] = UNSET
    dev_workspace_label: Union[Unset, CreateWorkspaceForkJsonBodyDevWorkspaceLabel] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        color = self.color
        forked_datatables: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.forked_datatables, Unset):
            forked_datatables = []
            for forked_datatables_item_data in self.forked_datatables:
                forked_datatables_item = forked_datatables_item_data.to_dict()

                forked_datatables.append(forked_datatables_item)

        shared_ducklakes: Union[Unset, List[str]] = UNSET
        if not isinstance(self.shared_ducklakes, Unset):
            shared_ducklakes = self.shared_ducklakes

        is_dev_workspace = self.is_dev_workspace
        lock_prod_deploy = self.lock_prod_deploy
        lock_prod_forking = self.lock_prod_forking
        copy_members = self.copy_members
        dev_workspace_label: Union[Unset, str] = UNSET
        if not isinstance(self.dev_workspace_label, Unset):
            dev_workspace_label = self.dev_workspace_label.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
            }
        )
        if color is not UNSET:
            field_dict["color"] = color
        if forked_datatables is not UNSET:
            field_dict["forked_datatables"] = forked_datatables
        if shared_ducklakes is not UNSET:
            field_dict["shared_ducklakes"] = shared_ducklakes
        if is_dev_workspace is not UNSET:
            field_dict["is_dev_workspace"] = is_dev_workspace
        if lock_prod_deploy is not UNSET:
            field_dict["lock_prod_deploy"] = lock_prod_deploy
        if lock_prod_forking is not UNSET:
            field_dict["lock_prod_forking"] = lock_prod_forking
        if copy_members is not UNSET:
            field_dict["copy_members"] = copy_members
        if dev_workspace_label is not UNSET:
            field_dict["dev_workspace_label"] = dev_workspace_label

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.create_workspace_fork_json_body_forked_datatables_item import (
            CreateWorkspaceForkJsonBodyForkedDatatablesItem,
        )

        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        color = d.pop("color", UNSET)

        forked_datatables = []
        _forked_datatables = d.pop("forked_datatables", UNSET)
        for forked_datatables_item_data in _forked_datatables or []:
            forked_datatables_item = CreateWorkspaceForkJsonBodyForkedDatatablesItem.from_dict(
                forked_datatables_item_data
            )

            forked_datatables.append(forked_datatables_item)

        shared_ducklakes = cast(List[str], d.pop("shared_ducklakes", UNSET))

        is_dev_workspace = d.pop("is_dev_workspace", UNSET)

        lock_prod_deploy = d.pop("lock_prod_deploy", UNSET)

        lock_prod_forking = d.pop("lock_prod_forking", UNSET)

        copy_members = d.pop("copy_members", UNSET)

        _dev_workspace_label = d.pop("dev_workspace_label", UNSET)
        dev_workspace_label: Union[Unset, CreateWorkspaceForkJsonBodyDevWorkspaceLabel]
        if isinstance(_dev_workspace_label, Unset):
            dev_workspace_label = UNSET
        else:
            dev_workspace_label = CreateWorkspaceForkJsonBodyDevWorkspaceLabel(_dev_workspace_label)

        create_workspace_fork_json_body = cls(
            id=id,
            name=name,
            color=color,
            forked_datatables=forked_datatables,
            shared_ducklakes=shared_ducklakes,
            is_dev_workspace=is_dev_workspace,
            lock_prod_deploy=lock_prod_deploy,
            lock_prod_forking=lock_prod_forking,
            copy_members=copy_members,
            dev_workspace_label=dev_workspace_label,
        )

        create_workspace_fork_json_body.additional_properties = d
        return create_workspace_fork_json_body

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
