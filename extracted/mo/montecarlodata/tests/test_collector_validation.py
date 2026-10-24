import uuid
from unittest import TestCase
from unittest.mock import Mock, patch

from box import Box
from click.testing import CliRunner
from pycarlo.core import Client, Session

from montecarlodata.collector.commands import run_validations
from montecarlodata.collector.validation import CollectorValidationService
from montecarlodata.common.user import UserService
from tests.test_common_user import _SAMPLE_CONFIG

_DC_UUID = "fb045f19-51c5-4b7b-926b-1defcce05180"
_ACTIVE_WAREHOUSE = {
    "uuid": str(uuid.uuid4()),
    "name": "active-warehouse",
    "connectionType": "snowflake",
    "isDeleted": False,
    "connections": [
        {
            "uuid": str(uuid.uuid4()),
            "type": "snowflake",
            "createdOn": None,
            "jobTypes": [],
            "isActive": True,
        }
    ],
    "dataCollector": {"uuid": _DC_UUID, "customerAwsRegion": "us-east-1"},
}
_DELETED_WAREHOUSE = {
    "uuid": str(uuid.uuid4()),
    "name": "deleted-warehouse",
    "connectionType": "snowflake",
    "isDeleted": True,
    "connections": [
        {"uuid": str(uuid.uuid4()), "type": "snowflake", "createdOn": None, "jobTypes": []}
    ],
    "dataCollector": {"uuid": _DC_UUID, "customerAwsRegion": "us-east-1"},
}
_WAREHOUSE_SNAKE_CASE_DELETED = {
    "uuid": str(uuid.uuid4()),
    "name": "snake-deleted-warehouse",
    "connectionType": "snowflake",
    "is_deleted": True,
    "connections": [
        {"uuid": str(uuid.uuid4()), "type": "snowflake", "createdOn": None, "jobTypes": []}
    ],
    "dataCollector": {"uuid": _DC_UUID, "customerAwsRegion": "us-east-1"},
}


class CollectorValidationServiceTest(TestCase):
    def setUp(self) -> None:
        self._user_service_mock = Mock(autospec=UserService)
        self._mc_client = Client(
            session=Session(
                endpoint=_SAMPLE_CONFIG.mcd_api_endpoint,
                mcd_id=_SAMPLE_CONFIG.mcd_id,
                mcd_token=_SAMPLE_CONFIG.mcd_token,
            )
        )
        self._user_service_mock.get_collector.return_value = Box({"uuid": _DC_UUID})

        self._service = CollectorValidationService(
            config=_SAMPLE_CONFIG,
            mc_client=self._mc_client,
            command_name="test",
            user_service=self._user_service_mock,
        )

    @patch.object(CollectorValidationService, "_run_storage_access_validation", return_value=0)
    @patch.object(
        CollectorValidationService,
        "_run_validations_for_integration",
        return_value=(0, []),
    )
    def test_run_validations_excludes_deleted_warehouses(
        self, mock_run_integration: Mock, mock_storage: Mock
    ) -> None:
        """Deleted warehouses (isDeleted=True) are excluded from validations."""
        self._user_service_mock.warehouses = [_ACTIVE_WAREHOUSE, _DELETED_WAREHOUSE]
        self._user_service_mock.bi_containers = []
        self._user_service_mock.etl_containers = []

        self._service.run_validations(dc_id=_DC_UUID)

        mock_run_integration.assert_called_once()
        called_integration = mock_run_integration.call_args[0][1]
        self.assertEqual(called_integration["name"], "active-warehouse")

    @patch.object(CollectorValidationService, "_run_storage_access_validation", return_value=0)
    @patch.object(
        CollectorValidationService,
        "_run_validations_for_integration",
        return_value=(0, []),
    )
    def test_run_validations_excludes_snake_case_deleted(
        self, mock_run_integration: Mock, mock_storage: Mock
    ) -> None:
        """Warehouses with is_deleted=True (snake_case) are excluded."""
        self._user_service_mock.warehouses = [
            _ACTIVE_WAREHOUSE,
            _WAREHOUSE_SNAKE_CASE_DELETED,
        ]
        self._user_service_mock.bi_containers = []
        self._user_service_mock.etl_containers = []

        self._service.run_validations(dc_id=_DC_UUID)

        mock_run_integration.assert_called_once()
        called_integration = mock_run_integration.call_args[0][1]
        self.assertEqual(called_integration["name"], "active-warehouse")

    @patch.object(CollectorValidationService, "_run_storage_access_validation", return_value=0)
    @patch.object(
        CollectorValidationService,
        "_run_validations_for_integration",
        return_value=(0, []),
    )
    def test_run_validations_includes_active_integrations(
        self, mock_run_integration: Mock, mock_storage: Mock
    ) -> None:
        """Active warehouses, BI containers, and ETL containers with active connections are
        included."""
        active_bi = {
            "uuid": str(uuid.uuid4()),
            "name": "active-bi",
            "isDeleted": False,
            "connections": [
                {
                    "uuid": str(uuid.uuid4()),
                    "type": "looker",
                    "createdOn": None,
                    "jobTypes": [],
                    "isActive": True,
                }
            ],
            "dataCollector": {"uuid": _DC_UUID, "customerAwsRegion": "us-east-1"},
        }
        active_etl = {
            "uuid": str(uuid.uuid4()),
            "name": "active-etl",
            "isDeleted": False,
            "connections": [
                {
                    "uuid": str(uuid.uuid4()),
                    "type": "airflow",
                    "createdOn": None,
                    "jobTypes": [],
                    "isActive": True,
                }
            ],
            "dataCollector": {"uuid": _DC_UUID, "customerAwsRegion": "us-east-1"},
        }
        self._user_service_mock.warehouses = [_ACTIVE_WAREHOUSE]
        self._user_service_mock.bi_containers = [active_bi]
        self._user_service_mock.etl_containers = [active_etl]

        self._service.run_validations(dc_id=_DC_UUID)

        self.assertEqual(mock_run_integration.call_count, 3)
        called_names = [
            mock_run_integration.call_args_list[i][0][1]["name"]
            for i in range(mock_run_integration.call_count)
        ]
        self.assertIn("active-warehouse", called_names)
        self.assertIn("active-bi", called_names)
        self.assertIn("active-etl", called_names)

    @patch.object(CollectorValidationService, "_run_storage_access_validation", return_value=0)
    @patch.object(
        CollectorValidationService,
        "_run_validations_for_integration",
        return_value=(0, []),
    )
    def test_run_validations_excludes_inactive_warehouse_connections(
        self, mock_run_integration: Mock, mock_storage: Mock
    ) -> None:
        """Warehouse connections with isActive=False are excluded from validations."""
        warehouse_with_mixed_connections = {
            **_ACTIVE_WAREHOUSE,
            "connections": [
                {
                    "uuid": str(uuid.uuid4()),
                    "type": "snowflake",
                    "createdOn": None,
                    "jobTypes": [],
                    "isActive": True,
                },
                {
                    "uuid": str(uuid.uuid4()),
                    "type": "snowflake",
                    "createdOn": None,
                    "jobTypes": [],
                    "isActive": False,
                },
            ],
        }
        self._user_service_mock.warehouses = [warehouse_with_mixed_connections]
        self._user_service_mock.bi_containers = []
        self._user_service_mock.etl_containers = []

        self._service.run_validations(dc_id=_DC_UUID)

        mock_run_integration.assert_called_once()
        called_integration = mock_run_integration.call_args[0][1]
        self.assertEqual(len(called_integration["connections"]), 1)
        self.assertTrue(called_integration["connections"][0].get("isActive"))

    @patch.object(CollectorValidationService, "_run_storage_access_validation", return_value=0)
    @patch.object(
        CollectorValidationService,
        "_run_validations_for_integration",
        return_value=(0, []),
    )
    def test_run_validations_excludes_inactive_bi_connections(
        self, mock_run_integration: Mock, mock_storage: Mock
    ) -> None:
        """BI container connections with isActive=False are excluded from validations."""
        bi_with_mixed_connections = {
            "uuid": str(uuid.uuid4()),
            "name": "test-bi",
            "isDeleted": False,
            "connections": [
                {
                    "uuid": str(uuid.uuid4()),
                    "type": "looker",
                    "createdOn": None,
                    "jobTypes": [],
                    "isActive": True,
                },
                {
                    "uuid": str(uuid.uuid4()),
                    "type": "looker",
                    "createdOn": None,
                    "jobTypes": [],
                    "isActive": False,
                },
            ],
            "dataCollector": {"uuid": _DC_UUID, "customerAwsRegion": "us-east-1"},
        }
        self._user_service_mock.warehouses = []
        self._user_service_mock.bi_containers = [bi_with_mixed_connections]
        self._user_service_mock.etl_containers = []

        self._service.run_validations(dc_id=_DC_UUID)

        mock_run_integration.assert_called_once()
        called_integration = mock_run_integration.call_args[0][1]
        self.assertEqual(called_integration["name"], "test-bi")
        self.assertEqual(len(called_integration["connections"]), 1)
        self.assertTrue(called_integration["connections"][0].get("isActive"))

    @patch.object(CollectorValidationService, "_run_storage_access_validation", return_value=0)
    @patch.object(
        CollectorValidationService,
        "_run_validations_for_integration",
        return_value=(0, []),
    )
    def test_run_validations_excludes_inactive_etl_connections(
        self, mock_run_integration: Mock, mock_storage: Mock
    ) -> None:
        """ETL container connections with isActive=False are excluded from validations."""
        etl_with_mixed_connections = {
            "uuid": str(uuid.uuid4()),
            "name": "test-etl",
            "isDeleted": False,
            "connections": [
                {
                    "uuid": str(uuid.uuid4()),
                    "type": "airflow",
                    "createdOn": None,
                    "jobTypes": [],
                    "isActive": True,
                },
                {
                    "uuid": str(uuid.uuid4()),
                    "type": "airflow",
                    "createdOn": None,
                    "jobTypes": [],
                    "isActive": False,
                },
            ],
            "dataCollector": {"uuid": _DC_UUID, "customerAwsRegion": "us-east-1"},
        }
        self._user_service_mock.warehouses = []
        self._user_service_mock.bi_containers = []
        self._user_service_mock.etl_containers = [etl_with_mixed_connections]

        self._service.run_validations(dc_id=_DC_UUID)

        mock_run_integration.assert_called_once()
        called_integration = mock_run_integration.call_args[0][1]
        self.assertEqual(called_integration["name"], "test-etl")
        self.assertEqual(len(called_integration["connections"]), 1)
        self.assertTrue(called_integration["connections"][0].get("isActive"))

    @patch.object(CollectorValidationService, "_run_storage_access_validation", return_value=0)
    @patch.object(
        CollectorValidationService,
        "_run_validations_for_integration",
        return_value=(0, []),
    )
    def test_run_validations_excludes_connections_with_disabled_on(
        self, mock_run_integration: Mock, mock_storage: Mock
    ) -> None:
        """Connections with disabledOn set are excluded even if isActive=True. Monolith
        treats a connection as active only when is_active=True AND disabled_on IS NULL."""
        warehouse_with_disabled_on_connection = {
            **_ACTIVE_WAREHOUSE,
            "connections": [
                {
                    "uuid": str(uuid.uuid4()),
                    "type": "snowflake",
                    "createdOn": None,
                    "jobTypes": [],
                    "isActive": True,
                    "disabledOn": None,
                },
                {
                    "uuid": str(uuid.uuid4()),
                    "type": "snowflake",
                    "createdOn": None,
                    "jobTypes": [],
                    "isActive": True,
                    "disabledOn": "2026-05-01T00:00:00+00:00",
                },
                {
                    "uuid": str(uuid.uuid4()),
                    "type": "snowflake",
                    "createdOn": None,
                    "jobTypes": [],
                    "is_active": True,
                    "disabled_on": "2026-05-01T00:00:00+00:00",
                },
            ],
        }
        self._user_service_mock.warehouses = [warehouse_with_disabled_on_connection]
        self._user_service_mock.bi_containers = []
        self._user_service_mock.etl_containers = []

        self._service.run_validations(dc_id=_DC_UUID)

        mock_run_integration.assert_called_once()
        called_integration = mock_run_integration.call_args[0][1]
        self.assertEqual(len(called_integration["connections"]), 1)
        self.assertIsNone(called_integration["connections"][0].get("disabledOn"))

    @patch.object(CollectorValidationService, "_run_storage_access_validation", return_value=0)
    @patch.object(
        CollectorValidationService,
        "_run_validations_for_integration",
        return_value=(0, []),
    )
    def test_run_validations_no_integrations_when_all_deleted(
        self, mock_run_integration: Mock, mock_storage: Mock
    ) -> None:
        """When all integrations are deleted, no integration validations run."""
        self._user_service_mock.warehouses = [_DELETED_WAREHOUSE, _WAREHOUSE_SNAKE_CASE_DELETED]
        self._user_service_mock.bi_containers = []
        self._user_service_mock.etl_containers = []

        self._service.run_validations(dc_id=_DC_UUID)

        mock_run_integration.assert_not_called()
        mock_storage.assert_called_once()


class SupportedValidationsIncludeInternalTest(TestCase):
    def setUp(self) -> None:
        self._mc_client = Mock()
        self._mc_client.return_value.get_supported_validations_v2.supported_validations = []
        self._service = CollectorValidationService(
            config=_SAMPLE_CONFIG,
            mc_client=self._mc_client,
            command_name="test",
            user_service=Mock(autospec=UserService),
        )

    def _sent_query(self) -> str:
        return str(self._mc_client.call_args.kwargs["query"])

    def test_include_internal_sent_when_requested(self) -> None:
        self._service._get_supported_validations(
            dc_uuid=_DC_UUID,
            connection_type="databricks-sql-warehouse",
            only_periodic=False,
            include_internal=True,
        )

        self.assertIn("includeInternal: true", self._sent_query())

    def test_include_internal_omitted_by_default(self) -> None:
        self._service._get_supported_validations(
            dc_uuid=_DC_UUID, connection_type="databricks-sql-warehouse", only_periodic=False
        )

        self.assertNotIn("includeInternal", self._sent_query())

    def _run_connection_validators(self, include_internal: bool) -> int:
        failures, _ = self._service._run_connection_validators(
            dc_uuid=_DC_UUID,
            name="dbx",
            connection_type="databricks-sql-warehouse",
            connection_uuid=str(uuid.uuid4()),
            only_periodic=False,
            include_internal=include_internal,
        )
        return failures

    def test_internal_validations_requested_only_with_flag(self) -> None:
        for include_internal in [True, False]:
            with self.subTest(include_internal=include_internal):
                self._mc_client.reset_mock()

                self._run_connection_validators(include_internal=include_internal)

                self.assertEqual("includeInternal: true" in self._sent_query(), include_internal)

    @patch.object(CollectorValidationService, "_run_storage_access_validation", return_value=0)
    def test_run_validations_passes_flag_to_query(self, mock_storage: Mock) -> None:
        user_service = self._service._user_service
        user_service.get_collector.return_value = Box({"uuid": _DC_UUID})
        user_service.warehouses = [_ACTIVE_WAREHOUSE]
        user_service.bi_containers = []
        user_service.etl_containers = []

        self._service.run_validations(dc_id=_DC_UUID, include_internal=True)

        self.assertIn("includeInternal: true", self._sent_query())

    def test_onboarding_does_not_request_internal_validations(self) -> None:
        self._service._validate_credentials(
            dc_uuid=_DC_UUID,
            connection_type="databricks-sql-warehouse",
            validation_variables={},
            query="query q { x }",
            operation_name="testFoo",
        )

        self.assertNotIn("includeInternal", str(self._mc_client.call_args_list[0].kwargs["query"]))

    def test_internal_validation_failure_counts(self) -> None:
        self._mc_client.side_effect = [
            Box(
                {
                    "get_supported_validations_v2": {
                        "supported_validations": [
                            {
                                "name": "validate_result_shape_duplicate_column_names",
                                "periodic_validation": False,
                            }
                        ]
                    }
                }
            ),
            Box(
                {
                    "test_existing_connection_v2": {
                        "success": False,
                        "warnings": [],
                        "errors": [{"cause": "ArrowInvalid"}],
                    }
                }
            ),
        ]

        failures = self._run_connection_validators(include_internal=True)

        self.assertEqual(failures, 1)
        self.assertEqual(self._mc_client.call_count, 2)
        first_query = str(self._mc_client.call_args_list[0].kwargs["query"])
        self.assertIn("includeInternal: true", first_query)


class RunValidationsCommandTest(TestCase):
    @patch("montecarlodata.collector.commands.create_mc_client")
    @patch("montecarlodata.collector.commands.CollectorValidationService")
    def test_include_internal_flag(self, service_class_mock: Mock, _: Mock) -> None:
        run_mock = service_class_mock.return_value.run_validations
        run_mock.return_value = 0
        for args, expected in [([], False), (["--include-internal"], True)]:
            with self.subTest(args=args):
                result = CliRunner().invoke(
                    run_validations,
                    obj={"config": _SAMPLE_CONFIG},
                    args=["--collector-id", _DC_UUID, *args],
                )

                self.assertEqual(result.exit_code, 0, result.output)
                self.assertIs(run_mock.call_args.kwargs["include_internal"], expected)

    def test_include_internal_hidden_from_help(self) -> None:
        result = CliRunner().invoke(run_validations, args=["--help"])

        self.assertNotIn("internal", result.output.lower())
