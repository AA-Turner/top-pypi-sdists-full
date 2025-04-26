from unittest import TestCase
from unittest.mock import Mock, call

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
