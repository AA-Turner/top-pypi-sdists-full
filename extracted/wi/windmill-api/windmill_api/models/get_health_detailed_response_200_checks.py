from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_health_detailed_response_200_checks_database import GetHealthDetailedResponse200ChecksDatabase
    from ..models.get_health_detailed_response_200_checks_queue import GetHealthDetailedResponse200ChecksQueue
    from ..models.get_health_detailed_response_200_checks_readiness import GetHealthDetailedResponse200ChecksReadiness
    from ..models.get_health_detailed_response_200_checks_workers import GetHealthDetailedResponse200ChecksWorkers


T = TypeVar("T", bound="GetHealthDetailedResponse200Checks")


@_attrs_define
class GetHealthDetailedResponse200Checks:
    """Detailed health checks

    Attributes:
        database (GetHealthDetailedResponse200ChecksDatabase): Database health status
        readiness (GetHealthDetailedResponse200ChecksReadiness): Server readiness status
        workers (Union[Unset, None, GetHealthDetailedResponse200ChecksWorkers]): Workers health status
        queue (Union[Unset, None, GetHealthDetailedResponse200ChecksQueue]): Job queue status
    """

    database: "GetHealthDetailedResponse200ChecksDatabase"
    readiness: "GetHealthDetailedResponse200ChecksReadiness"
    workers: Union[Unset, None, "GetHealthDetailedResponse200ChecksWorkers"] = UNSET
    queue: Union[Unset, None, "GetHealthDetailedResponse200ChecksQueue"] = UNSET
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
        from ..models.get_health_detailed_response_200_checks_database import GetHealthDetailedResponse200ChecksDatabase
        from ..models.get_health_detailed_response_200_checks_queue import GetHealthDetailedResponse200ChecksQueue
        from ..models.get_health_detailed_response_200_checks_readiness import (
            GetHealthDetailedResponse200ChecksReadiness,
        )
        from ..models.get_health_detailed_response_200_checks_workers import GetHealthDetailedResponse200ChecksWorkers

        d = src_dict.copy()
        database = GetHealthDetailedResponse200ChecksDatabase.from_dict(d.pop("database"))

        readiness = GetHealthDetailedResponse200ChecksReadiness.from_dict(d.pop("readiness"))

        _workers = d.pop("workers", UNSET)
        workers: Union[Unset, None, GetHealthDetailedResponse200ChecksWorkers]
        if _workers is None:
            workers = None
        elif isinstance(_workers, Unset):
            workers = UNSET
        else:
            workers = GetHealthDetailedResponse200ChecksWorkers.from_dict(_workers)

        _queue = d.pop("queue", UNSET)
        queue: Union[Unset, None, GetHealthDetailedResponse200ChecksQueue]
        if _queue is None:
            queue = None
        elif isinstance(_queue, Unset):
            queue = UNSET
        else:
            queue = GetHealthDetailedResponse200ChecksQueue.from_dict(_queue)

        get_health_detailed_response_200_checks = cls(
            database=database,
            readiness=readiness,
            workers=workers,
            queue=queue,
        )

        get_health_detailed_response_200_checks.additional_properties = d
        return get_health_detailed_response_200_checks

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
