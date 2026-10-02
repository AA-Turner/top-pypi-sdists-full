from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateHealthMonitor")


@_attrs_define
class UpdateHealthMonitor:
    """
    Attributes:
        url (str):
        uuid (UUID):
        name (Union[Unset, str]):
        delay (Union[Unset, int]): Interval between health checks in seconds Default: 5.
        timeout (Union[Unset, int]): Time in seconds to timeout a health check Default: 5.
        max_retries (Union[Unset, int]):  Default: 3.
        max_retries_down (Union[Unset, int]):  Default: 3.
    """

    url: str
    uuid: UUID
    name: Union[Unset, str] = UNSET
    delay: Union[Unset, int] = 5
    timeout: Union[Unset, int] = 5
    max_retries: Union[Unset, int] = 3
    max_retries_down: Union[Unset, int] = 3
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        name = self.name

        delay = self.delay

        timeout = self.timeout

        max_retries = self.max_retries

        max_retries_down = self.max_retries_down

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
            }
        )
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
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        name = d.pop("name", UNSET)

        delay = d.pop("delay", UNSET)

        timeout = d.pop("timeout", UNSET)

        max_retries = d.pop("max_retries", UNSET)

        max_retries_down = d.pop("max_retries_down", UNSET)

        update_health_monitor = cls(
            url=url,
            uuid=uuid,
            name=name,
            delay=delay,
            timeout=timeout,
            max_retries=max_retries,
            max_retries_down=max_retries_down,
        )

        update_health_monitor.additional_properties = d
        return update_health_monitor

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
