from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.list_data_tables_response_200_item_resource_type import ListDataTablesResponse200ItemResourceType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ListDataTablesResponse200Item")


@_attrs_define
class ListDataTablesResponse200Item:
    """
    Attributes:
        name (str):
        resource_type (ListDataTablesResponse200ItemResourceType):
        resource_path (str):
        permissioned (bool):
        governing_workspace_id (Union[Unset, str]):
    """

    name: str
    resource_type: ListDataTablesResponse200ItemResourceType
    resource_path: str
    permissioned: bool
    governing_workspace_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        resource_type = self.resource_type.value

        resource_path = self.resource_path
        permissioned = self.permissioned
        governing_workspace_id = self.governing_workspace_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "resource_type": resource_type,
                "resource_path": resource_path,
                "permissioned": permissioned,
            }
        )
        if governing_workspace_id is not UNSET:
            field_dict["governing_workspace_id"] = governing_workspace_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        resource_type = ListDataTablesResponse200ItemResourceType(d.pop("resource_type"))

        resource_path = d.pop("resource_path")

        permissioned = d.pop("permissioned")

        governing_workspace_id = d.pop("governing_workspace_id", UNSET)

        list_data_tables_response_200_item = cls(
            name=name,
            resource_type=resource_type,
            resource_path=resource_path,
            permissioned=permissioned,
            governing_workspace_id=governing_workspace_id,
        )

        list_data_tables_response_200_item.additional_properties = d
        return list_data_tables_response_200_item

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
