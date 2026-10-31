import asyncio
import contextlib
import glob
import os
import pickle
import uuid
from collections import defaultdict
from collections.abc import AsyncIterator, Awaitable, Callable
from contextlib import asynccontextmanager
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any, NotRequired
from uuid import UUID

import structlog
from langgraph.checkpoint.memory import PersistentDict
from typing_extensions import TypedDict

from langgraph_runtime_inmem import store
from langgraph_runtime_inmem._persistence import (
    register_persistent_dict,
    stop_flush_loop,
)
from langgraph_runtime_inmem.inmem_stream import start_stream, stop_stream

if TYPE_CHECKING:
    from langgraph_api.utils import AsyncConnectionProto

logger = structlog.stdlib.get_logger(__name__)


class Assistant(TypedDict):
    assistant_id: UUID
    graph_id: str
    name: str
    description: str | None
    created_at: NotRequired[datetime]
    updated_at: NotRequired[datetime]
    config: dict[str, Any]
    context: dict[str, Any]
    metadata: dict[str, Any]


class Thread(TypedDict):
    thread_id: UUID
    created_at: NotRequired[datetime]
    updated_at: NotRequired[datetime]
    state_updated_at: NotRequired[datetime]
    metadata: dict[str, Any]
    status: str


class Run(TypedDict):
    run_id: UUID
    thread_id: UUID
    assistant_id: UUID
    created_at: NotRequired[datetime]
    updated_at: NotRequired[datetime]
    metadata: dict[str, Any]
    status: str


class RunEvent(TypedDict):
    event_id: UUID
    run_id: UUID
    received_at: NotRequired[datetime]
    span_id: UUID
    event: str
    name: str
    tags: list[Any]
    data: dict[str, Any]
    metadata: dict[str, Any]


class AssistantVersion(TypedDict):
    assistant_id: UUID
    version: int
    graph_id: str
    config: dict[str, Any]
    context: dict[str, Any]
    metadata: dict[str, Any]
    created_at: NotRequired[datetime]
    name: str


class GlobalStore(PersistentDict):
    def __init__(self, *args: Any, filename: str, **kwargs: Any) -> None:
        super().__init__(*args, filename=filename, **kwargs)
        self.clear()

    def clear(self):
        assistants = self.get("assistants", [])
        super().clear()
        self["runs"] = []
        self["threads"] = []
        self["assistants"] = [
            a for a in assistants if a["metadata"].get("created_by") == "system"
        ]
        self["assistant_versions"] = []
        self["crons"] = []
        self["thread_has_next"] = {}
        self["thread_failed"] = {}


OPS_FILENAME = os.path.join(".langgraph_api", ".langgraph_ops.pckl")
RETRY_COUNTER_FILENAME = os.path.join(".langgraph_api", ".langgraph_retry_counter.pckl")


class InMemoryRetryCounter:
    def __init__(self):
        self._counters: dict[uuid.UUID, int] = PersistentDict(
            int, filename=RETRY_COUNTER_FILENAME
        )
        self._locks: dict[uuid.UUID, asyncio.Lock] = defaultdict(asyncio.Lock)

    async def increment(self, run_id: uuid.UUID) -> int:
        async with self._locks[run_id]:
            self._counters[run_id] += 1
            return self._counters[run_id]

    def close(self):
        self._counters.close()


# Global retry counter for in-memory implementation
GLOBAL_RETRY_COUNTER = InMemoryRetryCounter()
GLOBAL_STORE = GlobalStore(filename=OPS_FILENAME)


class InMemConnectionProto:
    def __init__(self):
        self.filename = OPS_FILENAME
        self.store = GLOBAL_STORE
        self.retry_counter = GLOBAL_RETRY_COUNTER
        self.can_execute = False

    @asynccontextmanager
    async def pipeline(self):
        yield None

    async def execute(self, query: str, *args, **kwargs):
        return None

    def clear(self):
        self.store.clear()
        keys = list(self.retry_counter._counters)
        for key in keys:
            del self.retry_counter._counters[key]
        keys = list(self.retry_counter._locks)
        for key in keys:
            del self.retry_counter._locks[key]
        if os.path.exists(self.filename):
            os.remove(self.filename)


@asynccontextmanager
async def connect(
    *, supports_core_api: bool = False, __test__: bool = False
) -> AsyncIterator["AsyncConnectionProto"]:
    yield InMemConnectionProto()


def _load_ops_file() -> None:
    """Load the saved ops file into ``GLOBAL_STORE``, setting it aside if unloadable.

    Runs the previous process left ``running`` are reset to ``pending`` to be retried.
    """
    if not os.path.exists(OPS_FILENAME):
        return

    # Not GLOBAL_STORE.load(): it treats a truncated file as empty.
    try:
        with open(OPS_FILENAME, "rb") as f:
            data = pickle.load(f)
        if not isinstance(data, dict):
            raise TypeError(f"expected a dict, found {type(data).__name__}")
    except Exception as e:
        if os.path.getsize(OPS_FILENAME) == 0:
            return
        _set_aside_ops_file(e)
        return
    GLOBAL_STORE.update(data)

    # No worker has started yet, so a run saved as running was cut off by a crash.
    # Left running, it blocks every later run on its thread (Runs.next skips the thread).
    orphaned = [r for r in GLOBAL_STORE.get("runs") or [] if r["status"] == "running"]
    now = datetime.now(UTC)
    for run in orphaned:
        run["status"] = "pending"
        run["updated_at"] = now
    if orphaned:
        logger.warning(
            "Retrying runs left running by a previous process that did not shut down cleanly",
            run_ids=[str(r["run_id"]) for r in orphaned],
        )


def upgrade_thread_status_facts(store: dict[str, Any]) -> None:
    """Ensure fact maps exist for ops files saved by older versions.

    Migration 000066 only adds nullable has_next / failed columns; it does not
    backfill. Writers fill the facts on the next status write, and status
    re-derivation keeps the stored status while either fact is still unknown.
    Cancels that older versions left in ``error`` are left as-is.
    """
    store.setdefault("thread_has_next", {})
    store.setdefault("thread_failed", {})


def _set_aside_ops_file(reason: Exception) -> None:
    """Rename an unloadable ops file to ``<file>.bak-<UTC timestamp>`` and log why."""
    from langgraph_api.graph import graph_file_module_names  # noqa: PLC0415

    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    backup = f"{OPS_FILENAME}.bak-{stamp}"
    n = 1
    while os.path.exists(backup):
        backup = f"{OPS_FILENAME}.bak-{stamp}-{n}"
        n += 1
    # Don't catch: carrying on would let the next flush overwrite the file.
    os.replace(OPS_FILENAME, backup)
    with contextlib.suppress(FileNotFoundError):
        os.remove(RETRY_COUNTER_FILENAME)
    try:
        with open(f"{backup}.reason", "w") as f:
            f.write(f"{type(reason).__name__}: {reason}")
    except OSError as e:
        logger.warning("Could not save why %s was set aside: %s", backup, e)

    message = (
        f"Could not load saved threads, runs and crons from {OPS_FILENAME}\n"
        f"  Reason: {type(reason).__name__}: {reason}\n"
        "  The server is starting without them. The file was NOT deleted; it was moved to:\n"
        f"    {backup}\n"
    )
    if (
        isinstance(reason, ModuleNotFoundError)
        and reason.name in graph_file_module_names()
    ):
        message += (
            f"  It references a class from your graph file (module '{reason.name}'), saved by an older\n"
            "  version of langgraph-api. It can't be restored; newer versions no longer save\n"
            "  data this way, so this won't happen again."
        )
    else:
        message += (
            "  To restore it: fix the cause, stop the server, and rename that file back to\n"
            f"  {os.path.basename(OPS_FILENAME)}. Threads created since this start will be lost.\n"
            "  This usually means a class stored in thread state was renamed, moved, or\n"
            "  failed to import (e.g. a syntax error in its module)."
        )
    logger.error(message, error_type=type(reason).__name__, backup=backup)


def _warn_about_ops_backups() -> None:
    """Log each ops-file backup left by an earlier start, with why it was set aside."""
    paths = glob.glob(f"{glob.escape(OPS_FILENAME)}.bak-*")
    backups = sorted(p for p in paths if not p.endswith(".reason"))
    for reason in paths:
        if reason.endswith(".reason") and reason.removesuffix(".reason") not in backups:
            os.remove(reason)
    if not backups:
        return

    lines = []
    for backup in backups:
        try:
            with open(f"{backup}.reason") as f:
                cause = f.read()
        except OSError:
            cause = "unknown cause"
        lines.append(f"  {backup}: {cause}")
    logger.warning(
        f"{len(backups)} unloadable ops file backup(s). Rename one to "
        f"{os.path.basename(OPS_FILENAME)} once its cause is fixed, or delete it:\n"
        + "\n".join(lines),
        backups=backups,
    )


async def start_pool() -> None:
    if store._STORE_CONFIG is None:
        from langgraph_api import config as langgraph_config  # noqa: PLC0415

        if langgraph_config.STORE_CONFIG:
            config_ = langgraph_config.STORE_CONFIG
            store.set_store_config(config_)

    if not os.path.exists(".langgraph_api"):
        os.mkdir(".langgraph_api")
    _warn_about_ops_backups()
    _load_ops_file()
    for k in ["runs", "threads", "assistant_versions", "assistants"]:
        if not GLOBAL_STORE.get(k):
            GLOBAL_STORE[k] = []
    upgrade_thread_status_facts(GLOBAL_STORE)
    # Remove agents that were created by the system to avoid removed graphs
    if GLOBAL_STORE.get("assistants"):
        for a in GLOBAL_STORE["assistants"]:
            if a["metadata"].get("created_by") == "system":
                GLOBAL_STORE["assistants"].remove(a)
            if "context" not in a:
                a["context"] = {}
    for k in ["crons"]:
        if not GLOBAL_STORE.get(k):
            GLOBAL_STORE[k] = []
    # Flushed in this order: a crash between the two writes then over-counts an
    # attempt rather than letting a retried run skip one.
    register_persistent_dict(GLOBAL_RETRY_COUNTER._counters)
    register_persistent_dict(GLOBAL_STORE)
    await start_stream()


async def stop_pool() -> None:
    # Stop flushing before closing: close() clears the dicts, and a later flush would write {}.
    stop_flush_loop()
    await asyncio.to_thread(GLOBAL_STORE.close)
    await asyncio.to_thread(GLOBAL_RETRY_COUNTER.close)
    from langgraph_runtime_inmem.checkpoint import Checkpointer  # noqa: PLC0415
    from langgraph_runtime_inmem.store import STORE  # noqa: PLC0415

    await asyncio.to_thread(STORE.close)

    async with Checkpointer():
        pass
    await stop_stream()


def dependency_checks() -> dict[str, Callable[[], Awaitable[None]]]:
    """No external data dependencies to probe."""
    return {}


async def healthcheck(*, check_db: bool = True) -> None:
    # What could possibly go wrong?
    pass


def pool_stats(*args, **kwargs) -> dict[str, dict[str, int]]:
    # TODO??
    return {}
