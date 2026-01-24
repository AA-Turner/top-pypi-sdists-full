from operator import attrgetter
from typing import Dict, List, Sequence, cast
from uuid import UUID

from galileo_core.schemas.logging.session import BaseSession, Session
from galileo_core.schemas.logging.span import Span
from galileo_core.schemas.logging.step import BaseStep, StepType
from galileo_core.schemas.logging.trace import Trace


def create_tree_for_trace(records: Sequence[BaseStep]) -> Sequence[Trace]:
    parent_id_to_child_ids: Dict[UUID, List[UUID]] = {}
    trace_id_to_trace: Dict[UUID, Trace] = {}
    span_id_to_span: Dict[UUID, Span] = {}
    for record in records:
        if record.id is None:
            raise ValueError("Node ID cannot be None")
        if record.type is StepType.trace:
            trace_id_to_trace[record.id] = Trace.model_validate(record)
        elif record.type is not StepType.session:
            span_id_to_span[record.id] = cast(Span, record)
            if (
                hasattr(record, "parent_id") and record.parent_id is not None
            ):  # Only add value to the parent-child relationship if there is a parent
                if record.parent_id not in parent_id_to_child_ids:
                    parent_id_to_child_ids[record.parent_id] = []
                parent_id_to_child_ids[record.parent_id].append(record.id)

    def populate_child_spans(id: UUID) -> List[Span]:
        child_spans = []
        for child_id in parent_id_to_child_ids.get(id, []):
            span = span_id_to_span[child_id]
            # Only call add_child_spans on spans that support it
            if hasattr(span, "add_child_spans"):
                span.add_child_spans(populate_child_spans(child_id))
            child_spans.append(span)
        return sorted(child_spans, key=lambda record: record.created_at)

    # Build the tree recursively
    traces = []
    for trace_id, trace in trace_id_to_trace.items():
        trace.add_child_spans(populate_child_spans(trace_id))
        traces.append(trace)

    return traces


def create_tree_for_session(records: Sequence[BaseStep]) -> List[Session]:
    session_id_to_session: Dict[UUID, Session] = {}
    session_id_to_children: Dict[UUID, List[BaseStep]] = {}
    for record in records:
        if record.id is None:
            raise ValueError("Node ID cannot be None")
        if record.type is StepType.session:
            session = BaseSession.model_validate(record)
            session_id_to_session[record.id] = Session(**session.model_dump(), traces=[])
        else:
            if (
                hasattr(record, "session_id") and record.session_id is not None
            ):  # Only add value to the Session tree if part of a session
                if record.session_id not in session_id_to_children:
                    session_id_to_children[record.session_id] = []
                session_id_to_children[record.session_id].append(record)

    sessions = []
    for session_id, session in session_id_to_session.items():
        traces = sorted(
            create_tree_for_trace(session_id_to_children.get(session_id, [])),
            key=attrgetter("created_at"),
        )
        session.traces = traces
        sessions.append(session)

    return sessions
