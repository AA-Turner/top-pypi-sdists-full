"""The execution-scoped resource container."""

import asyncio
from dataclasses import dataclass

from mistralai.vibe.sdk.agent.execution.resources.errors import (
    ResourceKeyConflictError,
    ResourceSharingConflictError,
    ScopeClosedError,
)
from mistralai.vibe.sdk.agent.execution.resources.types import (
    SHARED,
    AcquiredResource,
    CompatibilityMetadata,
    Finalizer,
    ResourceBinding,
    ResourceDefinition,
    ResourceSharing,
)


@dataclass
class InFlightAcquisition:
    """A shared, still-running acquisition for one resource key."""

    task: asyncio.Task[AcquiredResource[object]]
    compatibility: CompatibilityMetadata
    sharing: ResourceSharing


class ResourcesScope:
    """Owns the resources acquired for one unit of execution."""

    def __init__(self) -> None:
        self._parent: ResourcesScope | None = None
        self._children: set[ResourcesScope] = set()
        self._bindings: dict[str, ResourceBinding[object]] = {}
        self._in_flight: dict[str, InFlightAcquisition] = {}
        self._finalization_errors: list[Exception] = []
        self._closed = False
        self._close_task: asyncio.Task[None] | None = None

    def child_scope(self) -> "ResourcesScope":
        """Create a tracked child scope, rejecting new children once closing."""
        if self._closed:
            raise ScopeClosedError()

        child = ResourcesScope()
        child._parent = self
        self._children.add(child)

        return child

    async def get[T](self, definition: ResourceDefinition[T]) -> T:
        """Return the scope's resource for ``definition``, acquiring on first use."""
        key = definition.key
        requested = definition.compatibility

        if self._closed:
            raise ScopeClosedError(key=key)

        cached = self._bindings.get(key)
        if cached is not None:
            if cached.sharing != definition.sharing:
                raise ResourceSharingConflictError(
                    key=key, existing=cached.sharing, requested=definition.sharing
                )
            if dict(cached.compatibility) != dict(requested):
                raise ResourceKeyConflictError(
                    key=key, existing=cached.compatibility, requested=requested
                )
            return cached.value  # type: ignore[return-value]

        in_flight = self._in_flight.get(key)
        if in_flight is not None:
            if in_flight.sharing != definition.sharing:
                raise ResourceSharingConflictError(
                    key=key, existing=in_flight.sharing, requested=definition.sharing
                )
            if dict(in_flight.compatibility) != dict(requested):
                raise ResourceKeyConflictError(
                    key=key, existing=in_flight.compatibility, requested=requested
                )
        else:
            in_flight = self._begin_acquisition(definition)

        # Shield the shared task from this waiter's cancellation: cancelling one
        # waiter must not cancel an acquisition other waiters still need.
        await asyncio.shield(in_flight.task)

        # The acquisition finished. If close raced it, the resource was finalized
        # rather than cached, so refuse to hand it out.
        if self._closed:
            raise ScopeClosedError(key=key)

        resolved = self._bindings.get(key)
        if resolved is None:
            # Reaching here means that we closed in between so raising here.
            raise ScopeClosedError(key=key)

        return resolved.value  # type: ignore[return-value]

    def _begin_acquisition[T](self, definition: ResourceDefinition[T]) -> InFlightAcquisition:
        compatibility = dict(definition.compatibility)
        task: asyncio.Task[AcquiredResource[object]] = asyncio.ensure_future(
            self._acquire_and_cache(definition, compatibility)
        )
        # Retrieve a failed task's exception even if every waiter is cancelled,
        # so asyncio does not log "Task exception was never retrieved".
        task.add_done_callback(lambda t: None if t.cancelled() else t.exception())
        in_flight = InFlightAcquisition(
            task=task, compatibility=compatibility, sharing=definition.sharing
        )
        self._in_flight[definition.key] = in_flight

        return in_flight

    async def _acquire_and_cache[T](
        self, definition: ResourceDefinition[T], compatibility: CompatibilityMetadata
    ) -> AcquiredResource[object]:
        key = definition.key
        parent = self._parent
        try:
            if definition.sharing == SHARED and parent is not None:
                acquired: AcquiredResource[object] = AcquiredResource(
                    value=await parent.get(definition)
                )
                delegated = True
            else:
                acquired = await definition.acquire(self)
                delegated = False
        except BaseException:
            # Do not cache failed acquisitions; a later get() may retry.
            self._in_flight.pop(key, None)
            raise

        # No await between acquisition and caching/finalization below: close and
        # this acquisition cannot interleave into a leak or a double-finalize.
        if self._closed:
            if acquired.finalizer is not None:
                await self._finalize(acquired.finalizer)

            self._in_flight.pop(key, None)
            raise ScopeClosedError(key=key)

        self._bindings[key] = ResourceBinding(
            key=key,
            compatibility=compatibility,
            sharing=definition.sharing,
            value=acquired.value,
            finalizer=acquired.finalizer,
            owned=not delegated,
        )
        self._in_flight.pop(key, None)

        return acquired

    async def aclose(self) -> None:
        """Finalize owned resources in reverse acquisition order, idempotently."""
        self._mark_subtree_closing()
        if self._close_task is None:
            self._close_task = asyncio.ensure_future(self._do_close())

        # Shield so a cancelled aclose() caller does not abort the shared close.
        await asyncio.shield(self._close_task)

    def _mark_subtree_closing(self) -> None:
        """Flag this scope and every descendant closed synchronously, before any
        await. Otherwise a descendant stays open across the parent's teardown
        window and a racing get() could hand out a shared resource the parent
        is about to finalize.
        """
        self._closed = True
        for child in self._children:
            child._mark_subtree_closing()

    async def _do_close(self) -> None:
        # Close children before our own finalizers: a child may hold a non-owned
        # reference to one of our shared resources and must release it first.
        if self._children:
            results = await asyncio.gather(
                *(child.aclose() for child in list(self._children)),
                return_exceptions=True,
            )
            self._children.clear()
            for result in results:
                if isinstance(result, Exception):
                    self._finalization_errors.append(result)

        if self._in_flight:
            await asyncio.gather(
                *(p.task for p in self._in_flight.values()), return_exceptions=True
            )

        for key in reversed(list(self._bindings)):
            binding = self._bindings[key]
            if binding.owned and binding.finalizer is not None:
                await self._finalize(binding.finalizer)

        self._bindings.clear()

        # Unregister from the parent so a later parent close does not re-await or
        # re-surface this scope (relevant when a child is closed on its own).
        if self._parent is not None:
            self._parent._children.discard(self)
            self._parent = None

        if self._finalization_errors:
            raise ExceptionGroup("resource finalization failed", self._finalization_errors)

    async def _finalize(self, finalizer: Finalizer) -> None:
        """Run one finalizer, recording (not raising) any Exception for aclose()."""
        try:
            await finalizer()
        except Exception as exc:
            self._finalization_errors.append(exc)


__all__ = ["ResourcesScope"]
