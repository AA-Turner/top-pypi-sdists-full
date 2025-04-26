from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal, Mapping, Optional, Union

from typing_extensions import final

from chalk.features import Feature
from chalk.sql import IncrementalSettings
from chalk.sql.finalized_query import DataframeFinalizedChalkQuery, Finalizer, SingletonFinalizedChalkQuery
from chalk.sql.protocols import BaseSQLSourceProtocol, StringChalkQueryProtocol
from chalk.utils.duration import Duration, parse_chalk_duration
from chalk.utils.missing_dependency import missing_dependency_exception

if TYPE_CHECKING:
    from sqlalchemy.sql.elements import TextClause


@final
class StringChalkQuery(StringChalkQueryProtocol):
    def __init__(
        self,
        source: BaseSQLSourceProtocol,
        params: Mapping[str, Any],
        query: Union[str, TextClause],
        fields: Mapping[str, Feature],
    ):
        super().__init__()
        try:
            from sqlalchemy import text
        except ImportError:
            raise missing_dependency_exception("chalkpy[sql]")
        self._source = source
        self._query = text(query) if isinstance(query, str) else query
        self._params = params
        self._fields = {k: Feature.from_root_fqn(v) if isinstance(v, str) else v for (k, v) in fields.items()}

    @classmethod
    def __init_subclass__(cls, **kwargs: Any):
        raise RuntimeError(
            "The StringChalkQuery class should not be subclassed. The Chalk runtime assumes that this class is final."
        )

    def __repr__(self):
        return f"StringChalkQuery(query='{self._query}')"

    def one_or_none(self) -> SingletonFinalizedChalkQuery:
        return SingletonFinalizedChalkQuery(
            query=self._query,
            params=self._params,
            finalizer=Finalizer.ONE_OR_NONE,
            incremental_settings=None,
            source=self._source,
            fields=self._fields,
        )

    def one(self) -> SingletonFinalizedChalkQuery:
        return SingletonFinalizedChalkQuery(
            query=self._query,
            params=self._params,
            finalizer=Finalizer.ONE,
            incremental_settings=None,
            source=self._source,
            fields=self._fields,
        )

    def first(self) -> SingletonFinalizedChalkQuery:
        return SingletonFinalizedChalkQuery(
            query=self._query,
            params=self._params,
            finalizer=Finalizer.FIRST,
            incremental_settings=None,
            source=self._source,
            fields=self._fields,
        )

    def all(self) -> DataframeFinalizedChalkQuery:
        return DataframeFinalizedChalkQuery(
            query=self._query,
            params=self._params,
            finalizer=Finalizer.ALL,
            incremental_settings=None,
            source=self._source,
            fields=self._fields,
        )

    def incremental(
        self,
        *,
        incremental_column: Optional[str] = None,
        lookback_period: Duration | None = "0s",
        mode: Literal["row", "group", "parameter"] = "row",
        incremental_timestamp: Literal["feature_time", "resolver_execution_time"] = "feature_time",
    ) -> DataframeFinalizedChalkQuery:
        if mode in {"row", "group"} and incremental_column is None:
            raise ValueError(f"incremental mode set to '{mode}' but no 'incremental_column' argument was passed.")

        if mode == "parameter" and incremental_column is not None:
            raise ValueError(
                f"incremental mode set to '{mode}' but 'incremental_column' argument was passed."
                + " Please view documentation for proper usage."
            )

        return DataframeFinalizedChalkQuery(
            query=self._query,
            params=self._params,
            finalizer=Finalizer.ALL,
            incremental_settings=IncrementalSettings(
                lookback_period=parse_chalk_duration(lookback_period) if lookback_period is not None else None,
                incremental_column=None if incremental_column is None else incremental_column,
                mode=mode,
                incremental_timestamp=incremental_timestamp,
            ),
            source=self._source,
            fields=self._fields,
        )
