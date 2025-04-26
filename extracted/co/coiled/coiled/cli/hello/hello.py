from __future__ import annotations

import asyncio
import json
import subprocess
import sys
import time

import dask
import dask.config
import httpx
from rich import print
from rich.console import Group
from rich.markdown import Markdown
from rich.prompt import Prompt

import coiled
from coiled.scan import scan_prefix
from coiled.utils import login_if_required

from .examples import examples
from .utils import PRIMARY_COLOR, Panel, console, has_macos_system_python, log_interactions

DEFAULT_SLEEP = 1.5


def needs_login():
    if dask.config.get("coiled.token", False) is False:
        # Need login if no token
        return True

    token = dask.config.get("coiled.token")
    server = dask.config.get("coiled.server")
    # Manually hitting this endpoint to avoid implicitly triggering the login flow
    r = httpx.get(f"{server}/api/v2/user/me", headers={"Authorization": f"ApiToken {token}"})
    if r.is_success:
        return False
    else:
        # Need login if invalid token
        return True


def get_interactions():
    response = subprocess.check_output(["coiled", "curl", "/api/v2/interactions/user-interactions/hello"])
    return json.loads(response, strict=False)


def get_already_run_examples():
    already_run = dict.fromkeys(examples.keys(), False)
    interactions = get_interactions()
    for i in interactions:
        if i["action"].startswith("cli-hello:example-") and i["action"] != "cli-hello:example-exit" and i["success"]:
            name = i["action"].split(":")[1][len("example-") :]
            already_run[name] = True
    return already_run


def get_conda_info():
    scan = asyncio.run(scan_prefix())
    channels = {pkg["channel"] for pkg in scan if pkg["source"] == "conda"}
    non_conda_forge_channels = channels - {"conda-forge"}
    mixed_channels = bool(non_conda_forge_channels)
    packages = []
    if mixed_channels:
        # Only log full package / channel info when there are mixed channels
        packages = [(pkg["name"], pkg["channel"]) for pkg in scan if pkg["source"] == "conda"]
    return {"channels": tuple(channels), "packages": tuple(packages)}


def do_hello_wizard() -> bool:
    console.print(
        Panel(
            rf"""
[bold]                                                  [{PRIMARY_COLOR}]                ..       [/]
                                                   [{PRIMARY_COLOR}]               ###      [/]
              ____           _   _              _  [{PRIMARY_COLOR}]          .### ###.     [/]
             / ___|   ___   (_) | |   ___    __| | [{PRIMARY_COLOR}]         .#### .#.      [/]
            | |      / _ \  | | | |  / _ \  / _` | [{PRIMARY_COLOR}]         #####          [/]
            | |___  | (_) | | | | | |  __/ | (_| | [{PRIMARY_COLOR}]         .#### .        [/]
             \____|  \___/  |_| |_|  \___|  \__,_| [{PRIMARY_COLOR}]           .## ###      [/]
                                                   [{PRIMARY_COLOR}]               ###.     [/]
                 Website: [{PRIMARY_COLOR}][link=https://coiled.io?utm_source=coiled-hello&utm_medium=banner]https://coiled.io[/link][/{PRIMARY_COLOR}]        [{PRIMARY_COLOR}]             # ###      [/]
                 Docs: [{PRIMARY_COLOR}][link=https://docs.coiled.io?utm_source=coiled-hello&utm_medium=banner]https://docs.coiled.io[/link][/{PRIMARY_COLOR}]      [{PRIMARY_COLOR}]            ## ##.      [/]
                                                   [{PRIMARY_COLOR}]            ##          [/]
                                                   [{PRIMARY_COLOR}]             #          [/][/bold]
""".strip()  # noqa
        )
    )

    do_login = needs_login()
    # Here, and in a few other places, we need to be careful to not run code
    # like `coiled.add_interaction` that triggers the login flow implicitly.
    # We want to present the user with the welcome prompt first, so they know
    # what to expect -- then do the login flow if needed.
    if do_login:
        already_run = dict.fromkeys(examples.keys(), False)
    else:
        already_run = get_already_run_examples()

    console.print(
        Panel(
            Group(
                "[bold underline]Welcome![/bold underline]\n",
                Markdown(
                    f"""
Welcome to Coiled, a lightweight cloud computing platform!

To get started we'll go through these steps:

1. {"✅ " if not do_login else ""}Login to Coiled
2. {"✅ " if already_run["hello-world"] else ""}Run "Hello world"
3. Choose larger examples to run like:
    - Process 1 TB of Parquet data
    - Train a PyTorch model on a GPU
    - Churn through 2 TB of geospatial data
    - And more...

""".strip()
                ),
            )
        )
    )

    try:
        choice = Prompt.ask(
            "Good to go?",
            choices=["y", "n"],
            default="y",
            show_choices=True,
        )
    except KeyboardInterrupt:
        if not do_login:
            coiled.add_interaction("cli-hello:KeyboardInterrupt", success=False)
        return False

    if not do_login:
        coiled.add_interaction("cli-hello:ready-start", success=True, choice=choice)

    if choice == "n":
        print("See you next time :wave:")
        return True

    # Handle login if needed
    if do_login:
        console.print(
            Panel(
                Markdown("""
Fist let's make sure you have a Coiled account and that this machine can access your account.

I'll send you to cloud.coiled.io, have you login or make a free account, and download an API token.
Come back here when you're done.
"""),
                title="[white]Step 1: Login[/white]",
                border_style=PRIMARY_COLOR,
            )
        )
        try:
            choice = Prompt.ask(
                "Ready to login?",
                choices=["y", "n"],
                default="y",
                show_choices=True,
                show_default=True,
            )
        except KeyboardInterrupt:
            return False
        if choice == "y":
            with log_interactions("login"):
                asyncio.run(login_if_required())
                console.print(
                    Panel(
                        "Great! You're logged in with Coiled. Let's go run some jobs :thumbsup:",
                        border_style=PRIMARY_COLOR,
                        title="[white]Step 1: Login[/white] :white_check_mark:",
                    )
                )
        else:
            console.print("See you next time :wave:")
            return True
    else:
        console.print(
            Panel(
                "You've already logged into Coiled. Good job! :thumbsup:",
                border_style=PRIMARY_COLOR,
                title="[white]Step 1: Login[/white] :white_check_mark:",
            )
        )

    coiled.add_interaction(
        "cli-hello:info-system",
        success=True,
        platform=sys.platform,
        python=".".join(map(str, sys.version_info[:3])),
        macos_system_python=has_macos_system_python(),
    )
    coiled.add_interaction(
        "cli-hello:info-conda",
        success=True,
        **get_conda_info(),
    )

    # If login was needed, refresh already run examples in case this is a returning user
    if do_login:
        already_run = get_already_run_examples()
    else:
        # Give some time between messages to avoid lots of text flying by
        time.sleep(DEFAULT_SLEEP)

    # Run "Hello world" if needed
    if already_run["hello-world"]:
        console.print(
            Panel(
                "I see you've already run 'Hello world' too! On to bigger examples... :rocket:",
                border_style=PRIMARY_COLOR,
                title="[white]Step 2: Hello world[/white] :white_check_mark:",
            )
        )
    else:
        success = examples["hello-world"](first_time=True)
        if success:
            console.print(
                Panel(
                    """
Now that you've run a simple "Hello world" job, let's look at some larger examples...
""".strip(),  # noqa: E501
                    border_style=PRIMARY_COLOR,
                    title="[white]Step 2: Hello world[/white] :white_check_mark:",
                )
            )
        elif success is False:
            print("See you next time :wave:")
            return False
    time.sleep(DEFAULT_SLEEP)

    # Render examples
    run_example = True
    while run_example is not False:
        run_example = examples_prompt()
    return True


def examples_prompt() -> bool | None:
    already_run = get_already_run_examples()
    console.print(
        Panel(
            Markdown(
                f"""
Choose any computation you'd like to run:

1. {"✅ " if already_run["hello-world"] else ""}Run a script: Hello world
2. {"✅ " if already_run["nyc-parquet"] else ""}Dask at scale: Aggregate 1 TB of parquet data
3. {"✅ " if already_run["xarray-nwm"] else ""}Xarray at scale: Aggregate 2 TB of geospatial data
4. {"✅ " if already_run["pytorch"] else ""}Serverless functions: Train a PyTorch model on a GPU
5. Exit

"""  # noqa: E501,
            ),
            border_style=PRIMARY_COLOR,
            title="[white]Step 3: Big examples[/white]",
        )
    )

    choices = list(map(str, range(1, len(examples.keys()) + 1)))
    # Have default be the first non-run example, excluding the last "exit" option
    default = "1"
    for idx, value in enumerate(list(already_run.values())[:-1], start=1):
        if value is False:
            default = str(idx)
            break

    try:
        choice = Prompt.ask(
            "What would you like to run?",
            choices=choices,
            default=default,
            show_choices=True,
            show_default=True,
        )
        choice = int(choice)
        coiled.add_interaction("cli-hello:examples-prompt", success=True, choice=list(examples.keys())[choice - 1])
    except KeyboardInterrupt:
        coiled.add_interaction("cli-hello:KeyboardInterrupt", success=False)
        return False

    example = list(examples.values())[choice - 1]
    result = example()
    if result is True:
        # TODO: Once hosted exists, give option to run cloud setup
        if sum(already_run.values()) == len(examples) - 1:
            # Have run all examples
            console.print(
                Panel(
                    Markdown("""
Yee-haw you've done all my examples 🎉  
Now you can:
- Try Coiled in your own use case
- [Talk to us](https://calendly.com/d/cmph-386-cjt/coiled-help-getting-started)
- Explore the [docs](https://docs.coiled.io?utm_source=coiled-hello&utm_medium=finished) to see all the other things Coiled can do
"""),  # noqa
                    border_style="green",
                    title="[white]Congratulations[/white]",
                )
            )
        else:
            console.print(
                Panel(
                    "[green]Let's try another example...[/green]",
                    border_style="green",
                    title="[white]More examples[/white]",
                )
            )

    return result
