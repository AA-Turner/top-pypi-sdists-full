from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.active_query import ActiveQuery


T = TypeVar("T", bound="ActiveQueriesStats")


@_attrs_define
class ActiveQueriesStats:
    """
    Attributes:
        count (int): Number of currently active queries
        longest_duration_seconds (float): Duration of the longest running query in seconds
        waiting_on_locks (int): Number of queries waiting on locks
        queries (list['ActiveQuery']): List of active queries
    """

    count: int
    longest_duration_seconds: float
    waiting_on_locks: int
    queries: list["ActiveQuery"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        count = self.count

        longest_duration_seconds = self.longest_duration_seconds

        waiting_on_locks = self.waiting_on_locks

        queries = []
        for queries_item_data in self.queries:
            queries_item = queries_item_data.to_dict()
            queries.append(queries_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "count": count,
                "longest_duration_seconds": longest_duration_seconds,
                "waiting_on_locks": waiting_on_locks,
                "queries": queries,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.active_query import ActiveQuery

        d = dict(src_dict)
        count = d.pop("count")

        longest_duration_seconds = d.pop("longest_duration_seconds")

        waiting_on_locks = d.pop("waiting_on_locks")

        queries = []
        _queries = d.pop("queries")
        for queries_item_data in _queries:
            queries_item = ActiveQuery.from_dict(queries_item_data)

            queries.append(queries_item)

        active_queries_stats = cls(
            count=count,
            longest_duration_seconds=longest_duration_seconds,
            waiting_on_locks=waiting_on_locks,
            queries=queries,
        )

        active_queries_stats.additional_properties = d
        return active_queries_stats

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
