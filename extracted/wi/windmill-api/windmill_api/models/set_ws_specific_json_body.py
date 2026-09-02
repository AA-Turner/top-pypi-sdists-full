from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.set_ws_specific_json_body_item_kind import SetWsSpecificJsonBodyItemKind

T = TypeVar("T", bound="SetWsSpecificJsonBody")


@_attrs_define
class SetWsSpecificJsonBody:
    """
    Attributes:
        item_kind (SetWsSpecificJsonBodyItemKind):
        path (str):
        value (bool):
    """

    item_kind: SetWsSpecificJsonBodyItemKind
    path: str
    value: bool
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        item_kind = self.item_kind.value

        path = self.path
        value = self.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "item_kind": item_kind,
                "path": path,
                "value": value,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        item_kind = SetWsSpecificJsonBodyItemKind(d.pop("item_kind"))

        path = d.pop("path")

        value = d.pop("value")

        set_ws_specific_json_body = cls(
            item_kind=item_kind,
            path=path,
            value=value,
        )

        set_ws_specific_json_body.additional_properties = d
        return set_ws_specific_json_body

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
