import asyncio
import logging

import click

from lunchable_pushlunch import PushLunch
from lunchable_pushlunch.base import Notifier
from lunchable_pushlunch.ntfy import Ntfy

providers: dict[str, type[Notifier]] = {"pushover": PushLunch, "ntfy": Ntfy}


@click.group(invoke_without_command=True)
@click.pass_context
def pushlunch(ctx: click.Context) -> None:
    """
    Push Notifications for Lunch Money: PushLunch 📲
    """
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())
    if not ctx.parent:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )


@pushlunch.command("notify")
@click.option(
    "--continuous",
    "-c",
    is_flag=True,
    help="Whether to continuously check for more uncleared transactions, "
    "waiting a fixed amount in between checks.",
    envvar="PUSHLUNCH_CONTINUOUS",
    show_envvar=True,
)
@click.option(
    "--interval",
    "-i",
    default=None,
    help="Sleep Interval in Between Tries - only applies if `continuous` is set. "
    "Defaults to 60 (minutes). Cannot be less than 5 (minutes)",
    type=int,
    envvar="PUSHLUNCH_INTERVAL",
    show_envvar=True,
)
@click.option(
    "--key",
    "--user-key",
    "-k",
    default=None,
    help="Provider Credentials. `pushover`: User Key, `ntfy`: Topic",
)
@click.option(
    "--provider",
    "-p",
    default="pushover",
    type=click.Choice(choices=list(providers.keys()), case_sensitive=False),
    help="Notification Provider to use. Defaults to `ntfy`",
    envvar="PUSHLUNCH_PROVIDER",
    show_envvar=True,
)
def notify(continuous: bool, interval: int, key: str, provider: str) -> None:
    """
    Send a Notification for each Uncleared Transaction
    """
    provider_class: type[Notifier] = providers[provider.lower()]
    push: Notifier = provider_class(key=key)
    if interval is not None:
        interval = int(interval)
    asyncio.run(
        push.notify_uncleared_transactions(continuous=continuous, interval=interval)
    )


if __name__ == "__main__":
    pushlunch()
