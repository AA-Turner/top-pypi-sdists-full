"""Write an environment's resolved variables to a ``.env`` file (KEY=value).

    pysae-ai-tools env dotenv            # dev → ./.env
    pysae-ai-tools env dotenv --env prod -o .env.prod

Resolves the same set as ``env activate`` (every variable in scope for the
environment, under its usual name) but writes ``KEY=value`` lines to a file
instead of exporting them. Resolution is non-interactive — a variable needing a
browser/glab/credential prompt self-skips and is simply omitted.

When the file already exists it is **merged**: the variables pysae-ai-tools
resolves are updated in place (or appended), while every other line — foreign
variables, comments, blanks — is preserved. The file is written with ``0600``
perms since it holds secrets.
"""

import os
import re
import stat
from pathlib import Path
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

app = typer.Typer()

_NEEDS_QUOTING = set(" \t\"'#$`\\\n\r")
_ASSIGNMENT = re.compile(r"^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=")


def _format_line(name: str, value: str) -> str:
    """Format one ``.env`` assignment, double-quoting values that need it."""
    if value and not any(c in _NEEDS_QUOTING for c in value):
        return f"{name}={value}"
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'{name}="{escaped}"'


def _render(resolved: dict[str, str]) -> str:
    """Fresh file body: every resolved variable, sorted."""
    return "".join(f"{_format_line(name, resolved[name])}\n" for name in sorted(resolved))


def _merge(existing: str, resolved: dict[str, str]) -> str:
    """Merge ``resolved`` into ``existing`` file text.

    Managed variables already present are rewritten in place (preserving their
    position); unmanaged lines — foreign variables, comments, blanks — are kept
    verbatim; newly-resolved variables are appended (sorted).
    """
    pending = dict(resolved)
    lines: list[str] = []
    for line in existing.splitlines():
        match = _ASSIGNMENT.match(line)
        if match and match.group(1) in pending:
            key = match.group(1)
            lines.append(_format_line(key, pending.pop(key)))
        else:
            lines.append(line)
    for key in sorted(pending):
        lines.append(_format_line(key, pending[key]))
    return "\n".join(lines) + "\n" if lines else ""


@app.command()
def main(
    environment: EnvOption = Environment.DEV,
    output: Annotated[
        Path,
        typer.Option("--output", "-o", help="Destination file (merged in place if it already exists)."),
    ] = Path(".env"),
    ignore_project_config: Annotated[
        bool,
        typer.Option("--ignore-project-config", help="Ignore the repo's .pysae-ai-tools.yaml env.variables whitelist."),
    ] = False,
) -> None:
    """Generate (or update) a .env file with the environment's resolved variables."""
    targets = project_variable_filter(resolution_map(environment), ignore=ignore_project_config)

    resolved: dict[str, str] = {}
    with assume_noninteractive():
        preload_secrets(targets.values())
        for name, var in targets.items():
            value = os.environ.get(var) or try_auto_resolve(var)
            if value:
                resolved[name] = value

    if not resolved:
        typer.echo(f"no environment variable resolved for '{environment}' — {output} left untouched", err=True)
        raise typer.Exit(code=1)

    if output.exists():
        try:
            body = _merge(output.read_text(encoding="utf-8", errors="replace"), resolved)
        except OSError as exc:
            typer.echo(f"could not read {output}: {exc}", err=True)
            raise typer.Exit(code=1) from None
        verb = "updated"
    else:
        body = _render(resolved)
        verb = "wrote"

    fd = os.open(output, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(body)
    os.chmod(output, stat.S_IRUSR | stat.S_IWUSR)  # enforce 0600 even on an existing file

    typer.echo(f"{verb} {len(resolved)} variable(s) for '{environment}' in {output}", err=True)


if __name__ == "__main__":
    app()
