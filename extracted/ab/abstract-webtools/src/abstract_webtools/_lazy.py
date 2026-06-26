"""Lazy-import helpers — keep ``import abstract_webtools`` light.

This package historically funneled every dependency through one shared import hub
(``from ..imports import *``), so importing *anything* eagerly pulled the heaviest
optional deps (opencv, moviepy, pytesseract, pdf2image, pydub, speech_recognition,
selenium, playwright, …). That makes the package slow to import and impossible to
install on lean targets (e.g. Termux/Android) that can't build those wheels.

These two proxies let the hub keep exposing the same names while deferring the real
import to first use. A proxy is cheap to construct and never imports its target at
module-load time, so ``import abstract_webtools`` no longer requires the heavy deps
to be installed at all — only features that actually use them do.

    cv2 = LazyModule("cv2")                       # cv2.imread(...)  -> imports cv2 on first attr access
    Options = LazyAttr("selenium...options", "Options")  # Options() -> imports + calls on first use
"""
from __future__ import annotations

import importlib


class LazyModule:
    """Stand-in for ``import pkg`` / ``import pkg.sub as name``.

    Imports the underlying module on first attribute access, then delegates. Use
    for deps referenced in qualified form (``np.array``, ``cv2.imread``, ``EC.x``).
    """

    __slots__ = ("_lazy_name", "_lazy_mod")

    def __init__(self, name: str):
        object.__setattr__(self, "_lazy_name", name)
        object.__setattr__(self, "_lazy_mod", None)

    def _resolve(self):
        mod = object.__getattribute__(self, "_lazy_mod")
        if mod is None:
            mod = importlib.import_module(object.__getattribute__(self, "_lazy_name"))
            object.__setattr__(self, "_lazy_mod", mod)
        return mod

    def __getattr__(self, attr):
        return getattr(self._resolve(), attr)

    def __dir__(self):
        return dir(self._resolve())

    def __repr__(self):
        loaded = object.__getattribute__(self, "_lazy_mod") is not None
        return "<LazyModule %r (%s)>" % (
            object.__getattribute__(self, "_lazy_name"),
            "loaded" if loaded else "deferred",
        )


class LazyAttr:
    """Stand-in for ``from pkg import name``.

    Imports ``pkg`` and resolves ``name`` on first use. Transparent for both
    attribute access (``Cls.attr``) and calls (``fn(...)`` / ``Cls(...)``), so it
    substitutes for functions and classes alike.
    """

    __slots__ = ("_lazy_pkg", "_lazy_name", "_lazy_obj", "_lazy_done")

    def __init__(self, pkg: str, name: str):
        object.__setattr__(self, "_lazy_pkg", pkg)
        object.__setattr__(self, "_lazy_name", name)
        object.__setattr__(self, "_lazy_obj", None)
        object.__setattr__(self, "_lazy_done", False)

    def _resolve(self):
        if not object.__getattribute__(self, "_lazy_done"):
            mod = importlib.import_module(object.__getattribute__(self, "_lazy_pkg"))
            obj = getattr(mod, object.__getattribute__(self, "_lazy_name"))
            object.__setattr__(self, "_lazy_obj", obj)
            object.__setattr__(self, "_lazy_done", True)
        return object.__getattribute__(self, "_lazy_obj")

    def __getattr__(self, attr):
        return getattr(self._resolve(), attr)

    def __call__(self, *args, **kwargs):
        return self._resolve()(*args, **kwargs)

    def __dir__(self):
        return dir(self._resolve())

    def __repr__(self):
        done = object.__getattribute__(self, "_lazy_done")
        return "<LazyAttr %s.%s (%s)>" % (
            object.__getattribute__(self, "_lazy_pkg"),
            object.__getattribute__(self, "_lazy_name"),
            "loaded" if done else "deferred",
        )


class LazyValue:
    """Defers a zero-arg factory call until first use.

    For module-level *side effects* that need a heavy dep — e.g.
    ``ENC = tiktoken.get_encoding("cl100k_base")`` or a pre-built Selenium
    ``Options()`` — assigning ``LazyValue(factory)`` keeps the name a real module
    global (so ``from … import *`` still carries it) while doing the actual work,
    and the heavy import, only when the value is first touched. Transparent for
    attribute access, calls, and indexing, so it stands in for the built object.
    """

    __slots__ = ("_lazy_factory", "_lazy_val", "_lazy_done")

    def __init__(self, factory):
        object.__setattr__(self, "_lazy_factory", factory)
        object.__setattr__(self, "_lazy_val", None)
        object.__setattr__(self, "_lazy_done", False)

    def _resolve(self):
        if not object.__getattribute__(self, "_lazy_done"):
            val = object.__getattribute__(self, "_lazy_factory")()
            object.__setattr__(self, "_lazy_val", val)
            object.__setattr__(self, "_lazy_done", True)
        return object.__getattribute__(self, "_lazy_val")

    def __getattr__(self, attr):
        return getattr(self._resolve(), attr)

    def __call__(self, *args, **kwargs):
        return self._resolve()(*args, **kwargs)

    def __getitem__(self, key):
        return self._resolve()[key]

    def __dir__(self):
        return dir(self._resolve())
