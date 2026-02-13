from __future__ import annotations

import asyncio
import importlib.util
import random
import sys
import threading
from collections.abc import AsyncIterator, Callable
from contextlib import AsyncExitStack, asynccontextmanager
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Self, cast

import structlog
from langgraph.checkpoint.base import (
    BaseCheckpointSaver,
    ChannelVersions,
    Checkpoint,
    CheckpointMetadata,
)
from langgraph.graph import StateGraph
from langgraph.pregel import Pregel

from langgraph_api import config, timing
from langgraph_api.timing import profiled_import
from langgraph_api.utils.config import run_in_executor

if TYPE_CHECKING:
    from collections.abc import AsyncIterator, Callable, Iterable, Sequence

    from langchain_core.runnables import RunnableConfig
    from langgraph.checkpoint.base import (
        ChannelVersions,
        Checkpoint,
        CheckpointMetadata,
        CheckpointTuple,
    )

    from langgraph_api._checkpointer.protocol import CheckpointerProtocol

logger = structlog.stdlib.get_logger(__name__)

CUSTOM_CHECKPOINTER: BaseCheckpointSaver | Callable[[], BaseCheckpointSaver] | None = (
    None
)
# Capabilities singleton - computed once when the first adapter is created
_CHECKPOINTER_CAPABILITIES: CheckpointerCapabilities | None = None
# Connection pools, futures, etc. are commonly scoped to a single event loop, so we
# want to allow the user the option of exposing a generator/constructor that
# would be entered into once per event loop.
CHECKPOINTER_STACK = threading.local()
_REQUIRED = (
    BaseCheckpointSaver.aput,
    BaseCheckpointSaver.aput_writes,
    BaseCheckpointSaver.aget_tuple,
    BaseCheckpointSaver.aget,
    BaseCheckpointSaver.alist,
)


@dataclass(frozen=True, slots=True)
class CheckpointerCapabilities:
    """Capabilities detected once at adapter initialization."""

    has_aget_iter: bool
    has_adelete_thread: bool
    has_adelete_for_runs: bool
    has_acopy_thread: bool
    has_aprune: bool

    @classmethod
    def from_type(cls: type[Self], inner_type: type) -> Self:
        """Detect checkpointer capabilities once at init time."""
        return cls(
            has_aget_iter=_is_overridden(inner_type, "aget_iter"),
            has_adelete_thread=_is_overridden(inner_type, "adelete_thread"),
            has_adelete_for_runs=_has_method(inner_type, "adelete_for_runs"),
            has_acopy_thread=_has_method(inner_type, "acopy_thread"),
            has_aprune=_has_method(inner_type, "aprune"),
        )


class _CustomCheckpointerAdapter(BaseCheckpointSaver):
    def __init__(
        self, inner: BaseCheckpointSaver, capabilities: CheckpointerCapabilities
    ) -> None:
        _validate_required_methods(inner)
        self._inner = inner
        self._capabilities = capabilities
        super().__init__(serde=getattr(inner, "serde", None))

    def __getattr__(self, name: str) -> Any:
        return getattr(self._inner, name)

    async def aget_iter(self, config: RunnableConfig) -> AsyncIterator[CheckpointTuple]:
        if self._capabilities.has_aget_iter:
            return await cast("CheckpointerProtocol", self._inner).aget_iter(config)

        else:

            async def gen():
                tup = await self.aget_tuple(config)
                if tup is not None:
                    yield tup

            return gen()

    async def aput(
        self,
        config: RunnableConfig,
        checkpoint: Checkpoint,
        metadata: CheckpointMetadata,
        new_versions: ChannelVersions,
    ) -> RunnableConfig:
        metadata = _enrich_metadata(metadata, config)
        return await self._inner.aput(config, checkpoint, metadata, new_versions)

    async def aput_writes(
        self,
        config: RunnableConfig,
        writes: Sequence[tuple[str, Any]],
        task_id: str,
        task_path: str = "",
    ) -> None:
        await self._inner.aput_writes(config, writes, task_id, task_path)

    async def alist(
        self,
        config: RunnableConfig | None,
        *,
        filter: dict[str, Any] | None = None,
        before: RunnableConfig | None = None,
        limit: int | None = None,
    ) -> AsyncIterator[CheckpointTuple]:
        async for item in self._inner.alist(
            config,
            filter=filter,
            before=before,
            limit=limit,
        ):
            yield item

    async def adelete_thread(self, thread_id: str) -> None:
        if self._capabilities.has_adelete_thread:
            await self._inner.adelete_thread(thread_id)
            return
        raise RuntimeError(
            "Please implement adelete_thread in your custom checkpointer to support thread deletion."
        )

    async def adelete_for_runs(self, run_ids: Iterable[str]) -> None:
        if self._capabilities.has_adelete_for_runs:
            await self._inner.adelete_for_runs(run_ids)
            return
        raise RuntimeError(
            "Please implement adelete_for_runs in your custom checkpointer "
            "to support run deletion/rollback."
        )

    async def acopy_thread(self, source_thread_id: str, target_thread_id: str) -> None:
        if self._capabilities.has_acopy_thread:
            await self._inner.acopy_thread(source_thread_id, target_thread_id)
            return
        raise RuntimeError(
            "Please implement acopy_thread in your custom checkpointer "
            "to support thread copy."
        )

    async def aprune(
        self, thread_ids: Sequence[str], *, strategy: str = "keep_latest"
    ) -> None:
        if self._capabilities.has_aprune:
            await self._inner.aprune(thread_ids, strategy=strategy)
            return
        raise RuntimeError(
            "Please implement aprune in your custom checkpointer "
            "to support thread pruning."
        )

    async def aget_tuple(self, config: RunnableConfig) -> CheckpointTuple | None:
        return await self._inner.aget_tuple(config)

    def get_next_version(self, current: str | None, channel: None) -> str:
        if current is None:
            current_v = 0
        elif isinstance(current, int):
            current_v = current
        else:
            current_v = int(current.split(".")[0])
        next_v = current_v + 1
        next_h = random.random()
        return f"{next_v:032}.{next_h:.16f}"


async def get_checkpointer(
    *,
    conn: Any | None = None,
    unpack_hook: Callable[[int, bytes], Any] | None = None,
    use_direct_connection: bool = False,
) -> CheckpointerProtocol:
    global _CHECKPOINTER_CAPABILITIES
    if CUSTOM_CHECKPOINTER is not None:
        # Get or create the inner checkpointer (cached per-thread)
        if not hasattr(CHECKPOINTER_STACK, "inner"):
            stack = AsyncExitStack()
            CHECKPOINTER_STACK.stack = stack
            inner = await stack.enter_async_context(
                _yield_checkpointer(CUSTOM_CHECKPOINTER)
            )
            CHECKPOINTER_STACK.inner = inner
            # Detect capabilities once for the server lifetime
            if _CHECKPOINTER_CAPABILITIES is None:
                _CHECKPOINTER_CAPABILITIES = CheckpointerCapabilities.from_type(
                    type(inner)
                )
            await logger.ainfo(
                f"Using custom checkpointer: {inner}",
                kind=str(type(inner)),
            )
        # Create a fresh adapter each time (not cached) - each gets own latest_iter
        if _CHECKPOINTER_CAPABILITIES is None:
            raise RuntimeError("Capabilities not initialized")
        return _CustomCheckpointerAdapter(
            inner=CHECKPOINTER_STACK.inner, capabilities=_CHECKPOINTER_CAPABILITIES
        )

    from langgraph_runtime.checkpoint import Checkpointer  # noqa: PLC0415

    return Checkpointer(
        conn, unpack_hook=unpack_hook, use_direct_connection=use_direct_connection
    )


def get_checkpointer_capabilities() -> CheckpointerCapabilities | None:
    """Return the capabilities of the custom checkpointer, or None if not configured."""
    return _CHECKPOINTER_CAPABILITIES


async def exit_checkpointer() -> None:
    if CUSTOM_CHECKPOINTER is None:
        return
    stack = cast("AsyncExitStack|None", getattr(CHECKPOINTER_STACK, "stack", None))
    if stack is None:
        return
    await stack.aclose()


async def collect_checkpointer_from_env() -> None:
    global CUSTOM_CHECKPOINTER
    checkpointer_path = None
    if not config.CHECKPOINTER_CONFIG or not (
        checkpointer_path := config.CHECKPOINTER_CONFIG.get("path")
    ):
        return

    await logger.ainfo(
        f"Heads up! You are configuring a custom checkpointer at {checkpointer_path}\n\n"
        "This checkpointer will be used INSTEAD OF the default persistence backend.\n"
        "The availability of some functionality, such as TTLs and pruning, may depend on the completion of your implementation.\n"
        "Performance & feature support will depend on the quality of your implementation."
    )

    value = await run_in_executor(None, _load_checkpointer, checkpointer_path)
    if asyncio.iscoroutine(value):
        value = await value
    if not isinstance(value, BaseCheckpointSaver) and not (
        hasattr(value, "__aenter__") or hasattr(value, "__enter__") or callable(value)
    ):
        raise ValueError(
            "Custom checkpointer must be a BaseCheckpointSaver or a callable/context manager that returns one."
        )
    CUSTOM_CHECKPOINTER = value


@asynccontextmanager
async def _yield_checkpointer(value: Any):
    if isinstance(value, BaseCheckpointSaver):
        yield value
    # Async context manager
    elif hasattr(value, "__aenter__") and hasattr(value, "__aexit__"):
        async with value as ctx_value:
            yield ctx_value
    # Sync context manager
    elif hasattr(value, "__enter__") and hasattr(value, "__exit__"):
        with value as ctx_value:
            yield ctx_value
    # async factory
    elif asyncio.iscoroutine(value):
        result = await value
        if not isinstance(result, BaseCheckpointSaver):
            raise ValueError(
                "Custom checkpointer must resolve to a BaseCheckpointSaver instance."
            )
        yield result
    # factory
    elif callable(value):
        async with _yield_checkpointer(value()) as ctx_value:
            yield ctx_value
    else:
        raise ValueError(
            f"Unsupported checkpointer type: {type(value)}. Expected an instance of BaseCheckpointSaver "
            "or a function/coroutine that returns one."
        )


# TODO: Consolidate loading code.
@timing.timer(
    message="Loading checkpointer {checkpointer_path}",
    metadata_fn=lambda checkpointer_path: {"checkpointer_path": checkpointer_path},
    warn_threshold_secs=5,
    warn_message="Loading checkpointer '{checkpointer_path}' took longer than expected",
    error_threshold_secs=10,
)
def _load_checkpointer(checkpointer_path: str) -> Any:
    with profiled_import(checkpointer_path):
        if "/" in checkpointer_path or ".py:" in checkpointer_path:
            path_name, function = checkpointer_path.rsplit(":", 1)
            module_name = path_name.rstrip(":")
            # Use deterministic module name based on path so shared modules are reused
            modname = (
                module_name.replace("/", "__")
                .replace(".py", "")
                .replace(" ", "_")
                .lstrip(".")
            )
            # Check if module already loaded (e.g., shared with graph loading)
            if modname in sys.modules:
                module = sys.modules[modname]
            else:
                modspec = importlib.util.spec_from_file_location(modname, module_name)
                if modspec is None:
                    raise ValueError(f"Could not find checkpointer file: {path_name}")
                module = importlib.util.module_from_spec(modspec)
                sys.modules[modname] = module
                modspec.loader.exec_module(module)  # type: ignore[possibly-unbound-attribute]
        else:
            path_name, function = checkpointer_path.rsplit(".", 1)
            module = importlib.import_module(path_name)

    try:
        checkpointer: (
            BaseCheckpointSaver
            | Callable[[config.CheckpointerConfig], BaseCheckpointSaver]
        ) = module.__dict__[function]
    except KeyError as e:
        available = [k for k in module.__dict__ if not k.startswith("__")]
        suggestion = ""
        if available:
            likely = [
                k
                for k in available
                if isinstance(module.__dict__[k], StateGraph | Pregel)
            ]
            if likely:
                likely_ = "\n".join(
                    [f"\t- {path_name}:{k}" if path_name else k for k in likely]
                )
                suggestion = f"\nDid you mean to use one of the following?\n{likely_}"
            elif available:
                suggestion = f"\nFound the following exports: {', '.join(available)}"

        raise ValueError(
            f"Could not find checkpointer '{checkpointer_path}'. "
            f"Please check that:\n"
            f"1. The file exports a variable named '{function}'\n"
            f"2. The variable name in your config matches the export name{suggestion}"
        ) from e
    return checkpointer


# Keys from config["configurable"] that should NOT be copied into checkpoint metadata.
_EXCLUDED_CONFIGURABLE_KEYS = frozenset({"checkpoint_ns", "checkpoint_id"})
# Keys that are request-scoped and must not be persisted in checkpoints.
_TRANSIENT_CONFIGURABLE_KEYS = frozenset(
    {
        "langgraph_request_id",
        "langgraph_auth_user",
        "langgraph_auth_user_id",
        "langgraph_auth_permissions",
    }
)


def _enrich_metadata(
    metadata: CheckpointMetadata, config: RunnableConfig
) -> CheckpointMetadata:
    """Enrich checkpoint metadata with config fields.

    Mirrors the metadata enrichment performed by the built-in checkpointers
    so that downstream consumers (API, state endpoints, copy) see a
    consistent metadata shape regardless of checkpointer implementation.
    """
    configurable = config.get("configurable", {})
    config_metadata = config.get("metadata", {})
    enriched: dict = {
        # 1. Non-internal configurable keys (thread_id, graph_id, etc.)
        **{
            k: v
            for k, v in configurable.items()
            if not k.startswith("__")
            and k not in _EXCLUDED_CONFIGURABLE_KEYS
            and k not in _TRANSIENT_CONFIGURABLE_KEYS
        },
        # 2. Config metadata (assistant_id, model_name, etc.)
        **{
            k: v
            for k, v in config_metadata.items()
            if k not in _TRANSIENT_CONFIGURABLE_KEYS
        },
        # 3. Original metadata on top (source, step, parents, etc.)
        **{k: v for k, v in metadata.items() if k not in _TRANSIENT_CONFIGURABLE_KEYS},
    }
    # Ensure run_id is present when available (not always set, e.g. state updates)
    if not enriched.get("run_id"):
        run_id = (
            config.get("run_id")
            or config_metadata.get("run_id")
            or configurable.get("run_id")
        )
        if run_id:
            enriched["run_id"] = run_id
    return enriched


def _validate_required_methods(inner: BaseCheckpointSaver):
    # Note: We should always be using the async methods.
    not_implemented = set()
    for method in _REQUIRED:
        method_name = method.__name__
        if getattr(inner, method_name, None) is method:
            not_implemented.add(method_name)
    if not_implemented:
        raise ValueError(
            f"Custom checkpointer must implement {sorted(not_implemented)}"
        )


def _is_overridden(inner_type: type, method: str) -> bool:
    base = getattr(BaseCheckpointSaver, method, None)
    impl = getattr(inner_type, method, None)
    if base is None or impl is None:
        return impl is not None
    return impl is not base


def _has_method(inner_type: type, method: str) -> bool:
    """Check if a type has a callable method (for methods not on BaseCheckpointSaver)."""
    return callable(getattr(inner_type, method, None))
