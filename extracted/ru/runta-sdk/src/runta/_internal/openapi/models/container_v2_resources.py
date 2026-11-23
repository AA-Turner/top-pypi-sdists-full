from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.container_v2_compute import ContainerV2Compute


T = TypeVar("T", bound="ContainerV2Resources")


@_attrs_define
class ContainerV2Resources:
    """
    Attributes:
        requested (ContainerV2Compute):
        limit (ContainerV2Compute):
        disk_capacity_bytes (int):
    """

    requested: ContainerV2Compute
    limit: ContainerV2Compute
    disk_capacity_bytes: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        requested = self.requested.to_dict()

        limit = self.limit.to_dict()

        disk_capacity_bytes = self.disk_capacity_bytes

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "requested": requested,
                "limit": limit,
                "disk_capacity_bytes": disk_capacity_bytes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.container_v2_compute import ContainerV2Compute

        d = dict(src_dict)
        requested = ContainerV2Compute.from_dict(d.pop("requested"))

        limit = ContainerV2Compute.from_dict(d.pop("limit"))

        disk_capacity_bytes = d.pop("disk_capacity_bytes")

        container_v2_resources = cls(
            requested=requested,
            limit=limit,
            disk_capacity_bytes=disk_capacity_bytes,
        )

        container_v2_resources.additional_properties = d
        return container_v2_resources

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
