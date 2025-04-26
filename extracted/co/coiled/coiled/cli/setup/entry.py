import asyncio
import traceback

import click
from rich import print
from rich.panel import Panel
from rich.prompt import Prompt

import coiled

from ..utils import CONTEXT_SETTINGS
from .util import setup_failure


@click.command(context_settings=CONTEXT_SETTINGS)
def setup_wizard() -> bool:
    return asyncio.run(do_setup_wizard())


async def do_setup_wizard() -> bool:
    await coiled.utils.login_if_required()

    coiled.add_interaction(
        action="cli-setup-wizard:start",
        success=True,
    )

    print(
        Panel(
            """
[bold]Welcome to Coiled![/bold]

To begin you need to connect Coiled to your cloud account.
Select one of the following options:

  1. Amazon Web Service ([green]AWS[/green])
  2. Google Cloud Platform ([green]GCP[/green])
  3. I don't have a cloud account, set me up with a free trial?
  [red]x[/red]. Exit setup

""".strip(),
            width=90,
        )
    )

    try:
        choice = Prompt.ask(
            "Choice",
            choices=["1", "2", "3", "x"],
            show_choices=False,
        )
    except KeyboardInterrupt:
        coiled.add_interaction(action="cli-setup-wizard:KeyboardInterrupt", success=False)
        return False

    coiled.add_interaction(action="cli-setup-wizard:prompt", success=True, choice=choice)

    if choice == "1":  # AWS
        from .aws import do_setup

        try:
            return do_setup(slug="coiled")
        except Exception:
            setup_failure(f"Exception raised {traceback.format_exc()}", backend="aws")
            raise
    elif choice == "2":  # GCP
        print("\nRunning [green]coiled setup gcp[/green]\n")
        from .gcp import do_setup

        try:
            return do_setup()
        except Exception:
            setup_failure(f"Exception raised {traceback.format_exc()}", backend="gcp")
            raise
    elif choice == "3":  # Other
        print(
            "\nYou can easily set up a free account with AWS or GCP.\n\n"
            "[green]AWS[/green]: [link]https://aws.amazon.com/free[/link]\n"
            "[green]GCP[/green]: [link]https://cloud.google.com/free/[/link]\n\n"
            "Alternatively, ask for a temporary guest account. "
            "Reach out at "
            "[link=mailto:hello@coiled.io?subject=Trial%20Account]hello@coiled.io[/link] "
            "with a brief note about how you'd like to use Dask and Coiled"
        )

    return False
