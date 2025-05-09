from __future__ import annotations

from typing import Any, Callable, Dict, Sequence, TypeVar, overload

import tyro
from tyro._strings import delimeter_context, swap_delimeters
from tyro.constructors import ConstructorRegistry

CallableT = TypeVar("CallableT", bound=Callable)


class SubcommandApp:
    """This class provides a decorator-based API for subcommands in
    :mod:`tyro`, inspired by click. Under-the-hood, this is a light wrapper
    over :func:`tyro.cli`.

    Example:

    .. code-block:: python

        from tyro.extras import SubcommandApp

        app = SubcommandApp()

        @app.command
        def greet(name: str, loud: bool = False):
            '''Greet someone.'''
            greeting = f"Hello, {name}!"
            if loud:
                greeting = greeting.upper()
            print(greeting)

        @app.command(name="addition")
        def add(a: int, b: int):
            '''Add two numbers.'''
            print(f"{a} + {b} = {a + b}")

        if __name__ == "__main__":
            app.cli()

    Usage:

    .. code-block:: bash

        python my_script.py greet Alice
        python my_script.py greet Bob --loud
        python my_script.py addition 5 3

    """

    def __init__(self) -> None:
        self._subcommands: Dict[str, Callable] = {}

    @overload
    def command(self, func: CallableT) -> CallableT: ...

    @overload
    def command(
        self,
        func: None = None,
        *,
        name: str | None = None,
    ) -> Callable[[CallableT], CallableT]: ...

    def command(
        self,
        func: CallableT | None = None,
        *,
        name: str | None = None,
    ) -> CallableT | Callable[[CallableT], CallableT]:
        """A decorator to register a function as a subcommand.

        This method is inspired by Click's ``@cli.command()`` decorator.
        It adds the decorated function to the list of subcommands.

        Args:
            func: The function to register as a subcommand. If None, returns a
                function to use as a decorator.
            name: The name of the subcommand. If None, the name of the function is used.
        """

        def inner(func: CallableT) -> CallableT:
            nonlocal name
            if name is None:
                name = func.__name__

            self._subcommands[name] = func
            return func

        if func is not None:
            return inner(func)
        else:
            return inner

    def cli(
        self,
        *,
        prog: str | None = None,
        description: str | None = None,
        args: Sequence[str] | None = None,
        use_underscores: bool = False,
        console_outputs: bool = True,
        config: Sequence[Any] | None = None,
        sort_subcommands: bool = False,
        registry: ConstructorRegistry | None = None,
    ) -> Any:
        """Run the command-line interface.

        This method creates a CLI using tyro, with all subcommands registered using
        :func:`command()`.

        Args:
            prog: The name of the program printed in helptext. Mirrors argument from
                `argparse.ArgumentParser()`.
            description: Description text for the parser, displayed when the --help flag is
                passed in. If not specified, the class docstring is used. Mirrors argument from
                `argparse.ArgumentParser()`.
            args: If set, parse arguments from a sequence of strings instead of the
                commandline. Mirrors argument from `argparse.ArgumentParser.parse_args()`.
            use_underscores: If True, use underscores as a word delimiter instead of hyphens.
                This primarily impacts helptext; underscores and hyphens are treated equivalently
                when parsing happens. We default helptext to hyphens to follow the GNU style guide.
                https://www.gnu.org/software/libc/manual/html_node/Argument-Syntax.html
            console_outputs: If set to `False`, parsing errors and help messages will be
                suppressed.
            config: Sequence of config marker objects, from `tyro.conf`.
            sort_subcommands: If True, sort the subcommands alphabetically by name.
            registry: A :class:`tyro.constructors.ConstructorRegistry` instance containing custom
                constructor rules.
        """
        assert self._subcommands is not None

        # Sort subcommands by name.
        if sort_subcommands:
            subcommands = dict(sorted(self._subcommands.items(), key=lambda x: x[0]))
        else:
            subcommands = self._subcommands.copy()

        # Replace delimeter in subcommand names.
        with delimeter_context("_" if use_underscores else "-"):
            orig_subcommand_names = list(subcommands.keys())
            for orig_name in orig_subcommand_names:
                subcommands[swap_delimeters(orig_name)] = subcommands.pop(orig_name)

        return tyro.extras.subcommand_cli_from_dict(
            subcommands,
            prog=prog,
            description=description,
            args=args,
            use_underscores=use_underscores,
            console_outputs=console_outputs,
            config=config,
            registry=registry,
        )
