"""Utilities for run epilogs"""
from __future__ import annotations

from logging import Logger

from mcli.utils.utils_logging import FAIL, INFO, OK


class CommonLog():
    """Log some common epilog log outputs
    """

    def __init__(self, logger: Logger):
        self.logger = logger

    def log_timeout(self):
        self.logger.warning(('Run is taking awhile to start, returning you to the command line.\n'
                             'Common causes are the run is queued because the resources are not available '
                             'yet, or the docker image is taking awhile to download.\n\n'
                             'To continue to view job status, use `mcli get runs` and `mcli logs`.'))

    def log_run_terminated(self, run):
        msg = f'{FAIL} Run {run.name} is {run.status.value.lower()}'

        reason = run.reason
        if not reason:
            # MORC does not update the execution reason until the run is fully terminated,
            # however, the node reason is updated as soon as the main process fails or
            # is stopped on the node. So instead of waiting around for the run to fully
            # terminate, we check the node reasons
            for node in run.nodes:
                if node.reason:
                    reason = node.reason
                    break

        if reason:
            msg += f' with reason: {reason}'
        self.logger.warning(msg)

    def log_unknown_did_not_start(self):
        self.logger.warning(f'{INFO} Run did not start for an unknown reason. You can monitor it with '
                            '`mcli get runs` to see if it starts.')

    def log_connect_run_terminating(self, status_display: str):
        self.logger.warning(f'{FAIL} Cannot connect to run, run is already in a {status_display} status.')

    def log_run_interactive_starting(self, run_name: str):
        self.logger.info(f'{OK} Run [cyan]{run_name}[/] has started. Preparing your interactive session...')
