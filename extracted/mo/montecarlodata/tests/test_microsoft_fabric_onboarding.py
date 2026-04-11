from unittest import TestCase
from unittest.mock import Mock, patch

from click.testing import CliRunner
from pycarlo.core import Client, Session

from montecarlodata.common.user import UserService
from montecarlodata.integrations.commands import add_microsoft_fabric
from montecarlodata.integrations.onboarding.fields import MICROSOFT_FABRIC_CONNECTION_TYPE
from montecarlodata.integrations.onboarding.transactional.transactional_db import (
    TransactionalOnboardingService,
)
from montecarlodata.utils import GqlWrapper
from tests.test_base_onboarding import _SAMPLE_BASE_OPTIONS
from tests.test_common_user import _SAMPLE_CONFIG

_SAMPLE_HOST = "sample-workspace.datawarehouse.fabric.microsoft.com"
_SAMPLE_DATABASE = "sample_db"
_SAMPLE_CLIENT_ID = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
_SAMPLE_CLIENT_SECRET = "super-secret"
_SAMPLE_TENANT_ID = "ffffffff-gggg-hhhh-iiii-jjjjjjjjjjjj"
_SAMPLE_WAREHOUSE_NAME = "my-fabric-warehouse"


class MicrosoftFabricOnboardingTest(TestCase):
    def setUp(self) -> None:
        self._user_service_mock = Mock(autospec=UserService)
        self._request_wrapper_mock = Mock(autospec=GqlWrapper)
        self._mc_client = Client(
            session=Session(
                endpoint=_SAMPLE_CONFIG.mcd_api_endpoint,
                mcd_id=_SAMPLE_CONFIG.mcd_id,
                mcd_token=_SAMPLE_CONFIG.mcd_token,
            )
        )
        self._service = TransactionalOnboardingService(
            _SAMPLE_CONFIG,
            command_name="test",
            request_wrapper=self._request_wrapper_mock,
            mc_client=self._mc_client,
            user_service=self._user_service_mock,
        )

    @patch.object(TransactionalOnboardingService, "test_new_credentials")
    def test_microsoft_fabric_promoted_connection_type(self, test_new_credentials_mock):
        """Microsoft Fabric is a promoted subtype — connection_type and warehouse_type should be
        'microsoft-fabric', not the generic 'transactional-db'."""
        test_new_credentials_mock.return_value = "tmp-string"

        self._service.onboard_transactional_db(
            dbType=MICROSOFT_FABRIC_CONNECTION_TYPE,
            host=_SAMPLE_HOST,
            dbName=_SAMPLE_DATABASE,
            client_id=_SAMPLE_CLIENT_ID,
            client_secret=_SAMPLE_CLIENT_SECRET,
            tenant_id=_SAMPLE_TENANT_ID,
            **_SAMPLE_BASE_OPTIONS,
        )

        call_kwargs = test_new_credentials_mock.call_args[1]
        self.assertEqual(call_kwargs["connection_type"], MICROSOFT_FABRIC_CONNECTION_TYPE)
        self.assertEqual(call_kwargs["warehouse_type"], MICROSOFT_FABRIC_CONNECTION_TYPE)

    @patch.object(TransactionalOnboardingService, "test_new_credentials")
    def test_microsoft_fabric_credentials_passed_through(self, test_new_credentials_mock):
        """Service principal credentials are forwarded as client_id, client_secret,
        tenant_id — not mapped to the Salesforce consumer_key / domain fields."""
        test_new_credentials_mock.return_value = "tmp-string"

        self._service.onboard_transactional_db(
            dbType=MICROSOFT_FABRIC_CONNECTION_TYPE,
            host=_SAMPLE_HOST,
            dbName=_SAMPLE_DATABASE,
            client_id=_SAMPLE_CLIENT_ID,
            client_secret=_SAMPLE_CLIENT_SECRET,
            tenant_id=_SAMPLE_TENANT_ID,
            **_SAMPLE_BASE_OPTIONS,
        )

        call_kwargs = test_new_credentials_mock.call_args[1]
        self.assertEqual(call_kwargs["client_id"], _SAMPLE_CLIENT_ID)
        self.assertEqual(call_kwargs["client_secret"], _SAMPLE_CLIENT_SECRET)
        self.assertEqual(call_kwargs["tenant_id"], _SAMPLE_TENANT_ID)

    @patch("montecarlodata.integrations.commands.TransactionalOnboardingService")
    @patch("montecarlodata.integrations.commands.create_mc_client")
    def test_add_microsoft_fabric_cli_command(self, create_mc_client_mock, service_class_mock):
        """CLI command passes all options to onboard_transactional_db with correct kwarg names."""
        create_mc_client_mock.return_value = self._mc_client
        onboard_mock = service_class_mock.return_value.onboard_transactional_db

        runner = CliRunner()
        result = runner.invoke(
            add_microsoft_fabric,
            obj={"config": _SAMPLE_CONFIG},
            args=[
                "--host",
                _SAMPLE_HOST,
                "--database",
                _SAMPLE_DATABASE,
                "--client-id",
                _SAMPLE_CLIENT_ID,
                "--client-secret",
                _SAMPLE_CLIENT_SECRET,
                "--tenant-id",
                _SAMPLE_TENANT_ID,
                "--name",
                _SAMPLE_WAREHOUSE_NAME,
            ],
        )

        self.assertEqual(result.exit_code, 0, result.output)
        onboard_mock.assert_called_once()
        call_kwargs = onboard_mock.call_args[1]
        self.assertEqual(call_kwargs["dbType"], MICROSOFT_FABRIC_CONNECTION_TYPE)
        self.assertEqual(call_kwargs["warehouseName"], _SAMPLE_WAREHOUSE_NAME)
        self.assertEqual(call_kwargs["dbName"], _SAMPLE_DATABASE)
        self.assertEqual(call_kwargs["client_id"], _SAMPLE_CLIENT_ID)
        self.assertEqual(call_kwargs["client_secret"], _SAMPLE_CLIENT_SECRET)
        self.assertEqual(call_kwargs["tenant_id"], _SAMPLE_TENANT_ID)
