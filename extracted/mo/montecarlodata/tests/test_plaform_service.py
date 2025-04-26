import uuid
from unittest import TestCase
from unittest.mock import ANY, Mock, call, patch

import click
from box import Box
from pycarlo.core import Client

from montecarlodata.platform.service import PlatformService
from montecarlodata.queries.platform import (
    MUTATION_TRIGGER_CAAS_MIGRATION_TEST,
    QUERY_CAAS_MIGRATION_TEST_STATUS,
    QUERY_GET_SERVICES,
)

_DC_CLOUD_V2 = Box(uuid=str(uuid.uuid4()), deployment_type="CLOUD_V2", active=True, agents=[])
_DC_WITH_AGENT = Box(
    uuid=str(uuid.uuid4()),
    deployment_type="REMOTE_V1_5",
    active=True,
    agents=[
        Box(
            is_deleted=True,
            endpoint="deleted_agent_endpoint",
        ),
        Box(
            is_deleted=False,
            endpoint="agent_endpoint",
        ),
    ],
)


class PlatformServiceTest(TestCase):
    def setUp(self) -> None:
        self._mc_client_mock = Mock(autospec=Client)
        self._service = PlatformService(mc_client=self._mc_client_mock, command_name="test")

    @patch("montecarlodata.platform.service.tabulate")
    def test_platform_list(self, tabulate_mock):
        self._mc_client_mock.return_value = Box(
            get_user=Box(account=Box(data_collectors=[_DC_CLOUD_V2, _DC_WITH_AGENT]))
        )
        self._service.list_services()
        self._mc_client_mock.assert_called_once()
        tabulate_mock.assert_called_once_with(
            [
                [str(_DC_CLOUD_V2.uuid), "CLOUD_V2", "N/A"],
                [str(_DC_WITH_AGENT.uuid), "REMOTE_V1_5", "agent_endpoint"],
            ],
            headers=["Service ID", "Deployment Type", "Endpoint"],
            tablefmt="fancy_grid",
        )

    @patch("montecarlodata.platform.service.click.echo")
    def test_trigger_migration_test_not_needed(self, mock_click_echo):
        self._mc_client_mock.return_value = Box(
            get_user=Box(
                account=Box(
                    data_collectors=[_DC_CLOUD_V2],
                ),
            ),
        )
        with self.assertRaises(click.Abort):
            self._service.caas_migration_test(None)
        mock_click_echo.assert_called_once_with("No need to migrate CLOUD_V2 services.")

    @patch("montecarlodata.platform.service.click.echo")
    def test_trigger_migration_test_dc_id_required(self, mock_click_echo):
        self._mc_client_mock.return_value = Box(
            get_user=Box(
                account=Box(
                    data_collectors=[_DC_CLOUD_V2, _DC_WITH_AGENT],
                ),
            ),
        )
        with self.assertRaises(click.Abort):
            self._service.caas_migration_test(None)
        mock_click_echo.assert_called_once_with(
            "There are multiple active services, please specify one using --service-id."
        )

    @patch("montecarlodata.platform.service.click.echo")
    def test_trigger_migration_test_no_dcs(self, mock_click_echo):
        self._mc_client_mock.return_value = Box(
            get_user=Box(
                account=Box(
                    data_collectors=[],
                ),
            ),
        )
        with self.assertRaises(click.Abort):
            self._service.caas_migration_test(None)
        mock_click_echo.assert_called_once_with("There are no active services in this account.")

    @patch("montecarlodata.platform.service.click.echo")
    def test_trigger_migration_test_wrong_dc_ids(self, mock_click_echo):
        self._mc_client_mock.return_value = Box(
            get_user=Box(
                account=Box(
                    data_collectors=[_DC_CLOUD_V2],
                ),
            ),
        )
        with self.assertRaises(click.Abort):
            self._service.caas_migration_test(uuid.uuid4())
        mock_click_echo.assert_called_once_with(
            "No active service found with the specified ID, use "
            "`montecarlo platform list` to list the active services."
        )

    @patch("montecarlodata.platform.service.time.sleep")
    @patch("montecarlodata.platform.service.tabulate")
    def test_trigger_migration_multiple_dcs(self, mock_tabulate, mock_sleep):
        migration_uuid = str(uuid.uuid4())
        self._mc_client_mock.side_effect = [
            Box(
                get_user=Box(
                    account=Box(
                        data_collectors=[_DC_CLOUD_V2, _DC_WITH_AGENT],
                    ),
                ),
            ),
            Box(
                trigger_platform_migration_test=Box(
                    migration_uuid=migration_uuid,
                )
            ),
            Box(
                get_platform_migration_status=Box(
                    output=Box(
                        status="dry_run_completed",
                        success=True,
                        error_message=None,
                        tested_connections=[
                            Box(
                                name="connection_name",
                                uuid="connection_uuid",
                                connection_type="snowflake",
                                success=True,
                                error_message=None,
                            )
                        ],
                        tested_agent=None,
                    ),
                ),
            ),
        ]
        self._service.caas_migration_test(_DC_WITH_AGENT.uuid)
        mock_tabulate.assert_called_once_with(
            [
                [
                    "connection_name",
                    "connection_uuid",
                    "snowflake",
                    "Success",
                    "None",
                    "",
                ]
            ],
            headers=[
                "Name",
                "Connection UUID",
                "Connection Type",
                "Result",
                "Required Action",
                "Error Message",
            ],
            tablefmt="fancy_grid",
            maxcolwidths=ANY,
        )

    @patch("montecarlodata.platform.service.time.sleep")
    @patch("montecarlodata.platform.service.tabulate")
    def test_trigger_migration_single_dc(self, mock_tabulate, mock_sleep):
        migration_uuid = str(uuid.uuid4())
        self._mc_client_mock.side_effect = [
            Box(
                get_user=Box(
                    account=Box(
                        data_collectors=[_DC_WITH_AGENT],
                    ),
                ),
            ),
            Box(
                trigger_platform_migration_test=Box(
                    migration_uuid=migration_uuid,
                )
            ),
            Box(
                get_platform_migration_status=Box(
                    output=Box(
                        status="dry_run_completed",
                        success=True,
                        error_message=None,
                        tested_connections=[
                            Box(
                                name="connection_name",
                                uuid="connection_uuid",
                                connection_type="snowflake",
                                success=True,
                                error_message=None,
                            )
                        ],
                        tested_agent=None,
                    ),
                ),
            ),
        ]
        self._service.caas_migration_test(None)
        self._mc_client_mock.assert_has_calls(
            [
                call(
                    QUERY_GET_SERVICES,
                    additional_headers={
                        "x-mcd-telemetry-reason": "cli",
                        "x-mcd-telemetry-service": "platform_service",
                        "x-mcd-telemetry-command": "test",
                    },
                ),
                call(
                    MUTATION_TRIGGER_CAAS_MIGRATION_TEST,
                    variables={
                        "dcUuid": str(_DC_WITH_AGENT.uuid),
                    },
                    additional_headers={
                        "x-mcd-telemetry-reason": "cli",
                        "x-mcd-telemetry-service": "platform_service",
                        "x-mcd-telemetry-command": "test",
                    },
                ),
                call(
                    QUERY_CAAS_MIGRATION_TEST_STATUS,
                    variables={
                        "dcUuid": str(_DC_WITH_AGENT.uuid),
                        "migrationUuid": migration_uuid,
                    },
                    additional_headers={
                        "x-mcd-telemetry-reason": "cli",
                        "x-mcd-telemetry-service": "platform_service",
                        "x-mcd-telemetry-command": "test",
                    },
                ),
            ]
        )
        mock_tabulate.assert_called_once_with(
            [
                [
                    "connection_name",
                    "connection_uuid",
                    "snowflake",
                    "Success",
                    "None",
                    "",
                ]
            ],
            headers=[
                "Name",
                "Connection UUID",
                "Connection Type",
                "Result",
                "Required Action",
                "Error Message",
            ],
            tablefmt="fancy_grid",
            maxcolwidths=ANY,
        )
