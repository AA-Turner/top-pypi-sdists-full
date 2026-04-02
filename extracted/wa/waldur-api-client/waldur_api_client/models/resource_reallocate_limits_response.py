from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ResourceReallocateLimitsResponse")


@_attrs_define
class ResourceReallocateLimitsResponse:
    """
    Attributes:
        source_order_uuid (UUID): UUID of the source order for limit reallocation
        target_order_uuids (list[UUID]): List of UUIDs for target orders receiving the reallocated limits
    """

    source_order_uuid: UUID
    target_order_uuids: list[UUID]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        source_order_uuid = str(self.source_order_uuid)

        target_order_uuids = []
        for target_order_uuids_item_data in self.target_order_uuids:
            target_order_uuids_item = str(target_order_uuids_item_data)
            target_order_uuids.append(target_order_uuids_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "source_order_uuid": source_order_uuid,
                "target_order_uuids": target_order_uuids,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        source_order_uuid = UUID(d.pop("source_order_uuid"))

        target_order_uuids = []
        _target_order_uuids = d.pop("target_order_uuids")
        for target_order_uuids_item_data in _target_order_uuids:
            target_order_uuids_item = UUID(target_order_uuids_item_data)

            target_order_uuids.append(target_order_uuids_item)

        resource_reallocate_limits_response = cls(
            source_order_uuid=source_order_uuid,
            target_order_uuids=target_order_uuids,
        )

        resource_reallocate_limits_response.additional_properties = d
        return resource_reallocate_limits_response

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
