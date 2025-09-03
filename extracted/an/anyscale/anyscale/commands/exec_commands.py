import click

from anyscale.commands.util import DeprecatedAnyscaleCommand


@click.command(
    name="exec",
    hidden=True,
    help="[DEPRECATED] Execute shell commands in interactive cluster.",
    context_settings={"ignore_unknown_options": True, "allow_extra_args": True,},
    cls=DeprecatedAnyscaleCommand,
    removal_date="2025-10-01",
    deprecation_message="`anyscale exec` has been deprecated and no longer works on Anyscale",
    alternative="use `anyscale job submit` to run your script as a job in a cluster",
)
def anyscale_exec() -> None:
    """Execute shell commands in interactive cluster.

    DEPRECATED: This command will be removed on 2025-10-01.
    Use 'anyscale job submit' to run your script as a job in a cluster.
    """
    raise click.ClickException(
        "`anyscale exec` has been deprecated and no longer works on Anyscale. "
        "Please use `anyscale job submit` to run your script as a job in a cluster."
    )
