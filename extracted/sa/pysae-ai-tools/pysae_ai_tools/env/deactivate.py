"""Undo a previous ``env activate`` — restore or unset every variable it set.

    eval "$(pysae-ai-tools env deactivate)"

Reads the pre-activation snapshot ``env activate`` left in
``$PYSAE_ENV_ACTIVATE_BACKUP`` (JSON ``{name: old_value | null}``), restores each
variable to its old value (or unsets it when it had none), then clears the
backup itself. No-op when nothing is active. stdout carries only shell
statements (consumed by ``eval``); everything else goes to stderr.
"""

import json
import os
import sys
from typing import Annotated

import typer

from .resolve import ACTIVATE_BACKUP_VAR
from .shell_format import VALID_SHELLS, detect_shell, format_set_line, format_unset_line

app = typer.Typer()


@app.command()
def main(
    shell: Annotated[
        str | None,
        typer.Option("--shell", help="Force the output shell format: posix, powershell, or cmd (else auto-detected)."),
    ] = None,
) -> None:
    """Emit shell statements restoring the environment to its pre-activate state."""
    if shell is not None and shell not in VALID_SHELLS:
        typer.echo(f"--shell: invalid value {shell!r} (expected posix|powershell|cmd)", err=True)
        raise typer.Exit(code=2)

    resolved_shell = shell or detect_shell()

    raw = os.environ.get(ACTIVATE_BACKUP_VAR)
    if not raw:
        print("no active environment to deactivate", file=sys.stderr)
        return
    try:
        backup = json.loads(raw)
    except json.JSONDecodeError:
        backup = {}

    restored: list[str] = []
    for name, old in backup.items():
        if old is None:
            typer.echo(format_unset_line(resolved_shell, name))
        else:
            typer.echo(format_set_line(resolved_shell, name, old))
        restored.append(name)

    typer.echo(format_unset_line(resolved_shell, ACTIVATE_BACKUP_VAR))
    print(f"deactivated: {', '.join(restored) or 'nothing'}", file=sys.stderr)


if __name__ == "__main__":
    app()
