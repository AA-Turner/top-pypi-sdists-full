from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetDependencyMapResponse200Item")


@_attrs_define
class GetDependencyMapResponse200Item:
    """
    Attributes:
        workspace_id (Union[Unset, None, str]):
        importer_path (Union[Unset, None, str]):
        importer_kind (Union[Unset, None, str]):
        imported_path (Union[Unset, None, str]):
        importer_node_id (Union[Unset, None, str]):
    """

    workspace_id: Union[Unset, None, str] = UNSET
    importer_path: Union[Unset, None, str] = UNSET
    importer_kind: Union[Unset, None, str] = UNSET
    imported_path: Union[Unset, None, str] = UNSET
    importer_node_id: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        workspace_id = self.workspace_id
        importer_path = self.importer_path
        importer_kind = self.importer_kind
        imported_path = self.imported_path
        importer_node_id = self.importer_node_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if workspace_id is not UNSET:
            field_dict["workspace_id"] = workspace_id
        if importer_path is not UNSET:
            field_dict["importer_path"] = importer_path
        if importer_kind is not UNSET:
            field_dict["importer_kind"] = importer_kind
        if imported_path is not UNSET:
            field_dict["imported_path"] = imported_path
        if importer_node_id is not UNSET:
            field_dict["importer_node_id"] = importer_node_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        workspace_id = d.pop("workspace_id", UNSET)

        importer_path = d.pop("importer_path", UNSET)

        importer_kind = d.pop("importer_kind", UNSET)

        imported_path = d.pop("imported_path", UNSET)

        importer_node_id = d.pop("importer_node_id", UNSET)

        get_dependency_map_response_200_item = cls(
            workspace_id=workspace_id,
            importer_path=importer_path,
            importer_kind=importer_kind,
            imported_path=imported_path,
            importer_node_id=importer_node_id,
        )

        get_dependency_map_response_200_item.additional_properties = d
        return get_dependency_map_response_200_item

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
