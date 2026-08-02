"""Print the ``pysae-env`` shell function that wraps ``pysae-ai-tools env``.

The function evaluates ``activate`` / ``deactivate`` in the *current* shell (so
their assignments actually take effect) and passes every other subcommand
straight through. It removes the need to type ``eval "$(…)"`` by hand.

Add it once to your shell startup file:

    # bash/zsh/sh/ksh (~/.bashrc, ~/.zshrc)
    eval "$(pysae-ai-tools env shell-init)"

    # fish (~/.config/fish/config.fish)
    pysae-ai-tools env shell-init --shell fish | source

    # PowerShell ($PROFILE)
    pysae-ai-tools env shell-init --shell powershell | Out-String | Invoke-Expression

Then:  ``pysae-env activate --env dev`` / ``pysae-env deactivate`` / ``pysae-env list`` …

``pysae-ai-tools tools install`` sets this up for you by default: the rc line above
for POSIX shells / fish / PowerShell, and a ``pysae-env.bat`` shim on PATH for
cmd.exe. cmd has no shell *functions*, but a ``.bat`` invoked at the prompt runs in
the current cmd process, so its ``set`` persists — same end result as ``pysae-env``
elsewhere.
"""

from typing import Annotated

import typer

from .shell_format import VALID_SHELLS, detect_shell

app = typer.Typer()

_POSIX_FUNC = """\
pysae-env() {
  case "$1" in
    activate|deactivate) eval "$(command pysae-ai-tools env "$@")" ;;
    *) command pysae-ai-tools env "$@" ;;
  esac
}"""

_POWERSHELL_FUNC = """\
function pysae-env {
  if (@('activate','deactivate') -contains $args[0]) {
    pysae-ai-tools env @args --shell powershell | Out-String | Invoke-Expression
  } else {
    pysae-ai-tools env @args
  }
}"""

_FISH_FUNC = """\
function pysae-env
  switch $argv[1]
    case activate deactivate
      pysae-ai-tools env $argv --shell fish | source
    case '*'
      pysae-ai-tools env $argv
  end
end"""

CMD_SHIM = """\
@echo off
rem pysae-ai-tools env shell-init (pysae-env) — managed file, do not edit
if /I "%~1"=="activate"   goto :pysae_env_eval
if /I "%~1"=="deactivate" goto :pysae_env_eval
pysae-ai-tools env %*
goto :eof
:pysae_env_eval
for /f "usebackq delims=" %%i in (`pysae-ai-tools env %* --shell cmd`) do %%i"""


@app.command()
def main(
    shell: Annotated[
        str | None,
        typer.Option("--shell", help="Target shell: posix, fish, powershell, or cmd (else auto-detected)."),
    ] = None,
) -> None:
    """Print the pysae-env integration for the target shell.

    POSIX / fish / PowerShell emit a shell function (eval it in your rc); cmd emits
    the ``pysae-env.bat`` shim body (write it to a file on PATH).
    """
    resolved = shell or detect_shell()
    if resolved is not None and resolved not in VALID_SHELLS:
        typer.echo(f"--shell: invalid value {shell!r} (expected posix|powershell|cmd)", err=True)
        raise typer.Exit(code=2)
    if resolved == "powershell":
        typer.echo(_POWERSHELL_FUNC)
    elif resolved == "fish":
        typer.echo(_FISH_FUNC)
    elif resolved == "cmd":
        typer.echo(CMD_SHIM)
    else:
        typer.echo(_POSIX_FUNC)


if __name__ == "__main__":
    app()
