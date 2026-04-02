from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedOfferingSoftwareCatalogUpdateRequest")


@_attrs_define
class PatchedOfferingSoftwareCatalogUpdateRequest:
    """
    Attributes:
        offering_catalog_uuid (Union[Unset, UUID]):
        catalog (Union[Unset, UUID]):
        enabled_cpu_family (Union[Unset, Any]): List of enabled CPU families: ['x86_64', 'aarch64']
        enabled_cpu_microarchitectures (Union[Unset, Any]): List of enabled CPU microarchitectures: ['generic', 'zen3']
        partition (Union[None, UUID, Unset]):
    """

    offering_catalog_uuid: Union[Unset, UUID] = UNSET
    catalog: Union[Unset, UUID] = UNSET
    enabled_cpu_family: Union[Unset, Any] = UNSET
    enabled_cpu_microarchitectures: Union[Unset, Any] = UNSET
    partition: Union[None, UUID, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        offering_catalog_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.offering_catalog_uuid, Unset):
            offering_catalog_uuid = str(self.offering_catalog_uuid)

        catalog: Union[Unset, str] = UNSET
        if not isinstance(self.catalog, Unset):
            catalog = str(self.catalog)

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
        field_dict.update({})
        if offering_catalog_uuid is not UNSET:
            field_dict["offering_catalog_uuid"] = offering_catalog_uuid
        if catalog is not UNSET:
            field_dict["catalog"] = catalog
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
        _offering_catalog_uuid = d.pop("offering_catalog_uuid", UNSET)
        offering_catalog_uuid: Union[Unset, UUID]
        if isinstance(_offering_catalog_uuid, Unset):
            offering_catalog_uuid = UNSET
        else:
            offering_catalog_uuid = UUID(_offering_catalog_uuid)

        _catalog = d.pop("catalog", UNSET)
        catalog: Union[Unset, UUID]
        if isinstance(_catalog, Unset):
            catalog = UNSET
        else:
            catalog = UUID(_catalog)

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

        patched_offering_software_catalog_update_request = cls(
            offering_catalog_uuid=offering_catalog_uuid,
            catalog=catalog,
            enabled_cpu_family=enabled_cpu_family,
            enabled_cpu_microarchitectures=enabled_cpu_microarchitectures,
            partition=partition,
        )

        patched_offering_software_catalog_update_request.additional_properties = d
        return patched_offering_software_catalog_update_request

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
