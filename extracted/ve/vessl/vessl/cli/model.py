import os
from datetime import datetime
from typing import List, Optional

import click

from openapi_client import ModelRepositoryCreateAPIInput, ResponseSimpleModelInfo
from vessl import list_experiment_output_files, list_experiments, vessl_api
from vessl.cli._base import (
    VesslGroup,
    vessl_argument,
    vessl_conditional_option,
    vessl_option,
)
from vessl.cli._util import (
    print_data,
  print_table,
    print_volume_files,
  truncate_datetime,
)
from vessl.util.fmt import format_size, format_url
from vessl.util.prompt import prompt_confirm, prompt_text, prompt_choices, prompt_checkbox, generic_prompter
from vessl.util.echo import print_info, print_success, print_error
from vessl.util.endpoint import Endpoint
from vessl.cli.dataset import download_dest_path_prompter
from vessl.cli.organization import organization_name_option
from vessl.cli.project import project_name_option
from vessl.experiment import read_experiment_by_id
from vessl.models.vessl_model import VesslModel
from vessl.kernel_image import get_recent_framework_and_matchin_cuda_versions
from vessl.model import (
    _make_endpoint_file_for_hf,
    create_model,
    create_model_repository,
    delete_model_volume_file,
    download_model_volume_file,
    list_model_repositories,
    list_model_volume_files,
    list_models,
    read_model,
    read_model_repository,
    upload_model_volume_file,
)
from vessl.organization import _get_organization_name
from vessl.service import serve_model
from vessl.util.constant import MODEL_SOURCE_EXPERIMENT, MODEL_SOURCE_LOCAL


def model_repository_status(latest_model: ResponseSimpleModelInfo) -> str:
    if latest_model:
        return latest_model.status
    return "Empty repository"


def model_repository_update_dt(
    latest_model: ResponseSimpleModelInfo, default: datetime
) -> datetime:
    if latest_model:
        return truncate_datetime(latest_model.created_dt)
    return truncate_datetime(default)


def model_repository_name_callback(ctx: click.Context, param: click.Parameter, value: str) -> str:
    if value:
        ctx.obj["repository"] = value
    return value


def model_repository_name_prompter(
    ctx: click.Context,
    param: click.Parameter,
    value: str,
) -> str:
    model_repositories = list_model_repositories()
    if len(model_repositories) == 0:
        raise click.UsageError(
            message="Create model repository with `vessl model-repository create`"
        )
    repository = prompt_choices("Model repository", [x.name for x in model_repositories])
    ctx.obj["repository"] = repository
    return repository


@click.command(name="model-repository", cls=VesslGroup)
def model_repository_cli():
    pass


@model_repository_cli.vessl_command()
@vessl_argument("name", type=click.STRING, required=True, prompter=model_repository_name_prompter)
@organization_name_option
def read(name: str):
    model_repository = read_model_repository(repository_name=name)
    print_data(
        {
            "ID": model_repository.id,
            "Name": model_repository.name,
            "Description": model_repository.description,
            "Status": model_repository_status(model_repository.model_summary.latest_model),
            "Organization": model_repository.organization.name,
            "Created": truncate_datetime(model_repository.created_dt),
            "Updated": truncate_datetime(model_repository.updated_dt),
        }
    )
    print_info(
        f"For more info: {format_url(Endpoint.model_repository.format(model_repository.organization.name, model_repository.name))}"
    )


@model_repository_cli.vessl_command()
@organization_name_option
@vessl_option(
    "--limit",
    type=click.INT,
    required=False,
    default=None,
)
def list(limit: Optional[int]):
    model_repositories = list_model_repositories(limit=limit)
    print_table(
        model_repositories,
        ["Name", "Status", "Models", "Created", "Updated"],
        lambda x: [
            x.name,
            model_repository_status(x.model_summary.latest_model),
            x.model_summary.total,
            truncate_datetime(x.created_dt),
            model_repository_update_dt(x.model_summary.latest_model, x.updated_dt),
        ],
    )


@model_repository_cli.vessl_command()
@vessl_argument(
    "name",
    type=click.STRING,
    required=True,
    prompter=generic_prompter("Model repository name"),
)
@click.option("-m", "--description", type=click.STRING)
@organization_name_option
def create(
    name: str,
    description: str,
):
    model_repository = create_model_repository(
        name=name,
        description=description,
    )
    print_success(
        f"Created '{model_repository.name}'.\n"
        f"For more info: {format_url(Endpoint.model_repository.format(model_repository.organization.name, model_repository.name))}"
    )


def model_number_prompter(
    ctx: click.Context,
    param: click.Parameter,
    value: int,
) -> int:
    repository = ctx.obj.get("repository")
    if repository is None:
        raise click.BadArgumentUsage(
            message="Argument `REPOSITORY_NAME` must be specified before `MODEL_NUMBER`.",
        )
    models = list_models(repository_name=repository)
    return prompt_choices("Model", [x.number for x in models])


@click.command(name="model", cls=VesslGroup)
def model_cli():
    pass


@model_cli.vessl_command()
@vessl_argument(
    "repository_name",
    type=click.STRING,
    required=True,
    prompter=model_repository_name_prompter,
    callback=model_repository_name_callback,
)
@vessl_argument(
    "model_number",
    type=click.INT,
    required=True,
    prompter=model_number_prompter,
)
@click.option(
    "--install-reqs",
    type=click.BOOL,
    is_flag=True,
    help="Install requirements before serving.",
)
@click.option(
    "--remote",
    type=click.BOOL,
    is_flag=True,
    hidden=True,
)
@organization_name_option
def serve(repository_name: str, model_number: int, install_reqs: bool, remote: bool):
    serve_model(repository_name, model_number, install_reqs, remote)


@model_cli.vessl_command()
@vessl_argument(
    "repository_name",
    type=click.STRING,
    required=True,
    prompter=model_repository_name_prompter,
    callback=model_repository_name_callback,
)
@vessl_argument(
    "model_number",
    type=click.INT,
    required=True,
    prompter=model_number_prompter,
)
@organization_name_option
def read(repository_name: str, model_number: int):
    model = read_model(repository_name=repository_name, model_number=model_number)
    experiment_numbers = []
    if model.experiment:
        experiment_numbers.append(model.experiment.number)

    metrics_summary = "None"
    if model.metrics_summary:
        metrics_keys = model.metrics_summary.latest.keys()
        metrics_summary = {}
        for key in metrics_keys:
            metrics_summary[key] = model.metrics_summary.latest[key].value

    print_data(
        {
            "ID": model.id,
            "Number": model.number,
            "Name": model.name,
            "Status": model.status,
            "Related experiments": experiment_numbers,
            "Creator": model.created_by.username,
            "Created": truncate_datetime(model.created_dt),
            "Metrics summary": metrics_summary,
        }
    )
    print_info(
        f"For more info: {format_url(Endpoint.model.format(model.model_repository.organization.name, model.model_repository.name, model.number))}"
    )


@model_cli.vessl_command()
@vessl_argument(
    "repository",
    type=click.STRING,
    required=True,
    prompter=model_repository_name_prompter,
)
@organization_name_option
def list(repository: str):
    models = list_models(repository_name=repository)
    print_table(
        models,
        ["Number", "Created", "Status"],
        lambda x: [x.number, truncate_datetime(x.created_dt), x.status],
    )


@model_cli.vessl_command()
@vessl_argument(
    "repository_name",
    type=click.STRING,
    required=True,
    prompter=model_repository_name_prompter,
)
@vessl_argument(
    "model_number",
    type=click.INT,
    required=True,
    prompter=model_number_prompter,
)
@click.option("-p", "--path", type=click.Path(), default="", help="Defaults to root.")
@click.option("-r", "--recursive", is_flag=True)
@organization_name_option
def list_files(repository_name: str, model_number: int, path: str, recursive: bool):
    files = list_model_volume_files(
        repository_name=repository_name,
        model_number=model_number,
        need_download_url=False,
        path=path,
        recursive=recursive,
    )
    print_volume_files(files)


def model_source_prompter(
    ctx: click.Context,
    param: click.Parameter,
    value: str,
) -> str:
    return prompt_choices(
        "Source",
        [
            ("From an experiment", MODEL_SOURCE_EXPERIMENT),
            ("From local files", MODEL_SOURCE_LOCAL),
        ],
    )


def model_source_callback(
    ctx: click.Context,
    param: click.Parameter,
    value: str,
):
    if value:
        ctx.obj["model_source"] = value
    return value


def experiment_id_prompter(
    ctx: click.Context,
    param: click.Parameter,
    value: int,
) -> int:
    model_source = ctx.obj.get("model_source")
    if model_source is None:
        raise click.BadOptionUsage(
            option_name="--source",
            message="Model source (`--source`) must be specified before experiment_id (`--experiment-id`).",
        )
    if model_source == MODEL_SOURCE_EXPERIMENT:
        experiments = list_experiments(statuses=["completed"])
        experiment = prompt_choices(
            "Experiment",
            [(f"{x.name} #{x.number}", x) for x in reversed(experiments)],
        )
        ctx.obj["experiment_number"] = experiment.number
        return experiment.id


def experiment_id_callback(
    ctx: click.Context,
    param: click.Parameter,
    value: int,
):
    if value and "experiment_number" not in ctx.obj:
        experiment = read_experiment_by_id(value)
        ctx.obj["experiment_number"] = experiment.number
    return value


def paths_prompter(
    ctx: click.Context,
    param: click.Parameter,
    value: List[str],
) -> List[str]:
    model_source = ctx.obj.get("model_source")
    if model_source is None:
        raise click.BadOptionUsage(
            option_name="--source",
            message="Model source (`--source`) must be specified before experiment_id (`--experiment-id`).",
        )
    paths = ["/"]
    if model_source == MODEL_SOURCE_EXPERIMENT:
        experiment_number = ctx.obj.get("experiment_number")
        if experiment_number is None:
            raise click.BadOptionUsage(
                option_name="--experiment-id",
                message="Experiment id (`--experiment-id`) must be specified before paths (`--paths`).",
            )
        files = list_experiment_output_files(
            experiment_number=experiment_number,
            need_download_url=False,
            recursive=True,
            worker_number=0,
        )
        if len(files) > 0:
            paths = prompt_checkbox(
                "Paths (Press -> to select and <- to unselect)",
                choices=[(f"{x.path} {format_size(x.size)}", x.path) for x in files],
            )
            if len(paths) == 0:
                paths = ["/"]

    return paths


@model_cli.vessl_command()
@vessl_argument(
    "repository_name",
    type=click.STRING,
    required=True,
    prompter=model_repository_name_prompter,
)
@vessl_option("--model-name", type=click.STRING, help="Model name.")
@vessl_option(
    "--source",
    type=click.STRING,
    expose_value=False,
    prompter=model_source_prompter,
    callback=model_source_callback,
    help=f"{MODEL_SOURCE_EXPERIMENT} or {MODEL_SOURCE_LOCAL}.",
)
@vessl_option(
    "--experiment-id",
    type=click.INT,
    prompter=experiment_id_prompter,
    callback=experiment_id_callback,
    help=f"Experiment id to create model (only works for {MODEL_SOURCE_EXPERIMENT}).",
)
@vessl_option(
    "--path",
    type=click.STRING,
    multiple=True,
    prompter=paths_prompter,
    help=f"Path to create model (only works for {MODEL_SOURCE_EXPERIMENT}). Default: `/`",
)
@organization_name_option
@project_name_option
def create(
    repository_name: str,
    model_name: str = None,
    experiment_id: int = None,
    repository_description: str = None,
    path: str = None,
):
    model = create_model(
        repository_name=repository_name,
        repository_description=repository_description,
        experiment_id=experiment_id,
        model_name=model_name,
        paths=path,
    )
    print_success(
        f"Created '{model.model_repository.name}-{model.number}'.\n"
        f"For more info: {format_url(Endpoint.model.format(model.model_repository.organization.name, model.model_repository.name, model.number))}"
    )


@model_cli.vessl_command()
@vessl_argument(
    "repository_name",
    type=click.STRING,
    required=True,
    prompter=model_repository_name_prompter,
    callback=model_repository_name_callback,
)
@vessl_argument(
    "model_number",
    type=click.INT,
    required=True,
    prompter=model_number_prompter,
)
@vessl_argument(
    "source",
    type=click.Path(exists=True),
    required=True,
    prompter=generic_prompter("Source path"),
)
@vessl_argument(
    "dest",
    type=click.Path(),
    required=True,
    prompter=generic_prompter("Destination path", default="/"),
)
@organization_name_option
def upload(repository_name: str, model_number: int, source: str, dest: str):
    upload_model_volume_file(
        repository_name=repository_name,
        model_number=model_number,
        source_path=source,
        dest_path=dest,
    )
    print_success(f"Uploaded {source} to {dest}.")


@model_cli.vessl_command()
@vessl_argument(
    "repository_name",
    type=click.STRING,
    required=True,
    prompter=model_repository_name_prompter,
    callback=model_repository_name_callback,
)
@vessl_argument(
    "model_number",
    type=click.INT,
    required=True,
    prompter=model_number_prompter,
)
@vessl_argument(
    "source",
    type=click.Path(),
    required=True,
    prompter=generic_prompter("Source path", default="/"),
)
@vessl_argument(
    "dest",
    type=click.Path(),
    required=True,
    prompter=download_dest_path_prompter,
)
@organization_name_option
def download(repository_name: str, model_number: int, source: str, dest: str):
    download_model_volume_file(
        repository_name=repository_name,
        model_number=model_number,
        source_path=source,
        dest_path=dest,
    )
    print_success(f"Downloaded {source} to {dest}.")


@model_cli.vessl_command()
@vessl_argument(
    "repository_name",
    type=click.STRING,
    required=True,
    prompter=model_repository_name_prompter,
    callback=model_repository_name_callback,
)
@vessl_argument(
    "model_number",
    type=click.INT,
    required=True,
    prompter=model_number_prompter,
)
@vessl_argument("path", type=click.Path(), required=True, prompter=generic_prompter("File path"))
@organization_name_option
def delete_file(repository_name: str, model_number: int, path: str):
    delete_model_volume_file(
        repository_name=repository_name,
        model_number=model_number,
        path=path,
    )
    print_success(f"Deleted {path}.")


@model_cli.vessl_command()
@vessl_option(
    "--type",
    type=click.Choice(["vessl", "bento", "hf-transformers", "hf-diffusers"], case_sensitive=False),
    required=True,
    default="vessl",
    help="Type of model to register. (vessl, bento, hf-transformers, hf-diffusers)",
    prompt="Type of model to register",
)
@vessl_conditional_option(
    "--weight_name_or_path",
    type=click.STRING,
    help="Name or path of model weight. Required when the model type is huggingface",
    prompt="Name or path of model weight",
    condition=("type", ["hf-transformers", "hf-diffusers"]),
)
@vessl_option(
    "--repository_name",
    type=click.STRING,
    help="Model repository name.",
)
@vessl_option(
    "--model_number",
    type=click.INT,
    default=None,
    help="Model number (optional). If not provided, will be auto-incremented.",
)
@vessl_option(
    "--entrypoint",
    type=click.STRING,
    default=None,
    help="Entrypoint for the model. e.g. python service.py, bentoml serve model:ModelClass \n If not provided, auto-generation will be attempted.",
)
@vessl_option(
    "--python_version",
    type=click.STRING,
    default=None,
    help="Python version for the model running.",
)
@vessl_option(
    "--requirements_path",
    type=click.STRING,
    default=None,
    help="Path to requirements file. Needed for installing dependencies.",
)
@vessl_option(
    "--pyproject_path",
    type=click.STRING,
    default=None,
    help="Path to pyproject.toml file. Needed for installing dependencies.",
)
@vessl_option(
    "--cuda_version",
    type=click.STRING,
    default=None,
    help="CUDA version for the model running.",
)
@vessl_option(
    "--framework_type",
    type=click.Choice(["torch", "tensorflow"], case_sensitive=False),
    default=None,
    help="Framework type for the model running.",
)
@vessl_option(
    "--pytorch_version",
    type=click.STRING,
    default=None,
    help="PyTorch version for the model running.",
)
@vessl_option(
    "--tensorflow_version",
    type=click.STRING,
    default=None,
    help="TensorFlow version for the model running.",
)
@vessl_option(
    "-y",
    "--autocreate",
    is_flag=True,
    type=click.BOOL,
    default=False,
    help="Auto apply arguments if not provided.",
)
@vessl_option(
    "-d",
    "--dry-run",
    is_flag=True,
    type=click.BOOL,
    default=False,
    help="Dry run without registering. Only creates lockfile.",
)
@organization_name_option
def register(
    type,
    weight_name_or_path,
    repository_name,
    entrypoint,
    model_number,
    python_version,
    requirements_path,
    pyproject_path,
    cuda_version,
    framework_type,
    pytorch_version,
    tensorflow_version,
    autocreate,
    dry_run,
    **kwargs,
):
    if repository_name is None:
        repositories = list_model_repositories(limit=20)
        if len(repositories) == 0:
            if prompt_confirm("Model repository does not exist. Create?", default=True):
                repository_name = prompt_text("Model repository name")
                create_model_repository(repository_name)
                print_info(f"Created model repository {repository_name}.")
            else:
                return
        else:
            repository_name = prompt_choices("Model repository", [x.name for x in repositories])
    if os.path.exists(".vessl.model.lock") and not autocreate:
        if not prompt_confirm("Lockfile exists. Overwrite?", default=True):
            print_info("Exiting.")
            return

    if entrypoint is None:
        entrypoint = _generate_entrypoint(type, autocreate)

    if type in ("hf-transformers", "hf-diffusers"):
        # file_path = entrypoint.split(" ")[-1]
        file_path = "service.py"
        print_info(
            f"Model type is huggingface model. {file_path} file will be automatically generated."
        )
        if (
            not os.path.exists(file_path)
            or autocreate
            or prompt_confirm(f"{file_path} already exists. Overwrite?")
        ):
            _make_endpoint_file_for_hf(type, weight_name_or_path, file_path)
        else:
            print_info(f"Skipping generation of {file_path}.")

    if python_version is None:
        detected_version = ".".join(
            os.popen("python --version")
            .read()
            .strip()
            .split(" ")[1]
            .split(".")[0:2]  ## only MAJOR.MINOR version
        )
        if not autocreate:
            python_version = prompt_text(
                f"Python version? (detected: {detected_version})", default=detected_version
            )
        else:
            python_version = detected_version

    if framework_type is None:
        if autocreate:
            print_error("Framework type is required.")
            raise ValueError("Framework type is required.")
        framework_type = prompt_choices("Framework type", ["torch", "tensorflow"])

    matching_cuda_versions = []
    if framework_type == "torch" and  pytorch_version is None:
        framework_cuda_version_map = get_recent_framework_and_matchin_cuda_versions("torch")
        pytorch_version = prompt_choices("PyTorch version? (contact support@vessl.ai if you cannot find expected.)", framework_cuda_version_map.keys())
        matching_cuda_versions = framework_cuda_version_map[pytorch_version]
    elif framework_type == "tensorflow" and tensorflow_version is None:
        framework_cuda_version_map = get_recent_framework_and_matchin_cuda_versions("tensorflow")
        tensorflow_version = prompt_choices("TensorFlow version? (contact support@vessl.ai if you cannot find expected.)", framework_cuda_version_map.keys())
        matching_cuda_versions = framework_cuda_version_map[tensorflow_version]

    if cuda_version is None:
        if autocreate:
            print_error("CUDA version is required.")
            raise ValueError("CUDA version is required.")
        cuda_version = prompt_choices("CUDA version?", matching_cuda_versions)
        if cuda_version == "":
            print_error("CUDA version is required.")
            return

    (requirements_path, pyproject_path) = _get_requirement_or_pyproject(
        requirements_path, pyproject_path
    )
    if requirements_path is None and pyproject_path is None:
        print_error("Either requirements file or pyproject.toml is required.")
        return

    if model_number is None and not autocreate:
        model_number = prompt_text("Model number (optional)", default=None)

    if model_number is not None:
        try:
            existing_model = vessl_api.model_read_api(
                organization_name=_get_organization_name(**kwargs),
                repository_name=repository_name,
                number=model_number,
            )
            model_number = existing_model.number
        except Exception as e:
            print_error(f"Model {model_number} does not exist.")
            return

    if model_number is None:
        model_number = "supplied_when_registering"

    vessl_model = VesslModel.create(
        type=type,
        repository_name=repository_name,
        model_number=model_number,
        entrypoint=entrypoint,
        python_version=python_version,
        weight_name_or_path=weight_name_or_path,
        requirements_path=requirements_path,
        pyproject_path=pyproject_path,
        cuda_version=cuda_version,
        framework_type=framework_type,
        pytorch_version=pytorch_version,
        tensorflow_version=tensorflow_version,
        autocreate_repository=autocreate,
    )

    VesslModel.create_ignore_file()
    print_info("Generated ignore file.")
    if dry_run or not prompt_confirm("Register and upload current directory as model?", default=True):
        vessl_model.save_lockfile()
        print_info("Saved lockfile. Exiting.")
        return

    if model_number == "supplied_when_registering":
        print_info("Creating a new model.")
        created_model = vessl_api.model_create_api(
            organization_name=_get_organization_name(**kwargs),
            repository_name=repository_name,
        )
        model_number = created_model.number
        print_info(f"Created a new model with number {model_number}.")

    vessl_model.model_number = model_number
    vessl_model.save_lockfile()
    print_info("Lockfile saved.")

    try:
        repo = read_model_repository(repository_name=repository_name)
    except Exception as e:
        repo = None
    if repo is None:
        if autocreate:
            create_model_repository(repository_name)
        else:
            if prompt_confirm("Model repository does not exist. Create?", default=True):
                vessl_api.model_repository_create_api(
                    organization_name=_get_organization_name(**kwargs),
                    model_repository_create_api_input=ModelRepositoryCreateAPIInput(
                        name=repository_name,
                    ),
                )
            else:
                print_info("Model repository not created. Exiting.")
                print_info(
                    "Use `vessl model-repository create` to create a model repository first."
                )
                return

    src_path = f"{os.getcwd()}"
    print_info(f"{repository_name}-{model_number} {src_path} /")
    upload_model_volume_file(
        repository_name=repository_name,
        model_number=model_number,
        source_path=src_path,
        dest_path="/",
    )
    print_success(f"Registered {repository_name}-{model_number}.")


def _generate_entrypoint(input_type: str, auto) -> str:
    candidate = ""
    if input_type == "vessl":
        candidate = "vessl model launch service.py:Service -p 3000"
    elif input_type == "bento":
        candidate = "bentoml serve service:Service"
    elif input_type == "hf-transformers":
        candidate = "vessl model launch service.py:HfTransformerRunner -p 3000"
    elif input_type == "hf-diffusers":
        candidate = "vessl model launch service.py:HfDiffuserRunner -p 3000"
    if auto:
        return candidate
    if not auto and prompt_confirm(
        f"Generating entrypoint as `{candidate}`. Proceed? (No to input manually)", default=True
    ):
        target_file = "service.py" ## As every generated case uses service.py
        if not os.path.exists(target_file) and (input_type == "vessl" or input_type == "bento"):
            print_error(f"{target_file} does not exist. Please create the file first.")
            raise click.Abort()

        return candidate
    return prompt_text("Input entrypoint command")


def _get_requirement_or_pyproject(requirements_path, pyproject_path):
    if requirements_path is not None and requirements_path != "":
        return (requirements_path, None)
    if pyproject_path is not None and pyproject_path != "":
        return (None, pyproject_path)

    if requirements_path is None:
        detected_req = None
        if os.path.exists("requirements.txt"):
            detected_req = "requirements.txt"
        requirements_path = prompt_text(
            f"Path to requirements file? [detected: {detected_req}] (optional, press Enter to skip)",
            default=detected_req,
        )
        if requirements_path != "":
            return (requirements_path, None)

    if pyproject_path is None:
        detected_pyproject = None
        if os.path.exists("pyproject.toml"):
            detected_pyproject = "pyproject.toml"
        pyproject_path = prompt_text(
            f"Path to pyproject.toml file? [detected: {detected_pyproject}] (optional, press Enter to skip)",
            default=detected_pyproject,
        )
        if pyproject_path != "":
            return (None, pyproject_path)

    return (None, None)


@model_cli.vessl_command(
    help="""
    Launch model by local entrypoint. This uses .vessl.model.lock file to install dependencies.

    So you need to run `vessl model register` before launching the model.

    Directly launch model without referencing a model repository, which is the main difference from `vessl model serve` where it looks up model repository and pulls the specified model number to start.

    Also, this command only supports Runnerbase models.

    Example:

    $ vessl model launch service.py:Service
    $ vessl model launch service:Service

    """
)
@vessl_argument(
    "entrypoint",
    type=click.STRING,
    required=True,
    prompter=generic_prompter("entrypoint"),
)
@vessl_option(
    "-d",
    "--local",
    is_flag=True,
    help="Launch model locally.",
    default=False,
)
@vessl_option(
    "-p",
    "--port",
    type=click.INT,
    help="Port number to launch model. [default: 8000]",
    default=8000,
)
def launch(entrypoint: str, local: bool, port: int):
    if not os.path.exists(".vessl.model.lock"):
        print_error("Lockfile does not exist.")
        return

    filename, classname = entrypoint.split(":")
    if not os.path.exists(f"{filename}") and not os.path.exists(f"{filename}.py"):
        print_error(f"{filename} does not exist.")
        return

    lockfile = VesslModel.from_lockfile(".vessl.model.lock")
    lockfile.install_deps()
    lockfile.launch_model(filename, classname, remote=not local, port=port)
