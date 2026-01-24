from unittest import TestCase
from unittest.mock import Mock, call, patch

import click
from box import Box
from pycarlo.core import Client

from montecarlodata.monitors.monitor_service import MonitorService


class MonitorServiceTest(TestCase):
    MONITORS_TABLE = """\
╒════════════════╤═══════════╤═════════════╤══════════════════╤══════════════════════════════════╕
│ Monitor UUID   │ Type      │ Namespace   │ Description      │ Last Update Time                 │
╞════════════════╪═══════════╪═════════════╪══════════════════╪══════════════════════════════════╡
│ test_1         │ FRESHNESS │ main        │ some description │ 2000-01-01 00:00:00.000000+00:00 │
├────────────────┼───────────┼─────────────┼──────────────────┼──────────────────────────────────┤
│ test_2         │ FRESHNESS │ main        │ some description │ 2000-01-01 00:00:00.000000+00:00 │
╘════════════════╧═══════════╧═════════════╧══════════════════╧══════════════════════════════════╛"""
    LIMIT = 2

    def setUp(self):
        self._client = Mock(autospec=Client)
        self._print_func = Mock(autospec=click.echo)
        self._service = MonitorService(
            client=self._client,
            command_name="test",
            print_func=self._print_func,
        )

    @staticmethod
    def _get_monitors_response(monitors_count):
        return Box(
            {
                "get_monitors": [
                    {
                        "uuid": f"test_{i}",
                        "monitor_type": "FRESHNESS",
                        "namespace": "main",
                        "description": "some description",
                        "last_update_time": "2000-01-01 00:00:00.000000+00:00",
                    }
                    for i in range(1, monitors_count + 1)
                ]
            }
        )

    def test_get_monitors(self):
        self._client.return_value = self._get_monitors_response(self.LIMIT)
        self._service.list_monitors(self.LIMIT)
        self._print_func.assert_called_once_with(self.MONITORS_TABLE)

    def test_get_monitors_with_more_available(self):
        self._client.return_value = self._get_monitors_response(self.LIMIT + 1)
        self._service.list_monitors(self.LIMIT)
        expected_calls = [
            call(self.MONITORS_TABLE),
            call(self._service.MORE_MONITOR_MESSAGE),
        ]
        self._print_func.assert_has_calls(expected_calls)

    @patch("montecarlodata.monitors.monitor_service.CircuitBreakerService")
    def test_run_circuit_breaker_with_namespace_and_name(self, mock_cb_service_class):
        mock_cb_service = Mock()
        mock_cb_service.trigger_and_poll.return_value = False
        mock_cb_service_class.return_value = mock_cb_service

        result = self._service.run_circuit_breaker(namespace="test_namespace", name="test_monitor")

        self.assertFalse(result)
        mock_cb_service_class.assert_called_once_with(
            print_func=self._print_func, mc_client=self._client
        )
        mock_cb_service.trigger_and_poll.assert_called_once_with(
            namespace="test_namespace", rule_name="test_monitor"
        )
        expected_calls = [
            call("Running circuit breaker..."),
            call("✓ Circuit breaker passed (no breach detected)"),
        ]
        self._print_func.assert_has_calls(expected_calls)

    @patch("montecarlodata.monitors.monitor_service.CircuitBreakerService")
    def test_run_circuit_breaker_with_uuid(self, mock_cb_service_class):
        mock_cb_service = Mock()
        mock_cb_service.trigger_and_poll.return_value = False
        mock_cb_service_class.return_value = mock_cb_service

        result = self._service.run_circuit_breaker(uuid="test-uuid-123")

        self.assertFalse(result)
        mock_cb_service.trigger_and_poll.assert_called_once_with(rule_uuid="test-uuid-123")

    @patch("montecarlodata.monitors.monitor_service.CircuitBreakerService")
    def test_run_circuit_breaker_breach(self, mock_cb_service_class):
        mock_cb_service = Mock()
        mock_cb_service.trigger_and_poll.return_value = True
        mock_cb_service_class.return_value = mock_cb_service

        result = self._service.run_circuit_breaker(namespace="test_namespace", name="test_monitor")

        self.assertTrue(result)
        expected_calls = [
            call("Running circuit breaker..."),
            call("✗ Circuit breaker breached"),
        ]
        self._print_func.assert_has_calls(expected_calls)

    @patch("montecarlodata.monitors.monitor_service.CircuitBreakerService")
    def test_run_circuit_breaker_with_runtime_variables(self, mock_cb_service_class):
        mock_cb_service = Mock()
        mock_cb_service.trigger_and_poll.return_value = False
        mock_cb_service_class.return_value = mock_cb_service

        runtime_vars_json = '{"var1": "value1", "var2": "value2"}'
        result = self._service.run_circuit_breaker(
            namespace="test_namespace",
            name="test_monitor",
            runtime_variables=runtime_vars_json,
        )

        self.assertFalse(result)
        mock_cb_service.trigger_and_poll.assert_called_once_with(
            namespace="test_namespace",
            rule_name="test_monitor",
            runtime_variables={"var1": "value1", "var2": "value2"},
        )

    def test_run_circuit_breaker_missing_required_params(self):
        with self.assertRaises(click.UsageError) as context:
            self._service.run_circuit_breaker()

        self.assertIn(
            "You must provide either --uuid or both --namespace and --name",
            str(context.exception),
        )

    def test_run_circuit_breaker_conflicting_params(self):
        with self.assertRaises(click.UsageError) as context:
            self._service.run_circuit_breaker(
                uuid="test-uuid", namespace="test_namespace", name="test_monitor"
            )

        self.assertIn(
            "Cannot use --uuid together with --namespace or --name",
            str(context.exception),
        )

    def test_run_circuit_breaker_invalid_json(self):
        with self.assertRaises(click.UsageError) as context:
            self._service.run_circuit_breaker(
                namespace="test_namespace",
                name="test_monitor",
                runtime_variables="invalid json",
            )

        self.assertIn("Invalid JSON for runtime variables", str(context.exception))
