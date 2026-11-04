# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Driver heartbeats through a db:// connection (GEN-970).

The phalanx job runs with invalid AWS credentials, so every heartbeat read and
write here must use the jobs table's vended credentials.
"""

import contextlib
import time
import uuid
from collections.abc import Callable

import pyarrow as pa
import pytest

from geneva import connect
from geneva.db import Connection
from geneva.jobs import DriverLiveness
from geneva.jobs.heartbeat import DRIVER_EXITED, HEARTBEAT_INTERVAL_ENV

_INTERVAL_S = 0.5
_WAIT_S = 60.0


def _wait_for(predicate: Callable[[], bool]) -> None:
    deadline = time.monotonic() + _WAIT_S
    while not predicate():
        if time.monotonic() > deadline:
            raise AssertionError("condition not met in time")
        time.sleep(0.2)


@pytest.fixture(scope="module")
def phalanx_conn(session_db_uri: str, host_override: str, api_key: str) -> Connection:
    return connect(
        uri=session_db_uri,
        api_key=api_key,
        host_override=host_override,
        executor_mode=True,
    )


@pytest.mark.phalanx
def test_driver_heartbeat_uses_vended_credentials(
    phalanx_conn: Connection, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv(HEARTBEAT_INTERVAL_ENV, str(_INTERVAL_S))
    # Establish the db (and, lazily, the jobs table).
    name = f"heartbeat_{uuid.uuid4().hex[:8]}"
    phalanx_conn.create_table(name, pa.table({"id": [1, 2, 3]}))
    hist = phalanx_conn._history
    job_id = hist.launch(name, "col", job_id=uuid.uuid4().hex).job_id
    try:
        hist.set_running(job_id)
        assert hist.driver_liveness(hist.get(job_id)[0]) is DriverLiveness.UNKNOWN

        writer = hist.start_driver_heartbeat(job_id)
        assert writer is not None
        try:
            _wait_for(
                lambda: (
                    hist.driver_liveness(hist.get(job_id)[0]) is DriverLiveness.ALIVE
                )
            )
            # Reopen the file session, as after a credential refresh, and
            # check heartbeats keep landing.
            first = hist.get_heartbeat(job_id)
            assert first is not None
            hist._heartbeats._reset_session()
            _wait_for(lambda: (hist.get_heartbeat(job_id) or first).seq > first.seq)
        finally:
            writer.stop()

        heartbeat = hist.get_heartbeat(job_id)
        assert heartbeat is not None
        assert heartbeat.state == DRIVER_EXITED
        assert hist.driver_liveness(hist.get(job_id)[0]) is DriverLiveness.EXITED

        # A re-run under the same id deletes the previous run's heartbeat.
        hist.set_failed(job_id, "previous run failed")
        hist.set_running(job_id)
        assert hist.get_heartbeat(job_id) is None
        assert hist.driver_liveness(hist.get(job_id)[0]) is DriverLiveness.UNKNOWN
    finally:
        with contextlib.suppress(Exception):
            hist.set_completed(job_id)
        with contextlib.suppress(Exception):
            phalanx_conn.drop_table(name)
