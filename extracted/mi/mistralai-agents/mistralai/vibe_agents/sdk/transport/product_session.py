"""Describe a Vibe Agents product Session row as a Harness Session."""

from datetime import datetime

from mistralai.vibe.harness.app_server import session as harness_session
from mistralai.vibe_agents.sessions_client import AgentSessionResponse, AgentSessionStatus


def build_session_from_product(product: AgentSessionResponse) -> harness_session.Session:
    """Describe a product session row as a Harness session, before any event is folded."""

    status: harness_session.SessionStatus
    termination: harness_session.Termination | None = None
    if product.status is AgentSessionStatus.WAITING:
        status = "waiting"
    elif product.status in {
        AgentSessionStatus.COMPLETED,
        AgentSessionStatus.FAILED,
        AgentSessionStatus.TERMINATED,
    }:
        status = "terminated"
        if product.status is AgentSessionStatus.FAILED:
            termination = harness_session.FailedTermination(
                error=harness_session.ProtocolError(
                    code="remote_session_failed",
                    message=product.error or "Remote Session failed",
                )
            )
        elif product.status is AgentSessionStatus.TERMINATED:
            termination = harness_session.CancelledTermination(reason=product.error, cause=_cancelled_cause(product))
        else:
            termination = harness_session.CompletedTermination()
    else:
        status = "running"
    session_id = str(product.agent_session_id)
    return harness_session.Session(
        id=session_id,
        root_session_id=str(product.root_session_id or product.agent_session_id),
        parent_session_id=str(product.parent_session_id) if product.parent_session_id is not None else None,
        title=product.title if "title" in product.model_fields_set else product.generated_title,
        archived_at=_datetime_ms(product.archived_at) if product.archived_at is not None else None,
        status=status,
        termination=termination,
        created_at=_datetime_ms(product.created_at),
        updated_at=_datetime_ms(product.updated_at),
    )


def _cancelled_cause(product: AgentSessionResponse) -> str | None:
    """The Session limit that stopped the Session, recorded on its terminal output."""

    cause = (product.terminal_output or {}).get("cause")
    return cause if isinstance(cause, str) else None


def _datetime_ms(value: datetime) -> int:
    return int(value.timestamp() * 1000)
