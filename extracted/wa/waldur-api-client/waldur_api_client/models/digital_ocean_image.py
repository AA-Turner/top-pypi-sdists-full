import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.digital_ocean_region import DigitalOceanRegion


T = TypeVar("T", bound="DigitalOceanImage")


@_attrs_define
class DigitalOceanImage:
    """
    Attributes:
        url (str):
        uuid (UUID):
        name (str):
        distribution (str):
        type_ (str):
        regions (list['DigitalOceanRegion']):
        is_official (Union[Unset, bool]): Is image provided by DigitalOcean
        created_at (Union[None, Unset, datetime.datetime]):
        min_disk_size (Union[None, Unset, int]): Minimum disk required for a size to use this image
    """

    url: str
    uuid: UUID
    name: str
    distribution: str
    type_: str
    regions: list["DigitalOceanRegion"]
    is_official: Union[Unset, bool] = UNSET
    created_at: Union[None, Unset, datetime.datetime] = UNSET
    min_disk_size: Union[None, Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        name = self.name

        distribution = self.distribution

        type_ = self.type_

        regions = []
        for regions_item_data in self.regions:
            regions_item = regions_item_data.to_dict()
            regions.append(regions_item)

        is_official = self.is_official

        created_at: Union[None, Unset, str]
        if isinstance(self.created_at, Unset):
            created_at = UNSET
        elif isinstance(self.created_at, datetime.datetime):
            created_at = self.created_at.isoformat()
        else:
            created_at = self.created_at

        min_disk_size: Union[None, Unset, int]
        if isinstance(self.min_disk_size, Unset):
            min_disk_size = UNSET
        else:
            min_disk_size = self.min_disk_size

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "name": name,
                "distribution": distribution,
                "type": type_,
                "regions": regions,
            }
        )
        if is_official is not UNSET:
            field_dict["is_official"] = is_official
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if min_disk_size is not UNSET:
            field_dict["min_disk_size"] = min_disk_size

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.digital_ocean_region import DigitalOceanRegion

        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        name = d.pop("name")

        distribution = d.pop("distribution")

        type_ = d.pop("type")

        regions = []
        _regions = d.pop("regions")
        for regions_item_data in _regions:
            regions_item = DigitalOceanRegion.from_dict(regions_item_data)

            regions.append(regions_item)

        is_official = d.pop("is_official", UNSET)

        def _parse_created_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                created_at_type_0 = isoparse(data)

                return created_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        created_at = _parse_created_at(d.pop("created_at", UNSET))

        def _parse_min_disk_size(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        min_disk_size = _parse_min_disk_size(d.pop("min_disk_size", UNSET))

        digital_ocean_image = cls(
            url=url,
            uuid=uuid,
            name=name,
            distribution=distribution,
            type_=type_,
            regions=regions,
            is_official=is_official,
            created_at=created_at,
            min_disk_size=min_disk_size,
        )

        digital_ocean_image.additional_properties = d
        return digital_ocean_image

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
