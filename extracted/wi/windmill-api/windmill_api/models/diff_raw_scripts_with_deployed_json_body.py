from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.diff_raw_scripts_with_deployed_json_body_scripts import DiffRawScriptsWithDeployedJsonBodyScripts
    from ..models.diff_raw_scripts_with_deployed_json_body_workspace_deps_item import (
        DiffRawScriptsWithDeployedJsonBodyWorkspaceDepsItem,
    )


T = TypeVar("T", bound="DiffRawScriptsWithDeployedJsonBody")


@_attrs_define
class DiffRawScriptsWithDeployedJsonBody:
    """
    Attributes:
        scripts (DiffRawScriptsWithDeployedJsonBodyScripts): map of script path to SHA256 content hash
        workspace_deps (Union[Unset, List['DiffRawScriptsWithDeployedJsonBodyWorkspaceDepsItem']]): workspace
            dependencies to diff
    """

    scripts: "DiffRawScriptsWithDeployedJsonBodyScripts"
    workspace_deps: Union[Unset, List["DiffRawScriptsWithDeployedJsonBodyWorkspaceDepsItem"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        scripts = self.scripts.to_dict()

        workspace_deps: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.workspace_deps, Unset):
            workspace_deps = []
            for workspace_deps_item_data in self.workspace_deps:
                workspace_deps_item = workspace_deps_item_data.to_dict()

                workspace_deps.append(workspace_deps_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "scripts": scripts,
            }
        )
        if workspace_deps is not UNSET:
            field_dict["workspace_deps"] = workspace_deps

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.diff_raw_scripts_with_deployed_json_body_scripts import DiffRawScriptsWithDeployedJsonBodyScripts
        from ..models.diff_raw_scripts_with_deployed_json_body_workspace_deps_item import (
            DiffRawScriptsWithDeployedJsonBodyWorkspaceDepsItem,
        )

        d = src_dict.copy()
        scripts = DiffRawScriptsWithDeployedJsonBodyScripts.from_dict(d.pop("scripts"))

        workspace_deps = []
        _workspace_deps = d.pop("workspace_deps", UNSET)
        for workspace_deps_item_data in _workspace_deps or []:
            workspace_deps_item = DiffRawScriptsWithDeployedJsonBodyWorkspaceDepsItem.from_dict(
                workspace_deps_item_data
            )

            workspace_deps.append(workspace_deps_item)

        diff_raw_scripts_with_deployed_json_body = cls(
            scripts=scripts,
            workspace_deps=workspace_deps,
        )

        diff_raw_scripts_with_deployed_json_body.additional_properties = d
        return diff_raw_scripts_with_deployed_json_body

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
