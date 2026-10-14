"""Per-call dispatch between runtime-mode implementations.

``configure(kane_version=...)`` picks the mode. Mobile export is v4-only today
(``configure`` rejects anything else), so both slots point at
``testmu_appium._v4``; a v3 implementation plugs in as ``testmu_appium._v3``.
The shape mirrors testmu._router in the Playwright binding: every public name
that differs by mode is served by the mode's package on EACH call, because
generated tests bind names before they call ``configure``:

- functions  -> a sync/async forwarder matching the real function's kind
- classes    -> a proxy class (construction, attributes, ``isinstance``)
- mappings   -> a read-only mapping proxy (``ELEMENT_CONTRACT``)

Shared names (``configure``, ``step``, the exceptions) don't go through here.
"""
from __future__ import annotations

import collections.abc
import functools
import importlib
import inspect
import sys
from types import ModuleType
from typing import Any

from testmu_appium import _config

# mode -> implementation package.
_IMPLS = {
    "v4": "testmu_appium._v4",
    "v3": "testmu_appium._v4",  # no v3 implementation yet; configure rejects v3
}

# Every public name served per mode (pinned by tests/shared/test_router.py).
ROUTED_NAMES = (
    "test_config_overrides", "test", "run", "open_session", "close_session",
    "var", "set_var", "get_variable_value", "resolve_variable",
    "route_failure", "get_driver",
    "parse_tree", "format_for_prompt", "find_by_fingerprint", "position_hint",
    "ELEMENT_CONTRACT",
    "click", "type", "search", "clear", "select", "scroll", "scroll_until",
    "navigate", "keyevent", "app_lifecycle", "device_control", "device_control_query",
    "set_geolocation", "wait", "drag", "smartui_screenshot",
    "set_cookies", "delete_cookies", "clear_cookies",
    "set_local_storage", "delete_local_storage", "clear_local_storage",
    "set_clipboard", "paste_clipboard", "clear_clipboard",
    "go_back", "go_forward", "refresh", "accessibility_scan",
    "get_tabs", "new_tab", "switch_tab", "close_tab",
    "inject_media", "network_throttle", "network_mock",
    "verify_assertion", "verify_schema_assertion", "evaluate_math", "assertion", "evaluate_branch", "math",
    "textual_query", "vision_query", "check_until_condition", "execute_kane_cli",
    "execute_api", "execute_js", "execute_db", "network_query", "network_capture_query",
    "network_capture_capabilities", "evaluate_network_assertion",
    "textual_analyzer", "textual_analyzer_authoring",
    "HealHit", "HealNoMatch", "HealUnavailable", "HealDisabled", "HealProtocolError",
    "capture_action_timings",
)


def mode() -> str:
    """The active mode: "v3" when configured so, else "v4"."""
    return "v3" if _config.get("kane_version", "v4") == "v3" else "v4"


def impl() -> ModuleType:
    """The implementation package for the active mode (read per call)."""
    name = _IMPLS[mode()]
    module = sys.modules.get(name)
    return module if module is not None else importlib.import_module(name)


def load_impls() -> list[ModuleType]:
    """Import every implementation package (from ``testmu_appium/__init__``),
    so import-time behavior happens at ``import testmu_appium`` as before."""
    return [importlib.import_module(n) for n in dict.fromkeys(_IMPLS.values())]


def loaded_impls() -> list[ModuleType]:
    return [sys.modules[n] for n in dict.fromkeys(_IMPLS.values()) if n in sys.modules]


def _forward_function(name: str, template: Any):
    async def routed_async(*args, **kwargs):
        return await getattr(impl(), name)(*args, **kwargs)

    def routed_sync(*args, **kwargs):
        return getattr(impl(), name)(*args, **kwargs)

    routed = routed_async if inspect.iscoroutinefunction(template) else routed_sync
    functools.update_wrapper(routed, template)
    routed.__module__ = "testmu_appium"
    setattr(routed, "_testmu_routed", name)
    return routed


class _RoutedClass(type):
    """Metaclass of the proxy classes ``testmu`` exports for per-mode classes.

    A proxy has no real base, so a subclass of it couldn't inherit the mode's
    methods: subclassing raises instead of building the wrong object.
    """

    def __new__(mcs, name, bases, namespace):
        for base in bases:
            if isinstance(base, _RoutedClass):
                raise TypeError(
                    f"testmu_appium.{base._testmu_routed} is chosen per mode when called "
                    f"(configure(kane_version=...)) and can't be subclassed")
        return super().__new__(mcs, name, bases, namespace)

    def _target(cls):
        return getattr(impl(), cls._testmu_routed)

    def __call__(cls, *args, **kwargs):
        return cls._target()(*args, **kwargs)

    def __getattr__(cls, attr):
        return getattr(cls._target(), attr)

    def __instancecheck__(cls, obj):
        return any(isinstance(obj, getattr(m, cls._testmu_routed)) for m in loaded_impls())

    def __subclasscheck__(cls, sub):
        return any(issubclass(sub, getattr(m, cls._testmu_routed)) for m in loaded_impls())

    def __repr__(cls):
        return f"<routed class testmu_appium.{cls._testmu_routed}>"


def _forward_class(name: str, template: type):
    return _RoutedClass(name, (), {
        "_testmu_routed": name,
        "__doc__": template.__doc__,
        "__module__": "testmu_appium",
        "__qualname__": name,
    })


class _RoutedObject:
    """Forwarding proxy for a public object that is neither a function nor a
    class (``expect``: callable, with methods like ``set_options``)."""

    __slots__ = ("_testmu_routed",)

    def __init__(self, name: str):
        object.__setattr__(self, "_testmu_routed", name)

    def _target(self):
        return getattr(impl(), self._testmu_routed)

    def __call__(self, *args, **kwargs):
        return self._target()(*args, **kwargs)

    def __getattr__(self, attr):
        return getattr(self._target(), attr)

    def __repr__(self):
        return f"<routed testmu_appium.{self._testmu_routed}: {self._target()!r}>"


class _RoutedMapping(collections.abc.Mapping):
    """Read-only forwarding proxy for a public mapping constant."""

    def __init__(self, name: str):
        self._testmu_routed = name

    def _target(self):
        return getattr(impl(), self._testmu_routed)

    def __getitem__(self, key):
        return self._target()[key]

    def __iter__(self):
        return iter(self._target())

    def __len__(self):
        return len(self._target())

    def __repr__(self):
        return f"<routed testmu_appium.{self._testmu_routed}: {self._target()!r}>"


def forwarder(name: str) -> Any:
    """Build the forwarder for ``name`` from the v4 implementation's object,
    which fixes its kind (the v3 object must have the same kind; see tests)."""
    template = getattr(importlib.import_module(_IMPLS["v4"]), name)
    if inspect.isclass(template):
        return _forward_class(name, template)
    if inspect.isfunction(template) or inspect.isbuiltin(template):
        return _forward_function(name, template)
    if isinstance(template, collections.abc.Mapping):
        return _RoutedMapping(name)
    return _RoutedObject(name)


def build_public_namespace() -> dict[str, Any]:
    return {name: forwarder(name) for name in ROUTED_NAMES}


def active_vars() -> ModuleType:
    """The active mode's variable module (``configure`` fills its stores)."""
    return impl()._vars


def active_reporter():
    """The active mode's reporter (``step`` reports begin/end through it)."""
    return impl()._reporter.reporter()
