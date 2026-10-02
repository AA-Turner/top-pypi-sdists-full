from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.partition_qo_s_item_request import PartitionQoSItemRequest


T = TypeVar("T", bound="SetPartitionQoSRequest")


@_attrs_define
class SetPartitionQoSRequest:
    """
    Attributes:
        partition_uuid (UUID):
        qos_options (list['PartitionQoSItemRequest']):
    """

    partition_uuid: UUID
    qos_options: list["PartitionQoSItemRequest"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        partition_uuid = str(self.partition_uuid)

        qos_options = []
        for qos_options_item_data in self.qos_options:
            qos_options_item = qos_options_item_data.to_dict()
            qos_options.append(qos_options_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "partition_uuid": partition_uuid,
                "qos_options": qos_options,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.partition_qo_s_item_request import PartitionQoSItemRequest

        d = dict(src_dict)
        partition_uuid = UUID(d.pop("partition_uuid"))

        qos_options = []
        _qos_options = d.pop("qos_options")
        for qos_options_item_data in _qos_options:
            qos_options_item = PartitionQoSItemRequest.from_dict(qos_options_item_data)

            qos_options.append(qos_options_item)

        set_partition_qo_s_request = cls(
            partition_uuid=partition_uuid,
            qos_options=qos_options,
        )

        set_partition_qo_s_request.additional_properties = d
        return set_partition_qo_s_request

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
