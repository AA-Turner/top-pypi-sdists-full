# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Regression: job-state queries over a pushdown namespace connection must
not overflow the namespace ``query_table`` binding.

lancedb's ``_query_to_namespace_request`` encodes an *unlimited* query as
``k = sys.maxsize`` (i64::MAX). The namespace ``query_table`` binding's
``k`` field is 32-bit, so that value overflows at the Python->Rust
boundary with::

    OverflowError: out of range integral type conversion attempted

The job-state manager (``Connection.list_jobs`` / ``get_job``) issues
exactly such an unlimited query on the ``_geneva_jobs`` table. The crash
only surfaces when the connection has ``QueryTable`` pushdown enabled
(server-side query execution) — which is the default for enterprise
(``db://``) connections — so it was invisible to the local/unit suite and
only blew up inside the enterprise backfill/refresh driver. These tests
pin the contract using a ``dir`` namespace with pushdown forced on, so
they reproduce the failure in-process with no phalanx/driver/Ray.
"""

import pyarrow as pa
import pytest

from geneva import connect
from geneva.db import Connection


@pytest.fixture
def pushdown_db(tmp_path) -> Connection:
    """Namespace connection with ``QueryTable`` pushdown enabled — the
    server-side-query mode used by enterprise (``db://``) connections,
    which routes unlimited reads through the ``query_table`` binding."""
    db = connect(
        namespace_client_impl="dir",
        namespace_client_properties={"root": str(tmp_path)},
        namespace_client_pushdown_operations=["QueryTable"],
    )
    # Realize the connection / system tables.
    db.create_table("t", pa.table({"id": [0, 1, 2]}))
    return db


def test_list_jobs_no_limit_query_does_not_overflow(pushdown_db: Connection) -> None:
    # list_jobs() scans _geneva_jobs with no limit (k -> "all"); it must
    # complete rather than overflow the query_table binding.
    assert pushdown_db.list_jobs() == []


def test_get_job_no_limit_query_does_not_overflow(pushdown_db: Connection) -> None:
    # get_job() filters _geneva_jobs (also unlimited). A missing job must
    # surface as a clean ValueError, not an OverflowError from the binding.
    with pytest.raises(ValueError, match="not found"):
        pushdown_db.get_job("does-not-exist")
