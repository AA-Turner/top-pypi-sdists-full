import os
import pathlib
from typing import Callable, Dict
from unittest import TestCase
from unittest.mock import Mock

import click
from box import Box

from montecarlodata.common.common import read_as_json_string
from montecarlodata.common.data import MonolithResponse
from montecarlodata.common.user import UserService
from montecarlodata.integrations.onboarding.data_lake.events import (
    EventsOnboardingService,
)
from montecarlodata.integrations.onboarding.fields import (
    EXPECTED_CONFIGURE_METADATA_EVENTS_GQL_RESPONSE_FIELD,
    EXPECTED_CONFIGURE_QUERY_LOG_EVENTS_GQL_RESPONSE_FIELD,
    EXPECTED_DISABLE_METADATA_EVENTS_GQL_RESPONSE_FIELD,
    EXPECTED_DISABLE_QUERY_LOG_EVENTS_GQL_RESPONSE_FIELD,
)
from montecarlodata.queries.onboarding import (
    CONFIGURE_METADATA_EVENTS_MUTATION,
    CONFIGURE_QUERY_LOG_EVENTS_MUTATION,
    DISABLE_METADATA_EVENTS_MUTATION,
    DISABLE_QUERY_LOG_EVENTS_MUTATION,
)
from montecarlodata.utils import AwsClientWrapper, GqlWrapper
from tests.test_common_user import _SAMPLE_CONFIG


class EventsOnboardingTest(TestCase):
    def setUp(self) -> None:
        self._user_service_mock = Mock(autospec=UserService)
        self._request_wrapper_mock = Mock(autospec=GqlWrapper)
        self._aws_wrapper_mock = Mock(autospec=AwsClientWrapper)

        self._service = EventsOnboardingService(
            _SAMPLE_CONFIG,
            command_name="test",
            request_wrapper=self._request_wrapper_mock,
            aws_wrapper=self._aws_wrapper_mock,
            user_service=self._user_service_mock,
        )

    def test_configure_metadata_events(self):
        kwargs = {"connection_type": "glue", "name": "warehouse"}

        self._test(
            func=self._service.configure_metadata_events,
            kwargs=kwargs,
            expected_mutation=CONFIGURE_METADATA_EVENTS_MUTATION,
            expected_operation=EXPECTED_CONFIGURE_METADATA_EVENTS_GQL_RESPONSE_FIELD,
            expected_variables=kwargs,
        )

    def test_configure_query_log_events(self):
        mapping_file = os.path.join(pathlib.Path(__file__).parent.resolve(), "sample_mapping.json")
        kwargs = {
            "connection_type": "hive-s3",
            "format_type": "custom",
            "location": "foo",
            "source_format": "bar",
            "mapping_file": mapping_file,
            "name": "warehouse",
        }

        expected_variables = {**kwargs, "mapping": read_as_json_string(mapping_file)}
        expected_variables.pop("mapping_file")

        self._test(
            func=self._service.configure_query_log_events,
            kwargs=kwargs,
            expected_mutation=CONFIGURE_QUERY_LOG_EVENTS_MUTATION,
            expected_operation=EXPECTED_CONFIGURE_QUERY_LOG_EVENTS_GQL_RESPONSE_FIELD,
            expected_variables=expected_variables,
        )

    def test_disable_metadata_events(self):
        kwargs = {"name": "warehouse"}

        self._test(
            func=self._service.disable_metadata_events,
            kwargs=kwargs,
            expected_mutation=DISABLE_METADATA_EVENTS_MUTATION,
            expected_operation=EXPECTED_DISABLE_METADATA_EVENTS_GQL_RESPONSE_FIELD,
            expected_variables=kwargs,
        )

    def test_disable_query_log_events(self):
        kwargs = {"name": "warehouse"}

        self._test(
            func=self._service.disable_query_log_events,
            kwargs=kwargs,
            expected_mutation=DISABLE_QUERY_LOG_EVENTS_MUTATION,
            expected_operation=EXPECTED_DISABLE_QUERY_LOG_EVENTS_GQL_RESPONSE_FIELD,
            expected_variables=kwargs,
        )

    def _test(
        self,
        func: Callable,
        kwargs: Dict,
        expected_mutation: str,
        expected_operation: str,
        expected_variables: Dict,
    ):
        # test a successful GraphQL response
        self._verify_graphql_request(
            func=func,
            kwargs=kwargs,
            expected_mutation=expected_mutation,
            expected_operation=expected_operation,
            expected_variables=expected_variables,
            success=True,
        )

        # test a failed GraphQL response
        self._verify_graphql_request(
            func=func,
            kwargs=kwargs,
            expected_mutation=expected_mutation,
            expected_operation=expected_operation,
            expected_variables=expected_variables,
            success=False,
        )

    def _verify_graphql_request(
        self,
        func: Callable,
        kwargs: Dict,
        success: bool,
        expected_mutation: str,
        expected_operation: str,
        expected_variables: Dict,
    ):
        # given
        self._request_wrapper_mock.make_request_v2.return_value = MonolithResponse(
            data=Box({"success": success})
        )

        # when
        if success:
            func(**kwargs)
        else:
            self.assertRaises(click.exceptions.Abort, func, **kwargs)

        # then
        self._request_wrapper_mock.make_request_v2.assert_called_with(
            query=expected_mutation,
            operation=expected_operation,
            service="events_onboarding_service",
            variables=expected_variables,
        )
