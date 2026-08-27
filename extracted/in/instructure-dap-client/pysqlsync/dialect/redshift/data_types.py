"""
pysqlsync: Synchronize schema and large volumes of data.

Copyright 2023-2026, Levente Hunyadi; 2026 Instructure, Inc.

:see: https://github.com/instructure-internal/pysqlsync
"""

from pysqlsync.model.data_types import SqlVariableBinaryType


class RedshiftVariableBinaryType(SqlVariableBinaryType):
    def __str__(self) -> str:
        if self.storage is not None:
            storage = f"({self.storage})"
        else:
            storage = ""
        return f"varbyte{storage}"
