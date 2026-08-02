"""Run a command once with an environment's variables loaded.

    pysae-ai-tools env run pytest                  # dev (default)
    pysae-ai-tools env run -e prod python x.py     # prod
    pysae-env run -e prod pytest -v                # via the shell shim

Resolves every in-scope variable for the environment — the same set as
``env activate``, honouring the repo's ``.pysae-ai-tools.yaml`` whitelist and the
parallel secret preload — injects them under their per-environment usual names
into the child's environment, then runs the command. Unlike ``env activate`` it
never touches the calling shell: the variables live only for that single run.

``-e``/``--env`` and ``--ignore-project-config`` must come before the command;
everything after is passed to the command untouched (``pysae-env run -e prod
pytest -v`` runs ``pytest -v`` with the prod environment).
"""

import contextlib
import os
import subprocess
import sys
from typing import Annotated

import typer

from .resolve import (
    Environment,
    EnvOption,
    preload_secrets,
    project_variable_filter,
    resolution_map,
    try_auto_resolve,
)
from .trace import assume_noninteractive

app = typer.Typer(add_completion=False)


@app.command(
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True, "allow_interspersed_args": False}
)
def main(
    ctx: typer.Context,
    environment: EnvOption = Environment.DEV,
    ignore_project_config: Annotated[
        bool,
        typer.Option("--ignore-project-config", help="Ignore the repo's .pysae-ai-tools.yaml env.variables whitelist."),
    ] = False,
) -> None:
    """Execute a command with an environment's variables loaded for that single run."""
    command = list(ctx.args)
    if not command:
        typer.echo(
            "env run: no command given — usage: pysae-ai-tools env run [-e prod] <command> [args...]",
            err=True,
        )
        raise typer.Exit(code=2)

    targets = list(project_variable_filter(dict(resolution_map(environment)), ignore=ignore_project_config).items())

    child_env = dict(os.environ)
    resolved: list[str] = []
    # Resolver trace goes to stderr so the child's stdout stays clean; a var that
    # would need a prompt self-skips in non-interactive mode.
    with contextlib.redirect_stdout(sys.stderr), assume_noninteractive():
        preload_secrets(var for _, var in targets if not os.environ.get(var))
        for name, var in targets:
            value = os.environ.get(var) or try_auto_resolve(var)
            if value:
                child_env[name] = value
                resolved.append(name)

    loaded = ", ".join(resolved) or "no variable resolved"
    print(f"env run ({environment.value}): {loaded} — $ {' '.join(command)}", file=sys.stderr)

    try:
        completed = subprocess.run(command, env=child_env)
    except FileNotFoundError:
        typer.echo(f"env run: command not found: {command[0]}", err=True)
        raise typer.Exit(code=127) from None
    raise typer.Exit(code=completed.returncode)


if __name__ == "__main__":
    app()
