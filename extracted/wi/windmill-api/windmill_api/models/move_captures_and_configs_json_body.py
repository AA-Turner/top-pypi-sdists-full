from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="MoveCapturesAndConfigsJsonBody")


@_attrs_define
class MoveCapturesAndConfigsJsonBody:
    """
    Attributes:
        new_path (Union[Unset, str]):
    """

    new_path: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        new_path = self.new_path

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if new_path is not UNSET:
            field_dict["new_path"] = new_path

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        new_path = d.pop("new_path", UNSET)

        move_captures_and_configs_json_body = cls(
            new_path=new_path,
        )

        move_captures_and_configs_json_body.additional_properties = d
        return move_captures_and_configs_json_body

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
