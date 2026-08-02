# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Reproduces the "job not found" read-after-write failure on the geneva
system tables via phalanx when weak_read_consistency_interval_seconds is set
"""

import contextlib
import uuid

import pyarrow as pa
import pytest

from geneva import connect
from geneva.db import Connection


@pytest.fixture(scope="class")
def phalanx_conn(session_db_uri: str, host_override: str, api_key: str) -> Connection:
    return connect(
        uri=session_db_uri,
        api_key=api_key,
        host_override=host_override,
        executor_mode=True,
    )


@pytest.mark.phalanx
def test_job_visible_immediately_after_launch(phalanx_conn: Connection) -> None:
    # Establish the db (and, lazily, the __system/_geneva_jobs table).
    name = f"jobs_consistency_{uuid.uuid4().hex[:8]}"
    phalanx_conn.create_table(name, pa.table({"id": [1, 2, 3]}))
    try:
        for _ in range(5):
            job_id = uuid.uuid4().hex
            assert phalanx_conn._history.get(job_id) == []

            # Write a job row via JobStateManager (the client launch path).
            jr = phalanx_conn._history.launch(name, "col", job_id=job_id)

            phalanx_conn._history.table.checkout_latest()

            # Must be visible immediately, despite phalanx cache
            rec = phalanx_conn.get_job(jr.job_id)
            assert rec.job_id == jr.job_id, (
                f"job {jr.job_id} not visible immediately after launch; "
                f"phalanx is serving a stale cached view of the system table"
            )
    finally:
        with contextlib.suppress(Exception):
            phalanx_conn.drop_table(name)
