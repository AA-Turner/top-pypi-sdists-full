from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.principal_access_items_item_reasons_item import PrincipalAccessItemsItemReasonsItem


T = TypeVar("T", bound="PrincipalAccessItemsItem")


@_attrs_define
class PrincipalAccessItemsItem:
    """
    Attributes:
        kind (str):
        path (str):
        write (bool):
        reasons (List['PrincipalAccessItemsItemReasonsItem']):
    """

    kind: str
    path: str
    write: bool
    reasons: List["PrincipalAccessItemsItemReasonsItem"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        kind = self.kind
        path = self.path
        write = self.write
        reasons = []
        for reasons_item_data in self.reasons:
            reasons_item = reasons_item_data.to_dict()

            reasons.append(reasons_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "kind": kind,
                "path": path,
                "write": write,
                "reasons": reasons,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.principal_access_items_item_reasons_item import PrincipalAccessItemsItemReasonsItem

        d = src_dict.copy()
        kind = d.pop("kind")

        path = d.pop("path")

        write = d.pop("write")

        reasons = []
        _reasons = d.pop("reasons")
        for reasons_item_data in _reasons:
            reasons_item = PrincipalAccessItemsItemReasonsItem.from_dict(reasons_item_data)

            reasons.append(reasons_item)

        principal_access_items_item = cls(
            kind=kind,
            path=path,
            write=write,
            reasons=reasons,
        )

        principal_access_items_item.additional_properties = d
        return principal_access_items_item

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
