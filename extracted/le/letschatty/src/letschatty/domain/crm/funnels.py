"""Funnels of a company («embudos»): the port of the aggregate and the rules of its stages.

A funnel and its stages are one aggregate: a stage does not exist without its funnel, and the rules about the order
of the stages are the funnel's. They are stored in two collections (`funnels`, `funnel_stages`) that other services
read directly, so the documents keep their shape; one repository reads and writes both. The entities are
`letschatty.models.company.CRM.funnel.Funnel` and `FunnelStage`, unchanged.

The chat in a funnel (`chat_funnels`, `chats.active_funnel`) is another module.
"""
from __future__ import annotations

from typing import Any, Dict, List, Protocol, Sequence

from ...models.company.CRM.funnel import Funnel, FunnelStage
from ...models.utils.types import StrObjectId


# Also `ValueError`, as the old code raised them: a caller outside the layers that catches `ValueError` still does.
class StageOrderRejected(ValueError):
    """An edit gives a stage an order out of range or taken by a sibling."""


class ReorderRejected(ValueError):
    """A reorder that is not every stage of the funnel exactly once."""


class StageHasChats(ValueError):
    """A stage with chats in it cannot be deleted."""


def next_stage_order(stage_previews: Sequence[Dict[str, Any]]) -> int:
    """Where a new stage goes when the request does not say: after the last one (0 in an empty funnel)."""
    if not stage_previews:
        return 0
    return max(s.get("order", 0) for s in stage_previews) + 1


def check_stage_order(stage_id: StrObjectId, new_order: int, stages: Sequence[FunnelStage]) -> None:
    """`new_order` has to be a position of the funnel (0…N-1) that no other stage holds."""
    total = len(stages)
    if new_order < 0 or new_order >= total:
        raise StageOrderRejected(f"Order must be between 0 and {total - 1} (inclusive). Got {new_order}.")
    for stage in stages:
        if stage.id != stage_id and stage.order == new_order:
            raise StageOrderRejected(
                f"Order {new_order} is already assigned to stage '{stage.name}' (ID: {stage.id}). "
                f"Each stage must have a unique order.")


def check_reorder(stage_ids: Sequence[StrObjectId], stages: Sequence[FunnelStage]) -> None:
    """A reorder lists every live stage of the funnel, each once."""
    if len(stage_ids) != len(set(stage_ids)):
        raise ReorderRejected("Duplicate stage IDs found in reorder request. Each stage can only appear once.")
    expected, provided = {stage.id for stage in stages}, set(stage_ids)
    if provided != expected:
        missing, extra = expected - provided, provided - expected
        message = "All stages in the funnel must be included in the reorder request."
        if missing:
            message += f" Missing stages: {missing}"
        if extra:
            message += f" Extra stages (not in funnel): {extra}"
        raise ReorderRejected(message)


def refuse_deleting_a_stage_with_chats(stage: FunnelStage, chats_in_stage: int) -> None:
    if chats_in_stage:
        raise StageHasChats(
            f"No se puede eliminar la etapa '{stage.name}' porque tiene {chats_in_stage} chat(s). "
            f"Mové los chats a otra etapa antes de eliminarla.")


class FunnelRepository(Protocol):
    """Gets bring a funnel or a stage by id, of any company and also deleted; a missing one raises `NotFoundError`
    (and `InvalidId` for a malformed id). Lists are the company's live ones."""

    async def get(self, funnel_id: StrObjectId) -> Funnel: ...

    async def list_previews(self, company_id: StrObjectId) -> List[Dict[str, Any]]:
        """Live funnels of the company, newest first, as JSON-ready preview dicts."""
        ...

    async def add(self, funnel: Funnel) -> Funnel: ...

    async def update(self, funnel_id: StrObjectId, changes: Funnel) -> Funnel:
        """Writes only the fields `changes` was built with, on top of what is stored now."""
        ...

    async def delete(self, funnel_id: StrObjectId) -> Funnel:
        """Marks it deleted (the document stays) and returns it as it was before."""
        ...

    async def get_stage(self, stage_id: StrObjectId) -> FunnelStage: ...

    async def list_stage_previews(self, company_id: StrObjectId) -> List[Dict[str, Any]]:
        """Live stages of every funnel of the company, newest first, as JSON-ready preview dicts."""
        ...

    async def list_stages(self, company_id: StrObjectId) -> List[FunnelStage]:
        """Live stages of every funnel of the company."""
        ...

    async def add_stage(self, stage: FunnelStage) -> FunnelStage: ...

    async def update_stage(self, stage_id: StrObjectId, changes: FunnelStage) -> FunnelStage:
        """Writes only the fields `changes` was built with, on top of what is stored now."""
        ...

    async def delete_stage(self, stage_id: StrObjectId) -> FunnelStage:
        """Marks it deleted (the document stays) and returns it as it was before."""
        ...
