"""Framework-agnostic lifecycle bridge (L2).

Generic over any framework that exposes "wrap a user-facing method" entry
points (LangGraph's invoke/ainvoke/stream/astream, CrewAI's Crew.kickoff,
Strands' agent.run, etc.). Owns trace creation, thread stitching,
pause/done detection, re-entry guarding, and finalize routing.

Subclasses supply framework-specific hooks via the abstract methods below.

The four ``wrap_*`` methods share setup + teardown via ``_build_sync_setup``
/ ``_build_async_setup`` / ``_teardown`` helpers — each wrapper is then 8
lines of pure-shape glue.
"""

from __future__ import annotations

import abc
import logging
from collections.abc import Callable
from contextvars import Token
from typing import Any

from aigie.tracing.reasoning_plan import ReasoningPlan
from aigie.tracing.retention import is_retention_suppressed
from aigie.tracing.trace_state import close_ambient, open_ambient

_log = logging.getLogger(__name__)


class FrameworkLifecycleBridge(abc.ABC):
    """Subclass + override the abstract hooks below."""

    framework_type: str = "generic"

    # ─── Framework hooks (subclasses implement) ─────────────────────────

    @abc.abstractmethod
    def _graph_is_done(self, framework_handle: Any, config: dict | None) -> bool:
        """True when the run has no more pending work (no resume expected)."""

    @abc.abstractmethod
    def _is_controlled_pause(self, error: Exception | None) -> bool:
        """True for framework-native pause/interrupt signals (e.g. GraphInterrupt)."""

    @abc.abstractmethod
    def _extract_thread_id(self, config: dict | None) -> str | None:
        """Extract the resumable-thread identifier from the framework's config."""

    @abc.abstractmethod
    def _extract_workflow_name(self, input: Any, schema: Any = None) -> str:
        """Derive a human-readable workflow name from input + schema."""

    @abc.abstractmethod
    def extract_reasoning_plan(self, framework_handle: Any) -> ReasoningPlan | None:
        """Return the static reasoning plan for ``framework_handle``, or None.

        Called once per traced invocation by ``_build_sync_setup`` /
        ``_build_async_setup``. The substrate merges the result into trace
        metadata as ``reasoning_plan`` (and lifts ``agent_prompt`` when a
        single static prompt is present), so subclasses never need to wire
        emission themselves.

        Returning None is allowed when the framework genuinely has no static
        topology to expose at invocation time. Returning a partial plan
        (e.g. nodes-only) is fine; downstream consumers tolerate missing
        fields.
        """

    @abc.abstractmethod
    def _make_handler(self, trace_id: str) -> Any:
        """Construct the framework-binding callback. Must expose a
        ``spans`` attribute (a ``SpanEventHandler``) for close_pending_spans
        / close_trace dispatch."""

    @abc.abstractmethod
    def _create_trace_sync(self, *, name: str, metadata: dict[str, Any]) -> Any:
        """Create a trace and return an object exposing .id (str)."""

    @abc.abstractmethod
    async def _create_trace(self, *, name: str, metadata: dict[str, Any]) -> Any:
        """Async counterpart of _create_trace_sync."""

    def _already_tracing(self, config: dict | None) -> bool:
        """Override to detect the caller is inside an existing traced run."""
        return False

    def _zero_retention_from_handler(self) -> bool:
        """Subclasses override to short-circuit trace creation when their
        static config has zero_retention=True. Default: False (only the
        ContextVar route applies).
        """
        return False

    def _before_run(
        self, handler: Any, framework_handle: Any, input: Any, config: dict | None
    ) -> None:
        """Hook called after handler creation, before invoking user code."""
        return

    def _after_run(
        self, handler: Any, input: Any, config: dict | None, error: Exception | None
    ) -> None:
        """Hook called in the finally block, after _finalize."""
        return

    # ─── Shared setup / teardown ────────────────────────────────────────

    def _build_metadata(self, framework_handle: Any, input: Any, config: dict | None) -> dict:
        """Build trace metadata, merging the framework's reasoning plan.

        A buggy integration's ``extract_reasoning_plan`` must NOT take down
        the whole trace — the contract is "best-effort metadata enrichment",
        not "load-bearing". Swallow + log, never re-raise.
        """
        metadata = self._trace_metadata(input, config)
        try:
            plan = self.extract_reasoning_plan(framework_handle)
        except Exception:  # noqa: BLE001 — see docstring
            _log.debug("extract_reasoning_plan raised; emitting trace without plan", exc_info=True)
            return metadata
        if plan is not None:
            metadata["reasoning_plan"] = plan.to_dict()
            if plan.agent_prompt:
                metadata.setdefault("agent_prompt", plan.agent_prompt)
        return metadata

    def _build_sync_setup(
        self, framework_handle: Any, input: Any, config: dict | None
    ) -> tuple[Any | None, dict | None, Token | None]:
        """Returns (handler, mutable_config, ambient_token).
        (None, config, None) when caller should skip-trace (already tracing
        or zero-retention is active).
        """
        if self._already_tracing(config):
            return None, config, None
        if is_retention_suppressed() or self._zero_retention_from_handler():
            return None, config, None
        trace = self._create_trace_sync(
            name=self._extract_workflow_name(input),
            metadata=self._build_metadata(framework_handle, input, config),
        )
        token = open_ambient(trace_id=trace.id)
        handler = self._make_handler(trace.id)
        config = dict(config) if config is not None else {}
        self._before_run(handler, framework_handle, input, config)
        return handler, config, token

    async def _build_async_setup(
        self, framework_handle: Any, input: Any, config: dict | None
    ) -> tuple[Any | None, dict | None, Token | None]:
        if self._already_tracing(config):
            return None, config, None
        if is_retention_suppressed() or self._zero_retention_from_handler():
            return None, config, None
        trace = await self._create_trace(
            name=self._extract_workflow_name(input),
            metadata=self._build_metadata(framework_handle, input, config),
        )
        token = open_ambient(trace_id=trace.id)
        handler = self._make_handler(trace.id)
        config = dict(config) if config is not None else {}
        self._before_run(handler, framework_handle, input, config)
        return handler, config, token

    def _teardown(
        self,
        framework_handle: Any,
        config: dict | None,
        handler: Any | None,
        token: Token | None,
        error: Exception | None,
    ) -> None:
        if handler is None:
            return
        try:
            self._finalize(framework_handle, config, handler, error)
            self._after_run(handler, None, config, error)
        finally:
            if token is not None:
                close_ambient(token)

    # ─── Wrappers ───────────────────────────────────────────────────────

    def wrap_sync(
        self, *, framework_handle: Any, original: Callable[..., Any]
    ) -> Callable[..., Any]:
        bridge = self

        def wrapped(input: Any, config: dict | None = None, **kwargs: Any) -> Any:
            handler, config, token = bridge._build_sync_setup(framework_handle, input, config)
            if handler is None:
                return original(input, config=config, **kwargs)
            err: Exception | None = None
            try:
                return original(input, config=config, **kwargs)
            except Exception as e:
                err = e
                raise
            finally:
                bridge._teardown(framework_handle, config, handler, token, err)

        return wrapped

    def wrap_async(
        self, *, framework_handle: Any, original: Callable[..., Any]
    ) -> Callable[..., Any]:
        bridge = self

        async def wrapped(input: Any, config: dict | None = None, **kwargs: Any) -> Any:
            handler, config, token = await bridge._build_async_setup(
                framework_handle, input, config
            )
            if handler is None:
                return await original(input, config=config, **kwargs)
            err: Exception | None = None
            try:
                return await original(input, config=config, **kwargs)
            except Exception as e:
                err = e
                raise
            finally:
                bridge._teardown(framework_handle, config, handler, token, err)

        return wrapped

    def wrap_stream_sync(
        self, *, framework_handle: Any, original: Callable[..., Any]
    ) -> Callable[..., Any]:
        bridge = self

        def wrapped(input: Any, config: dict | None = None, **kwargs: Any):
            handler, config, token = bridge._build_sync_setup(framework_handle, input, config)
            if handler is None:
                yield from original(input, config=config, **kwargs)
                return
            err: Exception | None = None
            try:
                # Explicit for/yield (not `yield from`) so exceptions land in this frame.
                for chunk in original(input, config=config, **kwargs):  # noqa: UP028
                    yield chunk
            except Exception as e:
                err = e
                raise
            finally:
                bridge._teardown(framework_handle, config, handler, token, err)

        return wrapped

    def wrap_stream_async(
        self, *, framework_handle: Any, original: Callable[..., Any]
    ) -> Callable[..., Any]:
        bridge = self

        async def wrapped(input: Any, config: dict | None = None, **kwargs: Any):
            handler, config, token = await bridge._build_async_setup(
                framework_handle, input, config
            )
            if handler is None:
                async for chunk in original(input, config=config, **kwargs):
                    yield chunk
                return
            err: Exception | None = None
            try:
                async for chunk in original(input, config=config, **kwargs):
                    yield chunk
            except Exception as e:
                err = e
                raise
            finally:
                bridge._teardown(framework_handle, config, handler, token, err)

        return wrapped

    # ─── Internals ──────────────────────────────────────────────────────

    def _trace_metadata(self, input: Any, config: dict | None) -> dict[str, Any]:
        return {
            "type": self.framework_type,
            "framework": self.framework_type,
            "inputs": input if isinstance(input, dict) else {},
            "thread_id": self._extract_thread_id(config),
        }

    def _finalize(
        self,
        framework_handle: Any,
        config: dict | None,
        handler: Any,
        error: Exception | None,
    ) -> None:
        if self._is_controlled_pause(error):
            handler.spans.close_pending_spans(status="paused")
            return
        if not self._graph_is_done(framework_handle, config) and error is None:
            handler.spans.close_pending_spans(status="paused")
            return
        handler.spans.close_trace(status="error" if error else "success")
