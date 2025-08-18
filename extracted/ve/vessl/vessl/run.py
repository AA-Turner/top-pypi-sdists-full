import datetime
import time
from typing import List, TextIO

import yaml

from vessl.openapi_client import (
    InfluxdbWorkloadLog,
    ResponseRunExecutionInfo,
    ResponseRunExecutionListResponse,
)
from vessl import vessl_api
from vessl.experiment import list_experiment_logs, read_experiment_by_id
from vessl.kernel_cluster import list_clusters
from vessl.organization import _get_organization_name
from vessl.project import _get_project_name
from vessl.util.constant import LOGO, WEB_HOST, colors
from vessl.workspace import read_workspace


def read_run(
    run_id: int,
    **kwargs,
) -> ResponseRunExecutionInfo:
    """Read run in the default organization/project. If you want to
    override the default organization/project, then pass `organization_name` or
    `project_name` as `**kwargs`.

    Args:
        run_id(int): run ID.

    Example:
        ```python
        vessl.read_run(
            run_id=123,
        )
        ```
    """
    return vessl_api.run_execution_read_api(
        execution_id=run_id,
        organization_name=_get_organization_name(**kwargs),
        project_name=_get_project_name(**kwargs),
    )


def update_run(
    run_id: int,
    description: str,
    **kwargs,
):
    """Update run in the default organization/project. If you want to
    override the default organization/project, then pass `organization_name` or
    `project_name` as `**kwargs`.

    Args:
        run_id(int): run ID.
        description(str): description of run to update.

    Example:
        ```python
        vessl.update_run(
            run_id=123,
            description="Update # of hidden layer 32->64",
        )
        ```
    """
    return vessl_api.run_execution_edit_api(
        execution_id=run_id,
        organization_name=_get_organization_name(**kwargs),
        project_name=_get_project_name(**kwargs),
        run_execution_edit_api_input={"message": description},
    )


def list_runs(
    statuses: List[str] = None,
    **kwargs,
) -> List[ResponseRunExecutionListResponse]:
    """List runs in the default organization/project. If you want to
    override the default organization/project, then pass `organization_name` or
    `project_name` as `**kwargs`.

    Args:
        statuses(List[str]): A list of status filter. Defaults to None.

    Example:
        ```python
        vessl.list_runs(
            statuses=["completed"]
        )
        ```
    """
    statuses = [",".join(statuses)] if statuses else None
    return vessl_api.run_execution_list_api(
        statuses=statuses,
        organization_name=_get_organization_name(**kwargs),
        project_name=_get_project_name(**kwargs),
    ).results


def list_run_logs(
    run_id: int,
    tail: int = 200,
    after: int = 0,
    **kwargs,
) -> List[InfluxdbWorkloadLog]:
    """List run logs in the default organization/project. If you want to
    override the default organization/project, then pass `organization_name` or
    `project_name` as `**kwargs`.

    Args:
        run_id (int): Run ID.
        tail (int): The number of lines to display from the end. Display all if
            -1. Defaults to 200.
        after (int): The number of starting lines to display from the start.
            Defaults to 0.

    Example:
        ```python
        vessl.list_run_logs(
            run_id=23,
        )
        ```
    """
    if tail == -1:
        tail = None

    return vessl_api.run_execution_logs_api(
        execution_id=run_id,
        log_limit=tail,
        organization_name=_get_organization_name(**kwargs),
        project_name=_get_project_name(**kwargs),
        log_start=after,
    ).logs


def create_run(
    yaml_file: TextIO,
    yaml_body: str,
    yaml_file_name: str,
    watch=False,
    quiet=True, # Mitigation: sdk logic which contains rich contains or print will be moved to cli
    **kwargs,
) -> ResponseRunExecutionInfo:
    """Create run in the default organization/project. If you want to
    override the default organization/project, then pass `organization_name` or
    `project_name` as `**kwargs`.

    Args:
        yaml_file (TextIO): Run ID.
        yaml_body (str): YAML body.
        yaml_file_name (str): YAML file name.
        watch (bool): Whether to watch the run.
        quiet (bool): Whether to print the log.

    Example:
        ```python
        with open(file_name, "r") as yaml_file:
            vessl.create_run(
                yaml_file=yaml_file,
                yaml_body="",
                yaml_file_name=file_name,
            )
        ```
    """
    if yaml_body == "":
        body = yaml_file.read()
    else:
        body = yaml_body
    yaml_file_name = yaml_file_name.split("/")[-1]

    wrap_str(" Launch VESSL Run 👟", "green", quiet=quiet)
    organization = _get_organization_name(**kwargs)
    project = _get_project_name(**kwargs)
    wrap_str(f"   > Organization: {organization}", "cyan", quiet=quiet)
    wrap_str(f"   > Project: {project}", "cyan", quiet=quiet)

    interactive, out_str, yaml_obj = verify_yaml(body)

    if yaml_obj == False:
        wrap_str(" YAML verification failed!", "red", quiet=quiet)
        return
    else:
        wrap_str(" YAML definition verified!", "green", quiet=quiet)
    if not quiet:
        print(out_str)
    wrap_str(f" Running: {yaml_file_name} ➡️", "green", quiet=quiet)
    # yaml_obj["run"][0]["command"] = yaml_obj["run"][0]["command"].strip()
    clean_yaml_str = yaml.dump(yaml_obj, default_flow_style=False, sort_keys=False)
    if not quiet:
        msg_box(clean_yaml_str)

    response = vessl_api.run_spec_create_from_yamlapi(
        organization_name=_get_organization_name(**kwargs),
        project_name=_get_project_name(**kwargs),
        run_spec_create_from_yamlapi_input={"yaml_spec": clean_yaml_str},
    )
    run_id = response.run_execution.id
    run_execution_response = read_run(run_id=run_id)

    link = f"{WEB_HOST}/{_get_organization_name(**kwargs)}/runs/{_get_project_name(**kwargs)}/{run_id}"
    wrap_str(
        f" Check your Run at: {link}",
        "cyan",
        quiet=False,
    )

    if not watch:
        wrap_str("   💡 Tip: Use `--watch` flag to stream logs directly to the console.", "green", quiet=quiet)
        return run_execution_response

    wrap_str(f" --watch option enabled, waiting for the Run to be scheduled...", "green", quiet=quiet)
    started = check_run_exec_started(response)
    if not started:
        return

    wrap_str(f" Showing Run logs from now:", "green", quiet=quiet)

    # fetch pod outputs
    run_finished_dt = None
    after = 0
    first_log = True
    while True:
        if read_run(run_id=run_id).status not in ["pending", "running"] and run_finished_dt is None:
            run_finished_dt = time.time()

        if run_finished_dt is not None and (time.time() - run_finished_dt) > 5:
            break

        logs = list_run_logs(
            run_id=run_id,
            before=int(time.time() - 5),
            after=after,
        )
        # do not print first log - generated while cluster was pending.
        if not first_log:
            print_logs(logs)
        else:
            first_log = False
        if len(logs) > 0:
            after = logs[-1].timestamp + 0.000001
        time.sleep(3)
    
    return run_id

def terminate_run(run_id: int, **kwargs):
    """Terminate run in the default organization/project. If you want to
    override the default organization/project, then pass `organization_name` or
    `project_name` as `**kwargs`.

    Args:
        run_id(int): Run ID.

    Example:
        ```python
        vessl.terminate_run(
            run_id=123,
        )
        ```
    """
    return vessl_api.run_execution_terminate_api(
        execution_id=run_id,
        organization_name=_get_organization_name(**kwargs),
        project_name=_get_project_name(**kwargs),
    )


def delete_run(run_id: int, **kwargs):
    """Delete run in the default organization/project. If you want to
    override the default organization/project, then pass `organization_name` or
    `project_name` as `**kwargs`.

    Args:
        run_id(int): Run ID.

    Example:
        ```python
        vessl.delete_experiment(
            run_id=123,
        )
        ```
    """
    return vessl_api.run_execution_delete_api(
        execution_id=run_id,
        organization_name=_get_organization_name(**kwargs),
        project_name=_get_project_name(**kwargs),
    )


def get_dt():
    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dt = f"{colors.GREY}[{dt}]{colors.ENDC}"
    return dt


def wrap_str(string, color="default", end="", quiet=False):
    if color == "cyan":
        wrapped = f"{get_dt()}{colors.OKCYAN}{string}{end}{colors.ENDC}"
    elif color == "green":
        wrapped = f"{get_dt()}{colors.OKGREEN}{string}{end}{colors.ENDC}"
    elif color == "red":
        wrapped = f"{get_dt()}{colors.FAIL}{string}{end}{colors.ENDC}"
    elif color == "warn":
        wrapped = f"{get_dt()}{colors.WARNING}{string}{end}{colors.ENDC}"
    else:
        wrapped = f"{get_dt()}{string}{end}"
    if not quiet:
        print(wrapped)
    else:
        return wrapped


def msg_box(msg):
    indent = 1
    lines = msg.split("\n")
    space = " " * indent
    width = max(map(len, lines))
    box = f'╔{"═" * (width + indent * 2)}╗\n'  # upper_border
    box += "".join([f"║{space}{line:<{width}}{space}║\n" for line in lines])
    box += f'╚{"═" * (width + indent * 2)}╝'  # lower_border
    print(box)


def print_logs(logs: List[str]):
    timezone = datetime.datetime.now().astimezone().tzinfo
    for log in logs:
        ts = datetime.datetime.fromtimestamp(log.timestamp, tz=timezone).strftime("%H:%M:%S.%f")
        message = (
            log.message.replace("\\r", "\r")
            .replace("\\n", "\n")
            .replace("\\b", "\b")
            .replace("\\t", "\t")
            .replace("\\u001b", "\u001b")
        )
        for x in message.split("\n"):
            print(f"[{ts}] {x}")


# Check different stuffs in verify_yaml.
def verify_yaml(yaml_str):
    # replace \t to double spaces
    yaml_str = yaml_str.replace("\t", "  ")
    yaml_obj = yaml.safe_load(yaml_str)
    out_str = ""

    # Step 1: Check if all necessary keys exist.
    necessary_keys = [["image"], ["resources"]]
    for keyset in necessary_keys:
        _yaml = yaml_obj
        for key in keyset:
            if key not in _yaml.keys():
                wrap_str(f" Field {key} does not exist! Please specify them in your yaml.", "red"),
                return False, False, False
            _yaml = _yaml[key]

    # Check interactive
    is_interactive = True if "interactive" in yaml_obj.keys() else False

    # Check resources
    yaml_resource = yaml_obj["resources"]
    if "cluster" in yaml_resource:
        # Collect possible cluster and gpus
        cluster = yaml_resource["cluster"]
        cluster_cands = list_clusters()
        cluster_ids = dict()
        cluster_gpus = dict()
        for e in cluster_cands:
            cluster_ids[e.name] = e.id
            cluster_gpus[e.name] = e.available_gpus

        # Verify cluster
        if cluster not in cluster_ids.keys():
            wrap_str(
                f" {cluster} cluster does not exist! Please select among {list(cluster_ids.keys())}.",
                "red",
            )
            return False, False, False
        else:
            out_str += wrap_str(f"   ✓ Cluster verified", "cyan", "\n", quiet=True)

    if is_interactive:
        out_str += wrap_str("   ✓ Mode: Interactive", "cyan", quiet=True)
    else:
        out_str += wrap_str("   - 💡 Mode: Batch", "cyan", quiet=True)

    return is_interactive, out_str, yaml_obj


def check_run_exec_started(response, quiet=True):
    run_id = response.run_execution.id

    not_started = True
    terminated = False
    while not_started and (not terminated):
        status = read_run(run_id=run_id).status
        if status != "pending":
            not_started = False
        if status in ["failed", "stopped"]:
            terminated = True

    if terminated:
        wrap_str(f" Run terminated!", "green", quiet=quiet)
        return False
    wrap_str(f"> Your Run is assigned to the cluster.", "green", quiet=quiet)

    not_started = True
    while not_started and (not terminated):
        status = read_run(run_id=run_id).status
        if status == "running":
            not_started = False
        if status in ["failed", "stopped"]:
            terminated = True
    if terminated:
        wrap_str(f" Run terminated!", "green", quiet=True)
        return False
    wrap_str(f"> Run has started!", "green", quiet=True)
    if not quiet:
        print(LOGO)
        wrap_str(f" VESSL Run has succesfully launched! 🚀", "green", quiet=True)
    return True