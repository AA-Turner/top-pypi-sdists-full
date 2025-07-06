import importlib
import importlib.util
import inspect
import json
import logging
import os
import shutil
import subprocess
import sys
import traceback
import zipfile
from pathlib import Path
from typing import Callable, List, Optional, Tuple
from uuid import uuid4

import click

from . import __version__
from .build_config import get_build_config_for_stage
from .controller import AsyncLambdaController
from .env import enable_force_sync_mode
from .models.mock.mock_context import MockLambdaContext
from .models.mock.mock_event import MockAPILambdaEvent, MockSQSLambdaEvent
from .models.task import TaskTriggerType
from .util import nested_update


@click.group()
@click.option("-d", "--debug", help="Turn on debug logs", is_flag=True, default=False)
def cli(debug: bool):
    """
    async-lambda CLI. For building async-lambda applications.
    """
    if debug:
        logging.basicConfig(level=logging.INFO)


def import_module(module_name: str):
    project_dir = os.getcwd()
    vendor_dir = os.path.join(project_dir, "vendor")
    if os.path.exists(vendor_dir) and os.path.isdir(vendor_dir):
        sys.path.insert(0, vendor_dir)
    if project_dir not in sys.path:
        sys.path.insert(0, project_dir)
    return importlib.import_module(module_name)


def import_module_get_controller(module_name: str, config, stage: Optional[str]):
    build_config = get_build_config_for_stage(config, stage=stage)
    os.environ.update(build_config.environment_variables)
    os.environ["ASYNC_LAMBDA_BUILD_MODE"] = "1"
    app = import_module(module_name)
    controller = None
    for member, value in inspect.getmembers(app):
        if member[:2] == "__":
            continue
        if isinstance(value, AsyncLambdaController) and not value.is_sub:
            controller = value
            break

    if controller is None:
        raise Exception(
            f"No AsyncLambdaController instance found in the module: {module_name}"
        )
    return controller


@cli.command()
@click.argument("module")
@click.option("-s", "--stage", help="The stage to build the app for.")
@click.option(
    "-o",
    "--output",
    default="template.json",
    help="The name of the file for the output template.",
)
@click.option(
    "-e", "--extras", help="The path to a json file to merge the output template with."
)
def build(
    module: str, output: str, stage: Optional[str] = None, extras: Optional[str] = None
):
    """
    Builds/generates the SAM template for the given module.
    """
    dir = Path.cwd()
    config = {}
    config_file = dir.joinpath(".async_lambda/config.json")
    if config_file.exists():
        config = json.loads(config_file.read_bytes())
    controller = import_module_get_controller(
        module_name=module, config=config, stage=stage
    )

    extras_json = None
    if extras is not None:
        extras_file = dir.joinpath(extras)
        if not extras_file.exists():
            raise click.ClickException(
                f"Unable to find extras file {extras_file.as_posix()}"
            )
        click.echo("Collecting extras...")
        try:
            extras_json = json.loads(extras_file.read_text())
        except json.JSONDecodeError:
            click.echo(traceback.format_exc(), err=True)
            raise click.ClickException("Extras file contains invalid formatted data.")
        if not isinstance(extras_json, dict):
            raise click.ClickException("Extras file contains invalid formatted data.")

    click.echo("Generating SAM template...")
    template = controller.generate_sam_template(module, config, stage=stage)
    if extras_json is not None:
        click.echo("Merging template with extras...")
        nested_update(template, extras_json)
    click.echo(f"Writing template to {output}...")
    with open(os.path.join(os.getcwd(), output), "w") as template_file:
        template_file.write(
            json.dumps(
                template,
                indent=2,
            )
        )

    if os.path.exists(".async_lambda/build"):
        shutil.rmtree(".async_lambda/build")
    os.makedirs(".async_lambda/build/packages", exist_ok=True)

    if dir.joinpath("requirements.txt").exists():
        click.echo("Installing dependencies (requirements.txt) in build folder...")
        subprocess.check_call(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "-r",
                "requirements.txt",
                "--target",
                ".async_lambda/build/packages",
                "--upgrade",
            ]
        )

    click.echo("Bundling build zip file...")
    zip_file_name = ".async_lambda/build/deployment.zip"
    with zipfile.ZipFile(zip_file_name, "w") as z:
        entrypoint = dir.joinpath(f"{module}.py")
        z.write(entrypoint, entrypoint.relative_to(dir))

        src_dir = dir.joinpath("src")
        for entry in src_dir.rglob("*"):
            z.write(entry, entry.relative_to(dir))

        packages_dir = dir.joinpath(".async_lambda", "build", "packages")
        for entry in packages_dir.rglob("*"):
            if entry.match("*__pycache__*"):
                continue
            z.write(entry, entry.relative_to(packages_dir))

        app_vendor_dir = dir.joinpath("vendor")
        for entry in app_vendor_dir.rglob("*"):
            z.write(entry, entry.relative_to(app_vendor_dir))

    click.echo(f"Created zip bundle {zip_file_name}")


@cli.command()
@click.argument("module")
@click.option("-s", "--stage", help="The stage to ls the app for.")
def ls(module: str, stage: Optional[str] = None):
    dir = Path.cwd()
    config = {}
    config_file = dir.joinpath(".async_lambda/config.json")
    if config_file.exists():
        config = json.loads(config_file.read_bytes())
    controller = import_module_get_controller(
        module_name=module, config=config, stage=stage
    )
    task_ids = sorted(controller.tasks.keys())
    for task_id in task_ids:
        click.echo(f"{task_id} | {controller.tasks[task_id].trigger_type.name}")


@cli.command()
@click.argument("module")
@click.argument("task-id")
@click.option(
    "-b",
    "--body",
    help="The body or payload to pass into the task. Not valid for Scheduled Tasks.",
)
@click.option("-q", "--query-string", help="The querystring to pass into the API Task.")
@click.option(
    "-h", "--header", help="A header to attach to the API Task.", nargs=2, multiple=True
)
@click.option("-s", "--stage", help="The stage to run the app for.")
def invoke(
    module: str,
    task_id: str,
    body: Optional[str] = None,
    query_string: Optional[str] = None,
    header: Optional[List[Tuple[str, str]]] = None,
    stage: Optional[str] = None,
):
    """
    Invoke a task in local sync mode.
    """
    dir = Path.cwd()
    config = {}
    config_file = dir.joinpath(".async_lambda/config.json")
    if config_file.exists():
        config = json.loads(config_file.read_bytes())
    controller = import_module_get_controller(
        module_name=module, config=config, stage=stage
    )
    if task_id not in controller.tasks:
        raise click.ClickException(f"Task '{task_id}' not found.")

    task = controller.tasks[task_id]
    mock_context = MockLambdaContext(task.get_function_name())
    if task.trigger_type == TaskTriggerType.UNMANAGED_SQS:
        mock_event = MockSQSLambdaEvent(body or "")
    elif task.trigger_type in [
        TaskTriggerType.MANAGED_SQS,
        TaskTriggerType.MANAGED_SQS_BATCH,
    ]:
        sqs_payload = json.dumps(
            {
                "source_task_id": None,
                "destination_task_id": task_id,
                "invocation_id": uuid4().hex,
                "payload": json.dumps(body),
            }
        )
        mock_event = MockSQSLambdaEvent(sqs_payload)
    elif task.trigger_type == TaskTriggerType.SCHEDULED_EVENT:
        mock_event = {}
    elif task.trigger_type == TaskTriggerType.API_EVENT:
        mock_event = MockAPILambdaEvent(
            task.trigger_config["path"],
            task.trigger_config["method"],
            body=body,
            query_string=query_string,
            headers=header,
        )
    else:
        raise click.ClickException(f"Unknown task type {task.trigger_type}.")

    enable_force_sync_mode()
    controller.handle_invocation(mock_event, mock_context, task_id=task_id)


@cli.command()
@click.argument("module")
@click.option("-p", "--port", type=int, default=8000)
@click.option("-h", "--host", default="127.0.0.1")
@click.option("-s", "--stage", help="The stage to run the app for.")
def web_server(module: str, port: int, host: str, stage: Optional[str] = None):
    """
    Starts a web-server which serves any APITasks over Flask.
    """
    dir = Path.cwd()
    config = {}
    config_file = dir.joinpath(".async_lambda/config.json")
    if config_file.exists():
        config = json.loads(config_file.read_bytes())
    controller = import_module_get_controller(
        module_name=module, config=config, stage=stage
    )
    from flask import Flask, Response, jsonify, request

    enable_force_sync_mode()
    app = Flask(__name__)

    for task in controller.tasks.values():
        if task.trigger_type != TaskTriggerType.API_EVENT:
            continue

        path = task.trigger_config["path"]
        method = task.trigger_config["method"]
        function_name = task.get_function_name()
        task_id = task.task_id

        def make_route(function_name: str, task_id: str) -> Callable:
            def route():
                mock_event = MockAPILambdaEvent(
                    path,
                    method,
                    body=request.get_data(as_text=True),
                    query_string=request.query_string.decode(),
                    headers=[
                        (
                            key,
                            value,
                        )
                        for key, value in request.headers.items()
                    ],
                )
                mock_context = MockLambdaContext(
                    function_name,
                )

                response = controller.handle_invocation(
                    mock_event, mock_context, task_id=task_id
                )

                if isinstance(response, dict):
                    status_code = response.get("statusCode")
                    headers = response.get("headers")
                    body = response.get("body")
                    if body is not None:
                        body = str(body)

                    if (
                        len(set(response.keys()) - {"statusCode", "headers", "body"})
                        == 0
                    ):
                        return Response(
                            response=body,
                            status=status_code,
                            headers=headers,
                        )

                return jsonify(response)

            route.__name__ = function_name
            return route

        app.add_url_rule(
            rule=path,
            methods=[method],
            view_func=make_route(function_name=function_name, task_id=task_id),
        )

    app.run(host=host, port=port, debug=True)


@cli.command()
def version():
    """
    Returns the current version of this package.
    """
    click.echo(f"async-lambda-unstable {__version__}")


if __name__ == "__main__":
    cli()
