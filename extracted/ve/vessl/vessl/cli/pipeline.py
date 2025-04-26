import os
import time

import click

from vessl.util.exception import VesslApiException

from vessl.util.echo import print_warning, print_info

from vessl.cli._base import VesslGroup, VesslCommand
from vessl.cli.organization import organization_name_option
from vessl.pipeline import (
    get_paused_steps,
    resume_step,
    update_context_variables,
    list_pipeline_execution,
    pipeline_execution_abort,
    resume_step_api,
    format_step,
)
from vessl.util.prompt import prompt_confirm, prompt_choices
from vessl.util.ssh import ssh_command_from_endpoint, ssh_private_key_path_callback


@click.command(name="pipeline", cls=VesslGroup)
def cli():
    pass


@cli.vessl_command()
@organization_name_option
@click.option(
    "-p",
    "--key-path",
    type=click.STRING,
    help="SSH private key path.",
    callback=ssh_private_key_path_callback,
)
@click.option(
    "--pipeline-name", "--pipeline",
    type=click.STRING,
    help="Name of the pipeline.",
)
@click.option(
    "--number", "--execution",
    type=click.INT,
    help="Pipeline execution number.",
)
@click.option(
    "--step", "step_key",
    help="Step key.",
    type=click.STRING,
)
def ssh(key_path: str, pipeline_name: str, number: int, step_key: str):
    """This commands opens ssh debugging session to selected pipeline step."""
    steps = get_paused_steps(pipeline_name=pipeline_name, execution_number=number, step_key=step_key)
    choices = []
    for step in steps:
        step_name = format_step(step)
        command = ssh_command_from_endpoint(step.run_result.run_execution.endpoints.ssh.endpoint, key_path)
        choices.append((step_name, command))
    if len(choices) == 0:
        print_info("No matching idle pipeline execution found.")
        return
    elif len(choices) == 1:
        cmd = choices[0][1]
    else:
        cmd = prompt_choices("Choose step to ssh", choices)
    print_info(cmd)
    os.system(cmd)


@cli.vessl_command()
@organization_name_option
@click.option(
    "--pipeline-name", "--pipeline",
    type=click.STRING,
    help="Name of the pipeline.",
    required=True
)
@click.option(
    "--number", "--execution",
    help="Pipeline execution number.",
    type=click.INT,
)
@click.option(
    "--yes",
    is_flag=True,
    default=False,
)
def abort(pipeline_name: str, number: int, yes):
    """This commands aborts pipeline execution of pipeline_name."""
    try:
        execs = list_pipeline_execution(pipeline_name=pipeline_name)
    except VesslApiException as e:
        if e.code == 404:
            print_warning(f"Cannot find pipeline {pipeline_name}")
        else:
            print_warning(str(e))
        return

    if number is None:
        running = [e for e in execs if e.status == 'running']
        if len(running) == 0:
            print_warning(f"No execution running for {pipeline_name}")

        choices = []
        for e in running:
            choices.append((f"{pipeline_name} (#{e.number})", e))
        target = prompt_choices("Choose execution number to abort", choices)
        number = target.number

    if not yes:
        if not prompt_confirm(f"This will abort execution {pipeline_name} (#{number}). Are you sure?"):
            return

    pipeline_execution_abort(pipeline_name, number)
    print_info(f"{pipeline_name} (#{number}) has been aborted.")


@click.command(
    name="resume",
    cls=VesslCommand,
    login_required=True,
)
@organization_name_option
@click.option(
    "--pipeline-name", "--pipeline",
    type=click.STRING,
    help="Name of the pipeline.",
    required=True,
)
@click.option(
    "--number", "--execution",
    help="Pipeline execution number.",
    type=click.INT,
)
@click.option(
    "--step", "step_key",
    help="Step key.",
    type=click.STRING,
)
@click.option(
    "--yes",
    is_flag=True,
    default=False,
)
def resume_api(pipeline_name: str, number: int, step_key: str, yes: bool):
    """This command resumes selected pipeline step."""
    steps = get_paused_steps(pipeline_name=pipeline_name, execution_number=number, step_key=step_key)
    choices = []
    for step in steps:
        x = step.context.metadata.execution
        choices.append((format_step(step), (step.id, x.execution_number)))

    if len(choices) == 0:
        print_info("No matching idle pipeline execution found.")
        return
    elif len(choices) == 1:
        exec_id, number = choices[0][1]
    else:
        exec_id, number = prompt_choices("Choose step to resume", choices)

    if not yes:
        if not prompt_confirm(f"This will resume execution {pipeline_name} (#{number}). Are you sure?"):
            return

    resume_step_api(exec_id)
    print_info(f"{pipeline_name} (#{number}) has been resumed.")


@click.command()
def resume():
    """This command resumes current pipeline step.
    Only works in pipeline debugging mode."""
    if not in_debugging_context():
        print_warning("This command only works in pipeline debugging mode")
        return

    if prompt_confirm("This will terminate current debugging session and"
                      " resume pipeline step. Are you sure?", default=True):
        with open('/opt/vessl/.exit_code', 'w') as f:
            f.write("0")
        resume_step({"exit_code": "0"})
        print_info("Step resumed. Waiting for container to be terminated....")
        while True:
            time.sleep(1000)


@click.command
@click.option('--data', '-d', multiple=True)
def set_variable(data):
    """This command changes output variable for current step.
    Only works in pipeline debugging mode."""
    if not in_debugging_context():
        print_warning("This command only works in pipeline debugging mode")
        return

    vardict = {}
    for kvpair in data:
        try:
            k, v = kvpair.split(":")
        except ValueError:
            print_info(f"Invalid format: {kvpair}")
            return
        vardict[k] = v
    update_context_variables(vardict)


def in_debugging_context():
    try:
        with open("/opt/vessl/status", 'r') as f:
            return f.read() == 'idle'
    except FileNotFoundError:
        return False


if in_debugging_context():
    cli.add_command(resume)
    cli.add_command(set_variable)
else:
    cli.add_command(resume_api)
