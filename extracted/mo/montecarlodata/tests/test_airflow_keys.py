from unittest import TestCase
from unittest.mock import Mock, patch

import click.exceptions

from montecarlodata.common.user import UserService
from montecarlodata.config import Config
from montecarlodata.keys.airflow import AirflowService


class AirflowKeysTests(TestCase):
    config = Config(
        mcd_id="12345",
        mcd_token="67890",
        mcd_api_endpoint="https://api.getmontecarlo.com/graphql",
    )

    def setUp(self) -> None:
        self._user_service = Mock(autospec=UserService)
        self._service = AirflowService(
            config=self.config,
            command_name="test",
            user_service=self._user_service,
        )

    def test_get_resource_id(self):
        self._user_service.etl_containers = [
            {
                "name": "airflow_1",
                "uuid": "1234",
                "connections": [
                    {"type": "AIRFLOW"},
                ],
            },
        ]
        rid = self._service.get_airflow_resource_uuid()
        self.assertEqual("1234", rid)

    @patch("click.echo")
    def test_get_resource_id_no_etl_containers(self, mock_echo):
        self._user_service.etl_containers = []
        with self.assertRaises(click.exceptions.Abort):
            self._service.get_airflow_resource_uuid()
        mock_echo.assert_called_with("Error - No Airflow connection found", err=True)

    @patch("click.echo")
    def test_get_resource_id_no_airflow_containers(self, mock_echo):
        self._user_service.etl_containers = [
            {
                "name": "power_bi",
                "uuid": "1234",
                "connections": [
                    {"type": "POWER_BI"},
                ],
            },
        ]
        with self.assertRaises(click.exceptions.Abort):
            self._service.get_airflow_resource_uuid()
        mock_echo.assert_called_with("Error - No Airflow connection found", err=True)

    @patch("click.echo")
    def test_get_resource_multiple_etl_containers(self, mock_echo):
        self._user_service.etl_containers = [
            {
                "name": "airflow_1",
                "uuid": "1234",
                "connections": [
                    {"type": "AIRFLOW"},
                ],
            },
            {
                "name": "airflow_2",
                "uuid": "1235",
                "connections": [
                    {"type": "AIRFLOW"},
                ],
            },
        ]
        with self.assertRaises(click.exceptions.Abort):
            self._service.get_airflow_resource_uuid()
        mock_echo.assert_called_with(
            "Error - Multiple Airflow connections found, use --name to disambiguate",
            err=True,
        )

        rid = self._service.get_airflow_resource_uuid(name="airflow_1")
        self.assertEqual("1234", rid)

    @patch("click.echo")
    def test_get_resource_id_name_not_found(self, mock_echo):
        self._user_service.etl_containers = [
            {
                "name": "airflow_1",
                "uuid": "1234",
                "connections": [
                    {"type": "AIRFLOW"},
                ],
            },
        ]
        with self.assertRaises(click.exceptions.Abort):
            self._service.get_airflow_resource_uuid(name="invalid")
        mock_echo.assert_called_with(
            "Error - No Airflow connection found with name invalid", err=True
        )

    @patch("click.echo")
    def test_get_resource_id_multiple_same_name(self, mock_echo):
        self._user_service.etl_containers = [
            {
                "name": "airflow_1",
                "uuid": "1234",
                "connections": [
                    {"type": "AIRFLOW"},
                ],
            },
            {
                "name": "airflow_1",
                "uuid": "1234",
                "connections": [
                    {"type": "AIRFLOW"},
                ],
            },
        ]
        with self.assertRaises(click.exceptions.Abort):
            self._service.get_airflow_resource_uuid(name="airflow_1")
        mock_echo.assert_called_with(
            "Error - Multiple Airflow connections found with name airflow_1", err=True
        )
