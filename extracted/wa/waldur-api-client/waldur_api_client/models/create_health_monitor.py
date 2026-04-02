from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.load_balancer_protocol_enum import LoadBalancerProtocolEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateHealthMonitor")


@_attrs_define
class CreateHealthMonitor:
    """
    Attributes:
        url (str):
        uuid (UUID):
        pool (str): Pool this health monitor belongs to
        type_ (LoadBalancerProtocolEnum):
        delay (int): Interval between health checks in seconds
        timeout (int): Time in seconds to timeout a health check
        max_retries (int): Number of retries before marking member as down
        project (str):
        service_settings (str):
        name (Union[Unset, str]):
    """

    url: str
    uuid: UUID
    pool: str
    type_: LoadBalancerProtocolEnum
    delay: int
    timeout: int
    max_retries: int
    project: str
    service_settings: str
    name: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        pool = self.pool

        type_ = self.type_.value

        delay = self.delay

        timeout = self.timeout

        max_retries = self.max_retries

        project = self.project

        service_settings = self.service_settings

        name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "pool": pool,
                "type": type_,
                "delay": delay,
                "timeout": timeout,
                "max_retries": max_retries,
                "project": project,
                "service_settings": service_settings,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        pool = d.pop("pool")

        type_ = LoadBalancerProtocolEnum(d.pop("type"))

        delay = d.pop("delay")

        timeout = d.pop("timeout")

        max_retries = d.pop("max_retries")

        project = d.pop("project")

        service_settings = d.pop("service_settings")

        name = d.pop("name", UNSET)

        create_health_monitor = cls(
            url=url,
            uuid=uuid,
            pool=pool,
            type_=type_,
            delay=delay,
            timeout=timeout,
            max_retries=max_retries,
            project=project,
            service_settings=service_settings,
            name=name,
        )

        create_health_monitor.additional_properties = d
        return create_health_monitor

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
