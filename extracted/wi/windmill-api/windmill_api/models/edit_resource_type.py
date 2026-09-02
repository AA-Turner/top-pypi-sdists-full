from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="EditResourceType")


@_attrs_define
class EditResourceType:
    """
    Attributes:
        schema (Union[Unset, Any]):
        description (Union[Unset, str]):
        is_fileset (Union[Unset, bool]):
        format_extension (Union[Unset, None, str]): File extension for a type whose value is one file rather than a set
            of fields. Omit to leave it unchanged; send null to clear it.
    """

    schema: Union[Unset, Any] = UNSET
    description: Union[Unset, str] = UNSET
    is_fileset: Union[Unset, bool] = UNSET
    format_extension: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        schema = self.schema
        description = self.description
        is_fileset = self.is_fileset
        format_extension = self.format_extension

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if schema is not UNSET:
            field_dict["schema"] = schema
        if description is not UNSET:
            field_dict["description"] = description
        if is_fileset is not UNSET:
            field_dict["is_fileset"] = is_fileset
        if format_extension is not UNSET:
            field_dict["format_extension"] = format_extension

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        schema = d.pop("schema", UNSET)

        description = d.pop("description", UNSET)

        is_fileset = d.pop("is_fileset", UNSET)

        format_extension = d.pop("format_extension", UNSET)

        edit_resource_type = cls(
            schema=schema,
            description=description,
            is_fileset=is_fileset,
            format_extension=format_extension,
        )

        edit_resource_type.additional_properties = d
        return edit_resource_type

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
