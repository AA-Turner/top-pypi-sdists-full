"""Keep waiting for a completion across streams the platform closes, as it does when it is redeployed."""

import asyncio
import time
from collections.abc import Awaitable, Callable
from typing import ClassVar

from labqoat.json_document import JsonDocument
from labqoat.reconnect_budget import ReconnectBudget
from labqoat.worker.worker_api_error import WorkerApiError


class CompletionWait:
    """Open the completion stream again after a lost connection; an answer from the service ends the wait.

    A completion endpoint only reports what already happened, so reconnecting cannot repeat any work. A
    stream that stayed open restores the whole budget; only repeated immediate failures give up.
    """

    RECONNECTS: ClassVar[int] = 8

    @staticmethod
    def run(operation: Callable[[], JsonDocument]) -> JsonDocument:
        """Wait on a blocking completion stream."""
        budget = ReconnectBudget(CompletionWait.RECONNECTS)
        while True:
            budget.opened()
            try:
                return operation()
            except WorkerApiError as error:
                if not error.interrupted() or budget.exhausted():
                    raise
            time.sleep(budget.delay())

    @staticmethod
    async def run_async(operation: Callable[[], Awaitable[JsonDocument]]) -> JsonDocument:
        """Wait on an asynchronous completion stream; cancellation still ends the wait at once."""
        budget = ReconnectBudget(CompletionWait.RECONNECTS)
        while True:
            budget.opened()
            try:
                return await operation()
            except WorkerApiError as error:
                if not error.interrupted() or budget.exhausted():
                    raise
            await asyncio.sleep(budget.delay())
