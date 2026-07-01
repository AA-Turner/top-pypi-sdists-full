""" MCLI Deployment Filters """
import fnmatch
import logging
from typing import Dict, List, Optional

from mcli.api.exceptions import MCLIException
from mcli.api.inference_deployments.api_get_inference_deployments import get_inference_deployments
from mcli.api.model.inference_deployment import InferenceDeployment
from mcli.cli.common.run_filters import _split_glob_filters
from mcli.utils.utils_spinner import console_status

logger = logging.getLogger(__name__)


def get_deployments_with_filters(
    name_filter: Optional[List[str]] = None,
    cluster_filter: Optional[List[str]] = None,
    before_filter: Optional[str] = None,
    after_filter: Optional[str] = None,
    gpu_type_filter: Optional[List[str]] = None,
    gpu_num_filter: Optional[List[int]] = None,
    status_filter: Optional[List[str]] = None,
    action_all: Optional[bool] = None,
) -> List[InferenceDeployment]:

    filter_used = any([
        name_filter,
        before_filter,
        after_filter,
        cluster_filter,
        gpu_type_filter,
        gpu_num_filter,
        status_filter,
    ])
    if not filter_used:
        if action_all is False:
            raise MCLIException('Must specify at least one filter or --all')

    if not name_filter:
        # Accept all that pass other filters
        name_filter = []

    # Use get_deployments only for the non-glob names provided
    glob_filters, deployment_names = _split_glob_filters(name_filter)

    with console_status('Retrieving requested inference deployments...'):
        deployments = get_inference_deployments(
            deployments=(deployment_names or None) if not glob_filters else None,
            clusters=cluster_filter,
            before=before_filter,
            after=after_filter,
            gpu_types=gpu_type_filter,
            gpu_nums=gpu_num_filter,
            statuses=status_filter,
            timeout=None,
        )

    if glob_filters:
        found_deployments: Dict[str, InferenceDeployment] = {d.name: d for d in deployments}

        # Any globs will be handled by additional client-side filtering
        filtered = set()
        for pattern in glob_filters:
            for match in fnmatch.filter(found_deployments, pattern):
                filtered.add(match)

        expected_names = set(deployment_names)
        for deploy_name in found_deployments:
            if deploy_name in expected_names:
                filtered.add(deploy_name)

        return list(found_deployments[d] for d in filtered)

    return list(deployments)
