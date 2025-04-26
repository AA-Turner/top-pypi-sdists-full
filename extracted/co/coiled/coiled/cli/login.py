import asyncio

import click
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.rule import Rule

import coiled

from ..utils import login_if_required
from .hello import hello
from .utils import CONTEXT_SETTINGS

console = Console(width=80)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option("-s", "--server", help="Coiled server to use", hidden=True)
@click.option("-t", "--token", multiple=True, help="Coiled user token")
@click.option(
    "-a",
    "--account",
    "--workspace",
    help=(
        "Coiled workspace (uses default workspace if not specified). "
        "Note: --account is deprecated, please use --workspace instead."
    ),
)
@click.option(
    "--retry/--no-retry",
    default=True,
    help="Whether or not to automatically ask for a new token if an invalid token is entered",
)
@click.option("--browser/--no-browser", default=True, help="Open browser with page where you grant access")
@click.pass_context
def login(ctx, server, token, account, retry, browser):
    """Configure your Coiled account credentials"""
    # allow token split across multiple --token args, so we can have shorter lines for cloudshell command
    token = "".join(token) if token else None
    asyncio.run(
        login_if_required(
            server=server, token=token, workspace=account, save=True, use_config=False, retry=retry, browser=browser
        )
    )

    if not token and len(coiled.list_api_tokens()) <= 1:
        console.print(Rule(style="white"))
        console.print("""
[green]Welcome to Coiled![/green]
Next you can run a guided quickstart to get started.
""")
        try:
            choice = Prompt.ask(
                "Run quickstart?",
                choices=["y", "n"],
                default="y",
                show_choices=True,
            )
        except KeyboardInterrupt:
            return

        coiled.add_interaction("cli-hello:from-login", success=True, choice=choice)
        if choice == "y":
            ctx.invoke(hello)
        else:
            console.print(
                Markdown("""
Go through the quickstart at any point by running

```bash
$ coiled quickstart
```

in your terminal.
""")
            )
