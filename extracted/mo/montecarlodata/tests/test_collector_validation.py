import uuid
from unittest import TestCase
from unittest.mock import Mock, patch

from box import Box
from pycarlo.core import Client, Session

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
