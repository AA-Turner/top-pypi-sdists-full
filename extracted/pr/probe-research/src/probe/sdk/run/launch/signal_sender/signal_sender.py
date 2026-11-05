"""SignalSender: which process sent this one a signal, as the kernel recorded it (DESIGN.md).

The recorder (`recorder.c`, built per arch into ``lib/``) saves the sender at delivery; anywhere it
is missing (macOS, musl, another arch) every read is None and callers keep their old behaviour."""

from __future__ import annotations

import ctypes
import os
import platform
import sys
from dataclasses import dataclass
from pathlib import Path

#: Where release.yml puts the built recorders, one per arch: ``recorder-<arch>.so``.
_LIB_DIR = Path(__file__).resolve().parent / "lib"
_ARCHES = {"x86_64": "x86_64", "amd64": "x86_64", "aarch64": "aarch64", "arm64": "aarch64"}
#: The most of a sender's environment read for its session: environments are a few KB.
_ENVIRON_CAP_BYTES = 1 << 20


@dataclass(frozen=True)
class Sent:
    """The last sender of a signal: its pid, real uid and ``si_code``, and this process's parent
    when it arrived (a supervisor that signals and exits leaves this process reparented)."""

    pid: int
    uid: int
    code: int
    parent: int = -1

    def is_another_local_process(self) -> bool:
        """Sent with kill() by another process of this user in this pid namespace: not the kernel
        (``si_code`` > 0), not this process, not its parent (a supervisor such as torchrun), not 0
        (outside this pid namespace: a container runtime, the kubelet) and not 1 (init)."""
        if self.code > 0 or self.uid != os.getuid():
            return False
        return self.pid not in (0, 1, os.getpid(), self.parent, os.getppid())


class SignalSender:
    """The loaded recorder. One per process (`load_sender`)."""

    def __init__(self, library: ctypes.CDLL) -> None:
        self._arm = library.probe_sender_arm
        self._arm.argtypes = [ctypes.c_int]
        self._arm.restype = ctypes.c_int
        self._is_armed = library.probe_sender_is_armed
        self._is_armed.argtypes = [ctypes.c_int]
        self._is_armed.restype = ctypes.c_int
        self._last = library.probe_sender_last
        self._last.argtypes = [
            ctypes.c_int,
            ctypes.POINTER(ctypes.c_int),
            ctypes.POINTER(ctypes.c_uint),
            ctypes.POINTER(ctypes.c_int),
            ctypes.POINTER(ctypes.c_int),
        ]
        self._last.restype = ctypes.c_ulong
        #: Per signal, the delivery count already read (or current when re-armed): only a newer
        #: delivery is this signal's sender.
        self._read_counts: dict[int, int] = {}

    def install(self, signum: int) -> bool:
        """Stand in front of the handler ``signum`` has now. Again after a ``signal.signal`` put
        CPython's own back (Lightning's ``fit()``). True when armed afterwards."""
        result = self._arm(int(signum))
        if result == 2:
            # Newly in front: what arrived while it was not is no sender of a later signal.
            self._read_counts[int(signum)] = self._read_count(int(signum))
        return result in (1, 2)

    def read_last(self, signum: int) -> Sent | None:
        """The sender of the latest ``signum`` not read before; None when none arrived through the
        recorder since, or it is not in front now (a handler set since took the signal, and an
        older unread delivery would name the wrong sender)."""
        count, sent = self._read_raw(int(signum))
        is_fresh = count != self._read_counts.get(int(signum), 0)
        self._read_counts[int(signum)] = count
        if not is_fresh or not self._is_armed(int(signum)):
            return None
        return sent

    def _read_raw(self, signum: int) -> tuple[int, Sent]:
        pid, uid, code, parent = ctypes.c_int(), ctypes.c_uint(), ctypes.c_int(), ctypes.c_int()
        count = int(self._last(
            signum, ctypes.byref(pid), ctypes.byref(uid), ctypes.byref(code), ctypes.byref(parent)
        ))
        return count, Sent(pid=pid.value, uid=uid.value, code=code.value, parent=parent.value)

    def _read_count(self, signum: int) -> int:
        return self._read_raw(signum)[0]


_loaded: SignalSender | None = None
_has_tried = False


def load_sender() -> SignalSender | None:
    """This process's recorder, loaded once; None where none is built or it will not load."""
    global _loaded, _has_tried
    if _has_tried:
        return _loaded
    _has_tried = True
    arch = _ARCHES.get(platform.machine().lower())
    if not sys.platform.startswith("linux") or arch is None:
        return None
    try:
        _loaded = SignalSender(ctypes.CDLL(str(_LIB_DIR / f"recorder-{arch}.so")))
    except (OSError, AttributeError):
        _loaded = None
    return _loaded


def read_session(pid: int) -> str | None:
    """The coding-agent session the sender ran in, from its environment; None when it is gone,
    unreadable or ran in none. Plain syscalls: called from the SIGTERM handler (DESIGN.md)."""
    if pid <= 1:
        return None
    try:
        fd = os.open(f"/proc/{pid}/environ", os.O_RDONLY)
    except OSError:
        return None
    chunks: list[bytes] = []
    size = 0
    try:
        while size < _ENVIRON_CAP_BYTES:
            chunk = os.read(fd, 65536)
            if not chunk:
                break
            chunks.append(chunk)
            size += len(chunk)
    except OSError:
        return None
    finally:
        os.close(fd)
    env: dict[str, str] = {}
    for item in b"".join(chunks).split(b"\0"):
        key, sep, value = item.partition(b"=")
        if sep:
            env[key.decode("utf-8", "replace")] = value.decode("utf-8", "replace")
    from ....agent_session import session_id_from_env

    return session_id_from_env(env)
