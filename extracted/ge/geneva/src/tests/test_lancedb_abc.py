# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Tests for the lancedb ABC forward-compatibility shim (GEN-913).

Geneva's ``Table`` subclasses a lancedb ABC directly, so a lancedb release
that promotes a new method to ``@abstractmethod`` used to make it
un-instantiable -- surfacing as a ``TypeError`` on a Ray worker rather than
anywhere a test would look.

``Connection`` no longer inherits at all (GEN-914): it composes a lancedb
connection instead, which is a stronger guarantee than the shim provides, and
is covered by its own test below.

Two guarantees are covered here:

* the shim keeps such a class concrete, so only the new operation fails; and
* the conformance tripwire still fails when something is genuinely missing,
  which is what turns the next lancedb bump into a red unit test.
"""

import abc
import subprocess
import sys

import pytest
from lancedb.db import DBConnection

import geneva.db as gdb
from geneva.utils.lancedb_abc import (
    implement_missing_abstracts,
    unimplemented_members,
)


def test_connection_does_not_inherit_from_lancedb() -> None:
    """``Connection`` composes a lancedb connection rather than extending one.

    Inheriting ``DBConnection`` puts Geneva under lancedb's
    ``EnforceOverrides``, which rejects the class outright -- at definition
    time, so ``import geneva`` itself fails -- as soon as lancedb adds a method
    whose name Geneva already uses. That is what ``create_materialized_view``
    in lancedb 0.38 did. Re-adding the base class would reintroduce it, so the
    absence is asserted rather than assumed.
    """
    assert DBConnection not in gdb.Connection.__mro__, (
        "geneva.db.Connection must not inherit from lancedb's DBConnection; "
        "compose one via Connection._connect instead. See GEN-914."
    )


@pytest.mark.skipif(
    not hasattr(DBConnection, "register"),
    reason=(
        "lancedb swaps EnforceOverrides for a no-op stub on Python 3.12+, "
        "leaving DBConnection a plain class with no ABC machinery to register "
        "against -- and no override enforcement to protect against either."
    ),
)
def test_connection_still_registers_as_a_dbconnection() -> None:
    """Dropping the base class must not break callers that type-check."""
    assert issubclass(gdb.Connection, DBConnection)


def test_unimplemented_members_rejects_an_undecorated_class() -> None:
    """A class that never got the decorator must not read as conformant."""

    class Bare:
        pass

    with pytest.raises(AttributeError, match="implement_missing_abstracts"):
        unimplemented_members(Bare)


def _base() -> type:
    """An ABC shaped like lancedb's: methods, a property, an async method."""

    class Base(abc.ABC):
        @abc.abstractmethod
        def implemented(self) -> str: ...

        @abc.abstractmethod
        def missing_method(self, value: int) -> int: ...

        @property
        @abc.abstractmethod
        def missing_property(self) -> str: ...

        @property
        @abc.abstractmethod
        def missing_writable(self) -> str: ...

        @missing_writable.setter
        @abc.abstractmethod
        def missing_writable(self, value: str) -> None: ...

        @abc.abstractmethod
        async def missing_async(self) -> str: ...

    return Base


def test_a_fully_implemented_class_is_untouched() -> None:
    """The common case costs nothing but an empty record."""

    @implement_missing_abstracts
    class Complete(_base()):  # type: ignore[misc]
        def implemented(self) -> str:
            return "ok"

        def missing_method(self, value: int) -> int:
            return value

        @property
        def missing_property(self) -> str:
            return "prop"

        @property
        def missing_writable(self) -> str:
            return "rw"

        @missing_writable.setter
        def missing_writable(self, value: str) -> None:
            self._rw = value

        async def missing_async(self) -> str:
            return "async"

    assert unimplemented_members(Complete) == ()
    assert Complete().implemented() == "ok"
    assert Complete().missing_method(2) == 2
    assert Complete().missing_property == "prop"


def test_missing_members_are_stubbed_and_the_class_stays_concrete() -> None:
    """The failure mode this exists for: construction must still work."""

    @implement_missing_abstracts
    class Partial(_base()):  # type: ignore[misc]
        def implemented(self) -> str:
            return "ok"

    assert unimplemented_members(Partial) == (
        "missing_async",
        "missing_method",
        "missing_property",
        "missing_writable",
    )

    # Constructing is the whole point -- undecorated this raises TypeError.
    instance = Partial()
    # What the class *does* implement keeps working.
    assert instance.implemented() == "ok"


def test_a_stubbed_method_raises_when_called() -> None:
    @implement_missing_abstracts
    class Partial(_base()):  # type: ignore[misc]
        def implemented(self) -> str:
            return "ok"

    with pytest.raises(NotImplementedError) as excinfo:
        Partial().missing_method(1)
    message = str(excinfo.value)
    assert "Partial.missing_method" in message
    assert "lancedb" in message


def test_a_stubbed_property_raises_on_attribute_access() -> None:
    """A property must fail where it is read, not return a bound method."""

    @implement_missing_abstracts
    class Partial(_base()):  # type: ignore[misc]
        def implemented(self) -> str:
            return "ok"

    with pytest.raises(NotImplementedError, match="Partial.missing_property"):
        _ = Partial().missing_property


def test_a_stubbed_writable_property_raises_on_assignment() -> None:
    """The write half of a read/write property must fail the same way.

    A getter-only stub makes Python answer an assignment with a bare
    ``AttributeError: can't set attribute``, naming neither the member nor the
    lancedb version -- so the shim's contract holds on read and quietly breaks
    on write.
    """

    @implement_missing_abstracts
    class Partial(_base()):  # type: ignore[misc]
        def implemented(self) -> str:
            return "ok"

    instance = Partial()
    with pytest.raises(NotImplementedError, match="Partial.missing_writable"):
        _ = instance.missing_writable
    with pytest.raises(NotImplementedError, match="Partial.missing_writable"):
        instance.missing_writable = "x"


def test_a_read_only_property_stays_read_only() -> None:
    """Only a declared setter earns one; the shim does not invent write access."""

    @implement_missing_abstracts
    class Partial(_base()):  # type: ignore[misc]
        def implemented(self) -> str:
            return "ok"

    assert Partial.missing_property.fset is None
    assert Partial.missing_writable.fset is not None


def test_an_undecorated_subclass_does_not_inherit_conformance() -> None:
    """The guard must ask this class, not its ancestors.

    ``hasattr`` walks the MRO, so an undecorated subclass would report its
    parent's record while carrying a new abstract member of its own -- reading
    as conformant despite not being constructible at all.
    """

    @implement_missing_abstracts
    class Decorated(_base()):  # type: ignore[misc]
        def implemented(self) -> str:
            return "ok"

    class Sub(Decorated):
        @abc.abstractmethod
        def brand_new(self) -> str: ...

    # Genuinely broken: the subclass cannot be instantiated.
    assert Sub.__abstractmethods__ == frozenset({"brand_new"})
    with pytest.raises(TypeError, match="abstract"):
        Sub()

    # So the tripwire must refuse to answer for it.
    with pytest.raises(AttributeError, match="implement_missing_abstracts"):
        unimplemented_members(Sub)


async def test_a_stubbed_async_method_raises_when_awaited() -> None:
    """An async member stays awaitable so callers fail at the await."""

    @implement_missing_abstracts
    class Partial(_base()):  # type: ignore[misc]
        def implemented(self) -> str:
            return "ok"

    with pytest.raises(NotImplementedError, match="Partial.missing_async"):
        await Partial().missing_async()


# A method name no Geneva version has ever implemented, standing in for
# whatever lancedb adds next. Injected into the real ABC in a subprocess so
# the mutation cannot leak into other tests.
_WORKER_IMPORT_WITH_AN_UNKNOWN_ABSTRACT_METHOD = r"""
import abc

from lancedb.table import Table as LanceTable


@abc.abstractmethod
def a_method_from_a_future_lancedb(self, *args, **kwargs):
    raise NotImplementedError


LanceTable.a_method_from_a_future_lancedb = a_method_from_a_future_lancedb
abc.update_abstractmethods(LanceTable)

import geneva.table as gt
from geneva.utils.lancedb_abc import unimplemented_members

# The shim must have noticed, and recorded it for the conformance test.
missing = unimplemented_members(gt.Table)
assert missing == ("a_method_from_a_future_lancedb",), missing

# The break this fixes: constructing a Table at all.
gt.Table.__init__ = lambda self, *args, **kwargs: None
table = gt.Table(None, "test")

# Only the unknown operation is unavailable.
try:
    table.a_method_from_a_future_lancedb()
except NotImplementedError as exc:
    assert "a_method_from_a_future_lancedb" in str(exc), exc
else:
    raise AssertionError("the stub did not raise")
"""


def test_an_unknown_future_abstract_method_keeps_table_usable() -> None:
    """The regression GEN-913 is about, with a name nothing hardcodes.

    ``test_worker_import_is_compatible_with_new_table_abc`` covers methods
    already known to exist. This covers the case that actually bites: a method
    added by a future lancedb, which no list in this repo can name in advance.
    """
    proc = subprocess.run(
        [sys.executable, "-c", _WORKER_IMPORT_WITH_AN_UNKNOWN_ABSTRACT_METHOD],
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert proc.returncode == 0, proc.stderr
