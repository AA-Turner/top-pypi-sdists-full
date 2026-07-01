from __future__ import annotations

import typing as t
from contextlib import asynccontextmanager
from uuid import UUID, uuid4

from pydantic import ConfigDict, Field, PrivateAttr, SkipValidation, model_validator

from dreadnode.core.execution import Executor
from dreadnode.core.meta import Config
from dreadnode.optimization.backends.base import (
    CandidateT,
    OptimizationAdapter,
    OptimizationBackend,
    OptimizationBackendError,
    OptimizationEvaluator,
)
from dreadnode.optimization.backends.gepa import GEPABackend
from dreadnode.optimization.config import OptimizationConfig
from dreadnode.optimization.events import (
    OptimizationEnd,
    OptimizationEvent,
)
from dreadnode.optimization.result import OptimizationResult


class Optimization(
    Executor[OptimizationEvent[CandidateT], OptimizationResult[CandidateT]],
    t.Generic[CandidateT],
):
    """Dreadnode-native optimize_anything executor."""

    model_config = ConfigDict(arbitrary_types_allowed=True, use_attribute_docstrings=True)

    name: str = ""
    seed_candidate: CandidateT | None = None
    evaluator: SkipValidation[OptimizationEvaluator[CandidateT] | None] = None
    adapter: SkipValidation[OptimizationAdapter[CandidateT] | None] = None
    objective: str | None = None
    background: str | None = None
    dataset: list[t.Any] | None = None
    trainset: list[t.Any] | None = None
    valset: list[t.Any] | None = None
    config: OptimizationConfig = Field(default_factory=OptimizationConfig)
    backend: SkipValidation[str | OptimizationBackend[CandidateT]] = "gepa"
    tags: list[str] = Config(default_factory=lambda: ["optimization"])

    _optimization_id: UUID = PrivateAttr(default_factory=uuid4)

    def model_post_init(self, context: t.Any) -> None:
        super().model_post_init(context)
        if not self.name:
            self.name = f"optimization-{self._optimization_id.hex[:8]}"

        if self.seed_candidate is None and self.adapter is not None:
            self.seed_candidate = self.adapter.seed_candidate()

    @model_validator(mode="after")
    def _validate_inputs(self) -> Optimization[CandidateT]:
        if self.dataset is not None and self.trainset is not None:
            raise ValueError("Pass either 'dataset' or 'trainset', not both.")
        if self.seed_candidate is None and self.adapter is None:
            raise ValueError("optimize_anything requires a seed_candidate or an adapter.")
        if self.evaluator is None and self.adapter is None:
            raise ValueError("optimize_anything requires an evaluator or an adapter.")
        return self

    @property
    def optimization_id(self) -> UUID:
        """Stable identifier for this optimization run."""
        return self._optimization_id

    @property
    def effective_dataset(self) -> list[t.Any] | None:
        """Return the trainset if provided, otherwise dataset."""
        return self.trainset if self.trainset is not None else self.dataset

    def _extract_result(
        self,
        event: OptimizationEvent[CandidateT],
    ) -> OptimizationResult[CandidateT] | None:
        if isinstance(event, OptimizationEnd):
            return event.result  # ty: ignore[invalid-return-type] - CandidateT not narrowed through isinstance
        return None

    def _create_span(self) -> t.ContextManager[t.Any]:
        try:
            from dreadnode.tracing.spans import study_span

            return study_span(
                name=self.name,
                label=self.label,
                tags=[*self.tags, "optimize_anything"],
            )
        except (ImportError, RuntimeError):
            from contextlib import nullcontext

            return nullcontext()

    @asynccontextmanager
    async def stream(
        self,
    ) -> t.AsyncIterator[t.AsyncGenerator[OptimizationEvent[CandidateT], None]]:
        with self._create_span() as span:

            async def traced_stream() -> t.AsyncGenerator[OptimizationEvent[CandidateT], None]:
                async for event in self._stream():
                    if span is not None:
                        event.emit(span)
                    yield event

            yield traced_stream()

    async def _stream(self) -> t.AsyncGenerator[OptimizationEvent[CandidateT], None]:
        backend = self._resolve_backend()
        async for event in backend.stream(self):
            yield event

    async def _stream_batch(
        self,
        batch: list[t.Any],  # noqa: ARG002
    ) -> t.AsyncGenerator[OptimizationEvent[CandidateT], None]:
        raise NotImplementedError("Optimization uses _stream(), not _stream_batch().")
        yield

    def _resolve_backend(self) -> OptimizationBackend[CandidateT]:
        if isinstance(self.backend, str):
            if self.backend != "gepa":
                raise OptimizationBackendError(f"Unsupported optimization backend: {self.backend}")
            return GEPABackend()
        return self.backend

    async def console(self) -> OptimizationResult[CandidateT]:
        """Run the optimization with a live console adapter."""
        from dreadnode.optimization.console import OptimizationConsoleAdapter

        adapter = OptimizationConsoleAdapter(self)
        return await adapter.run()


def optimize_anything(
    seed_candidate: CandidateT | None = None,
    evaluator: OptimizationEvaluator[CandidateT] | None = None,
    *,
    name: str | None = None,
    description: str = "",
    objective: str | None = None,
    background: str | None = None,
    dataset: list[t.Any] | None = None,
    trainset: list[t.Any] | None = None,
    valset: list[t.Any] | None = None,
    config: OptimizationConfig | None = None,
    backend: str | OptimizationBackend[CandidateT] = "gepa",
    adapter: OptimizationAdapter[CandidateT] | None = None,
    tags: list[str] | None = None,
    label: str | None = None,
    concurrency: int = 1,
) -> Optimization[CandidateT]:
    """Construct a Dreadnode-native optimize_anything executor."""
    return Optimization(
        name=name or "",
        description=description,
        objective=objective,
        background=background,
        dataset=dataset,
        trainset=trainset,
        valset=valset,
        config=config or OptimizationConfig(),
        backend=backend,
        seed_candidate=seed_candidate,
        evaluator=evaluator,
        adapter=adapter,
        tags=tags or ["optimization"],
        label=label,
        concurrency=concurrency,
    )
