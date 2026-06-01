"""Unit tests."""

from typing import Annotated

import pytest
import typer
from typer.testing import CliRunner

from typer_injector import Depends, InjectingTyper
from typer_injector.exceptions import CircularDependencyError, ParameterNameConflictError, TyperInjectorError


def test_simple_dependency() -> None:
    """Test a simple dependency."""
    app = InjectingTyper()

    def simple_dependency(a: Annotated[str, typer.Option()], b: Annotated[int, typer.Option()]) -> tuple[str, int]:
        return a, b

    @app.command()
    def cmd(dep: Annotated[tuple[str, int], Depends(simple_dependency)]) -> tuple[str, int]:
        return dep

    runner = CliRunner()

    assert runner.invoke(
        app,
        ['--a', 'hello', '--b', '1337'],
        standalone_mode=False,
    ).return_value == ('hello', 1337)


def test_argument_dependency() -> None:
    """Test a dependency with positional arguments."""
    app = InjectingTyper()

    def simple_dependency(a: str, b: int) -> tuple[str, int]:
        return a, b

    @app.command()
    def cmd(dep: Annotated[tuple[str, int], Depends(simple_dependency)], c: str) -> tuple[tuple[str, int], str]:
        return dep, c

    runner = CliRunner()

    assert runner.invoke(
        app,
        ['hello', '1337', 'world'],
        standalone_mode=False,
    ).return_value == (('hello', 1337), 'world')


def test_dependency_in_callback() -> None:
    """Test a dependency in a command callback."""
    app = InjectingTyper()

    def simple_dependency(a: Annotated[str, typer.Option()], b: Annotated[int, typer.Option()]) -> tuple[str, int]:
        return a, b

    @app.callback()
    def callback(dep: Annotated[tuple[str, int], Depends(simple_dependency)]) -> None:
        assert dep == ('hello', 1337)

    @app.command()
    def cmd() -> None:
        pass

    runner = CliRunner()

    assert runner.invoke(
        app,
        ['--a', 'hello', '--b', '1337', 'cmd'],
        catch_exceptions=False,
    )


def test_stringified_annotations() -> None:
    """Test a command with stringified annotations."""
    app = InjectingTyper()

    global simple_dependency  # necessary for evaluation of string annotation

    def simple_dependency(a: 'Annotated[str, typer.Option()]', b: 'Annotated[int, typer.Option()]') -> 'tuple[str, int]':
        return a, b

    @app.command()
    def cmd(dep: 'Annotated[tuple[str, int], Depends(simple_dependency)]') -> 'tuple[str, int]':
        return dep

    runner = CliRunner()

    assert runner.invoke(
        app,
        ['--a', 'hello', '--b', '1337'],
        standalone_mode=False,
    ).return_value == ('hello', 1337)


def test_nested_dependency() -> None:
    """Test a nested dependency."""
    app = InjectingTyper()

    def inner_dependency(a: Annotated[str, typer.Option()], b: Annotated[int, typer.Option()]) -> tuple[str, int]:
        return a, b

    def outer_dependency(
        inner: Annotated[tuple[str, int], Depends(inner_dependency)],
        c: Annotated[bool, typer.Option()],
    ) -> tuple[tuple[str, int], float]:
        return inner, c

    @app.command()
    def cmd(dep: Annotated[tuple[str, int, float], Depends(outer_dependency)]) -> tuple[str, int, float]:
        return dep

    runner = CliRunner()

    assert runner.invoke(
        app,
        ['--a', 'hello', '--b', '1337', '--c'],
        standalone_mode=False,
    ).return_value == (
        ('hello', 1337),
        True,
    )


def test_dendency_caching() -> None:
    """Test dependency caching."""
    app = InjectingTyper()

    def obj_dependency() -> object:
        return object()

    @app.command()
    def cmd(
        dep1: Annotated[object, Depends(obj_dependency)],
        dep2: Annotated[object, Depends(obj_dependency)],
    ) -> tuple[object, object]:
        return dep1, dep2

    runner = CliRunner()

    result = runner.invoke(
        app,
        [],
        standalone_mode=False,
    ).return_value

    assert result[0] is result[1]


def test_parameter_conflict() -> None:
    """Test that parameter conflict raises an error."""
    app = InjectingTyper()

    def conflicting_dependency(a: Annotated[str, typer.Option()]) -> str:
        return a  # pragma: no cover

    with pytest.raises(ParameterNameConflictError):

        @app.command()
        def cmd(
            a: Annotated[str, typer.Option()],
            dep: Annotated[str, Depends(conflicting_dependency)],
        ) -> None:
            pass  # pragma: no cover


def test_typer_context_parameter_conflict() -> None:
    """Test that parameter conflict does not raise an error when both are `typer.Context`."""
    app = InjectingTyper()

    def conflicting_dependency(ctx: typer.Context) -> typer.Context:
        return ctx

    @app.command()
    def cmd(
        ctx: typer.Context,
        dep: Annotated[typer.Context, Depends(conflicting_dependency)],
    ) -> None:
        assert dep is ctx

    runner = CliRunner()

    assert runner.invoke(
        app,
        [],
        catch_exceptions=False,
    )


def test_circular_dependency() -> None:
    """Test that circular dependency raises an error."""
    app = InjectingTyper()

    global dep_b  # necessary for evaluation of forward reference

    def dep_a(b: 'Annotated[str, Depends(dep_b)]') -> str:
        return b  # pragma: no cover

    def dep_b(a: Annotated[str, Depends(dep_a)]) -> str:
        return a  # pragma: no cover

    with pytest.raises(CircularDependencyError):

        @app.command()
        def cmd(
            dep: Annotated[str, Depends(dep_a)],
        ) -> None:
            pass  # pragma: no cover


def test_positional_only_parameter() -> None:
    """Test that positional-only parameters in dependencies raise an error."""
    app = InjectingTyper()

    def pos_only_dependency(a: str, /) -> str:
        return a  # pragma: no cover

    with pytest.raises(TyperInjectorError, match=r'Positional-only parameter'):

        @app.command()
        def cmd(
            dep: Annotated[str, Depends(pos_only_dependency)],
        ) -> None:
            pass  # pragma: no cover
