# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union, Iterable, Optional
from typing_extensions import Literal, Required, TypedDict

__all__ = ["EvaluationEvaluateParams", "Evaluator", "EvaluatedModelAttachment"]


class EvaluationEvaluateParams(TypedDict, total=False):
    evaluators: Required[Iterable[Evaluator]]
    """List of evaluators to evaluate against."""

    app: Optional[str]
    """Assigns evaluation results to the app.

    - `app` cannot be used together with `experiment_id`.
    - If `app` and `experiment_id` is omitted, `app` is set automatically to
      "default" on capture.
    - Automatically creates an app if it doesn't exist.
    - Only relevant for captured results. If will capture the results under given
      app.
    """

    capture: Literal["all", "fails-only", "none"]
    """Capture evaluation result based on given option, default is none:

    - `all` captures the result of all evaluations (pass + failed).
    - `fails-only` captures the evaluation result when evaluation failed.
    - `none` does not capture evaluation result
    """

    confidence_interval_strategy: Literal["none", "full-history"]
    """Create confidence intervals based on one of the following strategies:

    - 'none': returns None
    - 'full-history': calculates upper boundary, median, and lower boundary of
      confidence interval based on all available historic records.
    - 'generated': calculates upper boundary, median, and lower boundary of
      confidence interval based on on-flight generated sample of evaluations.
    """

    dataset_id: Optional[str]
    """
    The ID of the dataset from which the evaluated sample originates. This field
    serves as metadata for the evaluation. This endpoint does not ensure data
    consistency for this field. There is no guarantee that the dataset with the
    given ID is present in the Patronus AI platform, as this is a self-reported
    value.
    """

    dataset_sample_id: Optional[str]
    """
    The ID of the sample within the dataset. This field serves as metadata for the
    evaluation. This endpoint does not ensure data consistency for this field. There
    is no guarantee that the dataset and sample are present in the Patronus AI
    platform, as this is a self-reported value.
    """

    evaluated_model_attachments: Optional[Iterable[EvaluatedModelAttachment]]
    """
    Optional list of attachments to be associated with the evaluation sample. This
    will be added to all evaluation results in this request. Each attachment is a
    dictionary with the following keys:

    - `url`: URL of the attachment.
    - `media_type`: Media type of the attachment (e.g., "image/jpeg", "image/png").
    - `usage_type`: Type of the attachment (e.g., "evaluated_model_system_prompt",
      "evaluated_model_input").
    """

    experiment_id: Optional[str]
    """Assign evaluation results to the experiment.

    - `experiment_id` cannot be used together with `app`.
    - Only relevant for captured results. If will capture the results under
      experiment.
    """

    gold_answer: Optional[str]
    """Gold answer for given evaluated model input"""

    log_id: Optional[str]

    project_id: Optional[str]
    """Attach project with given ID to the evaluation.

    **Note**: This parameter is ignored in case project_name or experiment_id is
    provided.
    """

    project_name: Optional[str]
    """
    Attach project with given name to the evaluation. If project with given name
    doesn't exist, one will be created.

    **Note:** This parameter is ignored in case experiment_id is provided.

    **Note:** This parameter takes precedence over project_id.
    """

    span_id: Optional[str]

    system_prompt: Optional[str]
    """The system prompt provided to the LLM."""

    tags: object
    """Tags are key-value pairs used to label resources"""

    task_context: Union[List[str], str, None]
    """
    Optional context retrieved from vector database. This is a list of strings, with
    the following restrictions:

    - Number of items must be less/equal than 50.
    - The sum of tokens in all elements must be less/equal than 120000, using
      o200k_base tiktoken encoding
    """

    task_input: Optional[str]
    """The input (prompt) provided to LLM."""

    task_output: Optional[str]
    """LLM's response to the given input."""

    trace_id: Optional[str]


class Evaluator(TypedDict, total=False):
    evaluator: Required[str]
    """Evaluator identifier, alias or id"""

    criteria: Optional[str]
    """Name of the criteria used for evaluator parametrization."""

    explain_strategy: Literal["never", "on-fail", "on-success", "always"]
    """
    Request evaluation result explanation based on given strategy, default is
    `None` - `never` do not explain any evaluation results - `on-fail` explains the
    result for failed evaluations only - `on-success` explains the result for passed
    evaluations only - `always` explains the result for all evaluations

                *Not all evaluation criteria support explanations.
                *Ignored if evaluation criteria don't support explanations.
                *`explain_strategy` is overwriting the `explain` parameter.
    """


class EvaluatedModelAttachment(TypedDict, total=False):
    media_type: Required[
        Literal["image/jpeg", "image/png", "audio/flac", "audio/mp3", "audio/mp4", "audio/mpeg", "audio/wav"]
    ]

    url: Required[str]

    usage_type: Literal[
        "evaluated_model_system_prompt",
        "evaluated_model_input",
        "evaluated_model_output",
        "evaluated_model_gold_answer",
        "evaluated_model_retrieved_context",
    ]
