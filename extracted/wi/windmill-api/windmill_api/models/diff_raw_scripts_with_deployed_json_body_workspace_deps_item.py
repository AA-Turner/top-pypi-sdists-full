from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.diff_raw_scripts_with_deployed_json_body_workspace_deps_item_language import (
    DiffRawScriptsWithDeployedJsonBodyWorkspaceDepsItemLanguage,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="DiffRawScriptsWithDeployedJsonBodyWorkspaceDepsItem")


@_attrs_define
class DiffRawScriptsWithDeployedJsonBodyWorkspaceDepsItem:
    """
    Attributes:
        path (str): CLI path (e.g. dependencies/package.json)
        language (DiffRawScriptsWithDeployedJsonBodyWorkspaceDepsItemLanguage):
        hash_ (str): SHA256 content hash
        name (Union[Unset, str]): named workspace dependency (null for default)
    """

    path: str
    language: DiffRawScriptsWithDeployedJsonBodyWorkspaceDepsItemLanguage
    hash_: str
    name: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        path = self.path
        language = self.language.value

        hash_ = self.hash_
        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "path": path,
                "language": language,
                "hash": hash_,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        path = d.pop("path")

        language = DiffRawScriptsWithDeployedJsonBodyWorkspaceDepsItemLanguage(d.pop("language"))

        hash_ = d.pop("hash")

        name = d.pop("name", UNSET)

        diff_raw_scripts_with_deployed_json_body_workspace_deps_item = cls(
            path=path,
            language=language,
            hash_=hash_,
            name=name,
        )

        diff_raw_scripts_with_deployed_json_body_workspace_deps_item.additional_properties = d
        return diff_raw_scripts_with_deployed_json_body_workspace_deps_item

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
