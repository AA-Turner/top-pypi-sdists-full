from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.catalog_summary import CatalogSummary
    from ..models.partition_summary import PartitionSummary


T = TypeVar("T", bound="NestedSoftwareCatalog")


@_attrs_define
class NestedSoftwareCatalog:
    """
    Attributes:
        uuid (Union[Unset, UUID]):
        catalog (Union[Unset, CatalogSummary]):
        enabled_cpu_family (Union[Unset, Any]): List of enabled CPU families: ['x86_64', 'aarch64']
        enabled_cpu_microarchitectures (Union[Unset, Any]): List of enabled CPU microarchitectures: ['generic', 'zen3']
        package_count (Union[Unset, int]):
        partition (Union['PartitionSummary', None, Unset]):
    """

    uuid: Union[Unset, UUID] = UNSET
    catalog: Union[Unset, "CatalogSummary"] = UNSET
    enabled_cpu_family: Union[Unset, Any] = UNSET
    enabled_cpu_microarchitectures: Union[Unset, Any] = UNSET
    package_count: Union[Unset, int] = UNSET
    partition: Union["PartitionSummary", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.partition_summary import PartitionSummary

        uuid: Union[Unset, str] = UNSET
        if not isinstance(self.uuid, Unset):
            uuid = str(self.uuid)

        catalog: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.catalog, Unset):
            catalog = self.catalog.to_dict()

        enabled_cpu_family = self.enabled_cpu_family

        enabled_cpu_microarchitectures = self.enabled_cpu_microarchitectures

        package_count = self.package_count

        partition: Union[None, Unset, dict[str, Any]]
        if isinstance(self.partition, Unset):
            partition = UNSET
        elif isinstance(self.partition, PartitionSummary):
            partition = self.partition.to_dict()
        else:
            partition = self.partition

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if catalog is not UNSET:
            field_dict["catalog"] = catalog
        if enabled_cpu_family is not UNSET:
            field_dict["enabled_cpu_family"] = enabled_cpu_family
        if enabled_cpu_microarchitectures is not UNSET:
            field_dict["enabled_cpu_microarchitectures"] = enabled_cpu_microarchitectures
        if package_count is not UNSET:
            field_dict["package_count"] = package_count
        if partition is not UNSET:
            field_dict["partition"] = partition

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.catalog_summary import CatalogSummary
        from ..models.partition_summary import PartitionSummary

        d = dict(src_dict)
        _uuid = d.pop("uuid", UNSET)
        uuid: Union[Unset, UUID]
        if isinstance(_uuid, Unset):
            uuid = UNSET
        else:
            uuid = UUID(_uuid)

        _catalog = d.pop("catalog", UNSET)
        catalog: Union[Unset, CatalogSummary]
        if isinstance(_catalog, Unset):
            catalog = UNSET
        else:
            catalog = CatalogSummary.from_dict(_catalog)

        enabled_cpu_family = d.pop("enabled_cpu_family", UNSET)

        enabled_cpu_microarchitectures = d.pop("enabled_cpu_microarchitectures", UNSET)

        package_count = d.pop("package_count", UNSET)

        def _parse_partition(data: object) -> Union["PartitionSummary", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                partition_type_1 = PartitionSummary.from_dict(data)

                return partition_type_1
            except:  # noqa: E722
                pass
            return cast(Union["PartitionSummary", None, Unset], data)

        partition = _parse_partition(d.pop("partition", UNSET))

        nested_software_catalog = cls(
            uuid=uuid,
            catalog=catalog,
            enabled_cpu_family=enabled_cpu_family,
            enabled_cpu_microarchitectures=enabled_cpu_microarchitectures,
            package_count=package_count,
            partition=partition,
        )

        nested_software_catalog.additional_properties = d
        return nested_software_catalog

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
