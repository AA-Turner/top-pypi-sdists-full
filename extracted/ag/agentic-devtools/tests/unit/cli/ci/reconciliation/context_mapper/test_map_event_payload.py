import pytest

from agentic_devtools.cli.ci.models import EventPayload
from agentic_devtools.cli.ci.reconciliation.context_mapper import map_event_payload
from agentic_devtools.cli.ci.reconciliation.exceptions import UnmappableContextError


def test_map_event_payload_supports_matrix_and_marks_self_trigger() -> None:
    payload = EventPayload(pr_number=7, action="completed", sender_login="loop-bot")
    context = map_event_payload(payload, "workflow_run", self_identities=frozenset({"loop-bot"}))
    assert context.target_id == 7
    assert context.suppressed is True
    assert context.evidence_hints == ("workflow_run", "completed")


def test_map_event_payload_rejects_non_positive_pr_number() -> None:
    payload = EventPayload(pr_number=0, action="completed", sender_login="user")
    with pytest.raises(UnmappableContextError, match="event has no pull-request number"):
        map_event_payload(payload, "workflow_run")


def test_map_event_payload_unsuppressed_when_not_self_trigger() -> None:
    payload = EventPayload(pr_number=7, action="completed", sender_login="user")
    context = map_event_payload(payload, "workflow_run", self_identities=frozenset({"loop-bot"}))
    assert context.suppressed is False


def test_map_event_payload_rejects_unsupported_event_action() -> None:
    payload = EventPayload(pr_number=7, action="unsupported", sender_login="user")
    with pytest.raises(UnmappableContextError, match="unsupported event/action"):
        map_event_payload(payload, "workflow_run")
