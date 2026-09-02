from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="FileResourceTypeToFileExtMapResponse200AdditionalProperty")


@_attrs_define
class FileResourceTypeToFileExtMapResponse200AdditionalProperty:
    """
    Attributes:
        format_extension (Union[Unset, None, str]):
        is_fileset (Union[Unset, bool]):
    """

    format_extension: Union[Unset, None, str] = UNSET
    is_fileset: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        format_extension = self.format_extension
        is_fileset = self.is_fileset

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if format_extension is not UNSET:
            field_dict["format_extension"] = format_extension
        if is_fileset is not UNSET:
            field_dict["is_fileset"] = is_fileset

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        format_extension = d.pop("format_extension", UNSET)

        is_fileset = d.pop("is_fileset", UNSET)

        file_resource_type_to_file_ext_map_response_200_additional_property = cls(
            format_extension=format_extension,
            is_fileset=is_fileset,
        )

        file_resource_type_to_file_ext_map_response_200_additional_property.additional_properties = d
        return file_resource_type_to_file_ext_map_response_200_additional_property

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
