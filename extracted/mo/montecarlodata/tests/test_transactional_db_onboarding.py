from unittest import TestCase
from unittest.mock import Mock, patch

from pycarlo.core import Client, Session

from montecarlodata.common.user import UserService
from montecarlodata.integrations.onboarding.transactional.transactional_db import (
    TransactionalOnboardingService,
)
from montecarlodata.utils import GqlWrapper
from tests.test_base_onboarding import _SAMPLE_BASE_OPTIONS
from tests.test_common_user import _SAMPLE_CONFIG


class TransactionalOnboardingTest(TestCase):
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
    def test_generic_transactional_db_flow(self, test_new_credentials_mock):
        expected_options = {
            **{
                "connection_type": "transactional-db",
                "warehouse_type": "transactional-db",
            },
            **_SAMPLE_BASE_OPTIONS,
        }

        test_new_credentials_mock.return_value = "tmp-string"

        self._service.onboard_transactional_db(**_SAMPLE_BASE_OPTIONS)
        test_new_credentials_mock.assert_called_once_with(**expected_options)
