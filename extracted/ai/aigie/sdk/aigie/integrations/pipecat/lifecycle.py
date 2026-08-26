"""Inject the Aigie `PipecatObserver` at `PipelineWorker` construction time.

Pipecat's own supported extension point for monitoring pipeline execution is the
``observers`` constructor kwarg, backed by the synchronous, public
``PipelineWorker.add_observer`` for late registration. Using that keeps us on tier 1 of
this repo's instrumentation preference ranking: we ride the framework's own callback
API rather than inventing one. The only reason a monkey-patch exists at all is that
nothing in Pipecat calls ``add_observer`` on our behalf — auto-instrumentation never
sees the worker object a host application builds, so patching the constructor is the
narrowest reachable seam to get our observer registered through that public API.

``PipelineTask`` is a deprecated subclass of ``PipelineWorker`` (removed in 2.0.0), so
patching ``PipelineWorker.__init__`` alone covers both; patching ``PipelineTask`` too
would double-inject. Do not patch it.

Pipecat's own docs (as of 1.7.0) still show ``PipelineParams(observers=[...])``. That
kwarg was removed from ``PipelineParams`` in 1.0.0 — ``observers`` is a
``PipelineWorker``/``PipelineTask`` constructor kwarg only. Do not "fix" this file to
match the stale docs.
"""

from __future__ import annotations

import functools
import importlib
import logging
from typing import Any

from aigie.tracing.callback_lifecycle import CallbackLifecycle

logger = logging.getLogger(__name__)


class PipecatLifecycle(CallbackLifecycle):
    """Patch/unpatch bookkeeping for the `PipelineWorker.__init__` seam.

    One `PipecatObserver` is created per worker (one per conversation) — there is no
    single "active observer" the way Strands has a shared hook provider, so this class
    intentionally has no `active_observer()` equivalent.
    """

    framework_type = "pipecat"

    def __init__(self) -> None:
        CallbackLifecycle.__init__(self)
        self._emitter: Any = None
        self._config: Any = None
        self._patched_cls: type | None = None

    def configure(self, emitter: Any, config: Any) -> None:
        """Bind the emitter/config the wrapper reads at call time (not closed over)."""
        self._emitter = emitter
        self._config = config

    def _make_observer(self) -> Any:
        from aigie.integrations.pipecat.native_callback import PipecatObserver

        return PipecatObserver(self._emitter, config=self._config)

    def _install_native_hook(self) -> bool:
        cls = self._resolve()
        if cls is None:
            return False
        self._patch_cls(cls)
        return True

    def _uninstall_native_hook(self) -> None:
        if self._patched_cls is not None:
            self._unpatch_cls(self._patched_cls)
            self._patched_cls = None

    def _resolve(self) -> type | None:
        try:
            module = importlib.import_module("pipecat.pipeline.worker")
        except ImportError:
            return None
        return getattr(module, "PipelineWorker", None)

    def _patch_cls(self, cls: type) -> None:
        if getattr(cls.__init__, "_aigie_patched", False):  # type: ignore[misc]
            # Already patched by another lifecycle instance: still record it as
            # ours to patch, or this instance's own uninstall() becomes a silent
            # no-op (it would never see anything to unpatch).
            self._patched_cls = cls
            return
        original = cls.__init__  # type: ignore[misc]
        # Capture the lifecycle instance, not its emitter: `_inject` below reads
        # `lifecycle._emitter`/`_config` fresh on every call, so a later
        # `configure()` (a re-`aigie.init()`) is picked up instead of being frozen
        # at patch time.
        lifecycle = self

        @functools.wraps(original)
        def patched(self_inst: Any, *args: Any, **kwargs: Any) -> None:
            original(self_inst, *args, **kwargs)  # theirs — never inside our try
            try:
                lifecycle._inject(self_inst)
            except Exception as e:  # noqa: BLE001
                logger.debug("pipecat observer injection failed: %s", e)

        patched._aigie_patched = True  # type: ignore[attr-defined]
        cls.__init__ = patched  # type: ignore[method-assign, misc]
        self._patched_cls = cls

    def _unpatch_cls(self, cls: type) -> None:
        if not getattr(cls.__init__, "_aigie_patched", False):  # type: ignore[misc]
            return
        original = getattr(cls.__init__, "__wrapped__", None)  # type: ignore[misc]
        if original is None:
            return  # not ours to restore; leave the host's callable alone
        cls.__init__ = original  # type: ignore[method-assign, misc]

    def _inject(self, worker: Any) -> None:
        existing = _existing_observers(worker)
        if any(getattr(type(o), "_is_aigie_handler", False) for o in existing):
            return  # a user-supplied PipecatObserver, or we already ran
        add = getattr(worker, "add_observer", None)
        if not callable(add):
            # No registration seam reachable: say so loudly rather than pretending
            # we succeeded. A prior version fell back to mutating a throwaway
            # `getattr(worker, "observers", [])` list here, which silently dropped
            # the observer the moment `add_observer` was renamed or removed.
            logger.debug(
                "pipecat: %s has no add_observer; no seam to register our observer",
                type(worker).__name__,
            )
            return
        observer = self._make_observer()
        add(observer)  # public, sync — Pipecat's own registration API
        tracker = getattr(worker, "turn_tracking_observer", None)
        if tracker is not None:
            observer.attach_turn_tracker(tracker)


def _existing_observers(worker: Any) -> list[Any]:
    """Observers already registered on `worker`.

    Duck-typed test doubles expose a plain `.observers` list — the constructor kwarg's
    own name. The real `PipelineWorker` has no such public attribute: the kwarg is
    folded into its internal `WorkerObserver` at `_observer._observers`. Check the
    public shape first, then fall back to the real one.
    """
    public = getattr(worker, "observers", None)
    if public is not None:
        return list(public)
    inner = getattr(worker, "_observer", None)
    return list(getattr(inner, "_observers", None) or [])


_singleton: PipecatLifecycle | None = None


def _get_singleton() -> PipecatLifecycle:
    global _singleton
    if _singleton is None:
        _singleton = PipecatLifecycle()
    return _singleton


def install_pipecat_patches() -> None:
    _get_singleton().install()


def uninstall_pipecat_patches() -> None:
    _get_singleton().uninstall()


__all__ = [
    "PipecatLifecycle",
    "install_pipecat_patches",
    "uninstall_pipecat_patches",
]
