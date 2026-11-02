"""compose() folds a class's parts into its own namespace: at runtime the class is the unsplit one."""

from __future__ import annotations

import functools
import inspect

import pytest

from probe.foundation.compose.compose import compose, fold_parts


class _Reads:
    LIMIT = 3

    def read(self) -> int:
        return self.value * self.LIMIT

    @property
    def doubled(self) -> int:
        return self.value * 2

    @staticmethod
    def name() -> str:
        return "reads"

    @classmethod
    def made(cls) -> str:
        return cls.__name__


class _Writes:
    count: int = 0

    def write(self, value: int) -> None:
        self.value = value
        self.count += 1


@compose
class Thing(_Reads, _Writes):
    """A thing."""

    def __init__(self) -> None:
        self.value = 1


def test_the_composed_class_has_no_parts_at_runtime() -> None:
    assert Thing.__bases__ == (object,)
    assert Thing.__mro__ == (Thing, object)
    assert {"read", "doubled", "name", "made", "write", "LIMIT", "__init__"} <= set(vars(Thing))
    assert Thing.__doc__ == "A thing." and Thing.__qualname__ == "Thing"
    assert inspect.get_annotations(Thing) == {"count": "int"}


def test_members_behave_as_if_defined_in_the_class() -> None:
    thing = Thing()
    thing.write(5)
    assert (thing.read(), thing.doubled, Thing.name(), Thing.made(), thing.count) == (15, 10, "reads", "Thing", 1)
    assert isinstance(vars(Thing)["doubled"], property) and isinstance(vars(Thing)["name"], staticmethod)


def test_a_class_patch_and_its_undo_behave_as_on_an_unsplit_class() -> None:
    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(Thing, "read", lambda self: -1)
        assert Thing().read() == -1
    assert Thing().read() == 3 and "read" in vars(Thing)


def test_a_subclass_overrides_as_usual() -> None:
    class Sub(Thing):
        def read(self) -> int:
            return 0

    assert Sub().read() == 0 and Sub.__mro__ == (Sub, Thing, object)


def test_a_name_in_two_parts_is_refused() -> None:
    class _A:
        def same(self) -> None: ...

    class _B:
        def same(self) -> None: ...

    with pytest.raises(TypeError, match="two parts define 'same'"):
        compose(type("X", (_A, _B), {}))


def test_a_name_in_the_class_and_a_part_is_refused() -> None:
    class _A:
        def same(self) -> None: ...

    with pytest.raises(TypeError, match="in the class and in a part"):
        compose(type("X", (_A,), {"same": lambda self: None}))


def test_a_part_with_its_own_bases_is_refused() -> None:
    class _Base: ...

    class _A(_Base): ...

    with pytest.raises(TypeError, match="has bases of its own"):
        compose(type("X", (_A,), {}))


def test_zero_argument_super_is_refused_even_behind_a_wrapper() -> None:
    def wraps(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            return fn(*args, **kwargs)

        return wrapper

    class _A:
        @wraps
        def method(self) -> None:
            super().method()  # type: ignore[misc]

    with pytest.raises(TypeError, match="zero-argument super"):
        compose(type("X", (_A,), {}))


class Folded:
    """Defined bare; its parts are folded in below, as a module whose parts import it back does."""

    def __init__(self) -> None:
        self.value = 1


EARLY = Folded  # what a part's bottom import binds before the fold
fold_parts(Folded, _Reads, _Writes)


def test_fold_parts_keeps_the_class_object_and_matches_compose() -> None:
    assert EARLY is Folded
    assert Folded.__bases__ == (object,) and Folded.__mro__ == (Folded, object)
    assert set(vars(Thing)) - {"__doc__"} <= set(vars(Folded)) | {"__doc__"}
    assert inspect.get_annotations(Folded) == {"count": "int"}
    folded = Folded()
    folded.write(5)
    assert (folded.read(), folded.doubled, Folded.name(), Folded.made(), folded.count) == (15, 10, "reads", "Folded", 1)


def test_fold_parts_refuses_what_compose_refuses() -> None:
    class Base:
        pass

    class Child(Base):
        pass

    class Clash:
        def read(self) -> int:
            return 0

    class Cell:
        def method(self):
            return __class__

    for parts in ((Child,), (_Reads, Clash), (Cell,)):
        bare = type("Bare", (), {})
        with pytest.raises(TypeError):
            fold_parts(bare, *parts)
