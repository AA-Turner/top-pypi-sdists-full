from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.volume_type_enum import VolumeTypeEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="AwsVolumeRequest")


@_attrs_define
class AwsVolumeRequest:
    """
    Attributes:
        name (str):
        service_settings (str):
        project (str):
        size (int): Size of volume in gigabytes
        region (str):
        volume_type (VolumeTypeEnum):
        description (Union[Unset, str]):
    """

    name: str
    service_settings: str
    project: str
    size: int
    region: str
    volume_type: VolumeTypeEnum
    description: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        service_settings = self.service_settings

        project = self.project

        size = self.size

        region = self.region

        volume_type = self.volume_type.value

        description = self.description

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "service_settings": service_settings,
                "project": project,
                "size": size,
                "region": region,
                "volume_type": volume_type,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        service_settings = d.pop("service_settings")

        project = d.pop("project")

        size = d.pop("size")

        region = d.pop("region")

        volume_type = VolumeTypeEnum(d.pop("volume_type"))

        description = d.pop("description", UNSET)

        aws_volume_request = cls(
            name=name,
            service_settings=service_settings,
            project=project,
            size=size,
            region=region,
            volume_type=volume_type,
            description=description,
        )

        aws_volume_request.additional_properties = d
        return aws_volume_request

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
