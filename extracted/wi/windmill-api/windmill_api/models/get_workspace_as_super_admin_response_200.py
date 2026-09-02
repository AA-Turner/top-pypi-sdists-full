from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetWorkspaceAsSuperAdminResponse200")


@_attrs_define
class GetWorkspaceAsSuperAdminResponse200:
    """
    Attributes:
        id (str):
        name (str):
        owner (str):
        domain (Union[Unset, str]):
        color (Union[Unset, str]):
        parent_workspace_id (Union[Unset, None, str]):
        deleted (Union[Unset, bool]): Archived (soft-deleted) workspace
        is_dev_workspace (Union[Unset, bool]):
        dev_workspace_label (Union[Unset, None, str]): Environment label of the dev workspace, e.g. 'dev' or 'staging';
            null defaults to 'dev'
    """

    id: str
    name: str
    owner: str
    domain: Union[Unset, str] = UNSET
    color: Union[Unset, str] = UNSET
    parent_workspace_id: Union[Unset, None, str] = UNSET
    deleted: Union[Unset, bool] = UNSET
    is_dev_workspace: Union[Unset, bool] = UNSET
    dev_workspace_label: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        owner = self.owner
        domain = self.domain
        color = self.color
        parent_workspace_id = self.parent_workspace_id
        deleted = self.deleted
        is_dev_workspace = self.is_dev_workspace
        dev_workspace_label = self.dev_workspace_label

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "owner": owner,
            }
        )
        if domain is not UNSET:
            field_dict["domain"] = domain
        if color is not UNSET:
            field_dict["color"] = color
        if parent_workspace_id is not UNSET:
            field_dict["parent_workspace_id"] = parent_workspace_id
        if deleted is not UNSET:
            field_dict["deleted"] = deleted
        if is_dev_workspace is not UNSET:
            field_dict["is_dev_workspace"] = is_dev_workspace
        if dev_workspace_label is not UNSET:
            field_dict["dev_workspace_label"] = dev_workspace_label

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        owner = d.pop("owner")

        domain = d.pop("domain", UNSET)

        color = d.pop("color", UNSET)

        parent_workspace_id = d.pop("parent_workspace_id", UNSET)

        deleted = d.pop("deleted", UNSET)

        is_dev_workspace = d.pop("is_dev_workspace", UNSET)

        dev_workspace_label = d.pop("dev_workspace_label", UNSET)

        get_workspace_as_super_admin_response_200 = cls(
            id=id,
            name=name,
            owner=owner,
            domain=domain,
            color=color,
            parent_workspace_id=parent_workspace_id,
            deleted=deleted,
            is_dev_workspace=is_dev_workspace,
            dev_workspace_label=dev_workspace_label,
        )

        get_workspace_as_super_admin_response_200.additional_properties = d
        return get_workspace_as_super_admin_response_200

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
