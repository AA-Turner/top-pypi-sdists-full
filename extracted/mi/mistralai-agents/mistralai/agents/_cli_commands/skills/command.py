"""`agents skills add NAME`: install a skill the SDK ships into .agents/skills, for the user's coding agent."""

from __future__ import annotations

from typing import Annotated

import typer
from rich.console import Console

from mistralai.agents._cli_commands import _shared as shared
from mistralai.agents._cli_commands.skills import install

skills_app = typer.Typer(
    help="Install the skills the SDK ships for your coding agent.",
    no_args_is_help=True,
)

_NAMES = ", ".join(install.SKILLS)


@skills_app.command(name="add")
def add_command(
    name: Annotated[str, typer.Argument(metavar="NAME", help=f"The skill to install: {_NAMES}.")],
) -> None:
    """Install a skill the SDK ships into .agents/skills in the current folder, for your coding agent.

    Run it at the root of your project.

    `migrate-1.1` migrates a project from Agents SDK 1.0 or a 1.1 release candidate to 1.1.

    A second run replaces the installed files with the ones of the installed SDK.
    """
    if name not in install.SKILLS:
        raise shared.fail(f"The SDK ships no skill named {name!r}.", f"Choose one of: {_NAMES}.")
    try:
        folder, outcome = install.install(name)
    except OSError as exc:
        raise shared.fail(f"Could not write the skill to {install.SKILLS_DIR}: {exc.strerror or exc}.") from exc
    entry = folder / "SKILL.md"
    message = {
        install.Outcome.ADDED: f"Added {entry}",
        install.Outcome.UPDATED: f"Updated {entry}",
        install.Outcome.UNCHANGED: f"{entry} is up to date",
    }[outcome]
    Console().print(f"[green]✓[/] {message}", highlight=False)
