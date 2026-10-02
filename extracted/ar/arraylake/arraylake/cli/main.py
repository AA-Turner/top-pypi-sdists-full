import typer

from arraylake import __version__
from arraylake import config as config_obj
from arraylake.api_utils import set_client_name
from arraylake.cli.auth import auth
from arraylake.cli.compute import app as compute_app
from arraylake.cli.config import app as config_app
from arraylake.cli.iceberg import app as iceberg_app
from arraylake.cli.org import app as org_app
from arraylake.cli.repo import app as repo_app
from arraylake.cli.skills import app as skills_app
from arraylake.cli.utils import rich_console
from arraylake.diagnostics import get_diagnostics

app = typer.Typer(
    no_args_is_help=True,
    context_settings={"help_option_names": ["-h", "--help"]},
    rich_markup_mode="markdown",
    pretty_exceptions_show_locals=False,
)


def version_callback(value: bool):
    if value:
        rich_console.print(f"arraylake, version {__version__}")
        raise typer.Exit()


def diagnostics_callback(value: bool):
    if value:
        service_uri = config_obj.get("service.uri", None)
        diagnostics = get_diagnostics(service_uri=service_uri)
        rich_console.print(diagnostics)
        raise typer.Exit()


@app.callback()
def main(
    config: list[str] | None = typer.Option([], help="arraylake config key-value (`key=value`) pairs to pass to sub commands"),
    version: bool | None = typer.Option(None, "--version", callback=version_callback, is_eager=True, help="print Arraylake version"),
    diagnostics: bool | None = typer.Option(
        None, "--diagnostics", callback=diagnostics_callback, is_eager=True, help="print Arraylake system diagnostics"
    ),
):
    """Manage ArrayLake from the command line."""
    # Distinguish CLI usage from library usage in server access logs
    set_client_name("python-cli")
    if config:
        opts = dict(map(lambda x: x.split("="), config))
        config_obj.set(opts, priority="new")


app.add_typer(auth, name="auth")
app.add_typer(org_app, name="org")
app.add_typer(repo_app, name="repo")
app.add_typer(iceberg_app, name="iceberg")
app.add_typer(config_app, name="config")
app.add_typer(compute_app, name="compute")
app.add_typer(skills_app, name="skills")
