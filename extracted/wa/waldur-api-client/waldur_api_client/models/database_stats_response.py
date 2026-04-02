from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.active_queries_stats import ActiveQueriesStats
    from ..models.cache_performance import CachePerformance
    from ..models.connection_stats import ConnectionStats
    from ..models.database_size_stats import DatabaseSizeStats
    from ..models.lock_stats import LockStats
    from ..models.maintenance_stats import MaintenanceStats
    from ..models.query_performance import QueryPerformance
    from ..models.replication_stats import ReplicationStats
    from ..models.table_size import TableSize
    from ..models.transaction_stats import TransactionStats


T = TypeVar("T", bound="DatabaseStatsResponse")


@_attrs_define
class DatabaseStatsResponse:
    """
    Attributes:
        table_stats (list['TableSize']): Top largest tables by size
        connections (ConnectionStats):
        database_size (DatabaseSizeStats):
        cache_performance (CachePerformance):
        transactions (TransactionStats):
        locks (LockStats):
        maintenance (MaintenanceStats):
        active_queries (ActiveQueriesStats):
        query_performance (QueryPerformance):
        replication (ReplicationStats):
    """

    table_stats: list["TableSize"]
    connections: "ConnectionStats"
    database_size: "DatabaseSizeStats"
    cache_performance: "CachePerformance"
    transactions: "TransactionStats"
    locks: "LockStats"
    maintenance: "MaintenanceStats"
    active_queries: "ActiveQueriesStats"
    query_performance: "QueryPerformance"
    replication: "ReplicationStats"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        table_stats = []
        for table_stats_item_data in self.table_stats:
            table_stats_item = table_stats_item_data.to_dict()
            table_stats.append(table_stats_item)

        connections = self.connections.to_dict()

        database_size = self.database_size.to_dict()

        cache_performance = self.cache_performance.to_dict()

        transactions = self.transactions.to_dict()

        locks = self.locks.to_dict()

        maintenance = self.maintenance.to_dict()

        active_queries = self.active_queries.to_dict()

        query_performance = self.query_performance.to_dict()

        replication = self.replication.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "table_stats": table_stats,
                "connections": connections,
                "database_size": database_size,
                "cache_performance": cache_performance,
                "transactions": transactions,
                "locks": locks,
                "maintenance": maintenance,
                "active_queries": active_queries,
                "query_performance": query_performance,
                "replication": replication,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.active_queries_stats import ActiveQueriesStats
        from ..models.cache_performance import CachePerformance
        from ..models.connection_stats import ConnectionStats
        from ..models.database_size_stats import DatabaseSizeStats
        from ..models.lock_stats import LockStats
        from ..models.maintenance_stats import MaintenanceStats
        from ..models.query_performance import QueryPerformance
        from ..models.replication_stats import ReplicationStats
        from ..models.table_size import TableSize
        from ..models.transaction_stats import TransactionStats

        d = dict(src_dict)
        table_stats = []
        _table_stats = d.pop("table_stats")
        for table_stats_item_data in _table_stats:
            table_stats_item = TableSize.from_dict(table_stats_item_data)

            table_stats.append(table_stats_item)

        connections = ConnectionStats.from_dict(d.pop("connections"))

        database_size = DatabaseSizeStats.from_dict(d.pop("database_size"))

        cache_performance = CachePerformance.from_dict(d.pop("cache_performance"))

        transactions = TransactionStats.from_dict(d.pop("transactions"))

        locks = LockStats.from_dict(d.pop("locks"))

        maintenance = MaintenanceStats.from_dict(d.pop("maintenance"))

        active_queries = ActiveQueriesStats.from_dict(d.pop("active_queries"))

        query_performance = QueryPerformance.from_dict(d.pop("query_performance"))

        replication = ReplicationStats.from_dict(d.pop("replication"))

        database_stats_response = cls(
            table_stats=table_stats,
            connections=connections,
            database_size=database_size,
            cache_performance=cache_performance,
            transactions=transactions,
            locks=locks,
            maintenance=maintenance,
            active_queries=active_queries,
            query_performance=query_performance,
            replication=replication,
        )

        database_stats_response.additional_properties = d
        return database_stats_response

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
