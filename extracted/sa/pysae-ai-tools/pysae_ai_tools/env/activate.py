"""Load supported vars into the current shell under their per-environment usual names.

    eval "$(pysae-ai-tools env activate)"        # dev (default)
    eval "$(pysae-ai-tools env activate prod)"   # prod

For the requested environment, every variable in scope is resolved and emitted
as a shell assignment under its **resolved name** — so tools expecting the
generic name (``MONGO_URI``, ``ATLAS_PUBLIC_KEY``, …) find it. Environment-agnostic
variables (``environment is None``) apply to every environment; an
environment-specific entry wins over an agnostic one on a name collision.

Best-effort: variables that fail to resolve are silently skipped (their assignment
is simply absent), so a partial environment still activates. Never prints a value
on stdout other than as a shell assignment consumed by ``eval``.

Before overwriting them, the pre-activation value of each variable is recorded
(JSON) in ``$PYSAE_ENV_ACTIVATE_BACKUP`` so ``env deactivate`` can restore or
unset them. Re-activating without deactivating keeps the earliest snapshot.
"""

import contextlib
import json
import os
import sys
from typing import Annotated

import typer

from .resolve import (
    ACTIVATE_BACKUP_VAR,
    Environment,
    EnvOption,
    preload_secrets,
    project_variable_filter,
    resolution_map,
    try_auto_resolve,
)
from .shell_format import VALID_SHELLS, detect_shell, format_set_line
from .trace import assume_noninteractive, is_tty

app = typer.Typer()


def _run_hint(shell: str, command: str) -> str:
    """How to feed ``command``'s output into the current shell."""
    if shell == "powershell":
        return f"{command} --shell powershell | Invoke-Expression"
    if shell == "cmd":
        return f"for /f \"delims=\" %i in ('{command} --shell cmd') do @%i"
    if shell == "fish":
        return f"{command} | source"
    return f'eval "$({command})"'  # posix (Linux, macOS, Git Bash/WSL)


def _load_backup() -> dict[str, str | None]:
    """Parse the pre-activation snapshot already in the environment (if any)."""
    raw = os.environ.get(ACTIVATE_BACKUP_VAR)
    if not raw:
        return {}
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def _targets(environment: str) -> list[tuple[str, str]]:
    """Return ``(output_name, canonical_var)`` pairs to export for ``environment``.

    dev/prod/testing expose in-scope variables under their usual name; ``all``
    exposes every variable under its original name (see :func:`resolution_map`).
    """
    return list(resolution_map(environment).items())


@app.command()
def main(
    environment: EnvOption = Environment.DEV,
    shell: Annotated[
        str | None,
        typer.Option("--shell", help="Force the output shell format: posix, powershell, or cmd (else auto-detected)."),
    ] = None,
    ignore_project_config: Annotated[
        bool,
        typer.Option("--ignore-project-config", help="Ignore the repo's .pysae-ai-tools.yaml env.variables whitelist."),
    ] = False,
) -> None:
    """Emit shell assignments loading supported vars under their usual names for an environment."""
    if shell is not None and shell not in VALID_SHELLS:
        typer.echo(f"--shell: invalid value {shell!r} (expected posix|powershell|cmd)", err=True)
        raise typer.Exit(code=2)

    resolved_shell = shell or detect_shell()
    targets = list(project_variable_filter(dict(_targets(environment)), ignore=ignore_project_config).items())

    # Snapshot the current value of each output name BEFORE resolving — the loop
    # mutates os.environ for agnostic vars (resolved_name == canonical name).
    old_values = {name: os.environ.get(name) for name, _ in targets}

    # stdout carries only the shell assignments (consumed by `eval "$(…)"`);
    # every resolver log line is redirected to stderr so it never pollutes it.
    # Non-interactive: a var needing a browser/glab/credential prompt self-skips
    # instead of hijacking the `$(…)` subshell.
    resolved: list[tuple[str, str]] = []
    with contextlib.redirect_stdout(sys.stderr), assume_noninteractive():
        preload_secrets(var for _, var in targets)
        for name, var in targets:
            value = os.environ.get(var) or try_auto_resolve(var)
            if value:
                resolved.append((name, value))

    if not resolved:
        print(f"no environment variable resolved for '{environment}'", file=sys.stderr)
        raise typer.Exit(code=1)

    for name, value in resolved:
        typer.echo(format_set_line(resolved_shell, name, value))

    # Record each set var's pre-activation value (keeping the earliest snapshot
    # across chained activations) so `env deactivate` can restore or unset it.
    backup = _load_backup()
    for name, _ in resolved:
        backup.setdefault(name, old_values[name])
    typer.echo(format_set_line(resolved_shell, ACTIVATE_BACKUP_VAR, json.dumps(backup)))

    activated = ", ".join(name for name, _ in resolved)
    # A TTY stdout means the output was NOT captured by `$()`/`eval` — the
    # assignments just scrolled past and nothing was loaded. Flag the misuse.
    if is_tty():
        suffix = "" if environment == Environment.DEV else f" --env {environment.value}"
        hint = _run_hint(resolved_shell, f"pysae-ai-tools env activate{suffix}")
        typer.secho(f"⚠ output not captured — load it with: {hint}", fg=typer.colors.YELLOW, err=True)
    print(f"activated ({environment}): {activated}", file=sys.stderr)


if __name__ == "__main__":
    app()
