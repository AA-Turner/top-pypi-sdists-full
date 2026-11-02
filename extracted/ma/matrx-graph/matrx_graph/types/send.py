from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict

from matrx_graph.types.channel import coerce_to_json


class Send(BaseModel):
    """Dynamic fanout directive.

    A node emits Send(target_node_id, payload) via `ctx.send(...)` during
    execute(). The scheduler processes all sends at the end of the current
    super-step, creating a new invocation of `target_node_id` in the next
    super-step with `payload` as its inputs. Each Send produces a distinct
    invocation (with its own attempt number), so many Sends to the same
    target fan out in parallel instead of aggregating.

    Lives in `types/` — NOT `executor/` — because both the executor and the
    checkpointer (in `NodeOutcome`) need to reference it. Keeping it in the
    lower layer avoids a circular import.

    Correlation identity (ENGINE_SPEC §4.1): ``dispatch_id`` is minted ONCE
    per dispatching invocation (by ``NodeExecutionContext.send``) and
    ``item_index`` is the send's position within that dispatch. Both persist
    inside the dispatcher's recorded ``NodeOutcome.sends``, so crash-replay
    reuses the SAME identity — byte-identical routing. Defaults ``''``/``0``
    keep historical rows correct.
    """

    model_config = ConfigDict(frozen=True)

    target_node_id: str
    payload: dict[str, Any] = {}
    dispatch_id: str = ""
    item_index: int = 0
    # Durable work-set correlation (matrx_graph.workset): when the dispatching
    # node claimed this payload from a run work set, the claimed item's id
    # rides the Send so the scheduler can settle the item (complete/fail) at
    # outcome-record time. ''/absent = ordinary Send. Persists inside
    # NodeOutcome.sends like the rest of the identity — replay settles
    # idempotently.
    work_item_id: str = ""

    @classmethod
    def create(
        cls,
        target_node_id: str,
        payload: dict[str, Any] | BaseModel | None = None,
        *,
        dispatch_id: str = "",
        item_index: int = 0,
        work_item_id: str = "",
    ) -> Send:
        if payload is None:
            payload_dict: dict[str, Any] = {}
        elif isinstance(payload, BaseModel):
            payload_dict = payload.model_dump(mode="json")
        else:
            payload_dict = coerce_to_json(payload)
        return cls(
            target_node_id=target_node_id,
            payload=payload_dict,
            dispatch_id=dispatch_id,
            item_index=item_index,
            work_item_id=work_item_id,
        )
