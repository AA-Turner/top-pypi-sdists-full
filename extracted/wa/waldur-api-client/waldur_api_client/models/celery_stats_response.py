from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.celery_stats_response_active_type_0 import CeleryStatsResponseActiveType0
    from ..models.celery_stats_response_query_task_type_0 import CeleryStatsResponseQueryTaskType0
    from ..models.celery_stats_response_reserved_type_0 import CeleryStatsResponseReservedType0
    from ..models.celery_stats_response_revoked_type_0 import CeleryStatsResponseRevokedType0
    from ..models.celery_stats_response_scheduled_type_0 import CeleryStatsResponseScheduledType0
    from ..models.celery_stats_response_stats_type_0 import CeleryStatsResponseStatsType0


T = TypeVar("T", bound="CeleryStatsResponse")


@_attrs_define
class CeleryStatsResponse:
    """
    Attributes:
        active (Union['CeleryStatsResponseActiveType0', None]): Currently executing tasks per worker. Keys are worker
            names, values are lists of active tasks.
        scheduled (Union['CeleryStatsResponseScheduledType0', None]): Tasks scheduled for future execution per worker.
            Keys are worker names, values are lists of scheduled tasks with ETA.
        reserved (Union['CeleryStatsResponseReservedType0', None]): Tasks that have been received but not yet started
            per worker. Keys are worker names, values are lists of reserved tasks.
        revoked (Union['CeleryStatsResponseRevokedType0', None]): IDs of revoked (cancelled) tasks per worker. Keys are
            worker names, values are lists of task IDs.
        query_task (Union['CeleryStatsResponseQueryTaskType0', None]): Query results for specific tasks. May be null if
            no query was performed.
        stats (Union['CeleryStatsResponseStatsType0', None]): Detailed statistics per worker including uptime, pool
            info, and resource usage. Keys are worker names.
    """

    active: Union["CeleryStatsResponseActiveType0", None]
    scheduled: Union["CeleryStatsResponseScheduledType0", None]
    reserved: Union["CeleryStatsResponseReservedType0", None]
    revoked: Union["CeleryStatsResponseRevokedType0", None]
    query_task: Union["CeleryStatsResponseQueryTaskType0", None]
    stats: Union["CeleryStatsResponseStatsType0", None]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.celery_stats_response_active_type_0 import CeleryStatsResponseActiveType0
        from ..models.celery_stats_response_query_task_type_0 import CeleryStatsResponseQueryTaskType0
        from ..models.celery_stats_response_reserved_type_0 import CeleryStatsResponseReservedType0
        from ..models.celery_stats_response_revoked_type_0 import CeleryStatsResponseRevokedType0
        from ..models.celery_stats_response_scheduled_type_0 import CeleryStatsResponseScheduledType0
        from ..models.celery_stats_response_stats_type_0 import CeleryStatsResponseStatsType0

        active: Union[None, dict[str, Any]]
        if isinstance(self.active, CeleryStatsResponseActiveType0):
            active = self.active.to_dict()
        else:
            active = self.active

        scheduled: Union[None, dict[str, Any]]
        if isinstance(self.scheduled, CeleryStatsResponseScheduledType0):
            scheduled = self.scheduled.to_dict()
        else:
            scheduled = self.scheduled

        reserved: Union[None, dict[str, Any]]
        if isinstance(self.reserved, CeleryStatsResponseReservedType0):
            reserved = self.reserved.to_dict()
        else:
            reserved = self.reserved

        revoked: Union[None, dict[str, Any]]
        if isinstance(self.revoked, CeleryStatsResponseRevokedType0):
            revoked = self.revoked.to_dict()
        else:
            revoked = self.revoked

        query_task: Union[None, dict[str, Any]]
        if isinstance(self.query_task, CeleryStatsResponseQueryTaskType0):
            query_task = self.query_task.to_dict()
        else:
            query_task = self.query_task

        stats: Union[None, dict[str, Any]]
        if isinstance(self.stats, CeleryStatsResponseStatsType0):
            stats = self.stats.to_dict()
        else:
            stats = self.stats

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "active": active,
                "scheduled": scheduled,
                "reserved": reserved,
                "revoked": revoked,
                "query_task": query_task,
                "stats": stats,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.celery_stats_response_active_type_0 import CeleryStatsResponseActiveType0
        from ..models.celery_stats_response_query_task_type_0 import CeleryStatsResponseQueryTaskType0
        from ..models.celery_stats_response_reserved_type_0 import CeleryStatsResponseReservedType0
        from ..models.celery_stats_response_revoked_type_0 import CeleryStatsResponseRevokedType0
        from ..models.celery_stats_response_scheduled_type_0 import CeleryStatsResponseScheduledType0
        from ..models.celery_stats_response_stats_type_0 import CeleryStatsResponseStatsType0

        d = dict(src_dict)

        def _parse_active(data: object) -> Union["CeleryStatsResponseActiveType0", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                active_type_0 = CeleryStatsResponseActiveType0.from_dict(data)

                return active_type_0
            except:  # noqa: E722
                pass
            return cast(Union["CeleryStatsResponseActiveType0", None], data)

        active = _parse_active(d.pop("active"))

        def _parse_scheduled(data: object) -> Union["CeleryStatsResponseScheduledType0", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                scheduled_type_0 = CeleryStatsResponseScheduledType0.from_dict(data)

                return scheduled_type_0
            except:  # noqa: E722
                pass
            return cast(Union["CeleryStatsResponseScheduledType0", None], data)

        scheduled = _parse_scheduled(d.pop("scheduled"))

        def _parse_reserved(data: object) -> Union["CeleryStatsResponseReservedType0", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                reserved_type_0 = CeleryStatsResponseReservedType0.from_dict(data)

                return reserved_type_0
            except:  # noqa: E722
                pass
            return cast(Union["CeleryStatsResponseReservedType0", None], data)

        reserved = _parse_reserved(d.pop("reserved"))

        def _parse_revoked(data: object) -> Union["CeleryStatsResponseRevokedType0", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                revoked_type_0 = CeleryStatsResponseRevokedType0.from_dict(data)

                return revoked_type_0
            except:  # noqa: E722
                pass
            return cast(Union["CeleryStatsResponseRevokedType0", None], data)

        revoked = _parse_revoked(d.pop("revoked"))

        def _parse_query_task(data: object) -> Union["CeleryStatsResponseQueryTaskType0", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                query_task_type_0 = CeleryStatsResponseQueryTaskType0.from_dict(data)

                return query_task_type_0
            except:  # noqa: E722
                pass
            return cast(Union["CeleryStatsResponseQueryTaskType0", None], data)

        query_task = _parse_query_task(d.pop("query_task"))

        def _parse_stats(data: object) -> Union["CeleryStatsResponseStatsType0", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                stats_type_0 = CeleryStatsResponseStatsType0.from_dict(data)

                return stats_type_0
            except:  # noqa: E722
                pass
            return cast(Union["CeleryStatsResponseStatsType0", None], data)

        stats = _parse_stats(d.pop("stats"))

        celery_stats_response = cls(
            active=active,
            scheduled=scheduled,
            reserved=reserved,
            revoked=revoked,
            query_task=query_task,
            stats=stats,
        )

        celery_stats_response.additional_properties = d
        return celery_stats_response

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
