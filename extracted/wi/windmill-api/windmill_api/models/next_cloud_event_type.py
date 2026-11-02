from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="NextCloudEventType")


@_attrs_define
class NextCloudEventType:
    """
    Attributes:
        id (str):
        name (str):
        path (str):
        description (Union[Unset, str]):
        category (Union[Unset, str]):
    """

    id: str
    name: str
    path: str
    description: Union[Unset, str] = UNSET
    category: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        path = self.path
        description = self.description
        category = self.category

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "path": path,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if category is not UNSET:
            field_dict["category"] = category

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        path = d.pop("path")

        description = d.pop("description", UNSET)

        category = d.pop("category", UNSET)

        next_cloud_event_type = cls(
            id=id,
            name=name,
            path=path,
            description=description,
            category=category,
        )

        next_cloud_event_type.additional_properties = d
        return next_cloud_event_type

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
