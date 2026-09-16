# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import json
import os
import threading

import pytest
from lancedb.background_loop import LOOP


@pytest.mark.skipif(not hasattr(os, "fork"), reason="requires os.fork")
@pytest.mark.timeout(10)
def test_lancedb_loop_restarts_lazily_after_fork(monkeypatch) -> None:
    """The child atfork callback must not start a Python thread."""
    read_fd, write_fd = os.pipe()
    fork_returned = False
    starts: list[tuple[bool, str]] = []
    original_start = threading.Thread.start

    def tracked_start(thread: threading.Thread) -> None:
        starts.append((fork_returned, thread.name))
        original_start(thread)

    monkeypatch.setattr(threading.Thread, "start", tracked_start)
    child_pid = os.fork()
    if child_pid == 0:
        os.close(read_fd)
        try:
            fork_returned = True

            async def child_pid_async() -> int:
                return os.getpid()

            value = LOOP.run(child_pid_async())
            payload = {
                "value": value,
                "starts_before_fork_return": [
                    name for returned, name in starts if not returned
                ],
                "starts_after_fork_return": [
                    name for returned, name in starts if returned
                ],
            }
        except BaseException as exc:
            payload = {"error": repr(exc)}
        os.write(write_fd, json.dumps(payload).encode())
        os.close(write_fd)
        os._exit(0)

    fork_returned = True
    os.close(write_fd)
    try:
        payload = json.loads(os.read(read_fd, 64 * 1024))
    finally:
        os.close(read_fd)
        _, status = os.waitpid(child_pid, 0)

    assert os.waitstatus_to_exitcode(status) == 0
    assert "error" not in payload, payload.get("error")
    assert payload["starts_before_fork_return"] == []
    assert payload["value"] == child_pid
    assert payload["starts_after_fork_return"] == ["LanceDBBackgroundEventLoop"]
