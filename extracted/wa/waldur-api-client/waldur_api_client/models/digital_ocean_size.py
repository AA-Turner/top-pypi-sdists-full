from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.digital_ocean_region import DigitalOceanRegion


T = TypeVar("T", bound="DigitalOceanSize")


@_attrs_define
class DigitalOceanSize:
    """
    Attributes:
        url (str):
        uuid (UUID):
        name (str):
        cores (int): Number of cores in a VM
        ram (int): Memory size in MiB
        disk (int): Disk size in MiB
        transfer (int): Amount of transfer bandwidth in MiB
        regions (list['DigitalOceanRegion']):
    """

    url: str
    uuid: UUID
    name: str
    cores: int
    ram: int
    disk: int
    transfer: int
    regions: list["DigitalOceanRegion"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        name = self.name

        cores = self.cores

        ram = self.ram

        disk = self.disk

        transfer = self.transfer

        regions = []
        for regions_item_data in self.regions:
            regions_item = regions_item_data.to_dict()
            regions.append(regions_item)

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
                "transfer": transfer,
                "regions": regions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.digital_ocean_region import DigitalOceanRegion

        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        name = d.pop("name")

        cores = d.pop("cores")

        ram = d.pop("ram")

        disk = d.pop("disk")

        transfer = d.pop("transfer")

        regions = []
        _regions = d.pop("regions")
        for regions_item_data in _regions:
            regions_item = DigitalOceanRegion.from_dict(regions_item_data)

            regions.append(regions_item)

        digital_ocean_size = cls(
            url=url,
            uuid=uuid,
            name=name,
            cores=cores,
            ram=ram,
            disk=disk,
            transfer=transfer,
            regions=regions,
        )

        digital_ocean_size.additional_properties = d
        return digital_ocean_size

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
