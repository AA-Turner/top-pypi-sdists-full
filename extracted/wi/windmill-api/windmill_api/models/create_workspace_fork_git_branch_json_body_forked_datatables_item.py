from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CreateWorkspaceForkGitBranchJsonBodyForkedDatatablesItem")


@_attrs_define
class CreateWorkspaceForkGitBranchJsonBodyForkedDatatablesItem:
    """
    Attributes:
        name (str): Datatable name
        new_dbname (str): New database name for the fork
    """

    name: str
    new_dbname: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        new_dbname = self.new_dbname

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "new_dbname": new_dbname,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        new_dbname = d.pop("new_dbname")

        create_workspace_fork_git_branch_json_body_forked_datatables_item = cls(
            name=name,
            new_dbname=new_dbname,
        )

        create_workspace_fork_git_branch_json_body_forked_datatables_item.additional_properties = d
        return create_workspace_fork_git_branch_json_body_forked_datatables_item

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
