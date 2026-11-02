"""PidWatcher: call back once when a pid exits, through the PidWaiter the kernel offers (pidfd, kqueue, else polling)."""

from __future__ import annotations

import asyncio
import contextlib
import os
import select
from collections.abc import Callable
from probe.service.server.policy import log
#: Where neither pidfd nor kqueue can watch a pid, poll it this often.
POLL_S = 2.0


class PidWatcher:
    """Calls back once when a pid exits. Event-driven where the kernel can be asked."""

    def __init__(self, loop: asyncio.AbstractEventLoop) -> None:
        self.loop = loop
        self._pidfds: dict[object, int] = {}
        self._kq = None
        self._kq_keys: dict[int, set] = {}
        self._callbacks: dict[object, tuple[int, str, Callable[[], None]]] = {}
        self._polled: set = set()
        self._poll_handle: asyncio.TimerHandle | None = None
        if hasattr(select, "kqueue") and hasattr(select, "KQ_FILTER_PROC"):
            try:
                self._kq = select.kqueue()
                loop.add_reader(self._kq.fileno(), self._drain_kqueue)
            except (OSError, NotImplementedError, ValueError):
                self._kq = None

    @property
    def mechanism(self) -> str:
        if hasattr(os, "pidfd_open"):
            return "pidfd"
        return "kqueue" if self._kq is not None else "poll"

    def watch(self, key: object, pid: int, start: str, callback: Callable[[], None]) -> None:
        self.cancel(key)
        self._callbacks[key] = (pid, start, callback)
        if hasattr(os, "pidfd_open"):
            try:
                fd = os.pidfd_open(pid)
            except ProcessLookupError:
                self.loop.call_soon(self._fire, key)
                return
            except OSError:
                self._poll(key)
                return
            self._pidfds[key] = fd
            self.loop.add_reader(fd, self._fire, key)
            return
        if self._kq is not None:
            keys = self._kq_keys.setdefault(pid, set())
            if not keys:
                try:
                    self._kq.control(
                        [
                            select.kevent(
                                pid,
                                filter=select.KQ_FILTER_PROC,
                                flags=select.KQ_EV_ADD | select.KQ_EV_ONESHOT,
                                fflags=select.KQ_NOTE_EXIT,
                            )
                        ],
                        0,
                        0,
                    )
                except ProcessLookupError:
                    del self._kq_keys[pid]
                    self.loop.call_soon(self._fire, key)
                    return
                except OSError:
                    del self._kq_keys[pid]
                    self._poll(key)
                    return
            keys.add(key)
            return
        self._poll(key)

    def _poll(self, key: object) -> None:
        self._polled.add(key)
        if self._poll_handle is None:
            self._poll_handle = self.loop.call_later(POLL_S, self._poll_tick)

    def _poll_tick(self) -> None:
        from ....foundation.service_api import procid

        self._poll_handle = None
        for key in list(self._polled):
            pid, start, _ = self._callbacks.get(key, (0, "", None))
            if procid.alive(pid, start) is False:
                self._fire(key)
        if self._polled:
            self._poll_handle = self.loop.call_later(POLL_S, self._poll_tick)

    def _drain_kqueue(self) -> None:
        try:
            events = self._kq.control(None, 64, 0)
        except OSError:
            return
        for ev in events:
            for key in list(self._kq_keys.pop(int(ev.ident), ())):
                self._fire(key)

    def _fire(self, key: object) -> None:
        entry = self._callbacks.get(key)
        self.cancel(key)
        if entry is not None:
            try:
                entry[2]()
            except Exception as exc:  # noqa: BLE001
                log(f"owner-exit callback failed: {exc!r}")

    def cancel(self, key: object) -> None:
        entry = self._callbacks.pop(key, None)
        fd = self._pidfds.pop(key, None)
        if fd is not None:
            with contextlib.suppress(Exception):
                self.loop.remove_reader(fd)
            with contextlib.suppress(OSError):
                os.close(fd)
        self._polled.discard(key)
        if entry is not None and self._kq is not None:
            pid = entry[0]
            keys = self._kq_keys.get(pid)
            if keys is not None:
                keys.discard(key)
                if not keys:
                    del self._kq_keys[pid]
                    with contextlib.suppress(OSError):
                        self._kq.control(
                            [select.kevent(pid, filter=select.KQ_FILTER_PROC, flags=select.KQ_EV_DELETE)],
                            0,
                            0,
                        )

    def close(self) -> None:
        for key in list(self._callbacks):
            self.cancel(key)
        if self._poll_handle is not None:
            self._poll_handle.cancel()
        if self._kq is not None:
            with contextlib.suppress(Exception):
                self.loop.remove_reader(self._kq.fileno())
            self._kq.close()
