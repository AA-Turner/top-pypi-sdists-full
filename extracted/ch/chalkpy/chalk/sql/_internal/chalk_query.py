from typing import Any, List, Literal, Mapping, Optional, Union

from typing_extensions import final

from chalk.features import Feature
from chalk.sql.finalized_query import DataframeFinalizedChalkQuery, Finalizer, SingletonFinalizedChalkQuery
from chalk.sql.protocols import BaseSQLSourceProtocol, ChalkQueryProtocol, IncrementalSettings
from chalk.utils.duration import Duration, parse_chalk_duration
from chalk.utils.missing_dependency import missing_dependency_exception


@final
class ChalkQuery(ChalkQueryProtocol):
    def __init__(
        self,
        features: Mapping[str, Feature],
        targets: List[Any],
        source: BaseSQLSourceProtocol,
    ):
        super().__init__()
        try:
            from sqlalchemy.orm import Query
        except ImportError:
            raise missing_dependency_exception("chalkpy[sql]")
        self._query = Query(entities=targets)
        self._features = features
        self._source = source

    @classmethod
    def __init_subclass__(cls, **kwargs: Any):
        raise RuntimeError(
            "The ChalkQuery class should not be subclassed. The Chalk runtime assumes that this class is final."
        )

    def first(self, params: Optional[Mapping[str, Any]] = None) -> SingletonFinalizedChalkQuery:
        from sqlalchemy.sql import Select

        self._query = self._query.limit(1)
        assert isinstance(self._query.selectable, Select), "A text query's selectable should always be a Select"
        return SingletonFinalizedChalkQuery(
            query=self._query.selectable,
            finalizer=Finalizer.FIRST,
            source=self._source,
            incremental_settings=None,
            params=params or {},
            fields=self._features,
        )

    def one_or_none(self, params: Optional[Mapping[str, Any]] = None) -> SingletonFinalizedChalkQuery:
        from sqlalchemy.sql import Select

        self._query = self._query.limit(1)
        assert isinstance(self._query.selectable, Select), "A text query's selectable should always be a Select"
        return SingletonFinalizedChalkQuery(
            query=self._query.selectable,
            finalizer=Finalizer.ONE_OR_NONE,
            source=self._source,
            incremental_settings=None,
            params=params or {},
            fields=self._features,
        )

    def one(self, params: Optional[Mapping[str, Any]] = None) -> SingletonFinalizedChalkQuery:
        from sqlalchemy.sql import Select

        self._query = self._query.limit(1)
        assert isinstance(self._query.selectable, Select), "A text query's selectable should always be a Select"
        return SingletonFinalizedChalkQuery(
            query=self._query.selectable,
            finalizer=Finalizer.ONE,
            source=self._source,
            incremental_settings=None,
            params=params or {},
            fields=self._features,
        )

    def all(self, params: Optional[Mapping[str, Any]] = None) -> DataframeFinalizedChalkQuery:
        from sqlalchemy.sql import Select

        assert isinstance(self._query.selectable, Select), "A text query's selectable should always be a Select"
        return DataframeFinalizedChalkQuery(
            query=self._query.selectable,
            finalizer=Finalizer.ALL,
            source=self._source,
            incremental_settings=None,
            params=params or {},
            fields=self._features,
        )

    def incremental(
        self,
        lookback_period: Duration = "0s",
        mode: Literal["row", "group", "parameter"] = "row",
        incremental_column: Optional[Union[str, Feature]] = None,
        incremental_timestamp: Literal["feature_time", "resolver_execution_time"] = "feature_time",
        params: Optional[Mapping[str, Any]] = None,
    ) -> DataframeFinalizedChalkQuery:
        from sqlalchemy.sql import Select

        assert isinstance(self._query.selectable, Select)
        return DataframeFinalizedChalkQuery(
            query=self._query.selectable,
            finalizer=Finalizer.ALL,
            source=self._source,
            incremental_settings=IncrementalSettings(
                lookback_period=parse_chalk_duration(lookback_period),
                incremental_column=None if incremental_column is None else str(incremental_column),
                mode=mode,
                incremental_timestamp=incremental_timestamp,
            ),
            params=params or {},
            fields=self._features,
        )

    def filter_by(self, **kwargs: Any):
        self._query = self._query.filter_by(**kwargs)
        return self

    def filter(self, *criterion: Any):
        self._query = self._query.filter(*criterion)
        return self

    def limit(self, *limits: Any):
        self._query = self._query.limit(*limits)
        return self

    def order_by(self, *clauses: Any):
        self._query = self._query.order_by(*clauses)
        return self

    def group_by(self, *clauses: Any):
        self._query = self._query.group_by(*clauses)
        return self

    def having(self, criterion: Any):
        self._query = self._query.having(*criterion)
        return self

    def union(self, *q: Any):
        self._query = self._query.union(*q)
        return self

    def union_all(self, *q: Any):
        self._query = self._query.union_all(*q)
        return self

    def intersect(self, *q: Any):
        self._query = self._query.intersect(*q)
        return self

    def intersect_all(self, *q: Any):
        self._query = self._query.intersect_all(*q)
        return self

    def join(self, target: Any, *props: Any, **kwargs: Any):
        self._query = self._query.join(target, *props, **kwargs)
        return self

    def outerjoin(self, target: Any, *props: Any, **kwargs: Any):
        self._query = self._query.outerjoin(target, *props, **kwargs)
        return self

    def select_from(self, *from_obj: Any):
        self._query = self._query.select_from(*from_obj)
        return self
