from __future__ import annotations

import traceback
import typing as t
from concurrent.futures import wait
from datetime import datetime, timezone

from query_cache_common.utils import extract_fqn_parts
from sqlglot import exp
from typing_extensions import override

from dbt_state import events
from dbt_state.adapters.base import BaseAdapterExtension
from dbt_state.adapters.common import EventualCache, ViewDefinition, ViewFetchResult

if t.TYPE_CHECKING:
    from dbt.adapters.base.relation import BaseRelation
    from google.cloud.bigquery import Table


class BigQueryAdapterExtension(BaseAdapterExtension):
    REQUIRES_NAMED_CONNECTION = False
    CLONE_CHAIN_DEPTH_LIMIT = 3

    def __init__(self, *args: t.Any, **kwargs: t.Any) -> None:
        super().__init__(*args, **kwargs)
        self._client = self.adapter.connections.get_thread_connection().handle
        self._table_cache: EventualCache[str, t.Optional[Table]] = EventualCache(
            ttl_seconds=kwargs.get("cache_ttl_seconds"),
            cache_name="bigquery_table_cache",
        )
        self._configure_http_pool()

    def current_timestamp_utc(self) -> datetime:
        epoch_micros = self.execute(
            "SELECT UNIX_MICROS(CURRENT_TIMESTAMP())",
            fetch=True,
        ).rows[0][0]
        return datetime.fromtimestamp(int(epoch_micros) / 1_000_000, tz=timezone.utc)

    def _configure_http_pool(self) -> None:
        # Google docs: https://docs.cloud.google.com/bigquery/docs/python-libraries#troubleshooting_connection_pool_errors
        try:
            from requests.adapters import HTTPAdapter

            pool_size = max(self._max_worker_threads or 10, 10)
            adapter = HTTPAdapter(pool_connections=pool_size, pool_maxsize=pool_size)
            self._client._http.mount("https://", adapter)  # noqa: SLF001
            self._client._http.mount("http://", adapter)  # noqa: SLF001
        except Exception:
            events.fire_debug_event(
                "Unable to configure BigQuery HTTP connection pool size. "
                "Connection pool warnings may occur with high thread counts."
            )

    def relation_exists(self, relation: BaseRelation) -> bool:
        if self.adapter._schema_is_cached(relation.database, relation.schema or ""):  # noqa: SLF001
            # If the adapter already cached the schema information, use that to avoid extra API calls
            return super().relation_exists(relation)

        relation_str = relation.render()
        fqn = self._to_fqn(relation_str)
        if any("`" in p.name for p in fqn.parts):
            # for debugging the issue that causes self.client.get_table() to fail due to quotes - this can be removed once we identify the root cause
            # dbt should not be returning double quoted relations but errors related to this have been observed in the wild
            events.fire_debug_event(
                "relation_exists() was called with a potentially double-quoted relation.\nRelation was: {} (type: {}),\nfqn was: {}\nrendered fqn: {}\nself type: {}\nself.adapter type: {}\ndialect: {}\ndialect type: {}\nexecution stack:\n{}",
                # use repr instead of str() incase we have an object that evaluates to something else when str() is called on it
                repr(relation_str),
                # typehints say we should have a str, show what we actually got
                repr(type(relation_str)),
                # show what the AST looked like
                repr(fqn),
                # show what the AST renders to
                fqn.sql(dialect=self.dialect),
                # what is 'self'?
                repr(type(self)),
                # what is 'self.adapter'?
                repr(type(self.adapter)),
                # what is `self.dialect`,
                repr(self.dialect),
                # what type is `self.dialect`?
                repr(type(self.dialect)),
                # show the execution trace that got us to this point
                "".join(traceback.format_stack()),
            )

        bq_table = self._get_table(fqn)
        return bq_table is not None

    def report(self) -> t.Dict[str, t.Any]:
        base_report = super().report()

        if self._table_cache.stats.contains_lock_timeouts:
            base_report["table_cache_stats"] = self._table_cache.stats.report()

        return base_report

    def _fetch_last_modified_epochs(
        self, table_batch: t.Collection[exp.Table]
    ) -> dict[str, t.Optional[int]]:
        epochs = {}
        for table in table_batch:
            fqn = self._to_fqn(table)
            bq_table = self._get_table(fqn)

            if bq_table and bq_table.table_type == "EXTERNAL":
                epochs[self._sql(fqn)] = None
                continue

            modified_ts = (
                int(bq_table.modified.timestamp() * 1000)
                if bq_table and bq_table.modified
                else None
            )

            epochs[self._sql(fqn)] = modified_ts

        return epochs

    def clear_cache(self, tables: t.Iterable[str | exp.Table]) -> None:
        super().clear_cache(tables)

        table_ids = [BigQueryAdapterExtension._to_table_id(self._to_fqn(table)) for table in tables]

        with self._table_cache as cache:
            cache.remove(table_ids)

    @override
    def _batch_table_names(
        self,
        tables: t.Collection[exp.Table],
    ) -> t.Collection[t.Collection[exp.Table]]:
        # The API call for get_table is synchronous and only applies to a single table, so we fetch concurrently
        # in batches of 1
        return [[t] for t in tables]

    def _fetch_view_definitions(self, table_batch: t.Collection[exp.Table]) -> ViewFetchResult:
        definitions = []

        for table in table_batch:
            if bq_table := self._get_table(table):
                if (query := bq_table.view_query) and isinstance(query, str):
                    fqn = self._sql(self._to_fqn(table))
                    catalog, schema, _ = extract_fqn_parts(fqn, dialect=self.dialect)
                    definitions.append(
                        ViewDefinition(
                            fqn=fqn,
                            definition=query,
                            dialect=self.dialect,
                            default_catalog=catalog,
                            default_schema=schema,
                        )
                    )

        return ViewFetchResult(definitions=definitions)

    def _get_table(self, table: exp.Table) -> Table | None:
        from google.api_core.exceptions import Forbidden, NotFound

        if self._is_system_metadata_table(table):
            return None

        table_id = BigQueryAdapterExtension._to_table_id(table)

        with self._table_cache as cache:
            fut = cache.resolve(table_id)

        if fut is not None:
            # another thread is already fetching this, wait for it to finish
            # and use its result instead of issuing a competing request
            wait([fut], timeout=self._timeout)
            return fut.result()

        table_rendered = table.sql(dialect=self.dialect)

        bq_table = None
        try:
            bq_table = self._client.get_table(table_id)
        except NotFound:
            pass
        except Forbidden:
            events.fire_warn_event_suboptimal("Access to table {} was denied", table_rendered)
        except Exception:
            events.fire_warn_event_suboptimal(
                "Error fetching metadata for table {}", table_rendered
            )
            events.fire_debug_event(
                "Unable to fetch metadata for {} (table id: {}), {}",
                table_rendered,
                table_id,
                # print full stack trace so we can identify the sequence of calls that lead to this
                traceback.format_exc(),
            )

        with self._table_cache as cache:
            cache.fulfill(table_id, bq_table)

        return bq_table

    def _is_system_metadata_table(self, table: exp.Table) -> bool:
        return any(table.name.lower().startswith(f"{s}.") for s in self.SYSTEM_METADATA_SCHEMAS)

    @staticmethod
    def _to_table_id(table: exp.Table) -> str:
        return ".".join(p.name for p in table.parts)
