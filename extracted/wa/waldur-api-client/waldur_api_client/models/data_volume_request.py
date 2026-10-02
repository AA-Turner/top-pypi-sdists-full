from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="DataVolumeRequest")


@_attrs_define
class DataVolumeRequest:
    """
    Attributes:
        size (int):
        mount_point (str):
        volume_type (Union[None, Unset, str]):
        filesystem (Union[Unset, str]):
    """

    size: int
    mount_point: str
    volume_type: Union[None, Unset, str] = UNSET
    filesystem: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        size = self.size

        mount_point = self.mount_point

        volume_type: Union[None, Unset, str]
        if isinstance(self.volume_type, Unset):
            volume_type = UNSET
        else:
            volume_type = self.volume_type

        filesystem = self.filesystem

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "size": size,
                "mount_point": mount_point,
            }
        )
        if volume_type is not UNSET:
            field_dict["volume_type"] = volume_type
        if filesystem is not UNSET:
            field_dict["filesystem"] = filesystem

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        size = d.pop("size")

        mount_point = d.pop("mount_point")

        def _parse_volume_type(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        volume_type = _parse_volume_type(d.pop("volume_type", UNSET))

        filesystem = d.pop("filesystem", UNSET)

        data_volume_request = cls(
            size=size,
            mount_point=mount_point,
            volume_type=volume_type,
            filesystem=filesystem,
        )

        data_volume_request.additional_properties = d
        return data_volume_request

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
