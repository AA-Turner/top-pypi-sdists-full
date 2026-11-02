import datetime
from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.get_health_status_response_200_status import GetHealthStatusResponse200Status

T = TypeVar("T", bound="GetHealthStatusResponse200")


@_attrs_define
class GetHealthStatusResponse200:
    """Health status response (cached with 5s TTL)

    Attributes:
        status (GetHealthStatusResponse200Status): Overall health status
        checked_at (datetime.datetime): Timestamp when the health check was actually performed (not cache return time)
        database_healthy (bool): Whether the database is reachable
        workers_alive (int): Number of workers that pinged within last 5 minutes
    """

    status: GetHealthStatusResponse200Status
    checked_at: datetime.datetime
    database_healthy: bool
    workers_alive: int
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        status = self.status.value

        checked_at = self.checked_at.isoformat()

        database_healthy = self.database_healthy
        workers_alive = self.workers_alive

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "status": status,
                "checked_at": checked_at,
                "database_healthy": database_healthy,
                "workers_alive": workers_alive,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        status = GetHealthStatusResponse200Status(d.pop("status"))

        checked_at = isoparse(d.pop("checked_at"))

        database_healthy = d.pop("database_healthy")

        workers_alive = d.pop("workers_alive")

        get_health_status_response_200 = cls(
            status=status,
            checked_at=checked_at,
            database_healthy=database_healthy,
            workers_alive=workers_alive,
        )

        get_health_status_response_200.additional_properties = d
        return get_health_status_response_200

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
