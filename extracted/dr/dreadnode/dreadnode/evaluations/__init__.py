import typing as t

from dreadnode.core.scorer import ScorersLike
from dreadnode.evaluations import events
from dreadnode.evaluations.evaluation import (
    DatasetLike,
    Evaluation,
    InputDataset,
    InputDatasetProcessor,
)
from dreadnode.evaluations.events import (
    EvalEnd,
    EvalEvent,
    EvalSample,
    EvalStart,
)
from dreadnode.evaluations.result import EvalResult
from dreadnode.evaluations.sample import Sample

# Rebuild models to resolve forward references
EvalEnd.model_rebuild()


def evaluation(
    func: t.Callable[..., t.Any] | None = None,
    /,
    *,
    dataset: t.Any | None = None,
    dataset_file: str | None = None,
    name: str | None = None,
    description: str = "",
    tags: list[str] | None = None,
    concurrency: int = 1,
    iterations: int = 1,
    max_errors: int | None = None,
    max_consecutive_errors: int = 10,
    dataset_input_mapping: list[str] | dict[str, str] | None = None,
    parameters: dict[str, list[t.Any]] | None = None,
    scorers: ScorersLike[t.Any] | None = None,
    assert_scores: list[str] | t.Literal[True] | None = None,
) -> t.Any:
    """
    Create an Evaluation from a function.

    Can be used as a decorator with or without arguments:

        @dn.evaluation(dataset=[...], scorers=[...])
        async def my_eval(prompt: str) -> str:
            return await my_model(prompt)

        result = await my_eval.run()

    Args:
        func: The task function to evaluate.
        dataset: Inline dataset (list of dicts or objects).
        dataset_file: Path to a dataset file (JSONL, CSV, JSON, YAML).
        name: Name of the evaluation.
        description: Description of the evaluation.
        tags: Tags for the evaluation.
        concurrency: Maximum concurrent samples.
        max_errors: Maximum total errors before stopping.
        max_consecutive_errors: Maximum consecutive errors before stopping.
        dataset_input_mapping: Mapping from dataset keys to task parameter names.
        scorers: Scorers to evaluate task output.
        assert_scores: Score names that must be truthy for a sample to pass.

    Returns:
        An Evaluation instance (if func provided) or a decorator.
    """
    from dreadnode.core.task import task as task_factory

    def make_evaluation(fn: t.Callable[..., t.Any]) -> Evaluation:
        task = task_factory(fn)
        eval_name = name or f"Eval {task.name}"

        return Evaluation(
            name=eval_name,
            description=description,
            task=task,
            dataset=dataset,
            dataset_file=dataset_file,
            dataset_input_mapping=dataset_input_mapping,
            scorers=scorers or [],
            assert_scores=assert_scores or [],
            tags=tags or ["eval"],
            concurrency=concurrency,
            iterations=iterations,
            max_errors=max_errors,
            max_consecutive_errors=max_consecutive_errors,
            parameters=parameters,
        )

    return make_evaluation if func is None else make_evaluation(func)


__all__ = [
    "DatasetLike",
    "EvalEnd",
    "EvalEvent",
    "EvalResult",
    "EvalSample",
    "EvalStart",
    "Evaluation",
    "InputDataset",
    "InputDatasetProcessor",
    "Sample",
    "evaluation",
    "events",
]
