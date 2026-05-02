from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ListAvailableScopesResponse200ItemScopesItem")


@_attrs_define
class ListAvailableScopesResponse200ItemScopesItem:
    """
    Attributes:
        value (str):
        label (str):
        requires_resource_path (bool):
        description (Union[Unset, None, str]):
    """

    value: str
    label: str
    requires_resource_path: bool
    description: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        value = self.value
        label = self.label
        requires_resource_path = self.requires_resource_path
        description = self.description

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "value": value,
                "label": label,
                "requires_resource_path": requires_resource_path,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        value = d.pop("value")

        label = d.pop("label")

        requires_resource_path = d.pop("requires_resource_path")

        description = d.pop("description", UNSET)

        list_available_scopes_response_200_item_scopes_item = cls(
            value=value,
            label=label,
            requires_resource_path=requires_resource_path,
            description=description,
        )

        list_available_scopes_response_200_item_scopes_item.additional_properties = d
        return list_available_scopes_response_200_item_scopes_item

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
