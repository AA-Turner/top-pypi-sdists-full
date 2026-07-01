""" Functions for deleting MCLI objects """
import logging
from typing import List, Optional, Union

from mcli.api.exceptions import cli_error_handler
from mcli.api.inference_deployments.api_delete_inference_deployments import delete_inference_deployments
from mcli.api.model.inference_deployment import InferenceDeployment
from mcli.api.model.run import Run
from mcli.api.runs.api_delete_runs import delete_runs
from mcli.api.secrets.api_delete_secrets import delete_secrets
from mcli.api.secrets.api_get_secrets import get_secrets
from mcli.cli.common.deployment_filters import get_deployments_with_filters
from mcli.cli.common.run_filters import get_runs_with_filters
from mcli.models.common import ObjectList
from mcli.utils.utils_interactive import query_yes_no
from mcli.utils.utils_logging import FAIL, INFO, OK, WARN, get_indented_list
from mcli.utils.utils_run_status import RunStatus
from mcli.utils.utils_spinner import console_status

logger = logging.getLogger(__name__)


def _confirm_secret_deletion(secrets):
    if len(secrets) > 1:
        logger.info(f'{INFO} Ready to delete secrets:\n'
                    f'{get_indented_list(sorted(secrets))}\n')
        details = ' listed above'
    else:
        details = f': {list(secrets)[0]}'
    confirm = query_yes_no(f'Would you like to delete the secret{details}?')

    if not confirm:
        raise RuntimeError('Canceling deletion')


@cli_error_handler('mcli delete secret')
def delete_secret(secret_names: List[str], force: bool = False, delete_all: bool = False, **kwargs) -> int:
    """Delete the requested secret(s) from the user's clusters

    Args:
        secret_names: List of secrets to delete
        force: If True, do not request confirmation. Defaults to False.

    Returns:
        True if deletion was successful
    """
    del kwargs

    if not (secret_names or delete_all):
        logger.error(f'{FAIL} Must specify secret names or --all.')
        return 1

    # Get secrets to delete
    to_delete_secrets = get_secrets(secret_names) if not delete_all else get_secrets()
    if not to_delete_secrets:
        if secret_names:
            logger.warning(f'{INFO} Could not find secrets(s) matching: {", ".join(secret_names)}')
        else:
            logger.warning(f'{INFO} Could not find any secrets')
        return 1

    # Confirm and delete
    if not force:
        _confirm_secret_deletion(to_delete_secrets)
    with console_status('Deleting secrets..'):
        deleted = delete_secrets(secrets=to_delete_secrets, timeout=None)
    logger.info(f'{OK} Deleted secret(s): {", ".join([s.name for s in deleted])}')

    return 0


def confirm_run_update(runs: Union[List[Run], ObjectList[Run]], action: str = 'delete') -> int:
    num_runs_compressed_view = 50

    if len(runs) == 1:
        chosen_run = list(runs)[0].name
        return query_yes_no(f'Would you like to {action} the run: {chosen_run}?')
    elif len(runs) < num_runs_compressed_view:
        pretty_runs = get_indented_list(sorted(r.name for r in runs))
        logger.info(f'{INFO} Ready to {action} runs:\n{pretty_runs}\n')
        return query_yes_no(f'Would you like to {action} the runs listed above?')

    logger.info(f'Ready to {action} {len(runs)} runs')
    return query_yes_no(f'Would you like to {action} all {len(runs)} runs?')


@cli_error_handler('mcli delete run')
def delete_run(
    name_filter: Optional[List[str]] = None,
    cluster_filter: Optional[List[str]] = None,
    before_filter: Optional[str] = None,
    after_filter: Optional[str] = None,
    gpu_type_filter: Optional[List[str]] = None,
    gpu_num_filter: Optional[List[int]] = None,
    status_filter: Optional[List[RunStatus]] = None,
    latest: bool = False,
    delete_all: bool = False,
    force: bool = False,
    **kwargs,
):
    del kwargs

    runs = get_runs_with_filters(
        name_filter,
        cluster_filter,
        before_filter,
        after_filter,
        gpu_type_filter,
        gpu_num_filter,
        status_filter,
        latest,
        delete_all,
    )

    if not runs:
        extra = '' if delete_all else ' matching the specified criteria'
        logger.error(f'{WARN} No runs found{extra}.')
        return 1

    if not force and not confirm_run_update(runs, 'delete'):
        logger.error(f'{FAIL} Canceling delete runs')
        return 1

    with console_status('Deleting runs...'):
        delete_runs(runs)

    logger.info(f'{OK} Deleted runs')
    return 0


def confirm_deployment_update(deployments: List[InferenceDeployment], action: str = 'delete') -> int:
    num_deployments_compressed_view = 50

    if len(deployments) == 1:
        chosen_run = list(deployments)[0].name
        return query_yes_no(f'Would you like to {action} the deployment: {chosen_run}?')
    elif len(deployments) < num_deployments_compressed_view:
        pretty_deployments = get_indented_list(sorted(d.name for d in deployments))
        logger.info(f'{INFO} Ready to {action} deployments:\n{pretty_deployments}\n')
        return query_yes_no(f'Would you like to {action} the deployments listed above?')

    return query_yes_no(f'Would you like to {action} all {len(deployments)} deployments?')


@cli_error_handler('mcli delete deployment')
def delete_deployment(
    name_filter: Optional[List[str]] = None,
    old_name_filter: Optional[str] = None,
    cluster_filter: Optional[List[str]] = None,
    before_filter: Optional[str] = None,
    after_filter: Optional[str] = None,
    gpu_type_filter: Optional[List[str]] = None,
    gpu_num_filter: Optional[List[int]] = None,
    status_filter: Optional[List[str]] = None,
    delete_all: bool = False,
    force: bool = False,
    **kwargs,
):
    del kwargs

    if delete_all:
        logger.info(f'{WARN} You cannot do this')
        return 1

    if not name_filter and old_name_filter:
        name_filter = [old_name_filter]

    deployments = get_deployments_with_filters(
        name_filter,
        cluster_filter,
        before_filter,
        after_filter,
        gpu_type_filter,
        gpu_num_filter,
        status_filter,
        delete_all,
    )

    if not deployments:
        extra = '' if delete_all else ' matching the specified criteria'
        logger.error(f'{WARN} No deployments found{extra}.')
        return 1
    if not force and not confirm_deployment_update(deployments, 'delete'):
        logger.error(f'{FAIL} Canceling delete deployments')
        return 1

    with console_status('Deleting deployments...'):
        delete_inference_deployments(deployments)

    logger.info(f'{OK} Deleted deployments')
    return 0
