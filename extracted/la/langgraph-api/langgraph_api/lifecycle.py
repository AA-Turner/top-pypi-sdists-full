"""`lifecycle` events on v1 runs: when each subgraph starts and how it ends.

A subgraph runs in the namespace `<node>:<task_id>` of the task that called it.
It starts with the first thing that runs in that namespace and ends with that
task, so both sources below apply the same rule:

- `SubgraphLifecycle` reads task payloads. Runs with `stream_subgraphs` already
  carry every subgraph's task events in `debug`, in order with its other events.
- `ChainLifecycle` listens to the chain callbacks every task fires. Without
  `stream_subgraphs` no subgraph event reaches the server, so it is the only
  source; `LifecycleFeed` sends its events as they happen.
"""

import asyncio
import threading
from collections.abc import AsyncIterator, Callable
from contextlib import suppress
from typing import Any, NamedTuple
from uuid import UUID

from langchain_core.callbacks import BaseCallbackHandler
from langgraph.constants import TAG_HIDDEN
from langgraph.errors import GraphBubbleUp, ParentCommand

from langgraph_api.serde import HIDDEN_ERROR_MESSAGE

# serde's shape for an error it hides, for a value that isn't an exception. A JS
# error arrives as a plain value whose `name` and message are whatever user code
# set, so neither is sent.
HIDDEN_ERROR = {"error": "Error", "message": HIDDEN_ERROR_MESSAGE}


class LifecycleEvent(NamedTuple):
    mode: str
    data: dict[str, Any]


def _event(ns: tuple[str, ...], data: dict[str, Any]) -> LifecycleEvent:
    return LifecycleEvent(f"lifecycle|{'|'.join(ns)}", {**data, "namespace": list(ns)})


def _with_tool_call_id(
    data: dict[str, Any], tool_call_id: str | None
) -> dict[str, Any]:
    return {**data, "tool_call_id": tool_call_id} if tool_call_id else data


def _subgraph_ns(ns: tuple[str, ...]) -> tuple[str, ...]:
    """`ns` without the `|<n>` langgraph appends when a task runs a subgraph again.

    A retry or a second call runs in `<node>:<task_id>|1`, but it is still that
    task's subgraph.
    """
    while ns and ns[-1].isdigit():
        ns = ns[:-1]
    return ns


def _task_id(ns: tuple[str, ...]) -> str:
    """The id of the task a namespace runs in, or "" for the root or a segment without one.

    `rpartition`: a `@task` may have `:` in its name; task ids never do.
    """
    return ns[-1].rpartition(":")[2] if ns and ":" in ns[-1] else ""


def _tool_call_id(task_input: Any) -> str | None:
    """The id of the one tool call a task runs, in the shapes agents pass it.

    `[tool_call]` (langchain `create_agent`), `{"tool_call": ...}` (langgraph
    `ToolNode`) or `{"lg_tool_call": ...}` (langchainjs `createAgent`). A list of
    several binds none: their subgraphs share one namespace.
    """
    if isinstance(task_input, dict):
        task_input = [task_input.get("tool_call") or task_input.get("lg_tool_call")]
    if not isinstance(task_input, list) or len(task_input) != 1:
        return None
    call = task_input[0]
    if not isinstance(call, dict) or "name" not in call or "args" not in call:
        return None
    tool_call_id = call.get("id")
    return tool_call_id if isinstance(tool_call_id, str) else None


def _failed(error: Any) -> dict[str, Any]:
    return {
        "event": "failed",
        "error": error if isinstance(error, BaseException) else HIDDEN_ERROR,
    }


def _graph_namespace(metadata: dict[str, Any]) -> tuple[str, ...]:
    """The namespace of the graph a task's chain runs in.

    Mirrors langgraph's private `langgraph.pregel._messages.graph_namespace`: drops
    the task's own segment, and one more per enclosing `@task` call (a call runs
    in its caller's graph, but nests its segment under the caller's).
    """
    ns = tuple(metadata["langgraph_checkpoint_ns"].split("|"))
    path = metadata.get("langgraph_path", ())
    drop = 1
    while len(path) == 4 and path[0] == "__pregel_push" and path[-1] is True:
        drop += 1
        path = path[1]
    return ns[:-drop]


class SubgraphLifecycle:
    """Lifecycle events from task payloads, root and namespaced."""

    def __init__(self) -> None:
        self._tool_call_ids: dict[str, str] = {}
        self._open: dict[str, tuple[str, ...]] = {}

    def on_task(
        self, ns: tuple[str, ...], task: dict[str, Any]
    ) -> list[LifecycleEvent]:
        if "result" in task:
            tool_call_id = self._tool_call_ids.pop(task["id"], None)
            if (child := self._open.pop(task["id"], None)) is None:
                return []
            if task.get("interrupts"):
                outcome = {"event": "interrupted"}
            elif task.get("error") is not None:
                outcome = _failed(task["error"])
            else:
                outcome = {"event": "completed"}
            return [_event(child, _with_tool_call_id(outcome, tool_call_id))]
        if tool_call_id := _tool_call_id(task.get("input")):
            self._tool_call_ids[task["id"]] = tool_call_id
        ns = _subgraph_ns(ns)
        task_id = _task_id(ns)
        if not task_id or task_id in self._open:
            return []
        self._open[task_id] = ns
        started = {"event": "started"}
        return [
            _event(ns, _with_tool_call_id(started, self._tool_call_ids.get(task_id)))
        ]


class ChainLifecycle(BaseCallbackHandler):
    """Lifecycle events from the chain callbacks of a run's tasks, at any depth.

    A task's own chain is the outermost chain named after its node. Callbacks of
    sync nodes come from worker threads, hence the lock.
    """

    run_inline = True
    ignore_llm = True
    ignore_chat_model = True
    ignore_retriever = True
    ignore_agent = True
    ignore_custom_event = True

    def __init__(self, emit: Callable[[LifecycleEvent], None]) -> None:
        self._emit = emit
        self._lock = threading.Lock()
        self._task_by_run: dict[UUID, str] = {}
        self._run_by_task: dict[str, UUID] = {}
        self._tool_call_ids: dict[str, str] = {}
        self._open: dict[str, tuple[str, ...]] = {}

    def on_chain_start(
        self,
        serialized: dict[str, Any] | None,
        inputs: Any,
        *,
        run_id: UUID,
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        if not metadata or "langgraph_checkpoint_ns" not in metadata:
            return
        if tags and TAG_HIDDEN in tags:
            return
        task_id = metadata["langgraph_checkpoint_ns"].rpartition(":")[2]
        ns = _subgraph_ns(_graph_namespace(metadata))
        with self._lock:
            if (
                kwargs.get("name") == metadata.get("langgraph_node")
                and task_id not in self._run_by_task
            ):
                self._task_by_run[run_id] = task_id
                self._run_by_task[task_id] = run_id
                if tool_call_id := _tool_call_id(inputs):
                    self._tool_call_ids[task_id] = tool_call_id
            trigger = _task_id(ns)
            if not trigger or trigger in self._open:
                return
            self._open[trigger] = ns
            started = {"event": "started"}
            event = _event(
                ns, _with_tool_call_id(started, self._tool_call_ids.get(trigger))
            )
        self._emit(event)

    def on_chain_end(self, outputs: Any, *, run_id: UUID, **kwargs: Any) -> None:
        self._end(run_id, {"event": "completed"})

    def on_chain_error(
        self, error: BaseException, *, run_id: UUID, **kwargs: Any
    ) -> None:
        if isinstance(error, ParentCommand):
            self._end(run_id, {"event": "completed"})
        elif isinstance(error, GraphBubbleUp):
            self._end(run_id, {"event": "interrupted"})
        else:
            self._end(run_id, _failed(error))

    def _end(self, run_id: UUID, outcome: dict[str, Any]) -> None:
        with self._lock:
            if (task_id := self._task_by_run.pop(run_id, None)) is None:
                return
            del self._run_by_task[task_id]
            tool_call_id = self._tool_call_ids.pop(task_id, None)
            if (child := self._open.pop(task_id, None)) is None:
                return
            event = _event(child, _with_tool_call_id(outcome, tool_call_id))
        self._emit(event)


class LifecycleFeed:
    """A graph's stream with `ChainLifecycle`'s events merged in as they happen.

    A subgraph can run for minutes with no chunk reaching the server, so its
    `started` can't wait for the next chunk. A lifecycle event never cancels the
    pending chunk: that would cancel the graph.
    """

    def __init__(self) -> None:
        self._loop = asyncio.get_running_loop()
        self._events: asyncio.Queue[LifecycleEvent] = asyncio.Queue()
        self.listener = ChainLifecycle(self._put)

    def _put(self, event: LifecycleEvent) -> None:
        try:
            on_loop = asyncio.get_running_loop() is self._loop
        except RuntimeError:
            on_loop = False
        if on_loop:
            self._events.put_nowait(event)
        else:
            self._loop.call_soon_threadsafe(self._events.put_nowait, event)

    async def merge(self, stream: AsyncIterator[Any]) -> AsyncIterator[Any]:
        sentinel = object()
        pending = asyncio.ensure_future(anext(stream, sentinel))
        try:
            while True:
                event = asyncio.ensure_future(self._events.get())
                try:
                    await asyncio.wait(
                        (pending, event), return_when=asyncio.FIRST_COMPLETED
                    )
                finally:
                    if not event.done():
                        event.cancel()
                if event.done() and not event.cancelled():
                    yield event.result()
                    continue
                chunk = pending.result()
                if chunk is sentinel:
                    # A `get` cancelled after the queue woke it leaves its event queued.
                    while not self._events.empty():
                        yield self._events.get_nowait()
                    return
                yield chunk
                pending = asyncio.ensure_future(anext(stream, sentinel))
        finally:
            if not pending.done():
                pending.cancel()
                with suppress(asyncio.CancelledError):
                    await pending
            await stream.aclose()
