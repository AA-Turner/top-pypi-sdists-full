"""Per-call dispatch between the v4 and v3 implementations.

``configure(kane_version=...)`` picks the mode ("v4" by default, "v3" opt-in).
Every public name that differs by mode is served by the mode's implementation
package (``testmu._v4`` / ``testmu._v3``). The choice happens on EACH call, not
at import: generated tests bind names (``from testmu import var, set_var``,
``from testmu import Condition``) at the top of the file, before they call
``configure``. So what ``testmu`` exports are small forwarders:

- functions  -> a sync/async forwarder matching the real function's kind
- classes    -> a proxy class (construction, attributes, ``isinstance``)
                that forwards to the mode's class. Only classes that really
                differ by mode are routed (``Condition``, ``ResolvedCondition``);
                identical ones (enums, DevTools records, ``ClipboardStore``) live
                in the shared layer and are exported as the real class.
- objects    -> a forwarding proxy (``expect`` and its ``.set_options``)

Shared names (``configure``, ``step``, the exceptions, the shared classes)
don't go through here: there is only one of each.

The router also owns the heal patch on Playwright's ``Locator``: one trampoline
per method, installed once, that hands off to the active mode's heal wrapper.
"""
from __future__ import annotations

import functools
import importlib
import inspect
import logging
import sys
from types import ModuleType
from typing import Any

from testmu import _configure

_log = logging.getLogger("testmu")

# mode -> implementation package.
_IMPLS = {
    "v4": "testmu._v4",
    "v3": "testmu._v3",
}

# Every public name served per mode. Order doesn't matter; the set is pinned
# by tests/shared/test_router.py.
ROUTED_NAMES = (
    # lifecycle
    "test", "run",
    # variables
    "var", "set_var", "get_variable_value",
    # assertions / conditions
    "expect", "verify_assertion", "verify_schema_assertion", "evaluate_branch", "route_failure",
    "Condition", "ResolvedCondition",
    "check_until_condition", "evaluate_math", "derive", "condition_compute",
    # locators / actions
    "locator", "resolve_ranked_locator", "as_text",
    "click_drag", "drag_drop", "element_drag", "multi_click", "long_press",
    "scroll_until_element", "prime_dialog",
    # tabs
    "new_tab", "switch_tab", "close_tab", "ensure_active_page",
    # AI helpers
    "vision_query", "textual_query", "vision_wait", "vision_action",
    "get_vision_coordinates", "textual_analyzer", "smartui_snapshot",
    # execution
    "execute_js", "execute_api", "execute_db", "execute_kane_cli",
    "get_api_call_log", "clear_api_call_log",
    # network / devtools
    "network_query", "evaluate_network_assertion",
    "devtools_network_query", "devtools_console_query", "devtools_cookies_query",
    "devtools_storage_query", "api_calls_query",
    "devtoolsNetworkQuery", "devtoolsConsoleQuery", "devtoolsCookiesQuery",
    "devtoolsStorageQuery", "devtoolsPerformanceQuery", "snapshotPerformanceTrace",
    # clipboard
    "install_clipboard", "devtools_clipboard_query",
    "clipboardWrite", "clipboardPaste", "clipboardClear", "devtoolsClipboardQuery",
    # misc
    "downloads_path", "get_cookies",
)


# --- mode selection ------------------------------------------------------------

def mode() -> str:
    """The active mode: "v3" when configured so, else "v4"."""
    return "v3" if _configure.get("kane_version", "v4") == "v3" else "v4"


def impl() -> ModuleType:
    """The implementation package for the active mode (read per call)."""
    name = _IMPLS[mode()]
    module = sys.modules.get(name)
    return module if module is not None else importlib.import_module(name)


def load_impls() -> list[ModuleType]:
    """Import every implementation package. Called once from ``testmu``'s
    ``__init__`` so each mode's import-time behavior (env reads, registries)
    happens at ``import testmu``, exactly as before the split."""
    return [importlib.import_module(n) for n in dict.fromkeys(_IMPLS.values())]


def loaded_impls() -> list[ModuleType]:
    """The implementation packages imported so far, without importing more."""
    return [sys.modules[n] for n in dict.fromkeys(_IMPLS.values()) if n in sys.modules]


# --- forwarders ----------------------------------------------------------------

def _forward_function(name: str, template: Any):
    async def routed_async(*args, **kwargs):
        return await getattr(impl(), name)(*args, **kwargs)

    def routed_sync(*args, **kwargs):
        return getattr(impl(), name)(*args, **kwargs)

    routed = routed_async if inspect.iscoroutinefunction(template) else routed_sync
    functools.update_wrapper(routed, template)
    routed.__module__ = "testmu"
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
                    f"testmu.{base._testmu_routed} is chosen per mode when called "
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
        return f"<routed class testmu.{cls._testmu_routed}>"


def _forward_class(name: str, template: type):
    return _RoutedClass(name, (), {
        "_testmu_routed": name,
        "__doc__": template.__doc__,
        "__module__": "testmu",
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
        return f"<routed testmu.{self._testmu_routed}: {self._target()!r}>"


def forwarder(name: str) -> Any:
    """Build the forwarder for ``name`` from the v4 implementation's object,
    which fixes its kind (the v3 object must have the same kind; see tests)."""
    template = getattr(importlib.import_module(_IMPLS["v4"]), name)
    if inspect.isclass(template):
        return _forward_class(name, template)
    if inspect.isfunction(template) or inspect.isbuiltin(template):
        return _forward_function(name, template)
    return _RoutedObject(name)


def build_public_namespace() -> dict[str, Any]:
    return {name: forwarder(name) for name in ROUTED_NAMES}


# --- heal patch ----------------------------------------------------------------

def _heal_trampoline(method: str, original):
    """Replace ``Locator.<method>`` once; each call runs the active mode's own
    heal wrapper, built by that mode's ``_heal_patch._make_wrapper`` around the
    same original method."""
    wrappers: dict[str, Any] = {}

    def wrapper_for(module: ModuleType):
        w = wrappers.get(module.__name__)
        if w is None:
            if method in module.playwright_async.HEAL_METHODS:
                w = module._heal_patch._make_wrapper(
                    method, original, module.playwright_async._default_heal)
            else:
                w = original
            wrappers[module.__name__] = w
        return w

    # Build now for every loaded mode, like the old import-time install did.
    for module in loaded_impls():
        wrapper_for(module)

    @functools.wraps(original)
    async def routed(self, *args, **kwargs):
        return await wrapper_for(impl())(self, *args, **kwargs)

    setattr(routed, "_testmu_heal_wrapped", True)
    setattr(routed, "_testmu_heal_router", True)
    return routed


async def _routed_long_press(self, *, duration, variables=None):
    """``Locator.long_press`` (selector-bound long press the generator emits as
    ``await _loc_N.long_press(duration=...)``), served by the active mode."""
    return await impl()._helpers.gesture.long_press(
        self, duration=duration, variables=variables)


_routed_long_press.__name__ = "long_press"
setattr(_routed_long_press, "_testmu_gesture_method", True)


def install_heal() -> None:
    """Install the heal trampolines and ``Locator.long_press`` once.
    Idempotent. Never raises: heal is best-effort, as before the split."""
    try:
        from playwright.async_api import Locator
    except ModuleNotFoundError:
        _log.warning("playwright not installed — heal patch skipped, continuing without heal")
        return
    except ImportError as e:
        # playwright present but a transitive dep failed to load (e.g. greenlet DLL on Windows)
        _log.warning("playwright internals failed to load (%s) — heal patch skipped, continuing without heal", e)
        return
    try:
        methods = list(dict.fromkeys(
            m for module in loaded_impls() for m in module.playwright_async.HEAL_METHODS))
        for method in methods:
            try:
                original = getattr(Locator, method, None)
                if original is None:
                    _log.debug("heal patch: Locator.%s not present, skipping", method)
                    continue
                if getattr(original, "_testmu_heal_wrapped", False):
                    continue  # idempotent — re-import won't double-wrap
                setattr(Locator, method, _heal_trampoline(method, original))
            except Exception as e:
                _log.warning("heal patch: failed to wrap Locator.%s (%s) — skipping", method, e)
        if getattr(Locator, "long_press", None) is None:
            setattr(Locator, "long_press", _routed_long_press)
        _log.debug("Heal patch installed on Locator")
    except Exception as e:
        _log.warning("heal patch installation failed (%s) — continuing without heal", e)


# --- configure() support ---------------------------------------------------------

def active_vars() -> ModuleType:
    """The active mode's variable module (``configure`` fills its stores)."""
    return impl()._vars
