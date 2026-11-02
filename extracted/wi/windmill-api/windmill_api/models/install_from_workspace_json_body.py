from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="InstallFromWorkspaceJsonBody")


@_attrs_define
class InstallFromWorkspaceJsonBody:
    """
    Attributes:
        source_workspace_id (str): The ID of the workspace containing the installation to copy
        installation_id (float): The ID of the GitHub installation to copy
    """

    source_workspace_id: str
    installation_id: float
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        source_workspace_id = self.source_workspace_id
        installation_id = self.installation_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "source_workspace_id": source_workspace_id,
                "installation_id": installation_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        source_workspace_id = d.pop("source_workspace_id")

        installation_id = d.pop("installation_id")

        install_from_workspace_json_body = cls(
            source_workspace_id=source_workspace_id,
            installation_id=installation_id,
        )

        install_from_workspace_json_body.additional_properties = d
        return install_from_workspace_json_body

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
