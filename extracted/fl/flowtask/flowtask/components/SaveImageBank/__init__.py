from typing import Optional
from collections.abc import Callable
import re
import asyncio
import asyncpg
from PIL.TiffImagePlugin import IFDRational
from pgvector.asyncpg import register_vector
from querysource.types.validators import Entity
from navigator.libs.json import JSONContent
from ..flow import FlowComponent
from ...exceptions import ConfigError, ComponentError
from ...conf import default_dsn

IDENT_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")

def qid(name: str) -> str:
    """
    Very small helper to quote SQL identifiers safely.
    Raises if name contains anything but letters, digits or '_'.
    """
    if not IDENT_RE.match(name):
        raise ValueError(
            f"illegal identifier: {name!r}"
        )
    return '"' + name + '"'

class SaveImageBank(FlowComponent):
    """
    SaveImageBank.

    Save images into a postgreSQL Table, with UPSERT and optional evaluation for duplicates.

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          SaveImageBank:
          # attributes here
        ```
    """
    _version = "1.0.0"
    def __init__(
        self,
        loop: Optional[asyncio.AbstractEventLoop] = None,
        job: Callable | None = None,
        stat: Callable | None = None,
        **kwargs,
    ):
        self.id_column: str = kwargs.get("id_column", "photo_id")
        self.hash_column: str = kwargs.get("hash_column", "image_hash")
        self.vector_column: str = kwargs.get("vector_column", "image_vector")
        self.detections_column: str = kwargs.get("detections_column", "image_features")
        self.hamming_threshold: int = kwargs.get("hamming_threshold", 4)
        self.vector_threshold: float = kwargs.get("vector_threshold", 0.05)
        self.tablename: str = kwargs.get("tablename", "image_bank")
        self.schema: str = kwargs.get("schema", "public")
        self.pool: asyncpg.Pool | None = None
        self._semaphore = asyncio.Semaphore(16)  # limit GPU tasks
        self.drop_columns: list[str] = kwargs.get("drop_columns", [])
        super().__init__(loop=loop, job=job, stat=stat, **kwargs)
        # JSON encoder:
        self._encoder = JSONContent()

    def _qualified_tablename(self) -> str:
        """
        Get the qualified table name.
        """
        if not self.schema:
            raise ConfigError("Schema is not set.")
        if not self.tablename:
            raise ConfigError("Table name is not set.")
        return f"{qid(self.schema)}.{qid(self.tablename)}"

    def _build_insert_sql(self, columns: list[str]) -> str:
        """
        Produces something like:

        INSERT INTO schema.table (col1,col2,…) VALUES ($1,$2,…)
        ON CONFLICT (photo_id) DO UPDATE SET
            col1 = EXCLUDED.col1,
            ...
        """
        col_list = ", ".join(map(qid, columns))
        placeholders = ", ".join(f"${i}" for i in range(1, len(columns) + 1))
        updates = ", ".join(f"{qid(c)} = EXCLUDED.{qid(c)}" for c in columns
                            if c != self.id_column)

        return (
            f"INSERT INTO {self._qualified_tablename()} ({col_list}) "
            f"VALUES ({placeholders}) "
            f"ON CONFLICT ({qid(self.id_column)}) "
            f"DO UPDATE SET {updates};"
        )

    def _build_phash_sql(self) -> str:
        return (
            f"SELECT 1 FROM {self._qualified_tablename()} "
            f"WHERE {qid(self.id_column)} IS DISTINCT FROM $3 "
            f"AND   bit_count(('x' || $1)::bit(256) # "
            f"                 ('x' || {qid(self.hash_column)})::bit(256)) "
            f"      <= $2 "
            f"LIMIT 1;"
        )

    def _build_vector_sql(self) -> str:
        return (
            f"SELECT 1 FROM {self._qualified_tablename()} "
            f"WHERE {qid(self.id_column)} IS DISTINCT FROM $3 "
            f"AND   {qid(self.vector_column)} <#> $1::vector < $2 "
            f"LIMIT 1;"
        )

    async def pgvector_init(self, conn):
        """
        Initialize pgvector extension in PostgreSQL.
        """
        # Setup jsonb encoder/decoder
        def _encoder(value):
            # return json.dumps(value, cls=BaseEncoder)
            return self._encoder.dumps(value)  # pylint: disable=E1120

        def _decoder(value):
            return self._encoder.loads(value)  # pylint: disable=E1120

        await conn.set_type_codec(
            "json",
            encoder=_encoder,
            decoder=_decoder,
            schema="pg_catalog"
        )
        await conn.set_type_codec(
            "jsonb",
            encoder=_encoder,
            decoder=_decoder,
            schema="pg_catalog"
        )

        await register_vector(conn)

    # ──────────────────────────────────────────────────────────────
    # Setup / teardown
    # ──────────────────────────────────────────────────────────────
    async def start(self, **kwargs):
        if self.previous:
            self.data = self.input

        # column checks
        for col in (self.id_column, self.hash_column,
                    self.vector_column, self.detections_column):
            if col not in self.data.columns:
                raise ConfigError(
                    f"Column '{col}' missing from DataFrame"
                )
        self.pool = await asyncpg.create_pool(
            dsn=default_dsn,
            min_size=1,
            max_size=4,
            max_queries=100,
            init=self.pgvector_init,
            timeout=10,
        )
        # Check if the table exists
        if not self.pool:
            raise ConfigError(
                "Database connection pool is not initialized."
            )
        async with self.pool.acquire() as conn:
            try:
                await conn.execute(
                    f"SELECT 1 FROM {self.schema}.{self.tablename} LIMIT 1"
                )
            except asyncpg.exceptions.UndefinedTableError:
                raise ConfigError(
                    f"Table {self.schema}.{self.tablename} does not exist."
                )
            except asyncpg.exceptions.UndefinedSchemaError:
                raise ConfigError(
                    f"Schema {self.schema} does not exist."
                )
        if "duplicated" not in self.data.columns:
            self.data["duplicated"] = False
        # prepare SQL strings
        self._sql_phash = self._build_phash_sql()
        self._sql_vector = self._build_vector_sql()

    async def close(self):
        if self.pool:
            await self.pool.close()

    # --------------- duplicate test --------------------
    async def _is_duplicated(self, conn, phash: str, vec: list[float], current_id: int) -> bool:
        """
        Check if the given hash and vector are duplicated in the database.
        :param conn: Database connection.
        :param phash: Perceptual hash of the image.
        :param vec: Vector representation of the image.
        :return: True if the image is duplicated, False otherwise.
        """
        # phash first
        phash_dup = False
        vector_dup = False
        if phash:
            if await conn.fetchval(self._sql_phash, phash, self.hamming_threshold, current_id):
                phash_dup = True
        # vector second
        vector_dup = bool(
            await conn.fetchval(self._sql_vector, vec, self.vector_threshold, current_id)
        )
        # return True if both are duplicated
        return phash_dup and vector_dup

    async def _upsert_row(self, conn, row) -> bool:
        """
        UPSERT a single row into the database.
        :param conn: Database connection.
        :param row: Row data to be inserted/updated.
        :return: True if the row was duplicated, False otherwise.
        """
        # --------------- UPSERT one row --------------------
        phash = row[self.hash_column]
        vec = row[self.vector_column]
        dup = await self._is_duplicated(
            conn,
            phash,
            vec,
            current_id=row[self.id_column]
        )

        # Add/overwrite duplicated flag in the in‑memory DF row
        row["duplicated"] = dup

        # Build VALUES array in the same order as self.data.columns
        values = [row[col] for col in self.data.columns]
        # asyncpg needs list/tuple for pgvector, ensure np → list
        idx_vec = self.data.columns.get_loc(self.vector_column)
        values[idx_vec] = list(values[idx_vec])

        await conn.execute(self._sql_insert, *values)

    async def run(self):
        """
        Run the task.
        """
        if self.pool is None:
            raise ConfigError("Database connection pool is not initialized.")
        if self.drop_columns:
            # drop columns from dataframe:
            self.data.drop(
                columns=self.drop_columns,
                axis=1,
                inplace=True,
            )
        #
        self._sql_insert = self._build_insert_sql(list(self.data.columns))

        # check for duplicates
        async def handle(idx):
            async with self._semaphore, self.pool.acquire() as conn:
                row = self.data.loc[idx].to_dict()
                await self._upsert_row(conn, row)
                # write duplicated flag back into DF
                self.data.at[idx, "duplicated"] = row["duplicated"]
        await asyncio.gather(*(handle(i) for i in self.data.index))

        self._result = self.data
        return self._result
