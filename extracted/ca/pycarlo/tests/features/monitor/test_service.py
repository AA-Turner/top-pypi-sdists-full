from __future__ import annotations

from unittest import TestCase
from unittest.mock import Mock, patch

from box import Box

from pycarlo.features.monitor import (
    AgentMonitorConfig,
    MonitorExecutionStatus,
    MonitorService,
)
from pycarlo.features.monitor.queries import (
    GET_AGENT_MONITOR_MINIMAL,
    GET_MANUAL_MONITOR_EXECUTION_STATUS,
    RUN_MONITOR,
)


class MonitorServiceTests(TestCase):
    def setUp(self) -> None:
        self._mock_client = Mock()
        self._service = MonitorService(mc_client=self._mock_client, print_func=Mock())

    def test_run_monitor_basic(self) -> None:
        """Test basic run_monitor call."""
        self._mock_client.return_value = Box(
            {
                "run_monitor": {
                    "success": True,
                    "manual_monitor_execution_uuid": "exec-uuid-123",
                }
            }
        )

        result = self._service.run_monitor(monitor_uuid="monitor-uuid-456")

        self._mock_client.assert_called_once()
        call_kwargs = self._mock_client.call_args
        self.assertEqual(call_kwargs.kwargs["query"], RUN_MONITOR)
        self.assertEqual(call_kwargs.kwargs["variables"], {"monitorUuid": "monitor-uuid-456"})
        self._assert_telemetry_headers(call_kwargs.kwargs["additional_headers"])
        self.assertEqual(result, "exec-uuid-123")

    def test_run_monitor_with_runtime_variables(self) -> None:
        """Test run_monitor with runtime variables."""
        self._mock_client.return_value = Box(
            {
                "run_monitor": {
                    "success": True,
                    "manual_monitor_execution_uuid": "exec-uuid-123",
                }
            }
        )

        result = self._service.run_monitor(
            monitor_uuid="monitor-uuid-456",
            runtime_variables={"ci_build_id": "build-789", "env": "staging"},
        )

        call_kwargs = self._mock_client.call_args
        self.assertEqual(
            call_kwargs.kwargs["variables"],
            {
                "monitorUuid": "monitor-uuid-456",
                "runtimeVariables": [
                    {"name": "ci_build_id", "value": "build-789"},
                    {"name": "env", "value": "staging"},
                ],
            },
        )
        self.assertEqual(result, "exec-uuid-123")

    def test_run_monitor_failure(self) -> None:
        """Test run_monitor raises ValueError on failure."""
        self._mock_client.return_value = Box(
            {
                "run_monitor": {
                    "success": False,
                    "manual_monitor_execution_uuid": None,
                }
            }
        )

        with self.assertRaises(ValueError) as context:
            self._service.run_monitor(monitor_uuid="monitor-uuid-456")

        self.assertIn("Failed to run monitor", str(context.exception))

    def test_get_execution_status_in_progress(self) -> None:
        """Test get_execution_status for in-progress execution."""
        self._mock_client.return_value = Box(
            {
                "get_manual_monitor_execution_status": {
                    "status": "IN_PROGRESS",
                    "breached": None,
                    "completed": False,
                }
            }
        )

        result = self._service.get_execution_status("exec-uuid-123")

        call_kwargs = self._mock_client.call_args
        self.assertEqual(call_kwargs.kwargs["query"], GET_MANUAL_MONITOR_EXECUTION_STATUS)
        self.assertEqual(
            call_kwargs.kwargs["variables"],
            {"manualMonitorExecutionUuid": "exec-uuid-123"},
        )
        self.assertIsInstance(result, MonitorExecutionStatus)
        self.assertEqual(result.status, "IN_PROGRESS")
        self.assertIsNone(result.breached)
        self.assertFalse(result.completed)

    def test_get_execution_status_success_breached(self) -> None:
        """Test get_execution_status for completed breached execution."""
        self._mock_client.return_value = Box(
            {
                "get_manual_monitor_execution_status": {
                    "status": "SUCCESS",
                    "breached": True,
                    "completed": True,
                }
            }
        )

        result = self._service.get_execution_status("exec-uuid-123")

        self.assertEqual(result.status, "SUCCESS")
        self.assertTrue(result.breached)
        self.assertTrue(result.completed)

    def test_get_execution_status_success_not_breached(self) -> None:
        """Test get_execution_status for completed non-breached execution."""
        self._mock_client.return_value = Box(
            {
                "get_manual_monitor_execution_status": {
                    "status": "SUCCESS",
                    "breached": False,
                    "completed": True,
                }
            }
        )

        result = self._service.get_execution_status("exec-uuid-123")

        self.assertEqual(result.status, "SUCCESS")
        self.assertFalse(result.breached)
        self.assertTrue(result.completed)

    @patch("pycarlo.features.monitor.service.time.sleep")
    def test_run_and_poll_success_breached(self, mock_sleep: Mock) -> None:
        """Test run_and_poll completes and returns breached status."""
        self._mock_client.side_effect = [
            Box(
                {
                    "run_monitor": {
                        "success": True,
                        "manual_monitor_execution_uuid": "exec-uuid-123",
                    }
                }
            ),
            Box(
                {
                    "get_manual_monitor_execution_status": {
                        "status": "IN_PROGRESS",
                        "breached": None,
                        "completed": False,
                    }
                }
            ),
            Box(
                {
                    "get_manual_monitor_execution_status": {
                        "status": "SUCCESS",
                        "breached": True,
                        "completed": True,
                    }
                }
            ),
        ]

        result = self._service.run_and_poll(
            monitor_uuid="monitor-uuid-456",
            runtime_variables={"ci_build_id": "build-789"},
            poll_interval_seconds=1,
        )

        self.assertTrue(result)
        mock_sleep.assert_called_once_with(1)

    @patch("pycarlo.features.monitor.service.time.sleep")
    def test_run_and_poll_success_not_breached(self, mock_sleep: Mock) -> None:
        """Test run_and_poll completes and returns not breached status."""
        self._mock_client.side_effect = [
            Box(
                {
                    "run_monitor": {
                        "success": True,
                        "manual_monitor_execution_uuid": "exec-uuid-123",
                    }
                }
            ),
            Box(
                {
                    "get_manual_monitor_execution_status": {
                        "status": "SUCCESS",
                        "breached": False,
                        "completed": True,
                    }
                }
            ),
        ]

        result = self._service.run_and_poll(
            monitor_uuid="monitor-uuid-456",
            poll_interval_seconds=1,
        )

        self.assertFalse(result)
        mock_sleep.assert_not_called()

    @patch("pycarlo.features.monitor.service.time.time")
    def test_run_and_poll_timeout(self, mock_time: Mock) -> None:
        """Test run_and_poll raises TimeoutError on timeout."""
        mock_time.side_effect = [0, 0, 700]  # Start, check, timeout exceeded

        self._mock_client.side_effect = [
            Box(
                {
                    "run_monitor": {
                        "success": True,
                        "manual_monitor_execution_uuid": "exec-uuid-123",
                    }
                }
            ),
            Box(
                {
                    "get_manual_monitor_execution_status": {
                        "status": "IN_PROGRESS",
                        "breached": None,
                        "completed": False,
                    }
                }
            ),
        ]

        with self.assertRaises(TimeoutError) as context:
            self._service.run_and_poll(
                monitor_uuid="monitor-uuid-456",
                timeout_in_minutes=10,
            )

        self.assertIn("timed out", str(context.exception))

    def test_get_agent_monitor_config_success(self) -> None:
        """Test get_agent_monitor_config returns AgentMonitorConfig with agent span filters."""
        self._mock_client.return_value = Box(
            {
                "get_monitors": [
                    {
                        "uuid": "monitor-uuid-123",
                        "name": "Test Monitor",
                        "description": "Test Description",
                        "monitor_type": "AGENT",
                        "entity_mcons": ["MCON++account++warehouse++table++schema.table"],
                        "agent_span_filters": [
                            {
                                "agent": {"value": "my-agent"},
                                "workflow": {"value": "my-workflow"},
                                "task": {"value": "my-task"},
                                "span_name": {"value": "my-span"},
                            }
                        ],
                        "filters": {
                            "type": "GROUP",
                            "operator": "AND",
                            "conditions": [
                                {
                                    "type": "BINARY",
                                    "predicate": {"name": "equal", "negated": False},
                                    "left": [{"type": "MAP_KEY", "key": "ci_build_id"}],
                                    "right": [{"type": "LITERAL", "literal": "{{ci_build_id}}"}],
                                }
                            ],
                        },
                    }
                ]
            }
        )

        result = self._service.get_agent_monitor_config("monitor-uuid-123")

        self._mock_client.assert_called_once()
        call_kwargs = self._mock_client.call_args
        self.assertEqual(call_kwargs.kwargs["query"], GET_AGENT_MONITOR_MINIMAL)
        self.assertEqual(call_kwargs.kwargs["variables"], {"uuids": ["monitor-uuid-123"]})

        self.assertIsInstance(result, AgentMonitorConfig)
        self.assertEqual(result.uuid, "monitor-uuid-123")
        self.assertEqual(result.name, "Test Monitor")
        self.assertEqual(result.description, "Test Description")
        self.assertEqual(result.monitor_type, "AGENT")
        self.assertEqual(result.mcon, "MCON++account++warehouse++table++schema.table")
        self.assertEqual(len(result.agent_span_filters), 1)
        self.assertEqual(result.agent_span_filters[0].agent, "my-agent")
        self.assertEqual(result.agent_span_filters[0].workflow, "my-workflow")
        self.assertEqual(result.agent_span_filters[0].task, "my-task")
        self.assertEqual(result.agent_span_filters[0].span_name, "my-span")
        self.assertEqual(result.runtime_variable_names, ["ci_build_id"])
        self.assertEqual(result.attribute_key, "ci_build_id")

    def test_get_agent_monitor_config_not_found(self) -> None:
        """Test get_agent_monitor_config raises ValueError when monitor not found."""
        self._mock_client.return_value = Box({"get_monitors": []})

        with self.assertRaises(ValueError) as context:
            self._service.get_agent_monitor_config("nonexistent-uuid")

        self.assertIn("Monitor not found", str(context.exception))

    def _assert_telemetry_headers(self, headers: dict[str, str]) -> None:
        self.assertEqual(headers["x-mcd-telemetry-reason"], "service")
        self.assertEqual(headers["x-mcd-telemetry-service"], "monitor_service")
