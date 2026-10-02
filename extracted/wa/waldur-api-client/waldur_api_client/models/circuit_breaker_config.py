from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CircuitBreakerConfig")


@_attrs_define
class CircuitBreakerConfig:
    """
    Attributes:
        failure_threshold (int): Number of failures before opening circuit
        recovery_timeout (int): Seconds to wait before attempting recovery
        success_threshold (int): Successful calls needed in half-open state to close
    """

    failure_threshold: int
    recovery_timeout: int
    success_threshold: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        failure_threshold = self.failure_threshold

        recovery_timeout = self.recovery_timeout

        success_threshold = self.success_threshold

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "failure_threshold": failure_threshold,
                "recovery_timeout": recovery_timeout,
                "success_threshold": success_threshold,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        failure_threshold = d.pop("failure_threshold")

        recovery_timeout = d.pop("recovery_timeout")

        success_threshold = d.pop("success_threshold")

        circuit_breaker_config = cls(
            failure_threshold=failure_threshold,
            recovery_timeout=recovery_timeout,
            success_threshold=success_threshold,
        )

        circuit_breaker_config.additional_properties = d
        return circuit_breaker_config

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
