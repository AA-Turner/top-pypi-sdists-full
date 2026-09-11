"""Data planes — where a workspace's data and execution live."""

from __future__ import annotations

# Python internals
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Awaitable, overload

# Current package
from dlthub_sdk._glue.base import Entity, Namespace
from dlthub_sdk._glue.context import Async, M, Sync, _Ctx
from dlthub_sdk._glue.enums import EntityKind

if TYPE_CHECKING:
    # Typing only: domain never imports _gen at runtime.
    # Current package
    from dlthub_sdk._gen.api.models import DataplaneInfo


@dataclass(frozen=True, repr=False)
class Dataplane(Entity[M]):
    """A data plane an organization can put its workspaces on.

    Attributes:
        id: What :meth:`Organization.set_dataplane` takes.
        name: Display name.
        region: Where it runs, so data residency is visible.
        description: Free-text description, or ``None``.
    """

    id: str
    name: str
    region: str
    description: str | None

    _identity = ("id", "region")
    _kind = EntityKind.DATAPLANE

    @staticmethod
    def _from_payload(ctx: _Ctx[Any], payload: DataplaneInfo) -> Dataplane[Any]:
        return Dataplane._bind(
            ctx,
            Dataplane(
                id=payload.id,
                name=payload.name,
                region=payload.region,
                description=(
                    payload.description
                    if isinstance(payload.description, str)
                    else None
                ),
            ),
        )

    @staticmethod
    def _all_from_payload(
        ctx: _Ctx[Any], payload: list[DataplaneInfo]
    ) -> tuple[Dataplane[Any], ...]:
        return tuple(Dataplane._from_payload(ctx, item) for item in payload)


class Dataplanes(Namespace[M]):
    """The data planes this caller may choose from.

    They arrive in one answer, so there is nothing to page and no count to ask
    for.
    """

    @overload
    def list(self: Dataplanes[Sync]) -> tuple[Dataplane[Sync], ...]: ...

    @overload
    def list(
        self: Dataplanes[Async],
    ) -> Awaitable[tuple[Dataplane[Async], ...]]: ...

    def list(
        self,
    ) -> tuple[Dataplane[Any], ...] | Awaitable[tuple[Dataplane[Any], ...]]:
        """Return every data plane available to this caller.

        Needs no scope, like :meth:`Organizations.list`.

        Returns:
            All of them, in the platform's order; awaitable in async mode.
        """
        return self._ctx.run(lambda t: t.list_dataplanes(), Dataplane._all_from_payload)
