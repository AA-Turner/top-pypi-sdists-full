# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from datetime import datetime
from typing_extensions import Literal, TypeAlias

from ..._models import BaseModel
from .flexible_chunk import FlexibleChunk
from ..evaluation_datasets.flexible_message import FlexibleMessage

__all__ = [
    "EvaluationTraceSpan",
    "OperationInput",
    "OperationInputExternalFile",
    "OperationInputInternalFile",
    "OperationOutput",
    "OperationOutputExternalFile",
    "OperationOutputInternalFile",
    "OperationExpected",
    "OperationExpectedExternalFile",
    "OperationExpectedInternalFile",
]


class OperationInputExternalFile(BaseModel):
    file_type: Literal["image", "pdf"]

    uri: str


class OperationInputInternalFile(BaseModel):
    file_id: str

    file_type: Literal["image", "pdf"]


OperationInput: TypeAlias = Union[
    str,
    float,
    List[FlexibleChunk],
    List[FlexibleMessage],
    List[object],
    Dict[str, object],
    OperationInputExternalFile,
    OperationInputInternalFile,
]


class OperationOutputExternalFile(BaseModel):
    file_type: Literal["image", "pdf"]

    uri: str


class OperationOutputInternalFile(BaseModel):
    file_id: str

    file_type: Literal["image", "pdf"]


OperationOutput: TypeAlias = Union[
    str,
    float,
    List[FlexibleChunk],
    List[FlexibleMessage],
    List[object],
    Dict[str, object],
    OperationOutputExternalFile,
    OperationOutputInternalFile,
]


class OperationExpectedExternalFile(BaseModel):
    file_type: Literal["image", "pdf"]

    uri: str


class OperationExpectedInternalFile(BaseModel):
    file_id: str

    file_type: Literal["image", "pdf"]


OperationExpected: TypeAlias = Union[
    str,
    float,
    List[FlexibleChunk],
    List[FlexibleMessage],
    List[object],
    Dict[str, object],
    OperationExpectedExternalFile,
    OperationExpectedInternalFile,
]


class EvaluationTraceSpan(BaseModel):
    id: str
    """Identifies the application step"""

    duration_ms: int
    """How much time the step took in milliseconds(ms)"""

    node_id: str
    """The id of the node in the application_variant config that emitted this insight"""

    operation_input: Dict[str, OperationInput]
    """The JSON representation of the input that this step received."""

    operation_output: Dict[str, OperationOutput]
    """The JSON representation of the output that this step emitted."""

    operation_status: Literal["SUCCESS", "ERROR", "CANCELED"]
    """The outcome of the operation"""

    operation_type: Literal[
        "TEXT_INPUT",
        "TEXT_OUTPUT",
        "COMPLETION_INPUT",
        "COMPLETION",
        "KB_RETRIEVAL",
        "KB_INPUT",
        "RERANKING",
        "EXTERNAL_ENDPOINT",
        "PROMPT_ENGINEERING",
        "DOCUMENT_INPUT",
        "MAP_REDUCE",
        "DOCUMENT_SEARCH",
        "DOCUMENT_PROMPT",
        "CUSTOM",
        "CODE_EXECUTION",
        "DATA_MANIPULATION",
        "EVALUATION",
        "FILE_RETRIEVAL",
        "KB_ADD_CHUNK",
        "KB_MANAGEMENT",
        "GUARDRAIL",
        "TRACER",
        "AGENT_TRACER",
        "AGENT_WORKFLOW",
        "STANDALONE",
    ]
    """Type of the operation, e.g. RERANKING"""

    start_timestamp: datetime
    """The start time of the step"""

    account_id: Optional[str] = None
    """The ID of the account that owns the given entity."""

    application_interaction_id: Optional[str] = None
    """The interaction ID this span belongs to"""

    application_variant_id: Optional[str] = None
    """The id of the application variant this span belongs to"""

    created_by_identity_type: Optional[Literal["user", "service_account"]] = None
    """The type of identity that created the entity."""

    created_by_user_id: Optional[str] = None
    """The user who originally created the entity."""

    end_timestamp: Optional[datetime] = None
    """
    The end time of the step, nullable, since it can be set to done at a later point
    in time.
    """

    group_id: Optional[str] = None
    """The ID of the group this span belongs to"""

    operation_expected: Optional[Dict[str, OperationExpected]] = None
    """The JSON representation of the expected output for this step"""

    operation_metadata: Optional[Dict[str, object]] = None
    """The JSON representation of the metadata insights emitted through the execution.

    This can differ based on different types of operations
    """

    parent_id: Optional[str] = None
    """Who is the parent span of this current span, null if span is root parent."""

    trace_id: Optional[str] = None
    """The root-level ID where this span belongs to"""
