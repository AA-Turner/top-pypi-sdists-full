from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="DigitalOceanDropletRequest")


@_attrs_define
class DigitalOceanDropletRequest:
    """
    Attributes:
        name (str):
        service_settings (str):
        project (str):
        region (str):
        image (str):
        size (str):
        description (Union[Unset, str]):
        ssh_public_key (Union[Unset, str]):
        user_data (Union[Unset, str]): Additional data that will be added to instance on provisioning
    """

    name: str
    service_settings: str
    project: str
    region: str
    image: str
    size: str
    description: Union[Unset, str] = UNSET
    ssh_public_key: Union[Unset, str] = UNSET
    user_data: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        service_settings = self.service_settings

        project = self.project

        region = self.region

        image = self.image

        size = self.size

        description = self.description

        ssh_public_key = self.ssh_public_key

        user_data = self.user_data

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "service_settings": service_settings,
                "project": project,
                "region": region,
                "image": image,
                "size": size,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if ssh_public_key is not UNSET:
            field_dict["ssh_public_key"] = ssh_public_key
        if user_data is not UNSET:
            field_dict["user_data"] = user_data

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        service_settings = d.pop("service_settings")

        project = d.pop("project")

        region = d.pop("region")

        image = d.pop("image")

        size = d.pop("size")

        description = d.pop("description", UNSET)

        ssh_public_key = d.pop("ssh_public_key", UNSET)

        user_data = d.pop("user_data", UNSET)

        digital_ocean_droplet_request = cls(
            name=name,
            service_settings=service_settings,
            project=project,
            region=region,
            image=image,
            size=size,
            description=description,
            ssh_public_key=ssh_public_key,
            user_data=user_data,
        )

        digital_ocean_droplet_request.additional_properties = d
        return digital_ocean_droplet_request

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
