from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ChangeWorkspaceIdJsonBody")


@_attrs_define
class ChangeWorkspaceIdJsonBody:
    """
    Attributes:
        new_id (Union[Unset, str]):
        new_name (Union[Unset, str]):
    """

    new_id: Union[Unset, str] = UNSET
    new_name: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        new_id = self.new_id
        new_name = self.new_name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if new_id is not UNSET:
            field_dict["new_id"] = new_id
        if new_name is not UNSET:
            field_dict["new_name"] = new_name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        new_id = d.pop("new_id", UNSET)

        new_name = d.pop("new_name", UNSET)

        change_workspace_id_json_body = cls(
            new_id=new_id,
            new_name=new_name,
        )

        change_workspace_id_json_body.additional_properties = d
        return change_workspace_id_json_body

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
