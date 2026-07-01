from __future__ import annotations

import contextlib
import contextvars
import inspect
import json
import typing as t
from uuid import uuid4

import typing_extensions as te
from loguru import logger
from pydantic import (
    ConfigDict,
    Field,
    FilePath,
    TypeAdapter,
    model_validator,
)

from dreadnode.core.discovery import find
from dreadnode.core.execution import Executor
from dreadnode.core.meta import Config
from dreadnode.core.scorer import Scorer, ScorersLike
from dreadnode.core.task import Task
from dreadnode.core.types.common import AnyDict, Unset
from dreadnode.core.util import concurrent_gen, get_callable_name, shorten_string
from dreadnode.datasets import load_dataset
from dreadnode.evaluations.events import (
    EvalEnd,
    EvalEvent,
    EvalSample,
    EvalStart,
)
from dreadnode.evaluations.result import EvalResult
from dreadnode.evaluations.sample import Sample
from dreadnode.tracing.constants import (
    EVALUATION_ATTRIBUTE_DATASET_SIZE,
    EVALUATION_ATTRIBUTE_ITERATIONS,
    EVALUATION_ATTRIBUTE_NAME,
    EVALUATION_ATTRIBUTE_SCORERS,
)

In = te.TypeVar("In", default=t.Any)
Out = te.TypeVar("Out", default=t.Any)

InputDataset = list[In]
InputDatasetProcessor = t.Callable[[InputDataset], InputDataset]
DatasetLike = InputDataset[In] | list[AnyDict]


class DatasetProducer(t.Protocol[In]):
    def __call__(self) -> t.Awaitable[DatasetLike[In]] | DatasetLike[In]: ...


DatasetOrProducer = DatasetLike | DatasetProducer

current_dataset_row = contextvars.ContextVar[t.Mapping[str, t.Any] | None](
    "current_dataset_row", default=None
)


class EvalWarning(UserWarning):
    """Warning raised during evaluation."""


class _ErrorTracker:
    """Tracks errors during evaluation for circuit-breaker logic."""

    def __init__(self, max_errors: int | None, max_consecutive_errors: int | None) -> None:
        self.max_errors = max_errors
        self.max_consecutive_errors = max_consecutive_errors
        self.total_errors: int = 0
        self.consecutive_errors: int = 0

    def record_success(self) -> None:
        self.consecutive_errors = 0

    def record_error(self) -> str | None:
        self.total_errors += 1
        self.consecutive_errors += 1

        if self.max_errors is not None and self.total_errors >= self.max_errors:
            return "max_errors_reached"
        if (
            self.max_consecutive_errors is not None
            and self.consecutive_errors >= self.max_consecutive_errors
        ):
            return "max_consecutive_errors_reached"
        return None


class Evaluation(Executor[EvalEvent[In, Out], EvalResult[In, Out]], t.Generic[In, Out]):
    """
    Evaluation of a task against a dataset.

    Attributes:
        task: The task to evaluate.
        dataset: The dataset to use for the evaluation.
        dataset_file: File path of a JSONL, CSV, JSON, or YAML dataset.
        name: The name of the evaluation.
        dataset_input_mapping: Mapping from dataset keys to task parameter names.
        preprocessor: Optional preprocessor for the dataset.
        scorers: Scorers to evaluate task output.
        assert_scores: Scores to assert are truthy.
        trace: Whether to produce trace contexts.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True, use_attribute_docstrings=True)

    name: str = ""
    tags: list[str] = Config(default_factory=lambda: ["eval"])

    task: Task[..., Out] | str
    dataset: t.Any | None = None
    dataset_file: FilePath | str | None = Config(default=None)
    dataset_input_mapping: list[str] | dict[str, str] | None = None
    preprocessor: InputDatasetProcessor | None = None
    scorers: ScorersLike[Out] = Field(default_factory=list)
    assert_scores: list[str] | t.Literal[True] = Field(default_factory=list)
    iterations: int = Config(default=1, ge=1)
    parameters: dict[str, list[t.Any]] | None = None
    trace: bool = True
    max_errors: int | None = Config(default=None)
    """Maximum total errors before stopping the evaluation."""
    max_consecutive_errors: int | None = Config(default=10)
    """Maximum consecutive errors before stopping the evaluation."""

    def model_post_init(self, context: t.Any) -> None:
        super().model_post_init(context)
        if not self.name:
            self.name = f"Eval {self.task_name}"

    @model_validator(mode="after")
    def _check_dataset(self) -> te.Self:
        if self.dataset is None and self.dataset_file is None:
            raise ValueError("One of 'dataset' or 'dataset_file' must be provided.")
        return self

    @property
    def task_name(self) -> str:
        if isinstance(self.task, str):
            return self.task.split(".")[-1]
        return self.task.name

    def __repr__(self) -> str:
        description = shorten_string(self.description or "", 50)
        parts: list[str] = [
            f"name='{self.name}'",
            f"description='{description}'",
            f"task={self.task!r}",
            f"dataset={self.dataset!r}",
        ]
        if self.scorers:
            scorers = ", ".join(
                get_callable_name(s, short=True) for s in Scorer.fit_many(self.scorers)
            )
            parts.append(f"scorers=[{scorers}]")
        if self.assert_scores:
            parts.append(f"assertions={self.assert_scores}")
        if self.concurrency > 1:
            parts.append(f"concurrency={self.concurrency}")
        if self.iterations > 1:
            parts.append(f"iterations={self.iterations}")
        return f"{self.__class__.__name__}({', '.join(parts)})"

    def _extract_result(self, event: EvalEvent[In, Out]) -> EvalResult[In, Out] | None:
        """Extract result from EvalEnd event."""
        if isinstance(event, EvalEnd):
            return event.result  # ty: ignore[invalid-return-type]
        return None

    def _should_trace(self) -> bool:
        """Evaluation handles its own tracing per sample."""
        return False

    def _create_error_tracker(self) -> _ErrorTracker:
        """Create an error tracker for circuit-breaker logic."""
        return _ErrorTracker(
            max_errors=self.max_errors,
            max_consecutive_errors=self.max_consecutive_errors,
        )

    async def _stream_batch(
        self,
        batch: list[t.Any],  # noqa: ARG002
    ) -> t.AsyncGenerator[EvalEvent[In, Out], None]:
        """Evaluation uses _stream, not _stream_batch."""
        raise NotImplementedError("Evaluation uses _stream, not _stream_batch")
        yield  # pragma: no cover - make this a generator

    async def _stream(self) -> t.AsyncGenerator[EvalEvent[In, Out], None]:
        """Core evaluation execution loop."""
        from dreadnode import task_and_run

        task, dataset = await self._prepare_task_and_dataset()
        scorers = Scorer.fit_many(self.scorers or [])

        dataset_keys = list(dataset[0].keys()) if dataset else []
        self._validate_scorers(scorers, dataset_keys=dataset_keys)

        logger.info(
            f"Starting Eval '{self.name}': "
            f"task='{task.name}', "
            f"dataset_size={len(dataset)}, "
            f"iterations={self.iterations}, "
            f"concurrency={self.concurrency}"
        )

        eval_id = uuid4()
        yield EvalStart(
            eval_id=eval_id,
            eval_name=self.name,
            dataset_size=len(dataset),
            iterations=self.iterations,
        )

        result = EvalResult[In, Out]()
        error_tracker = self._create_error_tracker()

        trace_context = (
            task_and_run(
                name=self.name,
                task_type="evaluation",
                tags=self.tags,
                label=self.label,
            )
            if self.trace
            else contextlib.nullcontext()
        )

        with trace_context as task_span:
            if task_span is not None:
                task_span.set_attribute(EVALUATION_ATTRIBUTE_NAME, self.name)
                task_span.set_attribute(EVALUATION_ATTRIBUTE_DATASET_SIZE, len(dataset))
                task_span.set_attribute(EVALUATION_ATTRIBUTE_ITERATIONS, self.iterations)
                scorer_names = [scorer.name for scorer in scorers]
                task_span.set_attribute(EVALUATION_ATTRIBUTE_SCORERS, json.dumps(scorer_names))
                task_span.log_param("dataset_size", len(dataset))
                task_span.log_param("scenario_count", 1)
                task_span.log_param("iterations", self.iterations)

            def emit_event(event: EvalEvent) -> None:
                if task_span is not None:
                    event.emit(task_span)

            configured_task = task.with_(
                scorers=scorers,
                assert_scores=self.assert_scores,
                append=True,
            )

            async for sample in self._run_samples(configured_task, dataset):
                sample_event = EvalSample(
                    eval_id=eval_id,
                    eval_name=self.name,
                    sample_index=sample.index,
                    input=sample.input,
                    output=sample.output,
                    scores={k: v.value for k, v in sample.metrics.items() if v.value is not None},
                    passed=sample.passed,
                    error=str(sample.error)[:500] if sample.error else None,
                )
                emit_event(sample_event)
                yield sample_event
                result.samples.append(sample)

                if not sample.failed:
                    error_tracker.record_success()
                    continue

                if stop_reason := error_tracker.record_error():
                    result.stop_reason = stop_reason  # ty: ignore[invalid-assignment]
                    logger.warning(
                        f"Stopping evaluation: reason='{stop_reason}', "
                        f"consecutive_errors={error_tracker.consecutive_errors}, "
                        f"total_errors={error_tracker.total_errors}"
                    )
                    eval_end = EvalEnd(
                        eval_id=eval_id,
                        eval_name=self.name,
                        result=result,
                        total_samples=len(result.samples),
                        passed_count=result.passed_count,
                        failed_count=result.failed_count,
                        error_count=result.error_count,
                        pass_rate=result.pass_rate,
                        stop_reason=result.stop_reason,
                        mean_scores=result.metrics_aggregated,
                    )
                    emit_event(eval_end)
                    yield eval_end
                    return

        result.stop_reason = "finished"
        logger.success(
            f"Finished Eval '{self.name}': "
            f"passed={result.passed_count}, failed={result.failed_count}, "
            f"pass_rate={result.pass_rate:.2%}"
        )
        eval_end = EvalEnd(
            eval_id=eval_id,
            eval_name=self.name,
            result=result,
            total_samples=len(result.samples),
            passed_count=result.passed_count,
            failed_count=result.failed_count,
            error_count=result.error_count,
            pass_rate=result.pass_rate,
            stop_reason=result.stop_reason,
            mean_scores=result.metrics_aggregated,
        )
        if task_span is not None:
            eval_end.emit(task_span)
        yield eval_end

    async def _run_samples(
        self,
        configured_task: Task[[In], Out],
        dataset: list[AnyDict],
    ) -> t.AsyncGenerator[Sample[In, Out], None]:
        """Run all samples concurrently."""
        expanded_dataset = [row for _ in range(self.iterations) for row in dataset]
        total_samples = len(expanded_dataset)

        async def _run_sample(index: int, row: AnyDict) -> Sample[In, Out]:
            token = current_dataset_row.set(row)
            try:
                task_params = set(configured_task.signature.parameters)
                if self.dataset_input_mapping:
                    if isinstance(self.dataset_input_mapping, list):
                        task_kwargs = {k: row[k] for k in self.dataset_input_mapping}
                    else:
                        task_kwargs = {
                            task_arg: row[ds_key]
                            for ds_key, task_arg in self.dataset_input_mapping.items()
                        }
                else:
                    task_kwargs = {k: v for k, v in row.items() if k in task_params}

                context = {f"dataset_{k}": v for k, v in row.items() if k not in task_kwargs}
                first_kwarg = next(iter(task_kwargs.values()), None)
                task_input = task_kwargs if len(task_kwargs) > 1 else first_kwarg

                indexed_task = configured_task.with_(
                    name=f"{configured_task.name} [{index + 1}/{total_samples}]"
                )
                span = await indexed_task.run_always(  # ty: ignore[missing-argument]
                    **{**task_kwargs, "__dn_ctx_inputs__": context}
                )

                return Sample.from_task(
                    configured_task,
                    span,
                    task_input,
                    index=index,
                    context=context,
                )
            finally:
                current_dataset_row.reset(token)

        coroutines = [_run_sample(index, row) for index, row in enumerate(expanded_dataset)]
        async with concurrent_gen(coroutines, self.concurrency) as sample_stream:
            async for sample in sample_stream:
                yield sample

    def with_(  # ty: ignore[invalid-method-override]
        self,
        *,
        name: str | None = None,
        description: str | None = None,
        tags: list[str] | None = None,
        label: str | None = None,
        task: Task[..., Out] | str | None = None,
        dataset: t.Any | None = None,
        concurrency: int | None = None,
        iterations: int | None = None,
        max_errors: int | None = None,
        max_consecutive_errors: int | None = None,
        parameters: dict[str, list[t.Any]] | None = None,
        scorers: ScorersLike[Out] | None = None,
        assert_scores: list[str] | t.Literal[True] | None = None,
        append: bool = False,
    ) -> te.Self:
        """Create a modified clone of the evaluation."""
        new = self.clone()  # ty: ignore[unresolved-attribute]

        updates = {
            "name_": name,
            "description": description,
            "label": label,
            "task": task,
            "dataset": dataset,
            "concurrency": concurrency,
            "iterations": iterations,
            "max_errors": max_errors,
            "max_consecutive_errors": max_consecutive_errors,
            "parameters": parameters,
            "assert_scores": assert_scores,
        }
        for field, value in updates.items():
            if value is not None:
                setattr(new, field, value)

        new._apply_updates(
            {"tags": tags, "scorers": Scorer.fit_many(scorers) if scorers else None},
            list_fields={"tags", "scorers"},
            append=append,
        )

        return new

    async def console(self) -> EvalResult[In, Out]:
        """Run the evaluation with a live display in the console."""
        from dreadnode.evaluations.console import EvalConsoleAdapter

        adapter = EvalConsoleAdapter(self)
        return await adapter.run()

    @classmethod
    def _generic_types(cls) -> tuple[type[In], type[Out]]:
        for c in cls.__mro__:
            if hasattr(c, "__origin__") and c.__origin__ is not t.Generic:
                continue
            metadata = getattr(c, "__pydantic_generic_metadata__", {})
            args = metadata.get("args", ()) or getattr(c, "__args__", ())
            if len(args) == 2:
                if all(not isinstance(a, t.TypeVar) and not hasattr(a, "__origin__") for a in args):
                    return args  # ty: ignore[invalid-return-type]
        return t.Any, t.Any  # ty: ignore[invalid-return-type]

    async def _prepare_task_and_dataset(self) -> tuple[Task[[In], Out], list[AnyDict]]:
        task = find(Task, self.task) if isinstance(self.task, str) else self.task

        dataset = self.dataset
        if self.dataset_file is not None:
            dataset = load_dataset(str(self.dataset_file))

        if inspect.isfunction(dataset):
            dataset = dataset()
            if inspect.isawaitable(dataset):
                dataset = await dataset

        input_type, _ = self._generic_types()
        if input_type is not t.Any:
            dataset = TypeAdapter(list[input_type]).validate_python(dataset)  # ty: ignore[invalid-type-form]
        elif not isinstance(dataset, list):
            dataset = list(dataset)

        if self.preprocessor:
            dataset = self.preprocessor(dataset)

        return task, dataset

    def _validate_scorers(self, scorers: list[Scorer[t.Any]], dataset_keys: list[str]) -> None:
        for scorer in scorers:
            defaults = scorer.defaults
            required_params = [
                name for name, default in defaults.items() if isinstance(default, Unset)
            ]
            if len(required_params) > 1:
                raise ValueError(
                    f"Scorer '{scorer.name}' has more than one required parameter. "
                    "Configure defaults or use DatasetField."
                )

            from dreadnode.core.meta import DatasetField

            dataset_params = {
                name: value for name, value in defaults.items() if isinstance(value, DatasetField)
            }
            for value in dataset_params.values():
                if value.ref_name not in dataset_keys:
                    raise ValueError(
                        f"Scorer '{scorer.name}' references dataset field '{value.ref_name}' "
                        "which is not available."
                    )
