# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable
from datetime import datetime
from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["InteractionCreateParams", "Input", "Output", "OutputContext", "TraceSpan"]


class InteractionCreateParams(TypedDict, total=False):
    application_variant_id: Required[str]
    """Identifier for the application variant that performed this interaction."""

    input: Required[Input]
    """The input data for the interaction."""

    output: Required[Output]
    """The output data from the interaction."""

    start_timestamp: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]
    """Timestamp marking the start of the interaction."""

    duration_ms: int
    """Duration of the interaction in milliseconds."""

    operation_metadata: Dict[str, object]
    """
    Optional metadata related to the operation, including custom or predefined keys.
    """

    operation_status: Literal["SUCCESS", "ERROR"]
    """The outcome status of the interaction."""

    thread_id: str
    """
    Optional UUID identifying the conversation thread associated with the
    interaction.The interaction will be associated with the thread if the id
    represents an existing thread.If the thread with the specified id is not found,
    a new thread will be created.
    """

    trace_spans: Iterable[TraceSpan]
    """
    List of trace spans associated with the interaction.These spans provide insight
    into the individual steps taken by nodes involved in generating the output.
    """


class Input(TypedDict, total=False, extra_items=object):  # type: ignore[call-arg]
    """The input data for the interaction."""

    query: Required[str]
    """The query or input text for the interaction."""


class OutputContext(TypedDict, total=False, extra_items=object):  # type: ignore[call-arg]
    text: Required[str]
    """The text of the context entry."""

    score: float
    """The score of the context entry."""


class Output(TypedDict, total=False, extra_items=object):  # type: ignore[call-arg]
    """The output data from the interaction."""

    response: Required[str]
    """The response or output text of the interaction."""

    context: Iterable[OutputContext]
    """Optional context information provided with the response."""


class TraceSpan(TypedDict, total=False):
    """
    Represents a trace span request, that contains the details of certain steps that took part in the interaction.
    """

    node_id: Required[str]
    """Identifier for the node that emitted this trace span."""

    operation_type: Required[Literal["COMPLETION", "RERANKING", "RETRIEVAL", "CUSTOM"]]
    """Type of the operation, e.g., RERANKING."""

    start_timestamp: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]
    """The start time of the step."""

    account_id: str
    """The ID of the account that owns this trace span."""

    duration_ms: int
    """The duration of the operation step in milliseconds."""

    end_timestamp: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]
    """The end time of the step."""

    operation_input: Dict[str, object]
    """The JSON representation of the input that this step received."""

    operation_metadata: Dict[str, object]
    """The JSON representation of the metadata insights emitted during execution.

    This can differ based on different types of operations.
    """

    operation_output: Dict[str, object]
    """The JSON representation of the output that this step emitted."""

    operation_status: Literal["SUCCESS", "ERROR"]
    """The outcome of the operation performed by this node."""
