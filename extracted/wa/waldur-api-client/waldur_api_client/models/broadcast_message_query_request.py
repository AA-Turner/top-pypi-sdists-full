from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="BroadcastMessageQueryRequest")


@_attrs_define
class BroadcastMessageQueryRequest:
    """
    Attributes:
        customers (Union[Unset, list[UUID]]):
        offerings (Union[Unset, list[UUID]]):
        all_users (Union[Unset, bool]):  Default: False.
    """

    customers: Union[Unset, list[UUID]] = UNSET
    offerings: Union[Unset, list[UUID]] = UNSET
    all_users: Union[Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        customers: Union[Unset, list[str]] = UNSET
        if not isinstance(self.customers, Unset):
            customers = []
            for customers_item_data in self.customers:
                customers_item = str(customers_item_data)
                customers.append(customers_item)

        offerings: Union[Unset, list[str]] = UNSET
        if not isinstance(self.offerings, Unset):
            offerings = []
            for offerings_item_data in self.offerings:
                offerings_item = str(offerings_item_data)
                offerings.append(offerings_item)

        all_users = self.all_users

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if customers is not UNSET:
            field_dict["customers"] = customers
        if offerings is not UNSET:
            field_dict["offerings"] = offerings
        if all_users is not UNSET:
            field_dict["all_users"] = all_users

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        customers = []
        _customers = d.pop("customers", UNSET)
        for customers_item_data in _customers or []:
            customers_item = UUID(customers_item_data)

            customers.append(customers_item)

        offerings = []
        _offerings = d.pop("offerings", UNSET)
        for offerings_item_data in _offerings or []:
            offerings_item = UUID(offerings_item_data)

            offerings.append(offerings_item)

        all_users = d.pop("all_users", UNSET)

        broadcast_message_query_request = cls(
            customers=customers,
            offerings=offerings,
            all_users=all_users,
        )

        broadcast_message_query_request.additional_properties = d
        return broadcast_message_query_request

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
