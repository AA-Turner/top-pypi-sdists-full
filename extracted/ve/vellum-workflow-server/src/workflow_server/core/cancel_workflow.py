import logging
from threading import Event, Event as ThreadingEvent, Thread
import time
from uuid import UUID
from typing import Optional

import requests

_TIMER_INTERVAL = 5

logger = logging.getLogger(__name__)


def get_is_workflow_cancelled(execution_id: UUID, vembda_public_url: Optional[str]) -> bool:
    response = requests.get(
        f"{vembda_public_url}/vembda-public/cancel-workflow-execution-status/{execution_id}",
        headers={"Accept": "application/json"},
        timeout=5,
    )
    response.raise_for_status()

    return response.json().get("cancelled")


class CancelWorkflowWatcherThread(Thread):
    _kill_switch: Event
    _execution_id: UUID
    _cancel_signal: ThreadingEvent
    _vembda_public_url: Optional[str]
    _start = time.time()

    def __init__(
        self,
        kill_switch: Event,
        execution_id: UUID,
        vembda_public_url: Optional[str],
        cancel_signal: ThreadingEvent,
        timeout_seconds: int,
    ) -> None:
        Thread.__init__(self)
        self._kill_switch = kill_switch
        self._execution_id = execution_id
        self._timeout_seconds = timeout_seconds
        self._cancel_signal = cancel_signal
        self._vembda_public_url = vembda_public_url

    def run(self) -> None:
        start_time = time.time()
        if not self._vembda_public_url:
            return

        cancelled = get_is_workflow_cancelled(self._execution_id, self._vembda_public_url)
        if cancelled:
            logger.info(f"Cancelling workflow: {self._execution_id}")
            self._cancel_signal.set()
            return

        while not self._kill_switch.wait(_TIMER_INTERVAL):
            try:
                reached_timeout = time.time() - start_time >= self._timeout_seconds

                cancelled = get_is_workflow_cancelled(self._execution_id, self._vembda_public_url)
                if cancelled or reached_timeout:
                    logger.info(f"Cancelling workflow: {self._execution_id}")
                    self._cancel_signal.set()
                    break
            except Exception:
                logger.exception("Error checking for cancel event")
                break
