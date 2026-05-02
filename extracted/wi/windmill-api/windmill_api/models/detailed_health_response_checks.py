from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.detailed_health_response_checks_database import DetailedHealthResponseChecksDatabase
    from ..models.detailed_health_response_checks_queue import DetailedHealthResponseChecksQueue
    from ..models.detailed_health_response_checks_readiness import DetailedHealthResponseChecksReadiness
    from ..models.detailed_health_response_checks_workers import DetailedHealthResponseChecksWorkers


T = TypeVar("T", bound="DetailedHealthResponseChecks")


@_attrs_define
class DetailedHealthResponseChecks:
    """Detailed health checks

    Attributes:
        database (DetailedHealthResponseChecksDatabase): Database health status
        readiness (DetailedHealthResponseChecksReadiness): Server readiness status
        workers (Union[Unset, None, DetailedHealthResponseChecksWorkers]): Workers health status
        queue (Union[Unset, None, DetailedHealthResponseChecksQueue]): Job queue status
    """

    database: "DetailedHealthResponseChecksDatabase"
    readiness: "DetailedHealthResponseChecksReadiness"
    workers: Union[Unset, None, "DetailedHealthResponseChecksWorkers"] = UNSET
    queue: Union[Unset, None, "DetailedHealthResponseChecksQueue"] = UNSET
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
        from ..models.detailed_health_response_checks_database import DetailedHealthResponseChecksDatabase
        from ..models.detailed_health_response_checks_queue import DetailedHealthResponseChecksQueue
        from ..models.detailed_health_response_checks_readiness import DetailedHealthResponseChecksReadiness
        from ..models.detailed_health_response_checks_workers import DetailedHealthResponseChecksWorkers

        d = src_dict.copy()
        database = DetailedHealthResponseChecksDatabase.from_dict(d.pop("database"))

        readiness = DetailedHealthResponseChecksReadiness.from_dict(d.pop("readiness"))

        _workers = d.pop("workers", UNSET)
        workers: Union[Unset, None, DetailedHealthResponseChecksWorkers]
        if _workers is None:
            workers = None
        elif isinstance(_workers, Unset):
            workers = UNSET
        else:
            workers = DetailedHealthResponseChecksWorkers.from_dict(_workers)

        _queue = d.pop("queue", UNSET)
        queue: Union[Unset, None, DetailedHealthResponseChecksQueue]
        if _queue is None:
            queue = None
        elif isinstance(_queue, Unset):
            queue = UNSET
        else:
            queue = DetailedHealthResponseChecksQueue.from_dict(_queue)

        detailed_health_response_checks = cls(
            database=database,
            readiness=readiness,
            workers=workers,
            queue=queue,
        )

        detailed_health_response_checks.additional_properties = d
        return detailed_health_response_checks

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
