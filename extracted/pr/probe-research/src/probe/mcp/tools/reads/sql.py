"""query_sql: read-only SQL passed straight to the backend, its row cap derived from the token budget."""

from __future__ import annotations

from ...generated.sql import MAX_ROWS_CEILING


class SqlMixin:
    """Part of ResearchReadService: its methods run with `self` the ResearchReadService; compose() folds them into ResearchReadService."""

    def query_sql(
        self,
        sql: str | None = None,
        tables: list[str] | None = None,
        token_budget: int = 2000,
        source: str | None = None,
    ) -> dict:
        """Read-only SQL, passed straight through: the server already bounds it.

        ``max_rows`` is DERIVED from the delivery budget rather than exposed, so
        the database is not asked for 200 rows the response can only carry 20 of.
        ~20 tokens per row is a deliberate over-estimate of a narrow row; the
        delivery branch in ``continuation`` still trims whatever does not fit.
        """
        max_rows = None if sql is None else max(1, min(MAX_ROWS_CEILING, token_budget // 20))
        return self.source.query_sql(sql=sql, tables=tables, max_rows=max_rows, source=source)
