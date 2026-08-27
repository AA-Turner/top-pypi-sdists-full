"""
pysqlsync: Synchronize schema and large volumes of data.

Copyright 2023-2026, Levente Hunyadi; 2026 Instructure, Inc.

:see: https://github.com/instructure-internal/pysqlsync
"""

from pysqlsync.model.data_types import SqlJsonType


class PostgreSQLJsonType(SqlJsonType):
    def __str__(self) -> str:
        return "jsonb"
