import asyncio
from collections.abc import Callable
from pathlib import PurePath
import aiofiles
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, text
from sqlalchemy.pool import NullPool
from querysource.conf import sqlalchemy_url
from ..conf import TASK_PATH
from ..exceptions import FileNotFound, FileError
from ..parsers.maps import open_map, open_model
from .flow import FlowComponent
from ..interfaces import TemplateSupport


class TableBase(TemplateSupport, FlowComponent):
    """
    TableBase.

    Abstract class for Using Pandas SQL features to manipulate data from databases.

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          TableBase:
          # attributes here
        ```
    """
    _version = "1.0.0"

    flavor: str = "postgres"

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        self._engine: Callable = None
        self.params: dict = {}
        self.use_template: bool = bool(kwargs.get('use_template', False))
        super(TableBase, self).__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def get_connection(self, dsn: str = None):
        if not dsn:
            dsn = sqlalchemy_url
        self._engine = create_engine(dsn, echo=False, poolclass=NullPool)
        self._session = Session(self._engine)

    async def close(self):
        """Closing Operations."""
        if self._engine:
            try:
                self._engine.dispose()
            except Exception as err:  # pylint: disable=W0703
                print(err)

    async def open_sqlfile(self, file: PurePath, **kwargs) -> str:
        if file.exists() and file.is_file():
            content = None
            # open SQL File:
            async with aiofiles.open(file, "r+") as afp:
                content = await afp.read()
                # check if we need to replace masks
            content = self.mask_replacement(content)
            if self.use_template is True:
                content = self._templateparser.from_string(content, kwargs)
            return content
        else:
            raise FileError(f"Table: Missing SQL File: {file}")

    def column_info(self, tablename):
        if self.flavor == "postgres":
            discover = f"""SELECT attname AS column_name, atttypid::regtype AS data_type, attnotnull::boolean as notnull
                    FROM pg_attribute WHERE attrelid = '{tablename}'::regclass AND attnum > 0
                    AND NOT attisdropped ORDER  BY attnum;
                    """
        else:
            raise ValueError(
                f"Column Info: DB Flavor not supported yet: {self.flavor}"
            )
        discover = text(discover)
        result = self._session.execute(discover)
        if result:
            # rows = result.fetchall()
            rows = result.mappings()
            # return {item['column_name']: item['data_type'] for item in rows}
            return {row["column_name"]: row["data_type"] for row in rows}
        else:
            model = open_model(self.tablename, self.program)
            if model:
                fields = model["fields"]
                return {field: fields[field]["data_type"] for field in fields}
            else:
                print(f"Table: table or Model {tablename} does not exists")
                return None

    async def start(self, **kwargs):
        if self.previous:
            self.data = self.input
        await self.get_connection()
        if hasattr(self, "tablename"):
            # Using a Table:
            if not hasattr(self, "schema"):
                self.schema = self._program
            # check for Table structure
            try:
                tablename = self.tablename
                schema = self.schema
                if self.flavor == "postgres":
                    tablename = f"{schema}.{tablename}"
                colinfo = self.column_info(tablename)
            except KeyError:
                if hasattr(self, "map"):
                    mapping = self.map["map"]
                    colinfo = open_map(mapping, self.program)
                if not colinfo:
                    colinfo = open_map(tablename, self.program)
            if colinfo:
                try:
                    ignore = self.map["ignore"]
                    colinfo = {k: v for k, v in colinfo.items() if k not in ignore}
                except (KeyError, AttributeError):
                    pass
                self.params["columns"] = colinfo.keys()
                parse_dates = []
                for column, dtype in colinfo.items():
                    if (
                        dtype == "timestamp without time zone"
                        or dtype == "timestamp with time zone"
                        or dtype == "date"
                    ):
                        parse_dates.append(column)
                if parse_dates:
                    self.params["parse_dates"] = parse_dates
        elif hasattr(self, "file_sql"):
            file_path = TASK_PATH.joinpath(self.program, "sql", self.file_sql)
            if not file_path.exists():
                raise FileNotFound(f"Table: SQL File {file_path} was not found.")
            self.query = await self.open_sqlfile(file_path)
        elif hasattr(self, "query"):
            ## passing query for mask conversion:
            if hasattr(self, "masks"):
                self.query = self.mask_replacement(self.query)
            for val in self._variables:
                if isinstance(self._variables[val], list):
                    if isinstance(self._variables[val], int):
                        self._variables[val] = ", ".join(self._variables[val])
                    else:
                        self._variables[val] = ", ".join(
                            "'{}'".format(v) for v in self._variables[val]
                        )
                self.query = self.query.replace(
                    "{{{}}}".format(str(val)), str(self._variables[val])
                )
