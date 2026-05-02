from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="EditDefaultScriptsJsonBody")


@_attrs_define
class EditDefaultScriptsJsonBody:
    """
    Attributes:
        order (Union[Unset, List[str]]):
        hidden (Union[Unset, List[str]]):
        default_script_content (Union[Unset, Any]):
    """

    order: Union[Unset, List[str]] = UNSET
    hidden: Union[Unset, List[str]] = UNSET
    default_script_content: Union[Unset, Any] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        order: Union[Unset, List[str]] = UNSET
        if not isinstance(self.order, Unset):
            order = self.order

        hidden: Union[Unset, List[str]] = UNSET
        if not isinstance(self.hidden, Unset):
            hidden = self.hidden

        default_script_content = self.default_script_content

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if order is not UNSET:
            field_dict["order"] = order
        if hidden is not UNSET:
            field_dict["hidden"] = hidden
        if default_script_content is not UNSET:
            field_dict["default_script_content"] = default_script_content

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        order = cast(List[str], d.pop("order", UNSET))

        hidden = cast(List[str], d.pop("hidden", UNSET))

        default_script_content = d.pop("default_script_content", UNSET)

        edit_default_scripts_json_body = cls(
            order=order,
            hidden=hidden,
            default_script_content=default_script_content,
        )

        edit_default_scripts_json_body.additional_properties = d
        return edit_default_scripts_json_body

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
