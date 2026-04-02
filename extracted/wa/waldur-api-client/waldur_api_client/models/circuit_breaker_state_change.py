from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CircuitBreakerStateChange")


@_attrs_define
class CircuitBreakerStateChange:
    """
    Attributes:
        timestamp (float): Unix timestamp of state change
        from_state (Union[None, str]): Previous state
        to_state (str): New state
        reason (str): Reason for state change
    """

    timestamp: float
    from_state: Union[None, str]
    to_state: str
    reason: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        timestamp = self.timestamp

        from_state: Union[None, str]
        from_state = self.from_state

        to_state = self.to_state

        reason = self.reason

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "timestamp": timestamp,
                "from_state": from_state,
                "to_state": to_state,
                "reason": reason,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        timestamp = d.pop("timestamp")

        def _parse_from_state(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        from_state = _parse_from_state(d.pop("from_state"))

        to_state = d.pop("to_state")

        reason = d.pop("reason")

        circuit_breaker_state_change = cls(
            timestamp=timestamp,
            from_state=from_state,
            to_state=to_state,
            reason=reason,
        )

        circuit_breaker_state_change.additional_properties = d
        return circuit_breaker_state_change

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
