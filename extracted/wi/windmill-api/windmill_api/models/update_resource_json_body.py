from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateResourceJsonBody")


@_attrs_define
class UpdateResourceJsonBody:
    """
    Attributes:
        path (Union[Unset, str]): The path to the resource
        description (Union[Unset, str]): The new description of the resource
        value (Union[Unset, Any]):
        resource_type (Union[Unset, str]): The new resource_type to be associated with the resource
    """

    path: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    value: Union[Unset, Any] = UNSET
    resource_type: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        path = self.path
        description = self.description
        value = self.value
        resource_type = self.resource_type

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if path is not UNSET:
            field_dict["path"] = path
        if description is not UNSET:
            field_dict["description"] = description
        if value is not UNSET:
            field_dict["value"] = value
        if resource_type is not UNSET:
            field_dict["resource_type"] = resource_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        path = d.pop("path", UNSET)

        description = d.pop("description", UNSET)

        value = d.pop("value", UNSET)

        resource_type = d.pop("resource_type", UNSET)

        update_resource_json_body = cls(
            path=path,
            description=description,
            value=value,
            resource_type=resource_type,
        )

        update_resource_json_body.additional_properties = d
        return update_resource_json_body

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
