from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.id_name_pair_request import IdNamePairRequest


T = TypeVar("T", bound="QueryOutputRequest")


@_attrs_define
class QueryOutputRequest:
    """
    Attributes:
        customers (Union[Unset, list['IdNamePairRequest']]):
        offerings (Union[Unset, list['IdNamePairRequest']]):
        all_users (Union[Unset, bool]):
    """

    customers: Union[Unset, list["IdNamePairRequest"]] = UNSET
    offerings: Union[Unset, list["IdNamePairRequest"]] = UNSET
    all_users: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        customers: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.customers, Unset):
            customers = []
            for customers_item_data in self.customers:
                customers_item = customers_item_data.to_dict()
                customers.append(customers_item)

        offerings: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.offerings, Unset):
            offerings = []
            for offerings_item_data in self.offerings:
                offerings_item = offerings_item_data.to_dict()
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
        from ..models.id_name_pair_request import IdNamePairRequest

        d = dict(src_dict)
        customers = []
        _customers = d.pop("customers", UNSET)
        for customers_item_data in _customers or []:
            customers_item = IdNamePairRequest.from_dict(customers_item_data)

            customers.append(customers_item)

        offerings = []
        _offerings = d.pop("offerings", UNSET)
        for offerings_item_data in _offerings or []:
            offerings_item = IdNamePairRequest.from_dict(offerings_item_data)

            offerings.append(offerings_item)

        all_users = d.pop("all_users", UNSET)

        query_output_request = cls(
            customers=customers,
            offerings=offerings,
            all_users=all_users,
        )

        query_output_request.additional_properties = d
        return query_output_request

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
