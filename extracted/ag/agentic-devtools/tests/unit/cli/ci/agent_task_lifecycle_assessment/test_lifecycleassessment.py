from agentic_devtools.cli.ci.agent_task_lifecycle_assessment import LifecycleAssessment


def test_default_metadata_is_additive() -> None:
    result = LifecycleAssessment(False, False, None, "no-blocking-lifecycle")
    assert result.inventory_availability.value == "complete"
    assert result.failure_category is None
    assert result.http_status is None
    assert result.failure_source is None
