"""The context threaded through every entity and collection.

The only mode-aware code in the SDK: ``run``, ``count``, ``page``, ``stream`` and
``poll`` return a value, a coroutine or an async iterable depending on the
transport, so a domain method has one body for both modes.
"""

from __future__ import annotations

# Python internals
import asyncio
import time
from dataclasses import dataclass, replace
from functools import cached_property
from typing import (
    TYPE_CHECKING,
    Any,
    AsyncIterable,
    AsyncIterator,
    Awaitable,
    Callable,
    Generic,
    Iterable,
    Iterator,
    Literal,
    Protocol,
    Sequence,
    TypeVar,
    cast,
)

# Current package
from dlthub_sdk._glue.enums import EntityKind
from dlthub_sdk._glue.urls import DEFAULT_BASE_URL
from dlthub_sdk.errors import ScopeMissing, WaitTimeout

if TYPE_CHECKING:
    # Typing only: importing the transport here would pull every generated
    # operation it wraps into `import dlthub_sdk`.
    # Current package
    from dlthub_sdk._gen.api.types import Unset
    from dlthub_sdk._glue.transport import AnyTransport, AsyncTransport, Transport

#: Which flavour of transport a context holds. Fixed by ``connect``/``connect_async``.
Sync = Literal["sync"]
Async = Literal["async"]

M = TypeVar("M", Sync, Async)
R = TypeVar("R")
P = TypeVar("P")
P_co = TypeVar("P_co", covariant=True)

PAGE_SIZE = 100

#: The platform caps a count here, so a count equal to it means "at least this
#: many", not exactly this many.
COUNT_CEILING = 10_001

#: How a poll backs off. A run may finish in seconds or take hours, so the first
#: few checks are quick and the interval then grows to a ceiling — a short run is
#: noticed almost at once without a long one costing thousands of requests.
POLL_FIRST_DELAY = 1.0
POLL_GROWTH = 1.5
POLL_MAX_DELAY = 10.0


#: One page of rows, given a transport, a limit and an offset. A collection
#: declares this once and both ``count`` and ``page`` consume it.
Listing = Callable[["AnyTransport", int, int], "_PageOf[P] | Awaitable[_PageOf[P]]"]


def _total(_ctx: _Ctx[Any], page: _PageOf[object]) -> int:
    # Shaped like a parse so `run` can drive it; the context goes unused.
    return int(page.total or 0)


@dataclass
class _Cursor:
    """How far a walk has got, so both modes share the arithmetic.

    Attributes:
        at: The next row to ask the server for.
        remaining: Rows the caller still wants, or ``None`` for all of them.
    """

    at: int
    remaining: int | None

    @property
    def wants_more(self) -> bool:
        """Whether another page is worth fetching.

        Returns:
            False once the caller's limit is satisfied, so ``limit=0`` fetches
            nothing at all.
        """
        return self.remaining is None or self.remaining > 0

    @property
    def take(self) -> int:
        """How many rows to ask for next.

        Returns:
            A full page, or only what is left of the limit.
        """
        return PAGE_SIZE if self.remaining is None else min(PAGE_SIZE, self.remaining)

    def advance(self, rows: int, total: int) -> bool:
        """Account for a page just yielded.

        Args:
            rows: How many rows it held.
            total: How many rows the server says match.

        Returns:
            True when the walk is over — an empty page ends it, so a server that
            keeps reporting more than it returns cannot loop forever.
        """
        self.at += rows
        if self.remaining is not None:
            self.remaining -= rows
        if not rows:
            return True
        # A saturated total is a ceiling rather than a count, so it cannot say
        # where the rows end; only an empty page can.
        return total < COUNT_CEILING and self.at >= total


@dataclass
class _Backoff:
    """When to poll next, so both modes share the arithmetic.

    Attributes:
        deadline: Monotonic time the caller's patience runs out, or ``None``.
        delay: What the next sleep will be, before the deadline clamps it.
    """

    deadline: float | None
    delay: float

    @property
    def expired(self) -> bool:
        """Whether the deadline has passed.

        Returns:
            True once there is no point asking again.
        """
        return self.deadline is not None and time.monotonic() >= self.deadline

    def sleep_for(self) -> float:
        """Take the next sleep and grow the one after it.

        Returns:
            Seconds to wait, never past the deadline — so a timeout is not
            overshot by most of an interval.
        """
        wait = self.delay
        self.delay = min(self.delay * POLL_GROWTH, POLL_MAX_DELAY)
        if self.deadline is None:
            return wait
        return max(0.0, min(wait, self.deadline - time.monotonic()))


class _PageOf(Protocol[P_co]):
    """One page of a generated list response, whatever it lists."""

    @property
    def items(self) -> Sequence[P_co] | Unset:
        """The rows on this page."""

    @property
    def total(self) -> int | Unset:
        """How many rows match, capped at :data:`COUNT_CEILING`."""


@dataclass(frozen=True, repr=False)
class _Ctx(Generic[M]):
    """Transport plus the scope resolved so far.

    :meth:`narrow` copies the scope and keeps the transport, so navigating never
    rebuilds a client.
    """

    transport: AnyTransport
    base_url: str = DEFAULT_BASE_URL
    organization_id: str | None = None
    workspace_id: str | None = None
    dataplane_url: str | None = None
    job_id: str | None = None

    @cached_property
    def is_async(self) -> bool:
        """Whether this context's transport awaits.

        Read off the lifecycle method, which is the only name the two protocols
        spell differently, so renaming an operation cannot break detection.

        Returns:
            True for an async transport.
        """
        return hasattr(self.transport, "aclose")

    def narrow(
        self,
        *,
        organization_id: str | None = None,
        workspace_id: str | None = None,
        dataplane_url: str | None = None,
        job_id: str | None = None,
    ) -> _Ctx[M]:
        """Return a context with the given scope applied on top of this one.

        Omitted values are inherited. Scope only ever widens: passing ``None``
        inherits rather than clears.

        Args:
            organization_id: Organization to scope to, if any.
            workspace_id: Workspace to scope to, if any.
            dataplane_url: Data plane the workspace lives on, if known.
            job_id: Job to scope to, if any.

        Returns:
            A narrowed context sharing this one's transport.
        """
        return replace(
            self,
            organization_id=(
                self.organization_id if organization_id is None else organization_id
            ),
            workspace_id=self.workspace_id if workspace_id is None else workspace_id,
            dataplane_url=(
                self.dataplane_url if dataplane_url is None else dataplane_url
            ),
            job_id=self.job_id if job_id is None else job_id,
        )

    def run(
        self,
        call: Callable[[AnyTransport], P | Awaitable[P]],
        parse: Callable[[_Ctx[Any], P], R],
    ) -> R | Awaitable[R]:
        """Perform one transport call and parse its payload.

        Args:
            call: Receives the transport, returns its payload (or an awaitable).
            parse: An entity's ``_from_payload``, which this context is passed to.

        Returns:
            The domain object, or a coroutine yielding it when async.
        """
        if self.is_async:

            async def _awaited() -> R:
                payload = await cast("Awaitable[P]", call(self.transport))
                return parse(self, payload)

            return _awaited()
        return parse(self, cast("P", call(self.transport)))

    def count(self, listing: Listing[object]) -> int | Awaitable[int]:
        """Ask how many rows a listing would yield, without fetching them.

        Args:
            listing: The collection's listing, as passed to :meth:`page`.

        Returns:
            The row count, or a coroutine yielding it when async. Saturates at
            :data:`COUNT_CEILING`.
        """
        # One row, because only the page's `total` is read.
        return self.run(lambda t: listing(t, 1, 0), _total)

    def page(
        self,
        listing: Listing[P],
        parse: Callable[[_Ctx[Any], P], R],
        *,
        limit: int | None = None,
        offset: int = 0,
    ) -> Iterable[R] | AsyncIterable[R]:
        """Walk limit/offset pages lazily, parsing each row as it is yielded.

        Args:
            listing: The collection's listing.
            parse: An entity's ``_from_payload``, which this context is passed to.
            limit: Stop after this many rows. ``None`` walks to the end.
            offset: Skip this many rows, server-side.

        Returns:
            An ``Iterable`` of entities, or an ``AsyncIterable`` when async.

        Raises:
            ValueError: ``limit`` or ``offset`` is negative.
        """
        # Validated out here, not in the generators: a generator body would not
        # run until the caller started iterating.
        if limit is not None and limit < 0:
            raise ValueError(f"limit must not be negative, got {limit}")
        if offset < 0:
            raise ValueError(f"offset must not be negative, got {offset}")
        if self.is_async:
            return self._awalk(listing, parse, _Cursor(offset, limit))
        return self._walk(listing, parse, _Cursor(offset, limit))

    def _take_page(
        self,
        page: _PageOf[P],
        parse: Callable[[_Ctx[Any], P], R],
        cursor: _Cursor,
    ) -> tuple[list[R], bool]:
        """Parse one page and account for it, so both walks share the arithmetic.

        Args:
            page: What the listing returned.
            parse: An entity's ``_from_payload``, which this context is passed to.
            cursor: Advanced by the number of rows the page held.

        Returns:
            The page's entities, and whether the walk is over.
        """
        rows = list(page.items or [])
        parsed = [parse(self, row) for row in rows]
        return parsed, cursor.advance(len(rows), int(page.total or 0))

    def _walk(
        self,
        listing: Listing[P],
        parse: Callable[[_Ctx[Any], P], R],
        cursor: _Cursor,
    ) -> Iterator[R]:
        while cursor.wants_more:
            page = cast("_PageOf[P]", listing(self.transport, cursor.take, cursor.at))
            parsed, done = self._take_page(page, parse, cursor)
            yield from parsed
            if done:
                return

    async def _awalk(
        self,
        listing: Listing[P],
        parse: Callable[[_Ctx[Any], P], R],
        cursor: _Cursor,
    ) -> AsyncIterator[R]:
        while cursor.wants_more:
            page = await cast(
                "Awaitable[_PageOf[P]]",
                listing(self.transport, cursor.take, cursor.at),
            )
            parsed, done = self._take_page(page, parse, cursor)
            for row in parsed:
                yield row
            if done:
                return

    def stream(
        self,
        open_: Callable[[AnyTransport], Iterator[P] | AsyncIterator[P]],
        parse: Callable[[_Ctx[Any], P], R],
    ) -> Iterable[R] | AsyncIterable[R]:
        """Walk an open response body lazily, parsing each row as it arrives.

        Unlike :meth:`page` there is no cursor: the server decides when the body
        ends, so nothing is asked for twice.

        Args:
            open_: Opens the stream on the transport and yields its rows.
            parse: An entity's ``_from_payload``, which this context is passed to.

        Returns:
            An ``Iterable`` of entities, or an ``AsyncIterable`` when async.
        """
        if self.is_async:
            return self._aflow(open_, parse)
        return self._flow(open_, parse)

    def _flow(
        self,
        open_: Callable[[AnyTransport], Iterator[P] | AsyncIterator[P]],
        parse: Callable[[_Ctx[Any], P], R],
    ) -> Iterator[R]:
        for row in cast("Iterator[P]", open_(self.transport)):
            yield parse(self, row)

    async def _aflow(
        self,
        open_: Callable[[AnyTransport], Iterator[P] | AsyncIterator[P]],
        parse: Callable[[_Ctx[Any], P], R],
    ) -> AsyncIterator[R]:
        async for row in cast("AsyncIterator[P]", open_(self.transport)):
            yield parse(self, row)

    def poll(
        self,
        call: Callable[[AnyTransport], P | Awaitable[P]],
        parse: Callable[[_Ctx[Any], P], R],
        settled: Callable[[R], bool],
        *,
        timeout: float | None,
        subject: str,
    ) -> R | Awaitable[R]:
        """Read something repeatedly until it settles.

        Always reads once before sleeping, so the answer is fresh even when the
        caller already knew it had settled.

        Args:
            call: Receives the transport, returns its payload (or an awaitable).
            parse: An entity's ``_from_payload``, which this context is passed to.
            settled: Whether a parsed value is the final one.
            timeout: Give up after this many seconds. ``None`` waits indefinitely.
            subject: What is being waited on, for the timeout message.

        Returns:
            The settled value, or a coroutine yielding it when async.

        Raises:
            WaitTimeout: The deadline passed while it was still unsettled.
            ValueError: ``timeout`` is negative.
        """
        # Validated out here, not in the coroutine, which would not run until awaited.
        if timeout is not None and timeout < 0:
            raise ValueError(f"timeout must not be negative, got {timeout}")
        backoff = _Backoff(
            None if timeout is None else time.monotonic() + timeout, POLL_FIRST_DELAY
        )
        if self.is_async:

            async def _awaited() -> R:
                while True:
                    value = parse(
                        self, await cast("Awaitable[P]", call(self.transport))
                    )
                    if settled(value):
                        return value
                    if backoff.expired:
                        raise WaitTimeout(f"{subject} after {timeout}s")
                    await asyncio.sleep(backoff.sleep_for())

            return _awaited()
        while True:
            value = parse(self, cast("P", call(self.transport)))
            if settled(value):
                return value
            if backoff.expired:
                raise WaitTimeout(f"{subject} after {timeout}s")
            time.sleep(backoff.sleep_for())

    def close(self) -> None | Awaitable[None]:
        """Close the transport's connections.

        Returns:
            ``None``, or a coroutine to await when async.
        """
        if self.is_async:
            return cast("AsyncTransport", self.transport).aclose()
        cast("Transport", self.transport).close()
        return None

    def require_workspace(self) -> str:
        """Return the workspace in scope.

        Returns:
            The workspace id.

        Raises:
            ScopeMissing: No workspace in scope.
        """
        if self.workspace_id is None:
            raise ScopeMissing("no workspace in scope; reach this through a workspace")
        return self.workspace_id

    def require_dataplane(self) -> str:
        """Return the data plane URL of the workspace in scope.

        Returns:
            The data plane's base URL.

        Raises:
            ScopeMissing: No workspace in scope, so no data plane is known.
        """
        if self.dataplane_url is None:
            raise ScopeMissing("no data plane in scope; reach this through a workspace")
        return self.dataplane_url

    def require_organization(self) -> str:
        """Return the organization in scope.

        Returns:
            The organization id.

        Raises:
            ScopeMissing: No organization in scope.
        """
        if self.organization_id is None:
            raise ScopeMissing("no organization in scope; pass organization_id")
        return self.organization_id

    def scope_repr(self) -> str:
        """Render the scope set so far.

        Returns:
            Space-separated ``kind=value`` pairs. Never includes the transport.
        """
        return " ".join(
            f"{label}={value!r}"
            for label, value in (
                (EntityKind.ORGANIZATION, self.organization_id),
                (EntityKind.WORKSPACE, self.workspace_id),
                (EntityKind.JOB, self.job_id),
            )
            if value is not None
        )

    def __repr__(self) -> str:
        scope = self.scope_repr()
        mode = "async" if self.is_async else "sync"
        return f"<_Ctx {mode} {scope}>" if scope else f"<_Ctx {mode} unscoped>"
