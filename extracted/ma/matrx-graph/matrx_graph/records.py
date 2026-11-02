"""Platform Record reading for graph nodes — the host injection seam.

A workflow frequently needs to READ one platform Record: the
``workbench.google_document`` row a Drive sync wrote, the
``communication.calendar_event`` a meeting produced, a ``crm.party``. Until
this seam existed there was no door at all: ``admin.sql.*`` is admin-only and
RLS-bypassing, and every feature that wanted one row grew its own reader node.

THE THREE THINGS A READ NEEDS, and why none of them live here
-------------------------------------------------------------
1. **Which table is this entity type?** ``platform.entity_types`` is THE noun
   registry (one row per entity, carrying schema/table/label). The host owns
   that registry and the ``(schema, table) -> generated Model`` resolution.
   **Never a hand-written dict in this package** — a mapping maintained here
   drifts away from the database the moment a table is registered or moved.
2. **May this actor read this row?** Exactly one answer exists:
   ``iam.has_access_for`` (owner, explicit permission, org membership, parent
   conveyance, super-admin), reached through
   ``matrx_orm.platform_access_check``. NEVER ``organization_id ==`` and NEVER
   ``created_by ==`` — organization is TENANCY, never permission.
3. **The row itself** — read through matrx-orm, soft-delete aware.

All three are host capabilities, so they arrive as ONE injected gateway, the
same shape ``configure_reference_resolver`` established: the engine stays
importable on a bare Postgres with nothing wired, and this package never
imports host code. Unconfigured, :func:`get_record_gateway` returns ``None``
and the node REFUSES BY NAME with the wiring remedy — never an empty success.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any, Protocol, runtime_checkable

__all__ = [
    "RecordEntity",
    "PlatformRecordGateway",
    "RecordReadRefused",
    "configure_record_gateway",
    "get_record_gateway",
    "is_record_gateway_configured",
]


@dataclass(frozen=True, slots=True)
class RecordEntity:
    """One ``platform.entity_types`` row, as this package needs it.

    ``entity_type`` is the registry TOKEN (``google_document``), which is also
    the token ``iam.has_access_for`` is asked about — the same word end to end,
    never translated on the way.
    """

    entity_type: str
    schema_name: str
    table_name: str
    label: str = ""
    #: The column the registry declares as this entity's human title, when it
    #: names one. Registry-driven, so a node never guesses a table's name column.
    title_column: str = ""
    #: Columns the registry marks as not-for-clients. A reader HIDES them and
    #: SAYS it hid them — never silently, never leaked.
    excluded_columns: tuple[str, ...] = ()

    @property
    def qualified_table(self) -> str:
        return f"{self.schema_name}.{self.table_name}"


@runtime_checkable
class PlatformRecordGateway(Protocol):
    """What the host supplies so a graph node can read ONE platform Record.

    Every method is async: a real implementation talks to Postgres through
    matrx-orm. Implementations RESOLVE, they never decide — the node owns the
    refusals, so a miss is returned as ``None``/``False``, never raised and
    never softened into an empty row.
    """

    async def describe_entity(self, entity_type: str) -> RecordEntity | None:
        """The registry row for ``entity_type``, or None when it is unknown."""

    async def known_entity_types(self) -> Sequence[str]:
        """Every readable entity-type token, for the unknown-type refusal."""

    async def may_read(
        self, *, actor_id: str, entity_type: str, record_id: str
    ) -> bool:
        """``iam.has_access_for(actor, token, id, 'viewer')``. Fails CLOSED."""

    async def read_row(
        self, *, entity: RecordEntity, record_id: str
    ) -> Mapping[str, Any] | None:
        """The live row as a JSON-safe mapping, or None when absent/deleted."""


class RecordReadRefused(Exception):
    """The host names why an entity type has no door to read by id — said by name, not "not found".

    A gateway raises this from ``read_row`` when the type lives somewhere the gateway cannot open
    (e.g. a record-store noun with no store door). The node turns ``reason`` into the refusal a
    person reads; it is never a missing record and never a log-only defect.
    """

    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason = reason


_gateway: PlatformRecordGateway | None = None


def configure_record_gateway(gateway: PlatformRecordGateway | None) -> None:
    """Register (or clear) the host's platform-Record gateway.

    Called once at app startup beside the other package ``configure_*`` calls.
    Passing None clears it (tests, and a deliberately DB-free standalone graph).
    """
    global _gateway
    _gateway = gateway


def is_record_gateway_configured() -> bool:
    return _gateway is not None


def get_record_gateway() -> PlatformRecordGateway | None:
    return _gateway
