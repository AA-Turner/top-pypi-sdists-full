from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ListPostgresReplicationSlotResponse200Item")


@_attrs_define
class ListPostgresReplicationSlotResponse200Item:
    """
    Attributes:
        slot_name (Union[Unset, str]):
        active (Union[Unset, bool]):
    """

    slot_name: Union[Unset, str] = UNSET
    active: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        slot_name = self.slot_name
        active = self.active

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if slot_name is not UNSET:
            field_dict["slot_name"] = slot_name
        if active is not UNSET:
            field_dict["active"] = active

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        slot_name = d.pop("slot_name", UNSET)

        active = d.pop("active", UNSET)

        list_postgres_replication_slot_response_200_item = cls(
            slot_name=slot_name,
            active=active,
        )

        list_postgres_replication_slot_response_200_item.additional_properties = d
        return list_postgres_replication_slot_response_200_item

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
