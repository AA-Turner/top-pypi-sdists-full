import temporalio.workflow
from temporalio.common import SearchAttributeKey

# Temporal native schedule id search attribute
TEMPORAL_SCHEDULE_ID_SEARCH_KEY = SearchAttributeKey.for_keyword("TemporalScheduledById")


def require_activity_context_value(value: str | None, *, field_name: str) -> str:
    if value is None:
        raise RuntimeError(f"Temporal activity info is missing {field_name}")
    return value


def current_run_id() -> str | None:
    if not temporalio.workflow.in_workflow():
        return None
    return temporalio.workflow.info().run_id


def is_current_run(run_id: str | None) -> bool:
    return current_run_id() == run_id
