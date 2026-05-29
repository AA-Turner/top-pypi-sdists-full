from typing import Callable, Dict, Any, Optional, List
import re
import asyncio
import gc
import asyncpg
import json
import ast
from decimal import Decimal
import numpy as np
import pandas as pd
from pgvector.asyncpg import register_vector
from pgvector.utils import Vector
from navigator.libs.json import JSONContent
from ..interfaces.flow import FlowComponent
from ..exceptions import ConfigError, ComponentError
from ..conf import default_dsn

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


class DuplicatePhoto(FlowComponent):
    """
    DuplicatePhoto.

    Check if Photo is Duplicated and add a column with the result.
    This component is used to check if a photo is duplicated in the dataset.
    It uses the image hash to check if the photo is duplicated.
    The image hash is a unique identifier for the image.
    The image hash is calculated using the image hash algorithm.
    The image hash algorithm is a fast and efficient way to calculate the hash of an image.
    saves a detailed information about matches based on perceptual hash and vector similarity.

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          DuplicatePhoto:
          # attributes here
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
        self.chunk_size: int = kwargs.get('chunk_size', 100)
        self.id_column: str = kwargs.get("id_column", "photo_id")
        self.hash_column: str = kwargs.get("hash_column", "image_hash")
        self.vector_column: str = kwargs.get("vector_column", "image_vector")
        # 4-6 (exact duplicates)
        self.hamming_threshold: int = kwargs.get("hamming_threshold", 4)
        # exact match: 0.05-0.10 (95-99% similarity for duplicates)
        self.vector_threshold: float = kwargs.get("vector_threshold", 0.05)
        # Similarity detection
        # More lenient threshold  8-12 (similar images)
        self.similar_hamming_threshold: int = kwargs.get("similar_hamming_threshold", 8)
        # ~95% similarity 0.15-0.25 (75-85% similarity for similar images)
        self.similar_vector_threshold: float = kwargs.get("similar_vector_threshold", 0.15)
        self.tablename: str = kwargs.get("tablename", "image_bank")
        self.schema: str = kwargs.get("schema", "public")
        self.duplicate_column: str = kwargs.get("duplicate_column", "duplicated")
        self.similar_column: str = kwargs.get("similar_column", "similar")
        # boolean flags for easy filtering:
        self._is_duplicated: str = kwargs.get("is_duplicated", "is_duplicated")
        self._is_similar: str = kwargs.get("is_similar", "is_similar")
        self.pool: asyncpg.Pool | None = None
        super(DuplicatePhoto, self).__init__(loop=loop, job=job, stat=stat, **kwargs)
        self._semaphore = asyncio.Semaphore(10)  # Adjust the limit as needed

    def _coerce_vector(self, vec) -> Optional[List[float]]:
        """
        Convert many possible representations into List[float] for pgvector.
        Returns None if it cannot be parsed.
        """
        if vec is None:
            return None

        # numpy arrays
        if isinstance(vec, np.ndarray):
            try:
                return [float(x) for x in vec.ravel().tolist()]
            except Exception:
                return None

        # sequences (list/tuple/set) including Decimals
        if isinstance(vec, (list, tuple, set)):
            try:
                return [float(x) if not isinstance(x, Decimal) else float(x) for x in vec]
            except Exception:
                return None

        # bytes → str
        if isinstance(vec, (bytes, bytearray)):
            vec = vec.decode("utf-8", "ignore")

        # strings: try JSON → literal_eval → split
        if isinstance(vec, str):
            s = vec.strip()
            # JSON-like "[...]" first
            if s.startswith("[") and s.endswith("]"):
                try:
                    arr = json.loads(s)
                    if isinstance(arr, list):
                        return [float(x) for x in arr]
                except Exception:
                    pass
            # Python repr or "{...}" / "(...)"
            try:
                arr = ast.literal_eval(s)
                if isinstance(arr, (list, tuple)):
                    return [float(x) for x in arr]
            except Exception:
                pass
            # Fallback: split by comma/space
            try:
                toks = re.split(r"[,\s]+", s.strip("[]{}()"))
                return [float(x) for x in toks if x]
            except Exception:
                return None
        # unknown type that is iterable of numbers
        try:
            return [float(x) for x in vec]  # type: ignore
        except Exception:
            return None

    def _qualified_tablename(self) -> str:
        """
        Get the qualified table name.
        """
        if not self.schema:
            raise ConfigError("Schema is not set.")
        if not self.tablename:
            raise ConfigError("Table name is not set.")
        return f"{qid(self.schema)}.{qid(self.tablename)}"

    def _build_phash_sql(self) -> str:
        return (
            f"SELECT {qid(self.id_column)}, "
            f"bit_count(('x' || $1)::bit(256) # ('x' || {qid(self.hash_column)})::bit(256)) as distance "
            f"FROM {self._qualified_tablename()} "
            f"WHERE {qid(self.id_column)} IS DISTINCT FROM $3::bigint "
            f"AND bit_count(('x' || $1)::bit(256) # ('x' || {qid(self.hash_column)})::bit(256)) <= $2::integer "
            f"ORDER BY distance ASC "
            f"LIMIT 1;"
        )

    def _build_vector_sql(self) -> str:
        return (
            f"SELECT {qid(self.id_column)}, "
            f"{qid(self.vector_column)} <-> $1::vector as distance, "
            f"1 - ({qid(self.vector_column)} <=> $1::vector) as similarity "
            f"FROM {self._qualified_tablename()} "
            f"WHERE {qid(self.id_column)} IS DISTINCT FROM $3::bigint "
            f"AND {qid(self.vector_column)} <-> $1::vector < $2::float8 "
            f"ORDER BY distance ASC "
            f"LIMIT 1;"
        )

    def _build_similar_phash_sql(self) -> str:
        return (
            f"SELECT {qid(self.id_column)}, "
            f"bit_count(('x' || $1)::bit(256) # ('x' || {qid(self.hash_column)})::bit(256)) as distance "
            f"FROM {self._qualified_tablename()} "
            f"WHERE {qid(self.id_column)} IS DISTINCT FROM $3::bigint "
            f"AND bit_count(('x' || $1)::bit(256) # ('x' || {qid(self.hash_column)})::bit(256)) > $2::integer "
            f"AND bit_count(('x' || $1)::bit(256) # ('x' || {qid(self.hash_column)})::bit(256)) <= $4::integer "
            f"ORDER BY distance ASC "
            f"LIMIT 1;"
        )

    def _build_similar_vector_sql(self) -> str:
        return (
            f"SELECT {qid(self.id_column)}, "
            f"{qid(self.vector_column)} <-> $1::vector as distance, "
            f"1 - ({qid(self.vector_column)} <=> $1::vector) as similarity "
            f"FROM {self._qualified_tablename()} "
            f"WHERE {qid(self.id_column)} IS DISTINCT FROM $3::bigint "
            f"AND {qid(self.vector_column)} <-> $1::vector >= $2::float8 "
            f"AND {qid(self.vector_column)} <-> $1::vector < $4::float8 "
            f"ORDER BY distance ASC "
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
        for col in (self.id_column, self.hash_column, self.vector_column,):
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
        if self.duplicate_column not in self.data.columns:
            self.data[self.duplicate_column] = {
                "phash": None,
                "vector": None,
                "duplicate": False
            }
        if self.similar_column not in self.data.columns:
            self.data[self.similar_column] = {
                "phash": None,
                "vector": None,
                "similar": False,
                "similarity_percentage": None
            }
        # boolean flag columns
        for bcol in (self._is_duplicated, self._is_similar):
            if bcol not in self.data.columns:
                self.data[bcol] = False
            self.data[bcol] = self.data[bcol].astype("boolean")

        # optional: similarity percentage as nullable float
        if "similarity_percentage" not in self.data.columns:
            self.data["similarity_percentage"] = pd.Series(
                [pd.NA] * len(self.data), dtype="Float64"
            )

        # prepare SQL strings
        self._sql_phash = self._build_phash_sql()
        self._sql_vector = self._build_vector_sql()
        self._sql_similar_phash = self._build_similar_phash_sql()
        self._sql_similar_vector = self._build_similar_vector_sql()

    async def close(self):
        if self.pool:
            await self.pool.close()

    # --------------- duplicate test --------------------
    async def _check_duplicates(
        self,
        conn,
        phash: str,
        vec: list[float],
        current_id: int
    ) -> tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Check if the given hash and vector are duplicated in the database.
        Return detailed information about matches.

        :param conn: Database connection.
        :param phash: Perceptual hash of the image.
        :param vec: Vector representation of the image.
        :param current_id: Current photo ID.
        :return: Tuple of dictionaries with duplicate and similarity information
        """
        duplicate_result = {
            "phash": None,
            "vector": None,
            "duplicate": False
        }
        similar_result = {
            "phash": None,
            "vector": None,
            "is_similar": False,
            "similarity_percentage": None
        }

        # Check perceptual hash match for both duplicates and similar images
        if phash:
            phash_match = await conn.fetchrow(
                self._sql_phash,
                phash,
                self.hamming_threshold,  # Strict threshold for duplicates
                current_id
            )

            if phash_match:
                distance = int(phash_match["distance"])
                duplicate_result["phash"] = {
                    "duplicate": True,
                    self.id_column: phash_match[self.id_column],
                    "threshold": distance
                }

        # Check vector match for both duplicates and similar images
        _vec = self._coerce_vector(vec)
        if _vec:
            vector_match = await conn.fetchrow(
                self._sql_vector,
                Vector(_vec),
                self.vector_threshold,
                current_id
            )
        else:
            vector_match = None

        if vector_match:
            distance = float(vector_match["distance"])
            similarity = float(vector_match.get("similarity", 1 - distance))
            similarity_pct = similarity * 100

            duplicate_result["vector"] = {
                "duplicate": True,
                "photo_id": vector_match[self.id_column],
                "threshold": distance,
                "similarity": similarity,
                "similarity_percentage": similarity_pct
            }

        # Determine overall duplicate status
        phash_duplicate = duplicate_result["phash"] is not None and duplicate_result["phash"].get("duplicate", False)
        vector_duplicate = duplicate_result["vector"] is not None and duplicate_result["vector"].get("duplicate", False)

        if phash_duplicate or vector_duplicate:
            duplicate_result["duplicate"] = True
            # If it's a duplicate, don't check for similarity
            return duplicate_result, similar_result

        similar_phash_match = await conn.fetchrow(
            self._sql_similar_phash,
            phash,
            self.hamming_threshold,      # Duplicate threshold (lower bound)
            current_id,
            self.similar_hamming_threshold  # Similar threshold (upper bound)
        )
        if similar_phash_match:
            distance = int(similar_phash_match["distance"])
            # Calculate perceptual hash similarity percentage
            hash_similarity_pct = 100 - (distance / 256 * 100)
            similar_result["phash"] = {
                "similar": True,
                self.id_column: similar_phash_match[self.id_column],
                "threshold": distance,
                "similarity_percentage": hash_similarity_pct
            }

        _vec = self._coerce_vector(vec)
        if _vec:
            similar_vector_match = await conn.fetchrow(
                self._sql_similar_vector,
                Vector(_vec),
                self.vector_threshold,      # Duplicate threshold (lower bound)
                current_id,
                self.similar_vector_threshold  # Similar threshold (upper bound)
            )
        else:
            similar_vector_match = None

        if similar_vector_match:
            distance = float(similar_vector_match["distance"])
            similarity = float(similar_vector_match.get("similarity", 1 - distance))
            similarity_pct = similarity * 100

            similar_result["vector"] = {
                "similar": True,
                "photo_id": similar_vector_match[self.id_column],
                "threshold": distance,
                "similarity": similarity,
                "similarity_percentage": similarity_pct
            }

        # Determine overall similarity status
        phash_similar = similar_result["phash"] is not None and similar_result["phash"].get("similar", False)
        vector_similar = similar_result["vector"] is not None and similar_result["vector"].get("similar", False)

        if phash_similar or vector_similar:
            similar_result["is_similar"] = True

            # Get the best similarity percentage
            if vector_similar and similar_result["vector"].get("similarity_percentage") is not None:
                similar_result["similarity_percentage"] = similar_result["vector"]["similarity_percentage"]
            elif phash_similar and similar_result["phash"].get("similarity_percentage") is not None:
                similar_result["similarity_percentage"] = similar_result["phash"]["similarity_percentage"]

        return duplicate_result or {}, similar_result or {}

    async def _process_row(self, conn, row) -> Dict[str, Any]:
        """
        Process a row and check for duplicates with detailed information.

        :param conn: Database connection.
        :param row: Row data to process.
        :return: Dictionary with detailed match information.
        """
        phash = row[self.hash_column]
        vec = row[self.vector_column]
        current_id = row[self.id_column]

        # Log current processing information for debugging
        self._logger.debug(
            f"Processing photo_id: {current_id} with threshold: {self.vector_threshold}"
        )

        duplicate_info, similar_info = await self._check_duplicates(conn, phash, vec, current_id)

        # Debug information about match results
        if duplicate_info["vector"]:
            self._logger.debug(f"Vector match found: {duplicate_info['vector']}")
        if duplicate_info["phash"]:
            self._logger.debug(f"Perceptual hash match found: {duplicate_info['phash']}")

        # Update the row with duplicate and similarity information
        row[self.duplicate_column] = duplicate_info
        row[self.similar_column] = similar_info
        if duplicate_info.get('duplicate', False) is True:
            row[self._is_duplicated] = True
        if similar_info.get('is_similar', False) is True and not duplicate_info.get('duplicate', False):
            row[self._is_similar] = True
            # If we have similarity percentage, add it directly to the row
        if similar_info.get('similarity_percentage') is not None:
            row['similarity_percentage'] = similar_info['similarity_percentage']
        return row

    async def run(self):
        """
        Run the duplicate detection with enhanced information, processing rows in
        chunks of ``chunk_size`` to keep RAM usage bounded.
        """
        if self.pool is None:
            raise ConfigError("Database connection pool is not initialized.")

        # Process rows and check for duplicates
        async def handle(idx):
            async with self._semaphore, self.pool.acquire() as conn:
                row = self.data.loc[idx].to_dict()
                updated_row = await self._process_row(conn, row)
                return idx, updated_row[self.duplicate_column], updated_row[self.similar_column]

        indices = list(self.data.index)
        total = len(indices)

        for chunk_start in range(0, total, self.chunk_size):
            chunk_indices = indices[chunk_start:chunk_start + self.chunk_size]
            chunk_end = min(chunk_start + self.chunk_size, total)
            self._logger.info(
                f"DuplicatePhoto: checking rows {chunk_start + 1}-{chunk_end} / {total}"
            )

            results = await asyncio.gather(*(handle(i) for i in chunk_indices))

            for idx, dup_result, sim_result in results:
                self.data.at[idx, self.duplicate_column] = dup_result
                self.data.at[idx, self.similar_column] = sim_result

                self.data.at[idx, self._is_duplicated] = dup_result.get('duplicate', False)

                is_similar = sim_result.get('is_similar', False) and not dup_result.get('duplicate', False)
                self.data.at[idx, self._is_similar] = is_similar

                if is_similar and sim_result.get('similarity_percentage') is not None:
                    self.data.at[idx, 'similarity_percentage'] = sim_result['similarity_percentage']

            gc.collect()

        self._result = self.data
        self._print_data_(self.data, title="DuplicatePhoto Result")
        return self._result
