from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="NestedPartitionQoS")


@_attrs_define
class NestedPartitionQoS:
    """
    Attributes:
        uuid (Union[Unset, UUID]):
        qos (Union[Unset, UUID]):
        qos_name (Union[Unset, str]):
        is_default (Union[Unset, bool]): Default QOS for this partition (seeds SLURM DefaultQOS).
    """

    uuid: Union[Unset, UUID] = UNSET
    qos: Union[Unset, UUID] = UNSET
    qos_name: Union[Unset, str] = UNSET
    is_default: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid: Union[Unset, str] = UNSET
        if not isinstance(self.uuid, Unset):
            uuid = str(self.uuid)

        qos: Union[Unset, str] = UNSET
        if not isinstance(self.qos, Unset):
            qos = str(self.qos)

        qos_name = self.qos_name

        is_default = self.is_default

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if qos is not UNSET:
            field_dict["qos"] = qos
        if qos_name is not UNSET:
            field_dict["qos_name"] = qos_name
        if is_default is not UNSET:
            field_dict["is_default"] = is_default

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _uuid = d.pop("uuid", UNSET)
        uuid: Union[Unset, UUID]
        if isinstance(_uuid, Unset):
            uuid = UNSET
        else:
            uuid = UUID(_uuid)

        _qos = d.pop("qos", UNSET)
        qos: Union[Unset, UUID]
        if isinstance(_qos, Unset):
            qos = UNSET
        else:
            qos = UUID(_qos)

        qos_name = d.pop("qos_name", UNSET)

        is_default = d.pop("is_default", UNSET)

        nested_partition_qo_s = cls(
            uuid=uuid,
            qos=qos,
            qos_name=qos_name,
            is_default=is_default,
        )

        nested_partition_qo_s.additional_properties = d
        return nested_partition_qo_s

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
