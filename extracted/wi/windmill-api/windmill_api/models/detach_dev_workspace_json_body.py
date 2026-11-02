from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="DetachDevWorkspaceJsonBody")


@_attrs_define
class DetachDevWorkspaceJsonBody:
    """
    Attributes:
        dev_workspace_id (str):
    """

    dev_workspace_id: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        dev_workspace_id = self.dev_workspace_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "dev_workspace_id": dev_workspace_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        dev_workspace_id = d.pop("dev_workspace_id")

        detach_dev_workspace_json_body = cls(
            dev_workspace_id=dev_workspace_id,
        )

        detach_dev_workspace_json_body.additional_properties = d
        return detach_dev_workspace_json_body

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
