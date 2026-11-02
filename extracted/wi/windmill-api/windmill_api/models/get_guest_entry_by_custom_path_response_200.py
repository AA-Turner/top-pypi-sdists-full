from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="GetGuestEntryByCustomPathResponse200")


@_attrs_define
class GetGuestEntryByCustomPathResponse200:
    """What a signed-out visitor needs to start a guest sign-in.

    Attributes:
        workspace_id (str):
        app_path (str):
    """

    workspace_id: str
    app_path: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        workspace_id = self.workspace_id
        app_path = self.app_path

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "workspace_id": workspace_id,
                "app_path": app_path,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        workspace_id = d.pop("workspace_id")

        app_path = d.pop("app_path")

        get_guest_entry_by_custom_path_response_200 = cls(
            workspace_id=workspace_id,
            app_path=app_path,
        )

        get_guest_entry_by_custom_path_response_200.additional_properties = d
        return get_guest_entry_by_custom_path_response_200

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
