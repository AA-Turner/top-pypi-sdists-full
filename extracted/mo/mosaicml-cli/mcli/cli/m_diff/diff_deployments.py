"""Implementation of mcli diff deployments"""
from __future__ import annotations

import logging
from typing import TypeVar

from termcolor import colored

from mcli.api.exceptions import cli_error_handler
from mcli.cli.common.deployment_filters import get_deployments_with_filters
from mcli.cli.m_diff.diff_runs import get_yaml_diff

logger = logging.getLogger(__name__)

T = TypeVar('T')


def _get_deployments_data(deployment_name):
    deployment = get_deployments_with_filters(name_filter=[deployment_name])
    if len(deployment) == 0:
        print(f'No deployments found with name: {deployment_name}')
        return
    return deployment[0]


@cli_error_handler("mcli diff deployment")
def diff_deployments(
    deployment_name1: str,
    deployment_name2: str,
    **kwargs,
):
    """
    Compare two runs and display the differences
    """
    del kwargs
    deployment1 = _get_deployments_data(deployment_name1)
    deployment2 = _get_deployments_data(deployment_name2)

    if not deployment1 or not deployment2:
        raise RuntimeError('Error fetching deployments')
    print(colored("YAML", attrs=['bold', 'underline']))
    get_yaml_diff(deployment1.submitted_config.__dict__, deployment2.submitted_config.__dict__)
