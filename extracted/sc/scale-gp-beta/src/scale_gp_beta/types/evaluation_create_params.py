# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable
from typing_extensions import Required, TypeAlias, TypedDict

from .._types import SequenceNotStr

__all__ = [
    "EvaluationCreateParams",
    "Evaluation",
    "EvaluationEvaluationStandaloneCreateRequest",
    "EvaluationEvaluationFromDatasetCreateRequest",
    "EvaluationEvaluationFromDatasetCreateRequestData",
    "EvaluationEvaluationWithDatasetCreateRequest",
    "EvaluationEvaluationWithDatasetCreateRequestDataset",
]


class EvaluationCreateParams(TypedDict, total=False):
    evaluation: Required[Evaluation]


class EvaluationEvaluationStandaloneCreateRequest(TypedDict, total=False):
    data: Required[Iterable[Dict[str, object]]]
    """Items to be evaluated"""

    name: Required[str]

    description: str

    files: Iterable[Dict[str, str]]
    """Files to be associated to the evaluation"""

    metadata: Dict[str, object]
    """Optional metadata key-value pairs for the evaluation"""

    tags: SequenceNotStr[str]
    """The tags associated with the entity"""

    tasks: Iterable["EvaluationTaskParam"]
    """Tasks allow you to augment and evaluate your data"""

    taxonomy_params: Dict[str, object]
    """Taxonomy params from the task builder.

    When provided, stores directly as evaluation taxonomy.
    """


class EvaluationEvaluationFromDatasetCreateRequestData(TypedDict, total=False, extra_items=object):  # type: ignore[call-arg]
    dataset_item_id: Required[str]


class EvaluationEvaluationFromDatasetCreateRequest(TypedDict, total=False):
    dataset_id: Required[str]
    """The ID of the dataset containing the items referenced by the `data` field"""

    name: Required[str]

    data: Iterable[EvaluationEvaluationFromDatasetCreateRequestData]
    """Items to be evaluated, including references to the input dataset"""

    description: str

    metadata: Dict[str, object]
    """Optional metadata key-value pairs for the evaluation"""

    tags: SequenceNotStr[str]
    """The tags associated with the entity"""

    tasks: Iterable["EvaluationTaskParam"]
    """Tasks allow you to augment and evaluate your data"""

    taxonomy_params: Dict[str, object]
    """Taxonomy params from the task builder.

    When provided, stores directly as evaluation taxonomy.
    """


class EvaluationEvaluationWithDatasetCreateRequestDataset(TypedDict, total=False):
    """Create a reusable dataset from items in the `data` field"""

    name: Required[str]

    description: str

    keys: SequenceNotStr[str]
    """Keys from items in the `data` field that should be included in the dataset.

    If not provided, all keys will be included.
    """

    tags: SequenceNotStr[str]
    """The tags associated with the entity"""


class EvaluationEvaluationWithDatasetCreateRequest(TypedDict, total=False):
    data: Required[Iterable[Dict[str, object]]]
    """Items to be evaluated"""

    dataset: Required[EvaluationEvaluationWithDatasetCreateRequestDataset]
    """Create a reusable dataset from items in the `data` field"""

    name: Required[str]

    description: str

    files: Iterable[Dict[str, str]]
    """Files to be associated to the evaluation"""

    metadata: Dict[str, object]
    """Optional metadata key-value pairs for the evaluation"""

    tags: SequenceNotStr[str]
    """The tags associated with the entity"""

    tasks: Iterable["EvaluationTaskParam"]
    """Tasks allow you to augment and evaluate your data"""

    taxonomy_params: Dict[str, object]
    """Taxonomy params from the task builder.

    When provided, stores directly as evaluation taxonomy.
    """


Evaluation: TypeAlias = Union[
    EvaluationEvaluationStandaloneCreateRequest,
    EvaluationEvaluationFromDatasetCreateRequest,
    EvaluationEvaluationWithDatasetCreateRequest,
]

from .evaluation_task_param import EvaluationTaskParam
