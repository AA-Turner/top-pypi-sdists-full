from datetime import datetime, timezone
from typing import Dict, List, Optional, Sequence, Type, TypeAlias, Union

from pydantic import UUID4, BaseModel, Field, TypeAdapter, field_validator
from pydantic_partial import PartialModelMixin
from typing_extensions import Annotated, Any, get_args

from galileo_core.schemas.logging.session import BaseSession
from galileo_core.schemas.logging.span import BaseAgentSpan, BaseRetrieverSpan, BaseToolSpan, BaseWorkflowSpan, LlmSpan
from galileo_core.schemas.logging.step import BaseStep, StepAllowedInputType
from galileo_core.schemas.logging.trace import BaseTrace
from galileo_core.schemas.shared.feedback import FeedbackRatingInfo


class RecordIdsWithMetrics(BaseModel):
    id: UUID4
    project_id: UUID4
    run_id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = Field(default=None)
    metrics: Dict[str, Any]


class BaseRecord(PartialModelMixin, BaseStep):
    id: UUID4 = Field(title="ID", description="Galileo ID of the session, trace or span")
    session_id: UUID4 = Field(title="Session ID", description="Galileo ID of the session")
    trace_id: Optional[UUID4] = Field(
        default=None,
        title="Trace ID",
        description="Galileo ID of the trace containing the span (or the same value as id for a trace)",
    )
    project_id: UUID4 = Field(
        title="Project ID", description="Galileo ID of the project associated with this trace or span"
    )
    run_id: UUID4 = Field(
        title="Run ID",
        description="Galileo ID of the run (log stream or experiment) associated with this trace or span",
    )
    updated_at: Optional[datetime] = Field(
        default=None, title="Last Updated", description="Timestamp of the session or trace or span's last update"
    )
    has_children: Optional[bool] = Field(default=None, description="Whether or not this trace or span has child spans")
    metrics_batch_id: Optional[UUID4] = Field(
        default=None, description="Galileo ID of the metrics batch associated with this trace or span"
    )
    session_batch_id: Optional[UUID4] = Field(
        default=None, description="Galileo ID of the metrics batch associated with this trace or span"
    )
    feedback_rating_info: Dict[str, FeedbackRatingInfo] = Field(
        default_factory=dict, description="Feedback information related to the record"
    )

    def to_record_ids_with_metrics(self) -> RecordIdsWithMetrics:
        return RecordIdsWithMetrics(
            id=self.id,
            project_id=self.project_id,
            run_id=self.run_id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            metrics=self.metrics.model_dump(exclude_unset=True, exclude_none=True),
        )

    @field_validator("created_at", "updated_at", mode="after")
    def ensure_tz_aware(cls, value: Optional[datetime]) -> Optional[datetime]:
        if value is None:
            return None
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value


class TraceRecord(BaseTrace, BaseRecord):
    session_id: UUID4 = Field(
        title="Session ID",
        description="Galileo ID of the session containing the trace (or the same value as id for a trace)",
    )
    trace_id: UUID4 = Field(
        title="Trace ID",
        description="Galileo ID of the trace containing the span (or the same value as id for a trace)",
    )
    id: UUID4 = Field(title="ID", description="Galileo ID of the trace")
    is_complete: bool = Field(default=True, description="Whether the trace is complete or not")


class SessionRecord(BaseSession, BaseRecord):
    id: UUID4 = Field(title="ID", description="Galileo ID of the session")
    input: StepAllowedInputType = Field(default="", validate_default=True)

    @field_validator("input", mode="after")
    def ensure_non_null_input(cls, value: Optional[StepAllowedInputType]) -> StepAllowedInputType:
        if value is None:
            value = ""
        return value


class BaseSpanRecord(BaseRecord):
    trace_id: UUID4 = Field(
        title="Trace ID",
        description="Galileo ID of the trace containing the span (or the same value as id for a trace)",
    )
    parent_id: UUID4 = Field(title="Parent ID", description="Galileo ID of the parent of this span")
    is_complete: bool = Field(default=True, description="Whether the parent trace is complete or not")


class WorkflowSpanRecord(BaseWorkflowSpan, BaseSpanRecord):
    session_id: UUID4 = Field(
        title="Session ID",
        description="Galileo ID of the session containing the trace (or the same value as id for a trace)",
    )
    parent_id: UUID4 = Field(title="Parent ID", description="Galileo ID of the parent of this span")
    id: UUID4 = Field(title="ID", description="Galileo ID of the session, trace or span")


class AgentSpanRecord(BaseAgentSpan, BaseSpanRecord):
    session_id: UUID4 = Field(
        title="Session ID",
        description="Galileo ID of the session containing the trace (or the same value as id for a trace)",
    )
    parent_id: UUID4 = Field(title="Parent ID", description="Galileo ID of the parent of this span")
    id: UUID4 = Field(title="ID", description="Galileo ID of the session, trace or span")


class LlmSpanRecord(LlmSpan, BaseSpanRecord):
    session_id: UUID4 = Field(
        title="Session ID",
        description="Galileo ID of the session containing the trace (or the same value as id for a trace)",
    )
    parent_id: UUID4 = Field(title="Parent ID", description="Galileo ID of the parent of this span")
    id: UUID4 = Field(title="ID", description="Galileo ID of the session, trace or span")


class ToolSpanRecord(BaseToolSpan, BaseSpanRecord):
    session_id: UUID4 = Field(
        title="Session ID",
        description="Galileo ID of the session containing the trace (or the same value as id for a trace)",
    )
    parent_id: UUID4 = Field(title="Parent ID", description="Galileo ID of the parent of this span")
    id: UUID4 = Field(title="ID", description="Galileo ID of the session, trace or span")


class RetrieverSpanRecord(BaseRetrieverSpan, BaseSpanRecord):
    session_id: UUID4 = Field(
        title="Session ID",
        description="Galileo ID of the session containing the trace (or the same value as id for a trace)",
    )
    parent_id: UUID4 = Field(title="Parent ID", description="Galileo ID of the parent of this span")
    id: UUID4 = Field(title="ID", description="Galileo ID of the session, trace or span")


SpanRecord = Annotated[
    Union[
        AgentSpanRecord,
        WorkflowSpanRecord,
        LlmSpanRecord,
        ToolSpanRecord,
        RetrieverSpanRecord,
    ],
    Field(discriminator="type"),
]


SpanRecordAdapter: TypeAdapter[SpanRecord] = TypeAdapter(SpanRecord)


SpanRecordTypes: List[Type[BaseRecord]] = list(get_args(get_args(SpanRecord)[0]))


TraceOrSpanRecord = Annotated[
    Union[
        TraceRecord,
        SpanRecord,
    ],
    Field(discriminator="type"),
]


TraceOrSpanRecordAdapter: TypeAdapter[TraceOrSpanRecord] = TypeAdapter(TraceOrSpanRecord)


RecordType = Annotated[
    Union[
        TraceRecord,
        SpanRecord,
        SessionRecord,
    ],
    Field(discriminator="type"),
]


RecordTypeAdapter: TypeAdapter[RecordType] = TypeAdapter(RecordType)


class RecordWithChildSpans(BaseModel):
    spans: Sequence["SpanRecordWithChildren"] = Field(default_factory=list)


class TraceRecordWithChildren(TraceRecord, RecordWithChildSpans):
    pass


class RecordWithChildTraces(BaseModel):
    traces: Sequence["TraceRecordWithChildren"] = Field(default_factory=list)


class WorkflowSpanRecordWithChildren(WorkflowSpanRecord, RecordWithChildSpans):
    pass


class AgentSpanRecordWithChildren(AgentSpanRecord, RecordWithChildSpans):
    pass


class RetrieverSpanRecordWithChildren(RetrieverSpanRecord, RecordWithChildSpans):
    pass


class ToolSpanRecordWithChildren(ToolSpanRecord, RecordWithChildSpans):
    pass


SpanRecordWithChildren = Annotated[
    Union[
        AgentSpanRecordWithChildren,
        WorkflowSpanRecordWithChildren,
        LlmSpanRecord,
        ToolSpanRecordWithChildren,
        RetrieverSpanRecordWithChildren,
    ],
    Field(discriminator="type"),
]


class SessionRecordWithChildren(SessionRecord, RecordWithChildTraces):
    pass


SpanRecordWithChildrenAdapter: TypeAdapter[SpanRecordWithChildren] = TypeAdapter(SpanRecordWithChildren)


PartialAgentSpanRecord: TypeAlias = AgentSpanRecord.model_as_partial()  # type: ignore[valid-type]
PartialWorkflowSpanRecord: TypeAlias = WorkflowSpanRecord.model_as_partial()  # type: ignore[valid-type]
PartialLlmSpanRecord: TypeAlias = LlmSpanRecord.model_as_partial()  # type: ignore[valid-type]
PartialToolSpanRecord: TypeAlias = ToolSpanRecord.model_as_partial()  # type: ignore[valid-type]
PartialRetrieverSpanRecord: TypeAlias = RetrieverSpanRecord.model_as_partial()  # type: ignore[valid-type]
PartialTraceRecord: TypeAlias = TraceRecord.model_as_partial()  # type: ignore[valid-type]
PartialSessionRecord: TypeAlias = SessionRecord.model_as_partial()  # type: ignore[valid-type]


PartialSpanRecord: TypeAlias = Annotated[
    Union[
        PartialAgentSpanRecord,
        PartialWorkflowSpanRecord,
        PartialLlmSpanRecord,
        PartialToolSpanRecord,
        PartialRetrieverSpanRecord,
    ],
    Field(discriminator="type"),
]


PartialSpanRecordAdapter: TypeAdapter[PartialSpanRecord] = TypeAdapter(PartialSpanRecord)  # type: ignore[valid-type]


PartialSpanRecordTypes: List[Type[BaseRecord]] = list(get_args(get_args(PartialSpanRecord)[0]))


PartialRecordType: TypeAlias = Annotated[
    Union[
        PartialTraceRecord,
        PartialSpanRecord,
        PartialSessionRecord,
    ],
    Field(discriminator="type"),
]


PartialRecordTypeAdapter: TypeAdapter[PartialRecordType] = TypeAdapter(PartialRecordType)  # type: ignore[valid-type]
