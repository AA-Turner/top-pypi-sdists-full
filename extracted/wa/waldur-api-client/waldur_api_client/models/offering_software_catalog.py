import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="OfferingSoftwareCatalog")


@_attrs_define
class OfferingSoftwareCatalog:
    """
    Attributes:
        uuid (UUID):
        created (datetime.datetime):
        modified (datetime.datetime):
        offering (UUID):
        catalog (UUID):
        offering_name (str):
        catalog_name (str):
        catalog_version (str):
        partition_name (str):
        enabled_cpu_family (Union[Unset, Any]): List of enabled CPU families: ['x86_64', 'aarch64']
        enabled_cpu_microarchitectures (Union[Unset, Any]): List of enabled CPU microarchitectures: ['generic', 'zen3']
        partition (Union[None, UUID, Unset]):
    """

    uuid: UUID
    created: datetime.datetime
    modified: datetime.datetime
    offering: UUID
    catalog: UUID
    offering_name: str
    catalog_name: str
    catalog_version: str
    partition_name: str
    enabled_cpu_family: Union[Unset, Any] = UNSET
    enabled_cpu_microarchitectures: Union[Unset, Any] = UNSET
    partition: Union[None, UUID, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        offering = str(self.offering)

        catalog = str(self.catalog)

        offering_name = self.offering_name

        catalog_name = self.catalog_name

        catalog_version = self.catalog_version

        partition_name = self.partition_name

        enabled_cpu_family = self.enabled_cpu_family

        enabled_cpu_microarchitectures = self.enabled_cpu_microarchitectures

        partition: Union[None, Unset, str]
        if isinstance(self.partition, Unset):
            partition = UNSET
        elif isinstance(self.partition, UUID):
            partition = str(self.partition)
        else:
            partition = self.partition

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "created": created,
                "modified": modified,
                "offering": offering,
                "catalog": catalog,
                "offering_name": offering_name,
                "catalog_name": catalog_name,
                "catalog_version": catalog_version,
                "partition_name": partition_name,
            }
        )
        if enabled_cpu_family is not UNSET:
            field_dict["enabled_cpu_family"] = enabled_cpu_family
        if enabled_cpu_microarchitectures is not UNSET:
            field_dict["enabled_cpu_microarchitectures"] = enabled_cpu_microarchitectures
        if partition is not UNSET:
            field_dict["partition"] = partition

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        offering = UUID(d.pop("offering"))

        catalog = UUID(d.pop("catalog"))

        offering_name = d.pop("offering_name")

        catalog_name = d.pop("catalog_name")

        catalog_version = d.pop("catalog_version")

        partition_name = d.pop("partition_name")

        enabled_cpu_family = d.pop("enabled_cpu_family", UNSET)

        enabled_cpu_microarchitectures = d.pop("enabled_cpu_microarchitectures", UNSET)

        def _parse_partition(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                partition_type_0 = UUID(data)

                return partition_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        partition = _parse_partition(d.pop("partition", UNSET))

        offering_software_catalog = cls(
            uuid=uuid,
            created=created,
            modified=modified,
            offering=offering,
            catalog=catalog,
            offering_name=offering_name,
            catalog_name=catalog_name,
            catalog_version=catalog_version,
            partition_name=partition_name,
            enabled_cpu_family=enabled_cpu_family,
            enabled_cpu_microarchitectures=enabled_cpu_microarchitectures,
            partition=partition,
        )

        offering_software_catalog.additional_properties = d
        return offering_software_catalog

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
