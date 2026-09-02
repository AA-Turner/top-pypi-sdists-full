"""Long-running operation (LRO) polling primitives.

This SDK uses Azure-style ``begin_*`` methods that return
:class:`~azure.core.polling.LROPoller` for any operation that takes more than
a few seconds (create sandbox, commit disk, stop/resume, etc.). Callers can:

* ``poller.result()`` — block until completion
* ``poller.status()`` — peek at current state ("InProgress" | "Succeeded" | "Failed")
* ``poller.done()`` — non-blocking completion check
* ``poller.wait(timeout=...)`` — block with a timeout
* Parallelize: ``[client.begin_create_sandbox(...) for _ in range(N)]`` then
  ``[p.result() for p in pollers]``

Our data-plane API does **not** use the ARM ``Azure-AsyncOperation`` /
``Location`` header convention. Instead, the resource has a ``state`` (or
``status.state``) field that transitions from ``Creating``/``Resuming`` to a
terminal value like ``Running``/``Ready``. We poll the resource via its
GET endpoint until the target state (or a failed state) is reached.

For deletion, we poll until GET returns 404.
"""

from __future__ import annotations

import logging
import time
from typing import Any, Callable, Generic, Iterable, TypeVar

from azure.core.exceptions import HttpResponseError, ResourceNotFoundError
from azure.core.polling import PollingMethod

T = TypeVar("T")
R = TypeVar("R")

logger = logging.getLogger("azure.containerapps.sandbox")


def _normalize_states(states: Iterable[str]) -> frozenset[str]:
    return frozenset(s.lower() for s in states)


class ResourceStatePoller(PollingMethod, Generic[T, R]):
    """Polls a resource via *getter* until it reaches one of *target_states*.

    The poller calls *getter()* every *poll_interval* seconds, extracts the
    state with *state_fn*, and returns when the state matches *target_states*.
    If the state matches *failed_states* the poll raises :class:`RuntimeError`.
    If the deadline passes, the poll raises :class:`TimeoutError`.

    The final result is *transform(resource)* — by default the resource
    itself, but useful for wrapping (e.g. ``Sandbox`` → ``SandboxClient``).
    """

    def __init__(
        self,
        getter: Callable[[], T],
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
        self._initial_resource = initial_resource
        self._resource: T | None = initial_resource
        self._final: R | None = None
        self._status = "InProgress"
        self._deadline: float = 0.0

    # ---- PollingMethod API ----
    def initialize(self, client, initial_response, deserialization_callback):  # noqa: ARG002
        self._deadline = time.monotonic() + self._timeout

    def run(self) -> None:
        # Quick-check initial resource (may already be in target state)
        if self._resource is not None:
            if self._check_state(self._resource):
                return

        while True:
            try:
                self._resource = self._getter()
            except (ResourceNotFoundError, HttpResponseError) as exc:
                if isinstance(exc, ResourceNotFoundError) or getattr(exc, "status_code", None) == 404:
                    # Transient — the resource may not yet be visible after PUT.
                    if time.monotonic() > self._deadline:
                        self._status = "Failed"
                        raise TimeoutError(
                            f"{self._resource_id} did not appear within {self._timeout}s"
                        ) from exc
                    time.sleep(self._poll_interval)
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
            time.sleep(self._poll_interval)

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


class DeletionPoller(PollingMethod):
    """Polls a resource via *getter* until it returns 404 (deleted)."""

    def __init__(
        self,
        getter: Callable[[], Any],
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

    def run(self) -> None:
        while True:
            try:
                self._getter()
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
            time.sleep(self._poll_interval)

    def status(self) -> str:
        return self._status

    def finished(self) -> bool:
        return self._status in ("Succeeded", "Failed")

    def resource(self) -> None:
        return None


class ResourceExistsPoller(PollingMethod, Generic[T]):
    """Polls a resource via *getter* until it returns successfully (GET 200).

    For dataplane operations that synchronously return the created resource
    but where a follow-up GET on the group-scoped path may be subject to
    eventual consistency (e.g. snapshot creation).
    """

    def __init__(
        self,
        getter: Callable[[], T],
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

    def run(self) -> None:
        while True:
            try:
                self._resource = self._getter()
                self._status = "Succeeded"
                return
            except (ResourceNotFoundError, HttpResponseError) as exc:
                if isinstance(exc, ResourceNotFoundError) or getattr(exc, "status_code", None) == 404:
                    if time.monotonic() > self._deadline:
                        self._status = "Failed"
                        raise TimeoutError(
                            f"{self._resource_id} did not appear within {self._timeout}s"
                        ) from exc
                    time.sleep(self._poll_interval)
                    continue
                raise

    def status(self) -> str:
        return self._status

    def finished(self) -> bool:
        return self._status in ("Succeeded", "Failed")

    def resource(self) -> T | None:
        return self._resource


__all__ = ["ResourceStatePoller", "DeletionPoller", "ResourceExistsPoller"]
