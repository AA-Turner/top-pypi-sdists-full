# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""DuckDB-based message cache for storing Airbyte messages.

This module provides a DuckDB-based message cache that persists Airbyte messages
to JSONL files and loads them into DuckDB for efficient querying.

Based on airbyte-ci implementation:
https://github.com/airbytehq/airbyte/blob/master/airbyte-ci/connectors/live-tests/src/live_tests/commons/backends/duckdb_backend.py
"""

from __future__ import annotations

import json
import logging
import re
from collections.abc import Iterable
from pathlib import Path
from typing import TextIO

import duckdb
from airbyte_protocol.models import AirbyteMessage
from airbyte_protocol.models import Type as AirbyteMessageType
from cachetools import LRUCache, cached
from uuid_extensions import uuid7str

logger = logging.getLogger(__name__)


def sanitize_stream_name(stream_name: str) -> str:
    """Sanitize a stream name for use as a file name.

    Replaces characters that are not alphanumeric or underscores with underscores.
    """
    return re.sub(r"[^a-zA-Z0-9_]", "_", stream_name)


def sanitize_table_name(table_name: str) -> str:
    """Sanitize a table name for use in DuckDB.

    Replaces spaces with underscores and removes non-alphanumeric characters.
    Prepends underscore if name starts with a digit.
    """
    sanitized = str(table_name).replace(" ", "_")
    sanitized = re.sub(r"[^\w\s]", "", sanitized)
    if sanitized and sanitized[0].isdigit():
        sanitized = "_" + sanitized
    return sanitized


def _add_message_id(json_str: str) -> str:
    """Add a UUIDv7 _message_id to a JSON string.

    The _message_id is a time-ordered identifier that provides:
    - Portable ordering in JSONL files (sortable as strings)
    - Traceability for debugging
    - Consistency with PyAirbyte's ab_raw_id pattern

    The _message_id is cache metadata and should be excluded from
    regression comparisons (like emitted_at).
    """
    payload = json.loads(json_str)
    payload["_message_id"] = uuid7str()
    return json.dumps(payload, sort_keys=True)


class _FileDescriptorLRUCache(LRUCache):
    """LRU cache that closes file descriptors when evicted."""

    def popitem(self) -> tuple:
        filepath, fd = LRUCache.popitem(self)
        fd.close()
        return filepath, fd


class DuckDbMessageCache:
    """DuckDB-based message cache for Airbyte messages.

    This cache writes messages to JSONL files (for debugging and portability)
    and loads them into DuckDB for efficient querying. Messages are stored with
    an explicit `message_index` column to preserve ordering.

    Based on airbyte-ci implementation:
    https://github.com/airbytehq/airbyte/blob/master/airbyte-ci/connectors/live-tests/src/live_tests/commons/backends/duckdb_backend.py
    """

    RELATIVE_CATALOGS_PATH = "catalog.jsonl"
    RELATIVE_CONNECTION_STATUS_PATH = "connection_status.jsonl"
    RELATIVE_RECORDS_PATH = "records.jsonl"
    RELATIVE_SPECS_PATH = "spec.jsonl"
    RELATIVE_STATES_PATH = "states.jsonl"
    RELATIVE_TRACES_PATH = "traces.jsonl"
    RELATIVE_LOGS_PATH = "logs.jsonl"
    RELATIVE_CONTROLS_PATH = "controls.jsonl"

    SAMPLE_SIZE = -1  # Read all rows for schema inference

    def __init__(
        self,
        output_directory: Path,
        duckdb_path: Path | None = None,
        schema: Iterable[str] | None = None,
    ):
        """Initialize the message cache.

        Args:
            output_directory: Directory where JSONL files will be written.
            duckdb_path: Path to the DuckDB database file. If None, uses
                output_directory / "messages.duckdb".
            schema: Optional schema name parts (e.g., ["connector", "version"]).
        """
        self._output_directory = output_directory
        self._output_directory.mkdir(parents=True, exist_ok=True)

        self.duckdb_path = duckdb_path or (output_directory / "messages.duckdb")
        self.schema = list(schema) if schema else None

        self.record_per_stream_directory = self._output_directory / "records_per_stream"
        self.record_per_stream_directory.mkdir(exist_ok=True, parents=True)
        self.record_per_stream_paths: dict[str, Path] = {}
        self.record_per_stream_paths_data_only: dict[str, Path] = {}

        self._file_cache: _FileDescriptorLRUCache = _FileDescriptorLRUCache(maxsize=250)
        self._db_connection: duckdb.DuckDBPyConnection | None = None

    @property
    def jsonl_specs_path(self) -> Path:
        return (self._output_directory / self.RELATIVE_SPECS_PATH).resolve()

    @property
    def jsonl_catalogs_path(self) -> Path:
        return (self._output_directory / self.RELATIVE_CATALOGS_PATH).resolve()

    @property
    def jsonl_connection_status_path(self) -> Path:
        return (self._output_directory / self.RELATIVE_CONNECTION_STATUS_PATH).resolve()

    @property
    def jsonl_records_path(self) -> Path:
        return (self._output_directory / self.RELATIVE_RECORDS_PATH).resolve()

    @property
    def jsonl_states_path(self) -> Path:
        return (self._output_directory / self.RELATIVE_STATES_PATH).resolve()

    @property
    def jsonl_traces_path(self) -> Path:
        return (self._output_directory / self.RELATIVE_TRACES_PATH).resolve()

    @property
    def jsonl_logs_path(self) -> Path:
        return (self._output_directory / self.RELATIVE_LOGS_PATH).resolve()

    @property
    def jsonl_controls_path(self) -> Path:
        return (self._output_directory / self.RELATIVE_CONTROLS_PATH).resolve()

    @property
    def jsonl_files(self) -> list[Path]:
        return [
            self.jsonl_catalogs_path,
            self.jsonl_connection_status_path,
            self.jsonl_records_path,
            self.jsonl_specs_path,
            self.jsonl_states_path,
            self.jsonl_traces_path,
            self.jsonl_logs_path,
            self.jsonl_controls_path,
        ]

    @property
    def jsonl_files_to_insert(self) -> list[Path]:
        """JSONL files that should be inserted into DuckDB."""
        return self.jsonl_files

    def write(
        self,
        airbyte_messages: Iterable[AirbyteMessage],
    ) -> None:
        """Write Airbyte messages to JSONL files and load into DuckDB.

        Messages are written to JSONL files first (preserving order), then
        loaded into DuckDB with an explicit message_index column.
        """
        self._write_to_jsonl(airbyte_messages)
        self._load_into_duckdb()

    def _write_to_jsonl(
        self,
        airbyte_messages: Iterable[AirbyteMessage],
    ) -> None:
        """Write messages to JSONL files.

        Uses an LRU cache to manage open file objects, limiting the number of
        concurrently open file descriptors.
        """

        @cached(cache=self._file_cache)
        def _open_file(path: Path) -> TextIO:
            return open(path, "a")

        try:
            logger.info("Writing airbyte messages to disk")
            for message in airbyte_messages:
                if not isinstance(message, AirbyteMessage):
                    continue
                filepaths, messages = self._get_filepaths_and_messages(message)
                for filepath, msg_json in zip(filepaths, messages, strict=False):
                    _open_file(self._output_directory / filepath).write(f"{msg_json}\n")
            logger.info("Finished writing airbyte messages to disk")
        finally:
            for f in self._file_cache.values():
                f.close()
            self._file_cache.clear()

    def _get_filepaths_and_messages(
        self,
        message: AirbyteMessage,
    ) -> tuple[tuple[str, ...], tuple[str, ...]]:
        """Get file paths and JSON strings for a message.

        Each message is serialized with a UUIDv7 _message_id for:
        - Portable ordering in JSONL files (sortable as strings)
        - Traceability for debugging
        - Consistency with PyAirbyte's ab_raw_id pattern

        Note: data-only files don't get _message_id since they only contain
        the record.data payload, not the full message envelope.
        """
        if message.type == AirbyteMessageType.CATALOG:
            return (self.RELATIVE_CATALOGS_PATH,), (
                _add_message_id(message.catalog.model_dump_json()),
            )

        if message.type == AirbyteMessageType.CONNECTION_STATUS:
            return (self.RELATIVE_CONNECTION_STATUS_PATH,), (
                _add_message_id(message.connectionStatus.model_dump_json()),
            )

        if message.type == AirbyteMessageType.RECORD:
            stream_name = message.record.stream
            stream_file_path = (
                self.record_per_stream_directory
                / f"{sanitize_stream_name(stream_name)}.jsonl"
            )
            stream_file_path_data_only = (
                self.record_per_stream_directory
                / f"{sanitize_stream_name(stream_name)}_data_only.jsonl"
            )
            self.record_per_stream_paths[stream_name] = stream_file_path
            self.record_per_stream_paths_data_only[stream_name] = (
                stream_file_path_data_only
            )
            # Full message gets _message_id, data-only does not
            message_with_id = _add_message_id(message.model_dump_json())
            return (
                self.RELATIVE_RECORDS_PATH,
                str(stream_file_path),
                str(stream_file_path_data_only),
            ), (
                message_with_id,
                message_with_id,
                json.dumps(message.record.data, sort_keys=True),
            )

        if message.type == AirbyteMessageType.SPEC:
            return (self.RELATIVE_SPECS_PATH,), (
                _add_message_id(message.spec.model_dump_json()),
            )

        if message.type == AirbyteMessageType.STATE:
            return (self.RELATIVE_STATES_PATH,), (
                _add_message_id(message.state.model_dump_json()),
            )

        if message.type == AirbyteMessageType.TRACE:
            return (self.RELATIVE_TRACES_PATH,), (
                _add_message_id(message.trace.model_dump_json()),
            )

        if message.type == AirbyteMessageType.LOG:
            return (self.RELATIVE_LOGS_PATH,), (
                _add_message_id(message.log.model_dump_json()),
            )

        if message.type == AirbyteMessageType.CONTROL:
            return (self.RELATIVE_CONTROLS_PATH,), (
                _add_message_id(message.control.model_dump_json()),
            )

        raise NotImplementedError(
            f"No handling for AirbyteMessage type {message.type} has been implemented."
        )

    def _load_into_duckdb(self) -> None:
        """Load JSONL files into DuckDB with explicit message ordering."""
        conn = duckdb.connect(str(self.duckdb_path))

        try:
            schema_name = None
            if self.schema:
                schema_name = "_".join([sanitize_table_name(s) for s in self.schema])
                conn.sql(f"CREATE SCHEMA IF NOT EXISTS {schema_name}")
                conn.sql(f"USE {schema_name}")
                logger.info(f"Using schema {schema_name}")

            # Load main JSONL files with message_index for ordering
            for json_file in self.jsonl_files_to_insert:
                if json_file.exists():
                    table_name = sanitize_table_name(json_file.stem)
                    logger.info(f"Creating table {table_name} from {json_file}")
                    # Add message_index column for explicit ordering
                    conn.sql(f"""
                        CREATE TABLE {table_name} AS
                        SELECT
                            row_number() OVER () AS message_index,
                            *
                        FROM read_json_auto(
                            '{json_file}',
                            sample_size = {self.SAMPLE_SIZE},
                            format = 'newline_delimited'
                        )
                    """)
                    logger.info(f"Table {table_name} created")

            # Load per-stream record files
            for json_file in self.record_per_stream_paths_data_only.values():
                if json_file.exists():
                    table_name = sanitize_table_name(f"records_{json_file.stem}")
                    logger.info(f"Creating table {table_name} from {json_file}")
                    conn.sql(f"""
                        CREATE TABLE {table_name} AS
                        SELECT
                            row_number() OVER () AS message_index,
                            *
                        FROM read_json_auto(
                            '{json_file}',
                            sample_size = {self.SAMPLE_SIZE},
                            format = 'newline_delimited'
                        )
                    """)
                    logger.info(f"Table {table_name} created")
        finally:
            conn.close()

    def get_connection(self) -> duckdb.DuckDBPyConnection:
        """Get a connection to the DuckDB database.

        Returns a cached connection to avoid connection lifecycle issues
        when returning DuckDB relations from query methods.
        """
        if self._db_connection is None:
            self._db_connection = duckdb.connect(str(self.duckdb_path))
        return self._db_connection

    def query(
        self,
        sql: str,
    ) -> duckdb.DuckDBPyRelation:
        """Execute a SQL query against the message cache.

        Args:
            sql: SQL query to execute.

        Returns:
            DuckDB relation with query results.
        """
        conn = self.get_connection()
        if self.schema:
            schema_name = "_".join([sanitize_table_name(s) for s in self.schema])
            conn.sql(f"USE {schema_name}")
        return conn.sql(sql)

    def get_records_ordered(
        self,
        stream_name: str | None = None,
    ) -> duckdb.DuckDBPyRelation:
        """Get records in their original order.

        Args:
            stream_name: Optional stream name to filter by.

        Returns:
            DuckDB relation with records ordered by message_index.
        """
        if stream_name:
            table_name = sanitize_table_name(
                f"records_{sanitize_stream_name(stream_name)}_data_only"
            )
            return self.query(f"SELECT * FROM {table_name} ORDER BY message_index")
        return self.query("SELECT * FROM records ORDER BY message_index")

    def get_states_ordered(self) -> duckdb.DuckDBPyRelation:
        """Get state messages in their original order."""
        return self.query("SELECT * FROM states ORDER BY message_index")

    def get_record_count(
        self,
        stream_name: str | None = None,
    ) -> int:
        """Get the count of records.

        Args:
            stream_name: Optional stream name to filter by.

        Returns:
            Number of records.
        """
        if stream_name:
            table_name = sanitize_table_name(
                f"records_{sanitize_stream_name(stream_name)}_data_only"
            )
            result = self.query(f"SELECT COUNT(*) FROM {table_name}")
        else:
            result = self.query("SELECT COUNT(*) FROM records")
        return result.fetchone()[0]
