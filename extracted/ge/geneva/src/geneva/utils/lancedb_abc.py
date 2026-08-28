# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Keep Geneva's lancedb ABC subclasses instantiable across lancedb versions.

``geneva.table.Table`` and ``geneva.db.Connection`` subclass lancedb's
``Table`` and ``DBConnection`` *abstract base classes* rather than a concrete
implementation. Whenever lancedb promotes a new method to ``@abstractmethod``,
those classes stop being instantiable on any process that resolves the newer
lancedb::

    TypeError: Can't instantiate abstract class Table with abstract methods
    refresh_column, refresh_column_async

The failure lands wherever a table is first constructed -- in practice a Ray
worker mid-backfill, long after the driver started -- and it takes out *every*
operation, including the ones Geneva does implement.

:func:`implement_missing_abstracts` closes that gap. Applied to a class, it
fills each abstract member the class left unimplemented with a stub that raises
:class:`NotImplementedError` naming the member, then clears
``__abstractmethods__`` so the class stays concrete. A version skew degrades
from "nothing works" to "this one call is unavailable".

This is a safety net, not a substitute for implementing the method. The names
it had to fill are recorded on the class so a test can assert the set is empty
against the pinned lancedb -- see ``src/tests/test_lancedb_abc.py``, which
turns a lancedb bump into a unit-test failure instead of a production one.
"""

from __future__ import annotations

import inspect
import logging
from typing import Any, TypeVar

_LOG = logging.getLogger(__name__)

_ClassT = TypeVar("_ClassT", bound=type)

# Names this class did not implement, as a sorted tuple. Always set, so a
# conformance test can read it without a getattr default that would hide a
# class the decorator was never applied to.
UNIMPLEMENTED_ATTR = "__geneva_unimplemented__"


def _lancedb_version() -> str:
    """Installed lancedb version, or ``"unknown"`` if it cannot be read."""
    try:
        import lancedb

        return str(getattr(lancedb, "__version__", "unknown"))
    except Exception:  # pragma: no cover - lancedb is a hard dependency
        return "unknown"


def _message(owner: str, member: str) -> str:
    """The error a synthesized stub raises."""
    return (
        f"{owner}.{member} is not available. The installed lancedb "
        f"({_lancedb_version()}) requires it, but this version of Geneva does "
        "not implement it. Other operations are unaffected; upgrade Geneva or "
        "pin an earlier lancedb."
    )


def _tag(fn: Any, owner: str, member: str) -> Any:
    """Name a synthesized stub after the member it stands in for.

    Introspection reads these -- including on a property's ``fget``/``fset``,
    which ``help()`` and ``inspect`` reach through. Kept in one place so the
    naming scheme cannot drift between the shapes below.
    """
    fn.__name__ = member
    fn.__qualname__ = f"{owner}.{member}"
    fn.__doc__ = _message(owner, member)
    return fn


def _stub_for(owner: str, member: str, declared: Any) -> Any:
    """Build the replacement for one unimplemented abstract member.

    Mirrors the *shape* the base class declared so callers fail where they
    would have called: a property raises on attribute access, an async method
    raises when awaited, everything else raises on call.
    """
    if isinstance(declared, property):

        def _get(_self: Any) -> Any:
            raise NotImplementedError(_message(owner, member))

        _tag(_get, owner, member)

        # A writable abstract property needs a raising setter too. Without one
        # Python answers an assignment with a bare ``AttributeError: can't set
        # attribute``, which names neither the member nor the version -- the
        # write half of the same failure this getter handles.
        _set = None
        if declared.fset is not None:

            def _raising_set(_self: Any, _value: Any) -> None:
                raise NotImplementedError(_message(owner, member))

            _set = _tag(_raising_set, owner, member)

        return property(_get, _set, doc=_message(owner, member))

    if inspect.iscoroutinefunction(declared):

        async def _async_stub(*_args: Any, **_kwargs: Any) -> Any:
            raise NotImplementedError(_message(owner, member))

        return _tag(_async_stub, owner, member)

    def _stub(*_args: Any, **_kwargs: Any) -> Any:
        raise NotImplementedError(_message(owner, member))

    return _tag(_stub, owner, member)


def implement_missing_abstracts(cls: _ClassT) -> _ClassT:
    """Fill unimplemented abstract members with raising stubs.

    Applied as a class decorator. A class that already implements everything is
    left untouched apart from an empty :data:`UNIMPLEMENTED_ATTR`, so the
    common case costs nothing.
    """
    missing = tuple(sorted(getattr(cls, "__abstractmethods__", frozenset())))
    setattr(cls, UNIMPLEMENTED_ATTR, missing)
    if not missing:
        return cls

    for member in missing:
        # Resolved off ``cls``, which inherits the base's declaration -- the
        # only place the member's shape (property vs method) is recorded.
        declared = inspect.getattr_static(cls, member, None)
        setattr(cls, member, _stub_for(cls.__name__, member, declared))

    # ABCMeta consults this set at instantiation only, so emptying it is what
    # makes the class concrete again.
    cls.__abstractmethods__ = frozenset()  # type: ignore[attr-defined]

    _LOG.warning(
        "%s does not implement %d member(s) required by the installed lancedb "
        "(%s): %s. These operations will raise; everything else works. This "
        "means Geneva and lancedb are out of step -- upgrade Geneva or pin an "
        "earlier lancedb.",
        cls.__name__,
        len(missing),
        _lancedb_version(),
        ", ".join(missing),
    )
    return cls


def unimplemented_members(cls: type) -> tuple[str, ...]:
    """Abstract members ``cls`` left to :func:`implement_missing_abstracts`.

    Empty when the class fully implements its base ABC. Raises if the class was
    never decorated, so a conformance test cannot silently pass on one that
    slipped through.

    Asks ``cls.__dict__`` rather than ``hasattr``: attribute lookup walks the
    MRO, so an *undecorated subclass* of a decorated class would inherit its
    ancestor's record and read as conformant -- while carrying its own new
    abstract member and not being constructible at all. That is precisely the
    silent pass this guard exists to prevent.
    """
    if UNIMPLEMENTED_ATTR not in cls.__dict__:
        raise AttributeError(
            f"{cls.__name__} is not decorated with @implement_missing_abstracts"
        )
    return getattr(cls, UNIMPLEMENTED_ATTR)
