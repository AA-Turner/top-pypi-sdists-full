import rich
import rich_click as click

from union.cli._app_common import DeployApplicationGroupForFiles
from union.cli._common import CommandBase
from union.remote import UnionRemote


@click.group(name="deploy")
def deploy():
    """Deploy a resource."""


app_help = """Deploy application on Union."""
app_group = DeployApplicationGroupForFiles(
    name="apps",
    help=app_help,
    command_name="deploy",
)
deploy.add_command(app_group)


@deploy.command(cls=CommandBase)
@click.argument("model_uri")
@click.option(
    "--engine",
    "-e",
    type=str,
    default="auto",
    help="Specify the engine to use for deployment. If not provided, an engine will be automatically selected."
    "Ensure the value corresponds to one of the supported engines; otherwise, an error will be returned.",
)
@click.option("--dry-run", is_flag=True, help="Print the app spec without deploying.")
def model(model_uri: str, project: str, domain: str, engine: str, dry_run: bool):
    """Deploy model on Union."""
    remote = UnionRemote(default_project=project, default_domain=domain)
    deployable_model = remote._get_deployable_model(model_uri)
    console = rich.console.Console()

    engines = []
    preferred_engine = None
    for t in deployable_model.app_templates:
        engines.append(t.engine)
        if t.preferred:
            preferred_engine = t.engine

    console.print(f"Engines: {engines}, Preferred Engine: {preferred_engine}")
    if engine != "auto":
        if engine not in engines:
            raise click.BadParameter(
                f"Engine {engine} is not supported for this model. Supported engines are: {engines}"
            )
    else:
        engine = preferred_engine

    console.print(f"Deploying model {model_uri} using engine {engine}")
    app_template = next(t for t in deployable_model.app_templates if t.engine == engine)
    app = app_template.app
    app.container_image = remote._get_deployable_engine_container(engine)

    if dry_run:
        console.print(app)
        return
    app = remote.deploy_app(app)
