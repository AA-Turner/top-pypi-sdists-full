"""Provider-neutral Sandbox Proxy lifecycle contracts."""

from __future__ import annotations

import asyncio
import time
from collections.abc import Awaitable, Callable, Sequence
from typing import Literal, Protocol, TypeVar

from mistralai.vibe.harness.runtime.model import RuntimeModel

SANDBOX_PROXY_RENEWAL_MARGIN_SECONDS = 5 * 60

_T = TypeVar("_T")


class SandboxProxyIdentity(RuntimeModel):
    """Legacy caller identity retained for in-flight proxy activities."""

    customer_id: str
    user_id: str
    workspace_id: str
    organization_id: str


class SandboxProxyEffects(Protocol):
    async def setup(self) -> int: ...

    async def renew(self) -> int: ...


class SandboxProxyLifecycleError(RuntimeError):
    def __init__(self, *, stage: Literal["initial_setup", "renewal"], message: str) -> None:
        self.stage = stage
        super().__init__(message)


class SandboxProxyInitialSetupError(SandboxProxyLifecycleError):
    def __init__(self) -> None:
        super().__init__(
            stage="initial_setup",
            message="Sandbox Proxy initial setup failed",
        )


class SandboxProxyRenewalError(SandboxProxyLifecycleError):
    def __init__(self) -> None:
        super().__init__(
            stage="renewal",
            message="Sandbox Proxy credential renewal failed",
        )


class SandboxProxyLifecycle:
    """Coordinate proxy credentials for one sandbox."""

    def __init__(
        self,
        *,
        effects: Sequence[SandboxProxyEffects],
        delete: Callable[[], Awaitable[None]],
        now: Callable[[], int] | None = None,
        is_cancellation: Callable[[BaseException], bool] | None = None,
        preserve_error: Callable[[BaseException], bool] | None = None,
    ) -> None:
        if not effects:
            raise ValueError("Sandbox Proxy lifecycle requires at least one integration")
        self._effects = tuple(effects)
        self._delete = delete
        self._now = now or (lambda: int(time.time()))
        self._is_cancellation = is_cancellation or (lambda error: isinstance(error, asyncio.CancelledError))
        self._preserve_error = preserve_error or (lambda _error: False)
        self._lock = asyncio.Lock()
        self._setup_complete = False
        self._expiration_times: list[int | None] = [None] * len(self._effects)

    def attach_existing_sandbox(self) -> None:
        self._expiration_times = [None] * len(self._effects)
        self._setup_complete = True

    async def initialize_new_sandbox(self) -> None:
        async with self._lock:
            if self._setup_complete:
                return
            try:
                for index, effects in enumerate(self._effects):
                    self._expiration_times[index] = await effects.setup()
            except BaseException as error:
                self._reset()
                await _best_effort_delete(self._delete, is_cancellation=self._is_cancellation)
                if isinstance(error, SandboxProxyLifecycleError) or self._preserve_error(error):
                    raise
                if self._is_cancellation(error) or not isinstance(error, Exception):
                    raise
                raise SandboxProxyInitialSetupError() from None
            self._setup_complete = True

    async def before_execute(self) -> None:
        async with self._lock:
            if not self._setup_complete:
                raise SandboxProxyInitialSetupError()
            for index, effects in enumerate(self._effects):
                if not self._needs_renewal(self._expiration_times[index]):
                    continue
                try:
                    self._expiration_times[index] = await effects.renew()
                except BaseException as error:
                    if isinstance(error, SandboxProxyLifecycleError) or self._preserve_error(error):
                        raise
                    if self._is_cancellation(error) or not isinstance(error, Exception):
                        raise
                    raise SandboxProxyRenewalError() from None

    async def execute(self, operation: Callable[[], Awaitable[_T]]) -> _T:
        await self.before_execute()
        return await operation()

    def _reset(self) -> None:
        self._setup_complete = False
        self._expiration_times = [None] * len(self._effects)

    def _needs_renewal(self, expires_at: int | None) -> bool:
        return expires_at is None or expires_at - self._now() <= SANDBOX_PROXY_RENEWAL_MARGIN_SECONDS


async def _best_effort_delete(
    delete: Callable[[], Awaitable[None]],
    *,
    is_cancellation: Callable[[BaseException], bool],
) -> None:
    try:
        await delete()
    except BaseException as error:
        if is_cancellation(error) or not isinstance(error, Exception):
            raise
