"""
pysqlsync: Synchronize schema and large volumes of data.

Copyright 2023-2026, Levente Hunyadi; 2026 Instructure, Inc.

:see: https://github.com/instructure-internal/pysqlsync
"""

from pysqlsync.base import BaseConnection, BaseEngine, BaseGenerator, Explorer

from ..postgresql.discovery import PostgreSQLExplorer
from .connection import RedshiftConnection
from .generator import RedshiftGenerator


class RedshiftEngine(BaseEngine):
    @property
    def name(self) -> str:
        return "redshift"

    def get_generator_type(self) -> type[BaseGenerator]:
        return RedshiftGenerator

    def get_connection_type(self) -> type[BaseConnection]:
        return RedshiftConnection

    def get_explorer_type(self) -> type[Explorer]:
        return PostgreSQLExplorer
