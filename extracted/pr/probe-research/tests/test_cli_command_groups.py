"""Every `probe` group lists its commands in `--help` as before the cli/ split (agent step 14):
a group whose commands sit in several modules states its order in the CommandGroup registry."""

from __future__ import annotations

import importlib
import sys


def _main():
    importlib.import_module("probe.cli.main")
    return sys.modules["probe.cli.main"]


def _typer_groups(app, path=("probe",)):
    """Every Typer app in the tree, by its command path."""
    yield path, app
    for info in app.registered_groups:
        yield from _typer_groups(info.typer_instance, (*path, info.name))


def test_every_registered_group_states_exactly_its_commands_in_order() -> None:
    from probe.cli.commands.commands import COMMAND_GROUPS

    _main()
    assert COMMAND_GROUPS, "the registry is empty"
    for group in COMMAND_GROUPS:
        registered = group.get_registered_names()
        assert registered == list(group.commands), (
            f"{group.typer_app.info.name or 'probe'}: --help order {group.commands} but registered {registered}; "
            "add or remove the command in its CommandGroup")


def test_a_group_whose_commands_sit_in_several_modules_is_registered() -> None:
    """Otherwise its --help order is whatever order those modules happen to load in. A group of
    shared/ (`probe summary`) is ordered by its own door, and shared/ never imports the CLI."""
    from probe.cli.commands.commands import COMMAND_GROUPS

    main = _main()
    registered = {id(group.typer_app) for group in COMMAND_GROUPS}
    for path, app in _typer_groups(main.app):
        modules = {info.callback.__module__ for info in app.registered_commands}
        if len(modules) > 1 and any(module.startswith("probe.cli.") for module in modules):
            assert id(app) in registered, f"`{' '.join(path)}` registers commands from {sorted(modules)}"


def test_putting_a_group_in_order_keeps_an_unlisted_command_after_the_listed_ones() -> None:
    import typer

    from probe.cli.commands.commands import CommandGroup

    app = typer.Typer()
    for command in ("c", "a", "new", "b"):
        app.command(command)(lambda: None)
    CommandGroup(app, ("a", "b", "c")).put_commands_in_order()
    assert [info.name for info in app.registered_commands] == ["a", "b", "c", "new"]


def test_a_command_s_registered_name_is_the_one_typer_gives_it() -> None:
    """commands.py spells `typer.main.get_command_name` rather than import it at every start."""
    from typer.main import get_command_name

    from probe.cli.commands.commands import get_registered_name

    main = _main()
    infos = [info for _path, app in _typer_groups(main.app) for info in app.registered_commands]
    assert len(infos) > 250
    for info in infos:
        assert get_registered_name(info) == (info.name or get_command_name(info.callback.__name__))
