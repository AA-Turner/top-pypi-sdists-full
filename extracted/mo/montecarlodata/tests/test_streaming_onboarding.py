import uuid
from unittest import TestCase
from unittest.mock import Mock

from box import Box
from pycarlo.core import Client

from montecarlodata.collector.validation import CollectorValidationService
from montecarlodata.common.data import MonolithResponse
from montecarlodata.common.user import UserService
from montecarlodata.integrations.onboarding.fields import (
    EXPECTED_ADD_CONFLUENT_CLUSTER_CONNECTION_RESPONSE_FIELD,
    EXPECTED_ADD_STREAMING_SYSTEM_RESPONSE_FIELD,
)
from montecarlodata.integrations.onboarding.streaming.streamings import (
    StreamingOnboardingService,
)
from montecarlodata.queries.onboarding import (
    ADD_STREAMING_CLUSTER_CONNECTION_MUTATION,
    ADD_STREAMING_SYSTEM_MUTATION,
)
from montecarlodata.utils import AwsClientWrapper, GqlWrapper
from tests.test_common_user import _SAMPLE_CONFIG


class StreamingOnboardingTest(TestCase):
    _EXPECTED_NEW_CONNECTION_RESPONSE = {
        "connection": {
            "id": "9511",
            "type": "CONFLUENT_KAFKA_CONNECT",
            "uuid": "de7b4ebb-1574-45c1-9433-07fae8b3fc9f",
            "streamingCluster": {
                "uuid": "c5c9f51d-06d6-47f6-90c1-27fda4160dda",
                "clusterType": "CONFLUENT_KAFKA_CONNECT",
                "externalClusterId": "test_cluster_id",
                "streamingSystemUuid": "6f5d117f-e644-41b4-aa60-f593c0f0dfd1",
            },
        }
    }

    def setUp(self) -> None:
        self._user_service_mock = Mock(autospec=UserService)
        self._request_wrapper_mock = Mock(autospec=GqlWrapper)
        self._aws_wrapper_mock = Mock(autospec=AwsClientWrapper)
        self._mc_client_mock = Mock(autospec=Client)
        self._validation_service_mock = Mock(autospec=CollectorValidationService)

        self._service = StreamingOnboardingService(
            _SAMPLE_CONFIG,
            command_name="test",
            mc_client=self._mc_client_mock,
            request_wrapper=self._request_wrapper_mock,
            aws_wrapper=self._aws_wrapper_mock,
            user_service=self._user_service_mock,
        )
        self._service._validation_service = self._validation_service_mock

    def test_create_streaming_system(self):
        self._request_wrapper_mock.make_request_v2.return_value = MonolithResponse(
            data=Box(
                {
                    "streamingSystem": {
                        "id": "1",
                        "createdTime": "2023-11-14T23:41:05.465076+00:00",
                        "updatedTime": "2023-11-14T23:41:05.465093+00:00",
                        "name": "test system 2",
                        "type": "CONFLUENT_CLOUD",
                        "accountUuid": "a5cbd8cc-8e91-4a41-aca4-4bf5bd320578",
                        "dcId": "c16e3efc-0d54-4088-9514-372a38506e62",
                        "deletedAt": None,
                        "uuid": "6f5d117f-e644-41b4-aa60-f593c0f0dfd1",
                    }
                }
            ),
            errors=[],
        )

        system_type = "confluent-cloud"
        system_name = "test confluent system"
        dc_id = str(uuid.uuid4())
        self._service.create_streaming_system(system_type, system_name, dc_id)

        self._request_wrapper_mock.make_request_v2.assert_called_once_with(
            query=ADD_STREAMING_SYSTEM_MUTATION,
            operation=EXPECTED_ADD_STREAMING_SYSTEM_RESPONSE_FIELD,
            service="streaming_onboarding_service",
            variables=dict(
                streaming_system_type=system_type,
                streaming_system_name=system_name,
                dc_id=dc_id,
            ),
        )

    def test_onboard_streaming_cluster_connection_with_key(self):
        self._request_wrapper_mock.make_request_v2.return_value = MonolithResponse(
            data=Box(self._EXPECTED_NEW_CONNECTION_RESPONSE), errors=[]
        )

        self._service.onboard_streaming_cluster_connection(
            connection_type="confluent-kafka-connect",
            key="tmp/mykey",
            dc_id="c16e3efc-0d54-4088-9514-372a38506e62",
            new_streaming_system_name="test",
            new_streaming_system_type="confluent-cloud",
            new_cluster_id="test_cluster_id",
            new_cluster_name="test_cluster_name",
        )

        self._request_wrapper_mock.make_request_v2.assert_called_once_with(
            query=ADD_STREAMING_CLUSTER_CONNECTION_MUTATION,
            operation=EXPECTED_ADD_CONFLUENT_CLUSTER_CONNECTION_RESPONSE_FIELD,
            service="streaming_onboarding_service",
            variables=dict(
                connection_type="confluent-kafka-connect",
                key="tmp/mykey",
                dc_id="c16e3efc-0d54-4088-9514-372a38506e62",
                new_streaming_system_name="test",
                new_streaming_system_type="confluent-cloud",
                new_cluster_id="test_cluster_id",
                new_cluster_name="test_cluster_name",
                new_cluster_type="confluent-kafka-connect",
            ),
        )
        self._validation_service_mock.test_new_credentials.assert_not_called()

    def test_onboard_streaming_cluster_connection_without_key(self):
        self._request_wrapper_mock.make_request_v2.return_value = MonolithResponse(
            data=Box(self._EXPECTED_NEW_CONNECTION_RESPONSE), errors=[]
        )
        self._validation_service_mock.test_new_credentials.return_value = "tmp/mykey"

        self._service.onboard_streaming_cluster_connection(
            connection_type="confluent-kafka-connect",
            api_key="api_key",
            secret="secret",
            url="http://confluent.com",
            dc_id="c16e3efc-0d54-4088-9514-372a38506e62",
            new_streaming_system_name="test",
            new_streaming_system_type="confluent-cloud",
            new_cluster_id="test_cluster_id",
            new_cluster_name="test_cluster_name",
        )

        self._request_wrapper_mock.make_request_v2.assert_called_once_with(
            query=ADD_STREAMING_CLUSTER_CONNECTION_MUTATION,
            operation=EXPECTED_ADD_CONFLUENT_CLUSTER_CONNECTION_RESPONSE_FIELD,
            service="streaming_onboarding_service",
            variables=dict(
                connection_type="confluent-kafka-connect",
                key="tmp/mykey",
                dc_id="c16e3efc-0d54-4088-9514-372a38506e62",
                new_streaming_system_name="test",
                new_streaming_system_type="confluent-cloud",
                new_cluster_id="test_cluster_id",
                new_cluster_name="test_cluster_name",
                new_cluster_type="confluent-kafka-connect",
                # following 3 only carried but not used in the call at all.
                api_key="api_key",
                secret="secret",
                url="http://confluent.com",
            ),
        )
        self._validation_service_mock.test_new_credentials.assert_called_once_with(
            connection_type="confluent-kafka-connect",
            dc_id="c16e3efc-0d54-4088-9514-372a38506e62",
            cluster="test_cluster_id",
            api_key="api_key",
            secret="secret",
            confluent_env=None,
            url="http://confluent.com",
        )
