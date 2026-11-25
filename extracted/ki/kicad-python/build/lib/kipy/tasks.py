# Copyright The KiCad Developers
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the “Software”), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Handles for long-running tasks started through the API.

Only one API task can run at a time.  While it runs, KiCad rejects other commands with
``AS_BUSY``; task status and result queries remain available.  Note that the task itself
runs on KiCad's main thread, so the client timeout must be long enough to cover the whole
task (a status query is answered only when KiCad gets a chance to service it).
"""

from __future__ import annotations

import time

from kipy.client import KiCadClient
from kipy.proto.common import tasks_pb2
from kipy.proto.common.tasks_pb2 import TaskState
from kipy.wrapper import Wrapper


class TaskStatus(Wrapper):
    """A snapshot of a task's state, as returned by ``GetTaskStatus``"""

    def __init__(
        self,
        proto: tasks_pb2.TaskStatusResponse | None = None,
        proto_ref: tasks_pb2.TaskStatusResponse | None = None,
    ):
        self._proto = proto_ref if proto_ref is not None else tasks_pb2.TaskStatusResponse()

        if proto is not None:
            self._proto.CopyFrom(proto)

    def __repr__(self) -> str:
        if self.error_message:
            return f"<TaskStatus state={self.state} error={self.error_message!r}>"
        return f"<TaskStatus state={self.state}>"

    @property
    def state(self) -> TaskState.ValueType:
        return self._proto.state

    @property
    def error_message(self) -> str:
        """Populated when the task failed or was cancelled; empty otherwise"""
        return self._proto.error_message

    @property
    def running(self) -> bool:
        return self.state == TaskState.TS_RUNNING

    @property
    def completed(self) -> bool:
        return self.state == TaskState.TS_COMPLETED

    @property
    def failed(self) -> bool:
        return self.state == TaskState.TS_FAILED

    @property
    def cancelled(self) -> bool:
        return self.state == TaskState.TS_CANCELLED

    @property
    def done(self) -> bool:
        """True once the task reached a terminal state (completed, failed or cancelled)"""
        return self.state in (
            TaskState.TS_COMPLETED,
            TaskState.TS_FAILED,
            TaskState.TS_CANCELLED,
        )


class Task:
    """A handle to a long-running task started by the API.

    Tasks are started by document methods (for example
    :meth:`kipy.board.Board.start_refill_zones_task`) and identified by an opaque token.
    Use :meth:`get_status` to poll or :meth:`wait` to block until completion.
    """

    def __init__(self, client: KiCadClient, token: str):
        self._client = client
        self._token = token

    @classmethod
    def from_start_response(
        cls, client: KiCadClient, response: tasks_pb2.StartTaskResponse
    ) -> Task:
        """Builds a task handle from the response to a start-task request"""
        return cls(client, response.token.value)

    def __repr__(self) -> str:
        return f"<Task token={self._token}>"

    @property
    def token(self) -> str:
        """The opaque token used to query this task"""
        return self._token

    def get_status(self) -> TaskStatus:
        """Returns a snapshot of the task's current state.

        .. versionadded:: 0.x.y (KiCad 11)
        """
        command = tasks_pb2.GetTaskStatus()
        command.token.value = self._token
        return TaskStatus(self._client.send(command, tasks_pb2.TaskStatusResponse))

    def wait(self, timeout: float | None = None, poll_interval: float = 0.1) -> TaskStatus:
        """Blocks until the task reaches a terminal state.

        The returned status may report completion, failure, or cancellation; inspect
        :attr:`TaskStatus.completed`, :attr:`TaskStatus.failed` and
        :attr:`TaskStatus.cancelled` (or :attr:`TaskStatus.error_message`) to tell them apart.

        :param timeout: Maximum number of seconds to wait, or ``None`` to wait indefinitely.
            This is a client-side limit; each individual status request is also bounded by
            the client's ``timeout_ms``, which must itself exceed the task's runtime.
        :param poll_interval: Seconds to sleep between status queries.
        :raises TimeoutError: if the task is still running when ``timeout`` expires.
        """
        deadline = None if timeout is None else time.monotonic() + timeout

        while True:
            status = self.get_status()

            if status.done:
                return status

            if deadline is not None and time.monotonic() >= deadline:
                raise TimeoutError(f"task {self._token} did not finish within {timeout} seconds")

            time.sleep(poll_interval)
