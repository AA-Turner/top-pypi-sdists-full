from agentic_devtools.cli.ci.reconciliation.context_mapper import coalesce_event_contexts
from agentic_devtools.cli.ci.reconciliation.models import RunEventContext


def test_coalesce_event_contexts_keeps_first_duplicate() -> None:
    first = RunEventContext("pull_request", 1, repository_full_name="o/r", event_type="pull_request", action="opened")
    duplicate = RunEventContext(
        "pull_request", 1, repository_full_name="o/r", event_type="pull_request", action="opened"
    )
    assert coalesce_event_contexts([first, duplicate]) == [first]
