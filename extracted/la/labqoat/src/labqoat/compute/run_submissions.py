"""Typed keyed child dispatch from an assignment-owned RunContext."""

from dataclasses import dataclass, field
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import ParamSpec, TypeVar

from labqoat._generated.compute_publication import ComputePublication
from labqoat._generated.new_child_run import NewChildRun
from labqoat._generated.new_compute_run import NewComputeRun
from labqoat.authoring.resources import Resources
from labqoat.compute.child_publication import ChildPublication
from labqoat.compute.child_admissions import ChildAdmissions
from labqoat.compute.child_observations import ChildObservations
from labqoat.compute.child_run_handle import ChildRunHandle
from labqoat.compute.function import Function
from labqoat.compute.function_signature import FunctionSignature
from labqoat.compute.run_options import RunOptions
from labqoat.json_document import JsonDocument, JsonValue
from labqoat.schemas.schema_document import SchemaDocument
from labqoat.worker.worker_api import WorkerApi

P = ParamSpec("P")
R = TypeVar("R")


@dataclass(frozen=True)
class RunSubmissions:
    """Accept child work durably without tying its lifetime to a worker connection or Python handle."""

    api: WorkerApi
    publication: ComputePublication
    options: RunOptions = field(default_factory=RunOptions)
    admissions: ChildAdmissions | None = field(default=None, compare=False)
    observations: ChildObservations | None = field(default=None, compare=False)

    def __post_init__(self) -> None:
        """Share one explicit admission queue across immutable per-child options."""
        if self.admissions is None:
            object.__setattr__(self, "admissions", ChildAdmissions(self.api))
        if self.observations is None:
            object.__setattr__(self, "observations", ChildObservations(self.api))

    @asynccontextmanager
    async def session(self) -> AsyncIterator[None]:
        """Own batched submissions and result streams within the invocation's transport lifetime."""
        assert self.admissions is not None and self.observations is not None
        async with self.api.async_session():
            try:
                yield
            finally:
                await self.observations.close()
                await self.admissions.close()

    def with_options(
        self,
        *,
        key: str,
        seed: int = 0,
        resources: Resources | None = None,
        location: str | None = None,
    ) -> "RunSubmissions":
        """Use immutable per-child options and a permanent logical key within the owning Run."""
        return RunSubmissions(
            self.api,
            self.publication,
            RunOptions(key=key, seed=seed, resources=resources, location=location),
            self.admissions,
            self.observations,
        )

    def submit(self, function: Function[P, R], *args: P.args, **kwargs: P.kwargs) -> ChildRunHandle[R]:
        """Capture typed inputs and the callee's declared executable before a single scoped acceptance request."""
        envelope = self._capture(function, function.encode(args, kwargs))
        path, body = self._transport(envelope)
        run = self.api.json("POST", path, body)
        return ChildRunHandle(
            JsonDocument.expect_scalar(run["id"], str),
            self.api,
            FunctionSignature(function.local).annotations["return"],
            self.observations,
        )

    async def submit_async(self, function: Function[P, R], *args: P.args, **kwargs: P.kwargs) -> ChildRunHandle[R]:
        """Accept an owned child without blocking other authored tasks; stable keys permit uncertain-acceptance replay."""
        assert self.admissions is not None
        envelope = self._capture(function, function.encode(args, kwargs))
        path, body = self._transport(envelope)
        run = (
            await self.admissions.submit(body)
            if "child_batches" in self.api.capabilities
            else await self.api.json_async("POST", path, body)
        )
        return ChildRunHandle(
            JsonDocument.expect_scalar(run["id"], str),
            self.api,
            FunctionSignature(function.local).annotations["return"],
            self.observations,
        )

    def _transport(self, envelope: NewChildRun) -> tuple[str, dict[str, JsonValue]]:
        """Negotiate compact transport without changing canonical intent or old-server behavior."""
        if "referenced_children" not in self.api.capabilities:
            return "/api/v1/worker/runs", envelope.to_dict()
        request = envelope.request
        publication = request.publication
        body: dict[str, JsonValue] = {
            "name": request.name,
            "arguments": dict(request.arguments),
            "input_schema_digest": request.input_schema_digest,
            "seed": self.options.seed,
            "publication": {
                "app_name": publication.app_name,
                "source_asset_sha": publication.source_asset_sha,
                "image": publication.image,
                "function": publication.function.to_dict(),
            },
        }
        if request.location is not None:
            body["location"] = request.location
        if request.resources is not None:
            body["resources"] = dict(request.resources)
        return "/api/v1/worker/runs/referenced", {"key": envelope.key, "request": body}

    def _capture(self, function: Function[P, R], arguments: dict[str, JsonValue]) -> NewChildRun:
        """Use identical immutable acceptance documents for synchronous and asynchronous submissions."""
        if self.options.key is None:
            raise ValueError("Child Run submission requires an explicit stable operation key")
        publication = ChildPublication(self.publication).capture(function, arguments)
        request = NewComputeRun(
            name=f"{function.app_name}/{publication.function.name}",
            publication=publication,
            arguments=arguments,
            input_schema_digest=SchemaDocument.capture(function.input_schema()).digest,
            seed=self.options.seed,
            location=self.options.location,
            resources=None if self.options.resources is None else dict(self.options.resources.to_dict()),
        )
        return NewChildRun(key=self.options.key, request=request)
