from __future__ import annotations

import typing
from contextlib import aclosing

from langgraph.constants import TASKS
from langgraph.pregel import Pregel
from langgraph.types import Interrupt, StateSnapshot

from langgraph_api.feature_flags import USE_NEW_INTERRUPTS
from langgraph_api.js.base import RemoteInterrupt

if typing.TYPE_CHECKING:
    from collections.abc import AsyncIterator, Iterable

    from langchain_core.runnables.config import RunnableConfig

    from langgraph_api.schema import Checkpoint, DeprecatedInterrupt, ThreadState
    from langgraph_api.schema import Interrupt as InterruptSchema


def runnable_config_to_checkpoint(
    config: RunnableConfig | None,
) -> Checkpoint | None:
    if (
        not config
        or not config["configurable"]
        or "thread_id" not in config["configurable"]
        or not config["configurable"]["thread_id"]
        or "checkpoint_id" not in config["configurable"]
        or not config["configurable"]["checkpoint_id"]
    ):
        return None

    configurable = config["configurable"]
    checkpoint: Checkpoint = {
        "checkpoint_id": configurable["checkpoint_id"],
        "thread_id": configurable["thread_id"],
    }

    if "checkpoint_ns" in configurable:
        checkpoint["checkpoint_ns"] = configurable["checkpoint_ns"] or ""

    if "checkpoint_map" in configurable:
        checkpoint["checkpoint_map"] = configurable["checkpoint_map"]

    return checkpoint


def patch_interrupt(
    interrupt: Interrupt | RemoteInterrupt | dict,
) -> InterruptSchema | DeprecatedInterrupt:
    """Convert a langgraph interrupt (v0 or v1) to standard interrupt schema.

    In v0.4 and v0.5, interrupt_id is a property on the langgraph.types.Interrupt object,
    so we reconstruct the type in order to access the id, with compatibility for the new
    v0.6 interrupt format as well. `response_schema` is optional; older langgraph releases
    do not set it.
    """

    # This is coming from JS, which already contains the interrupt ID.
    # Stay on the safe side and pass-through the interrupt ID if it exists.
    if isinstance(interrupt, RemoteInterrupt):
        id = interrupt.raw.pop("interrupt_id", None) or interrupt.raw.pop("id", None)
        if id is None:
            return interrupt.raw
        return {"id": id, **interrupt.raw}

    if USE_NEW_INTERRUPTS:
        response_schema = (
            interrupt.get("response_schema")
            if isinstance(interrupt, dict)
            else getattr(interrupt, "response_schema", None)
        )
        interrupt = Interrupt(**interrupt) if isinstance(interrupt, dict) else interrupt

        patched: InterruptSchema = {"id": interrupt.id, "value": interrupt.value}
        if response_schema is not None:
            patched["response_schema"] = response_schema
        return patched
    else:
        if isinstance(interrupt, dict):
            # interrupt_id is a deprecated property on Interrupt and should not be used for initialization
            # id is the new field we use for identification, also not supported on init for old versions
            interrupt.pop("interrupt_id", None)
            interrupt.pop("id", None)
            interrupt = Interrupt(**interrupt)

        return {
            "id": interrupt.interrupt_id
            if hasattr(interrupt, "interrupt_id")
            else None,
            "value": interrupt.value,
            "resumable": interrupt.resumable,
            "ns": interrupt.ns,
            "when": interrupt.when,
        }


def state_snapshot_to_thread_state(state: StateSnapshot) -> ThreadState:
    return {
        "values": state.values,
        "next": state.next,
        "tasks": [
            {
                "id": t.id,
                "name": t.name,
                "path": t.path,
                "error": t.error,
                "interrupts": [patch_interrupt(i) for i in t.interrupts],
                "checkpoint": t.state["configurable"]
                if t.state is not None and not isinstance(t.state, StateSnapshot)
                else None,
                "state": state_snapshot_to_thread_state(t.state)
                if isinstance(t.state, StateSnapshot)
                else None,
                "result": getattr(t, "result", None),
            }
            for t in state.tasks
        ],
        "metadata": state.metadata,
        "created_at": state.created_at,
        "checkpoint": runnable_config_to_checkpoint(state.config),
        "parent_checkpoint": runnable_config_to_checkpoint(state.parent_config),
        "interrupts": [patch_interrupt(i) for i in getattr(state, "interrupts", [])],
        # below are deprecated
        "checkpoint_id": state.config["configurable"].get("checkpoint_id")
        if state.config
        else None,
        "parent_checkpoint_id": state.parent_config["configurable"]["checkpoint_id"]
        if state.parent_config
        else None,
    }


async def iter_state_history(
    graph: Pregel,
    config: RunnableConfig,
    *,
    limit: int,
    filter: dict[str, typing.Any] | None = None,
    before: RunnableConfig | None = None,
) -> AsyncIterator[StateSnapshot]:
    """Yield up to ``limit`` history entries, loading checkpoints in doubling pages.

    ``aget_state_history`` loads every checkpoint it was asked for before it
    yields the first. Asking for 1, 2, 4, ... checkpoints at a time means a
    caller that stops early has loaded at most about twice what it consumed.
    A non-positive ``limit`` reads the whole history, as the server's
    checkpointer does, still in pages.
    """
    remaining = limit if limit > 0 else None
    page_size = 1
    while remaining is None or remaining > 0:
        page = page_size if remaining is None else min(page_size, remaining)
        loaded = 0
        async with aclosing(
            graph.aget_state_history(config, limit=page, filter=filter, before=before)
        ) as states:
            async for state in states:
                loaded += 1
                before = state.config
                yield state
                # Drop the entry before the next page loads.
                del state
        if loaded < page:
            return
        if remaining is not None:
            remaining -= loaded
        page_size *= 2


def history_channels(graph: Pregel, value_keys: Iterable[str]) -> frozenset[str] | None:
    """Channels a history read must load to return ``value_keys`` of each entry.

    Returns None when the graph needs every channel. Rebuilding each entry's
    ``next`` and ``tasks`` needs every trigger channel, since LangGraph only
    counts a trigger as fired when its value is loaded, plus the tasks channel
    and the input of each node that reads a single channel. Nodes with a
    mapper (Pydantic or dataclass state) validate their whole input, and a
    cache policy computes its key from the whole input when tasks are rebuilt,
    so those graphs aren't narrowed.
    """
    nodes = graph.nodes.values()
    if graph.cache_policy is not None or any(
        node.mapper is not None or node.cache_policy is not None for node in nodes
    ):
        return None
    triggers = [channel for node in nodes for channel in node.triggers]
    single_inputs = [node.channels for node in nodes if isinstance(node.channels, str)]
    return frozenset((*value_keys, *triggers, *single_inputs, TASKS))


_GraphT = typing.TypeVar("_GraphT")


def narrow_history_reads(
    graph: _GraphT, config: RunnableConfig, value_keys: Iterable[str] | None
) -> _GraphT:
    """``graph``, set to load only what history needs to return ``value_keys``.

    Applies to root history of Python graphs whose checkpointer can load part
    of each checkpoint (``with_load_channels``). Subgraph namespaces have their
    own triggers, so they load every channel. Returns ``graph`` unchanged when
    it doesn't apply.
    """
    if (
        value_keys is None
        or not isinstance(graph, Pregel)
        or config["configurable"].get("checkpoint_ns")
    ):
        return graph
    with_load_channels = getattr(graph.checkpointer, "with_load_channels", None)
    if with_load_channels is None:
        return graph
    channels = history_channels(graph, value_keys)
    if channels is None:
        return graph
    return graph.copy(update={"checkpointer": with_load_channels(channels)})
