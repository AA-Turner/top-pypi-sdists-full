"""Receptions (`recepciones`): the port every reception store implements.

A reception is its own aggregate: ONE document per company (a unique index on `company_id` among the live ones),
which holds the base reception (the default WhatsApp account's) and, in `account_receptions.<account_id>`, the block
of every other account. The entity is `letschatty.models.company.assets.recepcion.Recepcion`, unchanged.

It is not a simple catalog (ADR-010 of api-chatty): it is read by company (the runtime reads it on every incoming
message), never by id, and it has no delete. A block of one account is written with a dotted `$set`, which neither
overwrites the base nor another account (`set_account_block`); the whole-document `update` never carries the blocks.
Pausing or resuming accounts writes only the absence of each one (`set_absence`). Changing the default account moves
blocks between the base and an account in ONE write (`swap_default_block`). The port speaks of accounts, block field
names (`BLOCK_FIELDS`) and models: only the Mongo adapter knows the dotted paths (`account_receptions.<id>.<field>`,
`ausencia.activa`), the update operators and how a value is stored (an `Ausencia` as JSON, a date as ISO text).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Protocol, Sequence, Union

from ...models.company.assets.recepcion import Ausencia, Recepcion
from ...models.utils.types import StrObjectId

# The fields of an account's block (`account_receptions.<id>`): the only names `set_account_block` takes.
BLOCK_FIELDS = ("bienvenida_fast_answer_id", "ausencia", "atencion_estado")
# The fields of `ausencia` a pause or a resume overwrites (`set_absence` with a dict).
ABSENCE_FLAGS = ("activa", "activa_hasta")


@dataclass(frozen=True)
class StoredBlocks:
    """The blocks of the company's stored reception, as stored (read from the store, not the cache).

    `reception_id` is the store's own id, opaque: only `swap_default_block` takes it back. `base` has the base's block
    fields that the document has (a field it lacks is absent, not None). `accounts` is `account_receptions` as stored:
    `{account_id: block}`."""

    reception_id: Any
    base: Dict[str, Any] = field(default_factory=dict)
    accounts: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class StoredFlowStates:
    """The attention flow's stored states of a company's live reception, read narrow (not the whole document): `base` is
    the document's own `atencion_estado` (None when it has none) and `accounts` the `atencion_estado` of each account
    block that has one. Values are as stored: the use case decides which are known states."""

    base: Optional[Any] = None
    accounts: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class FlowStateWrite:
    """What a write of the flow's state matched and changed (a count of live receptions, 0 or 1)."""

    matched: int
    modified: int


class ReceptionRepository(Protocol):
    async def list_live(self, company_id: StrObjectId) -> List[Recepcion]:
        """The company's receptions without `deleted_at`, through the cache (one when all is well)."""
        ...

    async def add(self, reception: Recepcion) -> Recepcion: ...

    async def update(self, reception_id: StrObjectId, changes: Recepcion) -> Recepcion:
        """Writes only the fields `changes` was built with, merged onto what is in the store now."""
        ...

    async def set_account_block(self, company_id: StrObjectId, reception_id: StrObjectId, account_id: str,
                                fields: Dict[str, Any]) -> None:
        """Writes `fields` of the block of `account_id` (an account that is not the default's) in ONE write: each name
        is one of `BLOCK_FIELDS`, and `ausencia` is an `Ausencia`. It also sets `updated_at`; everything else stays, the
        base and the other blocks included. Raises `ValueError` for another name (before writing) and `NotFoundError`
        when no document has that id."""
        ...

    async def set_absence(self, company_id: StrObjectId, reception_id: StrObjectId,
                          by_account: Dict[Optional[str], Union[Ausencia, Dict[str, Any]]]) -> None:
        """Pauses or resumes accounts in ONE write: `{None: …}` is the base and `{<account_id>: …}` that account's
        block. An `Ausencia` replaces the whole `ausencia` of that block; a dict overwrites only the given
        `ABSENCE_FLAGS` (`activa`, `activa_hasta`: a date is stored as its ISO text, which cintia-lambdas reads). It
        also sets `updated_at`. Raises `ValueError` for another flag (before writing) and `NotFoundError` when no
        document has that id."""
        ...

    async def stored_blocks(self, company_id: StrObjectId, fields: Sequence[str]) -> Optional[StoredBlocks]:
        """The company's live reception blocks (`fields`: the names of a block's fields) read from the store and not
        from the cache; None when the company has none."""
        ...

    async def swap_default_block(self, company_id: StrObjectId, reception_id: Any, previous_account_id: str,
                                 to_previous: Dict[str, Any], to_base: Dict[str, Any],
                                 retired_account_id: Optional[str]) -> None:
        """Changing the default account, in ONE write: `to_previous` are the fields (names relative to the block) of
        the account that stops being the default, `to_base` the base's fields the new default's block brings, and
        `retired_account_id` the block that is removed (None: none). The cache of the item and the lists is cleared
        after it: a failed clear is NOT swallowed (as in `main`)."""
        ...

    async def flow_states(self, company_id: StrObjectId, *, max_time_ms: int) -> Optional[StoredFlowStates]:
        """The company's live reception's stored flow states (`atencion_estado` of the base and of each account block),
        read from the store and not from the cache, with a time limit; None when the company has no live reception."""
        ...

    async def set_flow_state(self, company_id: StrObjectId, state: str, *, account_id: Optional[str] = None,
                             only_if_missing: bool = False) -> FlowStateWrite:
        """Writes the flow's state (`atencion_estado`) of the base, or of the block of `account_id` (an account that is not
        the default's), in ONE write on the company's live reception. `only_if_missing` writes only when the base has no
        state yet (never over a stored one). It does not touch the item cache: the model does not carry the field. It does
        not create the reception: no live reception, nothing matched."""
        ...
