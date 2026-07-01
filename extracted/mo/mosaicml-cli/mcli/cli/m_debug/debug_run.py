"""Implementation of mcli debug run"""
import logging
from typing import Any, Optional

from mcli.api.exceptions import cli_error_handler
from mcli.api.runs.api_get_run_debug_info import get_run_debug_info

logger = logging.getLogger(__name__)


@cli_error_handler("mcli debug run")
def debug_run(run_name: str, resumption: Optional[int], **kwargs: Any):
    """Fetches debug information for a specific run, including pod and container
    status updates for the run. If no resumption is provided, debug info will be
    shown for the latest resumption."""
    del kwargs

    run_debug_info = get_run_debug_info(run_name)

    if resumption is not None and (resumption < 0 or resumption >= len(run_debug_info.executions_status_updates)):
        logger.error(f'Resumption index {resumption} is out of range. '
                     f'The run has {len(run_debug_info.executions_status_updates)} resumption(s).')
        return 1

    if resumption is None:
        resumption = len(run_debug_info.executions_status_updates) - 1
        logger.info('No resumption provided.'
                    f'Getting debug information for the latest resumption ({resumption}) of run {run_name}')

    run_debug_info.print(resumption)
