from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.health_checks_database import HealthChecksDatabase
    from ..models.health_checks_queue import HealthChecksQueue
    from ..models.health_checks_readiness import HealthChecksReadiness
    from ..models.health_checks_workers import HealthChecksWorkers


T = TypeVar("T", bound="HealthChecks")


@_attrs_define
class HealthChecks:
    """Detailed health checks

    Attributes:
        database (HealthChecksDatabase): Database health status
        readiness (HealthChecksReadiness): Server readiness status
        workers (Union[Unset, None, HealthChecksWorkers]): Workers health status
        queue (Union[Unset, None, HealthChecksQueue]): Job queue status
    """

    database: "HealthChecksDatabase"
    readiness: "HealthChecksReadiness"
    workers: Union[Unset, None, "HealthChecksWorkers"] = UNSET
    queue: Union[Unset, None, "HealthChecksQueue"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        database = self.database.to_dict()

        readiness = self.readiness.to_dict()

        workers: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.workers, Unset):
            workers = self.workers.to_dict() if self.workers else None

        queue: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.queue, Unset):
            queue = self.queue.to_dict() if self.queue else None

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "database": database,
                "readiness": readiness,
            }
        )
        if workers is not UNSET:
            field_dict["workers"] = workers
        if queue is not UNSET:
            field_dict["queue"] = queue

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.health_checks_database import HealthChecksDatabase
        from ..models.health_checks_queue import HealthChecksQueue
        from ..models.health_checks_readiness import HealthChecksReadiness
        from ..models.health_checks_workers import HealthChecksWorkers

        d = src_dict.copy()
        database = HealthChecksDatabase.from_dict(d.pop("database"))

        readiness = HealthChecksReadiness.from_dict(d.pop("readiness"))

        _workers = d.pop("workers", UNSET)
        workers: Union[Unset, None, HealthChecksWorkers]
        if _workers is None:
            workers = None
        elif isinstance(_workers, Unset):
            workers = UNSET
        else:
            workers = HealthChecksWorkers.from_dict(_workers)

        _queue = d.pop("queue", UNSET)
        queue: Union[Unset, None, HealthChecksQueue]
        if _queue is None:
            queue = None
        elif isinstance(_queue, Unset):
            queue = UNSET
        else:
            queue = HealthChecksQueue.from_dict(_queue)

        health_checks = cls(
            database=database,
            readiness=readiness,
            workers=workers,
            queue=queue,
        )

        health_checks.additional_properties = d
        return health_checks

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
