from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.list_all_workspace_dependencies_response_200_item_language import (
    ListAllWorkspaceDependenciesResponse200ItemLanguage,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="ListAllWorkspaceDependenciesResponse200Item")


@_attrs_define
class ListAllWorkspaceDependenciesResponse200Item:
    """
    Attributes:
        workspace_id (str):
        language (ListAllWorkspaceDependenciesResponse200ItemLanguage):
        name (Union[Unset, str]):
    """

    workspace_id: str
    language: ListAllWorkspaceDependenciesResponse200ItemLanguage
    name: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        workspace_id = self.workspace_id
        language = self.language.value

        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "workspace_id": workspace_id,
                "language": language,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        workspace_id = d.pop("workspace_id")

        language = ListAllWorkspaceDependenciesResponse200ItemLanguage(d.pop("language"))

        name = d.pop("name", UNSET)

        list_all_workspace_dependencies_response_200_item = cls(
            workspace_id=workspace_id,
            language=language,
            name=name,
        )

        list_all_workspace_dependencies_response_200_item.additional_properties = d
        return list_all_workspace_dependencies_response_200_item

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
