"""``LazyGroup`` — the click ``Group`` that imports its subcommands on demand.

Shared by the root CLI (``pysae_ai_tools.__main__``) and every per-group
``group.py`` module, so a group definition can reference its siblings and the
root without importing ``__main__`` (which would build the whole root app).
"""

import importlib
from typing import Any

import click
import typer


class LazyGroup(click.Group):
    """Click ``Group`` that imports its subcommands on demand.

    ``lazy_subcommands`` maps each CLI name to ``"module.path:attribute"``
    where the attribute is either a :class:`typer.Typer`, a
    :class:`click.Command` (including a nested :class:`LazyGroup`), or a
    typer-compatible function (registered as a single top-level command — its
    arguments become the command's arguments).
    """

    def __init__(
        self,
        *args: Any,
        lazy_subcommands: dict[str, str] | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._lazy = lazy_subcommands or {}

    def list_commands(self, ctx: click.Context) -> list[str]:
        return sorted({*super().list_commands(ctx), *self._lazy})

    def get_command(self, ctx: click.Context, cmd_name: str) -> click.Command | None:
        spec = self._lazy.get(cmd_name)
        if spec is None:
            return super().get_command(ctx, cmd_name)
        module_path, _, attr = spec.partition(":")
        mod = importlib.import_module(module_path)
        obj = getattr(mod, attr)
        if isinstance(obj, typer.Typer):
            return typer.main.get_command(obj)
        if isinstance(obj, click.Command):
            return obj
        # Assume a typer-compatible function: wrap as a single-command Typer
        # and unwrap the inner click command so the function's signature
        # becomes the command's signature directly.
        single = typer.Typer(add_completion=False)
        single.command(name=cmd_name)(obj)
        wrapped = typer.main.get_command(single)
        if isinstance(wrapped, click.Group) and len(wrapped.commands) == 1:
            return next(iter(wrapped.commands.values()))
        return wrapped
