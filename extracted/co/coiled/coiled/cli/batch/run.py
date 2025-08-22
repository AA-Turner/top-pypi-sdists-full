from __future__ import annotations

import datetime
import gzip
import json
import logging
import os
import re
import shlex

import click
import dask.config
from dask.utils import format_bytes, format_time, parse_timedelta
from rich.console import Console
from rich.panel import Panel

import coiled
from coiled.cli.curl import sync_request
from coiled.cli.run import dict_from_key_val_list
from coiled.cli.utils import CONTEXT_SETTINGS, fix_path_for_upload
from coiled.credentials.aws import get_aws_local_session_token
from coiled.utils import COILED_LOGGER_NAME, error_info_for_tracking, supress_logs

console = Console(width=80)

# Be fairly flexible in how we parse options in header, i.e., we allow:
# "#COILED"
# "# COILED"
# then ":" and/or " "
# then you can specify key as "key" or "--key"
# key/val pair as "key val" or "key=val"
# or just "key" if it's a flag
HEADER_REGEX = re.compile(r"^\s*(# ?COILED)[\s:-]+([\w_-]+)([ =](.+))?")

UPLOAD_FILE_TYPES = [".py", ".sh", ".yml", ".yaml", ".txt", ".csv", ".tsv", ".json"]


def parse_array_string(array):
    try:
        # is the input a single number?
        return [int(array)]
    except ValueError:
        ...

    if "," in array:
        # if we get a comma separated list, recursively parse items in the list
        result = []
        for a in array.split(","):
            result.extend(parse_array_string(a))
        return result

    array_range = array.split("-")
    if len(array_range) == 2:
        start, end = array_range
        skip = 1
        try:
            if len(end.split(":")) == 2:
                end, skip = end.split(":")
                skip = int(skip)
            start = int(start)
            end = int(end)
        except ValueError:
            ...
        else:
            # no value error so far
            if start > end:
                # can't have this inside the try or else it would be caught
                raise ValueError(
                    f"Unable to parse '{array}' as a valid array range, start {start} is greater than end {end}."
                )
            return list(range(start, end + 1, skip))

    raise ValueError(f"Unable to parse '{array}' as a valid array range. Valid formats are `n`, `n-m`, or `n-m:s`.")


def handle_possible_implicit_file(implicit_file):
    if os.path.exists(implicit_file) and os.path.isfile(implicit_file):
        try:
            with open(implicit_file) as f:
                file_content = f.read()
        except Exception:
            # Gracefully handle not being able to read the file (e.g. binary files)
            return

        # Avoid uploading large data files >32 kB
        if not implicit_file.endswith(".py") and not implicit_file.endswith(".sh"):
            try:
                kb_size = os.stat(implicit_file).st_size / 1_000
                if kb_size > 32:
                    console.print(
                        f"[orange1]WARNING:[/orange1] {implicit_file} is too large ({kb_size:.2f} kB) "
                        "to automatically upload to cloud VMs (32 kB limit)",
                    )
                    return
            except Exception:
                return

        remote_rel_dir, remote_base = fix_path_for_upload(local_path=implicit_file)

        return {
            "local_path": implicit_file,
            "path": f"{remote_rel_dir}{remote_base}",
            "remote_path": f"/scratch/{remote_rel_dir}{remote_base}",
            "content": file_content,
        }
    elif any(implicit_file.endswith(t) for t in UPLOAD_FILE_TYPES):
        console.print(
            f"[orange1]WARNING:[/orange1] {implicit_file} appears to be a filename, "
            "but this file not found locally and will not be copied to VMs",
        )


def search_content_for_implicit_files(f: dict):
    content = f["content"]
    implicit_files = []
    for line in content.split("\n"):
        if "python" in line or any(f_type in line for f_type in UPLOAD_FILE_TYPES):
            line_parts = shlex.split(line.strip())
            for part in line_parts:
                implicit_file = handle_possible_implicit_file(part)
                if implicit_file:
                    # TODO handle path translation?
                    implicit_files.append(implicit_file)
    return implicit_files


def get_kwargs_from_header(f: dict, click_params: list):
    click_lookup = {}
    for param in click_params:
        for opt in param.opts:
            lookup_key = opt.lstrip("-")
            click_lookup[lookup_key] = param
            if "-" in lookup_key:
                # support both (e.g.) `n-tasks` and `n_tasks`
                click_lookup[lookup_key.replace("-", "_")] = param

    kwargs = {}
    content = f["content"]
    for line in content.split("\n"):
        match = re.fullmatch(HEADER_REGEX, line)
        if match:
            kwarg = match.group(2).lower()
            val = match.group(4)
            val = val.strip().strip('"') if val else val

            if kwarg not in click_lookup:
                raise ValueError(f"Error parsing header in {f['path']}:\n{line}\n  {kwarg} is not valid argument")

            param = click_lookup[kwarg]
            val = True if param.is_flag else param.type.convert(val, param=param, ctx=None)
            key = param.name

            if param.multiple:
                if key not in kwargs:
                    kwargs[key] = []
                kwargs[key].append(val)
            else:
                kwargs[key] = val
        elif line.startswith(("# COILED", "#COILED")):
            console.print(f"Ignoring invalid option: {line}\nSupported formats: #COILED KEY=val` or `#COILED KEY val`.")
    return kwargs


@click.command(context_settings={**CONTEXT_SETTINGS, "ignore_unknown_options": True})
@click.pass_context
# general cluster options
@click.option("--name", default=None, type=str, help="Name to use for Coiled cluster.")
@click.option("--workspace", default=None, type=str, help="Coiled workspace (uses default workspace if not specified).")
@click.option(
    "--software",
    default=None,
    type=str,
    help=(
        "Existing Coiled software environment "
        "(Coiled will sync local Python software environment if neither software nor container is specified)."
    ),
)
@click.option(
    "--container",
    default=None,
    help=(
        "Docker container in which to run the batch job tasks; "
        "this does not need to have Dask (or even Python), "
        "only what your task needs in order to run."
    ),
)
@click.option(
    "--ignore-container-entrypoint",
    default=None,
    help=(
        "Ignore entrypoint for specified Docker container "
        "(like ``docker run --entrypoint``); "
        "default is to use the entrypoint (if any) set on the image."
    ),
)
@click.option(
    "--env",
    "-e",
    default=[],
    multiple=True,
    help=(
        "Environment variables transmitted to run command environment. "
        "Format is ``KEY=val``, multiple vars can be set with separate ``--env`` for each."
    ),
)
@click.option(
    "--secret-env",
    default=[],
    multiple=True,
    help=(
        "Environment variables transmitted to run command environment. "
        "Format is ``KEY=val``, multiple vars can be set with separate ``--secret-env`` for each. "
        "Unlike environment variables specified with ``--env``, these are only stored in our database temporarily."
    ),
)
@click.option(
    "--env-file",
    default=None,
    help="Path to .env file; all variables set in the file will be transmitted to run command environment.",
)
@click.option(
    "--secret-env-file",
    default=None,
    help=(
        "Path to .env file; all variables set in the file will be transmitted to run command environment. "
        "These environment variables will only be stored in our database temporarily."
    ),
)
@click.option(
    "--tag",
    "-t",
    default=[],
    multiple=True,
    help="Tags. Format is ``KEY=val``, multiple vars can be set with separate ``--tag`` for each.",
)
@click.option(
    "--vm-type",
    default=[],
    multiple=True,
    help="VM type to use. Specify multiple times to provide multiple options.",
)
@click.option(
    "--scheduler-vm-type",
    default=[],
    multiple=True,
    help=(
        "VM type to use specifically for scheduler. "
        "Default is to use small VM if scheduler is not running tasks, "
        "or use same VM type(s) for all nodes if scheduler node is running tasks."
    ),
)
@click.option("--arm", default=None, is_flag=True, help="Use ARM VM type.")
@click.option("--cpu", default=None, type=str, help="Number of cores per VM.")
@click.option("--memory", default=None, type=str, help="Memory per VM.")
@click.option(
    "--gpu",
    default=False,
    is_flag=True,
    help="Have a GPU available.",
)
@click.option(
    "--region",
    default=None,
    help="The cloud provider region in which to run the job.",
)
@click.option(
    "--spot-policy",
    default=None,
    type=click.Choice(["on-demand", "spot", "spot_with_fallback"]),
    help=(
        "Default is on-demand; allows using spot VMs, or spot VMs as available "
        "with on-demand as a fallback. Only applies to workers (scheduler VM is "
        "always on-demand)."
    ),
)
@click.option(
    "--allow-cross-zone/--no-cross-zone",
    default=True,
    is_flag=True,
    help="Allow workers to be placed in different availability zones.",
)
@click.option(
    "--disk-size",
    default=None,
    help="Use larger-than-default disk on VM, specified in GiB.",
)
@click.option(
    "--allow-ssh-from",
    default=None,
    type=str,
    help=(
        "IP address or CIDR from which connections to port 22 (SSH) are open; "
        "can also be specified as 'everyone' (0.0.0.0/0) or 'me' (automatically determines public IP detected "
        "for your local client)."
    ),
)
# batch specific options
@click.option(
    "--map-over-values",
    default=None,
    type=str,
    help=(
        "A list of values such that for each value, a task will be run with that value as the input. "
        "If you specify ``--map-over-values 'first,second,third'``, then batch will run three tasks with inputs "
        "'first', 'second', and 'third'. By default the input is passed to the task in the ``COILED_BATCH_TASK_INPUT`` "
        "environment variable, so one task will get ``COILED_BATCH_TASK_INPUT=first`` and so on."
    ),
)
@click.option(
    "--map-over-file",
    default=None,
    type=str,
    help=(
        "Like ``--map-over--values``, but instead of specifying the string of values directly, you specify the path "
        "to a file with the values. Note that by default, each line in the file is treated as an individual value; "
        "this can be controlled with the ``--map-over-delimiter`` option."
    ),
)
@click.option(
    "--map-over-input-var",
    default=None,
    type=str,
    help=(
        "The value from --map-over-values or --map-over-files is exposed to the task as an environment variable. "
        "By default, the environment variable is ``COILED_BATCH_TASK_INPUT``, but you can specify a different "
        "name for the environment variable using this option."
    ),
)
@click.option(
    "--map-over-delimiter",
    default=None,
    type=str,
    help=(
        "Delimiter for splitting the string from ``--map-over-values`` or the file contents from ``--map-over-file`` "
        "into individual values. By default this is ',' for ``--map-over-values`` and newline for ``--map-over-file``."
    ),
)
@click.option(
    "--ntasks",
    "--n-tasks",
    default=None,
    type=int,
    help=(
        "Number of tasks to run. "
        "Tasks will have ID from 0 to n-1, the ``COILED_ARRAY_TASK_ID`` environment variable "
        "for each task is set to the ID of the task."
    ),
)
@click.option(
    "--task-on-scheduler/--no-task-on-scheduler",
    default=None,
    is_flag=True,
    help="Run task with lowest job ID on scheduler node.",
)
@click.option(
    "--array",
    default=None,
    type=str,
    help=(
        "Specify array of tasks to run with specific IDs (instead of using ``--ntasks`` to array from 0 to n-1). "
        "You can specify list of IDs, a range, or a list with IDs and ranges. For example, ``--array 2,4-6,8-10``."
    ),
)
@click.option(
    "--scheduler-task-array",
    default=None,
    type=str,
    help=(
        "Which tasks in array to run on the scheduler node. "
        "In most cases you'll probably want to use ``--task-on-scheduler`` "
        "instead to run task with lowest ID on the scheduler node."
    ),
)
@click.option(
    "--max-workers",
    "-N",
    default=None,
    type=click.IntRange(-1),
    help=(
        "Maximum number of worker nodes. "
        "By default, there will be as many worker nodes as tasks, up to 1000; use -1 to explicitly request no limit."
    ),
)
@click.option(
    "--wait-for-ready-cluster", default=False, is_flag=True, help="Only assign tasks once full cluster is ready."
)
@click.option(
    "--forward-aws-credentials", default=False, is_flag=True, help="Forward STS token from local AWS credentials."
)
@click.option(
    "--package-sync-strict",
    default=False,
    is_flag=True,
    help="Require exact package version matches when using package sync.",
)
@click.option(
    "--package-sync-conda-extras",
    default=None,
    multiple=True,
    help=(
        "A list of conda package names (available on conda-forge) to include in the "
        "environment that are not in your local environment."
    ),
)
@click.option(
    "--package-sync-ignore",
    default=None,
    multiple=True,
    help=(
        "A list of package names to exclude from the environment. Note their dependencies may still be installed,"
        "or they may be installed by another package that depends on them!"
    ),
)
@click.option(
    "--host-setup-script",
    default=None,
    help="Path to local script which will be run on each VM prior to running any tasks.",
)
@click.option(
    "--job-timeout",
    default=None,
    type=str,
    help=(
        "Timeout for batch job; timer starts when the job starts running (after VMs have been provisioned). "
        "For example, you can specify '30 minutes' or '1 hour'. Default is no timeout."
    ),
)
@click.argument("command", nargs=-1, required=True)
def batch_run_cli(ctx, **kwargs):
    """
    Submit a batch job to run on Coiled.

    Batch Jobs is currently an experimental feature.
    """
    default_kwargs = {
        key: val for key, val in kwargs.items() if ctx.get_parameter_source(key) == click.core.ParameterSource.DEFAULT
    }

    success = True
    exception = None
    try:
        _batch_run(default_kwargs, from_cli=True, **kwargs)
    except Exception as e:
        success = False
        exception = e
        raise
    finally:
        coiled.add_interaction(
            "coiled-batch-cli",
            success=success,
            **error_info_for_tracking(exception),
        )


def _batch_run(default_kwargs, logger=None, from_cli=False, **kwargs) -> dict:
    command = kwargs["command"]

    # Handle command as string case (e.g. `coiled batch run "python myscript.py"`)
    if len(command) == 1:
        command = shlex.split(command[0])
        # unescape $ so that if someone has `echo "FOO is \$FOO"` this will be run as `echo "FOO is $FOO"`
        command = [
            part.replace(
                r"\$",
                "$",
            )
            for part in command
        ]

    # if user tries `coiled batch run foo.py --bar` they probably want to
    # run `python foo.py --bar` rather than `foo.py --bar`
    if command[0].endswith(".py"):
        command = ["python", *command]

    # unescape escaped COILED env vars in command
    command = [part.replace("\\$COILED", "$COILED") for part in command]

    user_files = []
    kwargs_from_header = None

    # identify implicit files referenced in commands like "python foo.py" or "foo.sh"
    for idx, implicit_file in enumerate(command):
        f = handle_possible_implicit_file(implicit_file)
        if f:
            user_files.append(f)
            command[idx] = f["path"]
            # just get kwargs (if any) from the first file that has some in the header
            kwargs_from_header = kwargs_from_header or get_kwargs_from_header(f, batch_run_cli.params)

    # merge options from file header with options specified on command line
    # command line takes precedence
    if kwargs_from_header:
        for key, val in kwargs_from_header.items():
            # only use the option from header if command line opt was "default" (i.e., not specified by user)
            if key in default_kwargs:
                kwargs[key] = val
            elif isinstance(val, list) and isinstance(kwargs[key], (list, tuple)):
                kwargs[key] = [*kwargs[key], *val]

    task_env_for_job_spec = {}

    if kwargs.get("map_over_task_var_dicts"):
        # for the Python API, you can explicitly specify multiple environment variables and values per task
        # e.g., map_over_task_var_dicts=[{"FOO": "1", "BAR": "2"}, {"FOO": "3", "BAR": "4"}]
        # will run two tasks, the first will have FOO=1 BAR=2, the second will have FOO=3 BAR=4

        if (
            kwargs.get("map_over_values")
            or kwargs.get("map_over_file")
            or kwargs["ntasks"] is not None
            or kwargs["array"] is not None
        ):
            raise ValueError(
                "`map_over_task_var_dicts` keyword argument cannot be combined with "
                "map_over_values, map_over_file, n_tasks, or array keyword arguments"
            )

        task_env_for_job_spec = {"task_map_env_vars_and_vals": kwargs["map_over_task_var_dicts"]}
        kwargs["ntasks"] = len(kwargs["map_over_task_var_dicts"])

    elif kwargs.get("map_over_values") or kwargs.get("map_over_file") or kwargs.get("map_over_split_values"):
        if kwargs["ntasks"] is not None:
            raise ValueError("You cannot specify ntasks while using map-over (tasks are determined by map inputs)")
        if kwargs["array"] is not None:
            raise ValueError("You cannot specify array while using map-over (tasks are determined by map inputs)")
        if (kwargs.get("map_over_values") or kwargs.get("map_over_split_values")) and kwargs.get("map_over_file"):
            raise ValueError("You cannot specify both map-over-values and map-over-file")

        if kwargs.get("map_over_split_values"):
            # for the Python API, we get a list rather than a string that needs to be split
            input_values = kwargs["map_over_split_values"]
        else:
            default_delim = ","
            raw_map_input = kwargs.get("map_over_values")
            if kwargs.get("map_over_file"):
                default_delim = "\n"
                with open(kwargs["map_over_file"]) as f:
                    raw_map_input = f.read()

            if not raw_map_input:
                raise ValueError("No values to map over")

            delim = kwargs.get("map_over_delimiter") or default_delim
            # strip so that (eg) \n at end of a file won't result in a final empty input value
            input_values = raw_map_input.rstrip(delim).split(delim)

        input_var_name = kwargs.get("map_over_input_var") or "COILED_BATCH_TASK_INPUT"

        task_env_for_job_spec = {
            "task_map_env_var": input_var_name,
            "task_map_env_vals": input_values,
        }
        kwargs["ntasks"] = len(input_values)

    # extra parsing/validation of options
    if kwargs["ntasks"] is not None and kwargs["array"] is not None:
        raise ValueError("You cannot specify both `--ntasks` and `--array`")

    if not kwargs["array"] and not kwargs["ntasks"]:
        kwargs["ntasks"] = 1

    # determine how many tasks to run on how many VMs
    job_array_kwargs = {}
    n_tasks = 0
    min_task_id = 0
    if kwargs["ntasks"]:
        n_tasks = kwargs["ntasks"]
        job_array_kwargs = {"task_array_ntasks": n_tasks}

    elif kwargs["array"]:
        # allow, e.g., `--array 0-12:3%2` to run tasks 0, 3, 9, and 12 (`0-12:3`) on 2 VMs (`%2`)
        if "%" in kwargs["array"]:
            array_string, max_workers_string = kwargs["array"].split("%", maxsplit=1)
            if max_workers_string:
                try:
                    kwargs["max_workers"] = int(max_workers_string)
                except ValueError:
                    pass
        else:
            array_string = kwargs["array"]

        job_array_ids = parse_array_string(array_string)
        n_tasks = len(job_array_ids)
        min_task_id = min(*job_array_ids)
        job_array_kwargs = {"task_array": job_array_ids}

    # default to limit of 1000 VMs, use -1 to explicitly ask for no limit
    max_workers = None if kwargs["max_workers"] == -1 else kwargs["max_workers"] or 1000

    n_tasks_on_workers = n_tasks - 1 if kwargs["task_on_scheduler"] else n_tasks
    n_task_workers = n_tasks_on_workers if max_workers is None else min(n_tasks_on_workers, max_workers)

    scheduler_task_ids = parse_array_string(kwargs["scheduler_task_array"]) if kwargs["scheduler_task_array"] else []
    if kwargs["task_on_scheduler"]:
        scheduler_task_ids.append(min_task_id)

    # if there's just one task, only make a single VM and run it there
    if n_tasks == 1 and kwargs["task_on_scheduler"] is not False:
        scheduler_task_ids = [min_task_id]
        n_task_workers = 0

    tags = dict_from_key_val_list(kwargs["tag"])

    job_env_vars = dict_from_key_val_list(kwargs["env"])
    job_secret_vars = dict_from_key_val_list(kwargs["secret_env"])

    if kwargs.get("env_file"):
        try:
            import dotenv

            env_file_values = dotenv.dotenv_values(kwargs["env_file"])
            job_env_vars = {**env_file_values, **job_env_vars}
        except ImportError:
            ValueError("--env-file option requires `python-dotenv` to be installed locally")

    if kwargs.get("secret_env_file"):
        try:
            import dotenv

            secret_env_file_values = dotenv.dotenv_values(kwargs["secret_env_file"])
            job_secret_vars = {**secret_env_file_values, **job_secret_vars}
        except ImportError:
            ValueError("--secret-env-file option requires `python-dotenv` to be installed locally")

    extra_message = ""

    if kwargs["forward_aws_credentials"]:
        # try to get creds that last 12 hours, but there's a good chance we'll get shorter-lived creds
        aws_creds = get_aws_local_session_token(60 * 60 * 12, log=False)
        if aws_creds["AccessKeyId"]:
            job_secret_vars["AWS_ACCESS_KEY_ID"] = aws_creds["AccessKeyId"]
            if aws_creds["Expiration"]:
                expires_in_s = (
                    aws_creds["Expiration"] - datetime.datetime.now(tz=datetime.timezone.utc)
                ).total_seconds()
                # TODO add doc explaining how to do this and refer to that doc

                extra_message = (
                    f"Note: Forwarding AWS credentials which will expire in [bright_blue]{format_time(expires_in_s)}[/]"
                    f"\n"
                    "Use AWS Instance Profiles if you need longer lasting credentials."
                )

            else:
                extra_message = (
                    "Note: Forwarding AWS credentials, expiration is not known.\n"
                    "Use AWS Instance Profiles if you need longer lasting credentials."
                )

        if aws_creds["SecretAccessKey"]:
            job_secret_vars["AWS_SECRET_ACCESS_KEY"] = aws_creds["SecretAccessKey"]
        if aws_creds["SessionToken"]:
            job_secret_vars["AWS_SESSION_TOKEN"] = aws_creds["SessionToken"]
    else:
        # don't set the ENV on container that makes AWS SDK look out our local endpoint for forwarded creds
        dask.config.set({"coiled.use_aws_creds_endpoint": False})

    # identify implicit files referenced by other files
    # for example, user runs "coiled batch run foo.sh" and `foo.sh` itself runs `python foo.py`
    user_files_from_content = []
    for f in user_files:
        if "python " in f["content"] or any(f_type in f["content"] for f_type in UPLOAD_FILE_TYPES):
            more_files = search_content_for_implicit_files(f)
            if more_files:
                user_files_from_content.extend(more_files)
    if user_files_from_content:
        user_files.extend(user_files_from_content)

    host_setup_content = None
    if kwargs["host_setup_script"]:
        with open(kwargs["host_setup_script"]) as f:
            host_setup_content = f.read()

    # don't show warnings about blocked dask event loop
    dask.config.set({"distributed.admin.tick.limit": "1 week"})

    # since we want to accept cpu and memory expressed just with strings,
    # we'll parse `N-M` and pass that to `Cluster` in the desired format
    cpu_desired = None
    mem_desired = None
    if kwargs["cpu"]:
        try:
            kwargs["cpu"] = str(kwargs["cpu"])
            if "-" in kwargs["cpu"]:
                cpu_min, cpu_max = kwargs["cpu"].split("-")
                cpu_desired = [int(cpu_min.strip()), int(cpu_max.strip())]
            else:
                cpu_desired = int(kwargs["cpu"])
        except Exception as e:
            raise ValueError(
                f"Unable to parse CPU value of {kwargs['cpu']!r}.\n"
                f"Valid formats are number or range, for example, '4' and '4-8'."
            ) from e

    if kwargs["memory"]:
        try:
            if "-" in kwargs["memory"]:
                mem_min, mem_max = kwargs["memory"].split("-")
                mem_desired = [mem_min.strip(), mem_max.strip()]
            else:
                mem_desired = kwargs["memory"]
        except Exception as e:
            raise ValueError(
                f"Unable for parse memory value of {kwargs['memory']!r}.\n"
                f"You can specify single value like '16GB', or a range like '16GB-32GB'."
            ) from e

    batch_job_container = f"{kwargs['container']}!" if kwargs["ignore_container_entrypoint"] else kwargs["container"]

    cluster_kwargs = {
        "name": kwargs["name"],
        "workspace": kwargs["workspace"],
        "n_workers": n_task_workers,
        "software": kwargs["software"],
        "show_widget": True,
        # batch job can either run in normal Coiled software env (which defaults to package sync)
        # or can run in an extra container (which doesn't need to include dask)
        "batch_job_container": batch_job_container,
        # if batch job is running in extra container, then we just need a pretty minimal dask container
        # so for now switch the default in that case to basic dask container
        # TODO would it be better to use a pre-built senv with our `cloud-env-run` container instead?
        "container": "daskdev/dask:latest" if kwargs["container"] and not kwargs["software"] else None,
        "region": kwargs["region"],
        "scheduler_options": {
            "idle_timeout": "520 weeks",  # TODO allow job timeout?
            "worker_ttl": "520 weeks",  # don't have scheduler restart unresponsive dask workers
        },
        "worker_vm_types": list(kwargs["vm_type"]) if kwargs["vm_type"] else None,
        "arm": kwargs["arm"],
        "worker_cpu": cpu_desired,
        "worker_memory": mem_desired,
        "spot_policy": kwargs["spot_policy"],
        "worker_disk_size": kwargs["disk_size"],
        "worker_gpu": kwargs["gpu"],
        "tags": {**tags, **{"coiled-cluster-type": "batch"}},
        "allow_ssh_from": kwargs["allow_ssh_from"],
        # "mount_bucket": mount_bucket,
        "package_sync_strict": kwargs.get("package_sync_strict"),
        "package_sync_conda_extras": kwargs.get("package_sync_conda_extras"),
        "package_sync_ignore": kwargs.get("package_sync_ignore"),
        "allow_cross_zone": True if kwargs["allow_cross_zone"] is None else kwargs["allow_cross_zone"],
    }

    # when task will run on scheduler, give it the same VM specs as worker node
    if scheduler_task_ids:
        cluster_kwargs = {
            **cluster_kwargs,
            "scheduler_vm_types": list(kwargs["vm_type"]) if kwargs["vm_type"] else None,
            "scheduler_cpu": cpu_desired,
            "scheduler_memory": mem_desired,
            "scheduler_disk_size": kwargs["disk_size"],
            "scheduler_gpu": kwargs["gpu"],
        }

    if kwargs["scheduler_vm_type"]:
        # user explicitly requested scheduler vm type, so override whatever would be default
        cluster_kwargs["scheduler_vm_types"] = kwargs["scheduler_vm_type"]

    # Create a job
    job_spec = {
        "user_command": coiled.utils.join_command_parts(command),
        "user_files": user_files,
        **job_array_kwargs,
        "scheduler_task_array": scheduler_task_ids,
        "env_vars": job_env_vars,
        "secret_env_vars": job_secret_vars,
        **task_env_for_job_spec,
        "wait_for_ready_cluster": kwargs["wait_for_ready_cluster"],
        # For non-prefect batch jobs, set workdir to the same place
        # where user's local files are copied onto the cloud VM.
        # Avoid possibly breaking prefect batch jobs
        # https://github.com/coiled/platform/pull/8655#pullrequestreview-2826448869
        "workdir": None if "flow-run-id" in tags else "/scratch/batch",
        "host_setup": host_setup_content,
        "job_timeout_seconds": parse_timedelta(kwargs["job_timeout"]) if kwargs["job_timeout"] else None,
    }

    with coiled.Cloud(workspace=kwargs["workspace"]) as cloud:
        job_spec["workspace"] = cloud.default_workspace

        compressed_data = gzip.compress(json.dumps(job_spec).encode())
        if len(compressed_data) > 2_400_000:
            raise ValueError(
                f"Cannot submit job because data is too large "
                f"({format_bytes(len(compressed_data))} is over 2.4 MiB limit)"
            )

        url = f"{cloud.server}/api/v2/jobs/compressed"
        response = sync_request(
            cloud=cloud,
            url=url,
            method="post",
            data=compressed_data,
            json_output=True,
        )

        job_id = response["id"]

        # Run the job on a cluster
        with supress_logs([COILED_LOGGER_NAME], level=logging.WARNING):
            cluster = coiled.Cluster(
                cloud=cloud,
                batch_job_ids=[job_id],
                **cluster_kwargs,
            )

        if logger:
            message = f"""
Command:     {coiled.utils.join_command_parts(command)}
Cluster ID:  {cluster.cluster_id}
URL:         {cluster.details_url}
Tasks:       {n_tasks}
"""
            logger.info(message)
            if extra_message:
                logger.warning(extra_message)
        else:
            extra_message = f"\n{extra_message}\n" if extra_message else ""
            if from_cli:
                status_command = "coiled batch status"
                if kwargs["workspace"]:
                    status_command = f"{status_command} --workspace {kwargs['workspace']}"
            else:
                status_command = f"coiled.batch.status({cluster.cluster_id})"
            message = f"""
[bold]Command[/]:     [bright_blue]{coiled.utils.join_command_parts(command)}[/]
[bold]Cluster ID[/]:  [bright_blue]{cluster.cluster_id}[/]
[bold]URL[/]:         [link][bright_blue]{cluster.details_url}[/bright_blue][/link]
[bold]Tasks[/]:       [bright_blue]{n_tasks}[/]

To track progress run:

  [green]{status_command}[/]
{extra_message}"""

            console.print(Panel(message, title="Coiled Batch"))

        return {"cluster_id": cluster.cluster_id, "cluster_name": cluster.name, "job_id": job_id}
