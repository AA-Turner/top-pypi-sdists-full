from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="OpenStackDataVolumeRequest")


@_attrs_define
class OpenStackDataVolumeRequest:
    """
    Attributes:
        size (int):
        volume_type (Union[None, Unset, str]):
    """

    size: int
    volume_type: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        size = self.size

        volume_type: Union[None, Unset, str]
        if isinstance(self.volume_type, Unset):
            volume_type = UNSET
        else:
            volume_type = self.volume_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "size": size,
            }
        )
        if volume_type is not UNSET:
            field_dict["volume_type"] = volume_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        size = d.pop("size")

        def _parse_volume_type(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        volume_type = _parse_volume_type(d.pop("volume_type", UNSET))

        open_stack_data_volume_request = cls(
            size=size,
            volume_type=volume_type,
        )

        open_stack_data_volume_request.additional_properties = d
        return open_stack_data_volume_request

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
