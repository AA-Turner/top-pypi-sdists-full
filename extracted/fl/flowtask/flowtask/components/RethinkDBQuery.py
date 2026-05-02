
import asyncio
from typing import List, Dict, Union
from collections.abc import Callable
import rethinkdb as r
from ..exceptions import ComponentError, DataNotFound, ConfigError
from .flow import FlowComponent
from ..interfaces.dataframes import PandasDataframe
from ..interfaces import TemplateSupport
from ..interfaces.databases.rethink import RethinkDBSupport


class RethinkDBQuery(
    RethinkDBSupport,
    TemplateSupport,
    FlowComponent,
    PandasDataframe,
):
    """
    RethinkDBQuery.

    Class to execute queries against a RethinkDB database and retrieve results.
    using asyncDB as backend.

    RethinkDB Query can support queries by mapping RethinkDB methods as attributes.
    Methods as "table", "filter", "order_by", "limit", "pluck" are supported.



        Example:

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          RethinkDBQuery:
          table: stores_reviews
          schema: epson
          filter:
          - rating:
          gt: 4
          - rating:
          lt: 6
          order_by:
          - rating: desc
          limit: 50
          columns:
          - store_id
          - store_name
          - formatted_address
          - latitude
          - longitude
          - reviews
          - rating
          - user_ratings_total
          as_dataframe: true
        ```
    """
    _version = "1.0.0"
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ) -> None:
        """Init Method."""
        self.table = kwargs.get('table', None)
        self.schema = kwargs.get('schema', None)
        super().__init__(loop=loop, job=job, stat=stat, **kwargs)
        self._db = None

    async def close(self):
        """Close the connection to the RethinkDB database."""
        if self._db:
            try:
                await self._db.close()
            except Exception:
                pass
        self._db = None

    async def start(self, **kwargs):
        await super().start(**kwargs)
        if not hasattr(self, 'table'):
            raise ConfigError(
                "'table' attribute is required in the RethinkDBQuery."
            )
        if not hasattr(self, 'schema'):
            raise ConfigError(
                "'schema' attribute is required in the RethinkDBQuery."
            )
        # Replacing with Masking if needed.
        self.schema = self.mask_replacement(self.schema)
        self.table = self.mask_replacement(self.table)
        if hasattr(self, 'columns'):
            # used as "pluck"
            self.pluck = self.columns
        return True

    def _filter_criteria(self, engine, cursor):
        result = engine.expr(True)
        for args in self.filter:
            field, inner_args = next(iter(args.items()))
            func, value = next(iter(inner_args.items()))
            if func == 'in':
                cursor = cursor.filter(
                    (
                        lambda exp: engine.expr(value)
                        .coerce_to("array")
                        .contains(exp[field])
                    )
                )
            elif func == 'gt':
                result = result.and_(
                    engine.row[field].gt(value)
                )
            elif func == 'eq':
                result = result.and_(
                    engine.row[field].eq(value)
                )
            elif func == 'lt':
                result = result.and_(
                    engine.row[field].lt(value)
                )
            elif func == 'ge':
                result = result.and_(
                    engine.row[field].ge(value)
                )
            elif func == 'le':
                result = result.and_(
                    engine.row[field].le(value)
                )
        cursor = cursor.filter(result)
        return cursor

    def _order_by(self, engine, cursor):
        order_clauses = []
        for order in self.order_by:
            field, direction = next(iter(order.items()))
            if direction.lower() == 'asc':
                order_clauses.append(engine.asc(field))
            elif direction.lower() == 'desc':
                order_clauses.append(engine.desc(field))
            else:
                raise ComponentError(
                    f"Invalid order direction: {direction}"
                )
        if order_clauses:
            cursor = cursor.order_by(*order_clauses)
        return cursor

    async def run(self):
        """Execute the RethinkDB query and retrieve the results."""
        if not self._db:
            # TODO: add support for datasources.
            self._db = self.default_connection()
        try:
            async with await self._db.connection() as conn:
                # Change to default database:
                engine = conn.engine()
                # changing to active database
                cursor = engine.db(self.schema).table(self.table)
                if hasattr(self, 'filter'):
                    # Build a Filter functionality:
                    cursor = self._filter_criteria(engine, cursor)
                if hasattr(self, 'order_by'):
                    cursor = self._order_by(engine, cursor)
                    # cursor = cursor.order_by(self.order_by)
                    pass
                if hasattr(self, 'limit'):
                    cursor = cursor.limit(self.limit)
                if hasattr(self, 'pluck'):
                    cursor = cursor.pluck(self.pluck)
                data = []
                print('CURSOR > ', cursor)
                cursor = await cursor.run(conn.get_connection())
                if isinstance(cursor, list):
                    data = cursor
                else:
                    while await cursor.fetch_next():
                        item = await cursor.next()
                        data.append(item)
            # Check if return as Dataframe:
            if self.as_dataframe is True:
                self._result = await self.create_dataframe(data)
            else:
                self._result = data
            return self._result
        except Exception as e:
            raise ComponentError(
                f"Error executing RethinkDB query: {e}"
            ) from e
