import click

from tinybird.tb.modules.cli import cli
from tinybird.tb.modules.feedback_manager import FeedbackManager


@cli.command(
    name="auth",
    context_settings=dict(
        ignore_unknown_options=True,
    ),
    hidden=True,
)
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
def auth(args) -> None:
    """
    `tb auth` is deprecated. Use `tb login` instead.
    """
    is_info_cmd = "info" in args
    message = "This command is deprecated. Use `tb login` instead."
    if is_info_cmd:
        message = "This command is deprecated. Use `tb info` instead."
    else:
        message = "This command is deprecated. Use `tb login` instead."
    click.echo(FeedbackManager.warning(message=message))
    click.echo(
        "You are using Tinybird Forward CLI.\nYou can find more information in the docs at https://www.tinybird.co/docs/forward"
    )


@cli.command(
    name="environment",
    context_settings=dict(
        ignore_unknown_options=True,
    ),
    hidden=True,
)
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
def environment(args) -> None:
    """
    `tb environment` has been renamed to `tb branch`.
    """
    click.echo(
        FeedbackManager.warning(
            message=f"`tb environment` has been renamed to `tb branch`. Please use `tb branch {args[0]}` instead."
        )
    )
    click.echo(
        "You are using Tinybird Forward CLI.\nYou can find more information in the docs at https://www.tinybird.co/docs/forward"
    )


@cli.command(
    name="check",
    context_settings=dict(
        ignore_unknown_options=True,
    ),
    hidden=True,
)
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
def check(args) -> None:
    """
    `tb check` is deprecated.
    """
    click.echo(FeedbackManager.warning(message="This command is deprecated."))
    click.echo(
        "You are using Tinybird Forward CLI.\nYou can find more information in the docs at https://www.tinybird.co/docs/forward"
    )


@cli.command(
    name="diff",
    context_settings=dict(
        ignore_unknown_options=True,
    ),
    hidden=True,
)
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
def diff(args) -> None:
    """
    `tb diff` is deprecated.
    """
    click.echo(FeedbackManager.warning(message="This command is deprecated."))
    click.echo(
        "You are using Tinybird Forward CLI.\nYou can find more information in the docs at https://www.tinybird.co/docs/forward"
    )


@cli.command(
    name="init",
    context_settings=dict(
        ignore_unknown_options=True,
    ),
    hidden=True,
)
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
def init(args) -> None:
    """
    `tb init` is deprecated. Use `tb create` instead.
    """
    click.echo(FeedbackManager.warning(message="This command is deprecated. Use `tb create` instead."))
    click.echo(
        "You are using Tinybird Forward CLI.\nYou can find more information in the docs at https://www.tinybird.co/docs/forward"
    )


@cli.command(
    name="push",
    context_settings=dict(
        ignore_unknown_options=True,
    ),
    hidden=True,
)
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
def push(args) -> None:
    """
    `tb push` is deprecated. Use `tb deploy` instead.
    """
    click.echo(FeedbackManager.warning(message="This command is deprecated. Use `tb deploy` instead."))
    click.echo(
        "You are using Tinybird Forward CLI.\nYou can find more information in the docs at https://www.tinybird.co/docs/forward"
    )


@cli.command(
    name="tag",
    context_settings=dict(
        ignore_unknown_options=True,
    ),
    hidden=True,
)
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
def tag(args) -> None:
    """
    `tb tag` is deprecated
    """
    click.echo(FeedbackManager.warning(message="This command is deprecated."))
    click.echo(
        "You are using Tinybird Forward CLI.\nYou can find more information in the docs at https://www.tinybird.co/docs/forward"
    )
