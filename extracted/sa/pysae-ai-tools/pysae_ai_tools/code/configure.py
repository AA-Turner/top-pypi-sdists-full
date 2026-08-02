"""Interactive configuration of pysae-ai-tools.

Lets the user (re-)set values stored in ``~/.config/pysae-ai-tools/config.toml``,
even if they were already filled in. The first-run prompt in
``code ensure-repo`` is one-shot — this command is the way to update the
choice afterwards.

Usage:
    pysae-ai-tools code configure              # re-prompt every setting
    pysae-ai-tools code configure --show       # only show the current resolved values
"""

import os
import sys
from pathlib import Path
from typing import Annotated

import typer

from .. import config as _config_module
from ..config import load_config, os_default_clone_dir, set_git_clone_dir
from .claude_perms import interactive_offer as _claude_perms_offer

DEFAULT_BASE_DIR_ENV = "PYSAE_AI_TOOLS_GIT_CLONE_DIR"


app = typer.Typer()


def _show_current() -> None:
    cfg = load_config()
    env_value = os.environ.get(DEFAULT_BASE_DIR_ENV, "")
    os_default = os_default_clone_dir()

    if env_value:
        effective = env_value
        source = f"${DEFAULT_BASE_DIR_ENV} (env)"
    elif cfg.git_clone_dir:
        effective = cfg.git_clone_dir
        source = "config file"
    else:
        effective = str(os_default)
        source = "OS default"

    print(f"Config file       : {_config_module.CONFIG_FILE}", file=sys.stderr)
    print(f"git_clone_dir (config) : {cfg.git_clone_dir or '(unset)'}", file=sys.stderr)
    print(f"${DEFAULT_BASE_DIR_ENV} (env) : {env_value or '(unset)'}", file=sys.stderr)
    print(f"OS default        : {os_default}", file=sys.stderr)
    print(f"→ Effective       : {effective}  [{source}]", file=sys.stderr)


def _prompt_git_clone_dir() -> None:
    cfg = load_config()
    os_default = os_default_clone_dir()
    current = cfg.git_clone_dir or str(os_default)

    print("📂 Où veux-tu cloner les projets Pysae ?", file=sys.stderr)
    print(f"   Valeur actuelle : {current}", file=sys.stderr)
    print(f"   Défaut OS       : {os_default}", file=sys.stderr)
    try:
        answer = input("   Nouveau chemin (Entrée = garder l'actuel) : ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\nAnnulé.", file=sys.stderr)
        raise typer.Exit(code=1) from None

    chosen = Path(answer).expanduser() if answer else Path(current).expanduser()
    set_git_clone_dir(str(chosen))
    print(f"✅ Sauvegardé dans la config : {chosen}", file=sys.stderr)

    env_value = os.environ.get(DEFAULT_BASE_DIR_ENV)
    if env_value:
        print(
            f"⚠️  ${DEFAULT_BASE_DIR_ENV}={env_value} reste prioritaire — "
            "unset cette env var si tu veux que la config prenne effet.",
            file=sys.stderr,
        )

    _claude_perms_offer(chosen)


@app.command()
def main(
    show: Annotated[
        bool,
        typer.Option("--show", help="Print current resolved settings without prompting"),
    ] = False,
) -> None:
    """(Re-)configure pysae-ai-tools settings interactively.

    By default, prompts for every configurable value. Use ``--show`` to print
    the current effective values without changing anything.
    """
    if show:
        _show_current()
        return

    if not sys.stdin.isatty():
        print(
            "ERROR: configure requires an interactive terminal (stdin is not a TTY).",
            file=sys.stderr,
        )
        raise typer.Exit(code=2)

    _show_current()
    print(file=sys.stderr)
    _prompt_git_clone_dir()


if __name__ == "__main__":
    app()
