from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_workspace_fork_git_branch_json_body_forked_datatables_item import (
        CreateWorkspaceForkGitBranchJsonBodyForkedDatatablesItem,
    )


T = TypeVar("T", bound="CreateWorkspaceForkGitBranchJsonBody")


@_attrs_define
class CreateWorkspaceForkGitBranchJsonBody:
    """
    Attributes:
        id (str):
        name (str):
        color (Union[Unset, str]):
        forked_datatables (Union[Unset, List['CreateWorkspaceForkGitBranchJsonBodyForkedDatatablesItem']]):
    """

    id: str
    name: str
    color: Union[Unset, str] = UNSET
    forked_datatables: Union[Unset, List["CreateWorkspaceForkGitBranchJsonBodyForkedDatatablesItem"]] = UNSET
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

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.create_workspace_fork_git_branch_json_body_forked_datatables_item import (
            CreateWorkspaceForkGitBranchJsonBodyForkedDatatablesItem,
        )

        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        color = d.pop("color", UNSET)

        forked_datatables = []
        _forked_datatables = d.pop("forked_datatables", UNSET)
        for forked_datatables_item_data in _forked_datatables or []:
            forked_datatables_item = CreateWorkspaceForkGitBranchJsonBodyForkedDatatablesItem.from_dict(
                forked_datatables_item_data
            )

            forked_datatables.append(forked_datatables_item)

        create_workspace_fork_git_branch_json_body = cls(
            id=id,
            name=name,
            color=color,
            forked_datatables=forked_datatables,
        )

        create_workspace_fork_git_branch_json_body.additional_properties = d
        return create_workspace_fork_git_branch_json_body

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
