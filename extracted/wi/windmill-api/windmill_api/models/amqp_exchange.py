from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AmqpExchange")


@_attrs_define
class AmqpExchange:
    """
    Attributes:
        exchange_name (str): Name of the exchange to bind the consumed queue to
        routing_keys (Union[Unset, List[str]]): Routing keys used to bind the queue to the exchange
    """

    exchange_name: str
    routing_keys: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        exchange_name = self.exchange_name
        routing_keys: Union[Unset, List[str]] = UNSET
        if not isinstance(self.routing_keys, Unset):
            routing_keys = self.routing_keys

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "exchange_name": exchange_name,
            }
        )
        if routing_keys is not UNSET:
            field_dict["routing_keys"] = routing_keys

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        exchange_name = d.pop("exchange_name")

        routing_keys = cast(List[str], d.pop("routing_keys", UNSET))

        amqp_exchange = cls(
            exchange_name=exchange_name,
            routing_keys=routing_keys,
        )

        amqp_exchange.additional_properties = d
        return amqp_exchange

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
