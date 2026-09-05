"""Agent runs over the generated gRPC stubs: create, poll, list, cancel.

A run is asynchronous: `create` returns at once with the run in `pending`
state, and the caller polls `get` (or lets `wait` / `create_and_wait` poll)
until `status` reaches a terminal state — completed, failed, or cancelled.
Runs typically take a few minutes and at most around 45.

Unlike the wrapper responses the monitor service returns, `create`, `get`,
`cancel` and the waiters return the bare `AgentRun` envelope: the per-RPC
response messages carry nothing else, and the envelope is the one shared run
type across every surface. `list` returns the `ListAgentRunsResponse` page
(`runs` + the `next` cursor).
"""

import asyncio
import json
import time
from typing import Any, Dict, Optional, Union

import grpc
from grpc import aio

from seltz_public_api.proto.v1 import agent_pb2, agent_pb2_grpc

from .._types import OMIT, Omit, is_given
from ..exceptions import SeltzTimeoutError, map_rpc_error
from . import DEFAULT_TIMEOUT_SECONDS

OutputSchemaInput = Union[Dict[str, Any], str]

# The terminal half of the run lifecycle (pending → running → these three).
TERMINAL_STATUSES = frozenset(
    {
        agent_pb2.AGENT_RUN_STATUS_COMPLETED,
        agent_pb2.AGENT_RUN_STATUS_FAILED,
        agent_pb2.AGENT_RUN_STATUS_CANCELLED,
    }
)

# How often the waiters poll. Runs last minutes, so seconds-scale polling
# costs nothing and notices completion promptly.
DEFAULT_POLL_INTERVAL_SECONDS = 10.0


# Request builders, shared by the synchronous and asynchronous services (the
# two cannot share method bodies; see monitor_service.py).


def _output_schema(output_schema: OutputSchemaInput) -> str:
    """The contract carries `output_schema` as a JSON string; accept the
    OpenAI-style `response_format` object as a dict (the natural way to write
    one) or as an already-encoded string."""
    if isinstance(output_schema, str):
        return output_schema
    return json.dumps(output_schema, ensure_ascii=False)


def _create_request(
    api_key: str, query: str, output_schema: Union[OutputSchemaInput, None, Omit]
) -> Any:
    request = agent_pb2.CreateAgentRunRequest(query=query, api_key=api_key)
    if is_given(output_schema) and output_schema is not None:
        request.output_schema = _output_schema(output_schema)
    return request


def _get_request(api_key: str, run_id: str) -> Any:
    return agent_pb2.GetAgentRunRequest(api_key=api_key, run_id=run_id)


def _list_request(
    api_key: str,
    limit: Union[int, None, Omit],
    after: Union[str, None, Omit],
) -> Any:
    request = agent_pb2.ListAgentRunsRequest(api_key=api_key)
    if is_given(limit) and limit is not None:
        request.limit = limit
    if is_given(after) and after is not None:
        request.after = after
    return request


def _cancel_request(api_key: str, run_id: str) -> Any:
    return agent_pb2.CancelAgentRunRequest(api_key=api_key, run_id=run_id)


def _wait_timeout(
    run: agent_pb2.AgentRun, timeout: Optional[float]
) -> SeltzTimeoutError:
    status = agent_pb2.AgentRunStatus.Name(run.status)
    return SeltzTimeoutError(
        f"Run {run.id} is still {status} after {timeout}s; it keeps running "
        f"server-side — keep polling get(), or cancel() it."
    )


class AgentService:
    """Synchronous agent-run operations."""

    def __init__(self, channel: grpc.Channel, api_key: str):
        self._stub = agent_pb2_grpc.AgentServiceStub(channel)
        self._api_key = api_key

    def create(
        self,
        query: str,
        *,
        output_schema: Union[OutputSchemaInput, None, Omit] = OMIT,
    ) -> agent_pb2.AgentRun:
        """Start a run. Returns the AgentRun envelope in `pending` state; poll
        `get` with its id (or use `create_and_wait`).

        `output_schema` is an optional OpenAI-style `response_format` object
        (dict or JSON string) requesting structured output; it adds
        `output.structured` and its `grounding` alongside the cited text
        answer. The request is validated before anything is billed."""
        request = _create_request(self._api_key, query, output_schema)
        try:
            response = self._stub.CreateAgentRun(
                request, timeout=DEFAULT_TIMEOUT_SECONDS
            )
        except grpc.RpcError as error:
            raise map_rpc_error(error) from error
        return response.run

    def get(self, run_id: str) -> agent_pb2.AgentRun:
        """Retrieve a run by id. Poll until `status` reaches a terminal state
        (completed / failed / cancelled); `stop_reason` then says why."""
        request = _get_request(self._api_key, run_id)
        try:
            response = self._stub.GetAgentRun(request, timeout=DEFAULT_TIMEOUT_SECONDS)
        except grpc.RpcError as error:
            raise map_rpc_error(error) from error
        return response.run

    def list(
        self,
        *,
        limit: Union[int, None, Omit] = OMIT,
        after: Union[str, None, Omit] = OMIT,
    ) -> agent_pb2.ListAgentRunsResponse:
        """A page of this org's runs, newest first. `limit` is 1-100 (default
        20); pass one page's `next` as the following call's `after`. The last
        page's `next` is unset."""
        request = _list_request(self._api_key, limit, after)
        try:
            return self._stub.ListAgentRuns(request, timeout=DEFAULT_TIMEOUT_SECONDS)
        except grpc.RpcError as error:
            raise map_rpc_error(error) from error

    def cancel(self, run_id: str) -> agent_pb2.AgentRun:
        """Stop a run that has not finished. A pending run is cancelled at
        once; a running one stops at its next step. Returns the run's current
        envelope — unchanged if it had already ended, so cancelling is safe to
        retry and to race against completion. A cancelled run has no output."""
        request = _cancel_request(self._api_key, run_id)
        try:
            response = self._stub.CancelAgentRun(
                request, timeout=DEFAULT_TIMEOUT_SECONDS
            )
        except grpc.RpcError as error:
            raise map_rpc_error(error) from error
        return response.run

    def wait(
        self,
        run_id: str,
        *,
        poll_interval: float = DEFAULT_POLL_INTERVAL_SECONDS,
        timeout: Optional[float] = None,
    ) -> agent_pb2.AgentRun:
        """Poll `get` until the run reaches a terminal state and return it.

        `timeout` bounds the wait client-side only: on expiry a
        SeltzTimeoutError is raised and the run keeps executing server-side."""
        deadline = None if timeout is None else time.monotonic() + timeout
        while True:
            run = self.get(run_id)
            if run.status in TERMINAL_STATUSES:
                return run
            if deadline is not None and time.monotonic() >= deadline:
                raise _wait_timeout(run, timeout)
            time.sleep(poll_interval)

    def create_and_wait(
        self,
        query: str,
        *,
        output_schema: Union[OutputSchemaInput, None, Omit] = OMIT,
        poll_interval: float = DEFAULT_POLL_INTERVAL_SECONDS,
        timeout: Optional[float] = None,
    ) -> agent_pb2.AgentRun:
        """`create` then `wait` in one call: start a run and return it once it
        reaches a terminal state. See both for the arguments' meaning."""
        run = self.create(query, output_schema=output_schema)
        return self.wait(run.id, poll_interval=poll_interval, timeout=timeout)


class AsyncAgentService(AgentService):
    """Asynchronous agent-run operations.

    Every method awaits the RPC inside its own try, so a failure raises the
    same Seltz exception the synchronous twin raises.
    """

    def __init__(self, channel: aio.Channel, api_key: str):
        self._stub = agent_pb2_grpc.AgentServiceStub(channel)
        self._api_key = api_key

    async def create(  # type: ignore[override]
        self,
        query: str,
        *,
        output_schema: Union[OutputSchemaInput, None, Omit] = OMIT,
    ) -> agent_pb2.AgentRun:
        """Start a run. Returns the AgentRun envelope in `pending` state; poll
        `get` with its id (or use `create_and_wait`).

        `output_schema` is an optional OpenAI-style `response_format` object
        (dict or JSON string) requesting structured output; it adds
        `output.structured` and its `grounding` alongside the cited text
        answer. The request is validated before anything is billed."""
        request = _create_request(self._api_key, query, output_schema)
        try:
            response = await self._stub.CreateAgentRun(
                request, timeout=DEFAULT_TIMEOUT_SECONDS
            )
        except grpc.RpcError as error:
            raise map_rpc_error(error) from error
        return response.run

    async def get(self, run_id: str) -> agent_pb2.AgentRun:  # type: ignore[override]
        """Retrieve a run by id. Poll until `status` reaches a terminal state
        (completed / failed / cancelled); `stop_reason` then says why."""
        request = _get_request(self._api_key, run_id)
        try:
            response = await self._stub.GetAgentRun(
                request, timeout=DEFAULT_TIMEOUT_SECONDS
            )
        except grpc.RpcError as error:
            raise map_rpc_error(error) from error
        return response.run

    async def list(  # type: ignore[override]
        self,
        *,
        limit: Union[int, None, Omit] = OMIT,
        after: Union[str, None, Omit] = OMIT,
    ) -> agent_pb2.ListAgentRunsResponse:
        """A page of this org's runs, newest first. `limit` is 1-100 (default
        20); pass one page's `next` as the following call's `after`. The last
        page's `next` is unset."""
        request = _list_request(self._api_key, limit, after)
        try:
            return await self._stub.ListAgentRuns(
                request, timeout=DEFAULT_TIMEOUT_SECONDS
            )
        except grpc.RpcError as error:
            raise map_rpc_error(error) from error

    async def cancel(self, run_id: str) -> agent_pb2.AgentRun:  # type: ignore[override]
        """Stop a run that has not finished. A pending run is cancelled at
        once; a running one stops at its next step. Returns the run's current
        envelope — unchanged if it had already ended, so cancelling is safe to
        retry and to race against completion. A cancelled run has no output."""
        request = _cancel_request(self._api_key, run_id)
        try:
            response = await self._stub.CancelAgentRun(
                request, timeout=DEFAULT_TIMEOUT_SECONDS
            )
        except grpc.RpcError as error:
            raise map_rpc_error(error) from error
        return response.run

    async def wait(  # type: ignore[override]
        self,
        run_id: str,
        *,
        poll_interval: float = DEFAULT_POLL_INTERVAL_SECONDS,
        timeout: Optional[float] = None,
    ) -> agent_pb2.AgentRun:
        """Poll `get` until the run reaches a terminal state and return it.

        `timeout` bounds the wait client-side only: on expiry a
        SeltzTimeoutError is raised and the run keeps executing server-side."""
        deadline = None if timeout is None else time.monotonic() + timeout
        while True:
            run = await self.get(run_id)
            if run.status in TERMINAL_STATUSES:
                return run
            if deadline is not None and time.monotonic() >= deadline:
                raise _wait_timeout(run, timeout)
            await asyncio.sleep(poll_interval)

    async def create_and_wait(  # type: ignore[override]
        self,
        query: str,
        *,
        output_schema: Union[OutputSchemaInput, None, Omit] = OMIT,
        poll_interval: float = DEFAULT_POLL_INTERVAL_SECONDS,
        timeout: Optional[float] = None,
    ) -> agent_pb2.AgentRun:
        """`create` then `wait` in one call: start a run and return it once it
        reaches a terminal state. See both for the arguments' meaning."""
        run = await self.create(query, output_schema=output_schema)
        return await self.wait(run.id, poll_interval=poll_interval, timeout=timeout)
