from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.aws_region import AwsRegion


T = TypeVar("T", bound="AwsSize")


@_attrs_define
class AwsSize:
    """
    Attributes:
        url (str):
        uuid (UUID):
        name (str):
        cores (int): Number of cores in a VM
        ram (int): Memory size in MiB
        disk (int): Disk size in MiB
        regions (list['AwsRegion']):
        description (str):
    """

    url: str
    uuid: UUID
    name: str
    cores: int
    ram: int
    disk: int
    regions: list["AwsRegion"]
    description: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        name = self.name

        cores = self.cores

        ram = self.ram

        disk = self.disk

        regions = []
        for regions_item_data in self.regions:
            regions_item = regions_item_data.to_dict()
            regions.append(regions_item)

        description = self.description

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "name": name,
                "cores": cores,
                "ram": ram,
                "disk": disk,
                "regions": regions,
                "description": description,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.aws_region import AwsRegion

        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        name = d.pop("name")

        cores = d.pop("cores")

        ram = d.pop("ram")

        disk = d.pop("disk")

        regions = []
        _regions = d.pop("regions")
        for regions_item_data in _regions:
            regions_item = AwsRegion.from_dict(regions_item_data)

            regions.append(regions_item)

        description = d.pop("description")

        aws_size = cls(
            url=url,
            uuid=uuid,
            name=name,
            cores=cores,
            ram=ram,
            disk=disk,
            regions=regions,
            description=description,
        )

        aws_size.additional_properties = d
        return aws_size

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
