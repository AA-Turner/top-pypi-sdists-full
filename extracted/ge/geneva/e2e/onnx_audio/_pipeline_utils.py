# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Shared helpers for local ONNX audio e2e pipelines."""

from __future__ import annotations

import contextlib
from contextlib import AbstractContextManager
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import geneva


def _default_local_context(
    conn: geneva.Connection,
) -> AbstractContextManager[None]:
    local_ctx = getattr(conn, "local_ray_context", None)
    if callable(local_ctx):
        return local_ctx()
    return contextlib.nullcontext()


def _open_or_create_table(
    conn: geneva.Connection,
    table_name: str,
    rows: list[dict[str, Any]],
) -> geneva.Table:
    """Open a table if it exists, otherwise create it from ``rows``."""

    try:
        return conn.open_table(table_name)
    except Exception:
        return conn.create_table(table_name, data=rows, mode="create")
