"""Concurrent input preparation waits for every owned thread before exposing or cleaning its leases."""

import asyncio
from contextlib import ExitStack

from labqoat.compute.pool_worker.accepted_input import AcceptedInput
from labqoat.json_document import JsonDocument


class InputBatch:
    """Prepare a bounded service-delivered batch without serializing independent assignment round trips."""

    @classmethod
    async def open(cls, envelopes: list[JsonDocument], lifetime: ExitStack) -> list[AcceptedInput]:
        """Drain in-flight setup even on cancellation so no background thread can leak a newly opened lease."""
        pending = asyncio.gather(
            *(asyncio.to_thread(cls._open, envelope) for envelope in envelopes), return_exceptions=True
        )
        try:
            results = await asyncio.shield(pending)
        except BaseException:
            results = await pending
            cls._retain(results, lifetime)
            raise
        inputs = cls._retain(results, lifetime)
        for result in results:
            if isinstance(result, BaseException):
                raise result
        return inputs

    @staticmethod
    def _open(envelope: JsonDocument) -> AcceptedInput:
        """Close a partially claimed assignment locally before propagating preparation failure."""
        item = AcceptedInput.open(envelope)
        try:
            item.claim()
        except BaseException:
            item.lifetime.close()
            raise
        return item

    @staticmethod
    def _retain(results: list[AcceptedInput | BaseException], lifetime: ExitStack) -> list[AcceptedInput]:
        """Transfer every successfully opened lease into the enclosing execution's cleanup stack."""
        inputs = [result for result in results if isinstance(result, AcceptedInput)]
        for item in inputs:
            lifetime.callback(item.lifetime.close)
        return inputs
