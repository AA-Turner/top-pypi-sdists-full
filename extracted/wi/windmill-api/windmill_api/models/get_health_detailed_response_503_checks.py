from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_health_detailed_response_503_checks_database import GetHealthDetailedResponse503ChecksDatabase
    from ..models.get_health_detailed_response_503_checks_queue import GetHealthDetailedResponse503ChecksQueue
    from ..models.get_health_detailed_response_503_checks_readiness import GetHealthDetailedResponse503ChecksReadiness
    from ..models.get_health_detailed_response_503_checks_workers import GetHealthDetailedResponse503ChecksWorkers


T = TypeVar("T", bound="GetHealthDetailedResponse503Checks")


@_attrs_define
class GetHealthDetailedResponse503Checks:
    """Detailed health checks

    Attributes:
        database (GetHealthDetailedResponse503ChecksDatabase): Database health status
        readiness (GetHealthDetailedResponse503ChecksReadiness): Server readiness status
        workers (Union[Unset, None, GetHealthDetailedResponse503ChecksWorkers]): Workers health status
        queue (Union[Unset, None, GetHealthDetailedResponse503ChecksQueue]): Job queue status
    """

    database: "GetHealthDetailedResponse503ChecksDatabase"
    readiness: "GetHealthDetailedResponse503ChecksReadiness"
    workers: Union[Unset, None, "GetHealthDetailedResponse503ChecksWorkers"] = UNSET
    queue: Union[Unset, None, "GetHealthDetailedResponse503ChecksQueue"] = UNSET
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
        from ..models.get_health_detailed_response_503_checks_database import GetHealthDetailedResponse503ChecksDatabase
        from ..models.get_health_detailed_response_503_checks_queue import GetHealthDetailedResponse503ChecksQueue
        from ..models.get_health_detailed_response_503_checks_readiness import (
            GetHealthDetailedResponse503ChecksReadiness,
        )
        from ..models.get_health_detailed_response_503_checks_workers import GetHealthDetailedResponse503ChecksWorkers

        d = src_dict.copy()
        database = GetHealthDetailedResponse503ChecksDatabase.from_dict(d.pop("database"))

        readiness = GetHealthDetailedResponse503ChecksReadiness.from_dict(d.pop("readiness"))

        _workers = d.pop("workers", UNSET)
        workers: Union[Unset, None, GetHealthDetailedResponse503ChecksWorkers]
        if _workers is None:
            workers = None
        elif isinstance(_workers, Unset):
            workers = UNSET
        else:
            workers = GetHealthDetailedResponse503ChecksWorkers.from_dict(_workers)

        _queue = d.pop("queue", UNSET)
        queue: Union[Unset, None, GetHealthDetailedResponse503ChecksQueue]
        if _queue is None:
            queue = None
        elif isinstance(_queue, Unset):
            queue = UNSET
        else:
            queue = GetHealthDetailedResponse503ChecksQueue.from_dict(_queue)

        get_health_detailed_response_503_checks = cls(
            database=database,
            readiness=readiness,
            workers=workers,
            queue=queue,
        )

        get_health_detailed_response_503_checks.additional_properties = d
        return get_health_detailed_response_503_checks

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
