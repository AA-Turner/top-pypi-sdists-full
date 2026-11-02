"""hooks.host/run/queue: run a harness's hook event off the loop, keep warm hosts, queue for sessions with none."""

from __future__ import annotations

import asyncio
import contextlib
import re
import threading
import time
from collections.abc import Callable

from ...actions import caller
from ...hooks.hooks import DRAIN_S, UNHOSTED_LANES, Via, run_event, timed_out_answer
from ....foundation.service_api.wire import (
    MAX_LINE_BYTES,
    encode,
    result)
from ....foundation.service_api.params import (
    need_hook_queue,
    need_hook_run)
from ...watch.incident import Family
from probe.service.server.connections.connections import Connection
from probe.service.server.policy import log
#: `hooks.run` events running at once, at most: each holds a thread while its
#: routes run (a caller waits 300 ms by default; a later one waits its turn,
#: within its own wait).
MAX_HOOK_RUNS = 8
#: `hooks.run` events taken in at once (running, or queued for a thread): past
#: it a request is refused at once, so stalled folder checks (a hung network
#: mount) never queue without limit. A queued event whose caller's wait has
#: passed is dropped unrun.
MAX_PENDING_HOOK_RUNS = 2 * MAX_HOOK_RUNS
#: `hooks.run`'s answer may land this long after its deadline: an event that
#: ended right at it still has its output read (`hookhosts.DRAIN_S`).
ANSWER_GRACE_S = DRAIN_S + 0.05
#: Host starts (`hooks.host`, a `hooks.run` warm-up) on their own threads, and
#: at most this many taken in at once.
HOST_START_THREADS = 2
MAX_PENDING_HOST_STARTS = 4
#: What a `hooks.queue` answer waits for its store, at most (the dispatcher
#: itself waits 300 ms, then writes the event beside it: one id runs once).
QUEUE_STORE_WAIT_S = 5.0
#: What a `hooks.host` caller waits for its host start, at most.
HOST_START_WAIT_S = 5.0
#: A folder's warm host is started for `hooks.run` at most this often (a host
#: that will not stay up is not started again on every tool call): the
#: dispatcher's own `ASK_EVERY_S`.
WARM_EVERY_S = 30.0
#: `hooks.run` runs only the events pi sends it (plan D38, pi's `serviceGuard.ts`):
#: the pre-tool lane, for the tools pi's guard reads (its `ClaudeTool` names, and
#: Probe's own MCP tools, which routes.json's matcher takes by `probe[-_]research`).
#: Any process of this user reaches the socket, and the payload is the caller's
#: word: another lane or tool would run Probe's consent routes on a forged
#: event -- a typed `/probe inline` on the prompt lane moves the switch, a
#: question-tool pick on the post-tool lane records a yes with the answer key the
#: hook reads, a question tool's pre-tool route records a permission mode the
#: daemon reads as bypass (#3355).
HOOK_RUN_LANES = frozenset({"pre-tool"})
HOOK_RUN_TOOLS = frozenset({"Bash", "Write", "Edit", "MultiEdit"})
PROBE_MCP_TOOL = "probe[-_]research"


class HookHandlersMixin:
    """Part of Service: its methods run with `self` the Service; compose() folds them into Service."""

    async def _hooks_host(self, conn: Connection, params: dict) -> dict:
        """`hooks.host` (plan A0): never for a caller in a sandbox, whose events
        (and the interpreter it names) would run outside it. The start itself
        (a folder check, a process start) runs on a thread (`_start_host`)."""
        if caller.sandboxed(conn.peer_pid):
            return {"refused": "a caller in a sandbox"}
        return await self._start_host(params)

    def _pool(self, name: str, workers: int):
        pool = getattr(self, name)
        if pool is None:
            from concurrent.futures import ThreadPoolExecutor

            pool = ThreadPoolExecutor(max_workers=workers, thread_name_prefix=name.strip("_").replace("_", "-"))
            setattr(self, name, pool)
        return pool

    async def _offload(self, pool: str, workers: int, slots, busy: str, wait: float, fn, *args, late=None):
        """`fn(*args)` on one of `pool`'s threads, never this loop: `(True,
        its value)`, or `(False, None)` when it is not done within `wait`
        (`late`, when given, then gets its value on this loop once it is).

        Admission is a slot of `slots`, taken here (`{"refused": busy}` at once
        when none is free) and given back only by the thread, when it has run
        the item: so the pool never holds more work items than there are slots,
        however many callers come and go while its threads are stalled. A
        caller past its wait gives up on the answer but never cancels the item
        (a cancelled item would keep its place in the queue with its slot
        given back); `fn` drops work whose deadline passed the moment a thread
        takes it (`hookhosts.run_event`)."""
        if not slots.acquire(blocking=False):
            return True, {"refused": busy}
        once = threading.Lock()  # the slot goes back exactly once

        def give_back() -> None:
            if once.acquire(blocking=False):
                slots.release()

        def held():
            try:
                return fn(*args)
            finally:
                give_back()

        try:
            future = asyncio.wrap_future(self._pool(pool, workers).submit(held))
        except RuntimeError:
            # Shut down (the service is stopping), or no thread would start for
            # an item already queued: that item still gives its slot back when
            # it runs, so never twice (a second release raises ValueError).
            give_back()
            return True, {"refused": "the service could not take it (stopping, or no thread would start)"}
        done, _ = await asyncio.wait({future}, timeout=max(wait, 0.0))
        if done:
            return True, future.result()
        future.add_done_callback(lambda settled: _settled(settled, late))
        return False, None

    async def _start_host(self, params: dict) -> dict:
        done, answer = await self._offload(
            "_host_starts", HOST_START_THREADS, self._host_slots, "busy: too many host starts in flight",
            HOST_START_WAIT_S, self.hookhosts.host, params,
        )
        return answer if done else {"refused": "the host is still starting"}

    async def _hooks_run(self, conn: Connection, params: dict) -> dict:
        """`hooks.run` (plan D38): one hook event of a harness that has no hooks
        of its own (pi), run for a Probe plugin folder exactly as its dispatcher
        runs it (`hookhosts.run_event`), and the merged output back. Same
        caller checks as `hooks.host`: the peer's uid (every connection), never
        a caller in a sandbox (or one whose pid the kernel will not name), whose
        event would run outside it with the environment it sent; and only a
        complete Probe plugin folder, checked on the thread (it reads files
        the request names: never on this loop, which every client waits on).
        A folder that had no warm host gets one for its next event, also when
        the event's answer comes past its caller's wait (`late`): where the
        kernel has no `os.waitid` (macOS) stopping an overrun outlasts
        ANSWER_GRACE_S."""
        request = need_hook_run(params)
        request["deadline"] = time.monotonic() + request["timeout_s"]
        refused = _hook_run_refusal(request["lane"], params["payload"].get("tool_name"))
        if refused is not None:
            return {"refused": refused}
        if caller.sandboxed(conn.peer_pid):
            return {"refused": "a caller in a sandbox"}
        # The folder's check reads files the request names: on the thread too,
        # and the answer by the deadline whatever that check costs.
        done, answer = await self._offload(
            "_hook_runs", MAX_HOOK_RUNS, self._hook_slots, "busy: too many hook events in flight",
            request["deadline"] - time.monotonic() + ANSWER_GRACE_S, run_event, request, conn.peer_pid,
            late=lambda late_answer: self._warm_after(request, late_answer),
        )
        if not done:
            self._note_hook_run(request, None)
            return timed_out_answer()
        if "refused" in answer:
            return answer
        self._note_hook_run(request, answer)
        self._warm_after(request, answer)
        # Past what a client reads in one line: stderr goes first, then stdout,
        # each marked cut, so an intact stdout keeps its verdict while it fits.
        for stream in ("stderr", "stdout"):
            if len(encode(result(0, answer))) <= MAX_LINE_BYTES:
                break
            answer = {**answer, stream: "", f"{stream}_truncated": True, "truncated": True}
        return answer

    async def _hooks_queue(self, conn: Connection, params: dict) -> dict:
        """`hooks.queue` (plan D36): a session's dispatcher that no warm host
        took an event from ran there only what the agent waits on, and hands
        this the event's record-keeping routes, to run once by its id
        (`hookqueue.HookQueue`: `{"queued": true, "duplicate": bool}`, or
        `{"refused": why}`, and the dispatcher then runs them itself). Never
        from a caller in a sandbox (as `hooks.run`: the event would run outside
        it, with the environment it sent). Stored on a thread (a file write),
        run on the queue's own, never on this loop."""
        item = need_hook_queue(params)
        if caller.sandboxed(conn.peer_pid):
            return {"refused": "a caller in a sandbox"}
        done, answer = await self._offload(
            "_queue_stores", 1, self._queue_slots, "busy: too many hook events queued at once",
            QUEUE_STORE_WAIT_S, self.hook_queue.store, item,
        )
        if not done:
            # Still being written, and its caller long gone (it wrote the
            # event beside it, or ran it): the store goes on and runs it once.
            log(f"hooks.queue {item['id']}: still storing after {QUEUE_STORE_WAIT_S}s")
            return {"queued": True, "duplicate": False}
        return answer

    def _note_hook_run(self, request: dict, answer: dict | None) -> None:
        """`hooks.run` ran out of time (`answer` None: not even an answer), or
        the warm host running its event was lost: one event of `hook_host`
        (plan B2). Never its exit code: 2 is a Stop message delivered (or a
        veto), and the dispatcher turns its own failures into 0 (Codex rev-3 #3)."""
        if answer is None or answer.get("timed_out"):
            reason = "timed_out"
        elif answer.get("via") == Via.HOST and answer.get("exit_code") is None:
            reason = "host_lost"
        else:
            return
        self.watch.note(Family.HOOK_HOST, reason, facts={
            "lane": request["lane"], "via": None if answer is None else answer.get("via"),
            "timeout_s": request["timeout_s"],
        }, env=request.get("env"))  # the session's own: its opt-out counts

    def _warm_after(self, request: dict, answer: dict) -> None:
        """After `hooks.run`'s event: its folder's warm host when it ran without one."""
        if (
            "refused" not in answer
            and answer.get("via") != Via.HOST
            and request["lane"] not in UNHOSTED_LANES
            and self.stop_reason is None
        ):
            root = request["root"]
            asyncio.get_running_loop().call_soon(lambda: self._warm(root))

    def _queue_changed(self) -> None:
        """From any thread: queued hook events started or stopped holding the service."""
        loop = self._loop
        if loop is not None and not loop.is_closed():
            with contextlib.suppress(RuntimeError):
                loop.call_soon_threadsafe(self.reevaluate)

    def _warm_soon(self, root: str) -> None:
        """From the queue's thread: `root`'s warm host for its next event."""
        loop = self._loop
        if loop is not None and not loop.is_closed():
            with contextlib.suppress(RuntimeError):
                loop.call_soon_threadsafe(self._warm, root)

    def _warm(self, root: str) -> None:
        """Start `root`'s warm host for its next `hooks.run` (`hooks.host`), at
        most every WARM_EVERY_S, on a thread (`_start_host`): never waited on."""
        now, last = time.monotonic(), self._warmed.get(root)
        if self.stop_reason is not None or (last is not None and now - last < WARM_EVERY_S):
            return
        self._warmed[root] = now
        task = asyncio.ensure_future(self._warm_task(root))
        self._warming.add(task)
        task.add_done_callback(self._warming.discard)

    async def _warm_task(self, root: str) -> None:
        try:
            await self._start_host({"root": root})
        except Exception as exc:  # noqa: BLE001 -- only the next event's speed is at stake
            log(f"hook host for {root} would not start: {exc!r}")


def _hook_run_refusal(lane: str, tool: object) -> str | None:
    """Why `hooks.run` will not run this event (`HOOK_RUN_LANES`, `HOOK_RUN_TOOLS`),
    or None: only what pi's guard sends."""
    if lane not in HOOK_RUN_LANES:
        return f"hooks.run runs only pi's guard: lane {lane!r} is not served"
    if not isinstance(tool, str) or not (tool in HOOK_RUN_TOOLS or re.search(PROBE_MCP_TOOL, tool)):
        return "hooks.run runs only pi's guard: not a tool it reads"
    return None


def _settled(future: asyncio.Future, then: Callable[[object], None] | None = None) -> None:
    """An answer nobody waits for any more: read, so it is never reported
    unread, and handed to `then` (when given) if it is a value."""
    if not future.cancelled() and future.exception() is None and then is not None:
        then(future.result())
