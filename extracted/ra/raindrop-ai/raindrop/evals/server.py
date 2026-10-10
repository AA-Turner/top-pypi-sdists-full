"""Framework-independent ASGI eval endpoint; mount behind application authentication."""

from __future__ import annotations

import json
from typing import Any, Awaitable, Callable
from uuid import UUID

from pydantic import BaseModel, Field, StrictInt, ValidationError

from .agents import DefinedEvalAgent, EvalParameterError
from .client import EvalClient
from .datasets import read_eval_dataset
from .models import Destination, EvalSuite
from .runner import EvalSuiteRunSession, read_details

ASGICall = Callable[..., Awaitable[Any]]
MAX_BODY_BYTES = 1024 * 1024


class _Invocation(BaseModel):
    run_id: UUID = Field(alias="runId")
    agent: str = Field(min_length=1, max_length=64)
    parameters: dict[str, Any] = Field(default_factory=dict)
    concurrency: StrictInt = Field(default=4, ge=1, le=100)


class EvalHandler:
    def __init__(
        self,
        client: EvalClient,
        agents: list[DefinedEvalAgent],
        destination: Destination,
    ) -> None:
        self.client, self.destination = client, destination
        self.agents = {agent.slug: agent for agent in agents}
        if len(self.agents) != len(agents):
            raise ValueError("Registered agent slugs must be unique")

    async def handle(
        self, method: str, body: bytes = b""
    ) -> tuple[int, dict[str, Any]]:
        if method == "GET":
            return 200, {
                "agents": [agent.catalog() for agent in self.agents.values()],
                "concurrencySupported": True,
            }
        if method != "POST":
            return 405, {"error": "Method not allowed"}
        if len(body) > MAX_BODY_BYTES:
            return 400, {"error": "Invalid eval request"}
        try:
            invocation = _Invocation.model_validate_json(body)
        except ValidationError:
            return 400, {"error": "Invalid eval request"}
        run_id = str(invocation.run_id)
        parameters = invocation.parameters
        agent = self.agents.get(invocation.agent)
        if agent is None:
            return 404, {"error": "Unknown agent"}
        try:
            agent.start(parameters)
        except EvalParameterError as error:
            return 400, {"error": str(error)}
        try:
            detail = await read_details(
                self.client, run_id, query_url=self.destination.query_url
            )
            replay = detail["replay"]
            if replay["status"] in ("complete", "failed"):
                return 200, {
                    "runId": run_id,
                    "status": replay["status"],
                    "counts": replay["counts"],
                }
            if replay["status"] != "queued":
                return 409, {"error": "Run is already claimed"}
            dataset = await read_eval_dataset(
                self.client,
                replay["dataset_id"],
                version_id=replay["dataset_version_id"],
                query_url=self.destination.query_url,
            )
            # UI endpoint execution captures rows. Grading is scheduled by the caller separately.
            suite = EvalSuite.model_construct(
                name=agent.name,
                dataset=dataset.dataset.slug,
                dataset_version_id=dataset.version.id,
                evaluators=[],
                agent=agent,
                concurrency=invocation.concurrency,
            )
            selected = list(dict.fromkeys(row["row_id"] for row in detail["rows"]))
            session = EvalSuiteRunSession(
                self.client,
                suite,
                dataset,
                selected,
                self.destination,
                parameters=parameters,
                run_id=run_id,
            )
            result = await session.run_selected()
            return 200, {
                "runId": result.run_id,
                "status": result.status,
                "counts": result.counts.wire(),
                "traceEvidence": list(session.evidence.values()),
            }
        except Exception as error:
            return 500, {"error": str(error).replace(self.client.api_key, "[redacted]")}

    async def __call__(
        self, scope: dict[str, Any], receive: ASGICall, send: ASGICall
    ) -> None:
        if scope["type"] != "http":
            return
        body = bytearray()
        while True:
            message = await receive()
            if message["type"] == "http.disconnect":
                return
            body.extend(message.get("body", b""))
            if len(body) > MAX_BODY_BYTES or not message.get("more_body", False):
                break
        status, payload = await self.handle(scope["method"], bytes(body))
        headers = [(b"content-type", b"application/json")]
        if status == 405:
            headers.append((b"allow", b"GET, POST"))
        await send(
            {"type": "http.response.start", "status": status, "headers": headers}
        )
        await send({"type": "http.response.body", "body": json.dumps(payload).encode()})


def create_eval_handler(
    client: EvalClient,
    *,
    agents: list[DefinedEvalAgent],
    query_url: str | None = None,
    replay_ingest_url: str | None = None,
) -> EvalHandler:
    """Create an ASGI handler to mount behind application authentication.

    The host must authenticate and authorize both catalog and execution requests.
    The Query API key authenticates outbound Raindrop calls, not incoming callers.
    """
    return EvalHandler(
        client,
        agents,
        Destination(query_url=query_url, replay_ingest_url=replay_ingest_url),
    )
