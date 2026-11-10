from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="HpcSoftware")


@_attrs_define
class HpcSoftware:
    """
    Attributes:
        name (str):
        version (str):
        catalog (str):
        catalog_type (str):
        description (str):
        setup (list[str]): Lines making the catalog available, placed before 'load'.
        load (str): Line loading this version in a job.
        cpu_families (list[str]):
        gpu_architectures (list[str]):
    """

    name: str
    version: str
    catalog: str
    catalog_type: str
    description: str
    setup: list[str]
    load: str
    cpu_families: list[str]
    gpu_architectures: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        version = self.version

        catalog = self.catalog

        catalog_type = self.catalog_type

        description = self.description

        setup = self.setup

        load = self.load

        cpu_families = self.cpu_families

        gpu_architectures = self.gpu_architectures

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "version": version,
                "catalog": catalog,
                "catalog_type": catalog_type,
                "description": description,
                "setup": setup,
                "load": load,
                "cpu_families": cpu_families,
                "gpu_architectures": gpu_architectures,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        version = d.pop("version")

        catalog = d.pop("catalog")

        catalog_type = d.pop("catalog_type")

        description = d.pop("description")

        setup = cast(list[str], d.pop("setup"))

        load = d.pop("load")

        cpu_families = cast(list[str], d.pop("cpu_families"))

        gpu_architectures = cast(list[str], d.pop("gpu_architectures"))

        hpc_software = cls(
            name=name,
            version=version,
            catalog=catalog,
            catalog_type=catalog_type,
            description=description,
            setup=setup,
            load=load,
            cpu_families=cpu_families,
            gpu_architectures=gpu_architectures,
        )

        hpc_software.additional_properties = d
        return hpc_software

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
