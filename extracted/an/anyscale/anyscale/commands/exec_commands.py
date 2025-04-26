import click


@click.command(
    name="exec",
    hidden=True,
    help="[DEPRECATED] Execute shell commands in interactive cluster.",
    context_settings={"ignore_unknown_options": True, "allow_extra_args": True,},
)
def anyscale_exec() -> None:
    raise click.ClickException(
        "Warning: `anyscale exec` has been deprecated and no longer works on Anyscale V2. "
        "Please use `anyscale job submit` to run your script as a job in a cluster."
    )
