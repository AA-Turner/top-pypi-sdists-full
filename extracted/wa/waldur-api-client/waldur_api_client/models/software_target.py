import datetime
from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="SoftwareTarget")


@_attrs_define
class SoftwareTarget:
    """
    Attributes:
        url (str):
        uuid (UUID):
        created (datetime.datetime):
        modified (datetime.datetime):
        target_type (str): Type of target (architecture, platform, variant, etc.)
        target_name (str): Target identifier (x86_64/generic, linux, variant_name, etc.)
        target_subtype (str): Target subtype (microarchitecture, distribution, etc.)
        location (str): Target location (CVMFS path, download URL, etc.)
        metadata (Any): Target-specific metadata (build options, system requirements, etc.)
        gpu_architectures (Any): List of GPU architectures this target supports (e.g., ['nvidia/cc70', 'nvidia/cc90'])
    """

    url: str
    uuid: UUID
    created: datetime.datetime
    modified: datetime.datetime
    target_type: str
    target_name: str
    target_subtype: str
    location: str
    metadata: Any
    gpu_architectures: Any
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        target_type = self.target_type

        target_name = self.target_name

        target_subtype = self.target_subtype

        location = self.location

        metadata = self.metadata

        gpu_architectures = self.gpu_architectures

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "created": created,
                "modified": modified,
                "target_type": target_type,
                "target_name": target_name,
                "target_subtype": target_subtype,
                "location": location,
                "metadata": metadata,
                "gpu_architectures": gpu_architectures,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        target_type = d.pop("target_type")

        target_name = d.pop("target_name")

        target_subtype = d.pop("target_subtype")

        location = d.pop("location")

        metadata = d.pop("metadata")

        gpu_architectures = d.pop("gpu_architectures")

        software_target = cls(
            url=url,
            uuid=uuid,
            created=created,
            modified=modified,
            target_type=target_type,
            target_name=target_name,
            target_subtype=target_subtype,
            location=location,
            metadata=metadata,
            gpu_architectures=gpu_architectures,
        )

        software_target.additional_properties = d
        return software_target

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
