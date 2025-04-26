from unittest import TestCase
from unittest.mock import Mock, patch

from montecarlodata.common.data import ValidationResult
from montecarlodata.common.user import UserService
from montecarlodata.integrations.onboarding.etl.airflow import AirflowOnboardingService
from montecarlodata.integrations.onboarding.fields import (
    EXPECTED_ADD_ETL_CONNECTION_RESPONSE_FIELD,
    EXPECTED_TEST_AIRFLOW_RESPONSE_FIELD,
)
from montecarlodata.queries.onboarding import (
    ADD_ETL_CONNECTION_MUTATION,
    TEST_AIRFLOW_CRED_MUTATION,
)
from montecarlodata.utils import AwsClientWrapper, GqlWrapper
from tests.test_common_user import _SAMPLE_CONFIG


class AirflowOnboardingTest(TestCase):
    def setUp(self) -> None:
        self._user_service_mock = Mock(autospec=UserService)
        self._request_wrapper_mock = Mock(autospec=GqlWrapper)
        self._aws_wrapper_mock = Mock(autospec=AwsClientWrapper)

        self._service = AirflowOnboardingService(
            _SAMPLE_CONFIG,
            command_name="test",
            request_wrapper=self._request_wrapper_mock,
            aws_wrapper=self._aws_wrapper_mock,
            user_service=self._user_service_mock,
        )
        self._service._disable_handle_errors = True

    @patch.object(AirflowOnboardingService, "_validate_connection")
    @patch("montecarlodata.integrations.onboarding.base.prompt_connection")
    def test_onboard_airflow(self, prompt_mock, validation_mock):
        validation_mock.return_value = ValidationResult(has_warnings=False, credentials_key="path")

        etl_name = "airflow_1"
        self._service.onboard_airflow(hostName="aws.com", etl_name=etl_name)

        validation_mock.assert_called_once_with(
            query=TEST_AIRFLOW_CRED_MUTATION,
            response_field=EXPECTED_TEST_AIRFLOW_RESPONSE_FIELD,
            hostName="aws.com",
        )

        self._request_wrapper_mock.make_request_v2.assert_called_with(
            query=ADD_ETL_CONNECTION_MUTATION,
            operation=EXPECTED_ADD_ETL_CONNECTION_RESPONSE_FIELD,
            service="onboarding_service",
            variables={
                "key": "path",
                "name": etl_name,
                "connectionType": "airflow",
            },
        )
