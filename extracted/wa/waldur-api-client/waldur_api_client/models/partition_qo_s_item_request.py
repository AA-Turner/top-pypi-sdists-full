from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PartitionQoSItemRequest")


@_attrs_define
class PartitionQoSItemRequest:
    """
    Attributes:
        qos_uuid (UUID):
        is_default (Union[Unset, bool]):  Default: False.
    """

    qos_uuid: UUID
    is_default: Union[Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        qos_uuid = str(self.qos_uuid)

        is_default = self.is_default

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "qos_uuid": qos_uuid,
            }
        )
        if is_default is not UNSET:
            field_dict["is_default"] = is_default

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        qos_uuid = UUID(d.pop("qos_uuid"))

        is_default = d.pop("is_default", UNSET)

        partition_qo_s_item_request = cls(
            qos_uuid=qos_uuid,
            is_default=is_default,
        )

        partition_qo_s_item_request.additional_properties = d
        return partition_qo_s_item_request

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
