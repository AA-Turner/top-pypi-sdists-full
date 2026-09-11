"""The root namespace, reached from `connect` / `connect_async`."""

from __future__ import annotations

# Python internals
from typing import Any, Awaitable, cast, overload

# Current package
from dlthub_sdk._glue.base import Namespace
from dlthub_sdk._glue.context import Async, M, Sync
from dlthub_sdk.domain.caller import Caller
from dlthub_sdk.domain.dataplanes import Dataplanes
from dlthub_sdk.domain.organizations import Organizations
from dlthub_sdk.domain.workspaces import Workspaces


class Runtime(Namespace[M]):
    """Entry point to the platform.

    Build one with :func:`~dlthub_sdk.connect` or
    :func:`~dlthub_sdk.connect_async`; ``M`` records which, so every object
    reached from it stays in the same mode.

    Usable as a context manager, which closes it on the way out::

        with dlthub_sdk.connect(token="...") as runtime:
            ...
    """

    @property
    def organizations(self) -> Organizations[M]:
        """Organization lookup.

        Returns:
            Every organization the caller belongs to.
        """
        return Organizations(self._ctx)

    @property
    def dataplanes(self) -> Dataplanes[M]:
        """The data planes a workspace can be placed on.

        Returns:
            Every one this caller may choose from, needing no scope.
        """
        return Dataplanes(self._ctx)

    @property
    def workspaces(self) -> Workspaces[M]:
        """Workspace lookup.

        Returns:
            A collection scoped to the organization given at connect time.
        """
        return Workspaces(self._ctx)

    @overload
    def me(self: Runtime[Sync]) -> Caller[Sync]: ...

    @overload
    def me(self: Runtime[Async]) -> Awaitable[Caller[Async]]: ...

    def me(self) -> Caller[Any] | Awaitable[Caller[Any]]:
        """Return the human this token belongs to.

        **Only a user token can call this.** The platform gates ``/user`` to
        human principals, so an API key is refused however broad its grants.
        Reading the API key's own identity is what :meth:`Organization.me` and
        :meth:`Workspace.me` are for — both answer for any principal, and both
        are scoped rather than account-wide.

        Calling it also settles the caller's default organization, so a first
        call on a new account is not side-effect free.

        Returns:
            The caller, with every organization they belong to; awaitable in
            async mode.

        Raises:
            NotAuthorized: The token is not a user token.
            NotAuthenticated: The token is missing, malformed, or rejected.
        """
        return self._ctx.run(lambda t: t.get_current_user(), Caller._from_payload)

    @overload
    def close(self: Runtime[Sync]) -> None: ...

    @overload
    def close(self: Runtime[Async]) -> Awaitable[None]: ...

    def close(self) -> Any:
        """Release the connections held for this client.

        Anything reached from it — a workspace, a job, a collection — shares
        those connections, so close only when done with all of them. Calling
        the platform through a closed client raises.

        Returns:
            ``None``; awaitable in async mode.
        """
        return self._ctx.close()

    def __enter__(self: Runtime[Sync]) -> Runtime[Sync]:
        return self

    def __exit__(self, *exc: object) -> None:
        # An async runtime would hand back an un-awaited coroutine; only the
        # __enter__ annotation stops one getting here, and that is typing only.
        if self._ctx.is_async:
            raise TypeError(
                "an async runtime closes with 'async with', not 'with'; "
                "await close() instead"
            )
        self._ctx.close()

    async def __aenter__(self: Runtime[Async]) -> Runtime[Async]:
        return self

    async def __aexit__(self, *exc: object) -> None:
        await cast("Awaitable[None]", self._ctx.close())
