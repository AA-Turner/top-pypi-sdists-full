"""Inject the shared Strands hook provider at construction time."""

from __future__ import annotations

import functools
import importlib
import logging
from typing import Any

from aigie.tracing.callback_lifecycle import CallbackLifecycle

logger = logging.getLogger(__name__)

_PATCH_TARGETS = [
    ("strands", "Agent"),
    ("strands.multiagent.swarm", "Swarm"),
    ("strands.multiagent.graph", "Graph"),
]


class StrandsLifecycle(CallbackLifecycle):
    framework_type = "strands"

    def __init__(self) -> None:
        CallbackLifecycle.__init__(self)
        self._emitter: Any = None
        self._config: Any = None
        self._provider: Any = None
        self._originals: list[tuple[type, str, Any]] = []

    def configure(self, emitter: Any, config: Any) -> None:
        """Bind the emitter and config before installing the constructor patches."""
        self._emitter = emitter
        self._config = config

    def _get_provider(self) -> Any:
        if self._provider is None:
            from aigie.integrations.strands.native_callback import StrandsHookProvider

            self._provider = StrandsHookProvider(self._emitter, config=self._config)
        return self._provider

    def _install_native_hook(self) -> bool:
        provider = self._get_provider()
        patched_any = False
        for module_path, cls_name in _PATCH_TARGETS:
            cls = self._resolve(module_path, cls_name)
            if cls is None:
                continue
            self._patch_init(cls, provider)
            patched_any = True
        return patched_any

    def _resolve(self, module_path: str, cls_name: str) -> type | None:
        try:
            module = importlib.import_module(module_path)
            return getattr(module, cls_name, None)
        except ImportError:
            return None

    def _patch_init(self, cls: type, provider: Any) -> None:
        original = cls.__init__  # type: ignore[misc]
        if getattr(original, "_aigie_patched", False):
            return

        @functools.wraps(original)
        def patched(self_inst: Any, *args: Any, **kwargs: Any) -> None:
            original(self_inst, *args, **kwargs)
            _inject(self_inst, provider)

        patched._aigie_patched = True  # type: ignore[attr-defined]
        self._originals.append((cls, "__init__", original))
        cls.__init__ = patched  # type: ignore[assignment, misc]

    def _uninstall_native_hook(self) -> None:
        for cls, attr, original in self._originals:
            setattr(cls, attr, original)
        self._originals.clear()
        self._provider = None


def _inject(instance: Any, provider: Any) -> None:
    registry = getattr(instance, "hooks", None)
    if registry is None:
        return
    if _already_registered(registry):
        return
    try:
        registry.add_hook(provider)
    except Exception:  # noqa: BLE001 - never break agent construction
        logger.debug("aigie: failed to inject Strands hook provider", exc_info=True)


def _already_registered(registry: Any) -> bool:
    callbacks = getattr(registry, "_registered_callbacks", {})
    for cbs in callbacks.values():
        for entry in cbs:
            cb = getattr(entry, "callback", entry)
            if getattr(getattr(cb, "__self__", None), "_is_aigie_handler", False):
                return True
    return False


_singleton: StrandsLifecycle | None = None


def _get_singleton() -> StrandsLifecycle:
    global _singleton
    if _singleton is None:
        _singleton = StrandsLifecycle()
    return _singleton


def install_strands_patches() -> None:
    _get_singleton().install()


def uninstall_strands_patches() -> None:
    _get_singleton().uninstall()


__all__ = [
    "StrandsLifecycle",
    "install_strands_patches",
    "uninstall_strands_patches",
]
