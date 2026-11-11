from __future__ import annotations

import asyncio
import threading
import time
from collections import deque
from typing import Any, Callable, Deque, Dict, Optional, Set, Union

from .errors import HOST_DISCONNECTED, NOTIFICATIONS_LAGGED, SuperDocError
from .protocol import JsonRpcNotification

DEFAULT_NOTIFICATION_CAPACITY = 64
_LAGGED_MESSAGE = 'resynchronize document state before using notification-derived caches'
_RESYNC_HINT = 'Call changes.list with the cursor of the last change record you processed.'
_CLOSED_MESSAGE = 'notification stream closed'

HostNotification = Dict[str, Any]


def _validate_capacity(capacity: Any) -> int:
    if type(capacity) is not int or capacity < 1:
        raise SuperDocError(
            'Notification capacity must be a positive integer.',
            code='INVALID_ARGUMENT',
            details={'capacity': capacity},
        )
    return capacity


def notification_frame(message: JsonRpcNotification) -> HostNotification:
    if message.frame is not None:
        return dict(message.frame)
    frame: HostNotification = {'jsonrpc': '2.0', 'method': message.method}
    if message.params is not None:
        frame['params'] = message.params
    return frame


def _lagged_error(skipped: int) -> SuperDocError:
    return SuperDocError(
        _LAGGED_MESSAGE,
        code=NOTIFICATIONS_LAGGED,
        details={'skipped': skipped, 'resync': _RESYNC_HINT},
    )


class _Buffer:
    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.queue: Deque[HostNotification] = deque()
        self.skipped = 0
        self.failure: Optional[SuperDocError] = None
        self.closed = False

    def push(self, frame: HostNotification) -> None:
        if self.closed:
            return
        if len(self.queue) >= self.capacity:
            self.queue.popleft()
            self.skipped += 1
        self.queue.append(frame)

    def take(self) -> Optional[HostNotification]:
        if self.skipped:
            skipped = self.skipped
            self.skipped = 0
            raise _lagged_error(skipped)
        if self.queue:
            return self.queue.popleft()
        if self.failure is not None:
            failure = self.failure
            self.failure = None
            raise failure
        return None

    def close(self) -> None:
        self.closed = True
        self.queue.clear()
        self.skipped = 0
        self.failure = None


class Notifications:
    def __init__(self, capacity: int, detach: Callable[['Notifications'], None]) -> None:
        self._buffer = _Buffer(capacity)
        self._condition = threading.Condition()
        self._detach = detach

    def recv(self, timeout: Optional[float] = None) -> Optional[HostNotification]:
        deadline = None if timeout is None else time.monotonic() + timeout
        with self._condition:
            while True:
                frame = self._buffer.take()
                if frame is not None:
                    return frame
                if self._buffer.closed:
                    raise SuperDocError(_CLOSED_MESSAGE, code=HOST_DISCONNECTED)
                if deadline is None:
                    self._condition.wait()
                    continue
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    return None
                self._condition.wait(remaining)

    def close(self) -> None:
        with self._condition:
            if self._buffer.closed:
                return
            self._buffer.close()
            self._condition.notify_all()
        self._detach(self)

    @property
    def closed(self) -> bool:
        return self._buffer.closed

    def __iter__(self) -> 'Notifications':
        return self

    def __next__(self) -> HostNotification:
        try:
            frame = self.recv()
        except SuperDocError as error:
            if self._buffer.closed and error.code == HOST_DISCONNECTED:
                raise StopIteration from None
            raise
        assert frame is not None
        return frame

    def __enter__(self) -> 'Notifications':
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    def _deliver(self, frame: HostNotification) -> None:
        with self._condition:
            self._buffer.push(frame)
            self._condition.notify_all()

    def _fail(self, error: SuperDocError) -> None:
        with self._condition:
            if not self._buffer.closed:
                self._buffer.failure = error
            self._condition.notify_all()


class AsyncNotifications:
    def __init__(self, capacity: int, detach: Callable[['AsyncNotifications'], None]) -> None:
        self._buffer = _Buffer(capacity)
        self._detach = detach
        self._changed: Optional[asyncio.Event] = None

    async def recv(self, timeout: Optional[float] = None) -> Optional[HostNotification]:
        loop = asyncio.get_running_loop()
        deadline = None if timeout is None else loop.time() + timeout
        while True:
            frame = self._buffer.take()
            if frame is not None:
                return frame
            if self._buffer.closed:
                raise SuperDocError(_CLOSED_MESSAGE, code=HOST_DISCONNECTED)
            if self._changed is None:
                self._changed = asyncio.Event()
            self._changed.clear()
            if deadline is None:
                await self._changed.wait()
                continue
            remaining = deadline - loop.time()
            if remaining <= 0:
                return None
            try:
                await asyncio.wait_for(self._changed.wait(), timeout=remaining)
            except asyncio.TimeoutError:
                return None

    def close(self) -> None:
        if self._buffer.closed:
            return
        self._buffer.close()
        self._wake()
        self._detach(self)

    @property
    def closed(self) -> bool:
        return self._buffer.closed

    def __aiter__(self) -> 'AsyncNotifications':
        return self

    async def __anext__(self) -> HostNotification:
        try:
            frame = await self.recv()
        except SuperDocError as error:
            if self._buffer.closed and error.code == HOST_DISCONNECTED:
                raise StopAsyncIteration from None
            raise
        assert frame is not None
        return frame

    async def __aenter__(self) -> 'AsyncNotifications':
        return self

    async def __aexit__(self, *exc: object) -> None:
        self.close()

    def _wake(self) -> None:
        if self._changed is not None:
            self._changed.set()

    def _deliver(self, frame: HostNotification) -> None:
        self._buffer.push(frame)
        self._wake()

    def _fail(self, error: SuperDocError) -> None:
        if not self._buffer.closed:
            self._buffer.failure = error
        self._wake()


Subscription = Union[Notifications, AsyncNotifications]


class NotificationHub:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._subscriptions: Set[Subscription] = set()

    def subscribe_sync(self, capacity: int = DEFAULT_NOTIFICATION_CAPACITY) -> Notifications:
        subscription = Notifications(_validate_capacity(capacity), self._detach)
        with self._lock:
            self._subscriptions.add(subscription)
        return subscription

    def subscribe_async(self, capacity: int = DEFAULT_NOTIFICATION_CAPACITY) -> AsyncNotifications:
        subscription = AsyncNotifications(_validate_capacity(capacity), self._detach)
        with self._lock:
            self._subscriptions.add(subscription)
        return subscription

    def publish(self, message: JsonRpcNotification) -> None:
        with self._lock:
            subscriptions = list(self._subscriptions)
        if not subscriptions:
            return
        frame = notification_frame(message)
        for subscription in subscriptions:
            subscription._deliver(dict(frame))

    def disconnect(self, error: SuperDocError) -> None:
        with self._lock:
            subscriptions = list(self._subscriptions)
        for subscription in subscriptions:
            subscription._fail(error)

    def close(self) -> None:
        with self._lock:
            subscriptions = list(self._subscriptions)
        for subscription in subscriptions:
            subscription.close()

    def _detach(self, subscription: Subscription) -> None:
        with self._lock:
            self._subscriptions.discard(subscription)
