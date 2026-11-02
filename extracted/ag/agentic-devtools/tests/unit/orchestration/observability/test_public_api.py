"""Tests for the observability public API re-export module."""

from agentic_devtools.orchestration.observability import (
    ErrorClassification,
    ErrorClassifier,
    EventWriter,
    LLMCallEvent,
    NodeExecutionEvent,
    ObservabilityEvent,
    Redactor,
    SummaryStats,
    ToolCallEvent,
    WorkflowRun,
    build_pricing_table,
    format_run_summary,
    format_summary_stats,
    lookup_call_cost,
    print_run_summary,
    record_llm_call,
    record_node_execution,
    record_tool_call,
    truncate_summary,
)


class TestObservabilityPublicAPI:
    """Verify all public symbols are importable from the facade module."""

    def test_all_exports_present(self) -> None:
        import agentic_devtools.orchestration.observability as obs

        assert len(obs.__all__) == 19

    def test_classes_are_importable(self) -> None:
        assert ErrorClassification is not None
        assert ErrorClassifier is not None
        assert EventWriter is not None
        assert LLMCallEvent is not None
        assert NodeExecutionEvent is not None
        assert ObservabilityEvent is not None
        assert Redactor is not None
        assert SummaryStats is not None
        assert ToolCallEvent is not None
        assert WorkflowRun is not None

    def test_functions_are_importable(self) -> None:
        assert callable(build_pricing_table)
        assert callable(format_run_summary)
        assert callable(format_summary_stats)
        assert callable(lookup_call_cost)
        assert callable(print_run_summary)
        assert callable(record_llm_call)
        assert callable(record_node_execution)
        assert callable(record_tool_call)
        assert callable(truncate_summary)
