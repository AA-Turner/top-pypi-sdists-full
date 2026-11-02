"""Kind-triggered nodes — the node that is wired to nothing, on purpose.

Plan of record §7.7c (ratified 2026-08-20):

    "A node sits off to the side, connected to nothing, declaring: run when
    this kind is generated… all of a particular kind, wherever they're
    generated from, doesn't matter what node, where, and doesn't matter how
    deeply nested they are."

This module owns only the DECLARATION — how an author says it and how the
engine reads it. Matching lives in ``subscriptions`` (shared with directive
kinds); firing lives in the scheduler.

AUTHORING SHAPE (on ``NodeDef.data``)
-------------------------------------
    "trigger_kind": "study_card"   # fire when this kind appears, anywhere
    "trigger_mode": "each"         # per instance, or "all" (the default)
    "trigger_fire_once": true      # at most once per run  (default false)
    "trigger_debounce_steps": 2    # coalesce over N super-steps (default 0)
    "trigger_item_key": "value"    # the argument the instances arrive under

THE TRAP THIS EXISTS TO CLOSE
-----------------------------
Compilation derives entry nodes as "every node with no incoming edges". A
trigger node has no incoming edges BY DESIGN — so without this declaration it
would be an entry node and fire immediately, on nothing, at step 1: precisely
the opposite of "run when the kind appears". ``compile`` therefore excludes
trigger nodes from derived entry nodes, and this is the function that tells it
which nodes those are. That is why the declaration must be readable without a
registry, without a database, and without running anything.

A trigger node with an INBOUND EDGE is a contradiction and is refused by
validation, not silently reconciled: the two mechanisms would each try to open
its firing and the author would have no way to tell which one did.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from matrx_graph.content_ir.edge_routing import DEFAULT_ITEM_KEY
from matrx_graph.content_ir.subscriptions import KindSubscription

__all__ = ["NodeTrigger", "parse_node_trigger", "TriggerDeclarationError"]


class TriggerDeclarationError(ValueError):
    """A malformed trigger declaration on a node (compile-time, loud)."""


class NodeTrigger(BaseModel):
    """One node's declared kind trigger, normalized."""

    model_config = ConfigDict(frozen=True)

    kind: str
    mode: Literal["all", "each"] = "all"
    fire_once: bool = False
    debounce_steps: int = Field(default=0, ge=0)
    item_key: str = DEFAULT_ITEM_KEY

    def subscription(self, node_id: str) -> KindSubscription:
        """The purpose-blind subscription this trigger registers."""
        return KindSubscription(
            subscriber_id=node_id,
            kind=self.kind,
            mode=self.mode,
            fire_once=self.fire_once,
            debounce_steps=self.debounce_steps,
            purpose="node_trigger",
        )


def parse_node_trigger(data: dict[str, Any] | None) -> NodeTrigger | None:
    """Read the trigger keys off a ``NodeDef.data`` payload.

    ``None`` when the node declares no trigger (the overwhelming majority).
    Loud on a malformed declaration — a node that silently failed to become a
    trigger would sit on the canvas doing nothing, and "it never fired" is the
    hardest possible thing to debug.
    """
    data = data or {}
    raw_kind = data.get("trigger_kind")
    if raw_kind is None:
        return None
    if not isinstance(raw_kind, str) or not raw_kind.strip():
        raise TriggerDeclarationError(
            f"trigger_kind must be a non-empty kind slug string, got {raw_kind!r}."
        )

    raw_mode = data.get("trigger_mode")
    if raw_mode is None:
        mode: Literal["all", "each"] = "all"
    elif raw_mode in ("all", "each"):
        mode = raw_mode
    else:
        raise TriggerDeclarationError(
            f"trigger_mode must be 'all' (one firing carrying every instance, "
            f"the default) or 'each' (one firing per instance), got {raw_mode!r}."
        )

    raw_once = data.get("trigger_fire_once", False)
    if not isinstance(raw_once, bool):
        raise TriggerDeclarationError(f"trigger_fire_once must be true or false, got {raw_once!r}.")

    raw_debounce = data.get("trigger_debounce_steps", 0)
    if isinstance(raw_debounce, bool) or not isinstance(raw_debounce, int) or raw_debounce < 0:
        raise TriggerDeclarationError(
            f"trigger_debounce_steps must be a non-negative whole number of "
            f"super-steps, got {raw_debounce!r}. (The engine debounces in "
            "super-steps, not milliseconds, so a replay fires exactly as many "
            "times as the original run.)"
        )

    raw_key = data.get("trigger_item_key")
    if raw_key is not None and (not isinstance(raw_key, str) or not raw_key.strip()):
        raise TriggerDeclarationError(
            f"trigger_item_key must be a non-empty target-argument name, got {raw_key!r}."
        )

    return NodeTrigger(
        kind=raw_kind.strip(),
        mode=mode,
        fire_once=raw_once,
        debounce_steps=raw_debounce,
        item_key=raw_key.strip() if isinstance(raw_key, str) else DEFAULT_ITEM_KEY,
    )
