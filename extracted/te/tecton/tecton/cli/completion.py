import sys

import click

from tecton.cli import cli
from tecton.cli.command import TectonCommand


@click.command(requires_auth=False, cls=TectonCommand)
@click.option("--zsh", default=False, is_flag=True, help="Generate a zsh tab completion script.")
@click.option("--bash", default=False, is_flag=True, help="Generate a bash tab completion script.")
@click.option("--fish", default=False, is_flag=True, help="Generate a fish tab completion script.")
def completion(zsh, bash, fish):
    """Generates a shell script to set up tab completion for Tecton. Zsh, bash, and fish shells are supported.

    See typical usage examples below:

    zsh:

        # Generate and save the Tecton auto-complete script.

        tecton completion --zsh > ~/.tecton-complete.zsh

        # Enable zsh auto-completion. (Not needed if you already have auto-complete enabled, e.g. are using oh-my-zsh.)

        echo 'autoload -Uz compinit && compinit' >> ~/.zshrc

        # Add sourcing the script into your .zshrc.

        echo '. ~/.tecton-complete.zsh' >> ~/.zshrc

    bash:

        # Generate and save the Tecton auto-complete script.

        tecton completion --bash > ~/.tecton-complete.bash

        # Add sourcing the script into your .bashrc.

        echo '. ~/.tecton-complete.bash' >> ~/.bashrc

    fish:

        # Generate and save the Tecton auto-complete script to your fish configs.

        tecton completion --fish > ~/.config/fish/completions/tecton.fish
    """
    true_count = sum([zsh, bash, fish])
    if true_count != 1:
        msg = "Please set exactly one of --zsh, --bash, or --fish to generate a script for your shell environment."
        raise SystemExit(msg)

    if zsh:
        instruction = "zsh_source"
    elif bash:
        instruction = "bash_source"
    elif fish:
        instruction = "fish_source"

    status_code = click.shell_completion.shell_complete(
        cli, ctx_args={}, prog_name="tecton", complete_var="_TECTON_COMPLETE", instruction=instruction
    )
    sys.exit(status_code)
