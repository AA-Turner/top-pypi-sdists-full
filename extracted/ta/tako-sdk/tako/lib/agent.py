"""Agent run subresources.

Two agent products hang off ``client.agent``:

* ``client.agent.retrieval.{run,get,stream}`` — Retrieval Agent (``/v1/agent/retrieval/runs``)
* ``client.agent.answer.{run,get,stream}`` — Answer Agent (``/v1/agent/answer/runs``)

``run``/``get`` are thin wrappers over the generated ``AgentApi`` (JSON, via the
generated transport). ``stream`` builds a hand-written httpx SSE client and
returns the per-product ``*Stream`` object.

``stream``'s ``read_timeout`` is the per-connection httpx timeout (seconds)
applied to the initial dispatch and every reconnect. For an active SSE stream
the read/idle meaning is operative: if the server sends no bytes for this long,
httpx raises ``ReadTimeout`` and the stream reconnects (up to ``max_retries``).
It is not a total reconnect budget.

Note: ``client.agent.answer`` (the Answer **Agent**) is distinct from the
top-level ``client.answer()`` (the one-shot ``/v1/answer`` grounding call).

The effort-routed generic agent (``/v1/agent/runs``) was removed in 2.2 in favor
of the two per-product endpoints.
"""

from __future__ import annotations

from typing import Optional

import httpx

from tako.aio.api.agent_api import AgentApi as AsyncAgentApi
from tako.aio.api_client import ApiClient as AsyncApiClient
from tako.aio.configuration import Configuration as AsyncConfiguration
from tako.aio.models.answer_agent_run import AnswerAgentRun as AsyncAnswerAgentRun
from tako.aio.models.answer_agent_run_request import AnswerAgentRunRequest as AsyncAnswerAgentRunRequest
from tako.aio.models.retrieval_agent_run import RetrievalAgentRun as AsyncRetrievalAgentRun
from tako.aio.models.retrieval_agent_run_request import RetrievalAgentRunRequest as AsyncRetrievalAgentRunRequest
from tako.api.agent_api import AgentApi
from tako.api_client import ApiClient
from tako.configuration import Configuration
from tako.lib.streaming import (
    AnswerAgentStream,
    AsyncAnswerAgentStream,
    AsyncRetrievalAgentStream,
    RetrievalAgentStream,
)
from tako.models.answer_agent_run import AnswerAgentRun
from tako.models.answer_agent_run_request import AnswerAgentRunRequest
from tako.models.retrieval_agent_run import RetrievalAgentRun
from tako.models.retrieval_agent_run_request import RetrievalAgentRunRequest

_RUN_ID_REQUIRED = "run_id is required to poll a run; the stream produced no events to resume from"


class RetrievalAgentResource:
    """Synchronous Retrieval Agent run operations: ``client.agent.retrieval.{run,get,stream}``."""

    def __init__(self, config: Configuration) -> None:
        self._config = config
        self._api = AgentApi(ApiClient(config))

    def run(self, request: RetrievalAgentRunRequest) -> RetrievalAgentRun:
        return self._api.create_retrieval_agent_run(request)

    def get(self, run_id: Optional[str], starting_after: Optional[int] = None) -> RetrievalAgentRun:
        if run_id is None:
            raise ValueError(_RUN_ID_REQUIRED)
        return self._api.get_retrieval_agent_run(run_id, starting_after=starting_after)

    def stream(
        self,
        request: RetrievalAgentRunRequest,
        *,
        max_retries: int = 5,
        read_timeout: float = 120.0,
    ) -> RetrievalAgentStream:
        """Open a live SSE stream over a new Retrieval Agent run (see module docstring)."""
        return RetrievalAgentStream(
            httpx.Client(timeout=read_timeout),
            config=self._config,
            request=request,
            max_retries=max_retries,
            read_timeout=read_timeout,
        )


class AnswerAgentResource:
    """Synchronous Answer Agent run operations: ``client.agent.answer.{run,get,stream}``."""

    def __init__(self, config: Configuration) -> None:
        self._config = config
        self._api = AgentApi(ApiClient(config))

    def run(self, request: AnswerAgentRunRequest) -> AnswerAgentRun:
        return self._api.create_answer_agent_run(request)

    def get(self, run_id: Optional[str], starting_after: Optional[int] = None) -> AnswerAgentRun:
        if run_id is None:
            raise ValueError(_RUN_ID_REQUIRED)
        return self._api.get_answer_agent_run(run_id, starting_after=starting_after)

    def stream(
        self,
        request: AnswerAgentRunRequest,
        *,
        max_retries: int = 5,
        read_timeout: float = 120.0,
    ) -> AnswerAgentStream:
        """Open a live SSE stream over a new Answer Agent run (see module docstring)."""
        return AnswerAgentStream(
            httpx.Client(timeout=read_timeout),
            config=self._config,
            request=request,
            max_retries=max_retries,
            read_timeout=read_timeout,
        )


class AgentResource:
    """Namespace for the agent products: ``.retrieval`` and ``.answer``."""

    def __init__(self, config: Configuration) -> None:
        self.retrieval = RetrievalAgentResource(config)
        self.answer = AnswerAgentResource(config)


class AsyncRetrievalAgentResource:
    """Asynchronous Retrieval Agent run operations (parallel ``tako.aio`` package)."""

    def __init__(self, config: AsyncConfiguration) -> None:
        self._config = config
        self._api = AsyncAgentApi(AsyncApiClient(config))

    async def run(self, request: AsyncRetrievalAgentRunRequest) -> AsyncRetrievalAgentRun:
        return await self._api.create_retrieval_agent_run(request)

    async def get(self, run_id: Optional[str], starting_after: Optional[int] = None) -> AsyncRetrievalAgentRun:
        if run_id is None:
            raise ValueError(_RUN_ID_REQUIRED)
        return await self._api.get_retrieval_agent_run(run_id, starting_after=starting_after)

    async def stream(
        self,
        request: AsyncRetrievalAgentRunRequest,
        *,
        max_retries: int = 5,
        read_timeout: float = 120.0,
    ) -> AsyncRetrievalAgentStream:
        """Open a live SSE stream over a new Retrieval Agent run (see module docstring)."""
        stream = AsyncRetrievalAgentStream(
            httpx.AsyncClient(timeout=read_timeout),
            config=self._config,
            request=request,
            max_retries=max_retries,
            read_timeout=read_timeout,
        )
        await stream.open()
        return stream


class AsyncAnswerAgentResource:
    """Asynchronous Answer Agent run operations (parallel ``tako.aio`` package)."""

    def __init__(self, config: AsyncConfiguration) -> None:
        self._config = config
        self._api = AsyncAgentApi(AsyncApiClient(config))

    async def run(self, request: AsyncAnswerAgentRunRequest) -> AsyncAnswerAgentRun:
        return await self._api.create_answer_agent_run(request)

    async def get(self, run_id: Optional[str], starting_after: Optional[int] = None) -> AsyncAnswerAgentRun:
        if run_id is None:
            raise ValueError(_RUN_ID_REQUIRED)
        return await self._api.get_answer_agent_run(run_id, starting_after=starting_after)

    async def stream(
        self,
        request: AsyncAnswerAgentRunRequest,
        *,
        max_retries: int = 5,
        read_timeout: float = 120.0,
    ) -> AsyncAnswerAgentStream:
        """Open a live SSE stream over a new Answer Agent run (see module docstring)."""
        stream = AsyncAnswerAgentStream(
            httpx.AsyncClient(timeout=read_timeout),
            config=self._config,
            request=request,
            max_retries=max_retries,
            read_timeout=read_timeout,
        )
        await stream.open()
        return stream


class AsyncAgentResource:
    """Namespace for the agent products (parallel ``tako.aio`` package): ``.retrieval`` and ``.answer``."""

    def __init__(self, config: AsyncConfiguration) -> None:
        self.retrieval = AsyncRetrievalAgentResource(config)
        self.answer = AsyncAnswerAgentResource(config)
