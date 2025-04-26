import base64
from unittest import TestCase
from unittest.mock import Mock, patch

from montecarlodata.common.user import UserService
from montecarlodata.integrations.onboarding.bi.reports import ReportsOnboardingService
from montecarlodata.queries.onboarding import (
    ADD_BI_CONNECTION_MUTATION,
    TEST_LOOKER_GIT_CLONE_CRED_MUTATION,
    TEST_LOOKER_METADATA_CRED_MUTATION,
    TEST_POWER_BI_CRED_MUTATION,
    TEST_TABLEAU_CRED_MUTATION,
)
from montecarlodata.utils import AwsClientWrapper, GqlWrapper
from tests.test_base_onboarding import _SAMPLE_BASE_OPTIONS
from tests.test_common_user import _SAMPLE_CONFIG

_SAMPLE_OPTIONS = {"foo": "bar"}


class ReportOnboardingTest(TestCase):
    def setUp(self) -> None:
        self._user_service_mock = Mock(autospec=UserService)
        self._request_wrapper_mock = Mock(autospec=GqlWrapper)
        self._aws_wrapper_mock = Mock(autospec=AwsClientWrapper)

        self._service = ReportsOnboardingService(
            _SAMPLE_CONFIG,
            command_name="test",
            request_wrapper=self._request_wrapper_mock,
            aws_wrapper=self._aws_wrapper_mock,
            user_service=self._user_service_mock,
        )

    @patch.object(ReportsOnboardingService, "onboard")
    def test_tableau_flow(self, onboard_mock):
        self._service.onboard_tableau(**_SAMPLE_BASE_OPTIONS)
        onboard_mock.assert_called_once_with(
            validation_query=TEST_TABLEAU_CRED_MUTATION,
            connection_query=ADD_BI_CONNECTION_MUTATION,
            validation_response="testTableauCredentials",
            connection_response="addBiConnection",
            connection_type="tableau",
            warehouse_type="tableau",
            **_SAMPLE_BASE_OPTIONS,
        )

    @patch.object(ReportsOnboardingService, "onboard")
    def test_looker_metadata_flow(self, onboard_mock):
        self._service.onboard_looker_metadata(**_SAMPLE_BASE_OPTIONS)
        onboard_mock.assert_called_once_with(
            validation_query=TEST_LOOKER_METADATA_CRED_MUTATION,
            connection_query=ADD_BI_CONNECTION_MUTATION,
            validation_response="testLookerCredentials",
            connection_response="addBiConnection",
            connection_type="looker",
            warehouse_type="looker",
            **_SAMPLE_BASE_OPTIONS,
        )

    @patch.object(ReportsOnboardingService, "onboard")
    @patch("montecarlodata.integrations.onboarding.bi.reports.read_as_base64")
    def test_looker_git_flow(self, read_as_base64_mock, onboard_mock):
        file_path, service_json = "foo", "bar"
        base64_key = base64.b64encode(service_json.encode("utf-8"))

        input_options = {"ssh_key": file_path, **_SAMPLE_BASE_OPTIONS}
        expected_options = {**{"ssh_key": base64_key.decode()}, **_SAMPLE_BASE_OPTIONS}

        read_as_base64_mock.return_value = base64_key

        self._service.onboard_looker_git(**input_options)
        read_as_base64_mock.assert_called_once_with(file_path)
        onboard_mock.assert_called_once_with(
            validation_query=TEST_LOOKER_GIT_CLONE_CRED_MUTATION,
            connection_query=ADD_BI_CONNECTION_MUTATION,
            validation_response="testLookerGitCloneCredentials",
            connection_response="addBiConnection",
            connection_type="looker-git-clone",
            warehouse_type="looker",
            **expected_options,
        )

    @patch.object(ReportsOnboardingService, "onboard")
    def test_power_bi_flow(self, onboard_mock):
        self._service.onboard_power_bi(**_SAMPLE_BASE_OPTIONS)
        onboard_mock.assert_called_once_with(
            validation_query=TEST_POWER_BI_CRED_MUTATION,
            connection_query=ADD_BI_CONNECTION_MUTATION,
            validation_response="testPowerBiCredentials",
            connection_response="addBiConnection",
            connection_type="power-bi",
            warehouse_type="power-bi",
            **_SAMPLE_BASE_OPTIONS,
        )
