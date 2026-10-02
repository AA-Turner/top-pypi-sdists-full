from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.circuit_breaker_config import CircuitBreakerConfig
    from ..models.circuit_breaker_state_change import CircuitBreakerStateChange


T = TypeVar("T", bound="CircuitBreakerStatus")


@_attrs_define
class CircuitBreakerStatus:
    """
    Attributes:
        state (str): Current state: closed, open, or half_open
        failure_count (int): Number of consecutive failures
        success_count (int): Successful calls since last state change
        last_failure_time (Union[None, float]): Unix timestamp of last failure
        last_state_change (Union[None, float]): Unix timestamp of last state change
        config (CircuitBreakerConfig):
        state_history (list['CircuitBreakerStateChange']): Recent state transitions (last 50)
    """

    state: str
    failure_count: int
    success_count: int
    last_failure_time: Union[None, float]
    last_state_change: Union[None, float]
    config: "CircuitBreakerConfig"
    state_history: list["CircuitBreakerStateChange"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        state = self.state

        failure_count = self.failure_count

        success_count = self.success_count

        last_failure_time: Union[None, float]
        last_failure_time = self.last_failure_time

        last_state_change: Union[None, float]
        last_state_change = self.last_state_change

        config = self.config.to_dict()

        state_history = []
        for state_history_item_data in self.state_history:
            state_history_item = state_history_item_data.to_dict()
            state_history.append(state_history_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "state": state,
                "failure_count": failure_count,
                "success_count": success_count,
                "last_failure_time": last_failure_time,
                "last_state_change": last_state_change,
                "config": config,
                "state_history": state_history,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.circuit_breaker_config import CircuitBreakerConfig
        from ..models.circuit_breaker_state_change import CircuitBreakerStateChange

        d = dict(src_dict)
        state = d.pop("state")

        failure_count = d.pop("failure_count")

        success_count = d.pop("success_count")

        def _parse_last_failure_time(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        last_failure_time = _parse_last_failure_time(d.pop("last_failure_time"))

        def _parse_last_state_change(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        last_state_change = _parse_last_state_change(d.pop("last_state_change"))

        config = CircuitBreakerConfig.from_dict(d.pop("config"))

        state_history = []
        _state_history = d.pop("state_history")
        for state_history_item_data in _state_history:
            state_history_item = CircuitBreakerStateChange.from_dict(state_history_item_data)

            state_history.append(state_history_item)

        circuit_breaker_status = cls(
            state=state,
            failure_count=failure_count,
            success_count=success_count,
            last_failure_time=last_failure_time,
            last_state_change=last_state_change,
            config=config,
            state_history=state_history,
        )

        circuit_breaker_status.additional_properties = d
        return circuit_breaker_status

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
