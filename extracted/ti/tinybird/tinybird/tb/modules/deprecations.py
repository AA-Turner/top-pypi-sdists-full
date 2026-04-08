import click

from tinybird.tb.modules.cli import cli
from tinybird.tb.modules.exceptions import CLIMockException
from tinybird.tb.modules.feedback_manager import FeedbackManager, get_cli_name


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
    message = f"This command is deprecated. Use `{get_cli_name()} login` instead."
    if is_info_cmd:
        message = f"This command is deprecated. Use `{get_cli_name()} info` instead."
    else:
        message = f"This command is deprecated. Use `{get_cli_name()} login` instead."
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
            message=f"`{get_cli_name()} environment` has been renamed to `{get_cli_name()} branch`. Please use `{get_cli_name()} branch {args[0]}` instead."
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
    click.echo(FeedbackManager.warning(message=f"This command is deprecated. Use `{get_cli_name()} deploy` instead."))
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


@cli.command(
    name="create",
    context_settings=dict(
        ignore_unknown_options=True,
    ),
    hidden=True,
)
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
def create(args) -> None:
    """
    `tb create` is deprecated. Use `tb init` instead.
    """
    _ = args
    click.echo(
        FeedbackManager.warning(
            message=f"`{get_cli_name()} create` is deprecated. Use `{get_cli_name()} init` to scaffold your project."
        )
    )
    click.echo(
        "You are using Tinybird Forward CLI.\nYou can find more information in the docs at https://www.tinybird.co/docs/forward"
    )


@cli.command(
    name="mock",
    context_settings=dict(
        ignore_unknown_options=True,
    ),
    hidden=True,
)
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
def mock(args) -> None:
    """
    `tb mock` is removed.
    """
    _ = args
    raise CLIMockException(
        FeedbackManager.error(
            message=(
                f"`{get_cli_name()} mock` has been removed. Create fixture files manually under the `fixtures/` folder.\n"
                "You can use Tinybird agent skills to generate mock behavior from your coding agent. "
                "Run: npx skills add @tinybirdco/tinybird-agent-skills"
            )
        )
    )
