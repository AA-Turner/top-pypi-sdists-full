from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.list_available_scopes_response_200_item_scopes_item import (
        ListAvailableScopesResponse200ItemScopesItem,
    )


T = TypeVar("T", bound="ListAvailableScopesResponse200Item")


@_attrs_define
class ListAvailableScopesResponse200Item:
    """
    Attributes:
        name (str):
        scopes (List['ListAvailableScopesResponse200ItemScopesItem']):
        description (Union[Unset, None, str]):
    """

    name: str
    scopes: List["ListAvailableScopesResponse200ItemScopesItem"]
    description: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        scopes = []
        for scopes_item_data in self.scopes:
            scopes_item = scopes_item_data.to_dict()

            scopes.append(scopes_item)

        description = self.description

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "scopes": scopes,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_available_scopes_response_200_item_scopes_item import (
            ListAvailableScopesResponse200ItemScopesItem,
        )

        d = src_dict.copy()
        name = d.pop("name")

        scopes = []
        _scopes = d.pop("scopes")
        for scopes_item_data in _scopes:
            scopes_item = ListAvailableScopesResponse200ItemScopesItem.from_dict(scopes_item_data)

            scopes.append(scopes_item)

        description = d.pop("description", UNSET)

        list_available_scopes_response_200_item = cls(
            name=name,
            scopes=scopes,
            description=description,
        )

        list_available_scopes_response_200_item.additional_properties = d
        return list_available_scopes_response_200_item

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
