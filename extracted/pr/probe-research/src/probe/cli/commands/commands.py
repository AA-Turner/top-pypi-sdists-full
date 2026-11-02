"""CommandGroup registry: the `--help` order of each group whose commands several pieces
register; click's ClickException/UsageError as the groups catch them."""

from __future__ import annotations

import typer


# Typer vendors its own click (`typer._click`, since 0.13). The standalone `click`
# package is a DIFFERENT module object, so `except click.ClickException` matched
# nothing typer raises and every usage error escaped main() as a traceback instead of
# an exit code — silently, on an unpinned typer bump.
#
# `typer.Exit`/`typer.Abort` are public re-exports of whichever click typer uses.
# ClickException — the base of every usage error (BadParameter, NoSuchOption,
# UsageError, ...) — is not re-exported, but it is reachable from BadParameter's MRO
# under either layout, so resolving it here follows typer rather than pinning to one.
ClickException = next(
    (base for base in typer.BadParameter.__mro__ if base.__name__ == "ClickException"),
    # Never expected; the fallback keeps `import probe.cli` working (a StopIteration at
    # import time would make the whole CLI unusable) and degrades to catching nothing.
    type("_NoClickException", (Exception,), {}),
)
#: UsageError (unknown command, missing argument), resolved the same way:
#: BadParameter's own base under either layout.
UsageError = next(
    (base for base in typer.BadParameter.__mro__ if base.__name__ == "UsageError"),
    type("_NoUsageError", (Exception,), {}),
)


class CommandGroup:
    """A `probe` Typer group and the order `--help` lists its commands in.

    Typer lists a group's commands in registration order. A group whose commands sit in
    several pieces is registered in whatever order the pieces load, so it states its order
    here; cli/main.py puts every registered group in order once all pieces have loaded."""

    def __init__(self, typer_app: typer.Typer, commands: tuple[str, ...]) -> None:
        self.typer_app = typer_app
        self.commands = commands

    def get_registered_names(self) -> list[str]:
        """The names the group's commands are registered under, in registration order."""
        return [get_registered_name(info) for info in self.typer_app.registered_commands]

    def put_commands_in_order(self) -> None:
        """Sort the registered commands into `commands` order; one not listed stays after them."""
        rank = {name: index for index, name in enumerate(self.commands)}
        self.typer_app.registered_commands.sort(key=lambda info: rank.get(get_registered_name(info), len(rank)))


#: Every group that states its order, registered by the module that defines its Typer app.
COMMAND_GROUPS: list[CommandGroup] = []


def register_group(typer_app: typer.Typer, commands: tuple[str, ...]) -> CommandGroup:
    """Add `typer_app`'s `--help` order to the registry (cli/main.py applies it)."""
    group = CommandGroup(typer_app, commands)
    COMMAND_GROUPS.append(group)
    return group


def get_registered_name(info) -> str:
    """The name `--help` lists a registered command under: its own, else Typer's from the function
    (`typer.main.get_command_name`, spelled here: every command's start imports this module)."""
    return info.name or info.callback.__name__.lower().replace("_", "-")
