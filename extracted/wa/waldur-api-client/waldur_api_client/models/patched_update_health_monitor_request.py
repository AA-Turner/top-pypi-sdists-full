from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedUpdateHealthMonitorRequest")


@_attrs_define
class PatchedUpdateHealthMonitorRequest:
    """
    Attributes:
        name (Union[Unset, str]):
        delay (Union[Unset, int]): Interval between health checks in seconds Default: 5.
        timeout (Union[Unset, int]): Time in seconds to timeout a health check Default: 5.
        max_retries (Union[Unset, int]):  Default: 3.
        max_retries_down (Union[Unset, int]):  Default: 3.
    """

    name: Union[Unset, str] = UNSET
    delay: Union[Unset, int] = 5
    timeout: Union[Unset, int] = 5
    max_retries: Union[Unset, int] = 3
    max_retries_down: Union[Unset, int] = 3
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        delay = self.delay

        timeout = self.timeout

        max_retries = self.max_retries

        max_retries_down = self.max_retries_down

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if delay is not UNSET:
            field_dict["delay"] = delay
        if timeout is not UNSET:
            field_dict["timeout"] = timeout
        if max_retries is not UNSET:
            field_dict["max_retries"] = max_retries
        if max_retries_down is not UNSET:
            field_dict["max_retries_down"] = max_retries_down

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name", UNSET)

        delay = d.pop("delay", UNSET)

        timeout = d.pop("timeout", UNSET)

        max_retries = d.pop("max_retries", UNSET)

        max_retries_down = d.pop("max_retries_down", UNSET)

        patched_update_health_monitor_request = cls(
            name=name,
            delay=delay,
            timeout=timeout,
            max_retries=max_retries,
            max_retries_down=max_retries_down,
        )

        patched_update_health_monitor_request.additional_properties = d
        return patched_update_health_monitor_request

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
