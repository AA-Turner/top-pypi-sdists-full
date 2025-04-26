import os
import sys
from typing import List

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# this line should be on the top to run it on a local environment as 'python vessl/cli/_main.py'
sys.path.append(project_root)

import warnings

warnings.filterwarnings(action='ignore', module='.*paramiko.*')
warnings.filterwarnings(action='ignore', module='.*requests.*')

import click
import sentry_sdk
from click.decorators import pass_context
from sentry_sdk.integrations.logging import ignore_logger

import vessl
from vessl._version import __VERSION__
from vessl.cli._base import VesslGroup
from vessl.cli.dataset import cli as dataset_cli
from vessl.cli.experiment import cli as experiment_cli
from vessl.cli.experiment import create as experiment_create
from vessl.cli.experiment import logs as experiment_logs
from vessl.cli.hub import cli as hub_cli
from vessl.cli.kernel_cluster import cli as kernel_cluster_cli
from vessl.cli.kernel_image import cli as kernel_image_cli
from vessl.cli.kernel_resource_spec import cli as kernel_resource_spec_cli
from vessl.cli.model import model_cli, model_repository_cli
from vessl.cli.organization import cli as organization_cli
from vessl.cli.pipeline import cli as pipeline_cli
from vessl.cli.project import cli as project_cli
from vessl.cli.run import cli as run_cli
from vessl.cli.serve import alias_cli
from vessl.cli.serve import cli as serve_cli
from vessl.cli.ssh_key import cli as ssh_key_cli
from vessl.cli.storage import storage_cli
from vessl.cli.sweep import cli as sweep_cli
from vessl.cli.volume import cli as volume_cli
from vessl.cli.workspace import cli as workspace_cli
from vessl.experiment import list_github_code_refs
from vessl.run import create_run, run_from_yaml, wrap_str
from vessl.util.common import safe_cast
from vessl.util.config import DEFAULT_CONFIG_PATH, VesslConfigLoader
from vessl.util.constant import (
    ENABLE_SENTRY,
    EXPERIMENT_WORKING_DIR,
    JUPYTER,
    MISTRAL_7B,
    SENTRY_DSN,
    SSD_1B,
    VEGAART,
    VESSL_ENV,
    WHISPER_V3,
)
from vessl.util.echo import print_warning
from vessl.util.exception import (
    InvalidOrganizationError,
    InvalidProjectError,
    InvalidTokenError,
    VesslApiException,
)
from vessl.util.git_remote import clone_by_force_reset, clone_codes, clone_codes_v2
from vessl.util.prompt import prompt_choices

# Configure Sentry in production
if VESSL_ENV == "prod" and ENABLE_SENTRY:
    sentry_sdk.init(
        SENTRY_DSN,
        traces_sample_rate=1.0,
        ignore_errors=[VesslApiException],
    )
    sentry_sdk.set_tag("cli_version", __VERSION__)
    ignore_logger("vessl.util.logger")
else:
    print_warning(f"Sentry is disabled - VESSL_ENV: {VESSL_ENV}, ENABLE_SENTRY: {ENABLE_SENTRY}")


def prompt_organizations() -> str:
    organizations = vessl.list_organizations()
    organization_count = len(organizations)
    if organization_count == 1:
        return organizations[0].name

    new_organization_string = "Create new organization..."
    choices = [(x.name, i) for i, x in enumerate(organizations)] + [
        (new_organization_string, organization_count)
    ]
    choice = prompt_choices("Default organization", choices)

    if choice == organization_count:
        organization_name = click.prompt("Organization name", type=click.STRING)
        vessl.create_organization(organization_name)
    else:
        organization_name = organizations[choice].name

    return organization_name


_insecure_warning_logged = False

@click.command(cls=VesslGroup)
@click.version_option()
@pass_context
def cli(ctx: click.Context):
    global _insecure_warning_logged
    allow_insecure = safe_cast(os.environ.get('VESSL_INSECURE_SKIP_TLS_VERIFY'), bool, False)
    if allow_insecure and not _insecure_warning_logged:
        vessl.logger.warning('WARNING: VESSL_INSECURE_SKIP_TLS_VERIFY is enabled, HTTPS certificate verification is disabled. Connections may be insecure and vulnerable to man-in-the-middle attacks. Use only in trusted environments such as air-gapped systems or during development.')
        _insecure_warning_logged = True
    vessl.EXEC_MODE = "CLI"
    ctx.ensure_object(dict)


@cli.group(cls=VesslGroup, invoke_without_command=True)
@click.pass_context
@click.option("-t", "--access-token", type=click.STRING)
@click.option("-o", "--organization", type=click.STRING)
@click.option("-p", "--project", type=click.STRING)
@click.option("-f", "--credentials-file", type=click.STRING)
@click.option("--renew-token", is_flag=True)
@click.option("--reset", is_flag=True)
def configure(
    ctx,
    access_token: str,
    organization: str,
    project: str,
    credentials_file: str,
    renew_token: bool,
    reset: bool,
):
    if ctx.invoked_subcommand:
        return

    if vessl.vessl_api.is_in_run_exec_context():
        print("This environment is currently connected to VESSL with VESSL Run context.")
        print("You can manually configure VESSL SDK, but it will break some run functions (e.g. vessl.log())")
        print("Please refer https://docs.vessl.ai/api-reference/cli/getting-started#configuration-precedence.")
        return

    if reset:
        vessl.vessl_api.config_loader = VesslConfigLoader()
        vessl.vessl_api.config_loader.reset()

    try:
        vessl.configure_access_token(
            access_token=access_token,
            credentials_file=credentials_file,
            force_update=renew_token,
        )
    except InvalidTokenError:
        vessl.configure_access_token(force_update=True)

    try:
        vessl.configure_organization(
            organization_name=organization,
            credentials_file=credentials_file,
        )
    except InvalidOrganizationError:
        organization_name = prompt_organizations()
        vessl.configure_organization(organization_name)

    try:
        vessl.configure_project(
            project_name=project,
            credentials_file=credentials_file,
        )
    except InvalidProjectError:
        projects = vessl.list_projects()
        if len(projects) == 1:
            project_name = projects[0].name
        else:
            new_project_string = "Create new project..."
            project_count = len(projects)
            choices = [(x.name, i) for i, x in enumerate(projects)] + [
                (new_project_string, project_count)
            ]
            choice = prompt_choices("Default project", choices)

        if choice == project_count:
            project_name = click.prompt("Project name", type=click.STRING)
            vessl.create_project(project_name)
        else:
            project_name = projects[choice].name

        if project_name is not None:
            vessl.configure_project(project_name)

    print(f"Welcome, {vessl.vessl_api.user.display_name}!")


@cli.group(cls=VesslGroup, invoke_without_command=True)
def whoami():
    if vessl.vessl_api.is_in_run_exec_context():
        vessl.vessl_api.set_access_token(no_prompt=True)
        user = vessl.vessl_api.user
        organization_name = vessl.vessl_api.set_organization()
        project_name = vessl.vessl_api.set_project()
    else:
        config = VesslConfigLoader()
        user = None
        if config.access_token:
            vessl.vessl_api.api_client.set_default_header(
                "Authorization", f"Token {config.access_token}"
            )

            try:
                user = vessl.vessl_api.get_my_user_info_api()
            except VesslApiException:
                pass

        organization_name = config.default_organization
        project_name = config.default_project

        if user is None or organization_name is None:
            print("Please run `vessl configure` first.")
            return

    print(
        f"""Username: {user.username}
Email: {user.email}
Default organization: {organization_name}
Default project: {project_name or 'N/A'}

(The default organization and project can be updated with `vessl configure --reset`.)"""
    )


@configure.vessl_command()
@click.argument("organization", type=click.STRING, required=False)
def organization(organization: str):
    if organization is None:
        organization = prompt_organizations()
    vessl.configure_organization(organization)
    print(f"Saved to {DEFAULT_CONFIG_PATH}.")


@configure.vessl_command()
@click.argument("project", type=click.STRING, required=False)
def project(project: str):
    vessl.vessl_api.set_organization()

    if project is None:
        projects = vessl.list_projects()
        if len(projects) == 0:
            return

        project = prompt_choices("Default project", [x.name for x in projects])
    vessl.configure_project(project)
    print(f"Saved to {DEFAULT_CONFIG_PATH}.")


@configure.command()
def list():
    config = VesslConfigLoader()

    username = ""
    email = ""
    organization = config.default_organization or ""
    project = config.default_project or ""

    if config.access_token:
        vessl.vessl_api.api_client.set_default_header(
            "Authorization", f"Token {config.access_token}"
        )

        try:
            user = vessl.vessl_api.get_my_user_info_api()
            username = user.username
            email = user.email
        except VesslApiException as e:
            pass

    print(
        f"Username: {username}\n"
        f"Email: {email}\n"
        f"Organization: {organization}\n"
        f"Project: {project}"
    )


@cli.vessl_run_command()
@click.pass_context
@click.argument("command", nargs=-1)
@click.option(
    "-f",
    "--file",
    type=click.STRING,
    help="yaml file for run definition.",
)
def run(ctx, command: List[str], file: str):
    if len(command) == 0 and file == None:
        print("Missing argument")
        return
    # configure
    ctx.params = {}
    args = []
    ctx.args = configure.parse_args(ctx, args)
    ctx.forward(configure)

    if file:
        if not os.path.exists(file):
            print(wrap_str(f" Yaml does not exist! Check yaml path {file}.", "red"))
            return
        with open(file, "r") as yaml_file:
            created_run = run_from_yaml(yaml_file=yaml_file, yaml_body="", yaml_file_name=file)
    elif len(command) > 0:
        args = []
        args.extend(["--command", " ".join(command)])
        args.extend(["--working-dir", f"{EXPERIMENT_WORKING_DIR}local/"])
        args.extend(["--upload-local-file", f".:{EXPERIMENT_WORKING_DIR}local/"])

        ctx.params = {}
        ctx.args = experiment_create.parse_args(ctx, args)
        ctx.forward(experiment_create)

        experiment_number = ctx.obj.get("experiment_number")
        ctx.params = {}
        ctx.args = experiment_logs.parse_args(ctx, [str(experiment_number), "--follow"])
        ctx.forward(experiment_logs)
    else:
        pass


@cli.vessl_run_command()
@click.pass_context
def hello(ctx):
    ctx.params = {}
    args = []
    ctx.args = configure.parse_args(ctx, args)
    ctx.forward(configure)

    choices = [
        ("[Mistral-7B] Inference app built with Streamlit.", 1),
        ("[SSD-1B] Inference with Segmind's Stable Diffusion model.", 2),
        ("[Whisper-v3] Small inference on data in librispeech_asr.", 3),
        ("[Segmind VegaRT] Inference with Segmind's VegaRT.", 4),
        ("[JupyterLab] Launch a JupyterLab on GPU instance.", 5),
    ]
    choice = prompt_choices("Choose an example run", choices)
    if choice == 1:
        create_run(
            yaml_file=None, yaml_body=MISTRAL_7B, yaml_file_name="mistral-7b.yaml")
    elif choice == 2:
        create_run(
            yaml_file=None, yaml_body=SSD_1B, yaml_file_name="ssd-1b.yaml")
    elif choice == 3:
        create_run(
            yaml_file=None, yaml_body=WHISPER_V3, yaml_file_name="whisper-v3.yaml")
    elif choice == 4:
        create_run(
            yaml_file=None, yaml_body=VEGAART, yaml_file_name="vegart.yaml")
    elif choice == 5:
        create_run(
            yaml_file=None, yaml_body=JUPYTER, yaml_file_name="jupyter.yaml")


@cli.vessl_command(hidden=True)
def download_code():
    """
    This command is not for users and supposed to run on initContainers of experiment, pipeline, and workspace Pods.
    """
    workload_id = safe_cast(os.environ.get("VESSL_WORKLOAD_ID", None), int)
    if workload_id is None:
        print("Failed to download source codes: no workload id.")
        return

    resp = list_github_code_refs(workload_id)
    if resp.scheme == "v2":
        github_code_refs = resp.results_v2
        if not github_code_refs:
            print("No source code to download.")
            return
        clone_codes_v2(github_code_refs)
    else:
        github_code_refs = resp.results
        if not github_code_refs:
            print("No source code to download.")
            return
        clone_codes(github_code_refs)


@cli.vessl_command(hidden=True)
@click.option(
    "-p",
    "--path",
    type=click.STRING,
    help="target directory to import codes.",
)
def import_code(path: str):
    """
    This command is not for users and supposed to run on VESSL Run workloads.
    """
    resp = vessl.vessl_api.run_execution_get_code_ref_api(path=path)
    clone_by_force_reset(resp)


cli.add_command(dataset_cli)
cli.add_command(experiment_cli)
cli.add_command(kernel_cluster_cli)
cli.add_command(kernel_image_cli)
cli.add_command(kernel_resource_spec_cli)
cli.add_command(model_cli)
cli.add_command(model_repository_cli)
cli.add_command(organization_cli)
cli.add_command(project_cli)
cli.add_command(run_cli)
cli.add_command(serve_cli)
cli.add_command(alias_cli)
cli.add_command(ssh_key_cli)
cli.add_command(sweep_cli)
cli.add_command(volume_cli)
cli.add_command(workspace_cli)
cli.add_command(pipeline_cli)
cli.add_command(hub_cli)
cli.add_command(storage_cli)

if __name__ == "__main__":
    cli()
