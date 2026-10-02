import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="HelpdeskHealth")


@_attrs_define
class HelpdeskHealth:
    """
    Attributes:
        provider_name (str):
        backend_type (str):
        is_active (bool):
        health_status (str):
        last_health_check (Union[None, datetime.datetime]):
        failed_routing_count (int):
    """

    provider_name: str
    backend_type: str
    is_active: bool
    health_status: str
    last_health_check: Union[None, datetime.datetime]
    failed_routing_count: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        provider_name = self.provider_name

        backend_type = self.backend_type

        is_active = self.is_active

        health_status = self.health_status

        last_health_check: Union[None, str]
        if isinstance(self.last_health_check, datetime.datetime):
            last_health_check = self.last_health_check.isoformat()
        else:
            last_health_check = self.last_health_check

        failed_routing_count = self.failed_routing_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "provider_name": provider_name,
                "backend_type": backend_type,
                "is_active": is_active,
                "health_status": health_status,
                "last_health_check": last_health_check,
                "failed_routing_count": failed_routing_count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        provider_name = d.pop("provider_name")

        backend_type = d.pop("backend_type")

        is_active = d.pop("is_active")

        health_status = d.pop("health_status")

        def _parse_last_health_check(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_health_check_type_0 = isoparse(data)

                return last_health_check_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        last_health_check = _parse_last_health_check(d.pop("last_health_check"))

        failed_routing_count = d.pop("failed_routing_count")

        helpdesk_health = cls(
            provider_name=provider_name,
            backend_type=backend_type,
            is_active=is_active,
            health_status=health_status,
            last_health_check=last_health_check,
            failed_routing_count=failed_routing_count,
        )

        helpdesk_health.additional_properties = d
        return helpdesk_health

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
