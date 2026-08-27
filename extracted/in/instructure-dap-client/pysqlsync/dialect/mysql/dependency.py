"""
pysqlsync: Synchronize schema and large volumes of data.

This module defines dependencies required for MySQL.

Copyright 2023-2026, Levente Hunyadi; 2026 Instructure, Inc.

:see: https://github.com/instructure-internal/pysqlsync
"""

import aiomysql  # pyright: ignore[reportUnusedImport] # noqa: F401
import cryptography  # pyright: ignore[reportUnusedImport] # noqa: F401
