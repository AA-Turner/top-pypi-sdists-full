"""Implementation of mcli diff runs"""
from __future__ import annotations

import logging
import subprocess
import textwrap
import uuid
from typing import TypeVar

import yaml
from termcolor import colored

from mcli.api.exceptions import cli_error_handler
from mcli.cli.common.run_filters import get_runs_with_filters

logger = logging.getLogger(__name__)

T = TypeVar('T')


def _get_run_data(run_name):
    run = get_runs_with_filters(name_filter=[run_name], include_details=True)
    if len(run) == 0:
        print(f'No runs found with name: {run_name}')
        return
    return run[0]


def get_yaml_diff(dict1, dict2):
    file1 = _dump_to_file(dict1)
    file2 = _dump_to_file(dict2)
    diff_command = f"diff -W 160 --color=always --ignore-blank-lines  --text -y {file1} {file2}"
    # The sed is needed to color changed lines, this is a workdaround for
    # the diff command not coloring the entire line
    diff_command += f"| sed -e 's/|/\x1b[0m&\x1b[34m/g' && rm {file1} {file2}"
    try:
        subprocess.run(diff_command, shell=True, check=True)
    except Exception as exc:
        raise RuntimeError('Error running diff command') from exc


def _wrap_values(obj, width=75):
    # Needed because otherwise only 60 characters per lined are picked up by diff
    if isinstance(obj, dict):
        return {key: _wrap_values(value, width) for key, value in obj.items()}
    elif isinstance(obj, str):
        return textwrap.fill(obj, width)
    else:
        return obj


def _dump_to_file(data):
    filename = f"{uuid.uuid4()}.yaml"
    with open(filename, 'w', encoding='UTF-8') as file:
        yaml.dump(_wrap_values(data), file, default_flow_style=False)
    return filename


@cli_error_handler("mcli diff run")
def diff_runs(
    run_name1: str,
    run_name2: str,
    **kwargs,
):
    """
    Compare two runs and display the differences
    """
    del kwargs

    run1 = _get_run_data(run_name1)
    run2 = _get_run_data(run_name2)

    if not run1 or not run2:
        raise RuntimeError('Error fetching runs')
    print(colored("YAML", attrs=['bold', 'underline']))
    get_yaml_diff(run1.submitted_config.__dict__, run2.submitted_config.__dict__)
