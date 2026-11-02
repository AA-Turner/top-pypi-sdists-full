"""`agents init`: create a new agent project that `agents deploy` deploys in one step.

The command only renders: `project` checks and writes the files, `uv` locks them, `git` commits them.
"""

from __future__ import annotations

from pathlib import Path
from typing import Annotated, Literal

import typer
from rich.console import Console
from rich.padding import Padding
from rich.panel import Panel
from rich.syntax import Syntax
from rich.text import Text

from mistralai.agents._cli_commands import _shared as shared
from mistralai.agents._cli_commands.init import api_key, git, project, uv


def init_command(
    name_argument: Annotated[
        str | None,
        typer.Argument(metavar="NAME", help="Agent name. The project is created in a new folder of that name."),
    ] = None,
    name: Annotated[str | None, typer.Option("--name", help="Agent name, as the NAME argument.")] = None,
    yes: Annotated[
        bool,
        typer.Option(
            "--yes", "-y", help="Install uv if it is missing, and commit the project in a new git repository."
        ),
    ] = False,
    no_git: Annotated[bool, typer.Option("--no-git", help="Do not create a git repository.")] = False,
    exempt_from_exclude_newer: Annotated[
        bool,
        typer.Option(
            "--exempt-from-exclude-newer",
            help="Exempt the SDK from your uv `exclude-newer` cutoff, which would hide a recent release.",
        ),
    ] = False,
) -> None:
    """Create a new agent project that `agents deploy` deploys in one step."""
    if name is not None and name_argument is not None and name != name_argument:
        raise shared.fail(f"Two names were given, {name_argument!r} and {name!r}. Pass one.")
    agent_name = name or name_argument
    if agent_name is None:
        if not shared.can_prompt():
            raise shared.fail("No agent name was given. Run `agents init NAME`.")
        agent_name = typer.prompt("Agent name").strip()

    folder = Path(agent_name)
    try:
        project.check_name(agent_name)
        project.check_folder(folder)
        sdk_version = project.sdk_version()
    except project.ProjectError as exc:
        raise shared.fail(str(exc)) from exc

    uv_path = uv.find() or _install_uv(yes=yes)

    written = project.write(folder, agent_name, sdk_version, exempt_from_exclude_newer=exempt_from_exclude_newer)
    _done(f"Created [bold]{folder}/[/]")
    Console().print(Padding(Text(", ".join(written), style="dim"), (0, 0, 0, 2)))
    try:
        with shared.loading_spinner("Locking dependencies with uv..."):
            uv.lock(folder, uv_path)
    except uv.UvError as exc:
        raise shared.fail(
            str(exc),
            *([exc.output] if exc.output else []),
            f"Fix it, then run `uv lock --directory {folder}`, and commit the project.",
        ) from exc
    _done("Locked the dependencies in uv.lock")

    key = None if yes else _ask_api_key()
    try:
        api_key.write_env(folder, key or "")
    except OSError as exc:
        raise shared.fail(f"Could not write {folder / api_key.ENV_FILE}: {exc.strerror}.") from exc
    if key:
        _done(f"Wrote {api_key.ENV_VARIABLE} to {api_key.ENV_FILE}")
    has_api_key = key is not None
    repository = _init_git(folder, yes=yes, no_git=no_git)
    _print_next_steps(folder, repository, has_api_key=has_api_key)
    raise typer.Exit(0)


def _install_uv(*, yes: bool) -> str:
    installer = uv.install_command()[-1]
    typer.echo(
        "uv is not installed. `agents init` locks the project's dependencies with it, "
        "and the Dockerfile builds from that lock."
    )
    if not yes:
        if not shared.can_prompt():
            raise shared.fail(
                "uv is not installed.",
                "Run `agents init` in a terminal to have it installed, or pass --yes.",
                f"To install it yourself, see {uv.INSTALL_DOCS_URL}",
            )
        if not typer.confirm(f"Install uv with `{installer}`?", default=True):
            raise shared.fail(f"Install uv, then run `agents init` again. See {uv.INSTALL_DOCS_URL}")
    try:
        return uv.install()
    except uv.UvError as exc:
        raise shared.fail(str(exc), f"To install it yourself, see {uv.INSTALL_DOCS_URL}") from exc


def _ask_api_key() -> str | None:
    """Ask for the API key, or return None when there is no terminal or the user skips.

    The key is typed hidden, never passed as an option or printed in a command, so it stays out of the
    shell history.
    """
    if not shared.can_prompt():
        return None
    typer.echo(
        f"The agent calls Mistral's API with an API key from Studio. `agents init` can write it to {api_key.ENV_FILE}."
    )
    choice = _choose("[o]pen Studio to create a key, [p]aste a key you have, or [s]kip", ("o", "p", "s"), default="o")
    if choice == "s":
        return None
    if choice == "o" and not api_key.open_studio():
        typer.echo(f"Open {api_key.STUDIO_API_KEYS_URL} to create a key.")
    while True:
        try:
            return api_key.checked(typer.prompt("API key", hide_input=True))
        except ValueError as exc:
            typer.echo(str(exc), err=True)


def _choose(question: str, choices: tuple[str, ...], *, default: str) -> str:
    while True:
        answer = typer.prompt(question, default=default).strip().lower()
        if answer in choices:
            return answer
        typer.echo(f"Answer one of {', '.join(choices)}.", err=True)


def _init_git(folder: Path, *, yes: bool, no_git: bool) -> _Repository:
    """Commit the project in a new repository if the user agrees, and say which repository it is in."""
    context = git.context(folder)
    if no_git:
        return "enclosing" if context.state is git.GitState.IN_REPOSITORY else "none"
    if context.state is git.GitState.IN_REPOSITORY:
        _note(f"{folder} is inside a git repository: commit it there.")
        return "enclosing"
    if context.state is git.GitState.NO_GIT or context.git is None:
        _note("git is not installed, so no repository was created.")
        return "none"
    if not yes:
        if not shared.can_prompt():
            return "none"
        typer.echo("`agents deploy` builds the commit you push to GitHub, so the project must be a git repository.")
        if not typer.confirm("Create a git repository and commit the project?", default=True):
            return "none"
    try:
        git.init(folder, context.git)
    except git.GitError as exc:
        raise shared.fail(str(exc), *([exc.output] if exc.output else []), "Finish with:", f"  {exc.command}") from exc
    _done("Created a git repository and committed the project")
    return "own"


# The repository the project ends up in: its own new one, an enclosing one such as a monorepo, or none yet.
_Repository = Literal["own", "enclosing", "none"]


def _done(message: str) -> None:
    Console().print(f"[green]✓[/] {message}", highlight=False)


def _note(message: str) -> None:
    Console().print(f"[yellow]![/] {message}", highlight=False)


def _commands(title: str, lines: list[str]) -> Panel:
    # ansi_dark keeps the terminal's own palette, and the default background its own background.
    code = Syntax("\n".join(lines), "bash", theme="ansi_dark", background_color="default")
    return Panel(code, title=f"[bold]{title}[/]", title_align="left", border_style="dim", expand=False, padding=(0, 1))


def _print_next_steps(folder: Path, repository: _Repository, *, has_api_key: bool) -> None:
    # One block, from one `cd`: the git commands must run in the project, not where `init` ran.
    lines = [f"cd {folder}"]
    if not has_api_key:
        lines.append(f"# Set {api_key.ENV_VARIABLE} in {api_key.ENV_FILE}: console.mistral.ai/api-keys")
    lines += ["", "# Try the agent", "uv run --env-file .env agents chat", "", "# Deploy it"]
    if repository == "enclosing":
        lines += ['git add . && git commit -m "Add the agent"', "git push"]
    else:
        if repository == "none":
            lines += ["git init", "git add --all", f'git commit -m "{git.COMMIT_MESSAGE}"']
        lines += ["git remote add origin <repository-url>", "git push -u origin HEAD"]
    lines.append("uv run --env-file .env agents deploy")
    console = Console()
    console.print()
    console.print(_commands("Next steps", lines))
