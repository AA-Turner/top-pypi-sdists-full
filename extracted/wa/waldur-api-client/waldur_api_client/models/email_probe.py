from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="EmailProbe")


@_attrs_define
class EmailProbe:
    """
    Attributes:
        success (bool):
        latency_ms (Union[None, int]): Time to open the connection, in milliseconds
        error (str): Failure reason, empty on success
    """

    success: bool
    latency_ms: Union[None, int]
    error: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        success = self.success

        latency_ms: Union[None, int]
        latency_ms = self.latency_ms

        error = self.error

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "success": success,
                "latency_ms": latency_ms,
                "error": error,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        success = d.pop("success")

        def _parse_latency_ms(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        latency_ms = _parse_latency_ms(d.pop("latency_ms"))

        error = d.pop("error")

        email_probe = cls(
            success=success,
            latency_ms=latency_ms,
            error=error,
        )

        email_probe.additional_properties = d
        return email_probe

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
