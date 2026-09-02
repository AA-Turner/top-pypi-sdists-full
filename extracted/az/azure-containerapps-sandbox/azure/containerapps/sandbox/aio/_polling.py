"""Async LRO polling primitives — mirrors :mod:`..._polling` for async clients."""

from __future__ import annotations

import asyncio
import logging
import time
from typing import Any, Awaitable, Callable, Generic, Iterable, TypeVar

from azure.core.exceptions import HttpResponseError, ResourceNotFoundError
from azure.core.polling import AsyncPollingMethod

T = TypeVar("T")
R = TypeVar("R")

logger = logging.getLogger("azure.containerapps.sandbox")


def _normalize_states(states: Iterable[str]) -> frozenset[str]:
    return frozenset(s.lower() for s in states)


class AsyncResourceStatePoller(AsyncPollingMethod, Generic[T, R]):
    """Async version of :class:`...polling.ResourceStatePoller`."""

    def __init__(
        self,
        getter: Callable[[], Awaitable[T]],
        state_fn: Callable[[T], str | None],
        *,
        target_states: Iterable[str],
        failed_states: Iterable[str] = (),
        timeout: int = 300,
        poll_interval: int = 3,
        resource_id: str = "<resource>",
        transform: Callable[[T], R] | None = None,
        initial_resource: T | None = None,
    ) -> None:
        self._getter = getter
        self._state_fn = state_fn
        self._target_states = _normalize_states(target_states)
        self._failed_states = _normalize_states(failed_states)
        self._timeout = timeout
        self._poll_interval = poll_interval
        self._resource_id = resource_id
        self._transform: Callable[[T], R] = transform or (lambda r: r)  # type: ignore[assignment,return-value]
        self._resource: T | None = initial_resource
        self._final: R | None = None
        self._status = "InProgress"
        self._deadline: float = 0.0

    def initialize(self, client, initial_response, deserialization_callback):  # noqa: ARG002
        self._deadline = time.monotonic() + self._timeout

    async def run(self) -> None:
        if self._resource is not None and self._check_state(self._resource):
            return

        while True:
            try:
                self._resource = await self._getter()
            except (ResourceNotFoundError, HttpResponseError) as exc:
                if isinstance(exc, ResourceNotFoundError) or getattr(exc, "status_code", None) == 404:
                    if time.monotonic() > self._deadline:
                        self._status = "Failed"
                        raise TimeoutError(
                            f"{self._resource_id} did not appear within {self._timeout}s"
                        ) from exc
                    await asyncio.sleep(self._poll_interval)
                    continue
                raise

            if self._check_state(self._resource):
                return

            if time.monotonic() > self._deadline:
                self._status = "Failed"
                state = (self._state_fn(self._resource) or "") if self._resource else ""
                raise TimeoutError(
                    f"{self._resource_id} did not reach state "
                    f"{sorted(self._target_states)} within {self._timeout}s "
                    f"(last state: {state!r})"
                )

            logger.info(
                "Polling %s state=%s, next poll in %ds...",
                self._resource_id,
                (self._state_fn(self._resource) if self._resource else None),
                self._poll_interval,
            )
            await asyncio.sleep(self._poll_interval)

    def _check_state(self, resource: T) -> bool:
        state = (self._state_fn(resource) or "").lower()
        if state in self._target_states:
            self._status = "Succeeded"
            self._final = self._transform(resource)
            return True
        if state in self._failed_states:
            self._status = "Failed"
            raise RuntimeError(
                f"{self._resource_id} entered terminal state '{state}'"
            )
        return False

    def status(self) -> str:
        return self._status

    def finished(self) -> bool:
        return self._status in ("Succeeded", "Failed")

    def resource(self) -> R | None:
        return self._final


class AsyncDeletionPoller(AsyncPollingMethod):
    """Async version of :class:`...polling.DeletionPoller`."""

    def __init__(
        self,
        getter: Callable[[], Awaitable[Any]],
        *,
        timeout: int = 300,
        poll_interval: int = 3,
        resource_id: str = "<resource>",
    ) -> None:
        self._getter = getter
        self._timeout = timeout
        self._poll_interval = poll_interval
        self._resource_id = resource_id
        self._status = "InProgress"
        self._deadline: float = 0.0

    def initialize(self, client, initial_response, deserialization_callback):  # noqa: ARG002
        self._deadline = time.monotonic() + self._timeout

    async def run(self) -> None:
        while True:
            try:
                await self._getter()
            except ResourceNotFoundError:
                self._status = "Succeeded"
                return
            except HttpResponseError as exc:
                if getattr(exc, "status_code", None) == 404:
                    self._status = "Succeeded"
                    return
                raise

            if time.monotonic() > self._deadline:
                self._status = "Failed"
                raise TimeoutError(
                    f"{self._resource_id} was not deleted within {self._timeout}s"
                )
            await asyncio.sleep(self._poll_interval)

    def status(self) -> str:
        return self._status

    def finished(self) -> bool:
        return self._status in ("Succeeded", "Failed")

    def resource(self) -> None:
        return None


class AsyncResourceExistsPoller(AsyncPollingMethod, Generic[T]):
    """Async version of :class:`...polling.ResourceExistsPoller`."""

    def __init__(
        self,
        getter: Callable[[], Awaitable[T]],
        *,
        timeout: int = 300,
        poll_interval: int = 3,
        resource_id: str = "<resource>",
        initial_resource: T | None = None,
    ) -> None:
        self._getter = getter
        self._timeout = timeout
        self._poll_interval = poll_interval
        self._resource_id = resource_id
        self._resource: T | None = initial_resource
        self._status = "InProgress"
        self._deadline: float = 0.0

    def initialize(self, client, initial_response, deserialization_callback):  # noqa: ARG002
        self._deadline = time.monotonic() + self._timeout

    async def run(self) -> None:
        while True:
            try:
                self._resource = await self._getter()
                self._status = "Succeeded"
                return
            except (ResourceNotFoundError, HttpResponseError) as exc:
                if isinstance(exc, ResourceNotFoundError) or getattr(exc, "status_code", None) == 404:
                    if time.monotonic() > self._deadline:
                        self._status = "Failed"
                        raise TimeoutError(
                            f"{self._resource_id} did not appear within {self._timeout}s"
                        ) from exc
                    await asyncio.sleep(self._poll_interval)
                    continue
                raise

    def status(self) -> str:
        return self._status

    def finished(self) -> bool:
        return self._status in ("Succeeded", "Failed")

    def resource(self) -> T | None:
        return self._resource


__all__ = ["AsyncResourceStatePoller", "AsyncDeletionPoller", "AsyncResourceExistsPoller"]
