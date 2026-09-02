from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ListAzureNamespacesResponse200Item")


@_attrs_define
class ListAzureNamespacesResponse200Item:
    """An ARM resource the service principal can see.

    Attributes:
        id (str):
        name (str):
        type (str):
        location (Union[Unset, str]):
    """

    id: str
    name: str
    type: str
    location: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        type = self.type
        location = self.location

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "type": type,
            }
        )
        if location is not UNSET:
            field_dict["location"] = location

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        type = d.pop("type")

        location = d.pop("location", UNSET)

        list_azure_namespaces_response_200_item = cls(
            id=id,
            name=name,
            type=type,
            location=location,
        )

        list_azure_namespaces_response_200_item.additional_properties = d
        return list_azure_namespaces_response_200_item

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
