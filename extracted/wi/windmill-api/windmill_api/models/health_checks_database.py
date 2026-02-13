from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.health_checks_database_pool import HealthChecksDatabasePool


T = TypeVar("T", bound="HealthChecksDatabase")


@_attrs_define
class HealthChecksDatabase:
    """Database health status

    Attributes:
        healthy (bool): Whether the database is reachable
        latency_ms (int): Database query latency in milliseconds
        pool (HealthChecksDatabasePool): Database connection pool statistics
    """

    healthy: bool
    latency_ms: int
    pool: "HealthChecksDatabasePool"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        healthy = self.healthy
        latency_ms = self.latency_ms
        pool = self.pool.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "healthy": healthy,
                "latency_ms": latency_ms,
                "pool": pool,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.health_checks_database_pool import HealthChecksDatabasePool

        d = src_dict.copy()
        healthy = d.pop("healthy")

        latency_ms = d.pop("latency_ms")

        pool = HealthChecksDatabasePool.from_dict(d.pop("pool"))

        health_checks_database = cls(
            healthy=healthy,
            latency_ms=latency_ms,
            pool=pool,
        )

        health_checks_database.additional_properties = d
        return health_checks_database

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
