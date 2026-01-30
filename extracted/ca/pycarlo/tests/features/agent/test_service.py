from __future__ import annotations

from datetime import datetime, timezone
from unittest import TestCase
from unittest.mock import Mock

from box import Box

from pycarlo.features.agent import (
    AgentService,
    AgentSpanFilter,
    SpanAttributeFilter,
    SpanQueryResult,
)
from pycarlo.features.agent.queries import GET_AGENT_SPAN_SAMPLE_V2


class AgentServiceTests(TestCase):
    def setUp(self) -> None:
        self._mock_client = Mock()
        self._service = AgentService(mc_client=self._mock_client)

    def test_get_agent_spans_basic(self) -> None:
        """Test basic get_agent_spans call with only mcon."""
        self._mock_client.return_value = Box(
            {
                "get_agent_span_sample_v2": {
                    "columns": ["span_id", "trace_id", "name"],
                    "rows": [["span-1", "trace-1", "test-span"]],
                    "has_error": False,
                    "error": None,
                }
            }
        )

        result = self._service.get_agent_spans(mcon="MCON++test++table")

        self._mock_client.assert_called_once()
        call_kwargs = self._mock_client.call_args
        self.assertEqual(call_kwargs.kwargs["query"], GET_AGENT_SPAN_SAMPLE_V2)
        self.assertEqual(call_kwargs.kwargs["variables"], {"mcon": "MCON++test++table"})
        self._assert_telemetry_headers(call_kwargs.kwargs["additional_headers"])

        self.assertIsInstance(result, SpanQueryResult)
        self.assertEqual(result.columns, ["span_id", "trace_id", "name"])
        self.assertEqual(result.rows, [["span-1", "trace-1", "test-span"]])
        self.assertFalse(result.has_error)
        self.assertIsNone(result.error)
        self.assertEqual(result.row_count, 1)

    def test_get_agent_spans_with_span_ids(self) -> None:
        """Test get_agent_spans with span_ids filter."""
        self._mock_client.return_value = Box(
            {
                "get_agent_span_sample_v2": {
                    "columns": ["span_id"],
                    "rows": [["span-1"], ["span-2"]],
                    "has_error": False,
                    "error": None,
                }
            }
        )

        result = self._service.get_agent_spans(
            mcon="MCON++test++table",
            span_ids=["span-1", "span-2"],
        )

        call_kwargs = self._mock_client.call_args
        self.assertEqual(
            call_kwargs.kwargs["variables"],
            {"mcon": "MCON++test++table", "spanIds": ["span-1", "span-2"]},
        )
        self.assertEqual(result.row_count, 2)

    def test_get_agent_spans_with_trace_ids(self) -> None:
        """Test get_agent_spans with trace_ids filter."""
        self._mock_client.return_value = Box(
            {
                "get_agent_span_sample_v2": {
                    "columns": ["trace_id"],
                    "rows": [["trace-1"]],
                    "has_error": False,
                    "error": None,
                }
            }
        )

        result = self._service.get_agent_spans(
            mcon="MCON++test++table",
            trace_ids=["trace-1", "trace-2"],
        )

        call_kwargs = self._mock_client.call_args
        self.assertEqual(
            call_kwargs.kwargs["variables"],
            {"mcon": "MCON++test++table", "traceIds": ["trace-1", "trace-2"]},
        )
        self.assertEqual(result.row_count, 1)

    def test_get_agent_spans_with_time_range(self) -> None:
        """Test get_agent_spans with time range filtering."""
        self._mock_client.return_value = Box(
            {
                "get_agent_span_sample_v2": {
                    "columns": [],
                    "rows": [],
                    "has_error": False,
                    "error": None,
                }
            }
        )

        start_time = datetime(2026, 1, 22, 10, 0, 0, tzinfo=timezone.utc)
        end_time = datetime(2026, 1, 22, 12, 0, 0, tzinfo=timezone.utc)

        self._service.get_agent_spans(
            mcon="MCON++test++table",
            ingestion_start_time=start_time,
            ingestion_end_time=end_time,
        )

        call_kwargs = self._mock_client.call_args
        self.assertEqual(
            call_kwargs.kwargs["variables"],
            {
                "mcon": "MCON++test++table",
                "ingestionStartTime": start_time.isoformat(),
                "ingestionEndTime": end_time.isoformat(),
            },
        )

    def test_get_agent_spans_with_limit_and_offset(self) -> None:
        """Test get_agent_spans with limit and offset."""
        self._mock_client.return_value = Box(
            {
                "get_agent_span_sample_v2": {
                    "columns": [],
                    "rows": [],
                    "has_error": False,
                    "error": None,
                }
            }
        )

        self._service.get_agent_spans(
            mcon="MCON++test++table",
            limit=100,
            offset=50,
        )

        call_kwargs = self._mock_client.call_args
        self.assertEqual(
            call_kwargs.kwargs["variables"],
            {"mcon": "MCON++test++table", "limit": 100, "offset": 50},
        )

    def test_get_agent_spans_with_error(self) -> None:
        """Test get_agent_spans when API returns an error."""
        self._mock_client.return_value = Box(
            {
                "get_agent_span_sample_v2": {
                    "columns": [],
                    "rows": [],
                    "has_error": True,
                    "error": "Query execution failed",
                }
            }
        )

        result = self._service.get_agent_spans(mcon="MCON++test++table")

        self.assertTrue(result.has_error)
        self.assertEqual(result.error, "Query execution failed")
        self.assertEqual(result.row_count, 0)

    def test_get_agent_spans_with_agent_span_filters(self) -> None:
        """Test get_agent_spans with agent_span_filters."""
        self._mock_client.return_value = Box(
            {
                "get_agent_span_sample_v2": {
                    "columns": ["agent", "workflow", "task", "span_name"],
                    "rows": [["my-agent", "my-workflow", "my-task", "my-span"]],
                    "has_error": False,
                    "error": None,
                }
            }
        )

        filters = [
            AgentSpanFilter(
                agent="mc-internal-sentry-root-cause-agent",
                workflow="Sentry Root Cause Agent",
                task="analyze_and_summarize",
                span_name="ChatBedrockConverse.chat",
            )
        ]

        result = self._service.get_agent_spans(
            mcon="MCON++test++table",
            agent_span_filters=filters,
        )

        call_kwargs = self._mock_client.call_args
        self.assertEqual(
            call_kwargs.kwargs["variables"],
            {
                "mcon": "MCON++test++table",
                "agentSpanFilters": [
                    {
                        "agent": {"value": "mc-internal-sentry-root-cause-agent"},
                        "workflow": {"value": "Sentry Root Cause Agent"},
                        "task": {"value": "analyze_and_summarize"},
                        "spanName": {"value": "ChatBedrockConverse.chat"},
                    }
                ],
            },
        )
        self.assertEqual(result.row_count, 1)

    def test_get_agent_spans_with_partial_agent_span_filter(self) -> None:
        """Test get_agent_spans with partial agent_span_filter (only some fields)."""
        self._mock_client.return_value = Box(
            {
                "get_agent_span_sample_v2": {
                    "columns": [],
                    "rows": [],
                    "has_error": False,
                    "error": None,
                }
            }
        )

        filters = [AgentSpanFilter(agent="my-agent")]

        self._service.get_agent_spans(
            mcon="MCON++test++table",
            agent_span_filters=filters,
        )

        call_kwargs = self._mock_client.call_args
        self.assertEqual(
            call_kwargs.kwargs["variables"],
            {
                "mcon": "MCON++test++table",
                "agentSpanFilters": [{"agent": {"value": "my-agent"}}],
            },
        )

    def test_get_agent_spans_with_attribute_filters(self) -> None:
        """Test get_agent_spans with attribute_filters."""
        self._mock_client.return_value = Box(
            {
                "get_agent_span_sample_v2": {
                    "columns": ["span_id", "attr_map"],
                    "rows": [["span-1", {"montecarlo.ci_build_id": "build-123"}]],
                    "has_error": False,
                    "error": None,
                }
            }
        )

        filters = [
            SpanAttributeFilter(key="montecarlo.ci_build_id", value="build-123"),
            SpanAttributeFilter(key="environment", value="production"),
        ]

        result = self._service.get_agent_spans(
            mcon="MCON++test++table",
            attribute_filters=filters,
        )

        call_kwargs = self._mock_client.call_args
        self.assertEqual(
            call_kwargs.kwargs["variables"],
            {
                "mcon": "MCON++test++table",
                "attributeFilters": [
                    {"key": "montecarlo.ci_build_id", "value": "build-123"},
                    {"key": "environment", "value": "production"},
                ],
            },
        )
        self.assertEqual(result.row_count, 1)

    def test_get_agent_spans_with_all_filters(self) -> None:
        """Test get_agent_spans with both agent_span_filters and attribute_filters."""
        self._mock_client.return_value = Box(
            {
                "get_agent_span_sample_v2": {
                    "columns": [],
                    "rows": [],
                    "has_error": False,
                    "error": None,
                }
            }
        )

        self._service.get_agent_spans(
            mcon="MCON++test++table",
            agent_span_filters=[AgentSpanFilter(agent="my-agent")],
            attribute_filters=[SpanAttributeFilter(key="env", value="prod")],
        )

        call_kwargs = self._mock_client.call_args
        self.assertEqual(
            call_kwargs.kwargs["variables"],
            {
                "mcon": "MCON++test++table",
                "agentSpanFilters": [{"agent": {"value": "my-agent"}}],
                "attributeFilters": [{"key": "env", "value": "prod"}],
            },
        )

    def _assert_telemetry_headers(self, headers: dict[str, str]) -> None:
        self.assertEqual(headers["x-mcd-telemetry-reason"], "service")
        self.assertEqual(headers["x-mcd-telemetry-service"], "agent_service")
