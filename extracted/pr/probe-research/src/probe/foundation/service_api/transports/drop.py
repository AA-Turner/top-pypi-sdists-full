"""The drop folder transport (service-only plan Q1 = A): a fenced caller whose sandbox refuses the socket writes its request as a file.

    <drop>/.<id>.tmp                   written, kept open for writing (the service names the writer by it)
    <drop>/requests/<id>.req.json      renamed in: {"v": 1, "pid", "pid_ns", "answer", "messages": [hello, request]}
    <drop>/answers/<answer>.ans.json   the service's answer: {"v": 1, "for": <id>, "messages": [hello's, request's]}

`<drop>` is `paths.get_drop_dir()` (0700, this user's); `requests/` holds only requests (launchd
starts the service while it holds any). `<id>` and `<answer>` are 32 random hex digits: the answer's
name the request carries, and its `for` must be the request's id. Every fenced session of this
user shares the folder (a known limit: one fenced agent can read or race another's; the fence
protects the machine from an agent, not agents of one user from each other). The service's twin is
`probe.service.server.connections.drop_door`. No file descriptors cross it: a call that needs the
caller's terminal says INTERACTIVE_NEEDS_TERMINAL. Each request carries its own hello (a fresh
connection to the service).
"""

from __future__ import annotations

import contextlib
import json
import os
import time
import uuid
from collections.abc import Sequence

from .. import paths
from ..service_api import AnswerTimeout, ServiceError
from ..wire import API_VERSION, MAX_LINE_BYTES, Method, request
from .folder_watch import FolderWatch
from .transport import INTERACTIVE_NEEDS_TERMINAL, Channel, FdsUnsupportedError, Transport

DROP_V = 1
REQUEST_SUFFIX = ".req.json"
ANSWER_SUFFIX = ".ans.json"
TEMP_SUFFIX = ".tmp"
#: A request or an answer is at most this big (a hello and one request line, each at most a line).
MAX_DROP_BYTES = 2 * MAX_LINE_BYTES + 4096
#: What a drop call waits for its answer by default: room for the OS to start the service (D19).
DROP_TIMEOUT_S = 5.0
#: What a request may wait to be taken however long its answer may take (a fenced `probe ask --wait`):
#: no service running and none the OS starts fails in a minute, never at the answer's 30; a slow
#: activation on a loaded machine still has room. A service that read the request and stalled past
#: this before removing it would run what the caller calls not taken: a fenced command only reads or
#: asks (D30), and the window is one read.
TAKE_TIMEOUT_S = 60.0
#: Where no folder watch can be made (a kernel or sandbox refusing inotify): look this often.
FALLBACK_LOOK_S = 0.005


def get_pid_namespace() -> str:
    """This process's pid namespace (`pid:[<inode>]`, Linux), so the service finds it from
    outside a sandbox that has its own; "" elsewhere."""
    try:
        return os.readlink("/proc/self/ns/pid")
    except OSError:
        return ""


def make_request_body(messages: list, answer: str) -> bytes:
    return json.dumps({"v": DROP_V, "pid": os.getpid(), "pid_ns": get_pid_namespace(), "answer": answer,
                       "messages": messages}, separators=(",", ":")).encode("utf-8")


def read_answer_body(raw: bytes, ident: str) -> list:
    """The messages of the answer to the request `ident`; ValueError for anything else."""
    data = json.loads(raw.decode("utf-8"))
    if not isinstance(data, dict) or data.get("v") != DROP_V or not isinstance(data.get("messages"), list):
        raise ValueError("not a drop answer")
    if data.get("for") != ident:
        raise ValueError("an answer to another request")
    return data["messages"]


class DropChannel(Channel):
    """Calls through the drop folder; every call is one request file and one answer file."""

    def __init__(self, folder, timeout: float, client: str, client_version: str) -> None:
        self.folder = folder
        self.requests = os.path.join(folder, paths.DROP_REQUESTS_DIRNAME)
        self.answers = os.path.join(folder, paths.DROP_ANSWERS_DIRNAME)
        self.timeout = timeout
        self.hello = {}
        self._hello_parameters = {"client": client, "client_version": client_version or "unknown", "api": API_VERSION}

    def call(self, method: str, parameters: dict | None = None, fds: Sequence[int] = ()) -> dict:
        if fds:
            raise FdsUnsupportedError(INTERACTIVE_NEEDS_TERMINAL)
        messages = [request(1, Method.HELLO, self._hello_parameters)]
        if method != Method.HELLO:
            messages.append(request(2, method, parameters))
        answers = self._exchange(messages)
        replies = [_read_reply(message) for message in answers]
        self.hello = replies[0] if isinstance(replies[0], dict) else {}
        return replies[-1]

    def close(self) -> None:
        pass

    def _exchange(self, messages: list) -> list:
        """Write the request, keep it open, wait for the answer by `timeout`."""
        ident, token = uuid.uuid4().hex, uuid.uuid4().hex
        temp = os.path.join(self.folder, f".{ident}{TEMP_SUFFIX}")
        asked = os.path.join(self.requests, f"{ident}{REQUEST_SUFFIX}")
        answer = os.path.join(self.answers, f"{token}{ANSWER_SUFFIX}")
        deadline = time.monotonic() + self.timeout
        take_by = min(deadline, time.monotonic() + TAKE_TIMEOUT_S)
        try:
            watch = FolderWatch(self.answers)
        except OSError:
            watch = None
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0)
        fd = os.open(temp, flags, 0o600)
        try:
            os.write(fd, make_request_body(messages, token))
            os.rename(temp, asked)
            return read_answer_body(_wait_for(answer, asked, deadline, watch, take_by), ident)
        finally:
            os.close(fd)  # held until now: the service names the writer by this open file
            with contextlib.suppress(OSError):
                os.unlink(temp)
            if watch is not None:
                watch.close()


class DropTransport(Transport):
    """The drop folder; OSError when it is not this user's private folder (no service ever ran)."""

    def connect(self, timeout: float = DROP_TIMEOUT_S, *, client: str, client_version: str) -> DropChannel:
        folder = paths.get_drop_dir()
        for each in (folder, paths.get_drop_requests_dir(), paths.get_drop_answers_dir()):
            paths.require_private(each)
        return DropChannel(str(folder), timeout, client, client_version)


def _wait_for(answer: str, asked: str, deadline: float, watch: FolderWatch | None,
              take_by: float | None = None) -> bytes:
    """The answer's bytes once it is there; ConnectionRefusedError when the request was not taken
    by `take_by` (or the deadline; it is withdrawn), AnswerTimeout when it was and no answer came by
    the deadline. The service removes a request once it reads it: taken is `asked` gone."""
    take_by = deadline if take_by is None else min(take_by, deadline)
    while True:
        raw = _take(answer)
        if raw is not None:
            return raw
        now = time.monotonic()
        if take_by is not None and now >= take_by:
            try:
                os.unlink(asked)
            except FileNotFoundError:
                take_by = None  # taken: its answer may take until the deadline
            else:
                raise ConnectionRefusedError("no Probe service took the request in time")
        left = deadline - now
        if left <= 0:
            raise AnswerTimeout("the Probe service took the request and did not answer in time")
        wait = left if take_by is None else max(0.0, min(left, take_by - now))
        if watch is not None:
            watch.wait(wait)
        else:
            time.sleep(min(wait, FALLBACK_LOOK_S))


def _take(path: str) -> bytes | None:
    """The answer file's bytes, removed; None when it is not there yet. Only a regular file of this user's."""
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NONBLOCK | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0))
    except FileNotFoundError:
        return None
    try:
        st = os.fstat(fd)
        if st.st_uid != os.getuid() or not (st.st_mode & 0o170000 == 0o100000):
            raise PermissionError(f"{path} is not this user's answer")
        raw = os.read(fd, MAX_DROP_BYTES + 1)
    finally:
        os.close(fd)
    with contextlib.suppress(OSError):
        os.unlink(path)
    if len(raw) > MAX_DROP_BYTES:
        raise ConnectionError("the Probe service's answer is too big")
    return raw


def _read_reply(message: object) -> object:
    if not isinstance(message, dict):
        raise ConnectionError("the Probe service answered something other than a JSON object")
    if "error" in message:
        failure = message["error"] or {}
        raise ServiceError(int(failure.get("code", 0)), str(failure.get("message", "")), failure.get("data"))
    return message.get("result")
