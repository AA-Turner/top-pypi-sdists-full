from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="HpcServiceHealth")


@_attrs_define
class HpcServiceHealth:
    """
    Attributes:
        service_type (Union[None, str]):
        healthy (Union[None, bool]):
        message (Union[None, Unset, str]):
        last_checked (Union[None, Unset, str]):
    """

    service_type: Union[None, str]
    healthy: Union[None, bool]
    message: Union[None, Unset, str] = UNSET
    last_checked: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        service_type: Union[None, str]
        service_type = self.service_type

        healthy: Union[None, bool]
        healthy = self.healthy

        message: Union[None, Unset, str]
        if isinstance(self.message, Unset):
            message = UNSET
        else:
            message = self.message

        last_checked: Union[None, Unset, str]
        if isinstance(self.last_checked, Unset):
            last_checked = UNSET
        else:
            last_checked = self.last_checked

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "service_type": service_type,
                "healthy": healthy,
            }
        )
        if message is not UNSET:
            field_dict["message"] = message
        if last_checked is not UNSET:
            field_dict["last_checked"] = last_checked

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_service_type(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        service_type = _parse_service_type(d.pop("service_type"))

        def _parse_healthy(data: object) -> Union[None, bool]:
            if data is None:
                return data
            return cast(Union[None, bool], data)

        healthy = _parse_healthy(d.pop("healthy"))

        def _parse_message(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        message = _parse_message(d.pop("message", UNSET))

        def _parse_last_checked(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        last_checked = _parse_last_checked(d.pop("last_checked", UNSET))

        hpc_service_health = cls(
            service_type=service_type,
            healthy=healthy,
            message=message,
            last_checked=last_checked,
        )

        hpc_service_health.additional_properties = d
        return hpc_service_health

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
