from typing import Any, Dict, List, Type, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.list_all_dedicated_with_deps_response_200_item_language import (
    ListAllDedicatedWithDepsResponse200ItemLanguage,
)

T = TypeVar("T", bound="ListAllDedicatedWithDepsResponse200Item")


@_attrs_define
class ListAllDedicatedWithDepsResponse200Item:
    """
    Attributes:
        workspace_id (str):
        path (str):
        language (ListAllDedicatedWithDepsResponse200ItemLanguage):
        workspace_dep_names (List[str]):
    """

    workspace_id: str
    path: str
    language: ListAllDedicatedWithDepsResponse200ItemLanguage
    workspace_dep_names: List[str]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        workspace_id = self.workspace_id
        path = self.path
        language = self.language.value

        workspace_dep_names = self.workspace_dep_names

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "workspace_id": workspace_id,
                "path": path,
                "language": language,
                "workspace_dep_names": workspace_dep_names,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        workspace_id = d.pop("workspace_id")

        path = d.pop("path")

        language = ListAllDedicatedWithDepsResponse200ItemLanguage(d.pop("language"))

        workspace_dep_names = cast(List[str], d.pop("workspace_dep_names"))

        list_all_dedicated_with_deps_response_200_item = cls(
            workspace_id=workspace_id,
            path=path,
            language=language,
            workspace_dep_names=workspace_dep_names,
        )

        list_all_dedicated_with_deps_response_200_item.additional_properties = d
        return list_all_dedicated_with_deps_response_200_item

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
